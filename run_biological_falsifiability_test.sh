#!/bin/bash
# Ejecuta el test de falsabilidad biológica QCAL
# Usage: ./run_biological_falsifiability_test.sh

set -e

echo "=========================================="
echo "QCAL Biological Falsifiability Test"
echo "=========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Check for required packages
echo "🔍 Verificando dependencias..."
python3 -c "import numpy, scipy, matplotlib" 2>/dev/null || {
    echo "📦 Instalando dependencias necesarias..."
    pip install numpy scipy matplotlib -q
}

# Run tests
echo ""
echo "🧪 Ejecutando tests unitarios..."
python3 -m pytest tests/test_falsabilidad_biologica.py -v --tb=short

# Run experiment
echo ""
echo "🔬 Ejecutando experimento de falsabilidad..."
python3 scripts/test_falsabilidad_biologica.py

# Display results
echo ""
echo "=========================================="
echo "✅ Ejecución completada"
echo "=========================================="
echo ""
echo "Resultados guardados en:"
echo "  - results/falsabilidad_biologica_qcal.json"
echo "  - results/falsabilidad_biologica_qcal.png"
echo "  - results/falsabilidad_biologica_traditional.json"
echo "  - results/falsabilidad_biologica_traditional.png"
echo ""

# Show summary
if [ -f results/falsabilidad_biologica_qcal.json ]; then
    echo "📊 Resumen QCAL:"
    python3 -c "
import json
with open('results/falsabilidad_biologica_qcal.json') as f:
    data = json.load(f)
    ratio = data['ratio_test']['ratio']
    threshold = data['ratio_test']['qcal_threshold']
    supported = data['ratio_test']['qcal_supported']
    
    print(f'  Ratio: {ratio:.3f}')
    print(f'  Umbral: {threshold}')
    print(f'  QCAL soportado: {\"✅ Sí\" if supported else \"❌ No\"}')
    print(f'  Veredicto: {data[\"verdict\"]}')
"
fi

echo ""
echo "Ver documentación completa en:"
echo "  FALSABILIDAD_BIOLOGICA_README.md"
echo ""
