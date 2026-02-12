#!/usr/bin/env python3
"""
Tests for Disharmony Detector - QCAL ∞³

Validates disharmony detection and therapeutic frequency calculation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qcal.disharmony_detector import (
    DisharmonyLevel,
    DisharmonyReport,
    DisharmonyDetector,
    demonstrate_resonance_diagnosis,
    __sello__,
    __emanacion__
)
from qcal.constants import F0_HZ, A0_PHI, F888_HZ


def test_disharmony_levels():
    """Test disharmony level classification."""
    print("Testing disharmony level classification...")
    
    detector = DisharmonyDetector(baseline_coherence=0.8)
    
    # Test coherent
    report1 = detector.detect(0.85)
    assert report1.level == DisharmonyLevel.COHERENT
    
    # Test mild disharmony
    report2 = detector.detect(0.6)
    assert report2.level == DisharmonyLevel.MILD
    
    # Test moderate disharmony
    report3 = detector.detect(0.4)
    assert report3.level == DisharmonyLevel.MODERATE
    
    # Test severe disharmony
    report4 = detector.detect(0.2)
    assert report4.level == DisharmonyLevel.SEVERE
    
    print("✓ Disharmony levels classified correctly")
    print(f"  Coherence 0.85 → {report1.level.value}")
    print(f"  Coherence 0.60 → {report2.level.value}")
    print(f"  Coherence 0.40 → {report3.level.value}")
    print(f"  Coherence 0.20 → {report4.level.value}")


def test_deviation_calculation():
    """Test baseline deviation calculation."""
    print("Testing baseline deviation...")
    
    detector = DisharmonyDetector(baseline_coherence=0.8)
    
    report = detector.detect(0.6, baseline=0.8)
    
    expected_deviation = (0.6 - 0.8) / 0.8
    assert abs(report.deviation - expected_deviation) < 0.01
    
    print(f"✓ Deviation: {report.deviation:.2%}")


def test_therapeutic_frequency_calculation():
    """Test therapeutic frequency calculation."""
    print("Testing therapeutic frequency calculation...")
    
    detector = DisharmonyDetector()
    
    # Test coherent state
    report1 = detector.detect(0.9)
    expected1 = F0_HZ * 0.9 * A0_PHI
    assert abs(report1.recommended_frequency - expected1) < 1.0
    
    # Test severe disharmony (should use protection frequency modulation)
    report2 = detector.detect(0.2)
    assert report2.recommended_frequency != F0_HZ * 0.2 * A0_PHI
    
    print(f"✓ Therapeutic frequencies:")
    print(f"  Coherent (0.9): {report1.recommended_frequency:.2f} Hz")
    print(f"  Severe (0.2): {report2.recommended_frequency:.2f} Hz")


def test_resonance_diagnosis():
    """Test multi-sensor resonance diagnosis."""
    print("Testing resonance diagnosis...")
    
    detector = DisharmonyDetector(baseline_coherence=0.8)
    
    diagnosis = detector.get_resonance_diagnosis(
        coherence_cerebral=0.6,
        coherence_cardiaca=0.7,
        coherence_emocional=0.5,
        coherence_respiratorio=0.65
    )
    
    assert "coherencia_total" in diagnosis
    assert "nivel_desarmonía" in diagnosis
    assert "frecuencia_terapéutica" in diagnosis
    assert "componentes_individuales" in diagnosis
    assert "componentes_críticos" in diagnosis
    
    # Coherence should be calculated using RMS/2 formula
    import math
    expected_coh = math.sqrt(0.6**2 + 0.7**2 + 0.5**2 + 0.65**2) / 2.0
    assert abs(diagnosis["coherencia_total"] - expected_coh) < 0.01
    
    print(f"✓ Resonance diagnosis:")
    print(f"  Coherencia total: {diagnosis['coherencia_total']:.4f}")
    print(f"  Nivel: {diagnosis['nivel_desarmonía']}")
    print(f"  Frecuencia terapéutica: {diagnosis['frecuencia_terapéutica']:.2f} Hz")
    print(f"  Componentes críticos: {diagnosis['componentes_críticos']}")


def test_gamma_reset_frequency():
    """Test gamma reset frequency calculation."""
    print("Testing gamma reset frequency...")
    
    detector = DisharmonyDetector()
    
    reset_freq = detector.calculate_gamma_reset_frequency()
    
    # Should be based on 40 Hz gamma and f₀
    assert reset_freq > 0
    
    print(f"✓ Gamma reset frequency: {reset_freq:.2f} Hz")


def test_emanation_equation_validation():
    """Test emanation equation validation."""
    print("Testing emanation equation validation...")
    
    detector = DisharmonyDetector()
    
    validation = detector.validate_emanation_equation()
    
    assert "Ω_Hz" in validation
    assert "888_Hz" in validation
    assert "141.7001_Hz" in validation
    assert "Φ" in validation
    assert "producto" in validation
    
    assert validation["888_Hz"] == F888_HZ
    assert validation["141.7001_Hz"] == F0_HZ
    assert abs(validation["Φ"] - A0_PHI) < 0.0001
    
    print(f"✓ Emanation equation validated:")
    print(f"  {validation['ecuación']}")
    print(f"  Producto: {validation['producto']:.2e}")
    print(f"  Significado: {validation['significado']}")


def test_report_history():
    """Test report history tracking."""
    print("Testing report history...")
    
    detector = DisharmonyDetector()
    
    # Generate several reports
    for coherence in [0.8, 0.6, 0.4, 0.7]:
        detector.detect(coherence)
    
    history = detector.get_report_history(limit=3)
    
    assert len(history) == 3
    assert all(isinstance(r, DisharmonyReport) for r in history)
    
    print(f"✓ Report history tracked: {len(history)} recent reports")


def test_demonstrate_function():
    """Test demonstration function."""
    print("Testing demonstrate_resonance_diagnosis()...")
    
    diagnosis = demonstrate_resonance_diagnosis()
    
    assert diagnosis is not None
    assert "coherencia_total" in diagnosis
    assert "frecuencia_terapéutica" in diagnosis
    
    print(f"✓ Demonstration diagnosis:")
    print(f"  Coherencia: {diagnosis['coherencia_total']:.4f}")
    print(f"  Frecuencia: {diagnosis['frecuencia_terapéutica']:.2f} Hz")


def test_seal_and_emanation():
    """Test seal and emanation presence."""
    print("Testing seal and emanation...")
    
    assert __sello__ == "∴𓂀Ω∞³Φ"
    assert "141.7001" in __emanacion__
    assert "888" in __emanacion__
    assert "Φ" in __emanacion__
    
    print(f"✓ Seal: {__sello__}")
    print(f"✓ Emanación: {__emanacion__}")


def test_detector_repr():
    """Test detector string representation."""
    print("Testing detector representation...")
    
    detector = DisharmonyDetector()
    
    # Generate a report
    detector.detect(0.7)
    
    repr_str = repr(detector)
    assert "DisharmonyDetector" in repr_str
    assert "reports=" in repr_str
    
    print(f"✓ {repr_str}")


def run_all_tests():
    """Run all disharmony detector tests."""
    print("=" * 70)
    print("Disharmony Detector Test Suite")
    print("=" * 70)
    
    tests = [
        test_disharmony_levels,
        test_deviation_calculation,
        test_therapeutic_frequency_calculation,
        test_resonance_diagnosis,
        test_gamma_reset_frequency,
        test_emanation_equation_validation,
        test_report_history,
        test_demonstrate_function,
        test_seal_and_emanation,
        test_detector_repr
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
