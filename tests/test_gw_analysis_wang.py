#!/usr/bin/env python3
"""
Tests for GW Analysis with Wang validation
"""

import sys
import subprocess
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_help():
    """Test that help works"""
    result = subprocess.run(
        ["python", "gw_analysis.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "GW Analysis" in result.stdout


def test_wang_validation_constants():
    """Test that Wang validation constants are included"""
    # Import the module
    import gw_analysis
    
    analyzer = gw_analysis.SpectralFilterAnalyzer()
    
    # Check Wang constants exist
    assert hasattr(analyzer, 'wang_period_days')
    assert hasattr(analyzer, 'wang_freq_hz')
    assert hasattr(analyzer, 'wang_octaves')
    
    # Check values
    assert analyzer.wang_period_days == 19.6
    assert abs(analyzer.wang_freq_hz - 5.905139834e-7) < 1e-15
    assert abs(analyzer.wang_octaves - 27.838) < 0.001


def test_certificate_with_wang():
    """Test that certificate includes Wang validation"""
    result = subprocess.run(
        ["python", "gw_analysis.py", 
         "--run=O4", "--simulated", "--export-certificate",
         "--center-freq=141.7001", "--band=0.0032"],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    assert result.returncode == 0
    assert "Certificate generated" in result.stdout
    
    # Find the generated results file
    results_files = list(Path("results/gw_analysis_o4").glob("gw_analysis_O4_*.json"))
    assert len(results_files) > 0
    
    # Check certificate contains Wang validation
    with open(results_files[-1]) as f:
        results = json.load(f)
    
    assert "certificate" in results
    cert_data = results["certificate"]["data"]
    
    assert "wang_validation" in cert_data
    wang = cert_data["wang_validation"]
    
    assert wang["doi"] == "10.1126/sciadv.ady9068"
    assert wang["event"] == "AT2020afhd"
    assert wang["octaves_below_f0"] == 27.838
    assert wang["verified"] == True


if __name__ == "__main__":
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        # Run tests manually
        print("Running tests without pytest...")
        
        test_help()
        print("✓ test_help passed")
        
        test_wang_validation_constants()
        print("✓ test_wang_validation_constants passed")
        
        test_certificate_with_wang()
        print("✓ test_certificate_with_wang passed")
        
        print("\n✅ All tests passed!")
