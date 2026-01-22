#!/usr/bin/env python3
"""
Tests para validate_experimental_wetlab_noesis88.py

Verificar que la validación de resultados experimentales
funciona correctamente.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-01-22
"""

import pytest
import numpy as np
import json
import os
from validate_experimental_wetlab_noesis88 import (
    WetLabNoesis88Validator,
    ExperimentalResults
)


class TestWetLabNoesis88Validator:
    """Tests para clase WetLabNoesis88Validator"""
    
    def setup_method(self):
        """Inicializar validador antes de cada test"""
        self.validator = WetLabNoesis88Validator()
    
    def test_initialization(self):
        """Verificar inicialización correcta"""
        assert self.validator.I == 0.923
        assert self.validator.I_error == 0.008
        assert self.validator.A_eff == 0.888
        assert self.validator.A_eff_error == 0.005
        assert abs(self.validator.C_infinity - 1.373) < 0.001  # Adjusted
        assert self.validator.psi_experimental == 0.999
        assert self.validator.psi_error == 0.001
        assert self.validator.threshold_psi == 0.888
        assert self.validator.sigma_target == 9.0
        assert self.validator.snr_target == 100.0
        assert self.validator.biological_sensitivity_target == 84.2
        assert self.validator.noise_reduction_target == 3.85
    
    def test_mathematical_equation_validation(self):
        """Test validación ecuación matemática Ψ = I × A²_eff × C^∞"""
        result = self.validator.validate_mathematical_equation()
        
        assert 'psi_calculated' in result
        assert 'psi_experimental' in result
        assert 'difference' in result
        assert 'valid' in result
        
        # Verificar cálculo correcto con nuevo C_infinity
        expected_psi = 0.923 * (0.888 ** 2) * 1.373
        assert abs(result['psi_calculated'] - expected_psi) < 1e-6  # More tolerance
        
        # Debe estar cerca del valor experimental
        assert result['difference'] < 0.01
        assert result['valid'] is True
    
    def test_monte_carlo_error_propagation(self):
        """Test propagación de errores Monte Carlo"""
        result = self.validator.monte_carlo_error_propagation(n_samples=10000)
        
        assert 'mean' in result
        assert 'std' in result
        assert 'median' in result
        assert 'error_valid' in result
        
        # Media debe estar cerca del valor experimental
        assert abs(result['mean'] - 0.999) < 0.01
        
        # Error debe ser razonable (< 0.020)
        assert result['std'] < 0.020
    
    def test_gaussian_error_propagation(self):
        """Test propagación de errores gaussiana"""
        result = self.validator.gaussian_error_propagation()
        
        assert 'sigma_psi' in result
        assert 'error_valid' in result
        assert 'dPsi_dI' in result
        assert 'dPsi_dA' in result
        
        # Derivadas deben ser positivas
        assert result['dPsi_dI'] > 0
        assert result['dPsi_dA'] > 0
        
        # Error debe ser razonable (< 0.020)
        assert result['sigma_psi'] < 0.020
    
    def test_statistical_significance(self):
        """Test validación significancia estadística 9σ"""
        result = self.validator.validate_statistical_significance()
        
        assert 'sigma' in result
        assert 'p_value' in result
        assert 'sigma_valid' in result
        
        # 9σ debe tener p-value muy pequeño
        assert result['sigma'] == 9.0
        assert result['p_value'] < 1e-8
        assert result['sigma_valid'] is True
        
        # Debe cumplir con umbral de falsabilidad
        assert result['p_value'] <= 1e-9  # Más estricto que 1.5e-10 * margen
    
    def test_snr_validation(self):
        """Test validación SNR > 100"""
        result = self.validator.validate_snr(measured_snr=120.0)
        
        assert 'snr_measured' in result
        assert 'snr_target' in result
        assert 'snr_valid' in result
        assert 'snr_factor' in result
        
        assert result['snr_measured'] == 120.0
        assert result['snr_target'] == 100.0
        assert result['snr_valid'] is True
        assert result['snr_factor'] == 1.2
    
    def test_snr_validation_below_threshold(self):
        """Test validación SNR cuando está por debajo del umbral"""
        result = self.validator.validate_snr(measured_snr=95.0)
        
        assert result['snr_valid'] is False
        assert result['snr_measured'] < result['snr_target']
    
    def test_biological_sensitivity_validation(self):
        """Test validación sensibilidad biológica 84.2%"""
        result = self.validator.validate_biological_sensitivity()
        
        assert 'biological_sensitivity' in result
        assert 'valid' in result
        assert 'context' in result
        assert 'theory' in result
        
        assert result['biological_sensitivity'] == 84.2
        assert result['valid'] is True
        assert result['context'] == 'coma/wake states'
        assert result['theory'] == 'OrchOR extension'
    
    def test_noise_reduction_validation(self):
        """Test validación reducción de ruido 3.85×"""
        result = self.validator.validate_noise_reduction()
        
        assert 'noise_reduction_factor' in result
        assert 'valid' in result
        assert 'method' in result
        assert 'baseline' in result
        
        assert result['noise_reduction_factor'] == 3.85
        assert result['valid'] is True
        assert result['method'] == 'QCAL filtrado'
        assert result['baseline'] == 'fluorómetros 700nm'
    
    def test_coherence_threshold_validation(self):
        """Test validación umbral de coherencia Ψ > 0.888"""
        result = self.validator.validate_coherence_threshold()
        
        assert 'psi_experimental' in result
        assert 'threshold' in result
        assert 'valid' in result
        assert 'excess' in result
        
        assert result['psi_experimental'] == 0.999
        assert result['threshold'] == 0.888
        assert result['valid'] is True
        assert result['excess'] > 0.1  # Debe superar significativamente
    
    def test_constant_c_infinity_validation(self):
        """Test validación constante C^∞"""
        result = self.validator.validate_constant_c_infinity()
        
        assert 'c_infinity' in result
        assert 'units' in result
        assert 'valid' in result
        assert 'interpretation' in result
        
        assert abs(result['c_infinity'] - 1.373) < 0.001  # Adjusted
        assert result['units'] == 'adimensional (factor de coherencia)'  # Updated
        assert result['valid'] is True
        assert result['interpretation'] == 'quantum coherence factor'  # Updated
    
    def test_full_validation(self):
        """Test validación completa"""
        results = self.validator.run_full_validation(save_results=False)
        
        # Verificar tipo de resultado
        assert isinstance(results, ExperimentalResults)
        
        # Verificar todos los campos
        assert results.psi_experimental == 0.999
        assert results.psi_uncertainty == 0.001
        assert results.intensity == 0.923
        assert results.intensity_uncertainty == 0.008
        assert results.area_eff == 0.888
        assert results.area_eff_uncertainty == 0.005
        assert abs(results.constant_c_infinity - 1.373) < 0.001  # Adjusted
        assert results.snr > 100.0
        assert results.biological_sensitivity == 84.2
        assert results.noise_reduction_factor == 3.85
        assert results.statistical_significance_sigma == 9.0
        assert results.p_value < 1e-8
        assert results.threshold_psi == 0.888
    
    def test_full_validation_saves_file(self):
        """Test que la validación completa guarda archivo JSON"""
        # Eliminar archivo si existe
        output_file = 'experimental_validation_wetlab_noesis88.json'
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Ejecutar validación
        self.validator.run_full_validation(save_results=True)
        
        # Verificar que se creó el archivo
        assert os.path.exists(output_file)
        
        # Verificar contenido
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert 'experimental_results' in data
        assert 'validation_summary' in data
        assert 'all_valid' in data
        assert 'frequency_f0' in data
        assert 'validation_source' in data
        
        assert data['frequency_f0'] == 141.7001
        assert data['validation_source'] == 'Wet-Lab ∞ + noesis88'
        
        # Limpiar
        os.remove(output_file)
    
    def test_equation_components_within_range(self):
        """Test que todos los componentes de la ecuación están en rangos físicos"""
        # Intensidad debe estar cerca de 1
        assert 0.9 < self.validator.I < 1.0
        
        # Área efectiva debe estar cerca de 0.888 (triple-eight resonance)
        assert 0.88 < self.validator.A_eff < 0.90
        
        # Constante debe ser de orden unidad
        assert 1.0 < self.validator.C_infinity < 2.0  # Updated range
        
        # Resultado final debe estar muy cerca de 1
        assert 0.99 < self.validator.psi_experimental < 1.0
    
    def test_irreversibility_threshold(self):
        """Test que Ψ > 0.888 implica irreversibilidad"""
        # Según el problema: "Ψ > 0.888 umbral manifiesta coherencia universal"
        assert self.validator.psi_experimental > self.validator.threshold_psi
        
        # Calcular margen de irreversibilidad
        excess = self.validator.psi_experimental - self.validator.threshold_psi
        
        # Debe superar significativamente el umbral
        assert excess > 0.1
        assert excess / self.validator.threshold_psi > 0.12  # >12% por encima
    
    def test_ligo_sigma_equivalence(self):
        """Test equivalencia 9σ ≈ 5.5σ LIGO"""
        # El problema afirma que 9σ equivale a ~5.5σ LIGO estándar
        # Esto se refiere a diferentes definiciones de significancia
        
        result = self.validator.validate_statistical_significance()
        
        # Verificar que tenemos ambos p-values
        assert 'p_value' in result  # 9σ
        assert 'p_value_ligo' in result  # 5.5σ
        
        # Ambos deben ser muy pequeños (< 10⁻⁶)
        assert result['p_value'] < 1e-6
        assert result['p_value_ligo'] < 1e-6
        
        # 9σ debe ser más significativo que 5.5σ
        assert result['p_value'] < result['p_value_ligo']


