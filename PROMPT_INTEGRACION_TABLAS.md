# 🚀 PROMPT PARA INTEGRACIÓN DE TABLAS - API MAPEO AGRÍCOLA

## 📋 **DESCRIPCIÓN DEL SISTEMA**
Este prompt contiene la estructura completa de tablas de la API de Mapeo Agrícola para que otra API pueda integrarse y consumir datos de la misma base de datos.

**Sistema**: API de Mapeo de Plantas y Cuarteles Agrícolas  
**Base de Datos**: MySQL (compartida)  
**Autenticación**: JWT con control de acceso por sucursal  
**Arquitectura**: REST API con Flask  

---

## 🗄️ **ESQUEMA DE TABLAS EXISTENTES**

### 🔐 **1. TABLAS DE AUTENTICACIÓN Y USUARIOS**

#### **general_dim_usuario**
**Campos principales:**
- `id` VARCHAR(45) - ID único del usuario
- `id_sucursalactiva` INT - Sucursal activa del usuario
- `usuario` VARCHAR(45) - Nombre de usuario para login
- `nombre` VARCHAR(45) - Nombre del usuario
- `apellido_paterno` VARCHAR(45) - Apellido paterno
- `apellido_materno` VARCHAR(45) - Apellido materno (opcional)
- `clave` VARCHAR(255) - Contraseña hasheada con bcrypt
- `fecha_creacion` DATE - Fecha de creación del usuario
- `id_estado` INT - Estado del usuario (1=activo, 0=inactivo)
- `correo` VARCHAR(100) - Email del usuario
- `id_rol` INT - Rol del usuario (3=usuario por defecto)
- `id_perfil` INT - Perfil del usuario (1=usuario por defecto)

**Relaciones:** `id_sucursalactiva` → `general_dim_sucursal.id`

#### **general_dim_sucursal**
**Campos principales:**
- `id` INT - ID único de la sucursal
- `nombre` VARCHAR(255) - Nombre de la sucursal
- `ubicacion` VARCHAR(255) - Ubicación física
- `id_estado` INT - Estado de la sucursal

**Uso:** Ubicaciones físicas donde operan los usuarios

#### **usuario_pivot_sucursal_usuario**
**Campos principales:**
- `id_sucursal` INT - ID de la sucursal
- `id_usuario` VARCHAR(45) - ID del usuario

**Propósito:** Tabla pivote para relación muchos a muchos entre usuarios y sucursales

#### **general_dim_empresa**
**Campos principales:**
- `id` INT - ID único de la empresa
- `nombre` VARCHAR(255) - Nombre de la empresa
- `rut` VARCHAR(20) - RUT de la empresa
- `codigo_verificador` VARCHAR(1) - Dígito verificador del RUT
- `fecha_suscripcion` DATE - Fecha de suscripción
- `id_estado` INT - Estado de la empresa

**Uso:** Empresas que utilizan el sistema

---

### 🌱 **2. TABLAS DE GESTIÓN AGRÍCOLA**

#### **general_dim_cuartel**
**Campos principales:**
- `id` INT - ID único del cuartel
- `id_ceco` VARCHAR(50) - Código de centro de costo
- `nombre` VARCHAR(255) - Nombre del cuartel
- `id_variedad` INT - ID de la variedad cultivada
- `superficie` DECIMAL(10,2) - Superficie en hectáreas
- `ano_plantacion` INT - Año de plantación
- `dsh` DECIMAL(10,2) - Distancia entre hileras
- `deh` DECIMAL(10,2) - Distancia entre plantas
- `id_propiedad` INT - ID de la propiedad
- `id_portainjerto` INT - ID del portainjerto
- `brazos_ejes` INT - Número de brazos y ejes
- `id_estado` INT - Estado del cuartel
- `fecha_baja` DATE - Fecha de baja (si aplica)
- `id_estadoproductivo` INT - Estado productivo
- `n_hileras` INT - Número de hileras
- `id_estadocatastro` INT - Estado del catastro
- `id_sucursal` INT - ID de la sucursal

**Relaciones:** `id_sucursal` → `general_dim_sucursal.id`

#### **general_dim_hilera**
**Campos principales:**
- `id` INT - ID único de la hilera
- `hilera` VARCHAR(50) - Número o código de la hilera
- `id_cuartel` INT - ID del cuartel al que pertenece
- `id_estado` INT - Estado de la hilera

**Relaciones:** `id_cuartel` → `general_dim_cuartel.id`

#### **general_dim_planta**
**Campos principales:**
- `id` INT - ID único de la planta
- `id_hilera` INT - ID de la hilera al que pertenece
- `planta` VARCHAR(50) - Número o código de la planta
- `ubicacion` VARCHAR(100) - Ubicación específica
- `fecha_creacion` DATE - Fecha de creación del registro
- `id_estado` INT - Estado de la planta

**Restricción:** Planta única por hilera  
**Relaciones:** `id_hilera` → `general_dim_hilera.id`

---

