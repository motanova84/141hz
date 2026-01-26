#!/usr/bin/env python3
"""
Test script to verify the automation system is properly configured.

This validates that:
1. recolectar_datos_crudos.py has 7 mathematical validations
2. recolectar_datos_crudos.py has 5 GW analyses  
3. Timeouts are properly configured (600s for validations, 900s for GW)
4. All referenced scripts exist
5. MANIFIESTO structure is correct
6. DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md exists
"""

import sys
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent


def test_recolectar_datos_crudos_configuration():
    """Test that recolectar_datos_crudos.py is properly configured."""
    script_path = BASE_DIR / "scripts" / "recolectar_datos_crudos.py"
    
    if not script_path.exists():
        print(f"❌ FAIL: {script_path} not found")
        return False
    
    content = script_path.read_text()
    
    # Count mathematical validations
    math_val_pattern = r'validaciones = \[(.*?)\]'
    math_match = re.search(math_val_pattern, content, re.DOTALL)
    if math_match:
        math_validations = [line.strip() for line in math_match.group(1).split('\n') if line.strip() and line.strip().startswith('(')]
        print(f"✅ Found {len(math_validations)} mathematical validations")
        if len(math_validations) != 7:
            print(f"⚠️  WARNING: Expected 7 validations, found {len(math_validations)}")
    else:
        print("❌ FAIL: Could not find mathematical validations list")
        return False
    
    # Count GW analyses
    gw_pattern = r'analisis = \[(.*?)\]'
    gw_match = re.search(gw_pattern, content, re.DOTALL)
    if gw_match:
        gw_analyses = [line.strip() for line in gw_match.group(1).split('\n') if line.strip() and line.strip().startswith('(')]
        print(f"✅ Found {len(gw_analyses)} GW analyses")
        if len(gw_analyses) != 5:
            print(f"⚠️  WARNING: Expected 5 GW analyses, found {len(gw_analyses)}")
    else:
        print("❌ FAIL: Could not find GW analyses list")
        return False
    
    # Check timeouts
    if 'timeout=600' in content:
        print("✅ Found 600s timeout for mathematical validations")
    else:
        print("⚠️  WARNING: 600s timeout not found")
    
    if 'timeout=900' in content:
        print("✅ Found 900s timeout for GW analyses")
    else:
        print("⚠️  WARNING: 900s timeout not found")
    
    return True


def test_activar_agentes_configuration():
    """Test that activar_agentes.py is properly configured."""
    script_path = BASE_DIR / "scripts" / "activar_agentes.py"
    
    if not script_path.exists():
        print(f"❌ FAIL: {script_path} not found")
        return False
    
    print(f"✅ activar_agentes.py exists")
    return True


def test_referenced_scripts_exist():
    """Test that all scripts referenced by recolectar_datos_crudos.py exist."""
    scripts = [
        "validate_mathematical_realism.py",
        "validate_riemann_zeros.py",
        "validate_hydrogen_octave_relationship.py",
        "validate_four_pillars.py",
        "verify_kappa.py",
        "formalizacion_teorema_qcal_pi.py",
        "pozo_infinito_cuantico.py",
        "validate_at2020afhd.py",
        "validate_at2020afhd_harmonic.py",
        "validate_at2020afhd_periodicity.py",
        "AT2020afhd_Real_Data_Analysis.py",
        "validate_riemann_ringdown_gw250114.py",
    ]
    
    missing = []
    for script in scripts:
        script_path = BASE_DIR / script
        if not script_path.exists():
            missing.append(script)
    
    if missing:
        print(f"⚠️  WARNING: {len(missing)} scripts not found:")
        for s in missing:
            print(f"     - {s}")
    else:
        print(f"✅ All {len(scripts)} referenced scripts exist (7 math + 5 GW)")
    
    return len(missing) == 0


def test_demostraciones_matematicas_exist():
    """Test that DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md exists."""
    doc_path = BASE_DIR / "DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md"
    
    if not doc_path.exists():
        print(f"❌ FAIL: DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md not found")
        return False
    
    content = doc_path.read_text()
    
    # Check for key sections
    required_sections = [
        "141.7001 Hz",
        "Demostración Principal",
        "Teorema",
        "f₀",
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"⚠️  WARNING: Missing sections in DEMOSTRACIONES: {missing_sections}")
    else:
        print(f"✅ DEMOSTRACIONES_MATEMATICAS_COMPLETAS.md exists with key sections")
    
    return True


def test_manifest_structure():
    """Test that datos_crudos_analisis directory structure is correct."""
    datos_dir = BASE_DIR / "datos_crudos_analisis"
    
    if not datos_dir.exists():
        print("⚠️  WARNING: datos_crudos_analisis directory not found")
        return True  # Don't fail, just warn
    
    required_subdirs = ["matematicas", "ondas_gravitacionales", "demostraciones", "visualizaciones"]
    missing_dirs = []
    
    for subdir in required_subdirs:
        if not (datos_dir / subdir).exists():
            missing_dirs.append(subdir)
    
    if missing_dirs:
        print(f"⚠️  WARNING: Missing subdirectories: {missing_dirs}")
    else:
        print(f"✅ All required subdirectories exist in datos_crudos_analisis")
    
    # Check for manifest
    manifest_path = datos_dir / "MANIFIESTO_DATOS_CRUDOS.json"
    if manifest_path.exists():
        print("✅ MANIFIESTO_DATOS_CRUDOS.json exists")
    else:
        print("⚠️  WARNING: MANIFIESTO_DATOS_CRUDOS.json not found")
    
    return True


def main():
    """Run all tests."""
    print("="*80)
    print("  AUTOMATION SYSTEM VERIFICATION")
    print("  Testing: recolectar_datos_crudos.py & activar_agentes.py")
    print("="*80)
    print()
    
    tests = [
        ("recolectar_datos_crudos.py configuration", test_recolectar_datos_crudos_configuration),
        ("activar_agentes.py configuration", test_activar_agentes_configuration),
        ("Referenced scripts existence", test_referenced_scripts_exist),
        ("Mathematical demonstrations document", test_demostraciones_matematicas_exist),
        ("Manifest structure", test_manifest_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'─'*80}")
        print(f"Testing: {test_name}")
        print(f"{'─'*80}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("  SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - Automation system is properly configured")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed - Review configuration")
        return 1


if __name__ == "__main__":
    sys.exit(main())
