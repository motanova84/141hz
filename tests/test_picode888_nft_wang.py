#!/usr/bin/env python3
"""
Tests for πCODE-888 NFT with Wang validation
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
        ["python", "picode888_nft.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "NFT Minting System" in result.stdout


def test_wang_validation_constants():
    """Test that Wang validation constants are included"""
    # Import the module
    import picode888_nft
    
    nft = picode888_nft.PiCode888NFT()
    
    # Check Wang constants exist
    assert hasattr(nft, 'wang_doi')
    assert hasattr(nft, 'wang_period_days')
    assert hasattr(nft, 'wang_freq_hz')
    assert hasattr(nft, 'wang_octaves')
    assert hasattr(nft, 'wang_error')
    
    # Check values
    assert nft.wang_doi == "10.1126/sciadv.ady9068"
    assert nft.wang_period_days == 19.6
    assert abs(nft.wang_freq_hz - 5.905139834e-7) < 1e-15
    assert nft.wang_octaves == 27.838
    assert nft.wang_error == 0.0018


def test_nft_metadata_with_wang():
    """Test that NFT metadata includes Wang validation"""
    # Clean old files first
    import shutil
    nft_output = Path("nft_output")
    if nft_output.exists():
        for f in nft_output.glob("picode888_*.json"):
            f.unlink()
    
    result = subprocess.run(
        ["python", "picode888_nft.py"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    assert result.returncode == 0
    assert "NFT Minting Complete" in result.stdout
    
    # Find the generated metadata file
    metadata_files = list(Path("nft_output").glob("picode888_metadata_*.json"))
    assert len(metadata_files) > 0
    
    # Check metadata contains Wang validation
    with open(metadata_files[-1]) as f:
        metadata = json.load(f)
    
    # Check in properties
    assert "properties" in metadata
    assert "wang_validation" in metadata["properties"]
    
    wang = metadata["properties"]["wang_validation"]
    assert wang["doi"] == "10.1126/sciadv.ady9068"
    assert wang["event"] == "AT2020afhd"
    assert wang["octaves_below_f0"] == 27.838
    assert wang["verified"] == True
    
    # Check in attributes
    attributes = metadata["attributes"]
    wang_attrs = [a for a in attributes if "Wang" in a.get("trait_type", "")]
    assert len(wang_attrs) >= 3  # At least Wang Validation, Wang DOI, Wang Error


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
        
        test_nft_metadata_with_wang()
        print("✓ test_nft_metadata_with_wang passed")
        
        print("\n✅ All tests passed!")
