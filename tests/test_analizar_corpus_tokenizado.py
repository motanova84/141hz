#!/usr/bin/env python3
"""
Tests para el analizador de corpus tokenizado QCAL ∞³
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analizar_corpus_tokenizado import (
    TokenCounter,
    CorpusAnalyzer,
    BenchmarkComparator,
    CorpusMetrics,
    format_number
)


class TestTokenCounter:
    """Tests para TokenCounter"""
    
    def test_count_tokens_python(self, tmp_path):
        """Test contar tokens en archivo Python"""
        py_file = tmp_path / "test.py"
        content = "def hello():\n    print('world')\n" * 10
        py_file.write_text(content)
        
        count = TokenCounter.count_tokens_in_file(py_file)
        assert count > 0
        assert count < len(content)  # Debe ser menor que caracteres
    
    def test_count_tokens_markdown(self, tmp_path):
        """Test contar tokens en archivo Markdown"""
        md_file = tmp_path / "test.md"
        content = "# Title\n\nSome content here.\n" * 10
        md_file.write_text(content)
        
        count = TokenCounter.count_tokens_in_file(md_file)
        assert count > 0
    
    def test_count_tokens_jupyter(self, tmp_path):
        """Test contar tokens en notebook Jupyter"""
        nb_file = tmp_path / "test.ipynb"
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["import numpy as np\n", "x = np.array([1,2,3])\n"]
                },
                {
                    "cell_type": "markdown",
                    "source": ["# Title\n", "Some text\n"]
                }
            ]
        }
        nb_file.write_text(json.dumps(notebook))
        
        count = TokenCounter.count_tokens_in_file(nb_file)
        assert count > 0
    
    def test_count_tokens_invalid_file(self, tmp_path):
        """Test manejar archivo inválido"""
        invalid_file = tmp_path / "nonexistent.py"
        count = TokenCounter.count_tokens_in_file(invalid_file)
        assert count == 0


class TestCorpusAnalyzer:
    """Tests para CorpusAnalyzer"""
    
    def setup_test_repo(self, tmp_path):
        """Crear repositorio de prueba"""
        # Crear archivos Python
        (tmp_path / "main.py").write_text("def main():\n    pass\n" * 100)
        (tmp_path / "utils.py").write_text("class Utils:\n    pass\n" * 50)
        
        # Crear archivos Markdown
        (tmp_path / "README.md").write_text("# README\n\nContent here.\n" * 50)
        (tmp_path / "DOCS.md").write_text("# Documentation\n\nMore content.\n" * 30)
        
        # Crear archivo Lean
        lean_dir = tmp_path / "formal"
        lean_dir.mkdir()
        (lean_dir / "theorem.lean").write_text("theorem test : True := trivial\n" * 20)
        
        # Crear ENV.lock para reproducibilidad
        (tmp_path / "ENV.lock").write_text("# Lock file\n")
        (tmp_path / "requirements.txt").write_text("numpy==1.24.0\n")
        
        # Crear directorio .github/workflows
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "ci.yml").write_text("name: CI\n")
        
        # Crear directorio excluido
        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "cache.pyc").write_text("binary content")
        
        return tmp_path
    
    def test_analyze_corpus(self, tmp_path):
        """Test analizar corpus completo"""
        repo = self.setup_test_repo(tmp_path)
        
        analyzer = CorpusAnalyzer(repo)
        metrics = analyzer.analyze_corpus()
        
        assert metrics.total_files > 0
        assert metrics.total_tokens > 0
        assert '.py' in metrics.tokens_by_type
        assert '.md' in metrics.tokens_by_type
        assert '.lean' in metrics.tokens_by_type
    
    def test_should_analyze_file(self, tmp_path):
        """Test filtro de archivos"""
        repo = self.setup_test_repo(tmp_path)
        analyzer = CorpusAnalyzer(repo)
        
        # Debe analizar
        assert analyzer._should_analyze_file(Path("test.py"))
        assert analyzer._should_analyze_file(Path("docs/guide.md"))
        
        # No debe analizar
        assert not analyzer._should_analyze_file(Path("__pycache__/cache.pyc"))
        assert not analyzer._should_analyze_file(Path(".git/config"))
        assert not analyzer._should_analyze_file(Path("test.exe"))
    
    def test_calculate_reproducibility(self, tmp_path):
        """Test cálculo de reproducibilidad"""
        repo = self.setup_test_repo(tmp_path)
        analyzer = CorpusAnalyzer(repo)
        
        score = analyzer._calculate_reproducibility()
        
        # Debe tener score alto (ENV.lock + requirements.txt + workflows)
        # Use >= 0.79 to account for floating point precision
        assert score >= 0.79
        assert score <= 1.0
    
    def test_calculate_repo_size(self, tmp_path):
        """Test cálculo de tamaño del repo"""
        repo = self.setup_test_repo(tmp_path)
        analyzer = CorpusAnalyzer(repo)
        
        size_mb = analyzer._calculate_repo_size()
        assert size_mb > 0
        assert size_mb < 10  # Repo de prueba pequeño


class TestBenchmarkComparator:
    """Tests para BenchmarkComparator"""
    
    def test_compare_with_benchmarks(self):
        """Test comparación con benchmarks"""
        metrics = CorpusMetrics(
            total_files=1000,
            total_tokens=5_000_000,
            tokens_by_type={'.py': 2_500_000, '.md': 2_500_000},
            files_by_type={'.py': 500, '.md': 500},
            coherence_density=5_000_000.0,
            reproducibility_score=0.8,
            repo_size_mb=100.0,
            timestamp="2026-01-01T00:00:00Z"
        )
        
        comparison = BenchmarkComparator.compare_with_benchmarks(metrics)
        
        # Verificar QCAL en comparación
        assert 'QCAL ∞³' in comparison
        assert comparison['QCAL ∞³']['tokens'] == 5_000_000
        assert comparison['QCAL ∞³']['coherence'] == 1.0
        
        # Verificar benchmarks estándar
        assert 'GPT-4' in comparison
        assert 'arXiv Math' in comparison
        assert 'Lean4 Library' in comparison
        
        # Verificar datos de GPT-4
        assert comparison['GPT-4']['tokens'] == 13_000_000_000_000
        assert comparison['GPT-4']['coherence'] == 0.20


class TestUtilityFunctions:
    """Tests para funciones de utilidad"""
    
    def test_format_number(self):
        """Test formateo de números"""
        assert format_number(500) == "500"
        assert format_number(1_500) == "1.5K"
        assert format_number(2_500_000) == "2.5M"
        assert format_number(3_500_000_000) == "3.5B"
        assert format_number(13_000_000_000_000) == "13.0T"
    
    def test_format_number_edge_cases(self):
        """Test casos extremos de formateo"""
        assert format_number(0) == "0"
        assert format_number(999) == "999"
        assert format_number(1_000) == "1.0K"
        assert format_number(999_999) == "1000.0K"
        assert format_number(1_000_000) == "1.0M"


class TestCorpusMetrics:
    """Tests para CorpusMetrics dataclass"""
    
    def test_corpus_metrics_creation(self):
        """Test creación de CorpusMetrics"""
        metrics = CorpusMetrics(
            total_files=100,
            total_tokens=1_000_000,
            tokens_by_type={'.py': 600_000, '.md': 400_000},
            files_by_type={'.py': 60, '.md': 40},
            coherence_density=1_000_000.0,
            reproducibility_score=0.9,
            repo_size_mb=50.0,
            timestamp="2026-01-01T00:00:00Z"
        )
        
        assert metrics.total_files == 100
        assert metrics.total_tokens == 1_000_000
        assert metrics.coherence_density == 1_000_000.0
        assert metrics.reproducibility_score == 0.9


class TestIntegration:
    """Tests de integración"""
    
    def test_full_analysis_workflow(self, tmp_path):
        """Test workflow completo de análisis"""
        # Crear repositorio de prueba
        repo = tmp_path / "test_repo"
        repo.mkdir()
        
        # Agregar contenido
        (repo / "main.py").write_text("def main():\n    pass\n" * 100)
        (repo / "README.md").write_text("# Project\n\nDescription.\n" * 50)
        (repo / "ENV.lock").write_text("# Lock\n")
        
        # Analizar
        analyzer = CorpusAnalyzer(repo)
        metrics = analyzer.analyze_corpus()
        
        # Verificar métricas
        assert metrics.total_files == 2
        assert metrics.total_tokens > 0
        assert metrics.reproducibility_score > 0
        
        # Comparar
        comparison = BenchmarkComparator.compare_with_benchmarks(metrics)
        assert 'QCAL ∞³' in comparison
        assert 'GPT-4' in comparison
        
        # Verificar coherencia
        assert comparison['QCAL ∞³']['coherence'] == 1.0
        assert comparison['GPT-4']['coherence'] == 0.20


class TestEdgeCases:
    """Tests para casos extremos"""
    
    def test_empty_repository(self, tmp_path):
        """Test repositorio vacío"""
        analyzer = CorpusAnalyzer(tmp_path)
        metrics = analyzer.analyze_corpus()
        
        assert metrics.total_files == 0
        assert metrics.total_tokens == 0
        assert metrics.tokens_by_type == {}
    
    def test_only_excluded_files(self, tmp_path):
        """Test repositorio solo con archivos excluidos"""
        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "cache.pyc").write_text("binary")
        
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("config")
        
        analyzer = CorpusAnalyzer(tmp_path)
        metrics = analyzer.analyze_corpus()
        
        assert metrics.total_files == 0
        assert metrics.total_tokens == 0
    
    def test_unicode_content(self, tmp_path):
        """Test contenido Unicode"""
        py_file = tmp_path / "unicode.py"
        content = "# Español: ñ, á, é, í, ó, ú\n" * 10
        content += "# Emoji: 🚀 ∞³ ✧ Ψ\n" * 10
        py_file.write_text(content, encoding='utf-8')
        
        count = TokenCounter.count_tokens_in_file(py_file)
        assert count > 0


# Configuración de pytest
@pytest.fixture
def tmp_path(tmp_path_factory):
    """Fixture para directorio temporal"""
    return tmp_path_factory.mktemp("test_corpus")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
