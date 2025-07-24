# 🚨 CAMBIOS API USUARIOS - FRONTEND

## ⚡ RESUMEN RÁPIDO

La tabla de usuarios cambió. **Ya no hay tabla de colaboradores**. Ahora todo está en `general_dim_usuario`.

## 🔥 CAMBIOS OBLIGATORIOS

### 1. **REGISTRO** (`POST /api/auth/register`)
```json
// ANTES
{
  "usuario": "juan123",
  "correo": "juan@email.com", 
  "clave": "password123",
  "id_sucursalactiva": 1
}

// AHORA - AGREGAR ESTOS CAMPOS
{
  "usuario": "juan123",
  "correo": "juan@email.com",
  "clave": "password123",
  "nombre": "Juan",              // ⚠️ NUEVO - OBLIGATORIO
  "apellido_paterno": "Pérez",   // ⚠️ NUEVO - OBLIGATORIO  
  "apellido_materno": "García",  // ⚠️ NUEVO - OPCIONAL
  "id_sucursalactiva": 1
}
```

### 2. **LOGIN** (`POST /api/auth/login`)
```json
// RESPUESTA NUEVA
{
  "access_token": "token...",
  "usuario": "juan123",
  "nombre_completo": "Juan Pérez García",  // ⚠️ NUEVO
  "id_sucursal": 1,
  "sucursal_nombre": "Sucursal Central",
  "id_rol": 3,
  "id_perfil": 1
}
```

### 3. **LISTA USUARIOS** (`GET /api/usuarios/`)
```json
// AHORA INCLUYE
{
  "id": "uuid-123",
  "usuario": "juan123",
  "correo": "juan@email.com",
  "nombre": "Juan",              // ⚠️ NUEVO
  "apellido_paterno": "Pérez",   // ⚠️ NUEVO
  "apellido_materno": "García",  // ⚠️ NUEVO
  // ... resto de campos
}
```

## 🆕 NUEVOS ENDPOINTS

### 4. **PERFIL USUARIO** (`GET /api/usuarios/perfil`)
```json
{
  "id": "uuid-123",
  "usuario": "juan123", 
  "correo": "juan@email.com",
  "nombre": "Juan",
  "apellido_paterno": "Pérez",
  "apellido_materno": "García",
  "nombre_completo": "Juan Pérez García",
  // ... resto de campos
}
```

### 5. **ACTUALIZAR PERFIL** (`PUT /api/usuarios/perfil`)
```json
// REQUEST
{
  "nombre": "Juan Carlos",        // Opcional
  "apellido_paterno": "Pérez",    // Opcional
  "apellido_materno": "García",   // Opcional
  "correo": "nuevo@email.com"     // Opcional
}
```

## ✅ TO-DO FRONTEND

- [ ] Agregar campos `nombre`, `apellido_paterno`, `apellido_materno` en registro
- [ ] Mostrar `nombre_completo` en login
- [ ] Actualizar listas de usuarios con nuevos campos
- [ ] Implementar pantalla de perfil con nuevos endpoints
- [ ] Validar que `nombre` y `apellido_paterno` no estén vacíos

## ❌ ELIMINADO

- `id_colaborador` ya no existe
- No más JOINs con tabla colaboradores

## 🚀 BENEFICIOS

- Consultas más rápidas
- Código más simple
- Menos complejidad

---

**⚠️ IMPORTANTE:** Estos cambios son **OBLIGATORIOS** para que funcione el frontend. 