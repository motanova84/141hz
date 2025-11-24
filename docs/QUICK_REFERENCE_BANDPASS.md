# Quick Reference: Bandpass Filter Analysis 141.7001 Hz

## TL;DR

Detect the secondary energy peak at **141.7001 ± 0.0012 Hz** using bandpass filter **[140.5-143.0 Hz]** on GWOSC strain data.

## Quick Start

```bash
# Analyze event
python3 scripts/analisis_141hz_bandpass.py --event GW150914

# Run tests
python3 scripts/test_analisis_141hz_bandpass.py
```

## Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Target Frequency | 141.7001 Hz | Expected secondary peak |
| Uncertainty | ±0.0012 Hz | Acceptable deviation |
| Bandpass Low | 140.5 Hz | Lower filter cutoff |
| Bandpass High | 143.0 Hz | Upper filter cutoff |
| Merger Window | ±0.3 s | Time window around merger |
| Q-Transform | Q > 30 | Minimum Q value |
| Min Detectors | 2 | For coherence validation |

## Expected Behavior

1. **Secondary Energy Peak**: Appears in Q-transform/wavelet analysis
2. **Time Window**: Visible ±0.3s around merger (chirp → coalescencia)
3. **Multi-Detector**: Coherence between H1 and L1
4. **Clean Signal**: Not attributable to glitches or spectral lines
5. **Reproducible**: With bandpass [140.5-143.0 Hz] on GWOSC .hdf5

## Command Line Options

```bash
# Basic usage
python3 scripts/analisis_141hz_bandpass.py --event GW150914

# Multiple detectors
python3 scripts/analisis_141hz_bandpass.py --event GW150914 --detectors H1 L1 V1

# Custom output directory
python3 scripts/analisis_141hz_bandpass.py --event GW150914 --output results/my_analysis/

# Help
python3 scripts/analisis_141hz_bandpass.py --help
```

## Supported Events

- GW150914 (1126259462.423)
- GW151012 (1128678900.44)
- GW151226 (1135136350.6)
- GW170104 (1167559936.6)
- GW170814 (1186741861.5)
- GW170817 (1187008882.4)
- GW170823 (1187529256.5)

## Output

### Files Generated

```
results/bandpass_analysis/
└── GW150914_141hz_bandpass_YYYYMMDD_HHMMSS.png
```

### Visualization Contains

1. **Spectrum Panel**: ASD with bandpass filter highlighted
2. **Q-Transform Panel**: Time-frequency energy evolution (Q > 30)
3. **Metrics Panel**: Detection statistics per detector

### Console Output Example

```
🌌 ANÁLISIS DE GW150914 CON FILTRO BANDPASS [140.5-143.0 Hz]
══════════════════════════════════════════════════════════════════════

🔍 Procesando detector: H1
   📡 Descargando datos de H1...
   ✅ Datos descargados: 131072 muestras a 4096.0 Hz
   🔧 Aplicando filtro bandpass [140.5-143.0] Hz...
   ✅ Filtro aplicado exitosamente
   ✂️  Extrayendo ventana de ±0.3s alrededor del merger...
   ✅ Ventana extraída: 2457 muestras (0.600s)
   📊 Calculando Q-transform (Q=30-100, f=140.5-143.0 Hz)...
   ✅ Q-transform calculado
   🎯 Analizando pico de frecuencia en 141.7001 Hz...
   ✅ Frecuencia detectada: 141.7023 Hz (Δf = 0.0022 Hz)
   ✅ SNR: 2.45
   ✅ Dentro del rango esperado: SÍ

📋 RESUMEN DEL ANÁLISIS
══════════════════════════════════════════════════════════════════════

H1: ✅ f = 141.7023 Hz, SNR = 2.45, Δf = 0.0022 Hz
L1: ✅ f = 141.6998 Hz, SNR = 2.31, Δf = 0.0003 Hz

✅ COHERENCIA CONFIRMADA entre detectores
   Frecuencia promedio: 141.7011 ± 0.0018 Hz
   SNR promedio: 2.38
```

## Validation Criteria

### ✅ Valid Detection

- Frequency within ±0.0012 Hz
- SNR > 1.5 (minimum)
- Coherence σ < 0.1 Hz between detectors
- Q-transform peak visible (Q > 30)
- Signal present in ±0.3s window

### ⚠️ Probable Detection

- Frequency within ±0.005 Hz
- SNR > 2.0
- Partial coherence between detectors

### ❌ No Detection

- Frequency outside range
- SNR < 1.5
- No coherence between detectors

## Testing

### Run All Tests

```bash
python3 scripts/test_analisis_141hz_bandpass.py
```

### Expected Output

```
✅ TODOS LOS TESTS PASARON
Ran 25 tests in 0.002s
OK (skipped=3)
```

### Test Coverage

- Bandpass parameters validation (6 tests)
- Event catalog validation (3 tests)
- Frequency analysis (3 tests)
- Coherence analysis (3 tests, requires NumPy)
- Filter validation (1 test)
- Merger window validation (2 tests)
- Q-transform validation (2 tests)
- Known events validation (2 tests)
- Constants validation (2 tests)
- Integration tests (1 test)

## Dependencies

### Required

- Python 3.9+
- NumPy >= 1.21.0
- GWPy >= 3.0.0
- SciPy >= 1.7.0

### Optional

- Matplotlib >= 3.5.0 (for visualization)

### Installation

```bash
pip install gwpy numpy scipy matplotlib
```

## Troubleshooting

### Issue: "GWPy no está instalado"

```bash
pip install gwpy
```

### Issue: "No module named 'numpy'"

```bash
pip install numpy
```

### Issue: "Matplotlib no disponible"

The script will run but won't generate visualizations.

```bash
pip install matplotlib
```

### Issue: "Error descargando datos"

Check internet connectivity and GWOSC availability:
- https://gwosc.org

### Issue: Event not found

Use `--event` with a supported event name:
- GW150914, GW151226, GW170814, etc.

## Performance

- **Download time**: ~2-5 seconds per detector
- **Analysis time**: ~5-10 seconds per detector
- **Total time**: ~30-60 seconds for 2 detectors
- **Memory usage**: ~500 MB per detector

## Integration with CI/CD

The script is designed to work with existing CI/CD workflows:

```yaml
- name: Run bandpass analysis
  run: |
    python3 scripts/analisis_141hz_bandpass.py --event GW150914
  continue-on-error: true

- name: Run bandpass tests
  run: |
    python3 scripts/test_analisis_141hz_bandpass.py
```

## References

- Full documentation: [BANDPASS_FILTER_141HZ.md](BANDPASS_FILTER_141HZ.md)
- Main README: [../README.md](../README.md)
- GWOSC: https://gwosc.org
- GWPy: https://gwpy.github.io

## Contact

- Repository: https://github.com/motanova84/141hz
- Issues: https://github.com/motanova84/141hz/issues
- Author: José Manuel Mota Burruezo (JMMB Ψ✧)

## License

MIT License - See LICENSE file for details.
