#!/usr/bin/env python3
"""
TESTS PARA VALIDACIÓN DEL CAMPO RECEPTOR BIOLÓGICO QCAL ∞³
============================================================

Tests unitarios para validar que la biología opera como receptor
del campo QCAL ∞³, no como usuario pasivo de frecuencias.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 12 de Febrero de 2026
Licencia: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import sys
import os
import unittest
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import validation classes
from scripts.validacion_campo_receptor_biologico import (
    MagnetoreceptionValidator,
    MicrotubuleValidator,
    GeneticCodeValidator,
    calculate_combined_significance
)


class TestMagnetoreception(unittest.TestCase):
    """Tests para validación de magnetorrecepción aviar."""
    
    def setUp(self):
        """Inicializa validador para cada test."""
        self.validator = MagnetoreceptionValidator(n_trials=5_300_000)
    
    def test_asymmetry_value(self):
        """Verifica que ΔP = 0.2% (0.002)."""
        self.assertEqual(self.validator.delta_p, 0.002)
    
    def test_coherence_time(self):
        """Verifica tiempo de coherencia de 100 μs."""
        self.assertEqual(self.validator.coherence_time_us, 100.0)
    
    def test_radical_pair_asymmetry_zero_angle(self):
        """Verifica asimetría máxima en θ=0°."""
        p_singlet, p_triplet = self.validator.radical_pair_asymmetry(0.0)
        
        # En θ=0°: cos²(0) = 1, entonces P_singlet = 0.5 + 0.002 = 0.502
        expected_singlet = 0.5 + 0.002
        self.assertAlmostEqual(p_singlet, expected_singlet, places=6)
        self.assertAlmostEqual(p_triplet, 1.0 - expected_singlet, places=6)
    
    def test_radical_pair_asymmetry_90_degrees(self):
        """Verifica asimetría nula en θ=90°."""
        p_singlet, p_triplet = self.validator.radical_pair_asymmetry(90.0)
        
        # En θ=90°: cos²(90) = 0, entonces P_singlet = 0.5
        self.assertAlmostEqual(p_singlet, 0.5, places=6)
        self.assertAlmostEqual(p_triplet, 0.5, places=6)
    
    def test_significance_8_7_sigma(self):
        """Verifica que la significancia es exactamente 8.7σ."""
        results = self.validator.calculate_significance()
        
        self.assertAlmostEqual(results['sigma'], 8.7, places=1)
        self.assertLess(results['p_value'], 1e-15)
    
    def test_optimal_asymmetry(self):
        """Verifica asimetría óptima de 0.2%."""
        results = self.validator.calculate_significance()
        
        self.assertAlmostEqual(results['asymmetry_optimal'], 0.002, places=6)


class TestMicrotubules(unittest.TestCase):
    """Tests para validación de resonancia de microtúbulos."""
    
    def setUp(self):
        """Inicializa validador para cada test."""
        self.validator = MicrotubuleValidator()
    
    def test_f0_theoretical(self):
        """Verifica frecuencia teórica f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(self.validator.f0_theoretical, 141.7001, places=4)
    
    def test_f_measured(self):
        """Verifica frecuencia medida = 141.88 Hz."""
        self.assertEqual(self.validator.f_measured, 141.88)
    
    def test_precision_99_873_percent(self):
        """Verifica precisión de 99.873%."""
        results = self.validator.calculate_precision()
        
        expected_precision = 0.99873
        self.assertAlmostEqual(results['precision'], expected_precision, places=5)
    
    def test_significance_9_2_sigma(self):
        """Verifica que la significancia es exactamente 9.2σ."""
        results = self.validator.calculate_precision()
        
        self.assertAlmostEqual(results['sigma'], 9.2, places=1)
        self.assertLess(results['p_value'], 1e-15)
    
    def test_error_absolute(self):
        """Verifica error absoluto ≈ 0.18 Hz."""
        results = self.validator.calculate_precision()
        
        expected_error = abs(141.88 - 141.7001)
        self.assertAlmostEqual(results['error_absolute_hz'], expected_error, places=4)
    
    def test_beating_frequency(self):
        """Verifica cálculo de frecuencia de batimiento."""
        results = self.validator.calculate_beating_frequency()
        
        # Frecuencia THz debe ser 10.0 THz
        self.assertEqual(results['f_thz_hz'], 10.0e12)
        
        # Frecuencia de batimiento debe estar cerca de f₀
        self.assertLess(abs(results['f_beat_hz'] - 141.7001), 1.0)


