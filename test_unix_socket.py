#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión Unix socket de Cloud SQL
"""

import os
import sys

def test_unix_socket_connection():
    """Prueba la conexión usando Unix socket"""
    print("🔍 Probando conexión Unix socket...")
    
    # Configurar variables de entorno como en Cloud Run
    os.environ['K_SERVICE'] = 'test-service'
    os.environ['PORT'] = '8080'
    os.environ['DEBUG'] = 'False'
    
    try:
        # Importar y crear la aplicación
        from app import create_app
        app = create_app()
        
        # Crear cliente de prueba
        with app.test_client() as client:
            print("✅ Aplicación creada correctamente")
            
            # Probar endpoint de test-db
            response = client.get('/api/test-db')
            print(f"📡 Test DB: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Conexión Unix socket funciona")
                print(f"📊 Respuesta: {response.get_json()}")
            else:
                print(f"❌ Error en conexión: {response.data}")
                return False
                
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False
    
    return True

def test_url_parser():
    """Prueba el parser de URL de Cloud SQL"""
    print("\n🔍 Probando parser de URL...")
    
    try:
        from utils.db import parse_cloud_sql_url
        
        # URL de prueba
        test_url = "mysql+pymysql://fsoto:@/lahornilla_base_normalizada?unix_socket=/cloudsql/gestion-la-hornilla:us-central1:gestion-la-hornilla"
        
        result = parse_cloud_sql_url(test_url)
        
        if result:
            print("✅ Parser funciona correctamente")
            print(f"   User: {result['user']}")
            print(f"   Database: {result['database']}")
            print(f"   Unix Socket: {result['unix_socket']}")
        else:
            print("❌ Error en el parser")
            return False
            
    except Exception as e:
        print(f"❌ Error en parser: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("🚀 Iniciando pruebas de Unix socket...")
    
    # Probar parser
    if test_url_parser():
        print("\n✅ Parser de URL funciona")
        
        # Probar conexión
        if test_unix_socket_connection():
            print("\n✅ Todas las pruebas exitosas")
            print("🎉 La aplicación está lista para Cloud Run con Unix socket!")
        else:
            print("\n❌ Error en conexión Unix socket")
            sys.exit(1)
    else:
        print("\n❌ Error en parser de URL")
        sys.exit(1) 