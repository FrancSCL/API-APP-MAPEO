import mysql.connector
import os
import logging
from config import Config

logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Obtiene conexión a la base de datos.
    Prioriza Cloud SQL si está configurado, sino usa conexión local.
    """
    try:
        # Priorizar Cloud SQL si está configurado
        if Config.CLOUD_SQL_HOST and Config.CLOUD_SQL_HOST != "None":
            # Conexión a Cloud SQL
            connection_params = {
                'host': Config.CLOUD_SQL_HOST,
                'user': Config.CLOUD_SQL_USER,
                'password': Config.CLOUD_SQL_PASSWORD,
                'database': Config.CLOUD_SQL_DB,
                'port': Config.CLOUD_SQL_PORT,
                'charset': 'utf8mb4',
                'autocommit': True,
                'use_unicode': True
            }
            logger.info(f"🔌 Conectando a Cloud SQL: {Config.CLOUD_SQL_HOST}")
        else:
            # Conexión local (fallback)
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
