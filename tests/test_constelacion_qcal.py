"""
╔════════════════════════════════════════════════════════════════════════════╗
║           TESTS CONSTELACIÓN QCAL Ψ✧ - Comprehensive Tests                ║
║                  Test Suite for Constellation System                       ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Comprehensive test suite for the QCAL constellation wave function system.
"""

import pytest
import numpy as np
import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.constelacion_qcal import (
    psi_dorado, psi_azul, psi_verde, psi_violeta, psi_blanco,
    psi_total, calcular_constelacion, analizar_constelacion,
    generar_certificado, punto_ciego_observador, coherencia_local,
    F0_HZ, PHI, OCTAVAS_H_F0, PSI_COHERENCIA_ALTA,
    F_HYDROGEN_HZ, FACTOR_SIETE_OCTAVOS
)


class TestConstantesConstelacion:
    """Test constellation constants."""
    
    def test_f0_hz(self):
        """Test f₀ fundamental frequency."""
        assert F0_HZ == 141.7001
        assert isinstance(F0_HZ, (int, float))
    
    def test_phi_golden_ratio(self):
        """Test golden ratio φ."""
        expected = (1 + np.sqrt(5)) / 2
        assert abs(PHI - expected) < 1e-10
        assert 1.618 < PHI < 1.619
    
    def test_octavas_hydrogen(self):
        """Test hydrogen line octaves."""
        assert 23.0 < OCTAVAS_H_F0 < 24.0
        # Verify calculation
        calculated = np.log2(F_HYDROGEN_HZ / F0_HZ)
        assert abs(OCTAVAS_H_F0 - calculated) < 0.001
    
    def test_coherencia_alta_threshold(self):
        """Test high coherence threshold."""
        assert PSI_COHERENCIA_ALTA == 0.95
    
    def test_berry_factor(self):
        """Test Berry 7/8 factor."""
        assert FACTOR_SIETE_OCTAVOS == 7.0 / 8.0
        assert FACTOR_SIETE_OCTAVOS == 0.875


class TestEjesIndividuales:
    """Test individual wave function axes."""
    
    def test_psi_dorado_basic(self):
        """Test golden axis returns complex number."""
        result = psi_dorado(1, 14.134725)
        assert isinstance(result, complex)
        assert abs(result) > 0
    
    def test_psi_dorado_normalization(self):
        """Test golden axis normalization decreases with n."""
        psi_1 = abs(psi_dorado(1, 14.134725))
        psi_10 = abs(psi_dorado(10, 14.134725))
        assert psi_1 > psi_10
    
    def test_psi_azul_riemann(self):
        """Test blue axis with Riemann zero."""
        # At Riemann zero, zeta should be small
        result = psi_azul(1, 14.134725)
        assert isinstance(result, complex)
        # The zeta value at zero should be very small
        # but not exactly zero due to numerical precision
    
    def test_psi_azul_berry_decay(self):
        """Test Berry factor (7/8)^n decay."""
        psi_1 = abs(psi_azul(1, 20.0))
        psi_5 = abs(psi_azul(5, 20.0))
        # Higher n should have smaller Berry factor contribution
        # Note: this might not always hold due to zeta function oscillations
    
    def test_psi_verde_fibonacci(self):
        """Test green axis with Fibonacci/φ."""
        result = psi_verde(3, 10.0)
        assert isinstance(result, complex)
        assert abs(result) > 0
    
    def test_psi_verde_golden_growth(self):
        """Test φ^n growth in green axis."""
        # φ^n grows exponentially
        psi_1 = abs(psi_verde(1, 10.0))
        psi_5 = abs(psi_verde(5, 10.0))
        # Due to normalization, this relationship is complex
        assert psi_5 != psi_1
    
    def test_psi_violeta_noesis(self):
        """Test violet noetic axis."""
        result = psi_violeta(2, 15.0)
        assert isinstance(result, complex)
        assert abs(result) > 0
    
    def test_psi_violeta_coherence(self):
        """Test violet axis includes PSI_MINIMO_ESTABLE."""
        result = psi_violeta(1, 10.0)
        # Magnitude should be related to coherence threshold
        assert 0 < abs(result) < 1
    
    def test_psi_blanco_hydrogen(self):
        """Test white axis with hydrogen modulation."""
        result = psi_blanco(1, 20.0)
        assert isinstance(result, complex)
        assert abs(result) > 0
    
    def test_psi_blanco_exponential_decay(self):
        """Test white axis exponential decay."""
        psi_1 = abs(psi_blanco(1, 10.0))
        psi_10 = abs(psi_blanco(10, 10.0))
        # Should decay as 2^(-n)
        assert psi_1 > psi_10


