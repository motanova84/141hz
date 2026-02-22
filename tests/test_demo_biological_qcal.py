#!/usr/bin/env python3
"""
Tests for demo_biological_qcal.py
"""

import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_help():
    """Test that help works"""
    result = subprocess.run(
        ["python", "demo_biological_qcal.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Multi-Scale Cascade Analysis" in result.stdout


def test_wang_cascade():
    """Test Wang validation cascade (27.838 octaves)"""
    result = subprocess.run(
        ["python", "demo_biological_qcal.py", 
         "--cascade=27.838", "--export-seal"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0
    assert "Wang et al. validation cascade confirmed" in result.stdout
    assert "27.838" in result.stdout


def test_modes():
    """Test different analysis modes"""
    result = subprocess.run(
        ["python", "demo_biological_qcal.py",
         "--modes=hrv"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0
    assert "HRV" in result.stdout or "Heart Rate" in result.stdout


def test_seal_export():
    """Test seal export"""
    result = subprocess.run(
        ["python", "demo_biological_qcal.py",
         "--export-seal"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0
    assert "Seal exported" in result.stdout
    
    # Check seal file was created
    seal_files = list(Path("results/biological_cascade").glob("biological_cascade_seal_*.json"))
    assert len(seal_files) > 0


if __name__ == "__main__":
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        # Run tests manually
        print("Running tests without pytest...")
        test_help()
        print("✓ test_help passed")
        
        test_wang_cascade()
        print("✓ test_wang_cascade passed")
        
        test_modes()
        print("✓ test_modes passed")
        
        test_seal_export()
        print("✓ test_seal_export passed")
        
        print("\n✅ All tests passed!")
