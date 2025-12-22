# Verificación de Estructura de Tablas

## Resumen de Verificación

Se ha realizado una revisión exhaustiva del código para verificar la estructura de las tablas documentadas en `TABLAS_BASE_DATOS.md`.

## ✅ Tablas Verificadas

Todas las 20 tablas documentadas están siendo utilizadas en el código y las columnas documentadas coinciden con las consultas SQL encontradas.

## ⚠️ Inconsistencias Encontradas

### 1. **general_dim_hilera** - Error en registromapeo.py

**Ubicación**: `blueprints/registromapeo.py`, línea 307

**Problema**: 
```sql
SELECT id, nombre, id_cuartel
FROM general_dim_hilera
WHERE id_cuartel = %s
ORDER BY nombre ASC
```

**Debería ser**:
```sql
SELECT id, hilera, id_cuartel
FROM general_dim_hilera
WHERE id_cuartel = %s
ORDER BY hilera ASC
```

**Evidencia**: 
- En `hileras.py` todas las consultas usan `hilera` (líneas 20, 42, 100, 115, 241, 264, 287, 310, 341)
- Los INSERT usan `hilera` (líneas 115, 341)
- Los UPDATE usan `hilera` (línea 180)

**Conclusión**: La columna correcta es `hilera`, no `nombre`. Hay un error en el código de `registromapeo.py`.

## 📋 Columnas Verificadas por Tabla

### general_dim_usuario
✅ Todas las columnas documentadas están en uso:
- id, usuario, correo, clave, nombre, apellido_paterno, apellido_materno
- id_sucursalactiva, id_estado, id_rol, id_perfil, fecha_creacion

### general_dim_sucursal
✅ Columnas verificadas:
- id, nombre, ubicacion, id_sucursaltipo

### general_dim_cuartel
✅ Todas las 17 columnas documentadas están en uso en las consultas SELECT

### general_dim_hilera
✅ Columnas verificadas:
- id, hilera, id_cuartel
⚠️ **Nota**: Ver inconsistencia arriba

### general_dim_planta
✅ Columnas verificadas:
- id, id_hilera, planta, ubicacion, fecha_creacion

### general_dim_variedad
✅ Columnas verificadas:
- id, nombre, id_especie, id_forma, id_color

### general_dim_especie
✅ Columnas verificadas:
- id, nombre, caja_equivalente

### mapeo_fact_registromapeo
✅ Columnas verificadas:
- id, id_temporada, id_cuartel, fecha_inicio, fecha_termino, id_estado
- id_evaluador (usado en subconsultas)

### mapeo_fact_registro
✅ Columnas verificadas:
- id, id_evaluador, hora_registro, id_planta, id_tipoplanta, imagen

### mapeo_dim_tipoplanta
✅ Columnas verificadas:
- id, nombre, factor_productivo, id_empresa

### mapeo_dim_estadocatastro
✅ Columnas verificadas:
- id, nombre

### mapeo_fact_estado_hilera
✅ Columnas verificadas:
- id, id_registro_mapeo, id_hilera, estado, id_usuario, fecha_actualizacion

### usuario_pivot_sucursal_usuario
✅ Columnas verificadas:
- id_sucursal, id_usuario

### usuario_pivot_app_usuario
✅ Columnas verificadas:
- id, id_usuario, id_app

### general_dim_ceco
✅ Columnas verificadas:
- id, nombre, id_sucursal (usado en JOINs)

### general_dim_app
✅ Columnas verificadas:
- id, nombre

### general_dim_empresa
✅ Columnas verificadas:
- id, nombre, rut, codigo_verificador, fecha_suscripcion

### general_dim_labor
✅ Columnas verificadas:
- id, nombre

### tarja_dim_unidad
✅ Columnas verificadas:
- id, nombre, id_estado

### general_dim_cecotipo
✅ Columnas verificadas:
- id, nombre

## 🔍 Recomendaciones

1. **Corregir el error en registromapeo.py**: Cambiar `nombre` por `hilera` en la línea 307
2. **Verificación directa en BD**: Si es posible, ejecutar `SHOW COLUMNS FROM nombre_tabla` en cada tabla para confirmar la estructura real
3. **Mantener documentación actualizada**: La documentación en `TABLAS_BASE_DATOS.md` parece estar correcta basada en el código

## 📝 Notas

- No fue posible conectarse directamente a la base de datos Cloud SQL desde el entorno local
- La verificación se basó en el análisis exhaustivo de todas las consultas SQL en el código
- Se recomienda verificar directamente en la base de datos cuando sea posible
