from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS
from datetime import timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación Flask
def create_app():
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"],
            "max_age": 3600
        }
    })

    # Configurar JWT
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=10)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    jwt = JWTManager(app)

    # Registrar los blueprints
    from blueprints.auth import auth_bp
    from blueprints.opciones import opciones_bp
    from blueprints.usuarios import usuarios_bp 
    from blueprints.registros import registros_bp
    from blueprints.cuarteles import cuarteles_bp
    from blueprints.estadocatastro import estadocatastro_bp
    from blueprints.plantas import plantas_bp
    from blueprints.tipoplanta import tipoplanta_bp
    from blueprints.hileras import hileras_bp
    from blueprints.especies import especies_bp
    from blueprints.variedades import variedades_bp
    
    
    # Registrar blueprints
    app.register_blueprint(opciones_bp, url_prefix="/api/opciones")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
    app.register_blueprint(registros_bp, url_prefix="/api/registros")
    app.register_blueprint(cuarteles_bp, url_prefix="/api/cuarteles")
    app.register_blueprint(estadocatastro_bp, url_prefix="/api/estadocatastro")
    app.register_blueprint(plantas_bp, url_prefix="/api/plantas")
    app.register_blueprint(tipoplanta_bp, url_prefix="/api/tipoplanta")
    app.register_blueprint(hileras_bp, url_prefix="/api/hileras")
    app.register_blueprint(especies_bp, url_prefix="/api/especies")
    app.register_blueprint(variedades_bp, url_prefix="/api/variedades")
    
    # Crear un nuevo blueprint para las rutas raíz
    root_bp = Blueprint('root_bp', __name__)
    
    # Importar y registrar las rutas raíz
    from blueprints.usuarios import obtener_sucursales
    root_bp.add_url_rule('/sucursales/', 'obtener_sucursales', obtener_sucursales, methods=['GET', 'OPTIONS'])
    
    # Registrar el blueprint raíz
    app.register_blueprint(root_bp, url_prefix="/api")

    # Endpoint de prueba de conexión a BD
    @app.route('/api/test-db', methods=['GET'])
    def test_database():
        """Endpoint para probar la conexión a la base de datos"""
        try:
            from utils.db import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Probar consulta simple
            cursor.execute("SELECT VERSION() as version, DATABASE() as database_name")
            result = cursor.fetchone()
            
            # Obtener información de tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [list(table.values())[0] for table in tables]
            
            cursor.close()
            conn.close()
            
            return {
                "status": "success",
                "message": "Conexión exitosa a la base de datos",
                "mysql_version": result['version'],
                "database": result['database_name'],
                "tables_count": len(table_names),
                "tables": table_names[:10]  # Solo las primeras 10
            }, 200
            
        except Exception as e:
            logger.error(f"Error en test-db: {str(e)}")
            return {
                "status": "error",
                "message": f"Error de conexión: {str(e)}"
            }, 500

    return app

# Crear una única instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)

