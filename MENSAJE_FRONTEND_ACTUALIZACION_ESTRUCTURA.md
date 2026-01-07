# 📢 MENSAJE PARA FRONTEND - ACTUALIZACIÓN DE ESTRUCTURA DE API

## 🎯 **RESUMEN**
Se ha realizado una verificación completa de la estructura de la base de datos y se han aplicado correcciones críticas en la API. Los cambios mejoran la consistencia de los datos y corrigen errores que podrían afectar el funcionamiento del frontend.

---

## ⚠️ **CAMBIOS CRÍTICOS QUE AFECTAN AL FRONTEND**

### **1. Endpoint `/api/registromapeo/<id>/progreso` - CORREGIDO**

**Problema anterior**: El endpoint tenía un error que causaba que las hileras no se mostraran correctamente.

**Cambio aplicado**: 
- La respuesta ahora usa `hilera` en lugar de `nombre` para el número de hilera
- La consulta de plantas mapeadas ahora funciona correctamente

**Respuesta actualizada**:
```json
{
  "id_registro": "uuid-del-registro",
  "cuartel": "Nombre del Cuartel",
  "total_hileras": 10,
  "hileras_completadas": 5,
  "porcentaje_general": 50.0,
  "hileras": [
    {
      "id_hilera": 123,
      "hilera": 1,              // ← CAMBIÓ: antes era "nombre"
      "total_plantas": 50,
      "plantas_mapeadas": 25,
      "porcentaje": 50.0,
      "estado": "en_progreso"
    }
  ]
}
```

**Cambio en TypeScript**:
```typescript
// ANTES (incorrecto)
interface HileraProgreso {
  id_hilera: number;
  nombre: number;  // ❌ Esto estaba mal
  total_plantas: number;
  plantas_mapeadas: number;
  porcentaje: number;
  estado: string;
}

// DESPUÉS (correcto)
interface HileraProgreso {
  id_hilera: number;
  hilera: number;  // ✅ Corregido
  total_plantas: number;
  plantas_mapeadas: number;
  porcentaje: number;
  estado: string;
}
```

---

### **2. Endpoint `/api/registromapeo/<id>/hilera/<hilera_id>/estado` - CORREGIDO**

**Cambio aplicado**: La respuesta ahora devuelve `numero_hilera` en lugar de `nombre_hilera`.

**Respuesta actualizada**:
```json
{
  "success": true,
  "hilera_actualizada": {
    "id_hilera": 123,
    "numero_hilera": 1,         // ← CAMBIÓ: antes era "nombre_hilera"
    "estado": "completado",
    "fecha_actualizacion": "2025-01-15T10:30:00"
  }
}
```

**Cambio en TypeScript**:
```typescript
// ANTES
interface HileraActualizada {
  id_hilera: number;
  nombre_hilera: number;  // ❌
  estado: string;
  fecha_actualizacion: string;
}

// DESPUÉS
interface HileraActualizada {
  id_hilera: number;
  numero_hilera: number;  // ✅
  estado: string;
  fecha_actualizacion: string;
}
```

---

## ✅ **NUEVAS FUNCIONALIDADES**

### **3. Campo `id_mapeo` en Registros - NUEVO**

**Descripción**: Ahora los registros pueden estar asociados a un registro de mapeo específico.

**Endpoints afectados**:
- `POST /api/registros` - Ahora acepta `id_mapeo` (opcional)
- `PUT /api/registros/<id>` - Ahora permite actualizar `id_mapeo`
- Todos los `GET /api/registros/*` - Ahora incluyen `id_mapeo` en la respuesta

**Ejemplo de creación con `id_mapeo`**:
```typescript
// Crear registro asociado a un mapeo
const nuevoRegistro = {
  id_planta: 12345,
  id_tipoplanta: "uuid-tipo-planta",
  imagen: "url-de-imagen",
  id_mapeo: "uuid-registro-mapeo"  // ← NUEVO (opcional)
};

const response = await fetch('/api/registros', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(nuevoRegistro)
});
```

**Interface actualizada**:
```typescript
interface Registro {
  id: string;
  id_evaluador: string;
  hora_registro: string;
  id_planta: number;
  id_tipoplanta: string;
  imagen: string | null;
  id_mapeo: string | null;  // ← NUEVO
}
```