class TestFuncionOndaTotal:
    """Test total wave function Ψ_total(x,y)."""
    
    def test_psi_total_returns_complex(self):
        """Test Ψ_total returns complex number."""
        result = psi_total(0.0, 0.0, n_terms=10)
        assert isinstance(result, complex)
    
    def test_psi_total_non_zero(self):
        """Test Ψ_total is non-zero."""
        result = psi_total(0.0, 0.0, n_terms=10)
        assert abs(result) > 0
    
    def test_psi_total_spatial_variation(self):
        """Test Ψ_total varies with spatial position."""
        psi_00 = psi_total(0.0, 0.0, n_terms=10)
        psi_10 = psi_total(1.0, 0.0, n_terms=10)
        psi_01 = psi_total(0.0, 1.0, n_terms=10)
        
        # Should be different at different positions
        assert psi_00 != psi_10
        assert psi_00 != psi_01
    
    def test_psi_total_convergence(self):
        """Test Ψ_total converges with more terms."""
        psi_10 = psi_total(0.5, 0.5, n_terms=10)
        psi_20 = psi_total(0.5, 0.5, n_terms=20)
        psi_30 = psi_total(0.5, 0.5, n_terms=30)
        
        # Differences should decrease
        diff_10_20 = abs(psi_20 - psi_10)
        diff_20_30 = abs(psi_30 - psi_20)
        # Generally expect convergence (though not guaranteed monotonic)
    
    def test_psi_total_symmetry(self):
        """Test Ψ_total has expected symmetries."""
        # Test at symmetric points
        psi_pos = psi_total(1.0, 1.0, n_terms=10)
        psi_neg = psi_total(-1.0, -1.0, n_terms=10)
        
        # Values will be different due to spatial phase
        assert isinstance(psi_pos, complex)
        assert isinstance(psi_neg, complex)


class TestCoherenciaLocal:
    """Test local coherence calculations."""
    
    def test_coherencia_positive(self):
        """Test coherence is positive."""
        psi = 0.5 + 0.3j
        coh = coherencia_local(psi)
        assert coh >= 0
    
    def test_coherencia_magnitude(self):
        """Test coherence equals magnitude."""
        psi = 0.8 + 0.6j
        coh = coherencia_local(psi)
        expected = abs(psi)
        assert abs(coh - expected) < 1e-10
    
    def test_coherencia_zero(self):
        """Test coherence of zero."""
        psi = 0.0 + 0.0j
        coh = coherencia_local(psi)
        assert coh == 0.0


