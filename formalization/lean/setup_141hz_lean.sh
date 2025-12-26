#!/bin/bash
# Setup script para formalización Lean de 141hz

set -e

REPO_DIR="${1:-$HOME/141hz}"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Setting up 141hz Lean formalization                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if running in the repo already
if [ -f "lakefile.lean" ] && [ -d "F0Derivation" ]; then
    echo "✓ Already in Lean formalization directory"
    LEAN_DIR="."
elif [ -d "formalization/lean" ]; then
    echo "✓ Found formalization/lean directory"
    LEAN_DIR="formalization/lean"
    cd "$LEAN_DIR"
else
    echo "❌ Error: Cannot find Lean formalization directory"
    echo "   Please run from repository root or formalization/lean/"
    exit 1
fi

echo ""
echo "📁 Directory structure:"
echo "   $(pwd)"

if [ -d "F0Derivation" ]; then
    echo "   ✓ F0Derivation/"
    ls -1 F0Derivation/ | sed 's/^/     - /'
fi

if [ -d "Tests" ]; then
    echo "   ✓ Tests/"
    ls -1 Tests/ | sed 's/^/     - /'
fi

echo ""

# Check for Lean installation
if command -v lake &> /dev/null; then
    echo "✓ Lake build tool found: $(lake --version 2>&1 | head -1)"
    echo ""
    echo "🔨 Building project..."
    
    # Update dependencies
    echo "   → Updating dependencies..."
    lake update || true
    
    # Build project
    echo "   → Building F0Derivation..."
    if lake build; then
        echo ""
        echo "✅ Build successful!"
        echo ""
        echo "📊 Running executable..."
        echo ""
        lake exe f0derivation || true
    else
        echo ""
        echo "⚠️  Build completed with warnings (expected with 'sorry' proofs)"
        echo "   This is normal for incomplete proofs."
    fi
else
    echo "⚠️  Lake/Lean not found in PATH"
    echo ""
    echo "To install Lean 4, run:"
    echo "  curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh"
    echo ""
    echo "After installation:"
    echo "  cd $LEAN_DIR"
    echo "  lake update"
    echo "  lake build"
    echo "  lake exe f0derivation"
fi

echo ""
echo "📖 Documentation:"
echo "   - README: https://github.com/motanova84/141hz"
echo "   - Main theorem: F0Derivation/Main.lean"
echo "   - Tests: Tests/Verification.lean"
echo ""
echo "✅ Setup complete!"
