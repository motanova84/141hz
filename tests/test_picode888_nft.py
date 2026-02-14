#!/usr/bin/env python3
"""
Tests for picode888_nft.py
===========================

Test suite for the πCODE-888 NFT minting system.
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from picode888_nft import PiCode888NFT


class TestPiCode888NFT:
    """Test cases for πCODE-888 NFT minting."""
    
    def test_initialization(self):
        """Test NFT minter initialization."""
        minter = PiCode888NFT()
        
        assert minter.f0 == 141.7001
        assert minter.kappa_pi == 2.5773
        assert minter.token_id == 888
        assert minter.symbol == "πCODE"
        assert minter.initial_value_usd == 2_000_000
    
    def test_custom_doi(self):
        """Test initialization with custom DOI."""
        custom_doi = "10.5281/zenodo.12345678"
        minter = PiCode888NFT(zenodo_doi=custom_doi)
        
        assert minter.zenodo_doi == custom_doi
    
    def test_pdf_hash_simulated(self):
        """Test PDF hash computation in simulated mode."""
        minter = PiCode888NFT()
        pdf_hash = minter.compute_pdf_hash()
        
        # Should return a valid SHA-256 hash
        assert len(pdf_hash) == 64
        assert all(c in "0123456789abcdef" for c in pdf_hash)
    
    def test_constants_encoding(self):
        """Test QCAL constants encoding."""
        minter = PiCode888NFT()
        encoded = minter.encode_constants()
        
        # Should be 3 doubles (24 bytes)
        assert len(encoded) == 24
    
    def test_proof_of_coherence(self):
        """Test Proof-of-Coherence generation."""
        minter = PiCode888NFT()
        pdf_hash = minter.compute_pdf_hash()
        poc_hash = minter.generate_proof_of_coherence(pdf_hash)
        
        # Should return valid SHA-256 hash
        assert len(poc_hash) == 64
        assert all(c in "0123456789abcdef" for c in poc_hash)
    
    def test_on_chain_seal(self):
        """Test on-chain seal generation."""
        minter = PiCode888NFT()
        pdf_hash = minter.compute_pdf_hash()
        poc_hash = minter.generate_proof_of_coherence(pdf_hash)
        seal = minter.generate_on_chain_seal(pdf_hash, poc_hash)
        
        # Check seal structure
        assert "version" in seal
        assert "timestamp" in seal
        assert "proof_of_coherence" in seal
        assert "components" in seal
        assert "verification" in seal
        
        # Check components
        assert seal["components"]["f0_hz"] == minter.f0
        assert seal["components"]["kappa_pi"] == minter.kappa_pi
    
    def test_nft_metadata(self):
        """Test NFT metadata generation."""
        minter = PiCode888NFT()
        pdf_hash = minter.compute_pdf_hash()
        poc_hash = minter.generate_proof_of_coherence(pdf_hash)
        metadata = minter.generate_nft_metadata(pdf_hash, poc_hash)
        
        # Check standard NFT fields
        assert "name" in metadata
        assert "description" in metadata
        assert "image" in metadata
        assert "external_url" in metadata
        assert "attributes" in metadata
        assert "properties" in metadata
        
        # Check specific attributes
        attributes = {attr["trait_type"]: attr["value"] for attr in metadata["attributes"]}
        assert attributes["Token ID"] == 888
        assert attributes["Symbol"] == "πCODE"
        assert attributes["Frequency (Hz)"] == 141.7001
    
    def test_smart_contract_data(self):
        """Test smart contract data generation."""
        minter = PiCode888NFT()
        pdf_hash = minter.compute_pdf_hash()
        poc_hash = minter.generate_proof_of_coherence(pdf_hash)
        contract_data = minter.generate_smart_contract_data(poc_hash)
        
        # Check contract structure
        assert "contract_type" in contract_data
        assert contract_data["contract_type"] == "ERC-721"
        assert "name" in contract_data
        assert "symbol" in contract_data
        assert contract_data["symbol"] == "πCODE"
        
        # Check initialization data
        assert "initialization" in contract_data
        assert "proof_of_coherence" in contract_data["initialization"]
        assert "verification_code" in contract_data["initialization"]
    
    def test_complete_minting(self):
        """Test complete NFT minting process."""
        minter = PiCode888NFT()
        
        # Use temporary output directory
        output_dir = Path("./test_nft_output")
        output_dir.mkdir(exist_ok=True)
        
        try:
            metadata_file, seal_file, contract_file = minter.mint_nft(
                output_dir=output_dir
            )
            
            # Check files exist
            assert metadata_file.exists()
            assert seal_file.exists()
            assert contract_file.exists()
            
            # Validate JSON structure
            with open(metadata_file) as f:
                metadata = json.load(f)
            assert "name" in metadata
            
            with open(seal_file) as f:
                seal = json.load(f)
            assert "proof_of_coherence" in seal
            
            with open(contract_file) as f:
                contract = json.load(f)
            assert "contract_type" in contract
            
        finally:
            # Clean up
            if output_dir.exists():
                for f in output_dir.glob("*"):
                    f.unlink()
                output_dir.rmdir()


class TestProofOfCoherenceConsistency:
    """Test Proof-of-Coherence consistency."""
    
    def test_poc_deterministic(self):
        """Test that PoC is deterministic."""
        minter = PiCode888NFT()
        pdf_hash = minter.compute_pdf_hash()
        
        poc1 = minter.generate_proof_of_coherence(pdf_hash)
        poc2 = minter.generate_proof_of_coherence(pdf_hash)
        
        assert poc1 == poc2
    
    def test_poc_unique_per_pdf(self):
        """Test that PoC changes with different PDF."""
        minter1 = PiCode888NFT(zenodo_doi="10.5281/zenodo.1")
        minter2 = PiCode888NFT(zenodo_doi="10.5281/zenodo.2")
        
        pdf_hash1 = minter1.compute_pdf_hash()
        pdf_hash2 = minter2.compute_pdf_hash()
        
        poc1 = minter1.generate_proof_of_coherence(pdf_hash1)
        poc2 = minter2.generate_proof_of_coherence(pdf_hash2)
        
        assert poc1 != poc2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
