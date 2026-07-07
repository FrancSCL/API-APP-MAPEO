#!/usr/bin/env python3
"""
Script para probar diferentes credenciales de Cloud SQL
"""

import os
import mysql.connector
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection_with_credentials(user, password, database, host=None, port=None, unix_socket=None):
    """Prueba conexión con credenciales específicas"""
    try:
        connection_params = {
            'user': user,
            'password': password,
            'database': database,
            'charset': 'utf8mb4',
            'autocommit': True,
            'use_unicode': True
        }
        
        if unix_socket:
            connection_params['unix_socket'] = unix_socket
            logger.info(f"🔌 Probando Unix socket: {unix_socket}")
        else:
            connection_params['host'] = host
            connection_params['port'] = port
            logger.info(f"🔌 Probando conexión TCP: {host}:{port}")
        
        logger.info(f"👤 Usuario: {user}")
        logger.info(f"🗄️  Base de datos: {database}")
        
        conn = mysql.connector.connect(**connection_params)
        cursor = conn.cursor(dictionary=True)
        
        # Probar consulta simple
        cursor.execute("SELECT VERSION() as version, DATABASE() as database_name, USER() as current_user")
        result = cursor.fetchone()
        
        logger.info(f"✅ Conexión exitosa!")
        logger.info(f"   MySQL Version: {result['version']}")
        logger.info(f"   Database: {result['database_name']}")
        logger.info(f"   Current User: {result['current_user']}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error de conexión: {str(e)}")
        return False

def main():
    """Prueba diferentes configuraciones de credenciales"""
    print("🔍 Probando diferentes credenciales de Cloud SQL...")
    
    # Configuración 1: Usando IP pública (como antes)
    print("\n📡 Configuración 1: IP Pública")
    test_connection_with_credentials(
        user="fsoto",
        password="",
        database="lahornilla_base_normalizada",
        host="34.41.120.220",
        port=3306
    )
    
    # Configuración 2: Unix socket con fsoto
    print("\n📡 Configuración 2: Unix Socket con fsoto")
    test_connection_with_credentials(
        user="fsoto",
        password="",
        database="lahornilla_base_normalizada",
        unix_socket="/cloudsql/gestion-la-hornilla:us-central1:gestion-la-hornilla"
    )
    
    # Configuración 3: Unix socket con root (para probar)
    print("\n📡 Configuración 3: Unix Socket con root")
    test_connection_with_credentials(
        user="root",
        password="",  # Sin password
        database="lahornilla_base_normalizada",
        unix_socket="/cloudsql/gestion-la-hornilla:us-central1:gestion-la-hornilla"
    )
    
    # Configuración 4: Probar con credenciales alternativas
    print("\n📡 Configuración 4: Credenciales alternativas")
    alternative_users = [
        ("admin", "admin123"),
        ("root", "root"),
        ("fsoto", "password"),
        ("fsoto", ""),
    ]
    
    for user, password in alternative_users:
        print(f"\n   Probando {user}...")
        test_connection_with_credentials(
            user=user,
            password=password,
            database="lahornilla_base_normalizada",
            unix_socket="/cloudsql/gestion-la-hornilla:us-central1:gestion-la-hornilla"
        )

if __name__ == '__main__':
    main() 