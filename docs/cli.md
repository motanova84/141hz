# CLI — Interfaz de Línea de Comandos

QCAL proporciona una interfaz de línea de comandos robusta para análisis de coherencia en datos de ondas gravitacionales.

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Comando principal: `qcal analyze`

### Uso básico

```bash
qcal analyze --event GW150914 --detector H1 --freq 141.7
```

### Parámetros

| Parámetro | Tipo | Descripción | Requerido | Default |
|-----------|------|-------------|-----------|---------|
| `--event` | str | ID del evento (e.g., GW150914) | Sí | - |
| `--detector` | str | Detector (H1, L1, V1) | Sí | - |
| `--freq` | float | Frecuencia objetivo (Hz) | No | 141.7 |
| `--output` | str | Directorio de salida | No | `results/` |
| `--format` | str | Formato: `json`, `csv`, `png` | No | `json,png` |

### Ejemplos

#### Análisis estándar de GW150914

```bash
qcal analyze --event GW150914 --detector H1
```

#### Análisis multi-detector

```bash
qcal analyze --event GW150914 --detector H1 --output results/h1/
qcal analyze --event GW150914 --detector L1 --output results/l1/
```

#### Exportar solo CSV

```bash
qcal analyze --event GW150914 --detector H1 --format csv
```

## Scripts auxiliares

### Validación completa

```bash
python run_all_validations.py
```

Ejecuta todas las validaciones del proyecto:
- Validación de radio cuántico
- Validación de energía cuántica
- Validación de simetría discreta
- Tests unitarios

### Análisis multi-evento

```bash
python multi_event_analysis.py
```

Analiza múltiples eventos de GWTC-1 en paralelo.

## Salida

Los resultados se guardan en el directorio especificado con `--output`:

```
results/
├── GW150914_H1_141.7Hz.json    # Resultados numéricos
├── GW150914_H1_spectrum.png    # Espectro de potencia
└── GW150914_H1_timeseries.png  # Serie temporal
```

Ver [Formatos de salida](FORMATOS_SALIDA.md) para detalles completos.

## Troubleshooting

### Error: "No module named 'qcal'"

Asegúrate de haber instalado las dependencias:

```bash
pip install -r requirements.txt
```

### Error de descarga de datos GWOSC

Verifica tu conexión a internet y que el evento existe en GWOSC:

```bash
# Listar eventos disponibles
python -c "import gwosc; print(gwosc.datasets.find_datasets())"
```

### Rendimiento lento

Para análisis largos, considera usar:

```bash
# Ejecutar en background
nohup qcal analyze --event GW150914 --detector H1 > analysis.log 2>&1 &
```

## Ver también

- [Reproducibilidad](reproducibilidad.md): Gestión de entornos
- [Validación](validation.md): Tests y CI/CD
- [Tutorial completo](TUTORIAL_COMPLETO.md): Guía paso a paso
# CLI

```bash
pip install -e .
python -m qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts
```

## Salidas

- **CSV**: `artifacts/tables/GWTC-1_band_141.7.csv`
- **PNG**: `artifacts/figures/GWTC-1_band_141.7.png`
# QCAL Command-Line Interface

## Installation

```bash
# From source
git clone https://github.com/motanova84/141hz.git
cd 141hz
pip install -e .

# Verify installation
qcal --version
```

## Basic Usage

### Analyze Command

The primary command for QCAL analysis:

```bash
qcal analyze [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--catalog` | str | required | Catalog name (GWTC-1, GWTC-2, GWTC-3, O4) |
| `--band` | float | 141.7 | Center frequency for analysis (Hz) |
| `--bandwidth` | float | 2.0 | Bandwidth around center frequency (Hz) |
| `--detector` | str | H1 | Detector name (H1, L1, V1, KAGRA) |
| `--outdir` | path | artifacts | Output directory for results |
| `--precision` | int | 50 | Decimal precision for mpmath calculations |
| `--event` | str | None | Specific event name (e.g., GW150914) |
| `--format` | str | json | Output format (json, csv, hdf5) |

### Examples

#### 1. Analyze GWTC-1 catalog with H1 detector

```bash
qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts
```

**Output:**
```
artifacts/
├── GWTC-1_H1_141.7Hz_summary.json
├── GWTC-1_H1_141.7Hz_events.csv
├── GW150914_H1_psd.png
├── GW151226_H1_psd.png
└── ...
```

#### 2. Analyze specific event with high precision

```bash
qcal analyze --catalog GWTC-1 --event GW150914 --band 141.7001 \
             --detector H1 --precision 100 --outdir results/gw150914
```

