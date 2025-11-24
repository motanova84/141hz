# QCAL Llama 4 Adapter

🌐 QCAL · Llama4 conectado ∞³

## Overview

The QCAL Llama 4 Adapter provides a simple, interactive CLI interface for conversing with Llama 4 models within the QCAL ecosystem. It's designed for symbiotic conversation and exploration of QCAL concepts.

## Features

- **Simple CLI Interface**: Interactive prompt-response loop
- **FP16 Precision**: Memory-efficient model loading with `torch.float16`
- **Auto Device Mapping**: Automatically distributes model across available devices
- **Configurable Generation**: 300 tokens by default for coherent responses
- **Symbolic Activation**: Clear visual indicators for QCAL connection

## Installation

### Prerequisites

```bash
# Ensure you have Python 3.11+ and required dependencies
pip install torch>=2.6.0
pip install transformers>=4.48.0
```

### Model Setup

The adapter expects the Llama 4 model to be available at `./models/llama4` by default. You can:

1. **Download the model**:
   ```bash
   # Set your HuggingFace token
   export HF_TOKEN=your_token_here
   
   # Download using huggingface-cli or Python
   python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8', cache_dir='./models/llama4')"
   ```

2. **Or specify a custom path** when initializing the adapter (see Usage section)

## Usage

### Basic Interactive Mode

```bash
python qcal_llama4_adapter.py
```

This will start an interactive session:

```
🌐 QCAL · Llama4 conectado ∞³
🧬> What is the fundamental frequency f₀?
🌀 The fundamental frequency f₀ = 141.7001 Hz emerges from...
🧬> Explain the QCAL equation
🌀 The QCAL equation Ψ = I × A²_eff × f₀ × χ(LLaMA)...
```

### Programmatic Usage

```python
from qcal_llama4_adapter import QCAL_Llama4

# Initialize with default path
engine = QCAL_Llama4()

# Or specify custom path and max tokens
engine = QCAL_Llama4(
    model_path="/path/to/your/model",
    max_tokens=500
)

# Evaluate a prompt
response = engine.evaluate("Explain quantum coherence at 141.7 Hz")
print(response)
```

### Custom Configuration

```python
from qcal_llama4_adapter import QCAL_Llama4

# Initialize with custom settings
engine = QCAL_Llama4(
    model_path="./my_models/llama4",  # Custom model path
    max_tokens=200                     # Shorter responses
)

# Use in your application
prompts = [
    "Derive f₀ from ζ'(1/2) and φ³",
    "Explain the Noetic Quantum Field",
    "What is the significance of 141.7001 Hz?"
]

for prompt in prompts:
    print(f"Q: {prompt}")
    print(f"A: {engine.evaluate(prompt)}\n")
```

## API Reference

### QCAL_Llama4 Class

#### `__init__(model_path="./models/llama4", max_tokens=300)`

Initialize the QCAL Llama 4 Adapter.

**Parameters:**
- `model_path` (str): Path to the Llama 4 model directory. Default: `"./models/llama4"`
- `max_tokens` (int): Maximum number of new tokens to generate. Default: `300`

**Example:**
```python
engine = QCAL_Llama4(
    model_path="./custom/path",
    max_tokens=500
)
```

#### `evaluate(prompt: str) -> str`

Evaluate a prompt and generate a response.

**Parameters:**
- `prompt` (str): Input text to evaluate

**Returns:**
- `str`: Generated response from the model

**Example:**
```python
response = engine.evaluate("What is the QCAL equation?")
print(response)
```

## Architecture

The adapter uses the following components:

1. **AutoTokenizer**: Handles text tokenization for the Llama 4 model
2. **AutoModelForCausalLM**: Loads the causal language model
3. **torch.float16**: Uses half-precision for memory efficiency
4. **device_map="auto"**: Automatically distributes model across CPU/GPU

### Memory Requirements

- **Model Size**: ~17B parameters (Llama-4-Maverick-17B-128E-Instruct-FP8)
- **Memory**: ~34GB in FP16 (with auto device mapping)
- **Recommended**: GPU with 40GB+ VRAM, or distributed across multiple devices

### Performance

- **Latency**: 100-500ms per generation (hardware dependent)
- **Throughput**: Depends on max_tokens and hardware
- **Optimization**: Consider batching for multiple prompts

## Integration with QCAL Ecosystem

The adapter is designed to work seamlessly with other QCAL components:

- **QCALLLMCore**: Use for coherence evaluation
- **llama4_coherence.py**: For detailed coherence scoring
- **example_llama4_integration.py**: For comprehensive demonstrations

### Example Integration

```python
from qcal_llama4_adapter import QCAL_Llama4
from QCALLLMCore import QCALLLMCore

# Initialize both systems
adapter = QCAL_Llama4()
core = QCALLLMCore(use_llama4=True)

# Generate response
prompt = "Explain the fundamental frequency"
response = adapter.evaluate(prompt)

# Evaluate coherence
coherence = core.compute_coherence(response)
print(f"Response coherence: {coherence:.3f}")
```

## Troubleshooting

### Model Not Found

```
Error: Model not found at ./models/llama4
```

**Solution**: Download the model first or specify the correct path:
```python
engine = QCAL_Llama4(model_path="/path/to/your/model")
```

### Out of Memory

```
Error: CUDA out of memory
```

**Solutions**:
1. Use a smaller model
2. Enable CPU offloading with `device_map="auto"`
3. Reduce `max_tokens`
4. Use a machine with more GPU memory

### Import Error

```
ImportError: No module named 'transformers'
```

**Solution**: Install required dependencies:
```bash
pip install transformers>=4.48.0 torch>=2.6.0
```

## Testing

Run the test suite to verify the adapter:

```bash
python test_qcal_llama4_adapter.py
```

The tests cover:
- Module import validation
- Class structure verification
- Initialization with various parameters
- Method signatures
- Model loading parameters

## Contributing

Contributions are welcome! Please ensure:

1. Code follows the existing style
2. Tests pass: `python test_qcal_llama4_adapter.py`
3. Documentation is updated
4. Changes are minimal and focused

## License

This project is part of the 141hz research ecosystem. See LICENSE file for details.

## Citation

If you use this adapter in your research, please cite:

```bibtex
@software{qcal_llama4_adapter,
  author = {Mota Burruezo, José Manuel},
  title = {QCAL Llama 4 Adapter},
  year = {2025},
  url = {https://github.com/motanova84/141hz},
  doi = {10.5281/zenodo.17445017}
}
```

## Acknowledgments

- **Framework**: QCAL-LLM by José Manuel Mota Burruezo (JMMB Ψ✧)
- **Model**: Llama 4 Maverick by Meta/Hugging Face
- **Infrastructure**: Transformers library by Hugging Face

## Support

- **Documentation**: See main README.md
- **Examples**: See example_llama4_integration.py
- **Issues**: GitHub Issues
- **Citation**: DOI 10.5281/zenodo.17445017

---

🌐 QCAL · Llama4 conectado ∞³
