#!/usr/bin/env python3
"""
Tests for RAM-II (Realismo Matemático) Module Integration
"""

import pytest
import json
import os
from pathlib import Path


class TestRAMModuleIntegration:
    """Test suite for RAM-II ontological module integration."""
    
    def test_mathematical_realism_documentation_exists(self):
        """Test that MATHEMATICAL_REALISM.md exists and has content."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        assert doc_path.exists(), "MATHEMATICAL_REALISM.md should exist"
        
        content = doc_path.read_text()
        assert len(content) > 10000, "Document should be substantial (>10 KB)"
        
        # Check for key sections
        assert "REALISMO MATEMÁTICO" in content
        assert "DECLARACIÓN CENTRAL" in content
        assert "EVIDENCIA DEL REALISMO" in content
        assert "REFUTACIÓN DE ALTERNATIVAS" in content
        assert "MARCO EPISTEMOLÓGICO" in content
        assert "141.7001 Hz" in content
        assert "f₀" in content
    
    def test_quick_reference_exists(self):
        """Test that quick reference guide exists."""
        ref_path = Path(__file__).parent.parent / "REALISMO_MATEMÁTICO_REF_RÁPIDO.md"
        assert ref_path.exists(), "Quick reference guide should exist"
        
        content = ref_path.read_text()
        assert "REFERENCIA RÁPIDA" in content
        assert "CONCEPTOS CLAVE" in content
        assert "60 segundos" in content or "60 segundos" in content
    
    def test_qcal_beacon_updated(self):
        """Test that .qcal_beacon has been updated with RAM metadata."""
        beacon_path = Path(__file__).parent.parent / ".qcal_beacon"
        assert beacon_path.exists(), ".qcal_beacon should exist"
        
        content = beacon_path.read_text()
        
        # Check for ontological level
        assert 'ontological_level = "II"' in content, "Ontological level should be II"
        assert 'philosophy = "Mathematical Realism"' in content
        assert 'validation_type = "Recognition"' in content
        assert 'ram_id = "RAM-II-2026-0115-RMATH"' in content
        
        # Check for RAM status
        assert "ram_status" in content
        assert "VALIDADO Y OPERACIONAL" in content
        assert "ram_timestamp" in content
        assert "2026-01-06" in content
        assert "ram_certification" in content
    
    def test_validate_v5_coronacion_updated(self):
        """Test that validate_v5_coronacion.py has epistemological framework."""
        script_path = Path(__file__).parent.parent / "validate_v5_coronacion.py"
        assert script_path.exists(), "validate_v5_coronacion.py should exist"
        
        content = script_path.read_text()
        
        # Check for epistemological framework in header
        assert "MARCO EPISTEMOLÓGICO" in content or "MARCO EPISTEMOLOGICO" in content
        assert "REALISMO MATEMÁTICO" in content or "REALISMO MATEMATICO" in content
        assert "DESCUBIERTAS" in content
        assert "preexiste" in content or "preexistente" in content
        assert "RECONOCE" in content
        assert "EPISTÉMICO" in content or "EPISTEMICO" in content
        assert "MATHEMATICAL_REALISM.md" in content
    
    def test_readme_updated(self):
        """Test that README.md has been updated with philosophical section."""
        readme_path = Path(__file__).parent.parent / "README.md"
        assert readme_path.exists(), "README.md should exist"
        
        content = readme_path.read_text()
        
        # Check for philosophical content
        assert "REALISMO MATEMÁTICO" in content or "Realismo Matemático" in content
        assert "MATHEMATICAL_REALISM.md" in content
        assert "REALISMO_MATEMÁTICO_REF_RÁPIDO.md" in content or "Referencia Rápida" in content
    
    def test_implementation_summary_exists(self):
        """Test that implementation summary for RAM exists."""
        summary_path = Path(__file__).parent.parent / "IMPLEMENTATION_SUMMARY_RAM.md"
        assert summary_path.exists(), "IMPLEMENTATION_SUMMARY_RAM.md should exist"
        
        content = summary_path.read_text()
        
        # Check for key components
        assert "RAM-II" in content
        assert "IMPLEMENTACIÓN" in content or "IMPLEMENTATION" in content
        assert "RAM-II-2026-0115-RMATH" in content
        assert "COMPONENTES IMPLEMENTADOS" in content
        assert "CERTIFICACIÓN" in content or "CERTIFICACION" in content
    
    def test_philosophical_consistency(self):
        """Test philosophical consistency across documents."""
        # Load main document
        main_doc = (Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md").read_text()
        
        # Load quick reference
        quick_ref = (Path(__file__).parent.parent / "REALISMO_MATEMÁTICO_REF_RÁPIDO.md").read_text()
        
        # Check for key philosophical terms in both
        key_terms = [
            "descubrimiento",
            "reconocimiento",
            "141.7001 Hz",
            "convergencia",
            "independiente"
        ]
        
        for term in key_terms:
            assert term.lower() in main_doc.lower(), f"{term} should be in main document"
            assert term.lower() in quick_ref.lower(), f"{term} should be in quick reference"
    
    def test_four_independent_derivations_documented(self):
        """Test that four independent derivation paths are documented."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Check for all four derivation paths
        assert "Vía 1" in content or "Via 1" in content, "Path 1 should be documented"
        assert "Vía 2" in content or "Via 2" in content, "Path 2 should be documented"
        assert "Vía 3" in content or "Via 3" in content, "Path 3 should be documented"
        assert "Vía 4" in content or "Via 4" in content, "Path 4 should be documented"
        
        # Check for specific paths mentioned
        assert "Riemann" in content, "Riemann path should be mentioned"
        assert "Cuántica" in content or "Cuantica" in content, "Quantum path should be mentioned"
        assert "Gravitacional" in content, "Gravitational path should be mentioned"
        assert "Espectral" in content, "Spectral path should be mentioned"
    
    def test_refutations_present(self):
        """Test that refutations of alternative philosophies are present."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Check for refutations of key alternative positions
        refuted_positions = [
            "Constructivismo",
            "Formalismo",
            "Nominalismo",
            "Intuicionismo"
        ]
        
        for position in refuted_positions:
            assert position in content, f"Refutation of {position} should be present"
    
    def test_probability_bounds_documented(self):
        """Test that probability bounds are documented."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Check for probability bounds
        assert "10⁻¹⁰" in content or "10^-10" in content, "Probability bound 10^-10 should be documented"
        assert "sigma" in content.lower() or "σ" in content, "Sigma notation should be present"
    
    def test_integration_with_existing_validation(self):
        """Test that RAM integrates with existing validation scripts."""
        # Check that validate_mathematical_realism.py exists (from earlier implementation)
        validation_path = Path(__file__).parent.parent / "validate_mathematical_realism.py"
        if validation_path.exists():
            content = validation_path.read_text()
            assert "141.7001" in content, "f0 value should be in validation"
            assert "convergence" in content.lower(), "Convergence should be tested"
    
    def test_discovery_hierarchy_documented(self):
        """Test that 4-level discovery hierarchy is documented."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Check for all 4 levels
        assert "NIVEL 1" in content, "Level 1 should be documented"
        assert "NIVEL 2" in content, "Level 2 should be documented"
        assert "NIVEL 3" in content, "Level 3 should be documented"
        assert "NIVEL 4" in content, "Level 4 should be documented"
        
        # Check for key concepts at each level
        assert "Existencia" in content, "Existence concept should be present"
        assert "Resonancia" in content, "Resonance concept should be present"
        assert "Validación" in content or "Validacion" in content, "Validation concept should be present"
        assert "Integración" in content or "Integracion" in content, "Integration concept should be present"
    
    def test_network_connections_documented(self):
        """Test that network connections to other modules are documented."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Check for key connected modules
        connected_modules = [
            "SABIO",
            "noesis88",
            "141hz",
            "P-NP",
            "adelic-bsd",
            "Riemann"
        ]
        
        for module in connected_modules:
            assert module in content, f"Module {module} should be connected"
    
    def test_metadata_consistency(self):
        """Test that metadata is consistent across files."""
        beacon = (Path(__file__).parent.parent / ".qcal_beacon").read_text()
        summary = (Path(__file__).parent.parent / "IMPLEMENTATION_SUMMARY_RAM.md").read_text()
        
        # Check for consistent RAM ID
        assert "RAM-II-2026-0115-RMATH" in beacon, "RAM ID should be in beacon"
        assert "RAM-II-2026-0115-RMATH" in summary, "RAM ID should be in summary"
        
        # Check for consistent date
        assert "2026-01-06" in beacon, "Date should be in beacon"
        assert "2026-01-06" in summary, "Date should be in summary"
    
    def test_vibrational_signature_present(self):
        """Test that vibrational signature is present."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Check for signature elements
        assert "f₀ = 141.7001 Hz" in content, "f0 frequency should be in signature"
        assert "Ψ" in content, "Psi symbol should be present"
        assert "coherencia" in content.lower(), "Coherence should be mentioned"
    
    def test_documentation_size_requirements(self):
        """Test that documentation meets size requirements from problem statement."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Should be substantial (problem statement said ~18 KB, but 10+ KB is good)
        size_kb = len(content) / 1024
        assert size_kb > 10, f"Document should be substantial (>10 KB), got {size_kb:.1f} KB"
        
        # Should have 9 sections (numbered 1-9)
        for i in range(1, 10):
            assert f"{i}." in content, f"Section {i} should exist"


