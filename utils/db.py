import mysql.connector
import os
import logging
from config import Config

logger = logging.getLogger(__name__)

def parse_cloud_sql_url(url):
    """
    Parsea manualmente la URL de Cloud SQL para extraer los componentes.
    Formato esperado: mysql+pymysql://UserApp:&8y7c()tu9t/+,6@/lahornilla_base_normalizada?unix_socket=/cloudsql/gestion-la-hornilla:us-central1:gestion-la-hornilla
    """
    try:
        logger.info(f"🔍 Parseando URL: {url}")
        
        # Extraer la parte después de mysql+pymysql://
        if 'mysql+pymysql://' in url:
            url_part = url.split('mysql+pymysql://')[1]
        else:
            url_part = url.split('://')[1]
        
        # Separar usuario:password@database
        auth_db_part = url_part.split('?')[0]
        
        # Extraer usuario y password
        if '@' in auth_db_part:
            user_pass_part = auth_db_part.split('@')[0]
            database = auth_db_part.split('@')[1]
            
            if ':' in user_pass_part:
                user = user_pass_part.split(':')[0]
                password = user_pass_part.split(':')[1]
            else:
                user = user_pass_part
                password = ""
        else:
            user = ""
            password = ""
            database = auth_db_part
        
        # Extraer unix_socket
        unix_socket = ""
        if 'unix_socket=' in url:
            unix_socket = url.split('unix_socket=')[1]
        
        logger.info(f"✅ Parseado manualmente:")
        logger.info(f"   User: {user}")
        logger.info(f"   Database: {database}")
        logger.info(f"   Unix Socket: {unix_socket}")
        
        return {
            'user': user,
            'password': password,
            'database': database,
            'unix_socket': unix_socket
        }
        
    except Exception as e:
        logger.error(f"❌ Error parseando URL: {str(e)}")
        return None

def get_db_connection():
    """
    Obtiene conexión a la base de datos.
    Prioriza Cloud SQL con unix_socket si está en Cloud Run, sino usa conexión local.
    """
    try:
        # Verificar si estamos en Cloud Run
        if os.getenv('K_SERVICE'):
            logger.info("🚀 Detectado Cloud Run - usando unix_socket")
            
            # URL de Cloud SQL para Cloud Run
            cloud_sql_url = "mysql+pymysql://UserApp:&8y7c()tu9t/+,6@/lahornilla_base_normalizada?unix_socket=/cloudsql/gestion-la-hornilla:us-central1:gestion-la-hornilla"
            
            # Parsear la URL
            parsed = parse_cloud_sql_url(cloud_sql_url)
            
            if parsed:
                connection_params = {
                    'user': parsed['user'],
                    'password': parsed['password'],
                    'database': parsed['database'],
                    'unix_socket': parsed['unix_socket'],
                    'charset': 'utf8mb4',
                    'autocommit': True,
                    'use_unicode': True
                }
                logger.info(f"🔗 Parámetros de conexión: {connection_params}")
            else:
                raise Exception("No se pudo parsear la URL de Cloud SQL")
                
        else:
            # Conexión local (desarrollo)
            logger.info("🏠 Modo desarrollo - usando conexión local")
            connection_params = {
                'host': Config.DB_HOST,
                'user': Config.DB_USER,
                'password': Config.DB_PASSWORD,
                'database': Config.DB_NAME,
                'port': Config.DB_PORT,
                'charset': 'utf8mb4',
                'autocommit': True,
                'use_unicode': True
            }
            logger.info(f"🔌 Conectando a BD local: {Config.DB_HOST}")
        
        return mysql.connector.connect(**connection_params)
        
    except Exception as e:
        logger.error(f"❌ Error conectando a BD: {str(e)}")
        raise
