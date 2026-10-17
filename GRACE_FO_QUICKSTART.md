# 🛰️ GRACE-FO Analysis - Quick Start

## Overview

This repository now includes complete analysis tools for **GRACE-FO (Gravity Recovery and Climate Experiment Follow-On)** satellite accelerometer data, specifically designed to detect QCAL modulation at **141.7001 mHz**.

## What is GRACE-FO?

GRACE-FO is a NASA/GFZ satellite mission that measures Earth's gravitational field variations with ultra-precise accelerometers. These measurements can potentially reveal coherent gravitational modulations at the QCAL frequency.

## Quick Start

### 1. Download Data

```bash
# See download instructions
python scripts/descargar_gracefo_act1b.py --instructions

# Or download automatically (requires wget)
python scripts/descargar_gracefo_act1b.py --wget --year 2024 --month 1
```

### 2. Run Analysis

```bash
# Basic analysis
python scripts/analizar_gracefo_act1b.py

# Specify custom data directory
python scripts/analizar_gracefo_act1b.py --data-dir /path/to/data

# Analyze GRACE-D instead of GRACE-C
python scripts/analizar_gracefo_act1b.py --satellite D
```

### 3. View Results

Results are saved in `results/gracefo/`:
- `qcal_spectrum.npz` - Spectral data
- `qcal_analysis_results.png` - Diagnostic plots

## Expected Output

```
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

## Documentation

See [scripts/README_GRACEFO_ANALYSIS.md](scripts/README_GRACEFO_ANALYSIS.md) for complete documentation including:
- Data format specification
- Quality filtering methodology
- Spectral analysis details
- Download instructions
- Test suite usage

## Data Sources

- **NASA PO.DAAC**: https://podaac.jpl.nasa.gov/dataset/GRACEFO_L1B_ASCII_GRAV_JPL_RL04
- **GFZ ISDC FTP**: ftp://isdcftp.gfz-potsdam.de/grace-fo/Level-1B/JPL/RL04/ACT/

## Testing

```bash
# Run test suite
python scripts/test_analizar_gracefo_act1b.py
```

All tests should pass (5/5 expected).

---

**Integration with QCAL ∞³**: This GRACE-FO analysis complements the existing LIGO/Virgo gravitational wave analysis by searching for QCAL signatures in satellite accelerometer measurements, providing an independent validation pathway for the 141.7001 Hz fundamental frequency.
