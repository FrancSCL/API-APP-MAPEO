from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import get_db_connection
from datetime import datetime, date
import uuid

hileras_bp = Blueprint('hileras_bp', __name__)

# 🔹 Obtener todas las hileras
@hileras_bp.route('/', methods=['GET'])
@jwt_required()
def obtener_hileras():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, hilera, id_cuartel
            FROM general_dim_hilera
            ORDER BY hilera ASC
        """)
        
        hileras = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(hileras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener una hilera específica por ID
@hileras_bp.route('/<int:hilera_id>', methods=['GET'])
@jwt_required()
def obtener_hilera(hilera_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, hilera, id_cuartel
            FROM general_dim_hilera
            WHERE id = %s
        """, (hilera_id,))
        
        hilera = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not hilera:
            return jsonify({"error": "Hilera no encontrada"}), 404
        
        return jsonify(hilera), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Crear una nueva hilera
@hileras_bp.route('/', methods=['POST'])
@jwt_required()
def crear_hilera():
    try:
        data = request.json
        
        # Validar campos requeridos
        campos_requeridos = ['hilera', 'id_cuartel']
        for campo in campos_requeridos:
            if campo not in data:
                return jsonify({"error": f"Campo requerido: {campo}"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar que el cuartel existe
        cursor.execute("""
            SELECT id FROM general_dim_cuartel WHERE id = %s
        """, (data['id_cuartel'],))
        
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Cuartel no encontrado"}), 404
        
        # Verificar que no existe una hilera con el mismo número en el mismo cuartel
        cursor.execute("""
            SELECT id FROM general_dim_hilera 
            WHERE id_cuartel = %s AND hilera = %s
        """, (data['id_cuartel'], data['hilera']))
        
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Ya existe una hilera con ese número en este cuartel"}), 400
        
        # Insertar la nueva hilera (sin especificar id, se genera automáticamente)
        cursor.execute("""
            INSERT INTO general_dim_hilera 
            (hilera, id_cuartel)
            VALUES (%s, %s)
        """, (
            data['hilera'],
            data['id_cuartel']
        ))
        
        # Obtener el ID de la hilera recién creada
        hilera_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Hilera creada exitosamente",
            "id": hilera_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Actualizar una hilera existente
@hileras_bp.route('/<int:hilera_id>', methods=['PUT'])
@jwt_required()
def actualizar_hilera(hilera_id):
    try:
        data = request.json
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar que la hilera existe
        cursor.execute("""
            SELECT id FROM general_dim_hilera WHERE id = %s
        """, (hilera_id,))
        
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Hilera no encontrada"}), 404
        
        # Construir la consulta de actualización dinámicamente
        campos_actualizables = ['hilera', 'id_cuartel']
        campos_a_actualizar = []
        valores = []
        
        for campo in campos_actualizables:
            if campo in data:
                campos_a_actualizar.append(f"{campo} = %s")
                valores.append(data[campo])
        
        if not campos_a_actualizar:
            cursor.close()
            conn.close()
            return jsonify({"error": "No hay campos para actualizar"}), 400
        
        # Agregar el ID al final de los valores
        valores.append(hilera_id)
        
        # Ejecutar la actualización
        query = f"""
            UPDATE general_dim_hilera 
            SET {', '.join(campos_a_actualizar)}
            WHERE id = %s
        """
        
        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Hilera actualizada exitosamente",
            "id": hilera_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Eliminar una hilera
@hileras_bp.route('/<int:hilera_id>', methods=['DELETE'])
@jwt_required()
def eliminar_hilera(hilera_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar que la hilera existe
        cursor.execute("""
            SELECT id FROM general_dim_hilera WHERE id = %s
        """, (hilera_id,))
        
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Hilera no encontrada"}), 404
        
        # Eliminar la hilera
        cursor.execute("""
            DELETE FROM general_dim_hilera WHERE id = %s
        """, (hilera_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Hilera eliminada exitosamente",
            "id": hilera_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener hileras por cuartel
@hileras_bp.route('/cuartel/<int:cuartel_id>', methods=['GET'])
@jwt_required()
def obtener_hileras_por_cuartel(cuartel_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, hilera, id_cuartel
            FROM general_dim_hilera
            WHERE id_cuartel = %s
            ORDER BY hilera ASC
        """, (cuartel_id,))
        
        hileras = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(hileras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener hileras por número de hilera
@hileras_bp.route('/numero/<int:numero_hilera>', methods=['GET'])
@jwt_required()
def obtener_hileras_por_numero(numero_hilera):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, hilera, id_cuartel
            FROM general_dim_hilera
            WHERE hilera = %s
            ORDER BY hilera ASC
        """, (numero_hilera,))
        
        hileras = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(hileras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener hileras con información del cuartel
@hileras_bp.route('/con-cuartel', methods=['GET'])
@jwt_required()
def obtener_hileras_con_cuartel():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT h.id, h.hilera, h.id_cuartel, c.nombre as nombre_cuartel
            FROM general_dim_hilera h
            LEFT JOIN general_dim_cuartel c ON h.id_cuartel = c.id
            ORDER BY h.hilera ASC
        """)
        
        hileras = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(hileras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Obtener hileras por cuartel con información del cuartel
@hileras_bp.route('/cuartel/<int:cuartel_id>/con-info', methods=['GET'])
@jwt_required()
def obtener_hileras_por_cuartel_con_info(cuartel_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT h.id, h.hilera, h.id_cuartel, c.nombre as nombre_cuartel
            FROM general_dim_hilera h
            LEFT JOIN general_dim_cuartel c ON h.id_cuartel = c.id
            WHERE h.id_cuartel = %s
            ORDER BY h.hilera ASC
        """, (cuartel_id,))
        
        hileras = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(hileras), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@hileras_bp.route('/agregar-multiples', methods=['POST'])
@jwt_required()
def agregar_multiples_hileras():
    try:
        data = request.json
        id_cuartel = data.get('id_cuartel')
        n_hileras = data.get('n_hileras')
        if not id_cuartel or not n_hileras:
            return jsonify({"error": "Faltan campos requeridos: id_cuartel y n_hileras"}), 400
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Contar cuántas hileras existen actualmente para ese cuartel
        cursor.execute("SELECT COUNT(*) as total FROM general_dim_hilera WHERE id_cuartel = %s", (id_cuartel,))
        total_actual = cursor.fetchone()['total']
        # Solo agregar si faltan hileras
        nuevas = []
        for i in range(total_actual + 1, n_hileras + 1):
            cursor.execute("INSERT INTO general_dim_hilera (hilera, id_cuartel) VALUES (%s, %s)", (i, id_cuartel))
            nuevas.append(i)
        # Actualizar n_hileras en la tabla cuartel
        cursor.execute("UPDATE general_dim_cuartel SET n_hileras = %s WHERE id = %s", (max(n_hileras, total_actual), id_cuartel))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            "message": f"Se agregaron {len(nuevas)} hileras nuevas al cuartel {id_cuartel}",
            "hileras_agregadas": nuevas
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 