### 🍇 **3. TABLAS DE VARIEDADES Y ESPECIES**

#### **general_dim_variedad**
**Campos principales:**
- `id` INT - ID único de la variedad
- `nombre` VARCHAR(255) - Nombre de la variedad
- `id_especie` INT - ID de la especie
- `id_forma` INT - ID de la forma
- `id_color` INT - ID del color
- `id_estado` INT - Estado de la variedad

**Relaciones:** `id_especie` → `general_dim_especie.id`

#### **general_dim_especie**
**Campos principales:**
- `id` INT - ID único de la especie
- `nombre` VARCHAR(255) - Nombre de la especie
- `caja_equivalente` DECIMAL(10,2) - Equivalencia en cajas
- `id_estado` INT - Estado de la especie

**Uso:** Especies de plantas con equivalencias de cajas

---

### 📝 **4. TABLAS DE MAPEO Y REGISTROS**

#### **mapeo_fact_registromapeo**
**Campos principales:**
- `id` VARCHAR(36) - UUID único del registro de mapeo
- `id_temporada` INT - ID de la temporada
- `id_cuartel` INT - ID del cuartel a mapear
- `fecha_inicio` DATE - Fecha de inicio del mapeo
- `fecha_termino` DATE - Fecha de término del mapeo
- `id_estado` INT - Estado del registro de mapeo
- `fecha_creacion` DATETIME - Timestamp de creación

**Relaciones:** `id_cuartel` → `general_dim_cuartel.id`

#### **mapeo_fact_registro**
**Campos principales:**
- `id` VARCHAR(36) - UUID único del registro
- `id_evaluador` VARCHAR(45) - ID del usuario evaluador
- `hora_registro` DATETIME - Hora exacta del registro
- `id_planta` INT - ID de la planta evaluada
- `id_tipoplanta` VARCHAR(36) - ID del tipo de planta
- `imagen` TEXT - Imagen en base64 (opcional)
- `fecha_creacion` DATETIME - Timestamp de creación

**Relaciones:** 
- `id_evaluador` → `general_dim_usuario.id`
- `id_planta` → `general_dim_planta.id`

#### **mapeo_fact_estado_hilera**
**Campos principales:**
- `id` VARCHAR(36) - UUID único del estado
- `id_registro_mapeo` VARCHAR(36) - ID del registro de mapeo
- `id_hilera` INT - ID de la hilera
- `estado` ENUM - Estado: 'pendiente', 'en_progreso', 'pausado', 'completado'
- `fecha_creacion` DATETIME - Timestamp de creación
- `fecha_actualizacion` DATETIME - Timestamp de última actualización
- `id_usuario` VARCHAR(36) - ID del usuario responsable
- `observaciones` TEXT - Observaciones adicionales

**Restricción:** Una hilera por registro de mapeo  
**Relaciones:**
- `id_registro_mapeo` → `mapeo_fact_registromapeo.id`
- `id_hilera` → `general_dim_hilera.id`
- `id_usuario` → `general_dim_usuario.id`

---

### 🏷️ **5. TABLAS DE CLASIFICACIÓN**

#### **mapeo_dim_tipoplanta**
**Campos principales:**
- `id` VARCHAR(36) - UUID único del tipo de planta
- `nombre` VARCHAR(255) - Nombre del tipo de planta
- `factor_productivo` DECIMAL(10,2) - Factor productivo
- `id_empresa` INT - ID de la empresa
- `id_estado` INT - Estado del tipo de planta

**Relaciones:** `id_empresa` → `general_dim_empresa.id`

#### **mapeo_dim_estadocatastro**
**Campos principales:**
- `id` INT - ID único del estado de catastro
- `nombre` VARCHAR(255) - Nombre del estado
- `id_estado` INT - Estado del registro

**Uso:** Estados del catastro de cuarteles

---

### 🔧 **6. TABLAS DE CONFIGURACIÓN**

#### **general_dim_labor**
**Campos principales:**
- `id` INT - ID único de la labor
- `nombre` VARCHAR(255) - Nombre de la labor
- `id_estado` INT - Estado de la labor

**Uso:** Tipos de labores agrícolas

#### **tarja_dim_unidad**
**Campos principales:**
- `id` INT - ID único de la unidad
- `nombre` VARCHAR(255) - Nombre de la unidad
- `id_estado` INT - Estado de la unidad

**Uso:** Unidades de medida

#### **general_dim_cecotipo**
**Campos principales:**
- `id` INT - ID único del tipo de centro de costo
- `nombre` VARCHAR(255) - Nombre del tipo
- `id_estado` INT - Estado del tipo

**Uso:** Tipos de centros de costo

---

## 🔗 **RELACIONES Y JERARQUÍAS**

### **Jerarquía de Ubicaciones:**
```
Empresa → Sucursal → Cuartel → Hilera → Planta
```

### **Flujo de Mapeo:**
```
Usuario → Registro Mapeo → Estado Hilera → Registro Planta
```

### **Relaciones de Usuario:**
```
Usuario ↔ Sucursal (Pivote) ↔ Empresa
```

