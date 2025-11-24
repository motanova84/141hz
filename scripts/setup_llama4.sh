#!/bin/bash
# QCAL-LLM Setup script for LLaMA 4 Maverick
# Prepares the environment for LLaMA 4 (17B Instruct / FP8) evaluation

set -e  # Exit on error

echo "🔧 QCAL-LLM Setup for LLaMA 4 Maverick"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f ".qcal_beacon" ]; then
    echo "❌ Error: .qcal_beacon not found. Please run from repository root."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p models/llama4/weights
mkdir -p data
mkdir -p results
mkdir -p qcal

echo "✅ Directories created"
echo ""

# Check for signed URL
if [ -z "$LLAMA4_DOWNLOAD_URL" ]; then
    echo "⚠️  Warning: LLAMA4_DOWNLOAD_URL environment variable not set."
    echo ""
    echo "To download LLaMA 4 Maverick (17B Instruct / FP8), you need:"
    echo "1. Request access at https://llama.meta.com/"
    echo "2. Get a signed download URL (valid for 48h)"
    echo "3. Set environment variable:"
    echo "   export LLAMA4_DOWNLOAD_URL='https://llama4.llamameta.net/...'"
    echo ""
    echo "For now, we'll prepare the environment without downloading the model."
    echo "You can manually place model files in: models/llama4/weights/"
    echo ""
else
    echo "🔽 Downloading LLaMA 4 model..."
    echo "This may take a while (model is ~34GB compressed)..."
    
    # Download with progress bar
    curl -L "$LLAMA4_DOWNLOAD_URL" \
         -o models/llama4/weights/model.tar.gz \
         --progress-bar
    
    echo ""
    echo "📦 Extracting model..."
    tar -xzvf models/llama4/weights/model.tar.gz -C models/llama4/weights/
    
    echo "🧹 Cleaning up..."
    rm models/llama4/weights/model.tar.gz
    
    echo "✅ Model downloaded and extracted"
fi

# Check Python version
echo ""
echo "🐍 Checking Python environment..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if Python >= 3.11
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo "❌ Error: Python 3.11+ required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python version compatible"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

# Check if in virtual environment (recommended)
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "Recommended: python3 -m venv venv && source venv/bin/activate"
    echo ""
    read -p "Continue with system-wide install? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

pip install -q --upgrade pip
pip install -q -r requirements.txt

# Verify key packages
echo ""
echo "✅ Verifying installation..."
python3 -c "import torch; print(f'PyTorch {torch.__version__} installed')" || {
    echo "❌ PyTorch not found"
    exit 1
}

python3 -c "import transformers; print(f'Transformers {transformers.__version__} installed')" || {
    echo "❌ Transformers not found"
    exit 1
}

echo ""

# Check GPU availability
echo "🎮 Checking GPU availability..."
python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}') if torch.cuda.is_available() else None"

echo ""

# Create sample prompts if not exists
if [ ! -f "data/prompts_qcal.json" ]; then
    echo "📝 Creating sample prompts..."
    cat > data/prompts_qcal.json << 'EOF'
[
  {
    "label": "f0_derivation",
    "text": "Deriva la frecuencia fundamental f₀ = 141.7001 Hz desde los principios matemáticos fundamentales ζ'(1/2) y φ³."
  },
  {
    "label": "gw150914_detection",
    "text": "Explica la detección de f₀ en el ringdown de GW150914 con SNR > 20."
  },
  {
    "label": "psi_metric",
    "text": "Define la métrica de coherencia Ψ = I × A_eff² y explica sus componentes."
  },
  {
    "label": "lisa_prediction",
    "text": "Predice los armónicos observables de f₀ en LISA (frecuencias bajas ~1.4 Hz)."
  },
  {
    "label": "quantum_coherence",
    "text": "Relaciona la coherencia cuántica con la frecuencia f₀ en el contexto de ondas gravitacionales."
  }
]
EOF
    echo "✅ Sample prompts created"
fi

echo ""
echo "=========================================="
echo "✅ Setup completo!"
echo ""
echo "Estructura de directorios:"
echo "  models/llama4/weights/  - Modelo LLaMA 4"
echo "  data/                   - Prompts de prueba"
echo "  qcal/                   - Módulo de coherencia"
echo "  scripts/                - Scripts de evaluación"
echo "  results/                - Resultados de evaluación"
echo ""
echo "Siguientes pasos:"
echo "1. Verificar modelo: ls -lh models/llama4/weights/"
echo "2. Ejecutar evaluación: python3 scripts/qcal_llm_eval.py"
echo "3. Ver notebook: jupyter notebook notebooks/benchmark_llama4.ipynb"
echo ""
echo "∴ — QCAL Ψ∞³ activo"
echo "=========================================="