#### 3. Multi-detector analysis

```bash
# H1
qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts/h1

# L1
qcal analyze --catalog GWTC-1 --band 141.7 --detector L1 --outdir artifacts/l1

# V1
qcal analyze --catalog GWTC-1 --band 141.7 --detector V1 --outdir artifacts/v1

# Compare results
qcal compare --dirs artifacts/h1 artifacts/l1 artifacts/v1 --outdir artifacts/combined
```

#### 4. O4 catalog analysis

```bash
qcal analyze --catalog O4 --band 141.7 --detector H1 --outdir artifacts/o4
```

#### 5. Custom bandwidth and format

```bash
qcal analyze --catalog GWTC-1 --band 141.7 --bandwidth 5.0 \
             --detector H1 --format hdf5 --outdir artifacts/wide_band
```

## Advanced Commands

### Validate Command

Run validation protocols on analysis results:

```bash
qcal validate --input artifacts/GWTC-1_H1_141.7Hz_summary.json \
              --criteria all --outdir validation_results
```

**Validation criteria:**
- `radio_cuantico`: Quantum radio (r_ψ) test
- `energia_cuantica`: Quantum energy test
- `simetria_discreta`: Discrete symmetry test
- `all`: Run all three criteria

### Compare Command

Compare results across detectors or catalogs:

```bash
qcal compare --dirs artifacts/h1 artifacts/l1 artifacts/v1 \
             --outdir comparison --plot
```

### Export Command

Export results to different formats:

```bash
# Export to LaTeX table
qcal export --input artifacts/summary.json --format latex --output table.tex

# Export to PDF report
qcal export --input artifacts/summary.json --format pdf --output report.pdf

# Export figures
qcal export --input artifacts/ --format figures --output figures/
```

## Configuration File

Create a `qcal.yaml` configuration file for repeated analyses:

```yaml
# qcal.yaml
default:
  band: 141.7001
  bandwidth: 2.0
  precision: 50
  outdir: artifacts

catalogs:
  GWTC-1:
    detectors: [H1, L1, V1]
    events:
      - GW150914
      - GW151226
      - GW170814
      # ... more events
  
  O4:
    detectors: [H1, L1]
    download: true

validation:
  criteria: [radio_cuantico, energia_cuantica, simetria_discreta]
  significance: 0.05
  snr_threshold: 5.0
```

Run with config:

```bash
qcal analyze --config qcal.yaml --catalog GWTC-1
```

## Output Format

### JSON Summary

```json
{
  "catalog": "GWTC-1",
  "detector": "H1",
  "center_frequency": 141.7001,
  "bandwidth": 2.0,
  "events": [
    {
      "name": "GW150914",
      "gps_time": 1126259462.4,
      "peak_frequency": 141.65,
      "delta_f": -0.05,
      "snr": 23.5,
      "p_value": 1.2e-26,
      "power_db": 2.1,
      "validated": true
    }
  ],
  "summary": {
    "total_events": 11,
    "detected": 11,
    "detection_rate": 1.0,
    "mean_snr": 21.38,
    "std_snr": 6.38,
    "mean_delta_f": -0.12,
    "combined_significance": "10.5σ"
  }
}
```

### CSV Export

```csv
event,detector,f_peak,delta_f,snr,p_value,power_db,validated
GW150914,H1,141.65,-0.05,23.5,1.2e-26,2.1,true
GW151226,H1,141.72,0.02,18.3,3.4e-21,1.8,true
...
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QCAL_CACHE_DIR` | Cache directory for downloaded data | `~/.qcal/cache` |
| `QCAL_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `QCAL_NUM_WORKERS` | Number of parallel workers | `4` |
| `GWOSC_API_KEY` | GWOSC API key (if required) | None |

## Troubleshooting

### Data Download Issues

```bash
# Clear cache
rm -rf ~/.qcal/cache

# Retry with verbose logging
QCAL_LOG_LEVEL=DEBUG qcal analyze --catalog GWTC-1 --detector H1
```

### Memory Issues

```bash
# Reduce precision
qcal analyze --precision 30 ...

# Process one event at a time
qcal analyze --event GW150914 ...
```

### Missing Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install optional dependencies
pip install weasyprint kaleido  # For PDF export
```

## Getting Help

```bash
# General help
qcal --help

# Command-specific help
qcal analyze --help
qcal validate --help
qcal compare --help
```

## See Also

- [Overview](overview.md) - QCAL architecture and features
- [Validation](validation.md) - Validation protocols
- [Roadmap](roadmap.md) - Development roadmap
