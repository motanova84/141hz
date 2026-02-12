#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Soberanía QCAL ∞³
Sovereignty System Test

Este test verifica el sistema de soberanía en CI/CD.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_sovereignty_system():
    """Test completo del sistema de soberanía."""
    print("=" * 80)
    print("TEST DE SOBERANÍA QCAL ∞³")
    print("=" * 80)
    print()
    
    # Import validate_sovereignty function
    from scripts.validate_sovereignty import validate_sovereignty
    
    # Run validation
    result = validate_sovereignty()
    
    # Return exit code
    return result


if __name__ == "__main__":
    sys.exit(test_sovereignty_system())