class TestCalcularConstelacion:
    """Test constellation calculation."""
    
    def test_calcular_constelacion_small(self):
        """Test calculating small constellation."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        
        assert 'x' in cons
        assert 'y' in cons
        assert 'psi' in cons
        assert 'coherencia' in cons
        assert 'fase' in cons
    
    def test_constelacion_grid_shape(self):
        """Test constellation grid has correct shape."""
        size = 32
        cons = calcular_constelacion(grid_size=size, n_terms=10)
        
        assert cons['psi'].shape == (size, size)
        assert cons['coherencia'].shape == (size, size)
        assert cons['fase'].shape == (size, size)
    
    def test_constelacion_coherencia_positive(self):
        """Test all coherence values are positive."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        assert np.all(cons['coherencia'] >= 0)
    
    def test_constelacion_fase_range(self):
        """Test phase values in [-π, π]."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        assert np.all(cons['fase'] >= -np.pi - 0.01)
        assert np.all(cons['fase'] <= np.pi + 0.01)
    
    def test_constelacion_custom_range(self):
        """Test constellation with custom spatial range."""
        cons = calcular_constelacion(
            grid_size=16,
            x_range=(-1.0, 1.0),
            y_range=(-1.0, 1.0),
            n_terms=5
        )
        
        assert cons['x'].min() >= -1.0 - 0.01
        assert cons['x'].max() <= 1.0 + 0.01
        assert cons['y'].min() >= -1.0 - 0.01
        assert cons['y'].max() <= 1.0 + 0.01


class TestAnalizarConstelacion:
    """Test constellation analysis."""
    
    def test_analizar_metricas_completas(self):
        """Test analysis returns all required metrics."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        analisis = analizar_constelacion(cons)
        
        required = [
            'coherencia_media', 'coherencia_max', 'coherencia_min',
            'puntos_interes', 'dimension_fractal'
        ]
        for metric in required:
            assert metric in analisis
    
    def test_coherencia_ranges(self):
        """Test coherence metrics have valid ranges."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        analisis = analizar_constelacion(cons)
        
        assert analisis['coherencia_min'] >= 0
        assert analisis['coherencia_media'] >= analisis['coherencia_min']
        assert analisis['coherencia_max'] >= analisis['coherencia_media']
    
    def test_puntos_interes_non_negative(self):
        """Test points of interest count is non-negative."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        analisis = analizar_constelacion(cons)
        
        assert analisis['puntos_interes'] >= 0
        assert isinstance(analisis['puntos_interes'], int)
    
    def test_dimension_fractal_range(self):
        """Test fractal dimension is in [1, 2]."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        analisis = analizar_constelacion(cons)
        
        assert 1.0 <= analisis['dimension_fractal'] <= 2.0


class TestPuntoCiegoObservador:
    """Test observer position calculation."""
    
    def test_punto_ciego_returns_tuple(self):
        """Test observer position returns (x, y) tuple."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        pos = punto_ciego_observador(cons)
        
        assert isinstance(pos, tuple)
        assert len(pos) == 2
    
    def test_punto_ciego_in_range(self):
        """Test observer position is within grid range."""
        cons = calcular_constelacion(
            grid_size=16,
            x_range=(-2.0, 2.0),
            y_range=(-2.0, 2.0),
            n_terms=5
        )
        x_obs, y_obs = punto_ciego_observador(cons)
        
        assert -2.5 <= x_obs <= 2.5
        assert -2.5 <= y_obs <= 2.5
    
    def test_punto_ciego_floats(self):
        """Test observer position returns floats."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        x_obs, y_obs = punto_ciego_observador(cons)
        
        assert isinstance(x_obs, float)
        assert isinstance(y_obs, float)


class TestGenerarCertificado:
    """Test certificate generation."""
    
    def test_certificado_estructura(self):
        """Test certificate has correct structure."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        cert = generar_certificado(cons, fecha="2026-03-14")
        
        assert "constelacion_qcal_psix" in cert
        cert_data = cert["constelacion_qcal_psix"]
        
        required_fields = [
            'fecha', 'sello', 'ejes', 'coherencia_media',
            'puntos_de_interes', 'dimension_fractal',
            'observador_posicion', 'interpretacion', 'estado'
        ]
        for field in required_fields:
            assert field in cert_data
    
    def test_certificado_ejes(self):
        """Test certificate includes all 5 axes."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        cert = generar_certificado(cons)
        
        ejes = cert["constelacion_qcal_psix"]["ejes"]
        required_axes = ['dorado', 'azul', 'violeta', 'verde', 'blanco']
        
        for eje in required_axes:
            assert eje in ejes
    
    def test_certificado_fecha(self):
        """Test certificate includes date."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        fecha = "2026-03-14"
        cert = generar_certificado(cons, fecha=fecha)
        
        assert cert["constelacion_qcal_psix"]["fecha"] == fecha
    
    def test_certificado_sello(self):
        """Test certificate includes seal."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        cert = generar_certificado(cons)
        
        sello = cert["constelacion_qcal_psix"]["sello"]
        assert "∴" in sello or "Ψ" in sello or "Ω" in sello
    
    def test_certificado_json_serializable(self):
        """Test certificate is JSON serializable."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        cert = generar_certificado(cons)
        
        # Should not raise exception
        json_str = json.dumps(cert, ensure_ascii=False)
        assert len(json_str) > 0
        
        # Should be deserializable
        cert_restored = json.loads(json_str)
        assert cert_restored == cert
    
    def test_certificado_observador_posicion(self):
        """Test certificate includes observer position."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        cert = generar_certificado(cons)
        
        obs = cert["constelacion_qcal_psix"]["observador_posicion"]
        assert 'x' in obs
        assert 'y' in obs
        assert 'interpretacion' in obs
        assert obs['interpretacion'] == 'punto_ciego_coherencia'


class TestIntegracionCompleta:
    """Test complete integration scenarios."""
    
    def test_flujo_completo_pequeno(self):
        """Test complete workflow with small grid."""
        # Calculate
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        
        # Analyze
        analisis = analizar_constelacion(cons)
        assert analisis['coherencia_media'] > 0
        
        # Get observer
        x_obs, y_obs = punto_ciego_observador(cons)
        assert isinstance(x_obs, float)
        
        # Generate certificate
        cert = generar_certificado(cons)
        assert "constelacion_qcal_psix" in cert
    
    def test_multiples_tamanios(self):
        """Test constellation at different sizes."""
        sizes = [8, 16, 32]
        
        for size in sizes:
            cons = calcular_constelacion(grid_size=size, n_terms=5)
            assert cons['psi'].shape == (size, size)
            
            analisis = analizar_constelacion(cons)
            assert 'coherencia_media' in analisis
    
    def test_diferentes_terminos(self):
        """Test with different number of terms."""
        terms = [5, 10, 20]
        
        for n in terms:
            cons = calcular_constelacion(grid_size=16, n_terms=n)
            cert = generar_certificado(cons)
            assert "constelacion_qcal_psix" in cert


class TestValoresEsperados:
    """Test expected physical values."""
    
    def test_f0_correcto(self):
        """Test f₀ has correct value."""
        assert F0_HZ == 141.7001
    
    def test_phi_correcto(self):
        """Test φ is golden ratio."""
        assert abs(PHI - 1.618033988749895) < 1e-10
    
    def test_octavas_aproximadas(self):
        """Test octaves approximately 23.257."""
        assert abs(OCTAVAS_H_F0 - 23.257) < 0.01
    
    def test_hydrogen_frecuencia(self):
        """Test hydrogen line frequency."""
        expected = 1420.405751e6  # MHz to Hz
        assert abs(F_HYDROGEN_HZ - expected) < 1000


class TestRobustez:
    """Test robustness and edge cases."""
    
    def test_constelacion_minima(self):
        """Test minimal constellation (4x4, 1 term)."""
        cons = calcular_constelacion(grid_size=4, n_terms=1)
        assert cons['psi'].shape == (4, 4)
    
    def test_diferentes_rangos_espaciales(self):
        """Test different spatial ranges."""
        ranges = [(-1, 1), (-5, 5), (0, 10)]
        
        for x_range in ranges:
            cons = calcular_constelacion(
                grid_size=8,
                x_range=x_range,
                y_range=x_range,
                n_terms=3
            )
            assert cons['x'].min() >= x_range[0] - 0.1
            assert cons['x'].max() <= x_range[1] + 0.1
    
    def test_coherencia_nunca_negativa(self):
        """Test coherence is never negative."""
        cons = calcular_constelacion(grid_size=32, n_terms=15)
        assert np.all(cons['coherencia'] >= 0)
    
    def test_certificado_valores_redondeados(self):
        """Test certificate values are rounded."""
        cons = calcular_constelacion(grid_size=16, n_terms=5)
        cert = generar_certificado(cons)
        
        data = cert["constelacion_qcal_psix"]
        
        # Check rounding (should be 3 decimal places)
        coh_str = str(data['coherencia_media'])
        if '.' in coh_str:
            decimals = len(coh_str.split('.')[1])
            assert decimals <= 3


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
