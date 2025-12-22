#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar la estructura real de las tablas en la base de datos
"""

import sys
import os
import mysql.connector
from config import Config

# Lista de todas las tablas que usamos
TABLAS = [
    'general_dim_usuario',
    'general_dim_sucursal',
    'general_dim_cuartel',
    'general_dim_hilera',
    'general_dim_planta',
    'general_dim_variedad',
    'general_dim_especie',
    'mapeo_fact_registromapeo',
    'mapeo_fact_registro',
    'mapeo_dim_tipoplanta',
    'mapeo_dim_estadocatastro',
    'mapeo_fact_estado_hilera',
    'usuario_pivot_sucursal_usuario',
    'usuario_pivot_app_usuario',
    'general_dim_ceco',
    'general_dim_app',
    'general_dim_empresa',
    'general_dim_labor',
    'tarja_dim_unidad',
    'general_dim_cecotipo'
]

def obtener_estructura_tabla(cursor, nombre_tabla):
    """Obtiene la estructura de una tabla"""
    try:
        cursor.execute(f"SHOW COLUMNS FROM {nombre_tabla}")
        columnas = cursor.fetchall()
        if columnas is None or len(columnas) == 0:
            return None
        return columnas
    except Exception as e:
        print(f"    Error: {str(e)}")
        return None

def main():
    # Configurar encoding para Windows
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    print("=" * 80)
    print("VERIFICACION DE ESTRUCTURA DE TABLAS")
    print("=" * 80)
    print()
    
    try:
        # Intentar conexión a través del proxy (localhost) primero
        print("Conectando a la base de datos a traves del proxy...")
        print("Intentando localhost:3306 (proxy)...")
        
        # Intentar primero con localhost (proxy)
        try:
            connection_params = {
                'host': 'localhost',
                'user': Config.CLOUD_SQL_USER,
                'password': Config.CLOUD_SQL_PASSWORD,
                'database': Config.CLOUD_SQL_DB,
                'port': 3306,
                'charset': 'utf8mb4',
                'autocommit': True,
                'use_unicode': True
            }
            conn = mysql.connector.connect(**connection_params)
            print("Conexion exitosa a traves del proxy (localhost:3306)!")
        except Exception as e1:
            print(f"Error con localhost:3306: {str(e1)}")
            print("Intentando localhost:3307...")
            # Intentar con puerto alternativo
            try:
                connection_params = {
                    'host': 'localhost',
                    'user': Config.CLOUD_SQL_USER,
                    'password': Config.CLOUD_SQL_PASSWORD,
                    'database': Config.CLOUD_SQL_DB,
                    'port': 3307,
                    'charset': 'utf8mb4',
                    'autocommit': True,
                    'use_unicode': True
                }
                conn = mysql.connector.connect(**connection_params)
                print("Conexion exitosa a traves del proxy (localhost:3307)!")
            except Exception as e2:
                print(f"Error con localhost:3307: {str(e2)}")
                print("Intentando conexion directa a Cloud SQL...")
                # Fallback a conexión directa
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
                conn = mysql.connector.connect(**connection_params)
                print("Conexion exitosa directa a Cloud SQL!")
        print()
        
        cursor = conn.cursor()
        
        resultados = {}
        
        for tabla in TABLAS:
            print(f"Consultando tabla: {tabla}...")
            columnas = obtener_estructura_tabla(cursor, tabla)
            
            if columnas is None:
                print(f"  [ERROR] Error al consultar {tabla}")
                resultados[tabla] = None
            else:
                print(f"  [OK] Encontrada - {len(columnas)} columnas")
                resultados[tabla] = columnas
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 80)
        print("RESUMEN DE ESTRUCTURAS")
        print("=" * 80)
        print()
        
        # Mostrar estructura de cada tabla
        for tabla, columnas in resultados.items():
            if columnas is None or len(columnas) == 0:
                print(f"\n[ERROR] {tabla}: ERROR al consultar o tabla vacia")
            else:
                print(f"\n[TABLA] {tabla}:")
                print("-" * 80)
                for col in columnas:
                    if col is None:
                        continue
                    campo = col[0]
                    tipo = col[1]
                    null = "NULL" if col[2] == "YES" else "NOT NULL"
                    key = col[3] if col[3] else ""
                    default = f"DEFAULT {col[4]}" if col[4] else ""
                    extra = col[5] if col[5] else ""
                    
                    print(f"  - {campo:30} {tipo:20} {null:10} {key:5} {default} {extra}")
        
        # Guardar resultados en un archivo
        with open('estructura_tablas_real.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ESTRUCTURA REAL DE TABLAS EN LA BASE DE DATOS\n")
            f.write("=" * 80 + "\n\n")
            
            for tabla, columnas in resultados.items():
                if columnas is None:
                    f.write(f"\n[ERROR] {tabla}: ERROR al consultar\n")
                else:
                    f.write(f"\n[TABLA] {tabla}:\n")
                    f.write("-" * 80 + "\n")
                    for col in columnas:
                        campo = col[0]
                        tipo = col[1]
                        null = "NULL" if col[2] == "YES" else "NOT NULL"
                        key = col[3] if col[3] else ""
                        default = f"DEFAULT {col[4]}" if col[4] else ""
                        extra = col[5] if col[5] else ""
                        
                        f.write(f"  - {campo:30} {tipo:20} {null:10} {key:5} {default} {extra}\n")
        
        print()
        print("=" * 80)
        print("[OK] Verificacion completada")
        print("[ARCHIVO] Resultados guardados en: estructura_tablas_real.txt")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] Error general: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
