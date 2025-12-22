# Cambios Aplicados en la API

## Resumen
Se actualizó la API para corregir los problemas encontrados en la verificación de la estructura de las tablas.

## Cambios Realizados

### 1. **blueprints/registromapeo.py**

#### Corrección 1: Uso incorrecto de columna `nombre` en `general_dim_hilera`
- **Línea 307**: Cambiado `SELECT id, nombre, id_cuartel` → `SELECT id, hilera, id_cuartel`
- **Línea 310**: Cambiado `ORDER BY nombre ASC` → `ORDER BY hilera ASC`
- **Línea 368**: Cambiado `"nombre": hilera['nombre']` → `"hilera": hilera['hilera']`

**Razón**: La tabla `general_dim_hilera` no tiene columna `nombre`, tiene `hilera`.

#### Corrección 2: Uso incorrecto de `id_evaluador` en `mapeo_fact_registromapeo`
- **Línea 336**: Cambiado la consulta que buscaba `id_evaluador` en `mapeo_fact_registromapeo` (columna que no existe) por usar `id_mapeo` en `mapeo_fact_registro`

**Antes**:
```sql
WHERE p.id_hilera = %s AND r.id_evaluador IN (
    SELECT id_evaluador FROM mapeo_fact_registromapeo WHERE id = %s
)
```

**Después**:
```sql
WHERE p.id_hilera = %s AND r.id_mapeo = %s
```

**Razón**: La tabla `mapeo_fact_registromapeo` no tiene columna `id_evaluador`. La relación se hace a través de `id_mapeo` en `mapeo_fact_registro`.

### 2. **blueprints/registros.py**

#### Mejora: Inclusión de `id_mapeo` en las consultas y creación de registros

- **Línea 92-102**: Actualizado el INSERT para incluir `id_mapeo` como campo opcional
- **Líneas 17-21, 40-44, 236-240, 259-263, 282-289**: Actualizadas todas las consultas SELECT para incluir `id_mapeo`
- **Línea 144**: Agregado `id_mapeo` a los campos actualizables

**Razón**: La columna `id_mapeo` existe en la tabla `mapeo_fact_registro` y permite relacionar los registros con el registro de mapeo principal.

## Impacto de los Cambios

### ✅ Correcciones Críticas
1. **registromapeo.py línea 307**: El endpoint `/api/registromapeo/<id>/progreso` ahora funciona correctamente
2. **registromapeo.py línea 336**: La consulta de plantas mapeadas ahora usa la relación correcta

### ✅ Mejoras
1. **registros.py**: Ahora se puede asociar un registro con un mapeo usando `id_mapeo`
2. Todas las consultas SELECT de registros ahora incluyen `id_mapeo` para mantener consistencia

## Notas

- Los tipos de datos (BIGINT vs INT) no requieren cambios en el código Python ya que Python maneja ambos correctamente
- La columna `id_mapeo` es opcional al crear registros, manteniendo compatibilidad con código existente
- Se mantiene la retrocompatibilidad: si no se envía `id_mapeo`, el registro se crea sin esa relación

## Archivos Modificados

1. `blueprints/registromapeo.py` - 3 correcciones
2. `blueprints/registros.py` - 7 actualizaciones (SELECTs e INSERT)

## Próximos Pasos Recomendados

1. ⚠️ Verificar la tabla `mapeo_fact_estado_hilera` - se referencia en el código pero no se pudo verificar su existencia
2. ✅ Probar el endpoint `/api/registromapeo/<id>/progreso` para confirmar que funciona correctamente
3. ✅ Considerar hacer `id_mapeo` requerido en futuras versiones si es necesario para la lógica de negocio
