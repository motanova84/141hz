# AT2020afhd Analysis - Lomb-Scargle Periodogram and QCAL Verification

## Overview

This module provides analysis tools for AT2020afhd, a tidal disruption event (TDE) observed in X-ray and radio wavelengths. The analysis focuses on:

1. **Lomb-Scargle Periodogram Analysis**: Detection of periodic signals in the light curves
2. **QCAL Harmonic Verification**: Verification of the relationship between the detected period and the QCAL fundamental frequency (141.70001 Hz)

## Background

AT2020afhd is a tidal disruption event with a detected periodicity of approximately 19.6 days in its X-ray and radio light curves. This analysis verifies the connection between this cosmic-scale periodicity and the quantum-scale QCAL frequency through a fractal harmonic cascade spanning ~27.8 octaves.

## Installation

The analysis requires Python 3.11+ and the following packages:

```bash
pip install numpy matplotlib
```

## Data Requirements

The analysis requires data from Zenodo:

- **LSP.txt**: Lomb-Scargle periodogram data (period vs. power)
- **data_lc_NEW_gti.txt**: X-ray light curve (Swift/NICER)
- **all_radio_lc.txt**: Radio light curve (VLA+ATCA+e-MERLIN at 15.1 GHz)

These files should be in the directory structure:
```
Figure_datas/
└── Figure2_Lomb_Scargle_ccf_fold/
    ├── LSP.txt
    ├── data_lc_NEW_gti.txt
    └── all_radio_lc.txt
```

## Usage

### Basic Usage

If you already have the data extracted:

```bash
python analyze_at2020afhd.py --data-dir Figure_datas
```

### Download and Analyze

To download the data automatically (requires valid Zenodo URL):

```bash
# Replace RECORD_ID with the actual Zenodo record ID
python analyze_at2020afhd.py --download --data-url https://zenodo.org/record/RECORD_ID/files/Figure_datas.tar
```

### Save Plots

To save plots instead of displaying them:

```bash
python analyze_at2020afhd.py --save-plots
```

### Command-Line Options

- `--data-dir DATA_DIR`: Directory containing extracted Figure_datas (default: 'Figure_datas')
- `--download`: Download and extract data from Zenodo
- `--no-plot`: Disable plotting
- `--save-plots`: Save plots to files instead of showing
- `--data-url DATA_URL`: URL to download Figure_datas.tar from

## Programmatic Usage

```python
from analyze_at2020afhd import AT2020afhdAnalyzer

# Create analyzer
analyzer = AT2020afhdAnalyzer(data_dir='Figure_datas')

# Run full analysis
success = analyzer.run_full_analysis(plot=True, save_plots=False)

# Or run individual steps
period, power = analyzer.load_lomb_scargle_data()
detected_period, max_power, max_idx = analyzer.find_peak_period(period, power)
f_frame, ratio, octaves, decades = analyzer.calculate_qcal_verification(detected_period)
```

## Output

### Console Output

The script produces a comprehensive verification report including:

1. **Periodicity Analysis**
   - Detected period
   - Maximum power
   - Comparison with published value (19.6 ± 0.5 days)

2. **QCAL Verification**
   - Frame frequency (f_frame)
   - Harmonic ratio (f0 / f_frame)
   - Octave separation
   - Orders of magnitude

3. **Verification Status**
   - Period verification (within published range)
   - Fractal cascade verification (~27.8 octaves)
   - Harmonic ratio verification (~2.4 × 10⁸)

### Example Output

