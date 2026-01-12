# Tablas de Base de Datos Utilizadas en la API

## Resumen
Esta API utiliza las siguientes tablas de la base de datos `lahornilla_base_normalizada`:

---

## 📊 Tablas Principales

### 1. **general_dim_usuario**
- **Descripción**: Usuarios del sistema
- **Uso**: Autenticación, gestión de usuarios, perfiles
- **Endpoints relacionados**: `/api/auth`, `/api/usuarios`
- **Columnas**:
  - `id` (VARCHAR(45)) - Identificador único del usuario
  - `usuario` (VARCHAR) - Nombre de usuario
  - `correo` (VARCHAR) - Correo electrónico
  - `clave` (VARCHAR) - Contraseña encriptada con bcrypt
  - `nombre` (VARCHAR) - Nombre del usuario
  - `apellido_paterno` (VARCHAR) - Apellido paterno
  - `apellido_materno` (VARCHAR) - Apellido materno
  - `id_sucursalactiva` (INT) - ID de la sucursal activa
  - `id_estado` (INT) - Estado del usuario (1=activo, 0=inactivo)
  - `id_rol` (INT) - Rol del usuario
  - `id_perfil` (INT) - Perfil del usuario (3=admin)
  - `fecha_creacion` (DATE) - Fecha de creación del usuario

### 2. **general_dim_sucursal**
- **Descripción**: Sucursales de la empresa
- **Uso**: Gestión de sucursales, asignación de usuarios
- **Endpoints relacionados**: `/api/auth`, `/api/usuarios`, `/api/opciones`
- **Columnas**:
  - `id` (INT) - Identificador único de la sucursal
  - `nombre` (VARCHAR(45)) - Nombre de la sucursal
  - `ubicacion` (VARCHAR(60)) - Ubicación de la sucursal
  - `id_empresa` (INT) - ID de la empresa
  - `id_sucursaltipo` (INT) - Tipo de sucursal (1=sucursal normal)

### 3. **general_dim_cuartel**
- **Descripción**: Cuarteles agrícolas
- **Uso**: Gestión de cuarteles, catastro
- **Endpoints relacionados**: `/api/cuarteles`
- **Columnas**:
  - `id` (INT) - Identificador único del cuartel
  - `id_ceco` (INT) - ID del centro de costo
  - `nombre` (VARCHAR) - Nombre del cuartel
  - `id_variedad` (INT) - ID de la variedad
  - `superficie` (FLOAT) - Superficie del cuartel
  - `ano_plantacion` (INT) - Año de plantación
  - `dsh` (FLOAT) - Distancia entre hileras
  - `deh` (FLOAT) - Distancia entre plantas en hilera
  - `id_propiedad` (INT) - ID de la propiedad
  - `id_portainjerto` (INT) - ID del portainjerto
  - `subdivisionesplanta` (INT) - Subdivisiones por planta
  - `id_estado` (INT) - Estado del cuartel (1=activo, 0=inactivo)
  - `fecha_baja` (DATE) - Fecha de baja (borrado lógico)
  - `id_estadoproductivo` (INT) - Estado productivo
  - `n_hileras` (INT) - Número de hileras
  - `id_estadocatastro` (INT) - Estado del catastro (2=finalizado)
  - `id_tiposubdivision` (INT) - Tipo de subdivisión

### 4. **general_dim_hilera**
- **Descripción**: Hileras dentro de los cuarteles
- **Uso**: Organización de plantas por hileras
- **Endpoints relacionados**: `/api/hileras`
- **Columnas**:
  - `id` (BIGINT) - Identificador único de la hilera
  - `hilera` (INT) - Número de hilera
  - `id_cuartel` (INT) - ID del cuartel al que pertenece

### 5. **general_dim_planta**
- **Descripción**: Plantas individuales dentro de las hileras
- **Uso**: Registro y mapeo de plantas
- **Endpoints relacionados**: `/api/plantas`
- **Columnas**:
  - `id` (BIGINT) - Identificador único de la planta
  - `id_hilera` (BIGINT) - ID de la hilera a la que pertenece
  - `planta` (INT) - Número de planta dentro de la hilera
  - `ubicacion` (VARCHAR(100)) - Ubicación de la planta
  - `fecha_creacion` (DATE) - Fecha de creación del registro

### 6. **general_dim_variedad**
- **Descripción**: Variedades de plantas
- **Uso**: Clasificación de variedades
- **Endpoints relacionados**: `/api/variedades`
- **Columnas**:
  - `id` (INT) - Identificador único de la variedad
  - `nombre` (VARCHAR) - Nombre de la variedad
  - `id_especie` (INT) - ID de la especie
  - `id_forma` (INT) - ID de la forma
  - `id_color` (INT) - ID del color

