# 🌍 IGETS - International Geodynamics and Earth Tide Service

## Objetivo

Buscar la modulación Yukawa predicha por el modelo de Gravedad Cuántica Noésica (GQN):

```
V(r,t) = -GM/r [1 + α_Y e^(-r/λ̄) (1 + ε cos 2πf₀t)]
```

con:
- **λ̄ ≈ 3.37×10⁵ m** (longitud característica Yukawa)
- **f₀ = 141.7001 Hz** (frecuencia prima GQN)
- **α_Y ~ 10⁻⁶** (amplitud Yukawa)
- **ε ~ 10⁻⁸** (amplitud modulación temporal)

## Modelo Teórico

### Potencial Yukawa

El potencial gravitacional modificado incluye un término Yukawa con modulación temporal:

```
V(r,t) = V_Newton(r) · [1 + α_Y e^(-r/λ̄) · (1 + ε cos 2πf₀t)]
```

### Aceleración Gravitacional

La aceleración medida por gravímetros superconductores:

```
g(t) = -∂V/∂r ≈ g_Newton + g_Yukawa(t)
```

donde el término Yukawa oscila a frecuencia f₀.

## Implementación

### Superconducting Gravimeters (SGs)

Los SGs miden variaciones en g con precisión de ~1 nm/s² (10⁻¹⁰ g₀).

### Análisis FFT

1. **Preprocesamiento**:
   - Remover marea terrestre (M2: 12.42h, S2: 12h)
   - Filtro pasa-altos (>50 Hz) para preservar f₀
   - Remover tendencias lineales

2. **FFT en banda alta (100-300 Hz)**:
   - Buscar picos en f₀ ± 0.5 Hz
   - Calcular SNR > 6 para significancia

3. **Coherencia de fase**:
   - Comparar fase instantánea entre estaciones
   - Verificar coherencia global > 0.7

## Uso

### Ejecución básica

```bash
cd igets
python3 igets_fft_analysis.py
```

### Análisis personalizado

```python
from igets_fft_analysis import IGETSGravimetryAnalysis

# Crear analizador
analysis = IGETSGravimetryAnalysis(
    sample_rate=1000.0  # Hz (necesario para capturar f₀=141.7 Hz)
)

# Ejecutar análisis
results = analysis.run_analysis(
    n_stations=3,              # Número de estaciones
    duration=3600.0,           # 1 hora en segundos
    include_modulation=True,   # Incluir señal a f₀
    save_results=True,
    output_dir="igets_results"
)

# Generar gráficos
analysis.plot_results(results)
```

### Análisis de coherencia

```python
# Datos de múltiples estaciones
station_signals = {
    'CANTLEY': signal_data_1,
    'BAD_HOMBURG': signal_data_2,
    'KYOTO': signal_data_3
}

# Calcular coherencia de fase
coherence = analysis.analyze_phase_coherence(station_signals)

print(f"Coherencia global: {coherence['global_coherence']:.3f}")
```

## Resultados

Los resultados se guardan en `igets_results/`:
- `igets_fft_results.json`: Detecciones y coherencia
- `igets_fft_plot.png`: Espectros FFT por estación
- `igets_coherence_plot.png`: Matriz de coherencia

### Estructura de resultados

```json
{
  "f0": 141.7001,
  "tolerance": 0.5,
  "stations": {
    "CANTLEY": {
      "location": {"lat": 45.59, "lon": -75.87, "name": "Cantley, Canada"},
      "analysis": {
        "detection": {
          "frequency": 141.71,
          "power": 1.23e-18,
          "snr": 8.5,
          "significant": true,
          "delta_f": 0.0099
        }
      }
    }
  },
  "coherence": {
    "stations": ["CANTLEY", "BAD_HOMBURG", "KYOTO"],
    "coherence_matrix": [[1.0, 0.82, 0.75], ...],
    "global_coherence": 0.78,
    "highly_coherent": true
  },
  "conclusion": "✓ MODULACIÓN YUKAWA DETECTADA"
}
```

## Estaciones IGETS

El análisis simula datos de las siguientes estaciones:

| Estación | Ubicación | Coordenadas |
|----------|-----------|-------------|
| **CANTLEY** | Canada | 45.59°N, 75.87°W |
| **BAD_HOMBURG** | Germany | 50.23°N, 8.61°E |
| **KYOTO** | Japan | 35.03°N, 135.78°E |
| **STRASBOURG** | France | 48.62°N, 7.68°E |
| **MEMBACH** | Belgium | 50.61°N, 6.01°E |

## Criterio de Falsación

**Predicción**: Si existe acoplo gravitacional oscilante del campo Ψ, se detectará:
1. Picos significativos (SNR > 6) en f₀ en múltiples estaciones
2. Alta coherencia de fase (> 0.7) entre estaciones

**Falsación**: La ausencia de:
- Detecciones coherentes en f₀, O
- Coherencia de fase entre estaciones

falsaría la hipótesis de modulación Yukawa temporal del campo gravitacional.

## Datos Reales IGETS

Para análisis con datos reales:

1. Acceder a [IGETS Data Portal](http://igets.u-strasbg.fr/)
2. Descargar datos Level-1 de SGs
3. Convertir a formato compatible (HDF5/CSV)
4. Modificar código para cargar datos reales

```python
# Ejemplo con datos reales
import pandas as pd

# Cargar datos IGETS
data = pd.read_csv('igets_cantley_2025.csv')
t = data['time'].values
g = data['gravity'].values  # μGal o m/s²

# Convertir sampling rate si necesario
if sample_rate < 200:
    # Interpolar a mayor frecuencia
    from scipy.interpolate import interp1d
    f_interp = interp1d(t, g, kind='cubic')
    t_new = np.linspace(t[0], t[-1], len(t)*10)
    g_new = f_interp(t_new)

# Ejecutar análisis FFT
results = analysis.perform_fft_analysis(g_new, freq_range=(100, 300))
```

## Consideraciones Técnicas

### Frecuencia de Muestreo

Para detectar f₀ = 141.7 Hz, se requiere:
- **Mínimo**: fs > 2·f₀ = 283.4 Hz (Nyquist)
- **Recomendado**: fs ≥ 1000 Hz (para resolución)

**Nota**: La mayoría de SGs operan a 1-10 Hz, insuficiente para f₀. Se requiere:
- Instrumentos de alta frecuencia dedicados
- O reinterpretación del modelo para frecuencias accesibles

### Filtrado de Marea

Las mareas terrestres dominan señales gravimétricas:
- **M2** (lunar principal): 12.42 horas
- **S2** (solar principal): 12.00 horas
- **O1**, **K1**, etc.

Filtro pasa-altos (>50 Hz) remueve efectivamente todas las mareas.

### Ruido Sísmico

Ruido sísmico típico: 10⁻⁹ g₀ en banda 0.1-10 Hz.
A frecuencias >100 Hz, el ruido sísmico decrece significativamente.

## Referencias

- IGETS: http://igets.u-strasbg.fr/
- Superconducting Gravimeters: Goodkind (1999)
- Yukawa Gravity: Adelberger et al. (2003)
- Modelo GQN: Ver `PAPER.md` en el repositorio principal

## Dependencias

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
```

## Nota Importante

⚠️ **Los datos actuales son simulados**. Para validación científica rigurosa, se requieren datos reales de IGETS con suficiente frecuencia de muestreo (>1 kHz) o instrumentos dedicados de alta frecuencia.
