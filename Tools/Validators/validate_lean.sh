#!/bin/bash
# Validate Lean 4 formalization

set -e

echo "==================================="
echo "Lean 4 Validation"
echo "==================================="

cd "$(dirname "$0")/../../Core"

echo "Checking if lake is installed..."
if ! command -v lake &> /dev/null; then
    echo "❌ Lake (Lean 4 build tool) not found"
    echo ""
    echo "Please install Lean 4 from:"
    echo "  https://leanprover-community.github.io/get_started.html"
    echo ""
    echo "Quick install (Linux/macOS):"
    echo "  curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh"
    exit 1
fi

echo "✅ Lake found"
echo ""

echo "Building Lean 4 project..."
lake build

echo ""
echo "✅ Lean 4 validation successful!"
echo "   All proofs compile and verify"
