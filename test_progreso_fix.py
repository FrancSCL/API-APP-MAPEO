#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test rápido del endpoint de progreso después de eliminar tabla"""

import requests
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

BASE_URL = "https://apimapeo-927498545444.us-central1.run.app"

# Login
print("1. Login...")
r = requests.post(f"{BASE_URL}/api/auth/login", json={"usuario": "fsoto", "clave": "212121"})
token = r.json()['access_token']
print(f"   ✅ Token obtenido")

# Obtener un registro de mapeo
print("\n2. Obteniendo registros de mapeo...")
h = {"Authorization": f"Bearer {token}"}
r2 = requests.get(f"{BASE_URL}/api/registromapeo/", headers=h)
if r2.status_code == 200 and len(r2.json()) > 0:
    registro_id = r2.json()[0]['id']
    print(f"   ✅ Registro encontrado: {registro_id}")
    
    # Probar progreso
    print(f"\n3. Probando endpoint de progreso...")
    r3 = requests.get(f"{BASE_URL}/api/registromapeo/{registro_id}/progreso", headers=h, allow_redirects=True)
    print(f"   Status: {r3.status_code}")
    if r3.status_code == 200:
        data = r3.json()
        print(f"   ✅ FUNCIONA!")
        print(f"   Total hileras: {data.get('total_hileras', 0)}")
        print(f"   Hileras completadas: {data.get('hileras_completadas', 0)}")
        print(f"   Porcentaje: {data.get('porcentaje_general', 0)}%")
    else:
        print(f"   ❌ Error: {r3.text[:200]}")
else:
    print(f"   ⚠️  No hay registros de mapeo para probar")

print("\n✅ Test completado")
