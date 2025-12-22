# Cambios en la Estructura de Tablas - Verificación Real

## Resumen
Se verificó la estructura real de las tablas en la base de datos `lahornilla_base_normalizada` y se actualizó la documentación en `TABLAS_BASE_DATOS.md`.

## Principales Cambios Encontrados

### 1. **general_dim_usuario**
- ✅ `id`: Cambió de UUID a `VARCHAR(45)`

### 2. **general_dim_sucursal**
- ✅ Agregada columna: `id_empresa` (INT)
- ✅ `ubicacion`: Especificado como `VARCHAR(60)`

### 3. **general_dim_cuartel**
- ✅ `superficie`: Cambió de DECIMAL a `FLOAT`
- ✅ `dsh`: Cambió de DECIMAL a `FLOAT`
- ✅ `deh`: Cambió de DECIMAL a `FLOAT`
- ✅ `id_estado`: Especificado como `TINYINT`

### 4. **general_dim_hilera**
- ✅ `id`: Cambió de INT a `BIGINT`

### 5. **general_dim_planta**
- ✅ `id`: Cambió de INT a `BIGINT`
- ✅ `id_hilera`: Cambió de INT a `BIGINT`
- ✅ `ubicacion`: Especificado como `VARCHAR(100)`

### 6. **general_dim_especie**
- ✅ `caja_equivalente`: Cambió de DECIMAL a `FLOAT`

### 7. **mapeo_fact_registromapeo**
- ✅ `id`: Especificado como `VARCHAR(45)` (no UUID)
- ⚠️ Removida columna `id_evaluador` (no existe en la estructura real)

### 8. **mapeo_fact_registro**
- ✅ `id`: Especificado como `VARCHAR(45)`
- ✅ `id_evaluador`: Especificado como `VARCHAR(45)`
- ✅ `id_planta`: Cambió de INT a `BIGINT`
- ✅ `id_tipoplanta`: Especificado como `VARCHAR(45)`
- ✅ `imagen`: Especificado como `TEXT`
- ✅ **NUEVA COLUMNA**: `id_mapeo` (VARCHAR(45)) - ID del registro de mapeo

### 9. **mapeo_dim_tipoplanta**
- ✅ `id`: Especificado como `VARCHAR(45)`
- ✅ `factor_productivo`: Cambió de DECIMAL a `FLOAT`
- ✅ **NUEVA COLUMNA**: `descripcion` (VARCHAR(100)) - Descripción del tipo de planta

### 10. **mapeo_fact_estado_hilera**
- ⚠️ **PROBLEMA**: No se pudo verificar la estructura de esta tabla. Se referencia en el código pero no se pudo consultar. Posiblemente no existe o requiere permisos especiales.

### 11. **usuario_pivot_sucursal_usuario**
- ✅ **NUEVA COLUMNA**: `id` (INT, auto_increment) - Identificador único de la relación
- ✅ `id_usuario`: Especificado como `VARCHAR(45)`

### 12. **usuario_pivot_app_usuario**
- ✅ `id`: Especificado como `VARCHAR(45)`
- ✅ `id_usuario`: Especificado como `VARCHAR(45)`

### 13. **general_dim_ceco**
- ✅ `nombre`: Especificado como `VARCHAR(60)`
- ✅ **NUEVAS COLUMNAS**:
  - `id_cecotipo` (INT) - ID del tipo de centro de costo
  - `id_estado` (TINYINT) - Estado del centro de costo
  - `fecha_baja` (DATE) - Fecha de baja

### 14. **general_dim_app**
- ✅ `id`: Especificado como INT con `auto_increment`
- ✅ **NUEVAS COLUMNAS**:
  - `descripcion` (VARCHAR(100)) - Descripción de la aplicación
  - `URL` (VARCHAR(100)) - URL de la aplicación

### 15. **general_dim_empresa**
- ✅ `id`: Especificado como INT con `auto_increment`
- ✅ `rut`: Cambió de VARCHAR a `INT`
- ✅ `codigo_verificador`: Cambió de VARCHAR a `TINYINT(1)`

### 16. **general_dim_labor**
- ✅ `id`: Cambió de INT a `VARCHAR(45)`
- ✅ **NUEVAS COLUMNAS**:
  - `id_laborgrupo` (INT) - ID del grupo de labor
  - `id_estado` (INT) - Estado de la labor
  - `id_unidadpordefecto` (INT) - ID de la unidad por defecto

### 17. **tarja_dim_unidad**
- ✅ Sin cambios significativos

### 18. **general_dim_cecotipo**
- ✅ `id`: Especificado como INT con `auto_increment`

## Archivos Generados

1. **estructura_tablas_real.txt**: Contiene la estructura completa de todas las tablas verificadas
2. **TABLAS_BASE_DATOS.md**: Actualizado con la estructura real
3. **VERIFICACION_ESTRUCTURA.md**: Resumen de la verificación basada en código

## Recomendaciones

1. ⚠️ Verificar manualmente la tabla `mapeo_fact_estado_hilera` - se referencia en el código pero no se pudo consultar
2. ✅ Revisar el código que usa `id_evaluador` en `mapeo_fact_registromapeo` - esta columna no existe en la estructura real
3. ✅ Actualizar el código que usa `nombre` en `general_dim_hilera` (debe ser `hilera`) - ver `registromapeo.py` línea 307
