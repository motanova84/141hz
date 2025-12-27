# GWTC-3 Complete Analysis

## Overview

This script performs a comprehensive analysis of GWTC-3 (Gravitational Wave Transient Catalog 3) events, searching for the 141.7 Hz frequency signature in gravitational wave data from 2019-2020.

## Features

- **Automatic Dependency Installation**: The script automatically installs required packages (gwpy, pycbc) if not already present
- **30 Representative Events**: Analyzes a curated selection of significant GWTC-3 events
- **Robust Analysis Pipeline**: Includes preprocessing, filtering, and SNR calculation
- **Statistical Comparison**: Compares GWTC-3 results with GWTC-1 (100% detection rate)
- **Visualization**: Generates plots comparing detection rates and SNR distributions
- **JSON Output**: Saves detailed results for further analysis

## Usage

### Using Make (Recommended)

```bash
make gwtc3-analysis
```

This will:
1. Set up the virtual environment
2. Install dependencies
3. Run the complete GWTC-3 analysis
4. Generate results and visualizations

### Direct Execution

```bash
# With virtual environment
./venv/bin/python scripts/analisis_gwtc3_completo.py

# Or directly (will auto-install dependencies)
python3 scripts/analisis_gwtc3_completo.py
```

### Google Colab

The script is designed to work seamlessly in Google Colab:

```python
!wget https://raw.githubusercontent.com/motanova84/141hz/main/scripts/analisis_gwtc3_completo.py
!python analisis_gwtc3_completo.py
```

## Parameters

The script uses the following default parameters:

- **Target Frequency**: 141.7 Hz
- **Frequency Tolerance**: ±1.0 Hz (search band: 140.7-142.7 Hz)
- **SNR Threshold**: 5.0
- **Sample Window**: 4 seconds centered on each event (±2s)

## Analyzed Events

The script analyzes 30 representative GWTC-3 events:

- GW190412, GW190425, GW190521, GW190814
- GW190828_063405 through GW190924_021846
- GW191103_012549 through GW191222_033537
- GW200105_162426 through GW200316_215756

These events represent the most significant detections from LIGO/Virgo's O3 observation run.

## Output Files

### 1. `gwtc3_analysis_results.json`

Complete analysis results including:
- Timestamp
- Individual event results (success/failure, SNR, detection status)
- GWTC-3 statistics
- GWTC-1 comparison data
- Combined detection rate
- Scientific verdict

Example structure:
```json
{
  "timestamp": "2024-10-24T11:09:44.903Z",
  "freq_target": 141.7,
  "gwtc3": {
    "n_analyzed": 30,
    "n_successful": 28,
    "n_detected": 22,
    "detection_rate": 0.786
  },
  "combined": {
    "n_detected": 33,
    "n_total": 39,
    "detection_rate": 0.846
  },
  "verdict": "✅ CONFIRMACIÓN DEFINITIVA"
}
```

### 2. `gwtc3_results.png`

Two-panel visualization:
- **Panel 1**: Bar chart comparing GWTC-1, GWTC-3, and combined detection rates
- **Panel 2**: SNR distribution histogram for detected events

## Interpretation Guidelines

The script provides automatic interpretation based on combined detection rate:

| Detection Rate | Verdict | Recommended Action |
|---------------|---------|-------------------|
| ≥80% | ✅ CONFIRMACIÓN DEFINITIVA | Publish immediately |
| ≥60% | ⚠️ EVIDENCIA FUERTE | Subgroup analysis needed |
| ≥40% | ⚠️ EVIDENCIA MODERADA | Review parameter correlations |
| <40% | ❌ EVIDENCIA INSUFICIENTE | Review methodology |

## Technical Details

### Analysis Pipeline

1. **Data Acquisition**: Fetches H1 strain data from GWOSC
2. **Preprocessing**: Applies 20 Hz highpass filter
3. **Spectral Analysis**: Calculates Amplitude Spectral Density (ASD)
4. **Peak Detection**: Identifies minimum ASD (lowest noise) in target band
5. **SNR Calculation**: Compares in-band ASD to reference band (130-155 Hz)
6. **Detection Classification**: Applies SNR threshold

### Error Handling

The script includes robust error handling:
- Graceful failures for unavailable events
- Network timeout management
- Cooling-down periods every 10 events
- Detailed error logging

## Requirements

Automatically installed if needed:
- `gwpy >= 3.0.0` - Gravitational wave data access
- `pycbc >= 2.0.0` - Event catalog access
- `numpy >= 1.21.0` - Numerical computations
- `matplotlib >= 3.5.0` - Visualization
- `scipy` (via dependencies) - Signal processing

## Comparison with GWTC-1

The script includes built-in comparison with GWTC-1 results:
- **GWTC-1 (2015-2017)**: 11/11 events (100% detection rate)
- **GWTC-3 (2019-2020)**: Variable detection rate
- **Combined**: Provides statistical significance assessment

## Performance

- **Execution Time**: ~5-10 minutes depending on network speed
- **Data Downloaded**: ~4 seconds of strain data per event
- **Memory Usage**: Moderate (< 2GB typical)
- **Network**: Requires GWOSC connectivity

## Troubleshooting

### Common Issues

1. **Network Timeouts**: The script includes automatic retry and cooling periods
2. **Missing Dependencies**: Auto-installation handles this automatically
3. **Data Unavailable**: Some events may not have public data yet - these are logged and skipped

### Debug Mode

For verbose output, check individual event results in the JSON file.

## Related Scripts

- `busqueda_sistematica_gwtc1.py` - GWTC-1 systematic search
- `analisis_bayesiano_multievento.py` - Bayesian multi-event analysis
- `pipeline_validacion.py` - Scientific validation pipeline

## Scientific Context

This analysis is part of the investigation into the 141.7001 Hz fundamental frequency hypothesis, which proposes a connection between Calabi-Yau compactification scales and observable gravitational wave signatures.

## Citation

If you use this script in your research, please cite:

```
GW250114-141Hz Analysis Repository
https://github.com/motanova84/141hz
```

## License

See repository LICENSE file for details.

## Contact

For issues or questions, please open an issue on the GitHub repository.
