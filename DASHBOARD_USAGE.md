# 📊 Guía de Uso del Dashboard GW250114

## Resumen
El Dashboard de Estado en Tiempo Real para GW250114 permite monitorear la disponibilidad y resultados del análisis del evento gravitacional GW250114 en tiempo real.

## 🚀 Inicio Rápido

### Opción 1: Usando Makefile (Recomendado)
```bash
make setup      # Instalar dependencias (solo la primera vez)
make dashboard  # Iniciar el dashboard
```

### Opción 2: Ejecución directa
```bash
pip install flask
python3 scripts/run_dashboard.py
```

### Opción 3: Desde el directorio dashboard
```bash
cd dashboard
python3 estado_gw250114.py
```

## 🌐 Acceso al Dashboard

Una vez iniciado, el dashboard estará disponible en:
- **Página de Monitoreo**: http://localhost:5000/monitor-gw
- **API JSON**: http://localhost:5000/estado-gw250114

## 📡 Endpoints

### 1. `/estado-gw250114` (JSON API)

Devuelve el estado actual del evento en formato JSON.

**Ejemplo de respuesta (sin resultados):**
```json
{
  "evento": "GW250114",
  "ultima_verificacion": "2025-10-15T12:00:00",
  "disponible": false,
  "estado": "NO_DISPONIBLE",
  "mensaje": "Esperando publicación en GWOSC",
  "eventos_similares": [],
  "timestamp": 1760530000.0
}
```

**Ejemplo de respuesta (con resultados):**
```json
{
  "evento": "GW250114",
  "ultima_verificacion": "2025-10-15T12:00:00",
  "disponible": true,
  "estado": "ANALIZADO",
  "eventos_similares": [],
  "timestamp": 1760530000.0,
  "resultados": {
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

### 2. `/monitor-gw` (Interfaz Web)

Página HTML con actualización automática que muestra:
- 🎯 Estado visual del evento (verde=disponible, rojo=no disponible)
- ⏰ Última verificación
- 🔄 Actualización automática cada 30 segundos

## 🧪 Pruebas

Para ejecutar los tests del dashboard:
```bash
python3 scripts/test_dashboard.py
```

Los tests verifican:
- ✅ Endpoint JSON sin resultados
- ✅ Endpoint JSON con resultados
- ✅ Página de monitoreo HTML
- ✅ Estructura correcta del JSON
- ✅ Múltiples peticiones consecutivas

## 📁 Archivos de Resultados

El dashboard busca automáticamente el archivo:
```
resultados/analisis_GW250114.json
```

Este archivo es generado por los scripts de análisis (como `scripts/analizar_gw250114.py`) cuando detectan y analizan el evento GW250114.

### Formato del archivo de resultados

```json
{
  "evento": "GW250114",
  "fecha_analisis": "2025-01-14T00:00:00",
  "detectores": {
    "H1": {
      "bayes_factor": 15.3,
      "p_value": 0.0075,
      "snr": 12.4,
      "chi2_single": 1.05,
      "chi2_double": 0.92
    },
    "L1": {
      "bayes_factor": 18.7,
      "p_value": 0.0042,
      "snr": 14.2,
      "chi2_single": 1.12,
      "chi2_double": 0.88
    }
  },
  "frecuencia_objetivo": 141.7001,
  "significancia_estadistica": "ALTA",
  "conclusion": "Componente en 141.7 Hz detectada con alta significancia"
}
```

## 🔧 Configuración

### Puerto
Por defecto usa el puerto 5000. Para cambiarlo, edita `dashboard/estado_gw250114.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambia 5000 al puerto deseado
```

### Modo Debug
En producción, desactiva el modo debug:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 🔗 Integración con Otros Sistemas

### Consultar desde Python
```python
import requests

response = requests.get('http://localhost:5000/estado-gw250114')
estado = response.json()

if estado['disponible']:
    print("GW250114 está disponible!")
    print(f"Bayes Factor H1: {estado['resultados']['detectores']['H1']['bayes_factor']}")
```

### Consultar desde línea de comandos
```bash
curl http://localhost:5000/estado-gw250114 | jq .
```

### Monitoreo Automático
Puedes crear un script que consulte periódicamente:
```bash
#!/bin/bash
while true; do
    curl -s http://localhost:5000/estado-gw250114 | jq '.disponible'
    sleep 300  # Verificar cada 5 minutos
done
```

## 🛠️ Solución de Problemas

### Error: "Address already in use"
El puerto 5000 está ocupado. Cambia el puerto en el código o detén el proceso que lo usa:
```bash
lsof -i :5000  # Ver qué proceso usa el puerto
```

### Error: "No module named 'flask'"
Instala Flask:
```bash
pip install flask
# O
pip install -r requirements.txt
```

### El dashboard no encuentra resultados
Verifica que existe el archivo `resultados/analisis_GW250114.json`. Si no existe, el dashboard mostrará estado "NO_DISPONIBLE" (comportamiento esperado).

## 📚 Documentación Adicional

- **Dashboard README**: `dashboard/README.md`
- **Tests**: `scripts/test_dashboard.py`
- **Script de ejecución**: `scripts/run_dashboard.py`

## 🎯 Casos de Uso

### 1. Monitoreo durante análisis
Inicia el dashboard mientras ejecutas análisis:
```bash
# Terminal 1
make dashboard

# Terminal 2
python3 scripts/analizar_gw250114.py
```

### 2. Visualización de resultados existentes
Si ya tienes resultados en `resultados/analisis_GW250114.json`:
```bash
make dashboard
# Abre http://localhost:5000/monitor-gw
```

### 3. API para automatización
Integra con sistemas de notificación:
```python
import requests
import time

while True:
    r = requests.get('http://localhost:5000/estado-gw250114')
    data = r.json()
    
    if data['disponible']:
        # Enviar notificación
        send_alert("GW250114 disponible!")
        break
    
    time.sleep(1800)  # Esperar 30 minutos
```

## ✨ Características Destacadas

- ✅ Sin dependencias de templates (HTML embebido)
- ✅ Auto-actualización en frontend
- ✅ Búsqueda flexible de archivos de resultados
- ✅ API REST completa
- ✅ Tests automatizados
- ✅ Integración con Makefile
- ✅ Documentación completa

## 📄 Licencia

Este dashboard es parte del proyecto GW250114 Analysis.
