#!/usr/bin/env python3
"""
Tests for QCAL signature generation and validation.

This module tests the cryptographic signature functionality for RAM certificates.
"""

import os
import sys
import json
import tempfile
import subprocess
from pathlib import Path


def test_signature_generation():
    """Test signature generation with a sample certificate."""
    print("Testing signature generation...")
    
    # Create a temporary certificate
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        cert_content = """# Test Certificate
        
This is a test certificate for QCAL signature validation.
Frequency: 141.7001 Hz
"""
        f.write(cert_content)
        cert_file = f.name
    
    try:
        # Generate signature
        result = subprocess.run(
            ['python3', 'generate_qcal_signature.py', cert_file, 'TEST-RAM-001'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Signature generation failed: {result.stderr}"
        
        # Check signature file exists
        sig_file = Path('TEST-RAM-001.qcal_sig')
        assert sig_file.exists(), "Signature file not created"
        
        # Verify signature content
        with open(sig_file) as f:
            sig_data = json.load(f)
        
        assert sig_data['ram_id'] == 'TEST-RAM-001'
        assert sig_data['algorithm'] == 'SHA3-256'
        assert 'hash' in sig_data
        assert len(sig_data['hash']) == 64  # SHA3-256 produces 64 hex chars
        
        print("✓ Signature generation test passed")
        return cert_file, sig_file
        
    except Exception as e:
        if Path(cert_file).exists():
            os.unlink(cert_file)
        raise e


def test_signature_validation(cert_file, sig_file):
    """Test signature validation with valid and invalid certificates."""
    print("\nTesting signature validation...")
    
    try:
        # Test with valid certificate
        result = subprocess.run(
            ['python3', 'validate_qcal_signature.py', cert_file, str(sig_file)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Valid signature validation failed: {result.stderr}"
        assert "✓ ¡FIRMA VÁLIDA!" in result.stdout
        assert "VALIDATED" in result.stdout
        
        print("✓ Valid signature validation test passed")
        
        # Test with modified certificate
        with open(cert_file, 'a') as f:
            f.write("\n# Modified content\n")
        
        result = subprocess.run(
            ['python3', 'validate_qcal_signature.py', cert_file, str(sig_file)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 1, "Invalid signature should return non-zero exit code"
        assert "❌ ¡FIRMA INVÁLIDA!" in result.stdout
        assert "INVALID" in result.stdout
        
        print("✓ Invalid signature detection test passed")
        
    finally:
        # Cleanup
        if Path(cert_file).exists():
            os.unlink(cert_file)
        if sig_file.exists():
            os.unlink(sig_file)


def test_real_certificate():
    """Test with the actual RAM-II certificate."""
    print("\nTesting real RAM-II certificate...")
    
    cert_file = Path('RAM-II-CERTIFICADO.md')
    sig_file = Path('RAM-II-2026-0115-RMATH.qcal_sig')
    
    if not cert_file.exists() or not sig_file.exists():
        print("⚠️  Skipping real certificate test (files not found)")
        return
    
    result = subprocess.run(
        ['python3', 'validate_qcal_signature.py', str(cert_file), str(sig_file)],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Real certificate validation failed: {result.stderr}"
    assert "✓ ¡FIRMA VÁLIDA!" in result.stdout
    assert "141.7001 Hz" in result.stdout
    
    print("✓ Real certificate validation test passed")


def main():
    """Run all tests."""
    print("=" * 70)
    print("QCAL Signature System Test Suite")
    print("=" * 70)
    
    try:
        # Test signature generation
        cert_file, sig_file = test_signature_generation()
        
        # Test signature validation
        test_signature_validation(cert_file, sig_file)
        
        # Test real certificate
        test_real_certificate()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
