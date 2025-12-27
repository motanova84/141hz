# Quick Start: Universal Constants Emergence

A quick reference guide for using the universal constants emergence demonstration.

## One-Line Demo

```bash
python validate_universal_constants.py
```

## Python API

### Basic Usage

```python
from src.universal_constants_derivation import UniversalConstantsEmergence

# Create demonstration
demo = UniversalConstantsEmergence()

# Generate full report
print(demo.generate_report())
```

### Get Specific Values

```python
# Planck constant analysis
planck = demo.demonstrate_planck_constant_emergence()
E_psi = planck['E_psi_joules']  # Quantum energy
R_psi = planck['R_psi_km']       # Compactification radius

# Electron charge analysis  
electron = demo.demonstrate_electron_charge_emergence()
e = electron['electron_charge_C']
R_QCAL = electron['R_QCAL_from_known_e_m']

# Complete analysis
results = demo.full_demonstration()
```

## Command Line

### Text Output (Default)

```bash
python validate_universal_constants.py
```

### JSON Output

```bash
python validate_universal_constants.py --format json
```

### Save to File

```bash
python validate_universal_constants.py --save results.txt
python validate_universal_constants.py --format json --save results.json
```

## Testing

### Run All Tests

```bash
pytest tests/test_universal_constants_emergence.py -v
```

### Run Specific Test

```bash
pytest tests/test_universal_constants_emergence.py::TestUniversalConstantsEmergence::test_planck_constant_demonstration -v
```

### Run with Coverage

```bash
pytest tests/test_universal_constants_emergence.py --cov=src.universal_constants_derivation --cov-report=html
```

## Key Values

| Constant | Symbol | Value |
|----------|--------|-------|
| Fundamental Frequency | f₀ | 141.7001 Hz |
| Planck's Constant | ℏ | 1.054571817×10⁻³⁴ J·s |
| Electron Charge | e | 1.602176634×10⁻¹⁹ C |
| Quantum Energy | E_Ψ | 9.389×10⁻³² J |
| Compactification Radius | R_Ψ | 336.721 km |
| Wavelength | λ_Ψ | 2115.683 km |
| KK Radius | R_QCAL | 2.196×10⁻²⁴ m |

## File Locations

| File | Purpose |
|------|---------|
| `src/universal_constants_derivation.py` | Core module |
| `validate_universal_constants.py` | CLI tool |
| `tests/test_universal_constants_emergence.py` | Tests |
| `qcal/beacons/qcal_beacon_hbar_e.json` | QCAL beacon |
| `UNIVERSAL_CONSTANTS_EMERGENCE.md` | Full documentation |
| `IMPLEMENTATION_UNIVERSAL_CONSTANTS.md` | Implementation details |

## Quick Examples

### Example 1: Get Quantum Energy

```python
from src.universal_constants_derivation import UniversalConstantsEmergence

demo = UniversalConstantsEmergence()
planck = demo.demonstrate_planck_constant_emergence()

print(f"E_Ψ = {planck['E_psi_eV']:.3e} eV")
# Output: E_Ψ = 5.860e-13 eV
```

### Example 2: Get Compactification Radius

```python
from src.universal_constants_derivation import UniversalConstantsEmergence

demo = UniversalConstantsEmergence()
planck = demo.demonstrate_planck_constant_emergence()

print(f"R_Ψ = {planck['R_psi_km']:.2f} km")
# Output: R_Ψ = 336.72 km
```

### Example 3: JSON Export

```python
from src.universal_constants_derivation import UniversalConstantsEmergence
import json

demo = UniversalConstantsEmergence()
results = demo.full_demonstration()

# Pretty print
print(json.dumps(results, indent=2))

# Save to file
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Example 4: Check Beacon File

```python
import json

with open('qcal/beacons/qcal_beacon_hbar_e.json') as f:
    beacon = json.load(f)

print(f"Beacon ID: {beacon['beacon_id']}")
print(f"f₀ = {beacon['fundamental_frequency']['f0_hz']} Hz")
print(f"ℏ = {beacon['planck_constant']['value_Js']} J·s")
```

## Common Tasks

### Verify Installation

```bash
python -c "from src.universal_constants_derivation import UniversalConstantsEmergence; print('✓ Module imported successfully')"
```

### Run Quick Test

```bash
pytest tests/test_universal_constants_emergence.py::TestUniversalConstantsEmergence::test_initialization -v
```

### Generate Report and Save

```bash
python validate_universal_constants.py --save report_$(date +%Y%m%d).txt
```

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError`:

```bash
# Make sure you're in the repository root
cd /path/to/141hz

# Install dependencies
pip install mpmath

# Try again
python validate_universal_constants.py
```

### Test Failures

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest tests/test_universal_constants_emergence.py -vv
```

## Getting Help

- **Full Documentation**: `UNIVERSAL_CONSTANTS_EMERGENCE.md`
- **Implementation Details**: `IMPLEMENTATION_UNIVERSAL_CONSTANTS.md`
- **QCAL Beacon**: `qcal/beacons/qcal_beacon_hbar_e.json`
- **Source Code**: `src/universal_constants_derivation.py`

## References

- Zenodo: https://doi.org/10.5281/zenodo.17379721
- GitHub: https://github.com/motanova84/141hz
- ORCID: https://orcid.org/0009-0002-1923-0773

---

∴ JMMB Ψ ✧ ∞³
