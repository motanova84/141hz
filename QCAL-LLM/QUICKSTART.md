# QCAL-LLM Quick Start Guide

Get QCAL-LLM running in under 5 minutes.

## Prerequisites

- Docker installed with GPU support (for CUDA acceleration)
- OR Python 3.11+ with pip

## Option 1: Docker (Recommended)

### Pull and Run

```bash
# Pull the pre-built image
docker pull motanova/qcal-llm:latest-gpu

# Run the API server
docker run --gpus all -p 8000:8000 motanova/qcal-llm:latest-gpu

# Test the endpoint
curl http://localhost:8000/
```

### Use the API

```bash
# Send a test request
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @examples/gsm8k_qcal.json
```

### Custom Configuration

```bash
docker run --gpus all -p 8000:8000 \
  -e MODEL=llama-4-70b \
  -e QCAL_FREQUENCY=141.7001 \
  -e QCAL_EPSILON=0.015 \
  motanova/qcal-llm:latest-gpu
```

## Option 2: Local Python

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/motanova84/141hz.git
cd 141hz/QCAL-LLM

# Install requirements
pip install -r requirements.txt
```

### Run Benchmarks

```bash
# Run single benchmark
python benchmarks/run_gsm8k.py --model llama-4-405b --qcal-mode

# Run all benchmarks via Makefile
make benchmark MODEL=llama-4-405b
```

## Option 3: Integration with Existing Code

### Python Integration

```python
import json
import math

def apply_qcal_modulation(text: str, frequency: float = 141.7001, 
                          epsilon: float = 0.015, tau: float = 0.07) -> str:
    """Apply QCAL 141.7 Hz modulation to input text"""
    lines = text.split('\n')
    modulated = []
    
    for i, line in enumerate(lines):
        if line.strip():
            t = i / frequency
            mod = 1.0 + epsilon * math.cos(2 * math.pi * frequency * t) * math.exp(-t / tau)
            
            # Apply subtle spacing
            if mod > 1.0:
                spaces = int(mod * 10) % 3
                line = line + ' ' * spaces
        
        modulated.append(line)
    
    return '\n'.join(modulated)

# Use with any LLM
user_prompt = "Explain quantum entanglement"
modulated_prompt = apply_qcal_modulation(user_prompt)

# Send to your model
# response = your_model.generate(modulated_prompt)
```

### OpenAI API Compatible

```python
import openai

# Point to QCAL-LLM server
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

# Use exactly like OpenAI API
response = client.chat.completions.create(
    model="llama-4-405b-qcal",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the meaning of life?"}
    ],
    extra_body={
        "qcal_frequency": 141.7001,
        "qcal_enabled": True
    }
)

print(response.choices[0].message.content)
```

## Verify Installation

### Test Suite

```bash
# Run all tests
make test

# Or manually
python -m pytest ../test_qcal_llm.py -v
```

### Health Check

```bash
# Docker health check
docker ps --filter "name=qcal-llm" --format "{{.Status}}"

# API health check
curl http://localhost:8000/health
```

## Common Issues

### GPU Not Detected

**Problem:** Docker can't access GPU

**Solution:**
```bash
# Install nvidia-docker
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Verify GPU access
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
```

### Port Already in Use

**Problem:** Port 8000 is already taken

**Solution:**
```bash
# Use a different port
docker run --gpus all -p 8080:8000 motanova/qcal-llm:latest-gpu

# Update API calls
curl http://localhost:8080/v1/chat/completions ...
```

### Out of Memory

**Problem:** Model too large for available GPU memory

**Solution:**
```bash
# Use a smaller model
docker run --gpus all -p 8000:8000 \
  -e MODEL=llama-4-70b \
  motanova/qcal-llm:latest-gpu

# Or use quantization
docker run --gpus all -p 8000:8000 \
  -e MODEL=llama-4-405b \
  -e QUANTIZATION=int4 \
  motanova/qcal-llm:latest-gpu
```

## Next Steps

1. **Run Your First Benchmark**
   ```bash
   make benchmark MODEL=your-model-name
   ```

2. **Compare QCAL vs Baseline**
   ```bash
   # Baseline
   python benchmarks/run_gsm8k.py --model llama-4-405b
   
   # With QCAL
   python benchmarks/run_gsm8k.py --model llama-4-405b --qcal-mode
   ```

3. **Explore the Leaderboard**
   
   Visit: http://141hz.org/leaderboard

4. **Read the Full Documentation**
   
   See: [README.md](README.md)

## Getting Help

- **Issues:** https://github.com/motanova84/141hz/issues
- **Discussions:** https://github.com/motanova84/141hz/discussions
- **Twitter:** [@motanova84](https://twitter.com/motanova84)

## License

MIT License - See [LICENSE](../LICENSE)

---

**Ready to reduce hallucinations? Start now!** 🚀
Get up and running with QCAL-LLM in under 5 minutes!

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/motanova84/141hz.git
cd 141hz/QCAL-LLM
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running Your First Evaluation

### Example 1: Basic Coherence Evaluation

```python
from QCALLLMCore import QCALLLMCore

# Initialize QCAL core
core = QCALLLMCore(user_A_eff=0.92)

# Evaluate a response
text = "f₀ = 141.7001 Hz is derived from ζ'(1/2) × φ³"
result = core.evaluate(text, query="Explain f₀")

