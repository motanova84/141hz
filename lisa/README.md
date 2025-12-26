# 🔭 LISA - Laser Interferometer Space Antenna

## Objetivo

Detectar o falsar la existencia de una línea espectral universal a **f₀ = 141.7001 ± 0.3 Hz** en el espectro de fondo de ondas gravitacionales.

## Modelo Teórico

El modelo de Gravedad Cuántica Noésica (GQN) predice armónicos descendentes de la frecuencia prima:

```
f_n = f₀ / (n·φ), n ∈ ℕ
```

donde φ = (1 + √5)/2 es el número áureo.

Para LISA (rango operativo: 0.1 mHz – 1 Hz), se esperan resonancias en:
- **f₁ = 0.0877 Hz** (n=1)
- **f₂ = 0.0542 Hz** (n=2)
- etc.

## Implementación

### Time Delay Interferometry (TDI)

LISA utiliza tres naves espaciales separadas 2.5 millones de km formando un triángulo equilátero. El TDI combina las mediciones láser para cancelar el ruido del disparo de fotones y las fluctuaciones del reloj.

### Cálculo de SNR

El SNR para ondas gravitacionales continuas se calcula como:

```
SNR_LISA = h₀ / √[S_n(f) / T_obs]
```

donde:
- **h₀**: amplitud de deformación de la onda gravitacional
- **S_n(f)**: densidad espectral de ruido de LISA
- **T_obs**: tiempo de observación

### Densidad Espectral de Ruido

El ruido de LISA proviene de dos fuentes principales:

1. **Ruido de aceleración** (masas de prueba): S_a ~ 3×10⁻¹⁵ m/s²/√Hz @ 1 mHz
2. **Ruido óptico** (disparo fotónico): S_x ~ 15 pm/√Hz

## Uso

### Ejecución básica

```bash
cd lisa
python3 lisa_search_pipeline.py
```

### Parámetros configurables

```python
from lisa_search_pipeline import LISASearchPipeline

# Crear pipeline
pipeline = LISASearchPipeline(
    sample_rate=10.0,      # Hz
    duration=86400.0       # 1 día en segundos
)

# Ejecutar búsqueda dirigida
results = pipeline.run_targeted_search(
    n_harmonics=10,
    save_results=True,
    output_dir="lisa_results"
)

# Generar gráficos
pipeline.plot_results(results)
```

## Resultados

Los resultados se guardan en `lisa_results/`:
- `lisa_search_results.json`: Datos numéricos completos
- `lisa_search_plot.png`: Visualizaciones del espectro y SNR

### Estructura de resultados

```json
{
  "f0": 141.7001,
  "phi": 1.618033988749895,
  "harmonics": [0.0877, 0.0542, ...],
  "detections": [
    {
      "target_frequency": 0.0877,
      "detected_frequency": 0.0878,
      "power": 1.234e-20,
      "snr_estimated": 8.5,
      "significant": true
    }
  ],
  "theoretical_snr": [...]
}
```

## Criterio de Falsación

**Predicción**: Si existe coherencia gravitacional en el campo noésico, aparecerá un pico estacionario en alguno de los armónicos descendentes de f₀.

**Falsación**: La ausencia de picos significativos (SNR < 6) en todos los armónicos dentro de LISA bandwidth falsaría la predicción de estructura armónica del modelo GQN.

## Datos Reales

Para análisis con datos reales de LISA Pathfinder:

1. Descargar datos del [ESA Archive](https://www.cosmos.esa.int/web/lisa-pathfinder-archive)
2. Procesarlos con formato TDI
3. Modificar `run_targeted_search()` para cargar datos reales

```python
# Ejemplo con datos reales
from gwpy.timeseries import TimeSeries

# Cargar datos LISA Pathfinder
data = TimeSeries.read('lisa_pathfinder_data.hdf5')

# Ejecutar análisis
results = pipeline.perform_fft_analysis(
    data.value,
    target_frequencies=pipeline.calculate_harmonic_frequencies()
)
```

## Referencias

- LISA Consortium: https://www.lisamission.org/
- LISA Pathfinder: https://www.cosmos.esa.int/web/lisa-pathfinder
- TDI: Armstrong, J. W., et al. (1999). "Time-Delay Interferometry"
- Modelo GQN: Ver `PAPER.md` en el repositorio principal

## Dependencias

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
gwpy>=3.0.0  # Opcional, para datos reales
```
