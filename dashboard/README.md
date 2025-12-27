# 📊 Dashboard de Estado en Tiempo Real - GW250114

Dashboard Flask para monitorear el estado de disponibilidad y análisis del evento GW250114.

## 🚀 Uso

### Instalación de dependencias

```bash
pip install flask
# O usando requirements.txt
pip install -r requirements.txt
```

### Ejecutar el dashboard

```bash
cd dashboard
python3 estado_gw250114.py
```

El servidor estará disponible en `http://localhost:5000`

### Endpoints disponibles

#### 1. `/estado-gw250114` - Estado en formato JSON

Endpoint API que devuelve el estado actual del evento GW250114 en formato JSON.

**Respuesta cuando NO está disponible:**
```json
{
  "evento": "GW250114",
  "ultima_verificacion": "2025-10-15T11:56:14.036324",
  "disponible": false,
  "estado": "NO_DISPONIBLE",
  "mensaje": "Esperando publicación en GWOSC",
  "eventos_similares": [],
  "timestamp": 1760529374.036332
}
```

**Respuesta cuando SÍ está disponible y analizado:**
```json
{
  "evento": "GW250114",
  "ultima_verificacion": "2025-10-15T11:56:14.036324",
  "disponible": true,
  "estado": "ANALIZADO",
  "eventos_similares": [],
  "timestamp": 1760529374.036332,
  "resultados": {
    "evento": "GW250114",
    "fecha_analisis": "2025-01-14T00:00:00",
    "detectores": {
      "H1": {
        "bayes_factor": 15.3,
        "p_value": 0.0075,
        "snr": 12.4
      },
      "L1": {
        "bayes_factor": 18.7,
        "p_value": 0.0042,
        "snr": 14.2
      }
    }
  }
}
```

#### 2. `/monitor-gw` - Interfaz web de monitoreo

Página web con actualización automática cada 30 segundos que muestra:
- Estado actual del evento GW250114
- Indicador visual (verde si disponible, rojo si no disponible)
- Última verificación
- Actualización automática cada 30 segundos

**Acceso:** `http://localhost:5000/monitor-gw`

## 📁 Estructura de archivos

```
dashboard/
├── estado_gw250114.py    # Aplicación Flask principal
└── README.md             # Esta documentación

resultados/
└── analisis_GW250114.json  # Archivo de resultados (creado por scripts de análisis)
```

## 🔄 Flujo de trabajo

1. El dashboard verifica la existencia del archivo `resultados/analisis_GW250114.json`
2. Si el archivo existe, el dashboard muestra el estado como **ANALIZADO** con los resultados
3. Si no existe, muestra el estado como **NO_DISPONIBLE** esperando datos
4. Los scripts de análisis (como `scripts/analizar_gw250114.py`) generan este archivo cuando GW250114 esté disponible

## 🎨 Características

- **Actualización automática**: La página web se actualiza cada 30 segundos
- **Diseño responsive**: Estilo oscuro optimizado para visualización
- **API REST**: Endpoint JSON para integración con otros sistemas
- **Sin dependencias de templates**: HTML embebido en el código para simplicidad

## 🧪 Testing

Para probar el dashboard sin necesidad de ejecutar un servidor:

```python
from estado_gw250114 import app

with app.test_client() as client:
    # Test estado endpoint
    response = client.get('/estado-gw250114')
    print(response.get_json())
    
    # Test monitor endpoint
    response = client.get('/monitor-gw')
    print(response.status_code)
```

## 🔗 Integración

El dashboard está diseñado para integrarse con:
- Scripts de análisis que generan `resultados/analisis_GW250114.json`
- Sistemas de monitoreo externos vía el endpoint JSON
- Dashboards personalizados que consumen la API REST

## 📝 Notas

- El puerto por defecto es 5000 (configurable en el código)
- El dashboard busca el archivo de resultados en múltiples ubicaciones relativas
- Modo debug habilitado por defecto para desarrollo (desactivar en producción)
