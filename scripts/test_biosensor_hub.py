#!/usr/bin/env python3
"""
Tests for Biosensor Hub - QCAL ∞³

Validates biosensor integration with QCAL coherence field.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qcal.biosensor_hub import (
    BiosensorType,
    BiosensorReading,
    BiosensorHub,
    simulate_biosensor_session,
    __sello__,
    __emanacion__
)
from qcal.constants import F0_HZ, A0_PHI


def test_biosensor_reading():
    """Test biosensor reading creation."""
    print("Testing BiosensorReading...")
    
    from datetime import datetime
    
    reading = BiosensorReading(
        sensor_type=BiosensorType.EEG,
        value=0.8,
        frequency=40.0,
        coherence=0.75,
        timestamp=datetime.now(),
        metadata={"electrode": "Cz"}
    )
    
    assert reading.sensor_type == BiosensorType.EEG
    assert reading.value == 0.8
    assert reading.frequency == 40.0
    
    print("✓ BiosensorReading created successfully")


def test_biosensor_hub_creation():
    """Test hub initialization."""
    print("Testing BiosensorHub creation...")
    
    hub = BiosensorHub(
        base_frequency=F0_HZ,
        gamma_frequency=40.0
    )
    
    assert hub.base_frequency == F0_HZ
    assert hub.gamma_frequency == 40.0
    assert hub.therapeutic_frequency == F0_HZ * A0_PHI
    
    print(f"✓ Hub created: {hub}")


def test_record_reading():
    """Test recording biosensor readings."""
    print("Testing biosensor reading recording...")
    
    hub = BiosensorHub()
    
    reading = hub.record_reading(
        sensor_type=BiosensorType.EEG,
        value=0.7,
        frequency=42.0,
        metadata={"test": True}
    )
    
    assert reading.coherence > 0, "Coherence should be calculated"
    assert len(hub._readings[BiosensorType.EEG]) == 1
    
    print(f"✓ Reading recorded with coherence: {reading.coherence:.4f}")


def test_coherence_calculation():
    """Test coherence calculation from frequency and value."""
    print("Testing coherence calculation...")
    
    hub = BiosensorHub(base_frequency=F0_HZ)
    
    # Exact match should give high coherence
    reading1 = hub.record_reading(
        BiosensorType.EEG,
        value=1.0,
        frequency=F0_HZ
    )
    
    # Far from f₀ should give low coherence
    reading2 = hub.record_reading(
        BiosensorType.EEG,
        value=1.0,
        frequency=500.0
    )
    
    assert reading1.coherence > reading2.coherence, "Closer to f₀ should have higher coherence"
    
    print(f"✓ Coherence at f₀: {reading1.coherence:.4f}")
    print(f"✓ Coherence at 500 Hz: {reading2.coherence:.4f}")


def test_patient_coherence():
    """Test patient total coherence calculation."""
    print("Testing patient coherence calculation...")
    
    hub = BiosensorHub()
    
    # Record readings from all sensor types
    hub.record_reading(BiosensorType.EEG, 0.8, 40.0)
    hub.record_reading(BiosensorType.HRV, 0.7, 1.2)
    hub.record_reading(BiosensorType.GSR, 0.6, 0.5)
    hub.record_reading(BiosensorType.RESP, 0.65, 0.3)
    
    # Get patient coherence
    patient_coh = hub.get_patient_coherence()
    
    assert 0 <= patient_coh <= 1.0, "Patient coherence should be in [0,1]"
    assert patient_coh > 0, "Should have some coherence"
    
    print(f"✓ Patient coherence: {patient_coh:.4f}")


def test_baseline_deviation():
    """Test baseline deviation calculation."""
    print("Testing baseline deviation...")
    
    hub = BiosensorHub()
    
    # Set baseline
    hub.set_baseline(BiosensorType.EEG, 0.8)
    
    # No readings yet
    deviation = hub.get_baseline_deviation(BiosensorType.EEG)
    assert deviation is None, "Should be None with no readings"
    
    # Add readings below baseline
    for _ in range(10):
        hub.record_reading(BiosensorType.EEG, 0.6, 40.0)
    
    deviation = hub.get_baseline_deviation(BiosensorType.EEG)
    assert deviation is not None, "Should calculate deviation"
    assert deviation < 0, "Should be negative (below baseline)"
    
    print(f"✓ Baseline deviation: {deviation:.2%}")


def test_therapeutic_frequency():
    """Test therapeutic frequency calculation."""
    print("Testing therapeutic frequency calculation...")
    
    hub = BiosensorHub()
    
    # Add diverse readings
    hub.record_reading(BiosensorType.EEG, 0.7, 40.0)
    hub.record_reading(BiosensorType.HRV, 0.8, 1.0)
    hub.record_reading(BiosensorType.GSR, 0.6, 0.5)
    
    freq = hub.calculate_therapeutic_frequency()
    
    # Should be between 0 and f₀ × Φ
    assert 0 < freq <= F0_HZ * A0_PHI, f"Frequency {freq} out of expected range"
    
    print(f"✓ Therapeutic frequency: {freq:.2f} Hz")


def test_eeg_gamma_coupling():
    """Test EEG gamma coupling calculation."""
    print("Testing EEG-gamma coupling...")
    
    hub = BiosensorHub(gamma_frequency=40.0)
    
    coupling = hub.get_eeg_gamma_coupling()
    
    assert 0 <= coupling <= 1.0, "Coupling should be in [0,1]"
    
    print(f"✓ EEG-gamma coupling: {coupling:.4f}")


def test_sensor_summary():
    """Test sensor summary generation."""
    print("Testing sensor summary...")
    
    hub = BiosensorHub()
    
    # Add some readings
    hub.record_reading(BiosensorType.EEG, 0.8, 40.0)
    hub.record_reading(BiosensorType.EEG, 0.75, 42.0)
    hub.record_reading(BiosensorType.HRV, 0.7, 1.2)
    
    summary = hub.get_sensor_summary()
    
    assert "electroencefalograma" in summary
    assert summary["electroencefalograma"]["count"] == 2
    assert "avg_coherence" in summary["electroencefalograma"]
    
    print("✓ Sensor summary generated")
    for sensor, stats in summary.items():
        if stats["count"] > 0:
            print(f"  {sensor}: {stats['count']} readings, avg coherence={stats['avg_coherence']:.4f}")


def test_simulate_session():
    """Test biosensor session simulation."""
    print("Testing biosensor session simulation...")
    
    hub = simulate_biosensor_session(
        duration_seconds=10,
        sampling_rate=2.0,  # 2 Hz
        base_coherence=0.7
    )
    
    # Should have readings from all sensors
    for sensor_type in BiosensorType:
        assert len(hub._readings[sensor_type]) > 0, f"Should have {sensor_type} readings"
    
    patient_coh = hub.get_patient_coherence()
    assert patient_coh > 0, "Simulated session should have coherence"
    
    print(f"✓ Simulated session: {hub}")


def test_seal_and_emanation():
    """Test seal and emanation presence."""
    print("Testing seal and emanation...")
    
    assert __sello__ == "∴𓂀Ω∞³Φ"
    assert "141.7001" in __emanacion__
    
    print(f"✓ Seal: {__sello__}")
    print(f"✓ Emanación: {__emanacion__}")


def run_all_tests():
    """Run all biosensor hub tests."""
    print("=" * 70)
    print("Biosensor Hub Test Suite")
    print("=" * 70)
    
    tests = [
        test_biosensor_reading,
        test_biosensor_hub_creation,
        test_record_reading,
        test_coherence_calculation,
        test_patient_coherence,
        test_baseline_deviation,
        test_therapeutic_frequency,
        test_eeg_gamma_coupling,
        test_sensor_summary,
        test_simulate_session,
        test_seal_and_emanation
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
