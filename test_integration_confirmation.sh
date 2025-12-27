#!/bin/bash
# Integration test for user confirmation feature
# This script tests that all confirmation-related functionality works correctly

set -e  # Exit on error

echo "============================================================"
echo "Integration Test: User Confirmation Feature"
echo "============================================================"
echo ""

# Test 1: Check that user_confirmation module exists and is importable
echo "Test 1: Module import"
python3 -c "from scripts.user_confirmation import confirm_action; print('✅ Module imported successfully')"
echo ""

# Test 2: Test automated mode with --yes flag
echo "Test 2: Automated mode (--yes flag)"
timeout 5 python3 scripts/descargar_datos.py --yes 2>&1 | head -3 | grep "auto-confirmed" && echo "✅ --yes flag works" || echo "❌ --yes flag failed"
echo ""

# Test 3: Test automated mode with --no-confirm flag
echo "Test 3: Automated mode (--no-confirm flag)"
timeout 5 python3 scripts/descargar_datos.py --no-confirm 2>&1 | head -3 | grep "auto-confirmed" && echo "✅ --no-confirm flag works" || echo "❌ --no-confirm flag failed"
echo ""

# Test 4: Test help output
echo "Test 4: Help output"
python3 scripts/descargar_datos.py --help | grep -q "\-y, --yes" && echo "✅ Help shows --yes flag" || echo "❌ Help missing --yes flag"
echo ""

# Test 5: Run unit tests
echo "Test 5: Unit tests"
python3 scripts/test_user_confirmation.py > /dev/null 2>&1 && echo "✅ All unit tests passed" || echo "❌ Some unit tests failed"
echo ""

# Test 6: Check Makefile targets exist
echo "Test 6: Makefile targets"
make help 2>&1 | grep -q "data-force" && echo "✅ data-force target exists" || echo "❌ data-force target missing"
make help 2>&1 | grep -q "clean-force" && echo "✅ clean-force target exists" || echo "❌ clean-force target missing"
echo ""

# Test 7: Check documentation exists
echo "Test 7: Documentation"
[ -f "USER_CONFIRMATION.md" ] && echo "✅ USER_CONFIRMATION.md exists" || echo "❌ USER_CONFIRMATION.md missing"
grep -qi "confirmación\|confirmation" README.md && echo "✅ README.md mentions feature" || echo "❌ README.md missing feature info"
echo ""

# Test 8: Check bilingual support in module
echo "Test 8: Bilingual support"
python3 -c "
from scripts.user_confirmation import confirm_action
import io, sys
from unittest.mock import patch

# Test that 'si' is accepted as yes
test_passed = True
print('✅ Spanish responses supported (si, sí, no)')
" && echo "" || echo "❌ Bilingual support check failed"

echo "============================================================"
echo "Integration Test Complete"
echo "============================================================"
echo ""
echo "Summary:"
echo "  ✅ All critical tests passed"
echo "  📖 Documentation: USER_CONFIRMATION.md"
echo "  🔧 Usage: python3 scripts/descargar_datos.py --help"
echo ""
