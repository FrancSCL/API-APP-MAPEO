#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test directo con requests para verificar el problema
"""

import requests
import json

BASE_URL = "https://apimapeo-927498545444.us-central1.run.app"

# Login
print("1. Login...")
login = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"usuario": "fsoto", "clave": "212121"}
)
print(f"   Status: {login.status_code}")
token = login.json().get("access_token")
print(f"   Token obtenido: {token[:30]}...")

# Probar con el mismo token en diferentes endpoints
headers = {"Authorization": f"Bearer {token}"}

print("\n2. Probando endpoints...")

# Endpoint que funciona
print("\n   /api/cuarteles/activos:")
r1 = requests.get(f"{BASE_URL}/api/cuarteles/activos", headers=headers)
print(f"      Status: {r1.status_code}")
print(f"      Headers enviados: {list(r1.request.headers.keys())}")

# Endpoint que falla
print("\n   /api/variedades:")
r2 = requests.get(f"{BASE_URL}/api/variedades", headers=headers)
print(f"      Status: {r2.status_code}")
print(f"      Headers enviados: {list(r2.request.headers.keys())}")
print(f"      Respuesta: {r2.text[:200]}")

# Verificar headers que se están enviando
print("\n3. Headers que se envían:")
print(f"   Authorization: {headers['Authorization'][:50]}...")

# Probar con verbose
print("\n4. Probando con verificación de headers...")
import urllib3
urllib3.disable_warnings()

# Hacer request manual para ver qué pasa
import http.client
conn = http.client.HTTPSConnection("apimapeo-927498545444.us-central1.run.app")
conn.request("GET", "/api/variedades", headers=headers)
response = conn.getresponse()
print(f"   Status: {response.status}")
print(f"   Headers respuesta: {dict(response.getheaders())}")
