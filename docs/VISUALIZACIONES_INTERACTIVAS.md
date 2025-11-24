# Visualizaciones Interactivas y Generación de Informes

## 📋 Descripción

Este módulo proporciona herramientas avanzadas para crear visualizaciones interactivas y generar informes automáticos del análisis de ondas gravitacionales. Incluye:

- **Visualizaciones Interactivas**: Gráficos explorables con Plotly
- **Generación de Informes**: Informes HTML y PDF automáticos
- **Dashboard Web**: Panel de monitoreo en tiempo real

## 🚀 Características Principales

### 1. Visualizaciones Interactivas

- ✅ Espectros de potencia interactivos con zoom y pan
- ✅ Series temporales explorables
- ✅ Espectrogramas dinámicos
- ✅ Dashboards comparativos multi-detector
- ✅ Gráficos de SNR para múltiples eventos
- ✅ Exportación a HTML, PNG, SVG, PDF

### 2. Generación de Informes

- ✅ Informes HTML con gráficos embebidos
- ✅ Generación de PDF (opcional con WeasyPrint)
- ✅ Templates personalizables
- ✅ Métricas y hallazgos destacados
- ✅ Tablas de resultados detallados
- ✅ Secciones de conclusiones

### 3. Dashboard Web

- ✅ Monitoreo en tiempo real
- ✅ Sistema de alertas automáticas
- ✅ Gráficos actualizados dinámicamente
- ✅ API REST completa
- ✅ Stream de datos con Server-Sent Events (SSE)
- ✅ Panel de análisis activos

## 📦 Instalación

### Dependencias Requeridas

```bash
pip install plotly>=5.18.0
pip install kaleido>=0.2.1
pip install jinja2>=3.1.2
pip install flask>=2.0.0
pip install numpy scipy matplotlib
```

### Dependencias Opcionales

```bash
# Para generación de PDF
pip install weasyprint>=60.0
```

## 💻 Uso

### Visualizaciones Interactivas

```python
from visualizaciones_interactivas import VisualizadorInteractivo
import numpy as np

# Crear visualizador
viz = VisualizadorInteractivo(theme="plotly_dark")

# Datos de ejemplo
frecuencias = np.linspace(100, 200, 1000)
potencias = np.random.lognormal(0, 1, 1000) * 1e-40

# Crear espectro interactivo
fig = viz.crear_espectro_interactivo(
    frecuencias=frecuencias,
    potencias=potencias,
    frecuencia_objetivo=141.7,
    detector="H1",
    snr=8.5
)

# Guardar como HTML
viz.guardar_html(fig, 'espectro_interactivo.html')

# Guardar como imagen
viz.guardar_imagen(fig, 'espectro.png', formato='png')
```

### Generación de Informes

```python
from generador_informes import GeneradorInformes

# Crear generador
generador = GeneradorInformes(directorio_salida='reports')

# Datos del análisis
datos_analisis = {
    'titulo': 'Análisis de GW250114',
    'subtitulo': 'Detección de componente en 141.7 Hz',
    'metricas': [
        {'label': 'SNR', 'valor': '10.5', 'unidad': ''},
        {'label': 'Frecuencia', 'valor': '141.7', 'unidad': 'Hz'}
    ],
    'hallazgos': [
        {
            'tipo': 'info',
            'titulo': 'Detección',
            'descripcion': 'Pico detectado en 141.7 Hz'
        }
    ],
    'graficos': [fig],
    'conclusiones': '<p>Se confirma la detección.</p>'
}

# Generar informe
archivos = generador.generar_informe_completo(
    datos_analisis=datos_analisis,
    incluir_pdf=True
)

print(f"HTML: {archivos['html']}")
print(f"PDF: {archivos.get('pdf', 'No generado')}")
```

### Dashboard Web

```bash
# Iniciar dashboard
cd dashboard
python3 dashboard_mejorado.py

# Acceder en navegador
# http://localhost:5000
```

#### Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal del dashboard |
| GET | `/api/metricas` | Métricas actuales del sistema |
| GET | `/api/alertas` | Alertas recientes |
| GET | `/api/stream` | Stream SSE de métricas en tiempo real |
| GET | `/api/grafico-tiempo-real` | Gráfico interactivo actualizado |
| GET | `/api/estado-sistema` | Estado completo del sistema |
| POST | `/api/analisis/iniciar` | Iniciar un nuevo análisis |
| GET | `/api/analisis/activos` | Lista de análisis en curso |

#### Ejemplo de uso de la API

```python
import requests
import json

# Obtener métricas actuales
response = requests.get('http://localhost:5000/api/metricas')
metricas = response.json()
print(f"SNR actual: {metricas['snr']}")

# Iniciar nuevo análisis
response = requests.post(
    'http://localhost:5000/api/analisis/iniciar',
    json={'evento': 'GW250114'},
    headers={'Content-Type': 'application/json'}
)
resultado = response.json()
print(f"Análisis ID: {resultado['analisis_id']}")

# Obtener alertas
response = requests.get('http://localhost:5000/api/alertas')
alertas_data = response.json()
for alerta in alertas_data['alertas'][:5]:
    print(f"{alerta['timestamp']}: {alerta['mensaje']}")
```

