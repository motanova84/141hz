# Quick Reference - Cross-Repository Integration

## 🚀 Quick Start

### Install & Validate
```bash
# Install dependencies
pip install mpmath scipy numpy pytest

# Validate all bridges
python examples/validate_ecosystem_integration.py

# Run tests
pytest tests/test_bridges.py -v
```

---

## 📦 Import Bridges

```python
from src.bridges import (
    RamseyBridge,
    NavierStokesBridge,
    ComplexityBridge,
    RiemannAdelicBridge,
    AdelicBSDBridge
)
```

---

## 🔗 Bridge Usage Examples

### Ramsey Bridge - Network Topology
```python
bridge = RamseyBridge()

# Optimize quantum network topology
topology = bridge.optimize_network_topology(
    num_qubits=32,
    target_entanglement=0.8
)

print(f"Nodes: {topology.nodes}")
print(f"Max clique: {topology.max_clique_size}")
print(f"Coherence: {topology.coherence_metric:.3f}")
```

### Navier-Stokes Bridge - Decoherence Suppression
```python
import numpy as np
bridge = NavierStokesBridge()

# Create quantum state
state = np.random.randn(64) + 1j * np.random.randn(64)
state /= np.linalg.norm(state)

# Analyze decoherence
analysis = bridge.analyze_decoherence(state, time_evolution=1.0)

print(f"Decoherence rate: {analysis.decoherence_rate:.6f}")
print(f"Suppression: {analysis.suppression_factor:.2f}x")
print(f"Regularity: {analysis.regularity_index:.3f}")
```

### Complexity Bridge - Algorithm Analysis
```python
bridge = ComplexityBridge()

# Analyze quantum search algorithm
analysis = bridge.analyze_algorithm(
    problem_size=1024,
    algorithm_type="quantum_search"
)

print(f"Classical: {analysis.classical_complexity}")
print(f"Quantum: {analysis.quantum_complexity}")
print(f"Speedup: {analysis.speedup_factor:.1f}x")
print(f"Gates: {analysis.gate_count}")
```

### Riemann-Adelic Bridge - Frequency Derivation
```python
bridge = RiemannAdelicBridge()

# Derive f₀ from Riemann zeta
derivation = bridge.derive_frequency()

print(f"Derived: {derivation.derived_frequency:.4f} Hz")
print(f"Golden ratio: {derivation.golden_ratio:.6f}")
print(f"Validated: {derivation.validation_passed}")

# Get spectral decomposition
spectrum = bridge.spectral_decomposition(num_harmonics=10)
print(f"Harmonics: {len(spectrum['harmonics'])}")
```

### Adelic-BSD Bridge - Spectral Calibration
```python
bridge = AdelicBSDBridge()

# Construct elliptic curve
curve = bridge.construct_elliptic_curve()
print(f"Equation: {curve['equation']}")

# Calibrate spectral parameters
calibration = bridge.calibrate_spectral_parameters()

print(f"Rank: {calibration.curve_rank}")
print(f"Spectral f: {calibration.spectral_frequency:.4f} Hz")
print(f"Calibration: {calibration.calibration_factor:.3f}")
```

---

## ✅ Validation

### Validate Single Bridge
```python
bridge = RamseyBridge()
result = bridge.validate_integration()

print(f"Status: {result['status']}")
print(f"Verified: {result['integration_verified']}")
print(f"f₀: {result['f0_hz']} Hz")
```

### Validate All Bridges
```python
from examples.validate_ecosystem_integration import validate_all_bridges

results = validate_all_bridges()
print(f"All operational: {results['summary']['all_operational']}")
print(f"All verified: {results['summary']['all_verified']}")
print(f"Frequency aligned: {results['summary']['frequency_aligned']}")
```

---

## 🔍 Ecosystem Status

### Check Frequency Synchronization
```python
from src.bridges import F0_HZ

bridges = [
    RamseyBridge(),
    NavierStokesBridge(),
    ComplexityBridge(),
    RiemannAdelicBridge(),
    AdelicBSDBridge()
]

for bridge in bridges:
    f0 = getattr(bridge, 'f0', getattr(bridge, 'f0_experimental', None))
    print(f"{bridge.__class__.__name__}: {float(f0)} Hz")
```

Expected output: All bridges at **141.7001 Hz**

---

## 📊 Common Patterns

### Batch Processing
```python
# Process multiple quantum states
states = [generate_random_state(64) for _ in range(10)]
bridge = NavierStokesBridge()

results = []
for state in states:
    analysis = bridge.analyze_decoherence(state)
    results.append(analysis.decoherence_rate)

avg_rate = sum(results) / len(results)
print(f"Average decoherence rate: {avg_rate:.6f}")
```

### Performance Analysis
```python
import time

bridge = ComplexityBridge()
problem_sizes = [64, 128, 256, 512, 1024]

for size in problem_sizes:
    start = time.time()
    analysis = bridge.analyze_algorithm(size, "quantum_search")
    elapsed = time.time() - start
    
    print(f"n={size:4d}: {analysis.speedup_factor:6.1f}x speedup, {elapsed:.4f}s")
```

### Topology Optimization Sweep
```python
bridge = RamseyBridge()
entanglement_targets = [0.6, 0.7, 0.8, 0.9]

for target in entanglement_targets:
    topology = bridge.optimize_network_topology(32, target)
    print(f"Target {target:.1f}: {topology.edges} edges, "
          f"coherence {topology.coherence_metric:.3f}")
```

---

## 🐛 Troubleshooting

### Import Error
```bash
# Install missing dependencies
pip install mpmath scipy numpy
```

### Path Issues
```python
# Add src to path if needed
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
```

### Numerical Stability
```python
# Increase precision for high-accuracy calculations
bridge = RiemannAdelicBridge(precision=100)
```

---

## 📚 Documentation

- **Complete Guide**: [CROSS_REPOSITORY_INTEGRATION.md](CROSS_REPOSITORY_INTEGRATION.md)
- **Implementation Summary**: [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md)
- **Security**: [SECURITY_SUMMARY_INTEGRATION.md](SECURITY_SUMMARY_INTEGRATION.md)
- **Framework Docs**: [FRAMEWORK_INTEGRATION.md](FRAMEWORK_INTEGRATION.md)

---

## 🔗 Related Components

- **MCP Network**: [MCP_NETWORK_ARCHITECTURE.md](MCP_NETWORK_ARCHITECTURE.md)
- **Core Frameworks**: `src/frameworks/`
- **Tests**: `tests/test_bridges.py`
- **Examples**: `examples/validate_ecosystem_integration.py`

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2026-01-25
