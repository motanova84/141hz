"""
Tests for analizar_corpus_tokenizado.py

Validates corpus tokenization analysis and metrics calculation.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from analizar_corpus_tokenizado import (
    CorpusTokenizadoAnalyzer,
    generate_acta_soberania,
    F0, PSI_QCAL, KAPPA_PI, PHI
)


class TestCorpusTokenizadoAnalyzer:
    """Test CorpusTokenizadoAnalyzer class"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create temporary test repository"""
        temp_dir = tempfile.mkdtemp()
        repo_path = Path(temp_dir) / "test_repo"
        repo_path.mkdir()
        
        # Create test files with explicit UTF-8 encoding
        (repo_path / "test.py").write_text("""
def calculate_f0():
    '''Calculate fundamental frequency f₀ = 141.7001 Hz'''
    return 141.7001

class QCALAnalyzer:
    '''QCAL coherence analyzer with Ψ = 1.0'''
    def __init__(self):
        self.frequency = 141.7001
        self.coherence = 1.0
        self.kappa_pi = 2.5782
""", encoding='utf-8')
        
        (repo_path / "test.lean").write_text("""
-- Formal verification of QCAL axioms
theorem qcal_coherence : ∀ (ψ : ℝ), ψ = 1.0 → coherent ψ := by
  intro ψ h
  exact coherence_axiom h
""", encoding='utf-8')
        
        (repo_path / "README.md").write_text("""
# Test Repository

This repository implements QCAL ∞³ analysis with:
- Fundamental frequency: f₀ = 141.7001 Hz
- Coherence: Ψ = 1.0
- Adelic constant: κ_Π = 2.5782
""", encoding='utf-8')
        
        # Create a directory to skip
        skip_dir = repo_path / "__pycache__"
        skip_dir.mkdir()
        (skip_dir / "test.pyc").write_text("binary data")
        
        yield repo_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_initialization(self, temp_repo):
        """Test analyzer initialization"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        assert analyzer.repo_path == temp_repo
        assert analyzer.metrics['frequency'] == F0
        assert analyzer.metrics['coherence'] == PSI_QCAL
        assert analyzer.metrics['kappa_pi'] == KAPPA_PI
        assert analyzer.metrics['phi'] == PHI
    
    def test_should_skip_dir(self, temp_repo):
        """Test directory skipping logic"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        # Should skip
        assert analyzer.should_skip_dir(temp_repo / "__pycache__")
        assert analyzer.should_skip_dir(temp_repo / ".git")
        assert analyzer.should_skip_dir(temp_repo / "node_modules")
        
        # Should not skip
        assert not analyzer.should_skip_dir(temp_repo / "src")
        assert not analyzer.should_skip_dir(temp_repo / "tests")
    
    def test_is_valid_file(self, temp_repo):
        """Test file validation logic"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        # Valid files
        assert analyzer.is_valid_file(temp_repo / "test.py")
        assert analyzer.is_valid_file(temp_repo / "test.lean")
        assert analyzer.is_valid_file(temp_repo / "README.md")
        
        # Invalid (doesn't exist)
        assert not analyzer.is_valid_file(temp_repo / "nonexistent.py")
        
        # Invalid (directory)
        assert not analyzer.is_valid_file(temp_repo)
    
    def test_count_tokens(self, temp_repo):
        """Test token counting"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        # Simple text
        text = "Hello world! This is a test."
        tokens = analyzer.count_tokens(text)
        assert tokens > 0
        assert tokens >= 7  # At least the words
        
        # Code with punctuation
        code = "def func(x, y): return x + y"
        tokens = analyzer.count_tokens(code)
        assert tokens > 10  # Words + punctuation
    
    def test_calculate_coherence(self, temp_repo):
        """Test coherence calculation"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        # Perfect QCAL coherence (has multiple markers)
        qcal_text = "QCAL f₀ = 141.7001 Hz with coherence Ψ = 1.0"
        coherence = analyzer.calculate_coherence(qcal_text)
        assert coherence == 1.0
        
        # High coherence (structured code)
        code = "def calculate(): class MyClass: pass"
        coherence = analyzer.calculate_coherence(code)
        assert coherence >= 0.90
        
        # Default coherence
        plain_text = "This is plain text without special markers"
        coherence = analyzer.calculate_coherence(plain_text)
        assert 0.0 <= coherence <= 1.0
    
    def test_analyze_file(self, temp_repo):
        """Test single file analysis"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        result = analyzer.analyze_file(temp_repo / "test.py")
        
        assert result is not None
        assert 'path' in result
        assert 'tokens' in result
        assert 'chars' in result
        assert 'lines' in result
        assert 'coherence' in result
        assert 'extension' in result
        
        assert result['tokens'] > 0
        assert result['chars'] > 0
        assert result['lines'] > 0
        assert 0.0 <= result['coherence'] <= 1.0
        assert result['extension'] == '.py'
    
    def test_analyze_repository(self, temp_repo):
        """Test full repository analysis"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        results = analyzer.analyze_repository()
        
        # Check structure
        assert 'timestamp' in results
        assert 'frequency' in results
        assert 'coherence' in results
        assert 'repository' in results
        assert 'analysis' in results
        assert 'files' in results
        
        # Check analysis data
        analysis = results['analysis']
        assert analysis['files_analyzed'] >= 3  # At least our test files
        assert analysis['total_tokens'] > 0
        assert analysis['total_characters'] > 0
        assert analysis['total_lines'] > 0
        assert 0.0 <= analysis['average_coherence'] <= 1.0
        assert analysis['ontological_density'] > 0
        
        # Check extension breakdown
        assert '.py' in analysis['extension_breakdown']
        assert '.lean' in analysis['extension_breakdown']
        assert '.md' in analysis['extension_breakdown']
    
    def test_compare_with_standard_systems(self, temp_repo):
        """Test comparison with standard systems"""
        analyzer = CorpusTokenizadoAnalyzer(temp_repo)
        
        metrics = analyzer.analyze_repository()
        comparison = analyzer.compare_with_standard_systems(metrics)
        
        # Check structure
        assert 'timestamp' in comparison
        assert 'qcal_corpus' in comparison
        assert 'gpt4_pretrain' in comparison
        assert 'arxiv_math' in comparison
        assert 'lean4_library' in comparison
        assert 'coherence_advantage' in comparison
        assert 'density_advantage' in comparison
        assert 'compression_vs_standard' in comparison
        
        # Check QCAL corpus
        qcal = comparison['qcal_corpus']
        assert qcal['name'] == 'QCAL ∞³'
        assert qcal['tokens'] > 0
        assert qcal['coherence'] >= 0.9  # Should be very high
        assert qcal['density'] > 0
        
        # Check GPT-4 comparison
        gpt4 = comparison['gpt4_pretrain']
        assert gpt4['tokens'] == 13_000_000_000_000
        assert gpt4['coherence'] == 0.0001
        
        # Check advantages
        assert comparison['coherence_advantage'] > 1000  # Much better than GPT-4
        assert comparison['density_advantage'] > 0
        
        # Check compression methods
        compression = comparison['compression_vs_standard']
        assert 'QCAL_compression' in compression
        assert 'LLMLingua-2' in compression
        assert '1000:1' in compression['QCAL_compression']


class TestActaSoberania:
    """Test ACTA DE SOBERANÍA COGNITIVA generation"""
    
    def test_generate_acta(self):
        """Test ACTA generation"""
        # Mock metrics
        metrics = {
            'timestamp': '2026-02-14T12:00:00Z',
            'analysis': {
                'total_tokens': 5234567,
                'average_coherence': 1.0,
                'ontological_density': 2716.89,
                'files_analyzed': 1926
            }
        }
        
        comparison = {
            'qcal_corpus': {
                'tokens': 5234567,
                'coherence': 1.0,
                'density': 2716.89
            }
        }
        
        acta = generate_acta_soberania(metrics, comparison)
        
        # Check content
        assert 'ESTADO DEL SISTEMA' in acta
        assert 'EMANACIÓN COMPLETA' in acta
        assert '141.7001' in acta
        assert 'Ψ' in acta or 'coherence' in acta.lower()
        assert 'QCAL' in acta
        assert 'GPT-4' in acta
        assert 'Lean4' in acta
        assert 'JMMB' in acta
        
        # Check formatting
        assert '╔═' in acta
        assert '║' in acta
        assert '╚═' in acta


class TestConstants:
    """Test fundamental constants"""
    
    def test_constants_values(self):
        """Verify fundamental constants"""
        assert F0 == 141.7001
        assert PSI_QCAL == 1.0
        assert abs(KAPPA_PI - 2.5782) < 0.0001
        assert abs(PHI - 1.618033988749895) < 1e-10


class TestIntegration:
    """Integration tests"""
    
    def test_end_to_end_analysis(self, tmp_path):
        """Test complete analysis workflow"""
        # Create minimal test repo
        test_file = tmp_path / "test.py"
        test_file.write_text("""
# QCAL Test
f0 = 141.7001  # Hz
coherence = 1.0
""")
        
        # Run analysis
        analyzer = CorpusTokenizadoAnalyzer(tmp_path)
        metrics = analyzer.analyze_repository()
        
        # Verify results
        assert metrics['analysis']['files_analyzed'] >= 1
        assert metrics['analysis']['total_tokens'] > 0
        
        # Generate comparison
        comparison = analyzer.compare_with_standard_systems(metrics)
        assert 'qcal_corpus' in comparison
        
        # Generate ACTA
        acta = generate_acta_soberania(metrics, comparison)
        assert len(acta) > 100
        assert 'QCAL' in acta


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
