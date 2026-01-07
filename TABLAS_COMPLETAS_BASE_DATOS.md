# 📊 DOCUMENTACIÓN COMPLETA DE TABLAS DE BASE DE DATOS

## 🎯 **RESUMEN**
Este documento contiene la estructura completa de todas las tablas utilizadas en la API, incluyendo columnas, tipos de datos, relaciones y restricciones.

**Base de Datos**: `lahornilla_base_normalizada`  
**Fecha de Verificación**: Enero 2025  
**Total de Tablas**: 20 tablas

---

## 📋 **ÍNDICE DE TABLAS**

### **Tablas de Dimensiones (Dim)**
1. `general_dim_usuario` - Usuarios del sistema
2. `general_dim_sucursal` - Sucursales
3. `general_dim_cuartel` - Cuarteles agrícolas
4. `general_dim_hilera` - Hileras dentro de cuarteles
5. `general_dim_planta` - Plantas individuales
6. `general_dim_variedad` - Variedades de plantas
7. `general_dim_especie` - Especies de plantas
8. `general_dim_ceco` - Centros de costo
9. `general_dim_app` - Aplicaciones del sistema
10. `general_dim_empresa` - Empresas
11. `general_dim_labor` - Tipos de labores
12. `general_dim_cecotipo` - Tipos de centros de costo
13. `mapeo_dim_tipoplanta` - Tipos de plantas (clasificación)
14. `mapeo_dim_estadocatastro` - Estados de catastro
15. `tarja_dim_unidad` - Unidades de medida

### **Tablas de Hechos (Fact)**
16. `mapeo_fact_registromapeo` - Registros principales de mapeo
17. `mapeo_fact_registro` - Registros individuales de evaluación
18. `mapeo_fact_estado_hilera` - Estados de progreso de hileras ⚠️

### **Tablas de Relación (Pivot)**
19. `usuario_pivot_sucursal_usuario` - Relación usuarios-sucursales
20. `usuario_pivot_app_usuario` - Relación usuarios-aplicaciones

---

## 📊 **DETALLE DE TABLAS**

### **1. general_dim_usuario**
**Descripción**: Usuarios del sistema  
**Uso**: Autenticación, gestión de usuarios, perfiles  
**Endpoints**: `/api/auth`, `/api/usuarios`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único del usuario |
| `id_sucursalactiva` | INT | NOT NULL | MUL | - | ID de la sucursal activa |
| `usuario` | VARCHAR(45) | NOT NULL | UNI | - | Nombre de usuario (único) |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre del usuario |
| `apellido_paterno` | VARCHAR(45) | NOT NULL | - | - | Apellido paterno |
| `apellido_materno` | VARCHAR(45) | NULL | - | - | Apellido materno |
| `clave` | VARCHAR(255) | NOT NULL | - | - | Contraseña encriptada (bcrypt) |
| `fecha_creacion` | DATE | NOT NULL | - | - | Fecha de creación |
| `id_estado` | INT | NOT NULL | MUL | 1 | Estado (1=activo, 0=inactivo) |
| `correo` | VARCHAR(100) | NOT NULL | - | - | Correo electrónico |
| `id_rol` | INT | NOT NULL | MUL | 3 | Rol del usuario |
| `id_perfil` | INT | NOT NULL | MUL | 1 | Perfil del usuario (3=admin) |

**Relaciones**:
- `id_sucursalactiva` → `general_dim_sucursal.id`
- `id_estado` → Tabla de estados
- `id_rol` → Tabla de roles
- `id_perfil` → Tabla de perfiles

---

### **2. general_dim_sucursal**
**Descripción**: Sucursales de la empresa  
**Uso**: Gestión de sucursales, asignación de usuarios  
**Endpoints**: `/api/auth`, `/api/usuarios`, `/api/opciones`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | - | Identificador único de la sucursal |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la sucursal |
| `ubicacion` | VARCHAR(60) | NULL | - | - | Ubicación de la sucursal |
| `id_empresa` | INT | NOT NULL | MUL | - | ID de la empresa |
| `id_sucursaltipo` | INT | NOT NULL | MUL | 1 | Tipo de sucursal (1=normal) |

