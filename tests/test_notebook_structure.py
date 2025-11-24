#!/usr/bin/env python3
"""
Test Notebook Structure and Validity
====================================

Tests that Jupyter notebooks are well-formed and have proper structure.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import json
from pathlib import Path


class TestNotebookStructure(unittest.TestCase):
    """Test suite for notebook structure validation"""
    
    def setUp(self):
        """Set up test environment"""
        self.notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        self.new_notebooks = [
            'spectral_analysis_gw150914.ipynb',
            'statistical_validation_bayesian.ipynb',
            'multi_event_snr_analysis.ipynb'
        ]
        
    def test_notebooks_exist(self):
        """Test that all new notebooks exist"""
        for notebook_name in self.new_notebooks:
            notebook_path = self.notebooks_dir / notebook_name
            self.assertTrue(notebook_path.exists(), 
                          f"Notebook {notebook_name} does not exist")
            
    def test_notebooks_are_valid_json(self):
        """Test that notebooks are valid JSON"""
        for notebook_name in self.new_notebooks:
            notebook_path = self.notebooks_dir / notebook_name
            
            with open(notebook_path, 'r') as f:
                try:
                    notebook_data = json.load(f)
                    self.assertIsInstance(notebook_data, dict)
                except json.JSONDecodeError as e:
                    self.fail(f"Notebook {notebook_name} is not valid JSON: {e}")
                    
    def test_notebooks_have_required_fields(self):
        """Test that notebooks have required fields"""
        required_fields = ['cells', 'metadata', 'nbformat', 'nbformat_minor']
        
        for notebook_name in self.new_notebooks:
            notebook_path = self.notebooks_dir / notebook_name
            
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
                
            for field in required_fields:
                self.assertIn(field, notebook_data,
                            f"Notebook {notebook_name} missing field: {field}")
                            
    def test_notebooks_have_cells(self):
        """Test that notebooks have cells"""
        for notebook_name in self.new_notebooks:
            notebook_path = self.notebooks_dir / notebook_name
            
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
                
            self.assertIn('cells', notebook_data)
            self.assertIsInstance(notebook_data['cells'], list)
            self.assertGreater(len(notebook_data['cells']), 0,
                             f"Notebook {notebook_name} has no cells")
                             
    def test_notebooks_have_markdown_cells(self):
        """Test that notebooks have markdown documentation cells"""
        for notebook_name in self.new_notebooks:
            notebook_path = self.notebooks_dir / notebook_name
            
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
                
            markdown_cells = [cell for cell in notebook_data['cells'] 
                            if cell.get('cell_type') == 'markdown']
            
            self.assertGreater(len(markdown_cells), 0,
                             f"Notebook {notebook_name} has no markdown cells")
                             
    def test_notebooks_have_code_cells(self):
        """Test that notebooks have code cells"""
        for notebook_name in self.new_notebooks:
            notebook_path = self.notebooks_dir / notebook_name
            
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
                
            code_cells = [cell for cell in notebook_data['cells'] 
                         if cell.get('cell_type') == 'code']
            
            self.assertGreater(len(code_cells), 0,
                             f"Notebook {notebook_name} has no code cells")
                             
    def test_spectral_analysis_has_key_sections(self):
        """Test that spectral analysis notebook has key sections"""
        notebook_path = self.notebooks_dir / 'spectral_analysis_gw150914.ipynb'
        
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
            
        # Get all markdown content
        markdown_content = []
        for cell in notebook_data['cells']:
            if cell.get('cell_type') == 'markdown':
                markdown_content.append('\n'.join(cell.get('source', [])))
        
        full_text = '\n'.join(markdown_content).lower()
        
        # Check for key sections
        key_terms = ['gw150914', 'espectral', 'fft', '141.7', 'snr']
        for term in key_terms:
            self.assertIn(term, full_text,
                         f"Key term '{term}' not found in spectral analysis notebook")
                         
    def test_statistical_validation_has_key_sections(self):
        """Test that statistical validation notebook has key sections"""
        notebook_path = self.notebooks_dir / 'statistical_validation_bayesian.ipynb'
        
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
            
        # Get all markdown content
        markdown_content = []
        for cell in notebook_data['cells']:
            if cell.get('cell_type') == 'markdown':
                markdown_content.append('\n'.join(cell.get('source', [])))
        
        full_text = '\n'.join(markdown_content).lower()
        
        # Check for key sections
        key_terms = ['bayes', 'p-value', 'estadística', 'significancia']
        for term in key_terms:
            self.assertIn(term, full_text,
                         f"Key term '{term}' not found in statistical validation notebook")
                         
    def test_multi_event_has_key_sections(self):
        """Test that multi-event notebook has key sections"""
        notebook_path = self.notebooks_dir / 'multi_event_snr_analysis.ipynb'
        
        with open(notebook_path, 'r') as f:
            notebook_data = json.load(f)
            
        # Get all markdown content
        markdown_content = []
        for cell in notebook_data['cells']:
            if cell.get('cell_type') == 'markdown':
                markdown_content.append('\n'.join(cell.get('source', [])))
        
        full_text = '\n'.join(markdown_content).lower()
        
        # Check for key sections
        key_terms = ['multi-evento', 'gwtc-1', 'snr', 'h1', 'l1']
        for term in key_terms:
            self.assertIn(term, full_text,
                         f"Key term '{term}' not found in multi-event notebook")


def run_notebook_tests():
    """Run all notebook structure tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNotebookStructure))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_notebook_tests()
    sys.exit(0 if success else 1)