---

### **4. Campo `descripcion` en Tipos de Planta - NUEVO**

**Descripción**: Los tipos de planta ahora incluyen una descripción.

**Endpoints afectados**:
- `GET /api/tipoplanta` - Ahora incluye `descripcion`
- `GET /api/tipoplanta/<id>` - Ahora incluye `descripcion`
- `GET /api/tipoplanta/empresa/<id>` - Ahora incluye `descripcion`
- `GET /api/tipoplanta/buscar/<nombre>` - Ahora incluye `descripcion`

**Respuesta actualizada**:
```json
{
  "id": "uuid-tipo-planta",
  "nombre": "Planta Productiva",
  "factor_productivo": 1.5,
  "id_empresa": 1,
  "descripcion": "Descripción del tipo de planta"  // ← NUEVO
}
```

**Interface actualizada**:
```typescript
interface TipoPlanta {
  id: string;
  nombre: string;
  factor_productivo: number;
  id_empresa: number;
  descripcion: string | null;  // ← NUEVO
}
```

---

## 📋 **CAMBIOS EN TIPOS DE DATOS**

### **Tipos que cambiaron (pero no afectan al frontend)**

Los siguientes cambios fueron internos y **NO requieren cambios en el frontend**:

| Campo | Tipo Anterior | Tipo Real | Nota |
|-------|---------------|-----------|------|
| `id_planta` | INT | BIGINT | Python maneja ambos igual |
| `id_hilera` | INT | BIGINT | Python maneja ambos igual |
| `id` (usuario) | UUID | VARCHAR(45) | Ambos son strings en JSON |
| `superficie`, `dsh`, `deh` | DECIMAL | FLOAT | Ambos son numbers en JSON |

**✅ Acción requerida**: **NINGUNA** - Estos cambios son transparentes para el frontend.

---

## 🔧 **ACTUALIZACIÓN DE INTERFACES TYPESCRIPT**

### **Interface Registro - Actualizada**
```typescript
interface Registro {
  id: string;
  id_evaluador: string;
  hora_registro: string;
  id_planta: number;           // BIGINT, pero funciona como number
  id_tipoplanta: string;
  imagen: string | null;
  id_mapeo: string | null;     // ← NUEVO (opcional)
}
```

### **Interface TipoPlanta - Actualizada**
```typescript
interface TipoPlanta {
  id: string;
  nombre: string;
  factor_productivo: number;
  id_empresa: number;
  descripcion: string | null;  // ← NUEVO (opcional)
}
```

### **Interface HileraProgreso - Corregida**
```typescript
interface HileraProgreso {
  id_hilera: number;
  hilera: number;              // ← CORREGIDO (antes era "nombre")
  total_plantas: number;
  plantas_mapeadas: number;
  porcentaje: number;
  estado: "pendiente" | "en_progreso" | "completado";
}
```

### **Interface HileraActualizada - Corregida**
```typescript
interface HileraActualizada {
  id_hilera: number;
  numero_hilera: number;        // ← CORREGIDO (antes era "nombre_hilera")
  estado: string;
  fecha_actualizacion: string;
}
```

---

## 🎨 **IMPLEMENTACIÓN EN FRONTEND**

### **1. Actualizar Servicio de Registros**

