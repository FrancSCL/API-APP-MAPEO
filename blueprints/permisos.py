"""
Sistema de permisos LH Mapeo — replica el patron del Portal Web.

Modelo:
- Cada usuario tiene un perfil (1=LECTOR, 2=EDITOR, 3=SUPER).
- Cada perfil trae por defecto un set de permisos (PERFIL_PERMISOS).
- Overrides individuales van en usuario_pivot_permiso_usuario (mismo mecanismo del Portal).
- permisos_efectivos(uid) = permisos_del_perfil ∪ overrides.
- SUPER (perfil=3) bypass total → {"*"}.

Enforcement:
- @require_permission("mapeo.catastro.eliminar") en endpoints sensibles.
- 403 si el usuario no tiene el permiso.
- El JWT trae "permisos" (list) para verificacion rapida sin ir a BD.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from utils.db import get_db_connection

# ID de esta app en general_dim_app (LH MAPEO = 5)
APP_ID = 5

# Receta de permisos por perfil. Al cambiar esto = deploy.
# La logica del Portal es: PERFIL_PERMISOS[id_perfil] = {set de codigos}.
#
# Contexto Mapeo (distinto del Portal): la mayoria de peones/mapeadores del
# campo tienen perfil LECTOR (1). Los damos operar en Mapeo pero NO eliminar.
# EDITOR (2) = capataz/supervisor: agrega eliminar catastro.
# SUPER (3) = admin TI (Francisco): bypass total.
PERFIL_PERMISOS = {
    1: {  # LECTOR — peon/mapeador: opera pero NO elimina
        "mapeo.catastro.ver",
        "mapeo.catastro.crear",
        "mapeo.catastro.editar",
        "mapeo.mapeo.ver",
        "mapeo.mapeo.registrar",
        "mapeo.mapeo.editar",
        "mapeo.mapeo.finalizar",
    },
    2: {  # EDITOR — capataz/supervisor: todo lo anterior + eliminar catastro
        "mapeo.catastro.ver",
        "mapeo.catastro.crear",
        "mapeo.catastro.editar",
        "mapeo.catastro.eliminar",
        "mapeo.mapeo.ver",
        "mapeo.mapeo.registrar",
        "mapeo.mapeo.editar",
        "mapeo.mapeo.finalizar",
    },
    3: {  # SUPER — admin TI: bypass total
        "*",
    },
}


def permisos_efectivos(id_usuario: str) -> set:
    """
    Retorna el set de codigos de permiso efectivos del usuario.
    - Base: PERFIL_PERMISOS[id_perfil]
    - Union con overrides individuales de usuario_pivot_permiso_usuario
    - SUPER retorna {"*"} (bypass).
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Perfil del usuario
    cursor.execute("SELECT id_perfil FROM general_dim_usuario WHERE id=%s", (id_usuario,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return set()

    id_perfil = row["id_perfil"]

    # SUPER bypass
    if id_perfil == 3:
        cursor.close()
        conn.close()
        return {"*"}

    # 2. Base del perfil
    permisos = set(PERFIL_PERMISOS.get(id_perfil, set()))

    # 3. Overrides individuales (solo permisos de la app 5)
    cursor.execute(
        """
        SELECT p.id
        FROM usuario_pivot_permiso_usuario pu
        JOIN usuario_dim_permiso p ON pu.id_permiso = p.id
        WHERE pu.id_usuario = %s AND p.id_app = %s AND p.id_estado = 1
        """,
        (id_usuario, APP_ID),
    )
    for r in cursor.fetchall():
        permisos.add(r["id"])

    cursor.close()
    conn.close()
    return permisos


def tiene_permiso(permisos: set, codigo: str) -> bool:
    """True si el set contiene '*' o el codigo exacto."""
    return "*" in permisos or codigo in permisos


def require_permission(codigo: str):
    """
    Decorator: exige un permiso especifico. Se apoya en el claim 'permisos' del JWT.
    Fallback: si el JWT no trae permisos (token viejo), consulta BD.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            permisos = set(claims.get("permisos") or [])
            if not permisos:
                # Fallback para tokens antiguos que no tienen claim 'permisos'
                uid = get_jwt_identity()
                permisos = permisos_efectivos(uid)
            if not tiene_permiso(permisos, codigo):
                return jsonify({"error": f"Falta permiso: {codigo}"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
