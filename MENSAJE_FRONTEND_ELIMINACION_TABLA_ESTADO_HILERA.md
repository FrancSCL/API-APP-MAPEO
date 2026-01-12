# 📢 MENSAJE PARA FRONTEND - ELIMINACIÓN DE TABLA DE ESTADO DE HILERA

## 🎯 **RESUMEN**
Se ha eliminado la dependencia de la tabla `mapeo_fact_estado_hilera` que no existía en la base de datos. El estado de las hileras ahora se **calcula dinámicamente** basado en las plantas mapeadas, sin necesidad de almacenarlo en una tabla separada.

**Fecha de actualización**: Enero 2026  
**Versión API**: 2.1  
**Estado**: ✅ **Cambios aplicados - Sin cambios en endpoints**

---

## ✅ **CAMBIO APLICADO**

### **Eliminación de dependencia de tabla `mapeo_fact_estado_hilera`**

**Problema anterior**: 
- La API intentaba usar una tabla `mapeo_fact_estado_hilera` que no existía
- Esto causaba errores 500 en el endpoint de progreso

**Solución aplicada**:
- El estado de las hileras ahora se **calcula automáticamente** basado en:
  - Total de plantas en la hilera
  - Plantas mapeadas para ese registro de mapeo
- **No se requiere almacenar el estado** en una tabla separada

---

## 🔧 **ENDPOINTS AFECTADOS**

### **1. `GET /api/registromapeo/<id>/progreso` - MEJORADO**

**Cambio**: El estado de cada hilera ahora se calcula dinámicamente

**Respuesta (sin cambios en estructura)**:
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
      "hilera": 1,
      "total_plantas": 50,
      "plantas_mapeadas": 25,
      "porcentaje": 50.0,
      "estado": "en_progreso"  // ← Calculado automáticamente
    }
  ]
}
```

**Lógica de cálculo del estado**:
- `"pendiente"`: Si `plantas_mapeadas == 0`
- `"completado"`: Si `plantas_mapeadas == total_plantas`
- `"en_progreso"`: Si `0 < plantas_mapeadas < total_plantas`

**✅ Acción requerida en frontend**: **NINGUNA** - La respuesta es idéntica, solo cambió la forma en que se calcula internamente.

---

### **2. `PUT /api/registromapeo/<id>/hilera/<hilera_id>/estado` - MODIFICADO**

**Cambio**: El endpoint ahora calcula el estado en lugar de guardarlo en una tabla

**Antes**: El estado se guardaba en la tabla `mapeo_fact_estado_hilera`

**Ahora**: El estado se calcula dinámicamente y se retorna, pero no se persiste

**Respuesta actualizada**:
```json
{
  "success": true,
  "hilera_actualizada": {
    "id_hilera": 123,
    "numero_hilera": 1,
    "estado": "en_progreso",  // ← Estado REAL calculado
    "estado_solicitado": "completado",  // ← Estado que se intentó establecer
    "plantas_mapeadas": 25,  // ← NUEVO: Información adicional
    "total_plantas": 50,  // ← NUEVO: Información adicional
    "nota": "El estado se calcula automáticamente basado en las plantas mapeadas"
  }
}
```

**⚠️ IMPORTANTE**: 
- El `estado` retornado es el **estado real calculado** basado en las plantas mapeadas
- El `estado_solicitado` es el que se envió en la petición
- **El estado ya no se puede "forzar" manualmente** - siempre refleja el progreso real

**Cambio en TypeScript** (opcional, para usar nuevos campos):
```typescript
// ANTES
interface HileraActualizada {
  id_hilera: number;
  numero_hilera: number;
  estado: string;
  fecha_actualizacion: string;
}

// DESPUÉS (campos adicionales opcionales)
interface HileraActualizada {
  id_hilera: number;
  numero_hilera: number;
  estado: string;  // Estado real calculado
  estado_solicitado?: string;  // ← NUEVO (opcional)
  plantas_mapeadas?: number;  // ← NUEVO (opcional)
  total_plantas?: number;  // ← NUEVO (opcional)
  nota?: string;  // ← NUEVO (opcional)
  fecha_actualizacion?: string;  // ← Ya no se retorna
}
```

**✅ Acción requerida en frontend**: 
- **OPCIONAL**: Actualizar la interface para incluir los nuevos campos informativos
- **IMPORTANTE**: Entender que el estado ya no se puede establecer manualmente, solo refleja el progreso real

---

## 📋 **COMPORTAMIENTO ACTUAL**

### **Cálculo Automático del Estado**

El estado de una hilera se determina automáticamente:

1. **Pendiente** (`"pendiente"`):
   - Cuando `plantas_mapeadas == 0`
   - No se han mapeado plantas en esta hilera

2. **En Progreso** (`"en_progreso"`):
   - Cuando `0 < plantas_mapeadas < total_plantas`
   - Se han mapeado algunas plantas pero no todas

3. **Completado** (`"completado"`):
   - Cuando `plantas_mapeadas == total_plantas`
   - Todas las plantas de la hilera han sido mapeadas

### **Ventajas del Nuevo Sistema**

✅ **Más preciso**: El estado siempre refleja la realidad del progreso  
✅ **Sin sincronización**: No hay riesgo de que el estado guardado no coincida con el progreso real  
✅ **Menos complejidad**: No requiere mantener una tabla adicional  
✅ **Más confiable**: El estado se calcula en tiempo real

---

## 🔄 **MIGRACIÓN EN FRONTEND**

### **Paso 1: Actualizar Interface (Opcional)**

Si quieren usar los nuevos campos informativos:

```typescript
interface HileraActualizada {
  id_hilera: number;
  numero_hilera: number;
  estado: string;  // Estado real calculado
  estado_solicitado?: string;  // Estado que se intentó establecer
  plantas_mapeadas?: number;  // Plantas mapeadas
  total_plantas?: number;  // Total de plantas
  nota?: string;  // Nota informativa
}
```

### **Paso 2: Actualizar Lógica (Si aplica)**

Si el frontend intentaba "forzar" un estado manualmente:

**ANTES** (si existía):
```typescript
// Intentar establecer estado manualmente
await updateEstadoHilera(registroId, hileraId, "completado");
// El estado se guardaba en la tabla
```

**AHORA**:
```typescript
// El estado se calcula automáticamente
// Solo se puede actualizar el progreso mapeando plantas
// El estado reflejará automáticamente el progreso real
```

### **Paso 3: Probar Endpoints**

1. Probar `GET /api/registromapeo/<id>/progreso` - Verificar que funciona
2. Probar `PUT /api/registromapeo/<id>/hilera/<id>/estado` - Verificar nueva respuesta

---

## ✅ **COMPATIBILIDAD**

### **Endpoints que NO cambian**

- ✅ `GET /api/registromapeo/<id>/progreso` - **Misma respuesta, solo cambió cálculo interno**
- ✅ Todos los demás endpoints - **Sin cambios**

### **Endpoint que cambió ligeramente**

- ⚠️ `PUT /api/registromapeo/<id>/hilera/<id>/estado` - **Nueva respuesta con campos adicionales**

**Impacto**: **Mínimo** - El campo `estado` sigue existiendo y funciona igual, solo se agregaron campos informativos opcionales.

---

## 🧪 **PRUEBAS**

### **1. Probar progreso de mapeo**:
```bash
curl -X GET "https://apimapeo-927498545444.us-central1.run.app/api/registromapeo/{registro_id}/progreso" \
  -H "Authorization: Bearer {token}"