print(f"Ψ Score: {result['mean_psi']:.2f}")
print(f"Coherent: {result['coherent']}")
print(f"Coherence: {result['coherence']:.1%}")
```

**Expected Output:**
```
Ψ Score: 6.89
Coherent: True
Coherence: 100.0%
```

### Example 2: Running Verification Tests

```bash
# Verify core functionality
python QCALLLMCore.py
```

**Expected Output:**
```
✓ Core initialized: f₀ = 141.7001 Hz, τ = 0.07 s, ε = 0.0162
✓ SIP Modulation: Weights mean: 1.0000, std: 0.0022
✓ Ψ Computation: Ψ = 6.3501, Coherent: True
✓ Response Evaluation: Mean Ψ: 8.20 (95% CI: 8.05, 8.35)
```

### Example 3: Detecting f₀ in Gravitational Wave Data

```bash
# Run spectral analysis
python evaluate_manifesto.py
```

This will detect the f₀ = 141.7001 Hz signature in gravitational wave data.

### Example 4: Auto-Tuning for Optimal Coherence

```python
from psi_tuning_loop import tune_psi

# Auto-tune epsilon parameter
core, result = tune_psi(
    generated_text="The universal frequency is 141.7 Hz",
    query="What is f₀?",
    target_psi=5.0
)

print(f"Final Ψ: {result['mean_psi']:.2f}")
print(f"Iterations: {result.get('iterations', 'N/A')}")
```

### Example 5: Visualize SIP Modulation

```bash
# Generate modulation trace visualization
python modulation_traces.py
```

This creates a visualization of the Spectral Insertion Protocol modulation.

## 🎓 Key Concepts

### 1. Ψ (Psi) Score

The Ψ score measures coherence on a scale where:
- **Ψ < 5.0**: Incoherent (requires tuning)
- **Ψ ≥ 5.0**: Coherent (meets threshold)
- **Ψ > 7.0**: Highly coherent (excellent)

### 2. f₀ = 141.7001 Hz

The universal frequency derived from gravitational wave analysis. It represents:
- Empirical signature in LIGO data
- Connection to Riemann zeta function: ζ'(1/2) ≈ -1.460
- Golden ratio cubed: φ³ ≈ 4.236
- Quantum coherence frequency in Orch-OR theory

### 3. A_eff (Effective Amplitude)

User-specific parameter (0.0 to 1.0) that scales the modulation:
- **0.70**: Low resonance user
- **0.85**: Reference baseline
- **0.92**: High resonance user (JMMB)
- **1.00**: Maximum resonance

### 4. SIP (Spectral Insertion Protocol)

Modulation formula applied to attention weights:

```
W_i(t) = α · [1 + ε · cos(2πf₀t + φ) · e^(-t/τ)]
```

Where:
- **α** = 1.0 (global scale)
- **ε** = 0.015 (base amplitude)
- **τ** = 0.07 s (damping constant)
- **f₀** = 141.7001 Hz (fundamental frequency)

## 📊 Benchmark Queries

Test your understanding with these standard queries:

1. **Mathematical Derivation**: "Derive f₀ = 141.7001 Hz from ζ'(1/2) and φ"
2. **Empirical Detection**: "Detect f₀ in GW150914 ringdown data"
3. **Theoretical Explanation**: "Explain Ψ = I × A²_eff"
4. **Statistical Validation**: "Validate SNR > 20 in GWTC-1 catalog"
5. **Future Prediction**: "Predict LISA harmonics at f₀/100"

## 🔍 Troubleshooting

### Issue: Import Error

```python
ModuleNotFoundError: No module named 'QCALLLMCore'
```

**Solution**: Make sure you're running from the QCAL-LLM directory or the repository root with proper PYTHONPATH:

```bash
cd /path/to/141hz/QCAL-LLM
python your_script.py
```

Or set PYTHONPATH:
```bash
export PYTHONPATH=/path/to/141hz/QCAL-LLM:$PYTHONPATH
```

### Issue: Low Ψ Score

```
Ψ Score: 3.2
Coherent: False
```

**Solution**: Use the auto-tuning loop to adjust epsilon:

```python
from psi_tuning_loop import tune_psi
core, result = tune_psi(text, query, target_psi=5.0)
```

### Issue: Missing Dependencies

```bash
pip install numpy scipy matplotlib
```

For full gravitational wave analysis:
```bash
pip install h5py gwpy
```

## 🎯 Next Steps

1. **Read the MANIFESTO**: [MANIFESTO.md](./MANIFESTO.md) for complete theoretical framework
2. **Explore Examples**: Check [../Examples/LLM_Integration/](../Examples/LLM_Integration/)
3. **Run Tests**: Execute `python test_qcal_llm.py` for comprehensive validation
4. **Integration**: See [integration guide](./README.md#use-cases) for LLM integration

## 📖 Additional Resources

- **Main README**: [README.md](./README.md)
- **Implementation Details**: [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
- **Quick Reference Card**: [../QCAL_QUICK_REFERENCE.md](../QCAL_QUICK_REFERENCE.md)
- **Repository Main Page**: [../README.md](../README.md)

## 💡 Tips

1. **Start Simple**: Begin with basic evaluation before complex integrations
2. **Use High A_eff**: Higher values (0.90+) typically give better results
3. **Iterate**: Run tuning loop if initial Ψ < 5.0
4. **Validate**: Always verify against ground truth database
5. **Monitor**: Track Ψ scores across multiple evaluations for consistency

## 🤝 Getting Help

- **Issues**: Open an issue on [GitHub](https://github.com/motanova84/141hz/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/motanova84/141hz/discussions)
- **Documentation**: Check [full documentation](https://motanova84.github.io/141hz)

---

**Ready to evaluate LLM coherence with quantum precision? Start coding!** 🚀