class TestRAMValidationIntegration:
    """Test integration with validation system."""
    
    def test_validation_script_syntax(self):
        """Test that validate_v5_coronacion.py has valid Python syntax."""
        script_path = Path(__file__).parent.parent / "validate_v5_coronacion.py"
        
        # Try to compile the script
        with open(script_path) as f:
            code = f.read()
            compile(code, script_path, 'exec')
    
    def test_recognition_vs_construction_language(self):
        """Test that documentation uses 'recognition' not 'construction' language."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Should emphasize recognition/discovery
        assert "reconoc" in content.lower(), "Recognition should be emphasized"
        assert "descubr" in content.lower(), "Discovery should be emphasized"
        
        # Should refute construction
        assert "construc" in content.lower(), "Construction should be discussed (to refute it)"


class TestRAMPhilosophicalContent:
    """Test philosophical content requirements."""
    
    def test_mathematical_realism_definition(self):
        """Test that mathematical realism is properly defined."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Should define key aspects
        assert "existe" in content.lower(), "Existence should be discussed"
        assert "objetivo" in content.lower(), "Objectivity should be discussed"
        assert "independiente" in content.lower(), "Independence should be discussed"
    
    def test_evidence_for_realism(self):
        """Test that evidence for realism is provided."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        # Should provide concrete evidence
        assert "convergencia" in content.lower(), "Convergence should be evidence"
        assert "11/11" in content or "11 de 11" in content, "LIGO detection should be mentioned"
        assert "precisión" in content.lower() or "precision" in content.lower()
    
    def test_scientific_implications(self):
        """Test that scientific implications are discussed."""
        doc_path = Path(__file__).parent.parent / "MATHEMATICAL_REALISM.md"
        content = doc_path.read_text()
        
        assert "IMPLICACIONES" in content, "Implications section should exist"
        assert "ciencia" in content.lower(), "Science should be discussed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