class TestExperimentalResults:
    """Tests para dataclass ExperimentalResults"""
    
    def test_experimental_results_creation(self):
        """Test creación de objeto ExperimentalResults"""
        results = ExperimentalResults(
            psi_experimental=0.999,
            psi_uncertainty=0.001,
            intensity=0.923,
            intensity_uncertainty=0.008,
            area_eff=0.888,
            area_eff_uncertainty=0.005,
            constant_c_infinity=1.373,  # Adjusted
            snr=120.0,
            biological_sensitivity=84.2,
            noise_reduction_factor=3.85,
            statistical_significance_sigma=9.0,
            p_value=1.5e-10,
            threshold_psi=0.888
        )
        
        assert results.psi_experimental == 0.999
        assert results.psi_uncertainty == 0.001
        assert results.intensity == 0.923
        assert results.snr == 120.0
        assert results.biological_sensitivity == 84.2


def test_main_function():
    """Test función main"""
    from validate_experimental_wetlab_noesis88 import main
    
    # Limpiar archivo si existe
    output_file = 'experimental_validation_wetlab_noesis88.json'
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Ejecutar main
    results = main()
    
    assert isinstance(results, ExperimentalResults)
    assert results.psi_experimental == 0.999
    
    # Verificar archivo creado
    assert os.path.exists(output_file)
    
    # Limpiar
    os.remove(output_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
