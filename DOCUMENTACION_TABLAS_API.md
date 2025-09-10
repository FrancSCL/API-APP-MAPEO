# 📋 DOCUMENTACIÓN DE TABLAS - API MAPEO

## 🏗️ **API: APP-MAPEO**
**Descripción**: API para gestión de mapeo de plantas y cuarteles agrícolas con sistema de autenticación JWT.

---

## 📊 **TABLAS PRINCIPALES**

### 🔐 **1. TABLAS DE AUTENTICACIÓN Y USUARIOS**

#### **general_dim_usuario**
```sql
CREATE TABLE general_dim_usuario (
    id VARCHAR(45) PRIMARY KEY,
    id_sucursalactiva INT NOT NULL,
    usuario VARCHAR(45) NOT NULL,
    nombre VARCHAR(45) NOT NULL,
    apellido_paterno VARCHAR(45) NOT NULL,
    apellido_materno VARCHAR(45) DEFAULT NULL,
    clave VARCHAR(255) NOT NULL,
    fecha_creacion DATE NOT NULL,
    id_estado INT NOT NULL DEFAULT 1,
    correo VARCHAR(100) NOT NULL,
    id_rol INT NOT NULL DEFAULT 3,
    id_perfil INT NOT NULL DEFAULT 1
);
```
**Descripción**: Tabla principal de usuarios del sistema con información personal y credenciales.

#### **general_dim_sucursal**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_sucursal (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(255)
);
```
**Descripción**: Tabla de sucursales o ubicaciones donde operan los usuarios.

#### **usuario_pivot_sucursal_usuario**
```sql
-- Estructura inferida del código
CREATE TABLE usuario_pivot_sucursal_usuario (
    id_sucursal INT,
    id_usuario VARCHAR(45),
    FOREIGN KEY (id_sucursal) REFERENCES general_dim_sucursal(id),
    FOREIGN KEY (id_usuario) REFERENCES general_dim_usuario(id)
);
```
**Descripción**: Tabla pivote que relaciona usuarios con las sucursales a las que tienen acceso.

#### **general_dim_empresa**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_empresa (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    rut VARCHAR(20),
    codigo_verificador VARCHAR(1),
    fecha_suscripcion DATE
);
```
**Descripción**: Tabla de empresas que utilizan el sistema.

---

### 🌱 **2. TABLAS DE GESTIÓN AGRÍCOLA**

#### **general_dim_cuartel**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_cuartel (
    id INT PRIMARY KEY,
    id_ceco VARCHAR(50),
    nombre VARCHAR(255) NOT NULL,
    id_variedad INT,
    superficie DECIMAL(10,2),
    ano_plantacion INT,
    dsh DECIMAL(10,2),
    deh DECIMAL(10,2),
    id_propiedad INT,
    id_portainjerto INT,
    brazos_ejes INT,
    id_estado INT DEFAULT 1,
    fecha_baja DATE,
    id_estadoproductivo INT,
    n_hileras INT,
    id_estadocatastro INT,
    id_sucursal INT
);
```
**Descripción**: Tabla principal de cuarteles (parcelas agrícolas) con información técnica y productiva.

#### **general_dim_hilera**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_hilera (
    id INT PRIMARY KEY,
    hilera VARCHAR(50) NOT NULL,
    id_cuartel INT NOT NULL,
    FOREIGN KEY (id_cuartel) REFERENCES general_dim_cuartel(id)
);
```
**Descripción**: Tabla de hileras dentro de cada cuartel.

#### **general_dim_planta**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_planta (
    id INT PRIMARY KEY,
    id_hilera INT NOT NULL,
    planta VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100),
    fecha_creacion DATE,
    FOREIGN KEY (id_hilera) REFERENCES general_dim_hilera(id)
);
```
**Descripción**: Tabla de plantas individuales dentro de cada hilera.

---

### 🍇 **3. TABLAS DE VARIEDADES Y ESPECIES**

#### **general_dim_variedad**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_variedad (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    id_especie INT,
    id_forma INT,
    id_color INT
);
```
**Descripción**: Tabla de variedades de plantas cultivadas.