### 7. **general_dim_especie**
- **Descripción**: Especies de plantas
- **Uso**: Clasificación de especies
- **Endpoints relacionados**: `/api/especies`
- **Columnas**:
  - `id` (INT) - Identificador único de la especie
  - `nombre` (VARCHAR) - Nombre de la especie
  - `caja_equivalente` (FLOAT) - Equivalente en cajas

---

## 📋 Tablas de Mapeo y Registros

### 8. **mapeo_fact_registromapeo**
- **Descripción**: Registros principales de mapeo por temporada y cuartel
- **Uso**: Control de procesos de mapeo
- **Endpoints relacionados**: `/api/registromapeo`
- **Columnas**:
  - `id` (VARCHAR(45)) - Identificador único del registro de mapeo
  - `id_temporada` (INT) - ID de la temporada
  - `id_cuartel` (INT) - ID del cuartel
  - `fecha_inicio` (DATE) - Fecha de inicio del mapeo
  - `fecha_termino` (DATE) - Fecha de término del mapeo
  - `id_estado` (INT) - Estado del mapeo (1=en progreso, 2=finalizado, 3=pausado)

### 9. **mapeo_fact_registro**
- **Descripción**: Registros individuales de evaluación de plantas
- **Uso**: Almacenamiento de evaluaciones por planta
- **Endpoints relacionados**: `/api/registros`
- **Columnas**:
  - `id` (VARCHAR(45)) - Identificador único del registro
  - `id_evaluador` (VARCHAR(45)) - ID del usuario evaluador
  - `hora_registro` (DATETIME) - Fecha y hora del registro
  - `id_planta` (BIGINT) - ID de la planta evaluada
  - `id_tipoplanta` (VARCHAR(45)) - ID del tipo de planta
  - `imagen` (TEXT) - Ruta o URL de la imagen asociada
  - `id_mapeo` (VARCHAR(45)) - ID del registro de mapeo (opcional)

### 10. **mapeo_dim_tipoplanta**
- **Descripción**: Tipos de plantas (clasificación)
- **Uso**: Categorización de plantas en registros
- **Endpoints relacionados**: `/api/tipoplanta`
- **Columnas**:
  - `id` (VARCHAR(45)) - Identificador único del tipo de planta
  - `nombre` (VARCHAR(45)) - Nombre del tipo de planta
  - `factor_productivo` (FLOAT) - Factor productivo
  - `id_empresa` (INT) - ID de la empresa
  - `descripcion` (VARCHAR(100)) - Descripción del tipo de planta (opcional)

### 11. **mapeo_dim_estadocatastro**
- **Descripción**: Estados del proceso de catastro
- **Uso**: Control de estado de catastro de cuarteles
- **Endpoints relacionados**: `/api/estadocatastro`
- **Columnas**:
  - `id` (INT) - Identificador único del estado
  - `nombre` (VARCHAR) - Nombre del estado de catastro

### 12. **mapeo_fact_estado_hilera** ❌ **NO SE USA**
- **Descripción**: ~~Estados de progreso de hileras en mapeo~~ (Tabla eliminada del uso)
- **Estado**: ❌ **Esta tabla NO se utiliza más en la API**
- **Nota**: El estado de las hileras ahora se calcula dinámicamente basado en las plantas mapeadas, sin necesidad de una tabla separada.

---

## 🔗 Tablas de Relación (Pivot)

### 13. **usuario_pivot_sucursal_usuario**
- **Descripción**: Relación muchos a muchos entre usuarios y sucursales
- **Uso**: Control de acceso de usuarios a sucursales
- **Endpoints relacionados**: `/api/usuarios`
- **Columnas**:
  - `id` (INT) - Identificador único de la relación (auto_increment)
  - `id_sucursal` (INT) - ID de la sucursal
  - `id_usuario` (VARCHAR(45)) - ID del usuario

### 14. **usuario_pivot_app_usuario**
- **Descripción**: Relación muchos a muchos entre usuarios y aplicaciones
- **Uso**: Control de acceso de usuarios a aplicaciones
- **Endpoints relacionados**: `/api/auth`, `/api/usuarios`
- **Columnas**:
  - `id` (VARCHAR(45)) - Identificador único de la relación
  - `id_usuario` (VARCHAR(45)) - ID del usuario
  - `id_app` (INT) - ID de la aplicación

---

