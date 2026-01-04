# Análisis con Filtro Bandpass [140.5-143.0 Hz]

## Descripción

Este documento describe la implementación del análisis de la frecuencia secundaria **141.7001 Hz** utilizando filtro bandpass específico **[140.5-143.0 Hz]** sobre datos strain en formato HDF5 publicados por GWOSC (Gravitational Wave Open Science Center).

## Comportamiento Esperado

Según las especificaciones del análisis, la frecuencia **f̂ = 141.7001 ± 0.0012 Hz** debe cumplir con los siguientes criterios:

### 1. Pico Secundario de Energía
- **Análisis**: Q-transform o wavelet packets
- **Requisito**: Q > 30
- **Característica**: Aparece como pico secundario en el análisis espectral

### 2. Ventana Temporal
- **Ventana**: ±0.3 s del merger
- **Fase**: Chirp → coalescencia
- **Ubicación**: Visible en el ringdown post-merger

### 3. Coherencia Multi-Detector
- **Mínimo**: 2 detectores (ej. H1 y L1)
- **Tipo**: Coherencia parcial entre detectores
- **Validación**: Frecuencia consistente entre detectores

### 4. Exclusión de Artefactos
- **No atribuible a**: Líneas espectrales conocidas
- **No atribuible a**: Glitches instrumentales estándar
- **Verificación**: Análisis de calidad de datos

### 5. Reproducibilidad
- **Filtro**: Bandpass [140.5-143.0 Hz]
- **Datos**: Strain .hdf5 publicado por GWOSC
- **Método**: Análisis reproducible y automatizado

## Implementación

### Script Principal

**Archivo**: `scripts/analisis_141hz_bandpass.py`

El script implementa el análisis completo con las siguientes características:

```python
# Parámetros de análisis
TARGET_FREQUENCY = 141.7001  # Hz
FREQUENCY_UNCERTAINTY = 0.0012  # Hz
BANDPASS_LOW = 140.5  # Hz
BANDPASS_HIGH = 143.0  # Hz
MERGER_WINDOW = 0.3  # segundos (±0.3s)
MIN_Q_VALUE = 30  # Q > 30 para Q-transform
MIN_DETECTORS = 2  # Coherencia entre al menos 2 detectores
```

### Flujo de Análisis

1. **Descarga de Datos**
   - Obtiene datos strain desde GWOSC
   - Ventana de ±16 segundos alrededor del merger
   - Formato: TimeSeries de GWPy

2. **Filtrado Bandpass**
   - Diseño: Filtro Butterworth bandpass [140.5-143.0 Hz]
   - Aplicación: `filtfilt=True` para fase cero
   - Resultado: Señal filtrada en banda objetivo

3. **Extracción de Ventana**
   - Segmento: ±0.3s alrededor del merger
   - Duración: 0.6 segundos totales
   - Muestras: ~2457 muestras @ 4096 Hz

4. **Q-Transform**
   - Rango Q: (30, 100)
   - Rango frecuencia: [140.5-143.0 Hz]
   - Ventana: ±0.3s del merger

5. **Análisis de Frecuencia**
   - Espectro: ASD con FFT
   - Búsqueda: Pico en 141.7001 Hz
   - Validación: Dentro de ±0.0012 Hz

6. **Coherencia Multi-Detector**
   - Análisis: Comparación entre detectores
   - Criterio: Desviación estándar < 0.1 Hz
   - SNR promedio > 1.5

7. **Visualización**
   - Espectro de potencia con bandpass
   - Q-transform con Q > 30
   - Métricas de detección

## Uso del Script

### Sintaxis Básica

```bash
python3 scripts/analisis_141hz_bandpass.py --event GW150914
```

### Opciones Avanzadas

```bash
# Analizar múltiples detectores
python3 scripts/analisis_141hz_bandpass.py --event GW150914 --detectors H1 L1 V1

# Especificar directorio de salida
python3 scripts/analisis_141hz_bandpass.py --event GW150914 --output results/my_analysis/

# Ver ayuda completa
python3 scripts/analisis_141hz_bandpass.py --help
```

### Eventos Soportados

El script soporta los siguientes eventos GWOSC:

- GW150914 (GPS: 1126259462.423)
- GW151012 (GPS: 1128678900.44)
- GW151226 (GPS: 1135136350.6)
- GW170104 (GPS: 1167559936.6)
- GW170814 (GPS: 1186741861.5)
- GW170817 (GPS: 1187008882.4)
- GW170823 (GPS: 1187529256.5)

## Tests Automatizados

### Script de Tests

**Archivo**: `scripts/test_analisis_141hz_bandpass.py`

El script de tests valida:

1. **Parámetros del Filtro**
   - Frecuencia objetivo: 141.7001 Hz
   - Incertidumbre: ±0.0012 Hz
   - Rango bandpass: [140.5-143.0 Hz]

