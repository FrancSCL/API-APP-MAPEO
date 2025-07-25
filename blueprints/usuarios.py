from flask import Blueprint, jsonify, request
from utils.db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt
from datetime import date
import uuid


usuarios_bp = Blueprint('usuarios_bp', __name__)

def verificar_admin(usuario_id):
    """Verifica si el usuario tiene perfil de administrador (id_perfil = 3)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_perfil FROM general_dim_usuario WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario and usuario['id_perfil'] == 3

# 🔹 Obtener todos los usuarios (solo admin)
@usuarios_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    usuario_id = get_jwt_identity()
    if not verificar_admin(usuario_id):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
    SELECT 
        u.id, u.usuario, u.correo, u.nombre, u.apellido_paterno, u.apellido_materno, 
        u.id_sucursalactiva, u.id_estado, u.id_rol, u.id_perfil, u.fecha_creacion, s.nombre AS nombre_sucursal
    FROM general_dim_usuario u
    LEFT JOIN general_dim_sucursal s ON u.id_sucursalactiva = s.id
""")

        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
# 🔹 Obtener sucursal activa del usuario logueado
@usuarios_bp.route('/sucursal', methods=['GET'])
@jwt_required()
def obtener_sucursal_usuario():
    try:
        usuario_id = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_sucursalactiva FROM general_dim_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if not usuario or not usuario['id_sucursalactiva']:
            return jsonify({"error": "Usuario no encontrado o sin sucursal asignada"}), 404

        return jsonify({"id_sucursal": usuario['id_sucursalactiva']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Actualizar la sucursal activa del usuario logueado
@usuarios_bp.route('/sucursal-activa', methods=['POST'])
@jwt_required()
def actualizar_sucursal_activa():
    try:
        usuario_id = get_jwt_identity()
        data = request.json
        nueva_sucursal = data.get("id_sucursal")

        if not nueva_sucursal:
            return jsonify({"error": "Sucursal no especificada"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

            # Verificar que el usuario tenga acceso a la sucursal
        cursor.execute("""
                SELECT 1 
                FROM usuario_pivot_sucursal_usuario 
                WHERE id_usuario = %s AND id_sucursal = %s
            """, (usuario_id, nueva_sucursal))
            
        if not cursor.fetchone():
                cursor.close()
                conn.close()
                return jsonify({"error": "No tienes acceso a esta sucursal"}), 403

            # Actualizar la sucursal activa
        cursor.execute("""
                UPDATE general_dim_usuario 
                SET id_sucursalactiva = %s 
                WHERE id = %s
            """, (nueva_sucursal, usuario_id))
            
        conn.commit()

            # Obtener el nombre de la sucursal para la respuesta
        cursor.execute("""
                SELECT nombre 
                FROM general_dim_sucursal 
                WHERE id = %s
            """, (nueva_sucursal,))
            
        sucursal = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
                "message": "Sucursal actualizada correctamente",
                "id_sucursal": nueva_sucursal,
                "sucursal_nombre": sucursal['nombre'] if sucursal else None
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener sucursal activa del usuario logueado
@usuarios_bp.route('/sucursal-activa', methods=['GET'])
@jwt_required()
def obtener_sucursal_activa():
    usuario_id = get_jwt_identity()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_sucursalactiva FROM general_dim_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if not usuario or usuario['id_sucursalactiva'] is None:
            return jsonify({"error": "No se encontró la sucursal activa"}), 404

        return jsonify({"sucursal_activa": usuario['id_sucursalactiva']}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener todas las sucursales disponibles (para crear usuarios)
@usuarios_bp.route('/sucursales', methods=['GET'])
@jwt_required()
def obtener_sucursales():
    usuario_id = get_jwt_identity()
    if not verificar_admin(usuario_id):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener solo sucursales con id_sucursaltipo = 1
        cursor.execute("""
            SELECT id, nombre, ubicacion
            FROM general_dim_sucursal
            WHERE id_sucursaltipo = 1
            ORDER BY nombre ASC
        """)
        
        sucursales = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(sucursales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener sucursales permitidas de un usuario
@usuarios_bp.route('/<string:usuario_id>/sucursales-permitidas', methods=['GET'])
@jwt_required()
def obtener_sucursales_permitidas(usuario_id):
    usuario_logueado = get_jwt_identity()
    if not verificar_admin(usuario_logueado):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener las sucursales permitidas del usuario
        cursor.execute("""
            SELECT s.id, s.nombre, s.ubicacion
            FROM general_dim_sucursal s
            INNER JOIN usuario_pivot_sucursal_usuario p ON s.id = p.id_sucursal
            WHERE p.id_usuario = %s AND s.id_sucursaltipo = 1
            ORDER BY s.nombre ASC
        """, (usuario_id,))
        
        sucursales_permitidas = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(sucursales_permitidas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Asignar sucursales permitidas a un usuario
@usuarios_bp.route('/<string:usuario_id>/sucursales-permitidas', methods=['POST'])
@jwt_required()
def asignar_sucursales_permitidas(usuario_id):
    usuario_logueado = get_jwt_identity()
    if not verificar_admin(usuario_logueado):
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    sucursales_ids = data.get('sucursales_ids', [])  # Lista de IDs de sucursales

    if not isinstance(sucursales_ids, list):
        return jsonify({"error": "sucursales_ids debe ser una lista"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM general_dim_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar que todas las sucursales existen y son del tipo correcto
        if sucursales_ids:
            placeholders = ','.join(['%s'] * len(sucursales_ids))
            cursor.execute(f"""
                SELECT id FROM general_dim_sucursal 
                WHERE id IN ({placeholders}) AND id_sucursaltipo = 1
            """, sucursales_ids)
            sucursales_validas = cursor.fetchall()
            
            if len(sucursales_validas) != len(sucursales_ids):
                cursor.close()
                conn.close()
                return jsonify({"error": "Una o más sucursales no existen o no son del tipo correcto"}), 400

        # Eliminar todas las asignaciones actuales del usuario
        cursor.execute("DELETE FROM usuario_pivot_sucursal_usuario WHERE id_usuario = %s", (usuario_id,))
        
        # Insertar las nuevas asignaciones
        if sucursales_ids:
            for sucursal_id in sucursales_ids:
                cursor.execute("""
                    INSERT INTO usuario_pivot_sucursal_usuario (id_sucursal, id_usuario)
                    VALUES (%s, %s)
                """, (sucursal_id, usuario_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Sucursales permitidas asignadas correctamente",
            "usuario_id": usuario_id,
            "sucursales_asignadas": len(sucursales_ids)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar todas las sucursales permitidas de un usuario
@usuarios_bp.route('/<string:usuario_id>/sucursales-permitidas', methods=['DELETE'])
@jwt_required()
def eliminar_sucursales_permitidas(usuario_id):
    usuario_logueado = get_jwt_identity()
    if not verificar_admin(usuario_logueado):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM general_dim_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Eliminar todas las asignaciones del usuario
        cursor.execute("DELETE FROM usuario_pivot_sucursal_usuario WHERE id_usuario = %s", (usuario_id,))
        filas_eliminadas = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Sucursales permitidas eliminadas correctamente",
            "usuario_id": usuario_id,
            "sucursales_eliminadas": filas_eliminadas
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener todas las aplicaciones disponibles
@usuarios_bp.route('/apps', methods=['GET'])
@jwt_required()
def obtener_apps():
    usuario_id = get_jwt_identity()
    if not verificar_admin(usuario_id):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, nombre
            FROM general_dim_app
            ORDER BY nombre ASC
        """)
        
        apps = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(apps), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener aplicaciones permitidas de un usuario
@usuarios_bp.route('/<string:usuario_id>/apps-permitidas', methods=['GET'])
@jwt_required()
def obtener_apps_permitidas(usuario_id):
    usuario_logueado = get_jwt_identity()
    if not verificar_admin(usuario_logueado):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener las aplicaciones permitidas del usuario
        cursor.execute("""
            SELECT a.id, a.nombre
            FROM general_dim_app a
            INNER JOIN usuario_pivot_app_usuario p ON a.id = p.id_app
            WHERE p.id_usuario = %s
            ORDER BY a.nombre ASC
        """, (usuario_id,))
        
        apps_permitidas = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(apps_permitidas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Asignar aplicaciones permitidas a un usuario
@usuarios_bp.route('/<string:usuario_id>/apps-permitidas', methods=['POST'])
@jwt_required()
def asignar_apps_permitidas(usuario_id):
    usuario_logueado = get_jwt_identity()
    if not verificar_admin(usuario_logueado):
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    apps_ids = data.get('apps_ids', [])  # Lista de IDs de aplicaciones

    if not isinstance(apps_ids, list):
        return jsonify({"error": "apps_ids debe ser una lista"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM general_dim_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Verificar que todas las aplicaciones existen
        if apps_ids:
            placeholders = ','.join(['%s'] * len(apps_ids))
            cursor.execute(f"""
                SELECT id FROM general_dim_app 
                WHERE id IN ({placeholders})
            """, apps_ids)
            apps_validas = cursor.fetchall()
            
            if len(apps_validas) != len(apps_ids):
                cursor.close()
                conn.close()
                return jsonify({"error": "Una o más aplicaciones no existen"}), 400

        # Eliminar todas las asignaciones actuales del usuario
        cursor.execute("DELETE FROM usuario_pivot_app_usuario WHERE id_usuario = %s", (usuario_id,))
        
        # Insertar las nuevas asignaciones
        if apps_ids:
            for app_id in apps_ids:
                # Generar UUID para el id de la tabla pivote
                pivot_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO usuario_pivot_app_usuario (id, id_usuario, id_app)
                    VALUES (%s, %s, %s)
                """, (pivot_id, usuario_id, app_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Aplicaciones permitidas asignadas correctamente",
            "usuario_id": usuario_id,
            "apps_asignadas": len(apps_ids)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar todas las aplicaciones permitidas de un usuario
@usuarios_bp.route('/<string:usuario_id>/apps-permitidas', methods=['DELETE'])
@jwt_required()
def eliminar_apps_permitidas(usuario_id):
    usuario_logueado = get_jwt_identity()
    if not verificar_admin(usuario_logueado):
        return jsonify({"error": "No autorizado"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que el usuario existe
        cursor.execute("SELECT id FROM general_dim_usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            cursor.close()
            conn.close()
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Eliminar todas las asignaciones del usuario
        cursor.execute("DELETE FROM usuario_pivot_app_usuario WHERE id_usuario = %s", (usuario_id,))
        filas_eliminadas = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Aplicaciones permitidas eliminadas correctamente",
            "usuario_id": usuario_id,
            "apps_eliminadas": filas_eliminadas
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener información del usuario actual
@usuarios_bp.route('/perfil', methods=['GET'])
@jwt_required()
def obtener_perfil_usuario():
    try:
        usuario_id = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.id, u.usuario, u.correo, u.nombre, u.apellido_paterno, u.apellido_materno,
                   CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', COALESCE(u.apellido_materno, '')) as nombre_completo,
                   u.id_sucursalactiva, u.id_estado, u.id_rol, u.id_perfil, u.fecha_creacion,
                   s.nombre AS nombre_sucursal
            FROM general_dim_usuario u
            LEFT JOIN general_dim_sucursal s ON u.id_sucursalactiva = s.id
            WHERE u.id = %s
        """, (usuario_id,))

        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify(usuario), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Actualizar perfil del usuario actual
@usuarios_bp.route('/perfil', methods=['PUT'])
@jwt_required()
def actualizar_perfil_usuario():
    try:
        usuario_id = get_jwt_identity()
        data = request.json
        
        # Campos que se pueden actualizar
        nombre = data.get('nombre')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        correo = data.get('correo')

        if not any([nombre, apellido_paterno, apellido_materno, correo]):
            return jsonify({"error": "Al menos un campo debe ser proporcionado para actualizar"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Construir la consulta dinámicamente
        update_fields = []
        update_values = []
        
        if nombre is not None:
            update_fields.append("nombre = %s")
            update_values.append(nombre)
        
        if apellido_paterno is not None:
            update_fields.append("apellido_paterno = %s")
            update_values.append(apellido_paterno)
        
        if apellido_materno is not None:
            update_fields.append("apellido_materno = %s")
            update_values.append(apellido_materno)
        
        if correo is not None:
            update_fields.append("correo = %s")
            update_values.append(correo)

        update_values.append(usuario_id)
        
        query = f"""
            UPDATE general_dim_usuario 
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        
        cursor.execute(query, update_values)
        conn.commit()

        # Obtener el usuario actualizado
        cursor.execute("""
            SELECT u.id, u.usuario, u.correo, u.nombre, u.apellido_paterno, u.apellido_materno,
                   CONCAT(u.nombre, ' ', u.apellido_paterno, ' ', COALESCE(u.apellido_materno, '')) as nombre_completo,
                   u.id_sucursalactiva, u.id_estado, u.id_rol, u.id_perfil, u.fecha_creacion,
                   s.nombre AS nombre_sucursal
            FROM general_dim_usuario u
            LEFT JOIN general_dim_sucursal s ON u.id_sucursalactiva = s.id
            WHERE u.id = %s
        """, (usuario_id,))

        usuario_actualizado = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Perfil actualizado correctamente",
            "usuario": usuario_actualizado
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