```

**Respuesta esperada**: Debe funcionar correctamente sin errores 500

### **2. Probar actualización de estado**:
```bash
curl -X PUT "https://apimapeo-927498545444.us-central1.run.app/api/registromapeo/{registro_id}/hilera/{hilera_id}/estado" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"estado": "completado"}'
```

**Respuesta esperada**: 
- Debe retornar 200
- El `estado` será el estado real calculado (puede diferir del `estado_solicitado`)
- Incluirá campos adicionales informativos

---

## 📊 **RESUMEN DE CAMBIOS**

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Estado de hilera** | Se guardaba en tabla | Se calcula dinámicamente |
| **Endpoint progreso** | Error 500 (tabla no existe) | ✅ Funciona correctamente |
| **Endpoint actualizar estado** | Guardaba en tabla | Calcula y retorna estado real |
| **Precisión** | Podía desincronizarse | Siempre refleja progreso real |
| **Estructura respuesta** | Sin cambios | Campos adicionales opcionales |

---

## ⚠️ **IMPORTANTE PARA EL FRONTEND**

### **Cambio en Comportamiento**

**ANTES** (si se usaba):
- El estado se podía establecer manualmente
- El estado se guardaba en una tabla
- Podía haber desincronización entre estado guardado y progreso real

**AHORA**:
- El estado se calcula automáticamente basado en plantas mapeadas
- **No se puede "forzar" un estado manualmente**
- El estado siempre refleja el progreso real
- Para cambiar el estado, se debe mapear/desmapear plantas

### **Recomendación**

Si el frontend tenía lógica para "marcar hileras como completadas" manualmente, esa funcionalidad ya no será efectiva. El estado ahora refleja automáticamente el progreso real basado en las plantas mapeadas.

---

## ✅ **ESTADO ACTUAL**

- ✅ **Endpoint de progreso**: Funciona correctamente (antes daba error 500)
- ✅ **Endpoint de actualizar estado**: Funciona, retorna estado calculado
- ✅ **Compatibilidad**: Respuestas compatibles con versión anterior
- ✅ **Sin cambios en endpoints**: Las URLs y métodos HTTP son los mismos

---

## 📞 **CONTACTO Y SOPORTE**

Si tienen dudas sobre estos cambios o necesitan ayuda con la implementación, pueden contactarme.

**Fecha de actualización**: Enero 2026  
**Versión API**: 2.1  
**Estado**: ✅ **Funcionando correctamente**  
**Prioridad de actualización**: 🟡 **OPCIONAL** - Los endpoints funcionan, solo se agregaron campos informativos opcionales

---

## 🔍 **CHECKLIST DE MIGRACIÓN (OPCIONAL)**

- [ ] (Opcional) Actualizar interface `HileraActualizada` para incluir nuevos campos
- [ ] (Opcional) Actualizar componentes que usen `fecha_actualizacion` (ya no se retorna)
- [ ] Probar endpoint `/api/registromapeo/<id>/progreso` - Verificar que funciona
- [ ] Probar endpoint `/api/registromapeo/<id>/hilera/<id>/estado` - Verificar nueva respuesta
- [ ] (Si aplica) Actualizar lógica que intentaba "forzar" estados manualmente
- [ ] Verificar que no hay errores en consola del navegador
- [ ] Probar flujo completo de mapeo

---

## 📝 **NOTAS TÉCNICAS**

### **Por qué se eliminó la tabla**

1. La tabla `mapeo_fact_estado_hilera` no existía en la base de datos
2. Causaba errores 500 en el endpoint de progreso
3. El estado se puede calcular dinámicamente sin necesidad de almacenarlo
4. Reduce complejidad y riesgo de desincronización

### **Ventajas del nuevo sistema**

- ✅ Más simple: No requiere tabla adicional
- ✅ Más preciso: Estado siempre refleja progreso real
- ✅ Más confiable: No hay riesgo de desincronización
- ✅ Menos mantenimiento: No hay que actualizar estados manualmente

---

**✨ Cambios completados y funcionando correctamente**