## 🏢 Tablas de Configuración

### 15. **general_dim_ceco**
- **Descripción**: Centros de costo
- **Uso**: Organización financiera, relación con cuarteles
- **Endpoints relacionados**: `/api/cuarteles` (JOIN)
- **Columnas**:
  - `id` (INT) - Identificador único del centro de costo
  - `nombre` (VARCHAR(60)) - Nombre del centro de costo
  - `id_cecotipo` (INT) - ID del tipo de centro de costo
  - `id_sucursal` (INT) - ID de la sucursal
  - `id_estado` (TINYINT) - Estado del centro de costo (1=activo)
  - `fecha_baja` (DATE) - Fecha de baja (opcional)

### 16. **general_dim_app**
- **Descripción**: Aplicaciones del sistema
- **Uso**: Control de acceso por aplicación
- **Endpoints relacionados**: `/api/usuarios`
- **Columnas**:
  - `id` (INT) - Identificador único de la aplicación (auto_increment)
  - `nombre` (VARCHAR(45)) - Nombre de la aplicación
  - `descripcion` (VARCHAR(100)) - Descripción de la aplicación (opcional)
  - `URL` (VARCHAR(100)) - URL de la aplicación (opcional)

### 17. **general_dim_empresa**
- **Descripción**: Empresas
- **Uso**: Información de empresas
- **Endpoints relacionados**: `/api/opciones`
- **Columnas**:
  - `id` (INT) - Identificador único de la empresa (auto_increment)
  - `nombre` (VARCHAR(45)) - Nombre de la empresa
  - `rut` (INT) - RUT de la empresa
  - `codigo_verificador` (TINYINT(1)) - Código verificador del RUT
  - `fecha_suscripcion` (DATE) - Fecha de suscripción (opcional)

### 18. **general_dim_labor**
- **Descripción**: Tipos de labores
- **Uso**: Catálogo de labores
- **Endpoints relacionados**: `/api/opciones`
- **Columnas**:
  - `id` (VARCHAR(45)) - Identificador único de la labor
  - `nombre` (VARCHAR(45)) - Nombre de la labor
  - `id_laborgrupo` (INT) - ID del grupo de labor
  - `id_estado` (INT) - Estado de la labor
  - `id_unidadpordefecto` (INT) - ID de la unidad por defecto (opcional)

### 19. **tarja_dim_unidad**
- **Descripción**: Unidades de medida
- **Uso**: Catálogo de unidades
- **Endpoints relacionados**: `/api/opciones`
- **Columnas**:
  - `id` (INT) - Identificador único de la unidad
  - `nombre` (VARCHAR(45)) - Nombre de la unidad
  - `id_estado` (INT) - Estado de la unidad

### 20. **general_dim_cecotipo**
- **Descripción**: Tipos de centros de costo
- **Uso**: Clasificación de cecos
- **Endpoints relacionados**: `/api/opciones`
- **Columnas**:
  - `id` (INT) - Identificador único del tipo de ceco (auto_increment)
  - `nombre` (VARCHAR(45)) - Nombre del tipo de centro de costo

---

## 📈 Resumen por Categoría

### Tablas de Dimensiones (Dim)
- `general_dim_usuario`
- `general_dim_sucursal`
- `general_dim_cuartel`
- `general_dim_hilera`
- `general_dim_planta`
- `general_dim_variedad`
- `general_dim_especie`
- `general_dim_ceco`
- `general_dim_app`
- `general_dim_empresa`
- `general_dim_labor`
- `general_dim_cecotipo`
- `mapeo_dim_tipoplanta`
- `mapeo_dim_estadocatastro`
- `tarja_dim_unidad`

### Tablas de Hechos (Fact)
- `mapeo_fact_registromapeo`
- `mapeo_fact_registro`
- `mapeo_fact_estado_hilera`

### Tablas de Relación (Pivot)
- `usuario_pivot_sucursal_usuario`
- `usuario_pivot_app_usuario`

---

## 🔍 Total de Tablas Utilizadas: **20 tablas**

---

## 📝 Notas
- La base de datos utilizada es: `lahornilla_base_normalizada`
- Todas las tablas siguen un esquema de normalización con prefijos según su función
- Las tablas `dim` son dimensiones (catálogos)
- Las tablas `fact` son hechos (transacciones/registros)
- Las tablas `pivot` son relaciones muchos a muchos
- **Última verificación**: Estructura verificada directamente en la base de datos el $(date)
- **Archivo de verificación**: Ver `estructura_tablas_real.txt` para detalles completos de tipos de datos