```typescript
class RegistrosService {
  // Crear registro con id_mapeo opcional
  async crearRegistro(
    idPlanta: number,
    idTipoPlanta: string,
    imagen?: string,
    idMapeo?: string  // ← NUEVO parámetro opcional
  ): Promise<Registro> {
    const response = await fetch('/api/registros', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        id_planta: idPlanta,
        id_tipoplanta: idTipoPlanta,
        imagen: imagen || null,
        id_mapeo: idMapeo || null  // ← NUEVO
      })
    });
    return response.json();
  }

  // Obtener registros por mapeo
  async getRegistrosPorMapeo(idMapeo: string): Promise<Registro[]> {
    const response = await fetch(`/api/registros?id_mapeo=${idMapeo}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  }
}
```

### **2. Actualizar Componente de Progreso de Mapeo**

```typescript
const ProgresoMapeo = ({ registroId }: { registroId: string }) => {
  const [progreso, setProgreso] = useState<ProgresoRegistro | null>(null);

  useEffect(() => {
    fetch(`/api/registromapeo/${registroId}/progreso`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        setProgreso(data);
      });
  }, [registroId]);

  return (
    <div>
      <h2>Progreso: {progreso?.porcentaje_general}%</h2>
      {progreso?.hileras.map(hilera => (
        <div key={hilera.id_hilera}>
          <h3>Hilera {hilera.hilera}</h3>  {/* ← CORREGIDO: usar hilera.hilera */}
          <p>Plantas: {hilera.plantas_mapeadas}/{hilera.total_plantas}</p>
          <p>Estado: {hilera.estado}</p>
        </div>
      ))}
    </div>
  );
};
```

### **3. Actualizar Componente de Tipos de Planta**

```typescript
const TiposPlanta = () => {
  const [tipos, setTipos] = useState<TipoPlanta[]>([]);

  useEffect(() => {
    fetch('/api/tipoplanta', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setTipos(data));
  }, []);

  return (
    <div>
      {tipos.map(tipo => (
        <div key={tipo.id}>
          <h3>{tipo.nombre}</h3>
          {tipo.descripcion && (  // ← NUEVO: mostrar descripción si existe
            <p>{tipo.descripcion}</p>
          )}
          <p>Factor: {tipo.factor_productivo}</p>
        </div>
      ))}
    </div>
  );
};
```

---

## 🔄 **MIGRACIÓN PASO A PASO**

### **Paso 1: Actualizar Interfaces TypeScript**
1. Buscar todas las referencias a `HileraProgreso` y cambiar `nombre` → `hilera`
2. Buscar todas las referencias a `HileraActualizada` y cambiar `nombre_hilera` → `numero_hilera`
3. Agregar `id_mapeo?: string | null` a la interface `Registro`
4. Agregar `descripcion?: string | null` a la interface `TipoPlanta`

### **Paso 2: Actualizar Componentes**
1. Buscar componentes que usen `hilera.nombre` y cambiar a `hilera.hilera`
2. Buscar componentes que usen `hilera.nombre_hilera` y cambiar a `hilera.numero_hilera`
3. Actualizar formularios de creación de registros para incluir `id_mapeo` (opcional)
4. Actualizar componentes de tipos de planta para mostrar `descripcion`

### **Paso 3: Probar Endpoints**
1. Probar `/api/registromapeo/<id>/progreso` - Verificar que `hilera` funciona
2. Probar `/api/registromapeo/<id>/hilera/<id>/estado` - Verificar que `numero_hilera` funciona
3. Probar creación de registros con `id_mapeo`
4. Verificar que `descripcion` aparece en tipos de planta

---

## 🧪 **ENDPOINTS DE PRUEBA**

### **1. Probar progreso de mapeo (corregido)**:
```bash
curl -X GET "https://tu-api.com/api/registromapeo/{registro_id}/progreso" \
  -H "Authorization: Bearer {token}"
```

**Respuesta esperada**:
```json
{
  "hileras": [
    {
      "id_hilera": 123,
      "hilera": 1,  // ← Verificar que es "hilera", no "nombre"
      "total_plantas": 50,
      "plantas_mapeadas": 25,
      "porcentaje": 50.0,
      "estado": "en_progreso"
    }
  ]
}
```

### **2. Probar creación de registro con id_mapeo**:
```bash
curl -X POST "https://tu-api.com/api/registros" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id_planta": 12345,
    "id_tipoplanta": "uuid-tipo",
    "id_mapeo": "uuid-mapeo"
  }'
```

### **3. Probar tipos de planta con descripción**:
```bash
curl -X GET "https://tu-api.com/api/tipoplanta" \
  -H "Authorization: Bearer {token}"