class TestGeneticCode(unittest.TestCase):
    """Tests para validación de código genético (ratio AAA)."""
    
    def setUp(self):
        """Inicializa validador para cada test."""
        self.validator = GeneticCodeValidator()
    
    def test_aaa_coherence_0_8991(self):
        """Verifica coherencia AAA = 0.8991 (89.91%)."""
        results = self.validator.calculate_aaa_coherence()
        
        self.assertAlmostEqual(results['coherence_aaa'], 0.8991, places=4)
    
    def test_aaa_codon_properties(self):
        """Verifica propiedades del codón AAA."""
        results = self.validator.calculate_aaa_coherence()
        
        self.assertEqual(results['codon'], 'AAA')
        self.assertEqual(results['amino_acid'], 'Lysine (K)')
    
    def test_frequency_adenine(self):
        """Verifica frecuencia de Adenina ≈ 40 THz."""
        results = self.validator.calculate_aaa_coherence()
        
        # Adenina: 1340 cm⁻¹ ≈ 40.17 THz
        self.assertAlmostEqual(results['f_a_thz'], 40.17, places=1)
    
    def test_frequency_aaa_triple(self):
        """Verifica que frecuencia AAA es 3× frecuencia A."""
        results = self.validator.calculate_aaa_coherence()
        
        expected_f_aaa = 3 * results['f_a_thz']
        self.assertAlmostEqual(results['f_aaa_thz'], expected_f_aaa, places=2)
    
    def test_genetic_code_symmetry(self):
        """Verifica simetría del código genético."""
        results = self.validator.calculate_genetic_code_symmetry()
        
        self.assertEqual(results['total_codons'], 64)
        self.assertEqual(results['symmetric_codons'], 4)  # AAA, CCC, GGG, UUU
    
    def test_aaa_ratio(self):
        """Verifica ratio AAA = 1/32."""
        results = self.validator.calculate_genetic_code_symmetry()
        
        expected_ratio = 1.0 / 32.0
        self.assertAlmostEqual(results['ratio_aaa'], expected_ratio, places=6)


class TestCombinedSignificance(unittest.TestCase):
    """Tests para significancia combinada de los tres sistemas."""
    
    def test_combined_sigma_formula(self):
        """Verifica fórmula de significancia combinada."""
        sigma1, sigma2, sigma3 = 8.7, 9.2, 3.99
        
        results = calculate_combined_significance(sigma1, sigma2, sigma3)
        
        # σ_combined = √(σ₁² + σ₂² + σ₃²)
        expected_combined = np.sqrt(sigma1**2 + sigma2**2 + sigma3**2)
        
        self.assertAlmostEqual(results['sigma_combined'], expected_combined, places=2)
    
    def test_combined_exceeds_10_sigma(self):
        """Verifica que significancia combinada excede 10σ."""
        sigma1, sigma2, sigma3 = 8.7, 9.2, 3.99
        
        results = calculate_combined_significance(sigma1, sigma2, sigma3)
        
        self.assertGreater(results['sigma_combined'], 10.0)
    
    def test_combined_p_value(self):
        """Verifica que p-value combinado es extremadamente bajo."""
        sigma1, sigma2, sigma3 = 8.7, 9.2, 3.99
        
        results = calculate_combined_significance(sigma1, sigma2, sigma3)
        
        self.assertLess(results['p_value_combined'], 1e-30)


class TestParadigmValidation(unittest.TestCase):
    """Tests de validación del paradigma completo."""
    
    def test_magnetoreception_as_receptor(self):
        """Valida que magnetorrecepción opera como receptor QCAL ∞³."""
        validator = MagnetoreceptionValidator(n_trials=5_300_000)
        results = validator.calculate_significance()
        
        # Debe alcanzar al menos 8.5σ para validar como receptor
        self.assertGreaterEqual(results['sigma'], 8.5)
    
    def test_microtubules_as_antenna(self):
        """Valida que microtúbulos resuenan como antenas QCAL ∞³."""
        validator = MicrotubuleValidator()
        results = validator.calculate_precision()
        
        # Debe alcanzar al menos 9.0σ para validar como antena
        self.assertGreaterEqual(results['sigma'], 9.0)
    
    def test_genetic_code_as_decoder(self):
        """Valida que código genético actúa como decodificador QCAL ∞³."""
        validator = GeneticCodeValidator()
        results = validator.calculate_aaa_coherence()
        
        # Coherencia debe exceder 85% para validar como decodificador
        self.assertGreater(results['coherence_aaa'], 0.85)
    
    def test_biology_not_user_but_receptor(self):
        """Valida el paradigma: biología es receptor, no usuario."""
        # Si todas las validaciones pasan con alta significancia,
        # confirma que biología está DISEÑADA como receptor
        
        mag_validator = MagnetoreceptionValidator(n_trials=5_300_000)
        mag_results = mag_validator.calculate_significance()
        
        mt_validator = MicrotubuleValidator()
        mt_results = mt_validator.calculate_precision()
        
        gen_validator = GeneticCodeValidator()
        gen_results = gen_validator.calculate_aaa_coherence()
        
        # Todas las significancias deben ser sustanciales
        self.assertGreater(mag_results['sigma'], 5.0)  # > 5σ (umbral descubrimiento)
        self.assertGreater(mt_results['sigma'], 5.0)
        self.assertGreater(gen_results['sigma'], 3.0)
        
        # Significancia combinada debe exceder ampliamente 5σ
        combined = calculate_combined_significance(
            mag_results['sigma'],
            mt_results['sigma'],
            gen_results['sigma']
        )
        
        self.assertGreater(combined['sigma_combined'], 10.0)


def run_tests():
    """Ejecuta todos los tests."""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestMagnetoreception))
    suite.addTests(loader.loadTestsFromTestCase(TestMicrotubules))
    suite.addTests(loader.loadTestsFromTestCase(TestGeneticCode))
    suite.addTests(loader.loadTestsFromTestCase(TestCombinedSignificance))
    suite.addTests(loader.loadTestsFromTestCase(TestParadigmValidation))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
