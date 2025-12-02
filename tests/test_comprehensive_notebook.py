#!/usr/bin/env python3
"""
Test Comprehensive 141.7 Hz Validation Notebook
=================================================

Tests that the comprehensive validation notebook has all required components
as specified in the problem statement.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import unittest
import json
from pathlib import Path


class TestComprehensiveNotebook(unittest.TestCase):
    """Test suite for comprehensive validation notebook"""
    
    def setUp(self):
        """Set up test environment"""
        self.notebooks_dir = Path(__file__).parent.parent / 'notebooks'
        self.notebook_path = self.notebooks_dir / 'comprehensive_141hz_validation.ipynb'
        
        # Load notebook
        with open(self.notebook_path, 'r') as f:
            self.notebook = json.load(f)
        
        # Extract all content
        self.all_content = ""
        for cell in self.notebook['cells']:
            if cell['source']:
                self.all_content += ''.join(cell['source']).lower() + "\n"
    
    def test_notebook_exists(self):
        """Test that comprehensive notebook exists"""
        self.assertTrue(self.notebook_path.exists(), 
                       "Comprehensive notebook does not exist")
    
    def test_notebook_is_valid_json(self):
        """Test that notebook is valid JSON"""
        self.assertIsInstance(self.notebook, dict)
        self.assertIn('cells', self.notebook)
        self.assertIsInstance(self.notebook['cells'], list)
    
    def test_has_minimum_cells(self):
        """Test that notebook has sufficient cells"""
        # Should have at least 40 cells for comprehensive analysis
        self.assertGreaterEqual(len(self.notebook['cells']), 40,
                              "Notebook should have at least 40 cells")
    
    def test_has_part1_fundamentals(self):
        """Test Part 1: Fundamentals section exists"""
        self.assertIn('parte 1', self.all_content)
        self.assertIn('import', self.all_content)
        self.assertIn('f0', self.all_content)
    
    def test_has_part2_single_event(self):
        """Test Part 2: Single Event Validation"""
        # Check for key components of Part 2
        required_elements = [
            'parte 2',
            'gw150914',
            'ringdown',
            'bayes factor',
            'damped',
            'chi',
            'q-transform'
        ]
        
        for element in required_elements:
            self.assertIn(element, self.all_content,
                         f"Part 2 should contain '{element}'")
    
    def test_has_bayes_factor_formula(self):
        """Test that Bayes Factor formula is documented"""
        # Check for BF formula components
        self.assertIn('bayes', self.all_content)
        self.assertIn('chi', self.all_content)
        self.assertIn('exp', self.all_content)
    
    def test_has_ringdown_isolation(self):
        """Test that ringdown isolation is documented"""
        self.assertIn('ringdown', self.all_content)
        # Check for time range (10-60 ms)
        self.assertTrue('10' in self.all_content or '60' in self.all_content)
    
    def test_has_part3_multi_event(self):
        """Test Part 3: Multi-Event Analysis"""
        required_elements = [
            'parte 3',
            'multi',
            'gwtc-1',
            'snr',
            'h1',
            'l1',
            '11'  # 11 events
        ]
        
        for element in required_elements:
            self.assertIn(element, self.all_content,
                         f"Part 3 should contain '{element}'")
    
    def test_has_snr_formula(self):
        """Test that SNR formula is documented"""
        self.assertIn('snr', self.all_content)
        # Check for SNR calculation components
        self.assertTrue(any(x in self.all_content 
                          for x in ['max', 'std', 'signal', 'noise']))
    
    def test_has_frequency_band(self):
        """Test that correct frequency band is used"""
        # Should mention 140.7-142.7 Hz or similar
        self.assertTrue(
            '140' in self.all_content or '141' in self.all_content or '142' in self.all_content,
            "Should specify frequency band around 141.7 Hz"
        )
    
    def test_has_part4_critical_tests(self):
        """Test Part 4: Critical Additional Tests"""
        required_elements = [
            'parte 4',
            'gwtc-3',
            'harmonic',
            'virgo'
        ]
        
        for element in required_elements:
            self.assertIn(element, self.all_content,
                         f"Part 4 should contain '{element}'")
    
    def test_has_harmonic_search(self):
        """Test that harmonic search is implemented"""
        self.assertIn('harmonic', self.all_content)
        # Check for multiple harmonics (2f0, 3f0, etc.)
        self.assertTrue(
            '2f' in self.all_content or '3f' in self.all_content,
            "Should search for harmonics (2f₀, 3f₀)"
        )
    
    def test_has_virgo_validation(self):
        """Test that Virgo validation is included"""
        self.assertTrue(
            'virgo' in self.all_content or 'v1' in self.all_content,
            "Should include Virgo (V1) detector validation"
        )
    
    def test_has_part5_conclusions(self):
        """Test Part 5: Summary and Conclusions"""
        required_elements = [
            'parte 5',
            'resumen',
            'conclusion',
            'evidencia'
        ]
        
        for element in required_elements:
            self.assertIn(element, self.all_content,
                         f"Part 5 should contain '{element}'")
    
    def test_has_evidence_summary_table(self):
        """Test that evidence summary table is present"""
        # Check for table with key metrics
        self.assertIn('tabla', self.all_content)
        
        # Check for key metrics in table
        metrics = ['bayes factor', 'p-value', 'tasa', 'armonic']
        found_metrics = sum(1 for m in metrics if m in self.all_content)
        
        self.assertGreaterEqual(found_metrics, 3,
                              "Evidence table should contain key metrics")
    
    def test_has_thresholds(self):
        """Test that scientific thresholds are documented"""
        # BF > 10
        self.assertTrue(
            ('bf' in self.all_content and '10' in self.all_content) or
            ('bayes' in self.all_content and '10' in self.all_content),
            "Should specify Bayes Factor threshold > 10"
        )
        
        # SNR > 5
        self.assertTrue(
            'snr' in self.all_content and '5' in self.all_content,
            "Should specify SNR threshold > 5"
        )
        
        # Detection rate >= 80%
        self.assertTrue(
            '80' in self.all_content or '0.8' in self.all_content,
            "Should specify detection rate threshold ≥ 80%"
        )
    
    def test_has_scientific_interpretation(self):
        """Test that scientific interpretation is included"""
        interpretation_terms = [
            'interpretaci',
            'significado',
            'evidencia',
            'universalidad',
            'física'
        ]
        
        found_terms = sum(1 for term in interpretation_terms 
                         if term in self.all_content)
        
        self.assertGreaterEqual(found_terms, 3,
                              "Should include scientific interpretation")
    
    def test_has_all_gwtc1_events(self):
        """Test that all 11 GWTC-1 events are mentioned"""
        gwtc1_events = [
            'gw150914', 'gw151012', 'gw151226', 'gw170104', 'gw170608',
            'gw170729', 'gw170809', 'gw170814', 'gw170817', 'gw170818', 'gw170823'
        ]
        
        # At least 8 out of 11 should be explicitly mentioned
        mentioned = sum(1 for event in gwtc1_events if event in self.all_content)
        
        self.assertGreaterEqual(mentioned, 8,
                              f"Should mention most GWTC-1 events (found {mentioned}/11)")
    
    def test_has_code_cells(self):
        """Test that notebook has executable code"""
        code_cells = [cell for cell in self.notebook['cells'] 
                     if cell.get('cell_type') == 'code']
        
        self.assertGreater(len(code_cells), 15,
                          "Should have at least 15 code cells")
    
    def test_has_markdown_documentation(self):
        """Test that notebook has sufficient documentation"""
        markdown_cells = [cell for cell in self.notebook['cells'] 
                         if cell.get('cell_type') == 'markdown']
        
        self.assertGreater(len(markdown_cells), 25,
                          "Should have at least 25 markdown cells for documentation")
    
    def test_has_colab_badge(self):
        """Test that notebook has Google Colab badge"""
        first_cell = self.notebook['cells'][0]
        content = ''.join(first_cell['source']).lower()
        
        self.assertIn('colab', content,
                     "First cell should have Google Colab badge")
    
    def test_has_author_info(self):
        """Test that author information is present"""
        self.assertTrue(
            'mota burruezo' in self.all_content or 'jmmb' in self.all_content,
            "Should include author information"
        )
    
    def test_has_doi(self):
        """Test that DOI is referenced"""
        self.assertIn('doi', self.all_content,
                     "Should reference DOI for citation")
    
    def test_structure_follows_specification(self):
        """Test that notebook structure follows problem statement"""
        # Check that content is organized in the 3 main parts
        parts_check = {
            'Parte 1': False,
            'Parte 2': False,
            'Parte 3': False,
            'Parte 4': False,
            'Parte 5': False
        }
        
        for i in range(1, 6):
            if f'parte {i}' in self.all_content:
                parts_check[f'Parte {i}'] = True
        
        for part, found in parts_check.items():
            self.assertTrue(found, f"{part} section not found")
    
    def test_has_visualization_code(self):
        """Test that visualization code is present"""
        # Check for matplotlib usage
        viz_terms = ['plt.', 'plot', 'figure', 'show', 'savefig']
        found_viz = sum(1 for term in viz_terms if term in self.all_content)
        
        self.assertGreater(found_viz, 3,
                          "Should have visualization code")
    
    def test_has_error_handling(self):
        """Test that code has error handling"""
        # Check for try/except blocks
        self.assertTrue(
            'try:' in self.all_content or 'except' in self.all_content,
            "Should include error handling for data download failures"
        )


def run_comprehensive_notebook_tests():
    """Run all comprehensive notebook tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestComprehensiveNotebook))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_comprehensive_notebook_tests()
    sys.exit(0 if success else 1)