#### **general_dim_especie**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_especie (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    caja_equivalente DECIMAL(10,2)
);
```
**Descripción**: Tabla de especies de plantas con equivalencias de cajas.

---

### 📝 **4. TABLAS DE MAPEO Y REGISTROS**

#### **mapeo_fact_registromapeo**
```sql
-- Estructura inferida del código
CREATE TABLE mapeo_fact_registromapeo (
    id VARCHAR(36) PRIMARY KEY,
    id_temporada INT NOT NULL,
    id_cuartel INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_termino DATE,
    id_estado INT NOT NULL,
    FOREIGN KEY (id_cuartel) REFERENCES general_dim_cuartel(id)
);
```
**Descripción**: Tabla principal de registros de mapeo por temporada y cuartel.

#### **mapeo_fact_registro**
```sql
-- Estructura inferida del código
CREATE TABLE mapeo_fact_registro (
    id VARCHAR(36) PRIMARY KEY,
    id_evaluador VARCHAR(45) NOT NULL,
    hora_registro DATETIME NOT NULL,
    id_planta INT NOT NULL,
    id_tipoplanta VARCHAR(36) NOT NULL,
    imagen TEXT,
    FOREIGN KEY (id_evaluador) REFERENCES general_dim_usuario(id),
    FOREIGN KEY (id_planta) REFERENCES general_dim_planta(id)
);
```
**Descripción**: Tabla de registros individuales de mapeo de plantas.

#### **mapeo_fact_estado_hilera**
```sql
CREATE TABLE mapeo_fact_estado_hilera (
    id VARCHAR(36) PRIMARY KEY,
    id_registro_mapeo VARCHAR(36) NOT NULL,
    id_hilera INT NOT NULL,
    estado ENUM('pendiente', 'en_progreso', 'pausado', 'completado') DEFAULT 'pendiente',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    id_usuario VARCHAR(36),
    observaciones TEXT,
    
    FOREIGN KEY (id_registro_mapeo) REFERENCES mapeo_fact_registromapeo(id) ON DELETE CASCADE,
    FOREIGN KEY (id_hilera) REFERENCES general_dim_hilera(id) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES general_dim_usuario(id) ON DELETE SET NULL,
    
    UNIQUE KEY unique_registro_hilera (id_registro_mapeo, id_hilera)
);
```
**Descripción**: Tabla para manejar el estado individual de cada hilera en un registro de mapeo.

---

### 🏷️ **5. TABLAS DE CLASIFICACIÓN**

#### **mapeo_dim_tipoplanta**
```sql
-- Estructura inferida del código
CREATE TABLE mapeo_dim_tipoplanta (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    factor_productivo DECIMAL(10,2),
    id_empresa INT
);
```
**Descripción**: Tabla de tipos de plantas con factores productivos.

#### **mapeo_dim_estadocatastro**
```sql
-- Estructura inferida del código
CREATE TABLE mapeo_dim_estadocatastro (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);
```
**Descripción**: Tabla de estados del catastro de cuarteles.

---

### 🔧 **6. TABLAS DE CONFIGURACIÓN**

#### **general_dim_labor**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_labor (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);
```
**Descripción**: Tabla de tipos de labores agrícolas.

#### **tarja_dim_unidad**
```sql
-- Estructura inferida del código
CREATE TABLE tarja_dim_unidad (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    id_estado INT DEFAULT 1
);
```
**Descripción**: Tabla de unidades de medida.

#### **general_dim_cecotipo**
```sql
-- Estructura inferida del código
CREATE TABLE general_dim_cecotipo (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);
```
**Descripción**: Tabla de tipos de centros de costo.

---

## 🔗 **RELACIONES PRINCIPALES**

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
- `VARCHAR(36)`: UUIDs para registros de mapeo
- `VARCHAR(45)`: IDs de usuario
- `INT`: IDs autoincrementales para entidades principales

### **Texto:**
- `VARCHAR(255)`: Nombres y descripciones largas
- `VARCHAR(100)`: Correos electrónicos
- `VARCHAR(50)`: Códigos y referencias
- `TEXT`: Observaciones y contenido largo

### **Fechas:**
- `DATE`: Fechas de creación, plantación, etc.
- `DATETIME`: Timestamps de registros

### **Numéricos:**
- `DECIMAL(10,2)`: Superficies, factores productivos
- `INT`: Años, cantidades, estados

### **Enumeraciones:**
- `ENUM`: Estados de hilera ('pendiente', 'en_progreso', 'pausado', 'completado')

---

## 🛡️ **SEGURIDAD Y AUTENTICACIÓN**

### **Tablas de Autenticación:**
- `general_dim_usuario`: Credenciales y perfiles
- `usuario_pivot_sucursal_usuario`: Control de acceso por sucursal

### **Validaciones:**
- Claves foráneas en todas las relaciones
- Restricciones únicas para evitar duplicados
- Estados por defecto para entidades activas

---

## 📈 **ESTADÍSTICAS DE LA BASE DE DATOS**

- **Total de tablas**: 15+ tablas principales
- **Tablas de dimensión**: 10+ (general_dim_*, mapeo_dim_*)
- **Tablas de hechos**: 3+ (mapeo_fact_*)
- **Tablas pivote**: 1 (usuario_pivot_sucursal_usuario)
- **Sistema de autenticación**: JWT con control de acceso por sucursal

---

**📅 Última actualización**: Diciembre 2024  
**🔧 Versión de la API**: 1.0.0  
**📋 Estado**: Documentación completa de tablas identificadas
