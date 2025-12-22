# 📢 MENSAJE PARA FRONTEND - ACTUALIZACIÓN DE CUARTELES CON SUCURSALES

## 🎯 **RESUMEN**
Se han actualizado los endpoints de cuarteles para incluir información de sucursales a través de la tabla `general_dim_ceco`. Ahora el frontend puede filtrar cuarteles por sucursal y mostrar información completa.

---

## 🔧 **ENDPOINTS ACTUALIZADOS**

### **1. `/api/cuarteles/activos` - Mejorado**
**Descripción**: Obtiene todos los cuarteles activos con información de sucursal incluida.

**Respuesta actualizada**:
```json
{
  "id": "1100200401",
  "id_ceco": 11002004,
  "nombre": "ALF 1 P1 MA CH",
  "ceco_nombre": "ALF 1 P1 MA CH",
  "id_sucursal": 110,
  "sucursal_nombre": "PESEBRERAS",
  "subdivisionesplanta": 1,
  "superficie": 1.43,
  "ano_plantacion": 2021,
  "dsh": 2.0,
  "deh": 4.0,
  "id_variedad": 5005,
  "id_estado": 1
}
```

### **2. `/api/cuarteles/sucursal/{sucursal_id}` - Nuevo**
**Descripción**: Filtra cuarteles por sucursal específica.

**Ejemplo de uso**:
```
GET /api/cuarteles/sucursal/110
```

**Respuesta**:
```json
[
  {
    "id": "1100200401",
    "nombre": "ALF 1 P1 MA CH",
    "sucursal_nombre": "PESEBRERAS",
    "id_sucursal": 110,
    "ceco_nombre": "ALF 1 P1 MA CH"
  }
]
```

---

## 📋 **CAMPOS NUEVOS AGREGADOS**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `ceco_nombre` | string | Nombre del centro de costo |
| `id_sucursal` | number | ID de la sucursal |
| `sucursal_nombre` | string | Nombre de la sucursal |

---

## 🔄 **CAMBIOS EN INTERFACES TYPESCRIPT**

### **Interface Cuartel Actualizada**:
```typescript
interface Cuartel {
  id: string;
  id_ceco: number;
  nombre: string;
  ceco_nombre: string;        // ← NUEVO
  id_sucursal: number;        // ← NUEVO
  sucursal_nombre: string;    // ← NUEVO
  subdivisionesplanta: number;
  id_tiposubdivision: number | null;
  superficie: number;
  ano_plantacion: number;
  dsh: number;
  deh: number;
  id_propiedad: number;
  id_portainjerto: number;
  id_estado: number;
  fecha_baja: string | null;
  id_estadoproductivo: number;
  n_hileras: number;
  id_estadocatastro: number;
}
```

---

## 🎨 **IMPLEMENTACIÓN EN FRONTEND**

### **1. Servicio de Cuarteles**:
```typescript
class CuartelesService {
  // Obtener todos los cuarteles con información de sucursal
  async getCuartelesActivos(): Promise<Cuartel[]> {
    const response = await fetch('/api/cuarteles/activos', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.json();
  }

  // Obtener cuarteles por sucursal específica
  async getCuartelesPorSucursal(sucursalId: number): Promise<Cuartel[]> {
    const response = await fetch(`/api/cuarteles/sucursal/${sucursalId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.json();
  }
}
```

### **2. Componente de Filtro por Sucursal**:
```typescript
const CuartelesFiltrados = () => {
  const [cuarteles, setCuarteles] = useState<Cuartel[]>([]);
  const [sucursalSeleccionada, setSucursalSeleccionada] = useState<number | null>(null);

  useEffect(() => {
    if (sucursalSeleccionada) {
      // Filtrar por sucursal específica
      cuartelesService.getCuartelesPorSucursal(sucursalSeleccionada)
        .then(setCuarteles);
    } else {
      // Mostrar todos los cuarteles
      cuartelesService.getCuartelesActivos()
        .then(setCuarteles);
    }
  }, [sucursalSeleccionada]);

  return (
    <div>
      <select onChange={(e) => setSucursalSeleccionada(Number(e.target.value))}>
        <option value="">Todas las sucursales</option>
        <option value="110">PESEBRERAS</option>
        <option value="102">SAN MANUEL</option>
        {/* Agregar más sucursales según sea necesario */}
      </select>
      
      {cuarteles.map(cuartel => (
        <div key={cuartel.id}>
          <h3>{cuartel.nombre}</h3>
          <p>Sucursal: {cuartel.sucursal_nombre}</p>
          <p>CECO: {cuartel.ceco_nombre}</p>
        </div>
      ))}
    </div>
  );
};
```

### **3. Agrupación por Sucursal**:
```typescript
const CuartelesAgrupados = () => {
  const [cuarteles, setCuarteles] = useState<Cuartel[]>([]);

  useEffect(() => {
    cuartelesService.getCuartelesActivos().then(setCuarteles);
  }, []);

  // Agrupar cuarteles por sucursal
  const cuartelesPorSucursal = cuarteles.reduce((acc, cuartel) => {
    const sucursal = cuartel.sucursal_nombre;
    if (!acc[sucursal]) {
      acc[sucursal] = [];
    }
    acc[sucursal].push(cuartel);
    return acc;
  }, {} as Record<string, Cuartel[]>);

  return (
    <div>
      {Object.entries(cuartelesPorSucursal).map(([sucursal, cuarteles]) => (
        <div key={sucursal}>
          <h2>{sucursal}</h2>
          {cuarteles.map(cuartel => (
            <div key={cuartel.id}>{cuartel.nombre}</div>
          ))}
        </div>
      ))}
    </div>
  );
};
```

---

## 🧪 **ENDPOINTS DE PRUEBA**

### **Probar endpoint general**:
```bash
curl -X GET "https://apimapeo-927498545444.us-central1.run.app/api/cuarteles/activos" \
  -H "Authorization: Bearer {token}"
```

### **Probar endpoint por sucursal**:
```bash
curl -X GET "https://apimapeo-927498545444.us-central1.run.app/api/cuarteles/sucursal/110" \
  -H "Authorization: Bearer {token}"
```

---

## ✅ **ESTADO ACTUAL**

- **✅ API funcionando**: Todos los endpoints operativos
- **✅ Información de sucursal**: Incluida en las respuestas
- **✅ Filtrado por sucursal**: Endpoint específico disponible
- **✅ Datos consistentes**: Estructura actualizada en todos los endpoints

---

## 📞 **CONTACTO**

Si necesitan más detalles sobre la implementación o tienen dudas sobre los nuevos campos, pueden contactarme.

**Fecha de actualización**: 10 de Septiembre 2025  
**Versión API**: 2.1  
**Estado**: ✅ Funcionando correctamente