**Relaciones**:
- `id_empresa` → `general_dim_empresa.id`
- `id_sucursaltipo` → Tabla de tipos de sucursal

---

### **3. general_dim_cuartel**
**Descripción**: Cuarteles agrícolas  
**Uso**: Gestión de cuarteles, catastro  
**Endpoints**: `/api/cuarteles`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | - | Identificador único del cuartel |
| `id_ceco` | INT | NOT NULL | MUL | - | ID del centro de costo |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre del cuartel |
| `id_variedad` | INT | NOT NULL | - | - | ID de la variedad |
| `superficie` | FLOAT | NOT NULL | - | - | Superficie del cuartel |
| `ano_plantacion` | INT | NULL | - | year(curdate()) | Año de plantación |
| `dsh` | FLOAT | NULL | - | - | Distancia entre hileras |
| `deh` | FLOAT | NULL | - | - | Distancia entre plantas en hilera |
| `id_propiedad` | INT | NOT NULL | MUL | - | ID de la propiedad |
| `id_portainjerto` | INT | NULL | MUL | - | ID del portainjerto |
| `subdivisionesplanta` | INT | NULL | - | - | Subdivisiones por planta |
| `id_estado` | TINYINT | NOT NULL | MUL | 1 | Estado (1=activo, 0=inactivo) |
| `fecha_baja` | DATE | NULL | - | - | Fecha de baja (borrado lógico) |
| `id_estadoproductivo` | INT | NOT NULL | MUL | - | Estado productivo |
| `n_hileras` | INT | NULL | - | - | Número de hileras |
| `id_estadocatastro` | INT | NOT NULL | MUL | 1 | Estado del catastro (2=finalizado) |
| `id_tiposubdivision` | INT | NULL | MUL | - | Tipo de subdivisión |

**Relaciones**:
- `id_ceco` → `general_dim_ceco.id`
- `id_variedad` → `general_dim_variedad.id`
- `id_propiedad` → Tabla de propiedades
- `id_portainjerto` → Tabla de portainjertos
- `id_estado` → Tabla de estados
- `id_estadoproductivo` → Tabla de estados productivos
- `id_estadocatastro` → `mapeo_dim_estadocatastro.id`
- `id_tiposubdivision` → Tabla de tipos de subdivisión

---

### **4. general_dim_hilera**
**Descripción**: Hileras dentro de los cuarteles  
**Uso**: Organización de plantas por hileras  
**Endpoints**: `/api/hileras`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | BIGINT | NOT NULL | PRI | - | Identificador único de la hilera |
| `hilera` | INT | NOT NULL | - | - | Número de hilera |
| `id_cuartel` | INT | NOT NULL | MUL | - | ID del cuartel al que pertenece |

**Relaciones**:
- `id_cuartel` → `general_dim_cuartel.id`

---

### **5. general_dim_planta**
**Descripción**: Plantas individuales dentro de las hileras  
**Uso**: Registro y mapeo de plantas  
**Endpoints**: `/api/plantas`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | BIGINT | NOT NULL | PRI | - | Identificador único de la planta |
| `id_hilera` | BIGINT | NOT NULL | MUL | - | ID de la hilera a la que pertenece |
| `planta` | INT | NOT NULL | - | - | Número de planta dentro de la hilera |
| `ubicacion` | VARCHAR(100) | NULL | - | - | Ubicación de la planta |
| `fecha_creacion` | DATE | NULL | - | - | Fecha de creación del registro |

**Relaciones**:
- `id_hilera` → `general_dim_hilera.id`

---

### **6. general_dim_variedad**
**Descripción**: Variedades de plantas  
**Uso**: Clasificación de variedades  
**Endpoints**: `/api/variedades`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único de la variedad |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la variedad |
| `id_especie` | INT | NOT NULL | MUL | - | ID de la especie |
| `id_forma` | INT | NULL | MUL | - | ID de la forma |
| `id_color` | INT | NULL | MUL | - | ID del color |

