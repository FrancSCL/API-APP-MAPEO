#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para el problema de 401 en endpoints
"""

import requests
import json
import sys
import os

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_URL = "https://apimapeo-927498545444.us-central1.run.app"
TEST_USER = "fsoto"
TEST_PASSWORD = "212121"

print("=" * 80)
print("DIAGNOSTICO DE ERROR 401")
print("=" * 80)

# 1. Login
print("\n1. Haciendo login...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"usuario": TEST_USER, "clave": TEST_PASSWORD},
    timeout=10
)

if login_response.status_code != 200:
    print(f"❌ Error en login: {login_response.status_code}")
    print(f"   Respuesta: {login_response.text}")
    sys.exit(1)

login_data = login_response.json()
token = login_data.get("access_token")
print(f"✅ Login exitoso")
print(f"   Token: {token[:50]}...")
print(f"   Usuario: {login_data.get('usuario')}")
print(f"   Rol: {login_data.get('id_rol')}")

# 2. Probar endpoints que funcionan
print("\n2. Probando endpoints que DEBERÍAN funcionar...")
headers = {"Authorization": f"Bearer {token}"}

endpoints_que_funcionan = [
    "/api/cuarteles/activos",
    "/api/registromapeo/estadisticas"
]

for endpoint in endpoints_que_funcionan:
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
    print(f"\n   {endpoint}:")
    print(f"      Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            print(f"      ✅ OK - {len(data)} elementos")
        else:
            print(f"      ✅ OK - {json.dumps(data, indent=2)[:100]}...")
    else:
        print(f"      ❌ Error: {response.text[:200]}")

# 3. Probar endpoints que fallan
print("\n3. Probando endpoints que FALLAN...")
endpoints_que_fallan = [
    "/api/variedades",
    "/api/especies",
    "/api/tipoplanta",
    "/api/registromapeo",
    "/api/registros",
    "/api/opciones"
]

for endpoint in endpoints_que_fallan:
    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
    print(f"\n   {endpoint}:")
    print(f"      Status: {response.status_code}")
    if response.status_code == 401:
        try:
            error_data = response.json()
            print(f"      ❌ 401 - {error_data.get('msg', error_data.get('error', 'Sin mensaje'))}")
        except:
            print(f"      ❌ 401 - {response.text[:200]}")
    elif response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            print(f"      ✅ OK - {len(data)} elementos")
        else:
            print(f"      ✅ OK")
    else:
        print(f"      ⚠️  Status {response.status_code}: {response.text[:200]}")

# 4. Verificar formato del token
print("\n4. Verificando formato del token...")
token_parts = token.split('.')
print(f"   Partes del token: {len(token_parts)}")
if len(token_parts) == 3:
    print("   ✅ Formato JWT correcto")
else:
    print("   ❌ Formato JWT incorrecto")

# 5. Probar sin Bearer
print("\n5. Probando sin 'Bearer' en el header...")
headers_sin_bearer = {"Authorization": token}
response = requests.get(f"{BASE_URL}/api/variedades", headers=headers_sin_bearer, timeout=10)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   ✅ Funciona sin 'Bearer'")
else:
    print("   ❌ No funciona sin 'Bearer'")

# 6. Probar con diferentes formatos
print("\n6. Probando diferentes formatos de header...")
formats = [
    ("Bearer " + token, "Bearer {token}"),
    ("bearer " + token, "bearer {token} (minúscula)"),
    (token, "Solo token"),
    ("Bearer  " + token, "Bearer con doble espacio"),
]

for header_value, description in formats:
    test_headers = {"Authorization": header_value}
    response = requests.get(f"{BASE_URL}/api/variedades", headers=test_headers, timeout=10)
    status = "✅" if response.status_code == 200 else "❌"
    print(f"   {status} {description}: Status {response.status_code}")

print("\n" + "=" * 80)
print("Diagnóstico completado")
print("=" * 80)
