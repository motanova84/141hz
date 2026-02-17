#!/usr/bin/env python3
"""
Tests for qcal_token_counter.py
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
        ["python", "qcal_token_counter.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "QCAL Token Counter" in result.stdout


def test_basic_count():
    """Test basic token counting"""
    result = subprocess.run(
        ["python", "qcal_token_counter.py"],
        capture_output=True,
        text=True,
        timeout=120
    )
    assert result.returncode == 0
    assert "Total tokens:" in result.stdout
    assert "Total files:" in result.stdout


def test_certificate_export():
    """Test certificate generation"""
    result = subprocess.run(
        ["python", "qcal_token_counter.py", "--export-certificate"],
        capture_output=True,
        text=True,
        timeout=120
    )
    assert result.returncode == 0
    assert "Certificate:" in result.stdout
    
    # Check certificate file exists
    cert_file = Path("results/token_count_certificate.json")
    assert cert_file.exists()
    
    # Verify certificate structure
    with open(cert_file) as f:
        cert = json.load(f)
    
    assert "certificate_id" in cert
    assert "hash" in cert
    assert "data" in cert
    assert "wang_validation" in cert["data"]
    assert cert["data"]["wang_validation"]["verified"] == True


def test_wang_validation_in_certificate():
    """Test that Wang validation is included in certificate"""
    result = subprocess.run(
        ["python", "qcal_token_counter.py", "--export-certificate"],
        capture_output=True,
        text=True,
        timeout=120
    )
    assert result.returncode == 0
    
    cert_file = Path("results/token_count_certificate.json")
    with open(cert_file) as f:
        cert = json.load(f)
    
    wang = cert["data"]["wang_validation"]
    assert wang["doi"] == "10.1126/sciadv.ady9068"
    assert wang["cascade_octaves"] == 27.838
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
        
        test_basic_count()
        print("✓ test_basic_count passed")
        
        test_certificate_export()
        print("✓ test_certificate_export passed")
        
        test_wang_validation_in_certificate()
        print("✓ test_wang_validation_in_certificate passed")
        
        print("\n✅ All tests passed!")