---

## 📊 **TIPOS DE DATOS UTILIZADOS**

### **Identificadores:**
- `VARCHAR(36)`: UUIDs para registros de mapeo (mapeo_fact_*)
- `VARCHAR(45)`: IDs de usuario
- `INT`: IDs autoincrementales para entidades principales
- `VARCHAR(50)`: Códigos y referencias cortas

### **Texto:**
- `VARCHAR(255)`: Nombres y descripciones largas
- `VARCHAR(100)`: Correos electrónicos y ubicaciones
- `VARCHAR(50)`: Códigos, números de planta/hilera
- `TEXT`: Observaciones, imágenes (base64), contenido largo

### **Fechas:**
- `DATE`: Fechas de creación, plantación, inicio/termino
- `DATETIME`: Timestamps de registros con hora
- `CURRENT_TIMESTAMP`: Valores por defecto automáticos

### **Numéricos:**
- `DECIMAL(10,2)`: Superficies, factores productivos, equivalencias
- `INT`: Años, cantidades, estados, IDs de referencia

### **Enumeraciones:**
- `ENUM('pendiente', 'en_progreso', 'pausado', 'completado')`: Estados de hilera

---

## 🛡️ **SEGURIDAD Y VALIDACIONES**

### **Restricciones de Integridad:**
- Claves foráneas en todas las relaciones
- Restricciones únicas para evitar duplicados
- Estados por defecto (id_estado = 1) para entidades activas
- CASCADE DELETE en relaciones jerárquicas

### **Autenticación:**
- JWT tokens con expiración
- Control de acceso por sucursal
- Validación de permisos por perfil de usuario

### **Validaciones de Negocio:**
- Planta única por hilera
- Hilera única por registro de mapeo
- Usuario debe tener acceso a la sucursal
- Fechas de inicio deben ser anteriores a fechas de término

---

## 📈 **ESTADÍSTICAS DE LA BASE DE DATOS**

- **Total de tablas**: 15 tablas principales
- **Tablas de dimensión**: 10 (general_dim_*, mapeo_dim_*)
- **Tablas de hechos**: 3 (mapeo_fact_*)
- **Tablas pivote**: 1 (usuario_pivot_sucursal_usuario)
- **Tablas de configuración**: 3 (tarja_dim_*, general_dim_*)

---

## 🚀 **INSTRUCCIONES PARA INTEGRACIÓN**

### **1. Configuración de Conexión:**
- Usar la misma base de datos MySQL
- Configurar credenciales de acceso
- Verificar permisos de lectura/escritura

### **2. Endpoints Recomendados:**
```python
# Autenticación
POST /auth/login
POST /auth/refresh
GET /auth/me

# Usuarios
GET /usuarios/
GET /usuarios/sucursal
POST /usuarios/sucursal-activa

# Cuarteles
GET /cuarteles/
GET /cuarteles/{id}
POST /cuarteles/

# Plantas
GET /plantas/
GET /plantas/{id}
POST /plantas/

# Mapeo
GET /registromapeo/
GET /registromapeo/{id}
POST /registromapeo/
GET /registromapeo/{id}/estado-hileras
POST /registromapeo/{id}/estado-hileras

# Registros
GET /registros/
POST /registros/
```

### **3. Configuración de Autenticación:**
- Implementar JWT con el mismo secret key
- Configurar expiración de tokens
- Implementar middleware de autenticación
- Validar acceso por sucursal

### **4. Validaciones Importantes:**
- Verificar que el usuario tenga acceso a la sucursal
- Validar que las plantas pertenezcan a hileras válidas
- Comprobar que los registros de mapeo estén activos
- Validar fechas de inicio y término

---

## 📋 **EJEMPLOS DE CONSULTAS ÚTILES**

### **Obtener plantas por cuartel:**
```sql
SELECT p.*, h.hilera, c.nombre as cuartel_nombre
FROM general_dim_planta p
JOIN general_dim_hilera h ON p.id_hilera = h.id
JOIN general_dim_cuartel c ON h.id_cuartel = c.id
WHERE c.id = ?
```

### **Obtener estado de hileras por registro de mapeo:**
```sql
SELECT eh.*, h.hilera, c.nombre as cuartel_nombre
FROM mapeo_fact_estado_hilera eh
JOIN general_dim_hilera h ON eh.id_hilera = h.id
JOIN general_dim_cuartel c ON h.id_cuartel = c.id
WHERE eh.id_registro_mapeo = ?
```

### **Obtener registros por evaluador:**
```sql
SELECT r.*, p.planta, u.nombre as evaluador_nombre
FROM mapeo_fact_registro r
JOIN general_dim_planta p ON r.id_planta = p.id
JOIN general_dim_usuario u ON r.id_evaluador = u.id
WHERE r.id_evaluador = ?
```

---

**📅 Última actualización**: Diciembre 2024  
**🔧 Versión de la API**: 1.0.0  
**📋 Estado**: Documentación para integración con base de datos compartida