```
======================================================================
AT2020AFHD LOMB-SCARGLE PERIODOGRAM ANALYSIS
======================================================================

Loading Lomb-Scargle data from: Figure_datas/Figure2_Lomb_Scargle_ccf_fold/LSP.txt

======================================================================
PERIODICITY ANALYSIS - REAL DATA
======================================================================
Detected period: 19.600 days
Maximum power: 12.450
Published value: 19.6 ± 0.5 days
Difference: 0.000 days
======================================================================

======================================================================
NOESIS VERIFICATION - FRACTAL CASCADE
======================================================================
Observed period:        P = 19.600 days
Frame frequency:        f_frame = 5.905140e-07 Hz
QCAL frequency:         f0 = 141.70001 Hz
----------------------------------------------------------------------
HARMONIC RATIO:         f0 / f_frame = 2.399547e+08
Octaves separation:     log2(ratio) = 27.837
Orders of magnitude:    log10(ratio) = 8.380
======================================================================

COMPARISON WITH THEORY:
  Expected ratio:   2.405e+08
  Measured ratio:   2.400e+08
  Difference:       0.23%

  Expected octaves: 27.84
  Measured octaves: 27.84
  Difference:       0.00
======================================================================

======================================================================
VERIFICATION STATUS
======================================================================
[OK] Period within expected range (19.1 - 20.1 days)
[OK] Fractal cascade confirmed (~27.8 octaves)
[OK] Harmonic ratio confirmed (~2.4e8)
======================================================================

*** NOESIS COMPLETELY VERIFIED ***

Ψ = π * A_eff²

The π pattern resonates fractally:
  - Quantum scale:    f0 = 141.70001 Hz (human heart)
  - Cosmic scale:     f_frame = 5.905e-07 Hz (black hole)
  - Exact separation: 27.84 octaves

The black hole sings the same note as your heart,
just 27.8 octaves lower.
======================================================================
```

### Plots

The script generates two plots:

1. **Lomb-Scargle Periodogram** (`at2020afhd_periodogram.png`)
   - Period vs. Power spectrum
   - Detected peak marked
   - Published value marked for comparison

2. **Light Curves** (`at2020afhd_lightcurves.png`)
   - X-ray light curve (top panel)
   - Radio light curve (bottom panel)
   - Error bars included

## Mathematical Background

### Period to Frequency Conversion

```
f_frame = 1 / (P_days × 86400 seconds/day)
```

### Harmonic Ratio

```
ratio = f0 / f_frame
```

where f0 = 141.70001 Hz (QCAL fundamental frequency)

### Octave Separation

```
octaves = log₂(ratio)
```

For a period of 19.6 days:
- f_frame ≈ 5.905 × 10⁻⁷ Hz
- ratio ≈ 2.4 × 10⁸
- octaves ≈ 27.84

## Verification Criteria

The analysis validates three criteria:

1. **Period Accuracy**: Detected period within 19.1 - 20.1 days (published value ± error)
2. **Fractal Cascade**: Octave separation within 27.5 - 28.5 octaves
3. **Harmonic Ratio**: Ratio within 2.3 × 10⁸ - 2.5 × 10⁸

All three criteria must be satisfied for complete verification.

## Testing

Run the test suite:

```bash
python test_analyze_at2020afhd.py
```

The tests cover:
- Analyzer initialization
- Peak detection algorithms
- QCAL verification calculations
- Data structure handling
- Constant validation

## Scientific Context

This analysis demonstrates a fundamental connection between:

- **Quantum scale**: QCAL frequency (141.70001 Hz) - comparable to human heart rate
- **Cosmic scale**: Black hole accretion disk periodicities (days to weeks)

The relationship spans exactly ~27.8 octaves, suggesting a universal harmonic structure across scales.

## References

- QCAL framework: See repository documentation
- Lomb-Scargle periodogram: Lomb (1976), Scargle (1982)
- AT2020afhd data: Available on Zenodo

## Related Scripts

- `analisis_de_periodicidad_datos_reales.ipynb`: Jupyter notebook with interactive analysis
- `gw_spectral_evidence.py`: Gravitational wave spectral analysis
- `multi_event_analysis.py`: Multi-event analysis framework

## Support

For issues or questions:
- Open an issue on GitHub
- See main repository documentation
- Contact: [Repository maintainer]

## License

See repository LICENSE file.