**Relaciones**:
- `id_especie` → `general_dim_especie.id`
- `id_forma` → Tabla de formas
- `id_color` → Tabla de colores

---

### **7. general_dim_especie**
**Descripción**: Especies de plantas  
**Uso**: Clasificación de especies  
**Endpoints**: `/api/especies`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único de la especie |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la especie |
| `caja_equivalente` | FLOAT | NOT NULL | - | - | Equivalente en cajas |

---

### **8. mapeo_fact_registromapeo**
**Descripción**: Registros principales de mapeo por temporada y cuartel  
**Uso**: Control de procesos de mapeo  
**Endpoints**: `/api/registromapeo`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único del registro de mapeo |
| `id_temporada` | INT | NOT NULL | - | - | ID de la temporada |
| `id_cuartel` | INT | NOT NULL | - | - | ID del cuartel |
| `fecha_inicio` | DATE | NOT NULL | - | - | Fecha de inicio del mapeo |
| `fecha_termino` | DATE | NULL | - | - | Fecha de término del mapeo |
| `id_estado` | INT | NOT NULL | - | - | Estado (1=en progreso, 2=finalizado, 3=pausado) |

**Relaciones**:
- `id_cuartel` → `general_dim_cuartel.id`
- `id_temporada` → Tabla de temporadas
- `id_estado` → Tabla de estados de mapeo

---

### **9. mapeo_fact_registro**
**Descripción**: Registros individuales de evaluación de plantas  
**Uso**: Almacenamiento de evaluaciones por planta  
**Endpoints**: `/api/registros`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único del registro |
| `id_evaluador` | VARCHAR(45) | NOT NULL | - | - | ID del usuario evaluador |
| `hora_registro` | DATETIME | NOT NULL | - | - | Fecha y hora del registro |
| `id_planta` | BIGINT | NOT NULL | - | - | ID de la planta evaluada |
| `id_tipoplanta` | VARCHAR(45) | NOT NULL | - | - | ID del tipo de planta |
| `imagen` | TEXT | NULL | - | - | Ruta o URL de la imagen asociada |
| `id_mapeo` | VARCHAR(45) | NULL | - | - | ID del registro de mapeo (opcional) |

**Relaciones**:
- `id_evaluador` → `general_dim_usuario.id`
- `id_planta` → `general_dim_planta.id`
- `id_tipoplanta` → `mapeo_dim_tipoplanta.id`
- `id_mapeo` → `mapeo_fact_registromapeo.id`

---

### **10. mapeo_dim_tipoplanta**
**Descripción**: Tipos de plantas (clasificación)  
**Uso**: Categorización de plantas en registros  
**Endpoints**: `/api/tipoplanta`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único del tipo de planta |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre del tipo de planta |
| `factor_productivo` | FLOAT | NOT NULL | - | - | Factor productivo |
| `id_empresa` | INT | NOT NULL | MUL | - | ID de la empresa |
| `descripcion` | VARCHAR(100) | NULL | - | - | Descripción del tipo de planta (opcional) |

**Relaciones**:
- `id_empresa` → `general_dim_empresa.id`

---

### **11. mapeo_dim_estadocatastro**
**Descripción**: Estados del proceso de catastro  
**Uso**: Control de estado de catastro de cuarteles  
**Endpoints**: `/api/estadocatastro`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único del estado |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre del estado de catastro |

---

### **12. mapeo_fact_estado_hilera** ⚠️
**Descripción**: Estados de progreso de hileras en mapeo  
**Uso**: Seguimiento de progreso por hilera  
**Endpoints**: `/api/registromapeo`

**⚠️ NOTA**: Esta tabla se referencia en el código pero no se pudo verificar su estructura en la base de datos. Posiblemente no existe o requiere permisos especiales.