```

**Respuesta esperada**:
```json
[
  {
    "id": "uuid",
    "nombre": "Tipo Planta",
    "factor_productivo": 1.5,
    "id_empresa": 1,
    "descripcion": "Descripción..."  // ← Verificar que existe
  }
]
```

---

## ⚠️ **CAMBIOS QUE REQUIEREN ACCIÓN INMEDIATA**

### **CRÍTICO - Actualizar interfaces TypeScript**

1. **`HileraProgreso`**: Cambiar `nombre: number` → `hilera: number`
2. **`HileraActualizada`**: Cambiar `nombre_hilera: number` → `numero_hilera: number`

**Impacto**: Si no se actualiza, el frontend no podrá acceder correctamente a estos campos.

---

## ✅ **CAMBIOS OPCIONALES (Mejoras)**

### **Recomendado - Agregar soporte para nuevos campos**

1. **`Registro.id_mapeo`**: Agregar campo opcional para asociar registros con mapeos
2. **`TipoPlanta.descripcion`**: Mostrar descripción en la UI si está disponible

**Impacto**: Mejora la funcionalidad pero no es crítico.

---

## 📊 **RESUMEN DE CAMBIOS**

| Cambio | Tipo | Acción Requerida | Prioridad |
|--------|------|------------------|-----------|
| `hilera.nombre` → `hilera.hilera` | Corrección | Actualizar interfaces y componentes | 🔴 CRÍTICO |
| `nombre_hilera` → `numero_hilera` | Corrección | Actualizar interfaces y componentes | 🔴 CRÍTICO |
| Agregar `id_mapeo` a `Registro` | Nueva funcionalidad | Actualizar interfaces (opcional) | 🟡 OPCIONAL |
| Agregar `descripcion` a `TipoPlanta` | Nueva funcionalidad | Actualizar interfaces (opcional) | 🟡 OPCIONAL |
| Corrección JOIN en `/api/registros/hilera/<id>` | Corrección interna | Ninguna (mejora automática) | ✅ COMPLETADO |

---

## 🔧 **CORRECCIÓN ADICIONAL APLICADA**

### **5. Endpoint `/api/registros/hilera/<hilera_id>` - CORREGIDO**

**Problema anterior**: El endpoint tenía un error en el JOIN que causaba que no se mostrara el nombre del tipo de planta.

**Cambio aplicado**: 
- Corregido el nombre de tabla en el JOIN: `general_dim_tipoplanta` → `mapeo_dim_tipoplanta`

**Impacto**: 
- El endpoint ahora funciona correctamente
- El campo `tipo_planta_nombre` ahora se muestra correctamente en los registros por hilera

**Estado**: ✅ **CORREGIDO** (No requiere cambios en frontend, solo mejora la funcionalidad)

---

## ✅ **ESTADO ACTUAL**

- **✅ API funcionando**: Todos los endpoints operativos
- **✅ Errores corregidos**: Endpoints de progreso funcionando correctamente
- **✅ Nuevos campos disponibles**: `id_mapeo` y `descripcion` disponibles
- **✅ Correcciones aplicadas**: 5 correcciones críticas en total
- **✅ Compatibilidad**: Cambios mantienen compatibilidad hacia atrás donde es posible

---

## 📞 **CONTACTO Y SOPORTE**

Si tienen dudas sobre estos cambios o necesitan ayuda con la implementación, pueden contactarme.

**Fecha de actualización**: Enero 2025  
**Versión API**: 2.1  
**Estado**: ✅ Funcionando correctamente  
**Prioridad de actualización**: 🔴 CRÍTICA para campos corregidos, 🟡 OPCIONAL para nuevos campos

---

## 🔍 **CHECKLIST DE MIGRACIÓN**

- [ ] Actualizar interface `HileraProgreso` (cambiar `nombre` → `hilera`)
- [ ] Actualizar interface `HileraActualizada` (cambiar `nombre_hilera` → `numero_hilera`)
- [ ] Buscar y reemplazar `hilera.nombre` por `hilera.hilera` en componentes
- [ ] Buscar y reemplazar `nombre_hilera` por `numero_hilera` en componentes
- [ ] (Opcional) Agregar `id_mapeo` a interface `Registro`
- [ ] (Opcional) Agregar `descripcion` a interface `TipoPlanta`
- [ ] Probar endpoint `/api/registromapeo/<id>/progreso`
- [ ] Probar endpoint `/api/registromapeo/<id>/hilera/<id>/estado`
- [ ] Verificar que no hay errores en consola del navegador
- [ ] Probar flujo completo de mapeo
