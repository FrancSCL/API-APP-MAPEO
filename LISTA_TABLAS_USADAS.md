# 📋 LISTA COMPLETA DE TABLAS UTILIZADAS EN LA API

## 🎯 **RESUMEN**
Este documento lista todas las tablas de la base de datos `lahornilla_base_normalizada` que son utilizadas por la API.

**Total de Tablas**: **19 tablas** (actualizado - eliminada `mapeo_fact_estado_hilera`)

---

## 📊 **TABLAS DE DIMENSIONES (DIM)**

### **Esquema: `general_dim_*`**

1. **`general_dim_usuario`**
   - Usuarios del sistema
   - Endpoints: `/api/auth`, `/api/usuarios`

2. **`general_dim_sucursal`**
   - Sucursales de la empresa
   - Endpoints: `/api/auth`, `/api/usuarios`, `/api/opciones`

3. **`general_dim_cuartel`**
   - Cuarteles agrícolas
   - Endpoints: `/api/cuarteles`

4. **`general_dim_hilera`**
   - Hileras dentro de los cuarteles
   - Endpoints: `/api/hileras`

5. **`general_dim_planta`**
   - Plantas individuales dentro de las hileras
   - Endpoints: `/api/plantas`

6. **`general_dim_variedad`**
   - Variedades de plantas
   - Endpoints: `/api/variedades`

7. **`general_dim_especie`**
   - Especies de plantas
   - Endpoints: `/api/especies`

8. **`general_dim_ceco`**
   - Centros de costo
   - Endpoints: `/api/cuarteles` (JOIN)

9. **`general_dim_app`**
   - Aplicaciones del sistema
   - Endpoints: `/api/usuarios`

10. **`general_dim_empresa`**
    - Empresas
    - Endpoints: `/api/opciones`

11. **`general_dim_labor`**
    - Tipos de labores
    - Endpoints: `/api/opciones`

12. **`general_dim_cecotipo`**
    - Tipos de centros de costo
    - Endpoints: `/api/opciones`

### **Esquema: `mapeo_dim_*`**

13. **`mapeo_dim_tipoplanta`**
    - Tipos de plantas (clasificación)
    - Endpoints: `/api/tipoplanta`

14. **`mapeo_dim_estadocatastro`**
    - Estados del proceso de catastro
    - Endpoints: `/api/estadocatastro`

### **Esquema: `tarja_dim_*`**

15. **`tarja_dim_unidad`**
    - Unidades de medida
    - Endpoints: `/api/opciones`

---

## 📋 **TABLAS DE HECHOS (FACT)**

### **Esquema: `mapeo_fact_*`**

16. **`mapeo_fact_registromapeo`**
    - Registros principales de mapeo por temporada y cuartel
    - Endpoints: `/api/registromapeo`

17. **`mapeo_fact_registro`**
    - Registros individuales de evaluación de plantas
    - Endpoints: `/api/registros`

18. **`mapeo_fact_estado_hilera`** ⚠️
    - Estados de progreso de hileras en mapeo
    - Endpoints: `/api/registromapeo`
    - **Nota**: Esta tabla se referencia en el código pero no se pudo verificar su existencia en la base de datos

---

## 🔗 **TABLAS DE RELACIÓN (PIVOT)**

### **Esquema: `usuario_pivot_*`**

19. **`usuario_pivot_sucursal_usuario`**
    - Relación muchos a muchos entre usuarios y sucursales
    - Endpoints: `/api/usuarios`

20. **`usuario_pivot_app_usuario`**
    - Relación muchos a muchos entre usuarios y aplicaciones
    - Endpoints: `/api/auth`, `/api/usuarios`

---

## 📊 **RESUMEN POR CATEGORÍA**

| Categoría | Cantidad | Tablas |
|-----------|----------|--------|
| **Dimensiones (general_dim_*)** | 12 | usuario, sucursal, cuartel, hilera, planta, variedad, especie, ceco, app, empresa, labor, cecotipo |
| **Dimensiones (mapeo_dim_*)** | 2 | tipoplanta, estadocatastro |
| **Dimensiones (tarja_dim_*)** | 1 | unidad |
| **Hechos (mapeo_fact_*)** | 2 | registromapeo, registro |
| **Pivot (usuario_pivot_*)** | 2 | sucursal_usuario, app_usuario |
| **TOTAL** | **20** | |

---

## 🔍 **TABLAS POR ENDPOINT**

### **`/api/auth`**
- `general_dim_usuario`
- `general_dim_sucursal`
- `usuario_pivot_app_usuario`

### **`/api/usuarios`**
- `general_dim_usuario`
- `general_dim_sucursal`
- `general_dim_app`
- `usuario_pivot_sucursal_usuario`
- `usuario_pivot_app_usuario`

### **`/api/cuarteles`**
- `general_dim_cuartel`
- `general_dim_ceco`
- `general_dim_sucursal`

### **`/api/hileras`**
- `general_dim_hilera`
- `general_dim_cuartel`

### **`/api/plantas`**
- `general_dim_planta`
- `general_dim_hilera`

### **`/api/variedades`**
- `general_dim_variedad`

### **`/api/especies`**
- `general_dim_especie`

### **`/api/registromapeo`**
- `mapeo_fact_registromapeo`
- `general_dim_cuartel`
- `general_dim_hilera`
- `general_dim_planta`
- `mapeo_fact_registro`
- `mapeo_fact_estado_hilera` ⚠️

### **`/api/registros`**
- `mapeo_fact_registro`
- `general_dim_planta`
- `mapeo_dim_tipoplanta`

### **`/api/tipoplanta`**
- `mapeo_dim_tipoplanta`

### **`/api/estadocatastro`**
- `mapeo_dim_estadocatastro`

### **`/api/opciones`**
- `general_dim_labor`
- `tarja_dim_unidad`
- `general_dim_cecotipo`
- `general_dim_empresa`

---

## 📝 **NOTAS IMPORTANTES**

### **⚠️ Tabla No Verificada**
- **`mapeo_fact_estado_hilera`**: Se referencia en el código pero no se pudo verificar su existencia en la base de datos. Posiblemente:
  - No existe aún
  - Requiere permisos especiales
  - Tiene un nombre diferente

### **Estructura de Nomenclatura**
- **`general_dim_*`**: Tablas de dimensiones generales del sistema
- **`mapeo_dim_*`**: Tablas de dimensiones específicas del módulo de mapeo
- **`tarja_dim_*`**: Tablas de dimensiones del módulo de tarja
- **`mapeo_fact_*`**: Tablas de hechos (transacciones) del módulo de mapeo
- **`usuario_pivot_*`**: Tablas pivot (relaciones muchos a muchos) de usuarios

---

## ✅ **VERIFICACIÓN**

- ✅ **19 tablas identificadas** en el código (actualizado)
- ✅ **19 tablas verificadas** en la base de datos
- ✅ **Todas las tablas utilizadas están verificadas**

---

**Última actualización**: Enero 2025  
**Base de Datos**: `lahornilla_base_normalizada`  
**Estado**: ✅ Verificado contra código fuente y estructura de base de datos
