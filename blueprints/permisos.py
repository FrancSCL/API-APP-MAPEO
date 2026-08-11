"""
Sistema de permisos LH Mapeo (id_app=5) — usa el modelo RBAC nuevo del Portal.

Fuentes:
- users_dim_rol            : roles por app (id_app=5)
- users_dim_permiso        : catalogo de permisos (formato mapeo.<modulo>.<submodulo>.<accion>)
- users_pivot_rol_usuario  : rol asignado a usuario
- users_pivot_rol_permiso  : que permisos trae cada rol
- users_pivot_permiso_usuario : override individual (otorgado=1) para sumar permisos

Rol con es_bypass=1 → retorna {"*"} (Admin Mapeo).

Enforcement:
- @require_permission("mapeo.catastro.plantas.eliminar") en endpoints sensibles.
- Se apoya en el claim 'permisos' del JWT. Fallback a BD si el token no lo trae.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from utils.db import get_db_connection

APP_ID = 5


def permisos_efectivos(id_usuario: str) -> set:
    """
    Retorna set de codigos de permiso efectivos del usuario para app_id=5.
    Si alguno de sus roles tiene es_bypass=1, retorna {"*"}.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    permisos = set()

    # 1. Roles del usuario en Mapeo — bypass corta
    cursor.execute(
        """SELECT r.id, r.es_bypass FROM users_pivot_rol_usuario ru
            JOIN users_dim_rol r ON ru.id_rol = r.id
            WHERE ru.id_usuario = %s AND r.id_app = %s AND r.activo = 1""",
        (id_usuario, APP_ID),
    )
    rol_ids = []
    for r in cursor.fetchall():
        if r["es_bypass"] == 1:
            cursor.close()
            conn.close()
            return {"*"}
        rol_ids.append(r["id"])

    # 2. Permisos que traen esos roles (via pivot rol_permiso)
    if rol_ids:
        placeholders = ",".join(["%s"] * len(rol_ids))
        cursor.execute(
            f"""SELECT DISTINCT rp.id_permiso FROM users_pivot_rol_permiso rp
                 JOIN users_dim_permiso p ON rp.id_permiso = p.id
                 WHERE rp.id_rol IN ({placeholders}) AND p.activo = 1""",
            rol_ids,
        )
        permisos.update(r["id_permiso"] for r in cursor.fetchall())

    # 3. Overrides individuales (otorgado=1)
    cursor.execute(
        """SELECT pu.id_permiso FROM users_pivot_permiso_usuario pu
            JOIN users_dim_permiso p ON pu.id_permiso = p.id
            WHERE pu.id_usuario = %s AND p.id_app = %s AND pu.otorgado = 1 AND p.activo = 1""",
        (id_usuario, APP_ID),
    )
    permisos.update(r["id_permiso"] for r in cursor.fetchall())

    cursor.close()
    conn.close()
    return permisos


def tiene_permiso(permisos: set, codigo: str) -> bool:
    return "*" in permisos or codigo in permisos


def require_permission(codigo: str):
    """Decorator: exige un permiso especifico via claim 'permisos' del JWT."""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            permisos = set(claims.get("permisos") or [])
            if not permisos:
                uid = get_jwt_identity()
                permisos = permisos_efectivos(uid)
            if not tiene_permiso(permisos, codigo):
                return jsonify({"error": f"Falta permiso: {codigo}"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
