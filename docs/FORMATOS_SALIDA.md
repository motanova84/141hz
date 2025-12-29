# Formatos de Salida: Guía Completa de JSON y Gráficos

## 🎯 Propósito

Este documento describe en detalle todos los formatos de salida generados por los scripts de análisis, incluyendo estructuras JSON, formatos de gráficos, y guías para integración con herramientas externas.

## 📋 Contenidos

1. [Formatos JSON](#formatos-json)
2. [Formatos de Gráficos](#formatos-de-gráficos)
3. [Guía de Integración](#guía-de-integración)
4. [Ejemplos de Uso](#ejemplos-de-uso)
5. [Referencia API](#referencia-api)

---

## Formatos JSON

### 1. Análisis Individual de Evento

**Archivo:** `results/<evento>_<detector>_analysis.json`  
**Ejemplo:** `results/GW150914_H1_analysis.json`

#### Estructura Completa

```json
{
  "metadata": {
    "event_name": "GW150914",
    "detector": "H1",
    "analysis_date": "2025-11-05T10:30:45.123456",
    "script_version": "2.1.0",
    "analyst": "JMMB"
  },
  "data_info": {
    "gps_start": 1126259446,
    "gps_end": 1126259478,
    "duration_s": 32,
    "sample_rate_hz": 4096,
    "total_samples": 131072
  },
  "processing": {
    "highpass_hz": 20,
    "notch_frequencies_hz": [60, 120],
    "whitening_applied": true,
    "bandpass_hz": [140.7, 142.7]
  },
  "results": {
    "frequency_target_hz": 141.7001,
    "frequency_detected_hz": 141.69,
    "frequency_error_hz": 0.01,
    "snr": 7.47,
    "snr_threshold": 5.0,
    "detection_confirmed": true,
    "peak_power": 2.34e-21,
    "noise_floor": 3.13e-22,
    "significance_sigma": 7.2
  },
  "statistics": {
    "mean_power": 1.05e-22,
    "std_power": 4.21e-23,
    "median_power": 8.92e-23,
    "peak_to_median_ratio": 26.25
  },
  "quality_flags": {
    "data_quality_good": true,
    "injection_free": true,
    "noise_stationary": true,
    "instrumental_lines_removed": true
  }
}
```

#### Descripción de Campos

##### metadata
- **event_name** (string): Nombre del evento GW (ej: "GW150914")
- **detector** (string): Código del detector ("H1", "L1", "V1", "K1")
- **analysis_date** (string ISO8601): Timestamp de cuando se ejecutó el análisis
- **script_version** (string): Versión del script usado
- **analyst** (string): Iniciales del analista o sistema

##### data_info
- **gps_start** (int): Tiempo GPS de inicio (segundos desde 1980-01-06 00:00:00 UTC)
- **gps_end** (int): Tiempo GPS de fin
- **duration_s** (float): Duración total en segundos
- **sample_rate_hz** (int): Frecuencia de muestreo en Hz
- **total_samples** (int): Número total de muestras = duration × sample_rate

##### processing
- **highpass_hz** (float): Frecuencia del filtro paso-alto aplicado
- **notch_frequencies_hz** (array of float): Frecuencias donde se aplicó notch filter
- **whitening_applied** (bool): Si se aplicó whitening al espectro
- **bandpass_hz** (array of 2 floats): [freq_min, freq_max] de banda de análisis

##### results
- **frequency_target_hz** (float): Frecuencia objetivo de búsqueda (141.7001)
- **frequency_detected_hz** (float): Frecuencia del pico más cercano detectado
- **frequency_error_hz** (float): Diferencia absoluta |detected - target|
- **snr** (float): Signal-to-Noise Ratio calculado
- **snr_threshold** (float): Umbral de SNR para considerarse detección (típicamente 5.0)
- **detection_confirmed** (bool): true si SNR >= threshold y freq_error < 1.0 Hz
- **peak_power** (float): Densidad espectral de potencia en el pico (Hz⁻¹)
- **noise_floor** (float): Mediana de la PSD en la banda (Hz⁻¹)
- **significance_sigma** (float): Significancia estadística en número de sigmas

##### statistics
- **mean_power** (float): Potencia promedio en la banda de análisis
- **std_power** (float): Desviación estándar de la potencia
- **median_power** (float): Mediana de la potencia (estimador robusto de ruido)
- **peak_to_median_ratio** (float): Ratio pico/mediana (otro indicador de SNR)

##### quality_flags
- **data_quality_good** (bool): Banderas de calidad de datos GWOSC
- **injection_free** (bool): No hay inyecciones de hardware conocidas
- **noise_stationary** (bool): El ruido es estadísticamente estacionario
- **instrumental_lines_removed** (bool): Líneas instrumentales fueron filtradas

---

### 2. Análisis Multi-Evento

**Archivo:** `multi_event_final.json`

#### Estructura

```json
{
  "discovery": {
    "frequency_target_hz": 141.7001,
    "bandpass_hz": [140.7, 142.7],
    "catalog": "GWTC-1",
    "equation": "Ψ = I × A_eff²",
    "author": "José Manuel Mota Burruezo (JMMB Ψ✧)",
    "date_analysis": "2025-11-03T22:33:11.514544"
  },
  "statistics": {
    "total_events": 11,
    "detection_rate": "100%",
    "h1_detections": "11/11",
    "l1_detections": "11/11",
    "snr_mean": 20.954545454545453,
    "snr_std": 5.536678301253401,
    "snr_min": 10.78,
    "snr_max": 31.35,
    "h1_mean": 21.37909090909091,
    "h1_std": 5.664788296686911,
    "l1_mean": 20.53,
    "l1_std": 5.372086102335766
  },
  "events": {
    "GW150914": {
      "date": "2015-09-14",
      "gps_range": [1126259462, 1126259494],
      "snr": {
        "H1": 18.45,
        "L1": 17.23
      },
      "detection": "confirmed",
      "h1_above_threshold": true,
      "l1_above_threshold": true
    },
    "GW151226": {
      "date": "2015-12-26",
      "gps_range": [1135136350, 1135136382],
      "snr": {
        "H1": 13.14,
        "L1": 13.14
      },
      "detection": "confirmed",
      "h1_above_threshold": true,
      "l1_above_threshold": true
    }
    // ... resto de eventos
  }
}
```

#### Descripción de Campos

##### discovery
Metadata del descubrimiento y análisis global.

##### statistics
Estadísticas agregadas sobre todos los eventos:
- **total_events** (int): Número de eventos analizados
- **detection_rate** (string): Porcentaje de eventos con detección positiva
- **h1_detections** (string): "N/M" eventos detectados en Hanford
- **l1_detections** (string): "N/M" eventos detectados en Livingston
- **snr_mean** (float): SNR promedio combinando H1 y L1
- **snr_std** (float): Desviación estándar del SNR
- **snr_min/max** (float): Valores mínimo y máximo de SNR observados
- **h1_mean/std** (float): Estadísticas específicas del detector H1
- **l1_mean/std** (float): Estadísticas específicas del detector L1

##### events
Diccionario con cada evento como clave:
- **date** (string YYYY-MM-DD): Fecha del evento
- **gps_range** (array of 2 ints): [start, end] en tiempo GPS
- **snr** (object): SNR por detector {"H1": float, "L1": float}
- **detection** (string): "confirmed", "marginal", o "not_detected"
- **h1_above_threshold** (bool): SNR_H1 >= 5.0
- **l1_above_threshold** (bool): SNR_L1 >= 5.0

---

### 3. Análisis de Validación Estadística

**Archivo:** `results/statistical_validation.json`

```json
{
  "analysis": {
    "method": "time_slides",
    "n_trials": 10000,
    "slide_range_s": 0.2,
    "event": "GW150914"
  },
  "observed": {
    "snr_h1": 7.47,
    "snr_l1": 0.95,
    "frequency_hz": 141.69
  },
  "background": {
    "snr_mean": 2.13,
    "snr_std": 0.84,
    "snr_95percentile": 3.85,
    "snr_99percentile": 4.52
  },
  "significance": {
    "p_value": 0.0003,
    "p_value_interpretation": "highly_significant",
    "sigma_equivalent": 3.43,
    "trials_above_observed": 3,
    "false_alarm_rate_per_year": 0.013
  },
  "bayes_factor": {
    "bf_h1": 145.2,
    "bf_l1": 1.8,
    "bf_combined": 261.36,
    "interpretation": "decisive_evidence"
  }
}
```

#### Descripción de Campos

##### analysis
Parámetros del análisis estadístico realizado.

##### observed
Valores observados en el análisis real.

##### background
Distribución del "ruido de fondo" estimada mediante time-slides:
- **snr_mean** (float): SNR promedio en trials aleatorios
- **snr_std** (float): Desviación estándar
- **snr_95percentile** (float): Percentil 95 (umbral de significancia)

##### significance
Métricas de significancia estadística:
- **p_value** (float): Probabilidad de resultado por azar (0 a 1)
  - < 0.05: significativo
  - < 0.01: muy significativo
  - < 0.001: altamente significativo
- **sigma_equivalent** (float): Equivalente en sigmas (σ)
- **trials_above_observed** (int): Número de trials con SNR >= observado
- **false_alarm_rate_per_year** (float): Tasa de falsas alarmas esperada

##### bayes_factor
Comparación bayesiana de modelos:
- **bf_h1/l1** (float): Bayes Factor por detector
- **bf_combined** (float): BF combinado
- **interpretation** (string): Escala de Jeffreys:
  - "anecdotal": 1-3
  - "moderate": 3-10
  - "strong": 10-30
  - "very_strong": 30-100
  - "decisive": >100

---

### 4. Análisis de Armónicos

**Archivo:** `results/harmonics_analysis.json`

```json
{
  "fundamental": {
    "f0_hz": 141.7001,
    "snr": 7.47,
    "detected": true
  },
  "harmonics": [
    {
      "n": 2,
      "frequency_hz": 283.4002,
      "frequency_expected_hz": 283.4002,
      "frequency_detected_hz": 283.38,
      "error_hz": 0.02,
      "snr": 3.21,
      "detected": false,
      "above_threshold": false
    },
    {
      "n": 3,
      "frequency_hz": 425.1003,
      "frequency_expected_hz": 425.1003,
      "frequency_detected_hz": 424.95,
      "error_hz": 0.15,
      "snr": 2.14,
      "detected": false,
      "above_threshold": false
    }
  ],
  "subharmonics": [
    {
      "n": -1,
      "description": "f0/phi",
      "frequency_hz": 87.5711,
      "frequency_expected_hz": 87.5711,
      "frequency_detected_hz": 87.60,
      "error_hz": 0.03,
      "snr": 4.12,
      "detected": false,
      "above_threshold": false
    }
  ],
  "summary": {
    "total_searched": 5,
    "detections": 1,
    "detection_rate": "20%",
    "fundamental_only": true
  }
}
```

---

## Formatos de Gráficos

### 1. Serie Temporal

**Archivo:** `results/figures/<evento>_<detector>_timeseries.png`  
**Formato:** PNG, 1920×1080 pixels, 300 DPI

#### Estructura del Gráfico

```
┌─────────────────────────────────────────────┐
│  Title: GW150914 H1 - Time Series          │
├─────────────────────────────────────────────┤
│                                             │
│     ▲ Strain (×10⁻²¹)                      │
│  20 │         ╱╲                            │
│     │        ╱  ╲                           │
│  10 │       ╱    ╲      ╱╲                  │
│     │      ╱      ╲    ╱  ╲                 │
│   0 ├─────╱────────╲──╱────╲─────────────→ │
│     │    ╱          ╲╱      ╲               │
│ -10 │   ╱                    ╲              │
│     │  ╱                      ╲             │
│ -20 │ ╱                        ╲            │
│     └─────────────────────────────────────→ │
│       0     5    10    15    20    25    30│
│                 Time (s)                    │
└─────────────────────────────────────────────┘
```

#### Elementos del Gráfico

- **Título**: Evento y detector
- **Eje X**: Tiempo en segundos desde el inicio del segmento
  - Rango típico: 0 a 32 s
  - Marca de merger (t=16s) indicada con línea vertical roja punteada
- **Eje Y**: Strain (deformación) adimensional
  - Unidades: Típicamente 10⁻²¹ o 10⁻²²
  - Escala lineal
- **Línea**: Datos del strain procesado (filtrado)
- **Grid**: Cuadrícula ligera para facilitar lectura
- **Leyenda**: Indica filtros aplicados (highpass, notch)

#### Interpretación Visual

- **Pre-merger** (t < 16s): Ruido de fondo con posible chirp
- **Merger** (t ≈ 16s): Pico de amplitud máxima
- **Post-merger/Ringdown** (t > 16s): Decaimiento exponencial

---

### 2. Espectro de Potencia

**Archivo:** `results/figures/<evento>_<detector>_spectrum.png`  
**Formato:** PNG, 1920×1080 pixels, 300 DPI

#### Estructura del Gráfico

```
┌──────────────────────────────────────────────┐
│  Title: GW150914 H1 - Power Spectrum        │
├──────────────────────────────────────────────┤
│                                              │
│ ▲ PSD (Hz⁻¹)                                │
│10⁻²⁰│                                        │
│     │  ╲                                     │
│10⁻²¹│   ╲                                    │
│     │    ╲╲      ┃                           │
│10⁻²²│     ╲╲     ┃  ╱╲                       │
│     │      ╲╲    ┃ ╱  ╲                      │
│10⁻²³│       ╲╲___┃╱____╲___                  │
│     │            ┃                           │
│10⁻²⁴│            ┃                           │
│     └────────────┃─────────────────────────→│
│        100  120 141.7 160  180  200  Hz     │
│                 Frequency                    │
│                                              │
│  Legend: ━━━ PSD    ┃ 141.7 Hz target       │
└──────────────────────────────────────────────┘
```

#### Elementos del Gráfico

- **Título**: Evento, detector, y "Power Spectrum"
- **Eje X**: Frecuencia en Hz
  - Rango típico: 100 a 200 Hz
  - Escala lineal
- **Eje Y**: Power Spectral Density (PSD) en Hz⁻¹
  - Escala logarítmica (típicamente 10⁻²⁴ a 10⁻²⁰)
- **Línea principal**: PSD calculada mediante FFT/Welch
- **Línea vertical roja**: Marca 141.7 Hz (frecuencia objetivo)
- **Sombreado**: Banda de análisis [140.7, 142.7] Hz (opcional)

#### Interpretación Visual

- **Pendiente decreciente**: Ruido típico de LIGO (1/f en muchas bandas)
- **Pico en 141.7 Hz**: Señal de interés
- **Otros picos**: Posibles líneas instrumentales o QNMs

---

### 3. Zoom en 141.7 Hz

**Archivo:** `results/figures/<evento>_<detector>_zoom_141hz.png`  
**Formato:** PNG, 1920×1080 pixels, 300 DPI

#### Estructura del Gráfico

```
┌──────────────────────────────────────────────┐
│  Title: GW150914 H1 - Zoom around 141.7 Hz  │
├──────────────────────────────────────────────┤
│                                              │
│ ▲ PSD (Hz⁻¹)                                │
│3.5│              ╱▲╲                         │
│   │             ╱ │ ╲                        │
│3.0│            ╱  │  ╲                       │
│   │           ╱   │   ╲                      │
│2.5│          ╱    │    ╲                     │
│   │         ╱     │     ╲                    │
│2.0│        ╱      ┃      ╲                   │
│   │       ╱       ┃       ╲                  │
│1.5│______╱________┃________╲_______          │
│   │               ┃                          │
│1.0│               ┃                          │
│   └───────────────┃──────────────────────→  │
│      130  135  140│141.7 145  150  155  Hz  │
│                   Frequency                  │
│                                              │
│  Stats: Peak=141.69 Hz, SNR=7.47            │
└──────────────────────────────────────────────┘
```

#### Elementos del Gráfico

- **Rango X**: Típicamente 130-160 Hz (±15 Hz alrededor de 141.7)
- **Eje Y**: PSD en unidades absolutas (Hz⁻¹) o normalizadas
- **Línea vertical roja**: 141.7 Hz objetivo
- **Anotación de pico**: Flecha señalando el máximo local
- **Caja de texto**: Estadísticas clave (freq detectada, SNR)
- **Línea horizontal**: Nivel de ruido (mediana)

#### Interpretación Visual

- **Pico claro sobre ruido**: Detección positiva
- **Pico cercano a línea roja**: Concordancia con predicción
- **Múltiples picos**: Puede indicar armónicos o ruido estructurado

---

### 4. Gráfico de Comparación Multi-Evento

**Archivo:** `multi_event_final.png`  
**Formato:** PNG, 2400×1400 pixels, 300 DPI

#### Estructura del Gráfico

```
┌──────────────────────────────────────────────────┐
│  141.7 Hz Detection: Multi-Event Comparison      │
├──────────────────────────────────────────────────┤
│                                                  │
│ ▲ SNR                                            │
│35│                                               │
│30│                          ██                   │
│25│              ██      ██  ██  ██  ██          │
│20│      ██  ██  ██  ██  ██  ██  ██  ██  ██      │
│15│  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  │
│10│  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  │
│ 5│  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  ██  │
│  ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──────────────→│
│    150914 151012 151226 170104 ... 170823       │
│                  Event                           │
│                                                  │
│  Legend: ██ H1   ██ L1   ─── Threshold (5.0)   │
└──────────────────────────────────────────────────┘
```

#### Elementos del Gráfico

- **Eje X**: Eventos ordenados cronológicamente
- **Eje Y**: SNR (0 a ~35)
- **Barras azules**: SNR en detector H1
- **Barras naranjas**: SNR en detector L1
- **Línea horizontal roja punteada**: Umbral de detección (SNR=5)
- **Título**: Indica frecuencia (141.7 Hz) y tipo de análisis
- **Caja de estadísticas**: SNR medio, detección rate, etc.

#### Interpretación Visual

- **Todas las barras sobre umbral**: 100% detección rate
- **Consistencia H1-L1**: Ambos detectores ven señal similar
- **Variabilidad**: SNR varía por condiciones del detector y evento

---

### 5. Histograma de Distribución

**Archivo:** `results/figures/<evento>_<detector>_histogram.png`  
**Formato:** PNG, 1920×1080 pixels, 300 DPI

#### Estructura del Gráfico

```
┌──────────────────────────────────────────────┐
│  GW150914 H1 - Power Distribution            │
├──────────────────────────────────────────────┤
│                                              │
│ ▲ Count                                      │
│800│██                                        │
│   │██                                        │
│600│██                                        │
│   │██                                        │
│400│██  ██                                    │
│   │██  ██  ██                                │
│200│██  ██  ██  ██  ▓▓                        │
│   │██  ██  ██  ██  ▓▓  │                     │
│  0└──────────────────────┼──────────────────→│
│     0    1    2    3    4                    │
│              PSD (Hz⁻¹) ×10⁻²²               │
│                                              │
│  Stats: Mean=1.05, Std=0.42, Peak=3.54      │
│  Legend: ██ Noise  ▓▓ Signal  │ Peak        │
└──────────────────────────────────────────────┘
```

#### Elementos del Gráfico

- **Eje X**: Valores de PSD (potencia espectral)
- **Eje Y**: Número de bins de frecuencia con ese valor de potencia
- **Histograma azul**: Distribución del "ruido" (mayoría de frecuencias)
- **Barras rojas**: Outliers (posible señal)
- **Línea vertical verde**: Ubicación del pico de 141.7 Hz
- **Caja de estadísticas**: Media, std, valor del pico

#### Interpretación Visual

- **Distribución concentrada a la izquierda**: Mayoría es ruido de bajo nivel
- **Cola derecha**: Valores extremos (señales potenciales)
- **Pico marcado muy a la derecha**: Señal significativa

---

## Guía de Integración

### Lectura de JSON en Python

```python
import json

# Leer análisis individual
with open('results/GW150914_H1_analysis.json', 'r') as f:
    data = json.load(f)

# Acceder a campos
event = data['metadata']['event_name']
snr = data['results']['snr']
detected = data['results']['detection_confirmed']

print(f"Evento: {event}, SNR: {snr}, Detectado: {detected}")
```

### Lectura de JSON en R

```r
library(jsonlite)

# Leer análisis multi-evento
data <- fromJSON('multi_event_final.json')

# Extraer estadísticas
stats <- data$statistics
snr_mean <- stats$snr_mean
detection_rate <- stats$detection_rate

cat(sprintf("SNR medio: %.2f, Tasa: %s\n", snr_mean, detection_rate))
```

### Lectura de JSON en Julia

```julia
using JSON

# Leer análisis
data = JSON.parsefile("results/GW150914_H1_analysis.json")

# Acceder a campos
snr = data["results"]["snr"]
freq = data["results"]["frequency_detected_hz"]

println("SNR: $snr, Frecuencia: $freq Hz")
```

### Procesamiento de Gráficos

#### Python (matplotlib)

```python
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Cargar imagen
img = mpimg.imread('results/figures/GW150914_H1_spectrum.png')

# Mostrar
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(img)
ax.axis('off')
plt.title('Espectro de GW150914')
plt.show()
```

#### Python (PIL/Pillow)

```python
from PIL import Image

# Abrir imagen
img = Image.open('results/figures/multi_event_final.png')

# Obtener información
print(f"Tamaño: {img.size}")
print(f"Formato: {img.format}")
print(f"Modo: {img.mode}")

# Redimensionar si necesario
img_small = img.resize((800, 600))
img_small.save('multi_event_thumbnail.png')
```

### Generación de Reportes

#### Markdown

```python
def generate_markdown_report(json_data):
    """Genera reporte en Markdown desde JSON."""
    md = f"# Análisis de {json_data['metadata']['event_name']}\n\n"
    md += f"**Detector:** {json_data['metadata']['detector']}\n"
    md += f"**Fecha:** {json_data['metadata']['analysis_date']}\n\n"
    
    md += "## Resultados\n\n"
    results = json_data['results']
    md += f"- Frecuencia detectada: **{results['frequency_detected_hz']:.2f} Hz**\n"
    md += f"- SNR: **{results['snr']:.2f}**\n"
    md += f"- Detección confirmada: **{'✅ Sí' if results['detection_confirmed'] else '❌ No'}**\n\n"
    
    return md

# Uso
with open('results/GW150914_H1_analysis.json', 'r') as f:
    data = json.load(f)

report = generate_markdown_report(data)
with open('report.md', 'w') as f:
    f.write(report)
```

#### HTML

```python
def generate_html_report(json_data, plot_path):
    """Genera reporte HTML con gráfico embebido."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Análisis {json_data['metadata']['event_name']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .stat {{ background: #f0f0f0; padding: 10px; margin: 5px 0; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>Análisis de {json_data['metadata']['event_name']}</h1>
        
        <div class="stat">
            <strong>SNR:</strong> {json_data['results']['snr']:.2f}
        </div>
        <div class="stat">
            <strong>Frecuencia:</strong> {json_data['results']['frequency_detected_hz']:.2f} Hz
        </div>
        
        <h2>Espectro</h2>
        <img src="{plot_path}" alt="Espectro">
    </body>
    </html>
    """
    return html
```

#### PDF (usando reportlab)

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generate_pdf_report(json_data, output_path='report.pdf'):
    """Genera reporte PDF."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Análisis de {json_data['metadata']['event_name']}")
    
    # Resultados
    c.setFont("Helvetica", 12)
    y = height - 100
    results = json_data['results']
    
    c.drawString(50, y, f"SNR: {results['snr']:.2f}")
    y -= 20
    c.drawString(50, y, f"Frecuencia: {results['frequency_detected_hz']:.2f} Hz")
    y -= 20
    c.drawString(50, y, f"Detección: {'Confirmada' if results['detection_confirmed'] else 'No confirmada'}")
    
    # Gráfico (si existe)
    # img = ImageReader('results/figures/spectrum.png')
    # c.drawImage(img, 50, y-300, width=500, height=300)
    
    c.save()
    print(f"Reporte generado: {output_path}")
```

---

## Ejemplos de Uso

### Ejemplo 1: Análisis Batch de Múltiples Eventos

```python
import json
import glob

# Leer todos los análisis individuales
results = []
for filepath in glob.glob('results/*_analysis.json'):
    with open(filepath, 'r') as f:
        data = json.load(f)
        results.append({
            'event': data['metadata']['event_name'],
            'detector': data['metadata']['detector'],
            'snr': data['results']['snr'],
            'detected': data['results']['detection_confirmed']
        })

# Filtrar detecciones confirmadas
detections = [r for r in results if r['detected']]

print(f"Total análisis: {len(results)}")
print(f"Detecciones confirmadas: {len(detections)}")
print(f"Tasa de detección: {100*len(detections)/len(results):.1f}%")

# Imprimir top 5 por SNR
top5 = sorted(detections, key=lambda x: x['snr'], reverse=True)[:5]
print("\nTop 5 por SNR:")
for i, r in enumerate(top5, 1):
    print(f"{i}. {r['event']} {r['detector']}: SNR={r['snr']:.2f}")
```

### Ejemplo 2: Comparación H1 vs L1

```python
import json
import matplotlib.pyplot as plt
import numpy as np

# Leer análisis multi-evento
with open('multi_event_final.json', 'r') as f:
    data = json.load(f)

# Extraer SNRs
events = []
h1_snrs = []
l1_snrs = []

for event, info in data['events'].items():
    events.append(event)
    h1_snrs.append(info['snr']['H1'])
    l1_snrs.append(info['snr']['L1'])

# Gráfico de dispersión
plt.figure(figsize=(10, 6))
plt.scatter(h1_snrs, l1_snrs, s=100, alpha=0.6)

# Línea de igualdad
max_snr = max(max(h1_snrs), max(l1_snrs))
plt.plot([0, max_snr], [0, max_snr], 'r--', alpha=0.5, label='H1 = L1')

# Umbral
plt.axhline(y=5, color='gray', linestyle=':', label='Threshold')
plt.axvline(x=5, color='gray', linestyle=':')

# Etiquetas
for i, event in enumerate(events):
    plt.annotate(event, (h1_snrs[i], l1_snrs[i]), 
                 fontsize=8, alpha=0.7)

plt.xlabel('SNR H1 (Hanford)')
plt.ylabel('SNR L1 (Livingston)')
plt.title('Comparación de SNR entre Detectores')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('h1_vs_l1_comparison.png', dpi=300)
plt.show()
```

### Ejemplo 3: Exportar a CSV

```python
import json
import csv

# Leer datos
with open('multi_event_final.json', 'r') as f:
    data = json.load(f)

# Escribir CSV
with open('results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Header
    writer.writerow(['Event', 'Date', 'SNR_H1', 'SNR_L1', 'SNR_Mean', 'Detected'])
    
    # Filas
    for event, info in data['events'].items():
        snr_h1 = info['snr']['H1']
        snr_l1 = info['snr']['L1']
        snr_mean = (snr_h1 + snr_l1) / 2
        detected = info['detection']
        
        writer.writerow([event, info['date'], snr_h1, snr_l1, snr_mean, detected])

print("CSV exportado: results.csv")
```

### Ejemplo 4: Integración con Pandas

```python
import json
import pandas as pd

# Leer y convertir a DataFrame
with open('multi_event_final.json', 'r') as f:
    data = json.load(f)

# Construir DataFrame
rows = []
for event, info in data['events'].items():
    rows.append({
        'Event': event,
        'Date': info['date'],
        'SNR_H1': info['snr']['H1'],
        'SNR_L1': info['snr']['L1'],
        'Detection': info['detection']
    })

df = pd.DataFrame(rows)

# Análisis con pandas
print("Estadísticas descriptivas:")
print(df[['SNR_H1', 'SNR_L1']].describe())

print("\nCorrelación H1-L1:")
print(df[['SNR_H1', 'SNR_L1']].corr())

# Filtrar eventos fuertes
strong_events = df[(df['SNR_H1'] > 20) & (df['SNR_L1'] > 20)]
print(f"\nEventos fuertes en ambos detectores: {len(strong_events)}")
print(strong_events[['Event', 'SNR_H1', 'SNR_L1']])
```

---

## Referencia API

### Esquema JSON (JSON Schema)

Para validación automática de archivos JSON:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GW Event Analysis",
  "type": "object",
  "required": ["metadata", "data_info", "results"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["event_name", "detector"],
      "properties": {
        "event_name": {"type": "string", "pattern": "^GW[0-9]{6}$"},
        "detector": {"type": "string", "enum": ["H1", "L1", "V1", "K1"]},
        "analysis_date": {"type": "string", "format": "date-time"}
      }
    },
    "results": {
      "type": "object",
      "required": ["snr", "frequency_detected_hz", "detection_confirmed"],
      "properties": {
        "snr": {"type": "number", "minimum": 0},
        "frequency_detected_hz": {"type": "number", "minimum": 0, "maximum": 1000},
        "detection_confirmed": {"type": "boolean"}
      }
    }
  }
}
```

### Validación con Python

```python
import json
import jsonschema

# Cargar schema
with open('schema.json', 'r') as f:
    schema = json.load(f)

# Cargar datos
with open('results/GW150914_H1_analysis.json', 'r') as f:
    data = json.load(f)

# Validar
try:
    jsonschema.validate(instance=data, schema=schema)
    print("✅ JSON válido")
except jsonschema.exceptions.ValidationError as e:
    print(f"❌ JSON inválido: {e.message}")
```

---

## Versionado y Compatibilidad

### Versión Actual: 2.1.0

**Changelog:**

**v2.1.0 (2025-11-05)**
- Añadido campo `significance_sigma` en results
- Incluido `quality_flags` en estructura principal
- Mejorada documentación de formatos

**v2.0.0 (2025-10-15)**
- Cambio de estructura de `events` de array a objeto
- Unificación de nomenclatura H1/L1
- Breaking change: Requiere actualizar scripts de lectura

**v1.0.0 (2025-09-01)**
- Primera versión estable
- Esquema básico de JSON implementado

### Compatibilidad

- **Backward compatible**: v2.1 puede leer v2.0 (con advertencias)
- **Forward compatible**: NO - v2.0 no puede leer v2.1 completamente

**Migración de v2.0 a v2.1:**
```python
def migrate_v20_to_v21(data_v20):
    """Migra JSON de v2.0 a v2.1."""
    data_v21 = data_v20.copy()
    
    # Añadir campos nuevos con valores por defecto
    if 'results' in data_v21:
        if 'significance_sigma' not in data_v21['results']:
            # Estimar sigma desde SNR
            snr = data_v21['results']['snr']
            data_v21['results']['significance_sigma'] = snr / 1.0  # Aproximación
    
    if 'quality_flags' not in data_v21:
        data_v21['quality_flags'] = {
            'data_quality_good': True,
            'injection_free': True,
            'noise_stationary': True,
            'instrumental_lines_removed': True
        }
    
    # Actualizar versión
    data_v21['metadata']['script_version'] = '2.1.0'
    
    return data_v21
```

---

## Contacto y Soporte

**Para preguntas sobre formatos:**
- Email: institutoconsciencia@proton.me
- GitHub Issues: https://github.com/motanova84/141hz/issues
- Documentación: https://github.com/motanova84/141hz

**Para contribuir mejoras a formatos:**
- Ver [CONTRIBUTING.md](../CONTRIBUTING.md)
- Proponer cambios via Pull Request
- Discutir en GitHub Discussions

---

**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Última actualización:** 2025-11-05  
**Versión del documento:** 1.0.0  
**Licencia:** MIT
