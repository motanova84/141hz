#!/bin/bash
# run_tests.sh — Ejecuta los tests de la cuadratura del círculo QCAL
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "════════════════════════════════════════════"
echo "  CUADRATURA DEL CÍRCULO QCAL — TEST SUITE"
echo "════════════════════════════════════════════"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "❌ python3 no encontrado"
    exit 1
fi

echo "🔬 Ejecutando tests de verificación..."
echo ""
python3 test_quadrature.py
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ TODOS LOS TESTS PASARON"
else
    echo "❌ ALGUNOS TESTS FALLARON (código: $EXIT_CODE)"
fi

exit $EXIT_CODE