**Estructura esperada** (según código):
| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único del estado |
| `id_registro_mapeo` | VARCHAR(45) | NOT NULL | - | - | ID del registro de mapeo |
| `id_hilera` | BIGINT | NOT NULL | - | - | ID de la hilera |
| `estado` | VARCHAR | NOT NULL | - | - | Estado (en_progreso, pausado, completado) |
| `id_usuario` | VARCHAR(45) | NULL | - | - | ID del usuario que actualizó |
| `fecha_actualizacion` | DATETIME | NULL | - | - | Fecha de última actualización |

**Relaciones esperadas**:
- `id_registro_mapeo` → `mapeo_fact_registromapeo.id`
- `id_hilera` → `general_dim_hilera.id`
- `id_usuario` → `general_dim_usuario.id`

---

### **13. usuario_pivot_sucursal_usuario**
**Descripción**: Relación muchos a muchos entre usuarios y sucursales  
**Uso**: Control de acceso de usuarios a sucursales  
**Endpoints**: `/api/usuarios`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único de la relación |
| `id_sucursal` | INT | NOT NULL | MUL | - | ID de la sucursal |
| `id_usuario` | VARCHAR(45) | NOT NULL | MUL | - | ID del usuario |

**Relaciones**:
- `id_sucursal` → `general_dim_sucursal.id`
- `id_usuario` → `general_dim_usuario.id`

---

### **14. usuario_pivot_app_usuario**
**Descripción**: Relación muchos a muchos entre usuarios y aplicaciones  
**Uso**: Control de acceso de usuarios a aplicaciones  
**Endpoints**: `/api/auth`, `/api/usuarios`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único de la relación |
| `id_usuario` | VARCHAR(45) | NOT NULL | MUL | - | ID del usuario |
| `id_app` | INT | NOT NULL | MUL | - | ID de la aplicación |

**Relaciones**:
- `id_usuario` → `general_dim_usuario.id`
- `id_app` → `general_dim_app.id`

---

### **15. general_dim_ceco**
**Descripción**: Centros de costo  
**Uso**: Organización financiera, relación con cuarteles  
**Endpoints**: `/api/cuarteles` (JOIN)

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | - | Identificador único del centro de costo |
| `nombre` | VARCHAR(60) | NOT NULL | - | - | Nombre del centro de costo |
| `id_cecotipo` | INT | NOT NULL | MUL | - | ID del tipo de centro de costo |
| `id_sucursal` | INT | NOT NULL | MUL | - | ID de la sucursal |
| `id_estado` | TINYINT | NOT NULL | MUL | 1 | Estado (1=activo) |
| `fecha_baja` | DATE | NULL | - | - | Fecha de baja (opcional) |

**Relaciones**:
- `id_cecotipo` → `general_dim_cecotipo.id`
- `id_sucursal` → `general_dim_sucursal.id`
- `id_estado` → Tabla de estados

---

### **16. general_dim_app**
**Descripción**: Aplicaciones del sistema  
**Uso**: Control de acceso por aplicación  
**Endpoints**: `/api/usuarios`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único de la aplicación |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la aplicación |
| `descripcion` | VARCHAR(100) | NULL | - | - | Descripción de la aplicación (opcional) |
| `URL` | VARCHAR(100) | NULL | - | - | URL de la aplicación (opcional) |

---

### **17. general_dim_empresa**
**Descripción**: Empresas  
**Uso**: Información de empresas  
**Endpoints**: `/api/opciones`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único de la empresa |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la empresa |
| `rut` | INT | NULL | - | - | RUT de la empresa |
| `codigo_verificador` | TINYINT(1) | NULL | - | - | Código verificador del RUT |
| `fecha_suscripcion` | DATE | NULL | - | - | Fecha de suscripción (opcional) |

---

