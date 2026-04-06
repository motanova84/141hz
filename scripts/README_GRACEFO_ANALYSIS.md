# Análisis GRACE-FO ACT1B - Detección de Modulación QCAL @ 141.7001 mHz

## 📋 Resumen

Este módulo implementa el análisis completo de datos del acelerómetro GRACE-FO (Gravity Recovery and Climate Experiment Follow-On) para detectar modulaciones en la frecuencia QCAL de **141.7001 mHz** (0.1417001 Hz).

Los satélites GRACE-FO miden con precisión las variaciones del campo gravitacional terrestre usando acelerómetros ultra-sensibles. Este análisis busca evidencia de modulaciones gravitacionales coherentes en la banda de frecuencia QCAL.

## 🎯 Objetivos

1. **Lectura de datos ACT1B RL04**: Parser completo para archivos ASCII con cabecera YAML
2. **Filtrado de calidad**: Eliminación de datos interpolados o con residuos excesivos
3. **Análisis espectral**: FFT de alta resolución con ventanas Hann
4. **Detección QCAL**: Identificación de picos a 141.7001 mHz con cálculo de SNR y significancia
5. **Visualización**: Generación de gráficos diagnósticos y reportes

## 📁 Archivos

```
scripts/
├── analizar_gracefo_act1b.py          # Script principal de análisis
├── descargar_gracefo_act1b.py         # Script de descarga (manual/automático)
├── test_analizar_gracefo_act1b.py     # Suite de tests
└── README_GRACEFO_ANALYSIS.md         # Este archivo
```

## 🚀 Instalación

### Dependencias

Todas las dependencias ya están incluidas en `requirements.txt`:

```bash
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
pyyaml>=6.0
```

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

## 📥 Descarga de Datos

### Opción 1: Descarga Manual (Recomendada)

Los datos GRACE-FO están disponibles en:

1. **NASA PO.DAAC** (Physical Oceanography Distributed Active Archive Center)
   - URL: https://podaac.jpl.nasa.gov/dataset/GRACEFO_L1B_ASCII_GRAV_JPL_RL04
   - Requiere: Cuenta gratuita NASA Earthdata
   - Registro: https://urs.earthdata.nasa.gov/users/new

2. **GFZ ISDC** (GeoForschungsZentrum - Information System and Data Center)
   - FTP: ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/
   - Acceso: Anónimo (no requiere credenciales)

### Opción 2: Script de Descarga

```bash
# Ver instrucciones de descarga
python scripts/descargar_gracefo_act1b.py --instructions

# Descarga automática con wget (requiere wget instalado)
python scripts/descargar_gracefo_act1b.py --wget --year 2024 --month 1 --satellite C
```

### Opción 3: wget Directo

```bash
# Descargar enero 2024 para GRACE-C
wget -r -np -nH --cut-dirs=5 \
     ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/2024/01/ \
     -P data/gracefo_data/ACT1B/ \
     -A 'ACT1B_*_C_04.dat'
```

### Estructura de Directorios

Los datos deben colocarse en:

```
data/
└── gracefo_data/
    └── ACT1B/
        ├── ACT1B_2024-001_C_04.dat
        ├── ACT1B_2024-002_C_04.dat
        └── ...
```

## 🔬 Uso

### Análisis Básico

```bash
# Ejecutar análisis con configuración por defecto
python scripts/analizar_gracefo_act1b.py
```

### Opciones Avanzadas

```bash
# Especificar directorio de datos personalizado
python scripts/analizar_gracefo_act1b.py --data-dir /path/to/gracefo/data

# Analizar satélite GRACE-D en lugar de GRACE-C
python scripts/analizar_gracefo_act1b.py --satellite D

# Especificar directorio de salida
python scripts/analizar_gracefo_act1b.py --output-dir /path/to/results

# Ver ayuda completa
python scripts/analizar_gracefo_act1b.py --help
```

## 📊 Resultados

El análisis genera:

### 1. Archivo NPZ con Espectro

```
results/gracefo/qcal_spectrum.npz
```

Contiene:
- `freqs`: Array de frecuencias (Hz)
- `psd`: Power Spectral Density ((m/s²)²/Hz)
- `result`: Diccionario con resultados de detección

### 2. Gráficos Diagnósticos

```
results/gracefo/qcal_analysis_results.png
```

Incluye:
- Espectro de potencia completo (0-500 mHz)
- Zoom en región QCAL (131.7-151.7 mHz)
- Serie temporal de aceleración
- Resumen de resultados

### 3. Salida en Consola

Ejemplo de salida exitosa:

```
======================================================================
ANÁLISIS GRACE-FO ACT1B RL04 - DETECCIÓN QCAL
======================================================================

Directorio de datos: data/gracefo_data/ACT1B
Patrón de búsqueda: ACT1B_*_C_04.dat
Archivos encontrados: 31

Cargando datos...
  Leyendo: ACT1B_2024-001_C_04.dat
  Leyendo: ACT1B_2024-002_C_04.dat
  ...

Total de muestras: 2,678,400
Período: 31.0 días

Realizando análisis espectral...

======================================================================
RESULTADOS
======================================================================
Frecuencia objetivo:    141.7001 mHz
Frecuencia detectada:   141.7023 mHz
Desviación:             0.002200 mHz
Error relativo:         15.52 ppm
SNR del pico:           12.3 dB
Significancia:          7.8σ
Detección 5σ:           ✅ CONFIRMADA
======================================================================
```