## 📊 Tipos de Visualizaciones

### 1. Espectro de Potencia

```python
fig = viz.crear_espectro_interactivo(
    frecuencias=freqs,
    potencias=powers,
    frecuencia_objetivo=141.7,
    titulo="Espectro de Potencia",
    detector="H1",
    snr=8.5
)
```

**Características:**
- Escala logarítmica en el eje Y
- Línea vertical en la frecuencia objetivo
- Información de SNR en el título
- Hover interactivo con valores precisos
- Zoom y pan

### 2. Serie Temporal

```python
fig = viz.crear_serie_temporal_interactiva(
    tiempo=time_array,
    datos=strain_data,
    titulo="Serie Temporal",
    detector="H1",
    zoom_inicio=0,
    zoom_fin=4
)
```

**Características:**
- Zoom opcional en región de interés
- Hover con valores de tiempo y strain
- Navegación temporal

### 3. Espectrograma

```python
fig = viz.crear_espectrograma_interactivo(
    tiempo=time,
    frecuencias=freqs,
    potencias_2d=spectrogram,
    frecuencia_objetivo=141.7
)
```

**Características:**
- Mapa de calor interactivo
- Escala de colores personalizable
- Línea horizontal en frecuencia objetivo

### 4. Dashboard Comparativo

```python
fig = viz.crear_dashboard_comparativo(
    datos_h1={'frecuencias': freqs_h1, 'potencias': powers_h1},
    datos_l1={'frecuencias': freqs_l1, 'potencias': powers_l1},
    frecuencia_objetivo=141.7
)
```

**Características:**
- Comparación lado a lado de detectores
- Zoom automático en región de interés
- 4 subplots (espectros completos y zooms)

### 5. Gráfico de SNR

```python
fig = viz.crear_grafico_snr(
    eventos=['GW150914', 'GW151226', 'GW170814'],
    snr_valores=[8.5, 6.2, 10.3],
    snr_umbral=5.0
)
```

**Características:**
- Barras coloreadas según umbral
- Valores mostrados sobre las barras
- Línea de umbral de detección

## 🎨 Personalización

### Temas Disponibles

```python
# Tema oscuro (por defecto)
viz = VisualizadorInteractivo(theme="plotly_dark")

# Tema claro
viz = VisualizadorInteractivo(theme="plotly_white")

# Otros temas
viz = VisualizadorInteractivo(theme="seaborn")
viz = VisualizadorInteractivo(theme="simple_white")
```

### Configuración de Exportación

```python
viz.config = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'mi_grafico',
        'height': 1920,
        'width': 1080,
        'scale': 2
    }
}
```

## 📈 Ejemplos Completos

Ejecutar el script de ejemplos:

```bash
python3 examples/ejemplo_uso_completo.py
```

Esto genera:
- `examples/output/espectro_interactivo.html`
- `examples/output/serie_temporal_interactiva.html`
- `examples/output/dashboard_comparativo.html`
- `examples/output/snr_eventos.html`
- `examples/output/reports/informe_analisis_*.html`

## 🧪 Tests

Ejecutar tests:

```bash
# Tests de visualizaciones
python3 tests/test_visualizaciones_interactivas.py

# Tests de generación de informes
python3 tests/test_generador_informes.py

# Tests del dashboard mejorado
python3 tests/test_dashboard_mejorado.py
```

## 📚 Estructura de Archivos

```
.
├── src/
│   ├── visualizaciones_interactivas.py  # Módulo de visualizaciones
│   └── generador_informes.py            # Módulo de informes
├── dashboard/
│   ├── dashboard_mejorado.py            # Dashboard web
│   └── templates/
│       └── dashboard_mejorado.html      # Template del dashboard
├── tests/
│   ├── test_visualizaciones_interactivas.py
│   ├── test_generador_informes.py
│   └── test_dashboard_mejorado.py
└── examples/
    ├── ejemplo_uso_completo.py          # Ejemplos de uso
    └── output/                          # Archivos generados
```

## 🔧 Solución de Problemas

### Error: "No module named 'plotly'"

```bash
pip install plotly kaleido
```

### Error: "No module named 'flask'"

```bash
pip install flask
```

### PDF no se genera

Instalar WeasyPrint:

```bash
pip install weasyprint
```

### Dashboard no se conecta

Verificar que el puerto 5000 no esté en uso:

```bash
lsof -i :5000
```

Cambiar puerto en `dashboard_mejorado.py`:

```python
app.run(host='0.0.0.0', port=8080)
```

## 🌟 Mejoras Futuras

- [ ] Soporte para más formatos de exportación (WebGL, PowerPoint)
- [ ] Integración con Jupyter Notebooks
- [ ] Animaciones de series temporales
- [ ] Comparación de múltiples eventos simultáneos
- [ ] Dashboard con autenticación
- [ ] Notificaciones push para alertas críticas
- [ ] Integración con bases de datos para histórico

## 📄 Licencia

Este módulo es parte del proyecto 141Hz y sigue la misma licencia del proyecto principal.

## 👥 Contribuciones

Para contribuir, consultar el archivo CONTRIBUTING.md del proyecto principal.

## 📞 Soporte

Para reportar problemas o solicitar nuevas características, crear un issue en el repositorio del proyecto.