### **18. general_dim_labor**
**Descripción**: Tipos de labores  
**Uso**: Catálogo de labores  
**Endpoints**: `/api/opciones`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | VARCHAR(45) | NOT NULL | PRI | - | Identificador único de la labor |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la labor |
| `id_laborgrupo` | INT | NOT NULL | MUL | - | ID del grupo de labor |
| `id_estado` | INT | NOT NULL | MUL | - | Estado de la labor |
| `id_unidadpordefecto` | INT | NULL | MUL | - | ID de la unidad por defecto (opcional) |

**Relaciones**:
- `id_laborgrupo` → Tabla de grupos de labor
- `id_estado` → Tabla de estados
- `id_unidadpordefecto` → `tarja_dim_unidad.id`

---

### **19. tarja_dim_unidad**
**Descripción**: Unidades de medida  
**Uso**: Catálogo de unidades  
**Endpoints**: `/api/opciones`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | - | Identificador único de la unidad |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre de la unidad |
| `id_estado` | INT | NOT NULL | MUL | - | Estado de la unidad |

**Relaciones**:
- `id_estado` → Tabla de estados

---

### **20. general_dim_cecotipo**
**Descripción**: Tipos de centros de costo  
**Uso**: Clasificación de cecos  
**Endpoints**: `/api/opciones`

| Columna | Tipo | Null | Key | Default | Descripción |
|---------|------|------|-----|---------|-------------|
| `id` | INT | NOT NULL | PRI | auto_increment | Identificador único del tipo de ceco |
| `nombre` | VARCHAR(45) | NOT NULL | - | - | Nombre del tipo de centro de costo |

---

## 🔗 **DIAGRAMA DE RELACIONES PRINCIPALES**

```
general_dim_empresa
    └── general_dim_sucursal
            ├── general_dim_usuario (id_sucursalactiva)
            └── general_dim_ceco
                    └── general_dim_cuartel
                            └── general_dim_hilera
                                    └── general_dim_planta
                                            └── mapeo_fact_registro

general_dim_cuartel
    └── mapeo_fact_registromapeo
            ├── mapeo_fact_registro (id_mapeo)
            └── mapeo_fact_estado_hilera

general_dim_usuario
    ├── mapeo_fact_registro (id_evaluador)
    ├── usuario_pivot_sucursal_usuario
    └── usuario_pivot_app_usuario

general_dim_variedad
    └── general_dim_cuartel (id_variedad)

general_dim_especie
    └── general_dim_variedad (id_especie)

mapeo_dim_tipoplanta
    └── mapeo_fact_registro (id_tipoplanta)
```

---

## 📝 **NOTAS IMPORTANTES**

### **Tipos de Datos**
- **BIGINT**: Usado para `id` en `general_dim_hilera` y `general_dim_planta` (números grandes)
- **VARCHAR(45)**: IDs de usuario y registros de mapeo
- **TINYINT**: Estados booleanos (1=activo, 0=inactivo)
- **FLOAT**: Valores decimales (superficie, distancias, factores)
- **TEXT**: Campos de texto largo (imágenes, descripciones extensas)

### **Claves Foráneas (MUL)**
Las relaciones están indicadas con `MUL` (Multiple) en la columna Key. Estas son las relaciones principales:
- Usuarios → Sucursales
- Cuarteles → CECOs → Sucursales
- Plantas → Hileras → Cuarteles
- Registros → Plantas, Tipos de Planta, Mapeos
- Variedades → Especies

### **Tablas Pivot**
Las tablas `usuario_pivot_*` permiten relaciones muchos a muchos:
- Un usuario puede tener acceso a múltiples sucursales
- Un usuario puede tener acceso a múltiples aplicaciones

### **⚠️ Tabla No Verificada**
`mapeo_fact_estado_hilera` no se pudo verificar en la base de datos. Se recomienda verificar manualmente si existe o necesita ser creada.

---

## 🔍 **TOTAL DE TABLAS: 20**

- **15 Tablas de Dimensiones (Dim)**
- **3 Tablas de Hechos (Fact)**
- **2 Tablas de Relación (Pivot)**

---

**Última actualización**: Enero 2025  
**Estado**: ✅ Verificado contra estructura real de base de datos