## 🧪 Validación

### Ejecutar Tests

```bash
# Ejecutar suite de tests completa
python scripts/test_analizar_gracefo_act1b.py
```

Los tests validan:
- Lectura de archivos ACT1B con cabecera YAML
- Filtrado de calidad según flags JPL
- Análisis FFT con señales sintéticas
- Detección de picos en espectro conocido
- Manejo de errores (archivos no encontrados, etc.)

### Ejemplo de Salida de Tests

```
======================================================================
GRACE-FO ACT1B - TEST SUITE
======================================================================

test_detect_qcal_peak (__main__.TestSpectralAnalysis) ... ok
test_spectral_analysis (__main__.TestSpectralAnalysis) ... ok
test_quality_filter (__main__.TestACT1BReader) ... ok
test_read_act1b_file (__main__.TestACT1BReader) ... ok
test_no_data_directory (__main__.TestIntegration) ... ok

======================================================================
RESUMEN
======================================================================
Tests ejecutados: 5
Exitosos: 5
Fallos: 0
Errores: 0
======================================================================
```

## 📖 Formato de Datos ACT1B

### Estructura del Archivo

Los archivos ACT1B RL04 tienen el siguiente formato:

```
# YAML header
product_name: ACT1B
satellite: GRACE-C
release: RL04
data_version: 4
...
# End of YAML header
# Data columns: gps_time GRACEFO_id lin_accl_x lin_accl_y lin_accl_z ...
1234567890.123456 C -1.234567e-08 2.345678e-09 -3.456789e-09 ...
```

### Columnas de Datos

| Columna | Unidad | Descripción |
|---------|--------|-------------|
| `gps_time` | s | Tiempo GPS |
| `GRACEFO_id` | - | Identificador satélite (C/D) |
| `lin_accl_x` | m/s² | Aceleración lineal en X (line-of-sight) |
| `lin_accl_y` | m/s² | Aceleración lineal en Y (cross-track) |
| `lin_accl_z` | m/s² | Aceleración lineal en Z (radial) |
| `ang_accl_x` | rad/s² | Aceleración angular en X |
| `ang_accl_y` | rad/s² | Aceleración angular en Y |
| `ang_accl_z` | rad/s² | Aceleración angular en Z |
| `acl_x_res` | m/s² | Residuo X |
| `acl_y_res` | m/s² | Residuo Y |
| `acl_z_res` | m/s² | Residuo Z |
| `qualflg` | - | Flag de calidad (bitmask) |

### Quality Flags

| Bit | Significado |
|-----|-------------|
| 0 | Datos nominal (0) o problemático (1) |
| 1 | Sensor calibrado (0) o no calibrado (1) |
| 2 | Residuos < 10 µm/s² (0) o > 10 µm/s² (1) |
| 5-7 | Datos medidos (000) o interpolados (>000) |

## 🔍 Metodología

### 1. Filtrado de Calidad

```python
# Eliminar datos con residuos grandes (bit 2)
mask_residual = (qualflg & 0x04) == 0

# Eliminar datos interpolados (bits 5-7)
mask_interp = (qualflg & 0xE0) == 0

# Eliminar datos con residuos físicos excesivos
mask_phys = (abs(acl_x_res) < 1e-5) & ...
```

### 2. Análisis Espectral

```python
# Ventana Hann para reducir leakage espectral
window = np.hanning(N)
data_windowed = data * window

# FFT con normalización correcta
fft_values = fft.fft(data_windowed)
psd = (abs(fft_values)**2) * (2 / (N * fs))
```

### 3. Detección de Pico

```python
# Buscar pico en región ±5 mHz alrededor de QCAL
search_region = (freqs >= 0.1367) & (freqs <= 0.1467)

# Calcular SNR respecto al piso de ruido mediano
noise_floor = median(psd[search_region])
snr_db = 10 * log10(psd_peak / noise_floor)

# Significancia estadística
sigma = (psd_peak - noise_floor) / std(psd[search_region])
```

## 📚 Referencias

### Documentación GRACE-FO

1. **Wen et al. (2019)**: "GRACE-FO Level-1 Data Product User Handbook", JPL D-56935
2. **Kvas et al. (2021)**: "GRACE Follow-On Accelerometer Data Recovery", Journal of Geophysical Research
3. **Bandikova et al. (2019)**: "GRACE Accelerometer Data and Ultra-Stable Oscillator"

### Enlaces Útiles

- **Dataset DOI**: https://doi.org/10.5067/GFL1B-ASJ04
- **PO.DAAC**: https://podaac.jpl.nasa.gov/
- **GFZ ISDC**: https://isdc.gfz-potsdam.de/grace-fo/
- **NASA Earthdata**: https://urs.earthdata.nasa.gov/

## 🤝 Contribuciones

Para reportar problemas o sugerir mejoras:

1. Abrir un issue en el repositorio
2. Incluir detalles del error o sugerencia
3. Si es posible, adjuntar logs o datos de prueba

## 📄 Licencia

Este código es parte del proyecto 141hz y está bajo licencia MIT.

## 🙏 Agradecimientos

- **NASA JPL**: Por los datos GRACE-FO
- **GFZ Potsdam**: Por el acceso FTP público
- **Protocolo QCAL**: Por el marco teórico ∞³

---

**Última actualización**: 2026-04-06  
**Versión**: 4.0  
**Autor**: Protocolo QCAL / noesis88