2. **Validación de Eventos**
   - Catálogo de eventos conocidos
   - Tiempos GPS correctos

3. **Análisis de Frecuencia**
   - Detección dentro del rango
   - Detección fuera del rango
   - Casos límite

4. **Coherencia Multi-Detector**
   - Detectores insuficientes
   - Detectores coherentes
   - Detectores incoherentes

5. **Ventana Temporal**
   - Tamaño: ±0.3s
   - Muestras: ~2457 @ 4096 Hz

6. **Q-Transform**
   - Q mínimo: 30
   - Rango válido: (30, 100)

### Ejecutar Tests

```bash
python3 scripts/test_analisis_141hz_bandpass.py
```

### Resultados Esperados

```
✅ TODOS LOS TESTS PASARON

Ran 25 tests in 0.002s
OK (skipped=3)
```

## Dependencias

### Requeridas

- **Python**: 3.9+
- **NumPy**: >= 1.21.0
- **GWPy**: >= 3.0.0
- **SciPy**: >= 1.7.0

### Opcionales

- **Matplotlib**: >= 3.5.0 (para visualizaciones)

### Instalación

```bash
pip install gwpy numpy scipy matplotlib
```

## Resultados

### Estructura de Salida

El script genera los siguientes archivos:

```
results/bandpass_analysis/
├── GW150914_141hz_bandpass_YYYYMMDD_HHMMSS.png
└── [otros eventos]
```

### Formato de Visualización

Cada visualización contiene (por detector):

1. **Panel Superior**: Espectro de potencia
   - ASD con filtro bandpass marcado
   - Frecuencia objetivo (línea verde)
   - Frecuencia detectada (línea roja)
   - Banda del filtro (zona amarilla)

2. **Panel Central**: Q-Transform
   - Energía vs tiempo y frecuencia
   - Q > 30
   - Frecuencia objetivo (línea blanca)
   - Ventana: ±0.3s del merger

3. **Panel Inferior**: Métricas
   - Frecuencia detectada vs objetivo
   - Desviación y incertidumbre
   - SNR y potencia
   - Estado de validación

### Métricas de Salida

Para cada detector, el análisis reporta:

- **Frecuencia detectada**: f_detected ± Δf
- **Desviación**: |f_detected - 141.7001| Hz
- **SNR**: Relación señal/ruido en la banda
- **Potencia**: ASD en la frecuencia objetivo
- **Validación**: Dentro/fuera del rango esperado

### Análisis de Coherencia

El análisis de coherencia reporta:

- **Frecuencia media**: Promedio entre detectores
- **Desviación estándar**: Coherencia entre detectores
- **SNR medio**: Promedio de SNR
- **Estado**: Coherente / No coherente

## Validación Científica

### Criterios de Validación

Una detección se considera válida si:

1. **Frecuencia**: |f_detected - 141.7001| ≤ 0.0012 Hz
2. **SNR**: SNR > 1.5 (al menos)
3. **Coherencia**: Desviación estándar < 0.1 Hz entre detectores
4. **Q-Transform**: Pico visible con Q > 30
5. **Ventana**: Señal presente en ±0.3s del merger

### Interpretación de Resultados

#### ✅ Detección Confirmada
- Todos los criterios cumplidos
- Coherencia entre al menos 2 detectores
- SNR promedio > 2.5

#### ⚠️ Detección Probable
- Criterios principales cumplidos
- SNR promedio > 2.0
- Coherencia parcial

#### ❌ No Detectado
- Criterios no cumplidos
- SNR < 1.5
- No coherencia entre detectores

## Reproducibilidad

### Datos GWOSC

Los datos utilizados son públicos y accesibles a través de:

- **Portal**: https://gwosc.org
- **API**: GWPy `fetch_open_data`
- **Formato**: HDF5 strain data

### Parámetros Fijos

Todos los parámetros están documentados y fijos:

- Filtro bandpass: [140.5-143.0 Hz]
- Ventana temporal: ±0.3s
- Q mínimo: 30
- Sample rate: 4096 Hz

### Código Abierto

El código es completamente abierto y está disponible en:

```
https://github.com/motanova84/141hz/
```

## Referencias

1. **GWOSC**: Gravitational Wave Open Science Center
   - https://gwosc.org

2. **GWPy Documentation**: GWPy - Python package for gravitational-wave astrophysics
   - https://gwpy.github.io/

3. **Q-Transform**: Time-frequency analysis for gravitational waves
   - Chatterji et al., Classical and Quantum Gravity (2004)

4. **LIGO Scientific Collaboration**: Data quality and detector characterization
   - https://www.ligo.org/

## Contacto

Para preguntas, sugerencias o reportar problemas:

- **Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)
- **Repositorio**: https://github.com/motanova84/141hz/
- **Issues**: https://github.com/motanova84/141hz/issues

## Licencia

Este código está bajo licencia MIT. Ver archivo LICENSE para más detalles.
