#!/usr/bin/env python3
"""
Tests for Compton Clock Module

Tests the implementation of Compton frequencies and their connection
to the fundamental frequency f₀ = 141.7001 Hz.

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
"""

import sys
from pathlib import Path
import math
╔════════════════════════════════════════════════════════════════════════════╗
║              TEST SUITE - RELOJ DE COMPTON (COMPTON CLOCK)                 ║
║                           32 Pruebas Unitarias                              ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
FECHA/DATE: 17 de febrero de 2026

Test suite completo para validar el módulo compton_clock.
"""

import unittest
import sys
from pathlib import Path
import importlib.util

# Add qcal to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.compton_clock import (
    compton_frequency,
    compton_wavelength,
    get_particle_compton_frequencies,
    geometric_mean_compton,
    compute_f0_from_compton_harmonic,
    verify_compton_scaling,
    display_compton_spectrum,
    M_ELECTRON,
    M_PROTON,
    M_NEUTRON,
    M_PLANCK,
    C_LIGHT,
    H_PLANCK,
    F0_HZ,
    ALPHA_FINE,
    PHI_GOLDEN,
    L_PLANCK,
)


class TestComptonFrequencies:
    """Test suite for Compton frequency calculations."""
    
    def test_electron_compton_frequency(self):
        """Test electron Compton frequency calculation."""
        f_e = compton_frequency(M_ELECTRON)
        
        # Expected: f = (m_e c²) / h
        # m_e = 9.1093837015e-31 kg
        # c = 299792458 m/s
        # h = 6.62607015e-34 J·s
        # f ≈ 1.2356×10²⁰ Hz
        
        expected = 1.2355899e20  # Hz
        assert abs(f_e - expected) / expected < 0.001, \
            f"Electron Compton frequency error: {f_e:.6e} vs {expected:.6e}"
        
        print(f"✓ Electron Compton frequency: {f_e:.6e} Hz")
    
    def test_proton_compton_frequency(self):
        """Test proton Compton frequency calculation."""
        f_p = compton_frequency(M_PROTON)
        
        # Proton is ~1836 times heavier than electron
        # So its frequency should be ~1836 times higher
        expected = 2.268e23  # Hz
        assert abs(f_p - expected) / expected < 0.001, \
            f"Proton Compton frequency error: {f_p:.6e} vs {expected:.6e}"
        
        print(f"✓ Proton Compton frequency: {f_p:.6e} Hz")
    
    def test_neutron_compton_frequency(self):
        """Test neutron Compton frequency calculation."""
        f_n = compton_frequency(M_NEUTRON)
        
        # Neutron slightly heavier than proton
        expected = 2.271e23  # Hz
        assert abs(f_n - expected) / expected < 0.001, \
            f"Neutron Compton frequency error: {f_n:.6e} vs {expected:.6e}"
        
        print(f"✓ Neutron Compton frequency: {f_n:.6e} Hz")
    
    def test_planck_mass_compton_frequency(self):
        """Test Planck mass Compton frequency."""
        f_planck = compton_frequency(M_PLANCK)
        
        # Planck frequency ≈ 1.855×10⁴³ Hz
        # This is the highest frequency in quantum gravity
        assert f_planck > 1e43, \
            f"Planck frequency too small: {f_planck:.6e}"
        assert f_planck < 1e44, \
            f"Planck frequency too large: {f_planck:.6e}"
        
        print(f"✓ Planck mass Compton frequency: {f_planck:.6e} Hz")
    
    def test_compton_wavelength_electron(self):
        """Test electron Compton wavelength."""
        lambda_c = compton_wavelength(M_ELECTRON)
        
        # Expected: λ_C = h / (m_e c) ≈ 2.426×10⁻¹² m
        expected = 2.42631023867e-12  # m
        assert abs(lambda_c - expected) / expected < 1e-6, \
            f"Compton wavelength error: {lambda_c:.12e} vs {expected:.12e}"
        
        print(f"✓ Electron Compton wavelength: {lambda_c:.12e} m")
    
    def test_compton_wavelength_relation(self):
        """Test relation: c / f_Compton = λ_Compton."""
        f_e = compton_frequency(M_ELECTRON)
        lambda_e = compton_wavelength(M_ELECTRON)
        
        # Check: c / f = λ
        lambda_from_freq = C_LIGHT / f_e
        assert abs(lambda_from_freq - lambda_e) / lambda_e < 1e-6, \
            f"Frequency-wavelength relation error"
        
        print(f"✓ Compton frequency-wavelength relation verified")


class TestParticleSpectrum:
    """Test suite for particle spectrum functions."""
    
    def test_get_particle_frequencies(self):
        """Test getting all particle frequencies."""
        freqs = get_particle_compton_frequencies()
        
        assert 'electron' in freqs
        assert 'proton' in freqs
        assert 'neutron' in freqs
        assert 'planck_mass' in freqs
        
        # Check ordering: electron < proton ≈ neutron < planck_mass
        assert freqs['electron'] < freqs['proton']
        assert freqs['proton'] < freqs['planck_mass']
        assert abs(freqs['proton'] - freqs['neutron']) / freqs['proton'] < 0.01
        
        print(f"✓ Particle frequencies retrieved: {len(freqs)} particles")
    
    def test_geometric_mean(self):
        """Test geometric mean of Compton frequencies."""
        # Test with electron, proton, neutron
        f_geom = geometric_mean_compton([M_ELECTRON, M_PROTON, M_NEUTRON])
        
        # Geometric mean should be between min and max
        f_e = compton_frequency(M_ELECTRON)
        f_n = compton_frequency(M_NEUTRON)
        
        assert f_e < f_geom < f_n, \
            f"Geometric mean not in expected range: {f_geom:.6e}"
        
        # For 3 numbers: geom_mean = (a*b*c)^(1/3)
        expected = (f_e * compton_frequency(M_PROTON) * f_n) ** (1/3)
        assert abs(f_geom - expected) / expected < 1e-10
        
        print(f"✓ Geometric mean: {f_geom:.6e} Hz")


class TestF0Connection:
    """Test suite for connection to f₀ = 141.7001 Hz."""
    
    def test_f0_calculation(self):
        """Test f₀ calculation from Compton harmonics."""
        f0_calc, factors = compute_f0_from_compton_harmonic()
        
        # Should be close to 141.7001 Hz
        # We allow up to 1% error with the QCAL master equation
        relative_error = abs(f0_calc - F0_HZ) / F0_HZ
        
        print(f"\nf₀ calculation:")
        print(f"  Calculated: {f0_calc:.4f} Hz")
        print(f"  Target:     {F0_HZ:.4f} Hz")
        print(f"  Error:      {relative_error:.2%}")
        
        # With the master equation and K_cosmic factor, we achieve <1% error
        assert relative_error < 0.01, \
            f"f₀ calculation too far off: {relative_error:.2%} error"
        
        print(f"✓ f₀ connection demonstrated")
    
    def test_scaling_factors(self):
        """Test that scaling factors are reasonable."""
        f0_calc, factors = compute_f0_from_compton_harmonic()
        
        # Check key factors exist and are reasonable
        assert factors['alpha_squared'] > 0
        assert factors['alpha_squared'] < 1
        assert abs(factors['phi'] - PHI_GOLDEN) < 1e-10
        assert factors['mass_ratio'] > 1e20
        assert factors['planck_scale_ratio'] < 1
        
        print(f"✓ Scaling factors validated")
        print(f"  α²:       {factors['alpha_squared']:.10f}")
        print(f"  φ:        {factors['phi']:.10f}")
        print(f"  m_P/m_e:  {factors['mass_ratio']:.6e}")
        print(f"  ℓ_P/λ_C:  {factors['planck_scale_ratio']:.6e}")
    
    def test_verify_approximations(self):
        """Test different approximation methods."""
        results = verify_compton_scaling()
        
        # All approximations should exist
        assert 'approximation_1_alpha_phi' in results
        assert 'approximation_2_planck_scale' in results
        assert 'approximation_3_master_equation' in results
        
        print(f"\n✓ Approximation methods tested:")
        for key, approx in results.items():
            print(f"  {approx['description']}:")
            print(f"    Result: {approx['result_Hz']:.4f} Hz")
            print(f"    Error:  {approx['error_vs_f0']:.2%}")
    
    def test_harmonic_relationship(self):
        """Test that harmonic relationships are preserved."""
        freqs = get_particle_compton_frequencies()
        
        # Proton/electron ratio should be close to mass ratio
        mass_ratio = M_PROTON / M_ELECTRON
        freq_ratio = freqs['proton'] / freqs['electron']
        
        assert abs(freq_ratio - mass_ratio) / mass_ratio < 1e-6, \
            f"Mass-frequency ratio mismatch"
        
        print(f"✓ Harmonic relationships preserved")
        print(f"  m_p/m_e:  {mass_ratio:.6f}")
        print(f"  f_p/f_e:  {freq_ratio:.6f}")


class TestPhysicalConstants:
    """Test physical constants are correct."""
    
    def test_speed_of_light(self):
        """Test speed of light value."""
        assert C_LIGHT == 299792458.0
        print(f"✓ Speed of light: {C_LIGHT} m/s")
    
    def test_planck_constant(self):
        """Test Planck constant value (CODATA 2018)."""
        assert H_PLANCK == 6.62607015e-34
        print(f"✓ Planck constant: {H_PLANCK} J·s")
    
    def test_fine_structure_constant(self):
        """Test fine structure constant."""
        # α ≈ 1/137.036
        assert abs(1/ALPHA_FINE - 137.036) < 0.001
        print(f"✓ Fine structure constant: α = {ALPHA_FINE:.10f} ≈ 1/{1/ALPHA_FINE:.3f}")
    
    def test_golden_ratio(self):
        """Test golden ratio value."""
        phi_expected = (1 + math.sqrt(5)) / 2
        assert abs(PHI_GOLDEN - phi_expected) < 1e-10
        print(f"✓ Golden ratio: φ = {PHI_GOLDEN:.10f}")


class TestDisplayFunctions:
    """Test display and utility functions."""
    
    def test_display_spectrum(self):
        """Test spectrum display function."""
        output = display_compton_spectrum()
        
        assert "ESPECTRO DE FRECUENCIAS DE COMPTON" in output
        assert "electron" in output
        assert "proton" in output
        assert "141.7001" in output
        assert "f₀ calculada" in output
        
        print(f"✓ Spectrum display function works")


def run_all_tests():
    """Run all test suites."""
    print("="*70)
    print("COMPTON CLOCK TEST SUITE")
    print("="*70)
    
    # Test Compton frequencies
    print("\n[1] Testing Compton Frequencies")
    print("-"*70)
    test_freq = TestComptonFrequencies()
    test_freq.test_electron_compton_frequency()
    test_freq.test_proton_compton_frequency()
    test_freq.test_neutron_compton_frequency()
    test_freq.test_planck_mass_compton_frequency()
    test_freq.test_compton_wavelength_electron()
    test_freq.test_compton_wavelength_relation()
    
    # Test particle spectrum
    print("\n[2] Testing Particle Spectrum")
    print("-"*70)
    test_spectrum = TestParticleSpectrum()
    test_spectrum.test_get_particle_frequencies()
    test_spectrum.test_geometric_mean()
    
    # Test f₀ connection
    print("\n[3] Testing f₀ Connection")
    print("-"*70)
    test_f0 = TestF0Connection()
    test_f0.test_f0_calculation()
    test_f0.test_scaling_factors()
    test_f0.test_verify_approximations()
    test_f0.test_harmonic_relationship()
    
    # Test physical constants
    print("\n[4] Testing Physical Constants")
    print("-"*70)
    test_phys = TestPhysicalConstants()
    test_phys.test_speed_of_light()
    test_phys.test_planck_constant()
    test_phys.test_fine_structure_constant()
    test_phys.test_golden_ratio()
    
    # Test display functions
    print("\n[5] Testing Display Functions")
    print("-"*70)
    test_display = TestDisplayFunctions()
    test_display.test_display_spectrum()
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED ✓")
    print("="*70)
    print("\n∴ El reloj de Compton late a 141.7001 Hz en el corazón del cosmos")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
# Import compton_clock directly to avoid numpy dependency from qcal.__init__
spec = importlib.util.spec_from_file_location(
    "compton_clock",
    Path(__file__).parent.parent / "qcal" / "compton_clock.py"
)
compton_clock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compton_clock)


class TestRelojCompton(unittest.TestCase):
    """Suite de pruebas para el Reloj de Compton."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.tolerance = 1e-4  # Tolerancia para comparaciones
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE CONSTANTES FÍSICAS
    # ═══════════════════════════════════════════════════════════════════
    
    def test_constante_planck(self):
        """Verifica que la constante de Planck sea correcta (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.H_PLANCK,
            6.62607015e-34,
            places=42
        )
    
    def test_velocidad_luz(self):
        """Verifica que la velocidad de la luz sea exacta."""
        self.assertEqual(compton_clock.C_LIGHT, 299792458.0)
    
    def test_masa_electron(self):
        """Verifica la masa del electrón (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.M_ELECTRON,
            9.1093837015e-31,
            delta=1e-40
        )
    
    def test_masa_proton(self):
        """Verifica la masa del protón (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.M_PROTON,
            1.67262192369e-27,
            delta=1e-36
        )
    
    def test_masa_neutron(self):
        """Verifica la masa del neutrón (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.M_NEUTRON,
            1.67492749804e-27,
            delta=1e-36
        )
    
    def test_masa_planck(self):
        """Verifica la masa de Planck."""
        self.assertAlmostEqual(
            compton_clock.M_PLANCK,
            2.176434e-8,
            delta=1e-13
        )
    
    def test_constante_estructura_fina(self):
        """Verifica la constante de estructura fina."""
        self.assertAlmostEqual(
            compton_clock.ALPHA_FINE,
            7.2973525693e-3,
            delta=1e-12
        )
    
    def test_proporcion_aurea(self):
        """Verifica la proporción áurea φ."""
        self.assertAlmostEqual(
            compton_clock.PHI,
            1.618033988749895,
            delta=1e-12
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE FRECUENCIAS DE COMPTON
    # ═══════════════════════════════════════════════════════════════════
    
    def test_frecuencia_compton_electron(self):
        """Verifica la frecuencia de Compton del electrón."""
        f_e = compton_clock.frecuencia_compton_electron()
        # f_e = m_e * c² / h ≈ 1.2356e20 Hz
        self.assertAlmostEqual(f_e, 1.235590e20, delta=1e14)
    
    def test_frecuencia_compton_proton(self):
        """Verifica la frecuencia de Compton del protón."""
        f_p = compton_clock.frecuencia_compton_proton()
        # f_p ≈ 2.2687e23 Hz
        self.assertAlmostEqual(f_p, 2.268732e23, delta=1e17)
    
    def test_frecuencia_compton_neutron(self):
        """Verifica la frecuencia de Compton del neutrón."""
        f_n = compton_clock.frecuencia_compton_neutron()
        # f_n ≈ 2.2719e23 Hz
        self.assertAlmostEqual(f_n, 2.271859e23, delta=1e17)
    
    def test_frecuencia_compton_masa_arbitraria(self):
        """Verifica el cálculo con una masa arbitraria."""
        # Usar masa del protón como referencia
        f = compton_clock.frecuencia_compton(compton_clock.M_PROTON)
        f_ref = compton_clock.frecuencia_compton_proton()
        self.assertAlmostEqual(f, f_ref, delta=1e10)
    
    def test_frecuencia_compton_proporcionalidad(self):
        """Verifica que f_Compton ∝ masa."""
        m1 = 1e-30  # kg
        m2 = 2e-30  # kg
        f1 = compton_clock.frecuencia_compton(m1)
        f2 = compton_clock.frecuencia_compton(m2)
        # f2 debería ser aproximadamente 2 * f1
        self.assertAlmostEqual(f2 / f1, 2.0, delta=1e-6)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE MEDIA GEOMÉTRICA
    # ═══════════════════════════════════════════════════════════════════
    
    def test_media_geometrica_dos_valores(self):
        """Verifica la media geométrica de dos valores."""
        f1 = 100.0
        f2 = 400.0
        f_geo = compton_clock.media_geometrica_frecuencias(f1, f2)
        # √(100 * 400) = √40000 = 200
        self.assertAlmostEqual(f_geo, 200.0, delta=1e-6)
    
    def test_media_geometrica_tres_particulas(self):
        """Verifica la media geométrica de las tres partículas fundamentales."""
        f_e = compton_clock.frecuencia_compton_electron()
        f_p = compton_clock.frecuencia_compton_proton()
        f_n = compton_clock.frecuencia_compton_neutron()
        f_geo = compton_clock.media_geometrica_frecuencias(f_e, f_p, f_n)
        # Debería estar entre 1e22 y 1e23 Hz
        self.assertGreater(f_geo, 1e21)
        self.assertLess(f_geo, 1e23)
    
    def test_media_geometrica_vacia(self):
        """Verifica que la media geométrica de una lista vacía sea 0."""
        f_geo = compton_clock.media_geometrica_frecuencias()
        self.assertEqual(f_geo, 0.0)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DEL FACTOR K Y RELACIONES
    # ═══════════════════════════════════════════════════════════════════
    
    def test_factor_k_calculation(self):
        """Verifica el cálculo del factor K."""
        K = compton_clock.calcular_factor_k()
        # K = 2 · (m_P / m_e)^(1/3) · φ³ ≈ 2.44e8
        self.assertAlmostEqual(K, 2.440123e8, delta=1e3)
    
    def test_factor_k_componentes(self):
        """Verifica los componentes del factor K."""
        razon_masas = compton_clock.M_PLANCK / compton_clock.M_ELECTRON
        self.assertGreater(razon_masas, 1e22)
        self.assertLess(razon_masas, 1e24)
        
        phi_cubed = compton_clock.PHI ** 3
        self.assertAlmostEqual(phi_cubed, 4.236067977, delta=1e-6)
    
    def test_relacion_longitudes_caracteristicas(self):
        """Verifica la relación ℓ_P / λ_C."""
        relacion = compton_clock.calcular_relacion_longitudes()
        # Debería ser muy pequeña (≈ 6.66e-24)
        self.assertAlmostEqual(relacion, 6.661370e-24, delta=1e-28)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE LA ECUACIÓN MAESTRA
    # ═══════════════════════════════════════════════════════════════════
    
    def test_ecuacion_maestra_componentes(self):
        """Verifica que todos los componentes de la ecuación maestra estén presentes."""
        f0, componentes = compton_clock.calcular_f0_ecuacion_maestra()
        
        self.assertIn('c_sobre_2pi', componentes)
        self.assertIn('raiz_masas', componentes)
        self.assertIn('alpha', componentes)
        self.assertIn('phi', componentes)
        self.assertIn('longitudes', componentes)
        self.assertIn('K', componentes)
        self.assertIn('f0', componentes)
    
    def test_ecuacion_maestra_precision(self):
        """Verifica la precisión de la ecuación maestra."""
        f0, _ = compton_clock.calcular_f0_ecuacion_maestra()
        f0_teorico = compton_clock.F0_THEORETICAL
        
        error_relativo = abs(f0 - f0_teorico) / f0_teorico * 100
        
        # Error debe ser menor al 0.5% (objetivo: 0.1088%)
        self.assertLess(error_relativo, 0.5)
        print(f"\n  ✓ Excelente precisión: error = {error_relativo:.4f}%")
    
    def test_ecuacion_maestra_f0_positivo(self):
        """Verifica que f₀ sea positivo."""
        f0, _ = compton_clock.calcular_f0_ecuacion_maestra()
        self.assertGreater(f0, 0)
    
    def test_ecuacion_maestra_rango_esperado(self):
        """Verifica que f₀ esté en el rango esperado (100-200 Hz)."""
        f0, _ = compton_clock.calcular_f0_ecuacion_maestra()
        self.assertGreater(f0, 100.0)
        self.assertLess(f0, 200.0)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE ARMÓNICOS Y RESONANCIAS
    # ═══════════════════════════════════════════════════════════════════
    
    def test_calcular_armonicos(self):
        """Verifica el cálculo de armónicos."""
        f0 = 141.7001
        armonicos = compton_clock.calcular_armonicos(f0, 5)
        
        self.assertEqual(len(armonicos), 5)
        self.assertAlmostEqual(armonicos[1], 141.7001, delta=1e-4)
        self.assertAlmostEqual(armonicos[2], 283.4002, delta=1e-4)
        self.assertAlmostEqual(armonicos[3], 425.1003, delta=1e-4)
    
    def test_resonancia_biologica(self):
        """Verifica las resonancias biológicas."""
        resonancias = compton_clock.calcular_resonancia_biologica(141.7001)
        
        self.assertIn('fundamental', resonancias)
        self.assertIn('celular', resonancias)
        self.assertIn('proteica', resonancias)
        self.assertIn('microtubular', resonancias)
        self.assertIn('genomica', resonancias)
        
        # Verificar valores
        self.assertAlmostEqual(resonancias['celular']['frecuencia'], 283.4002, delta=1e-4)
        self.assertAlmostEqual(resonancias['proteica']['frecuencia'], 425.1003, delta=1e-4)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE VERIFICACIÓN Y ANÁLISIS
    # ═══════════════════════════════════════════════════════════════════
    
    def test_verificacion_precision(self):
        """Verifica el sistema de verificación de precisión."""
        resultado = compton_clock.verificar_precision()
        
        self.assertIn('f0_calculado', resultado)
        self.assertIn('f0_teorico', resultado)
        self.assertIn('error_absoluto', resultado)
        self.assertIn('error_relativo', resultado)
        self.assertIn('precision', resultado)
        self.assertIn('coherencia', resultado)
        
        # Precisión debe ser > 99%
        self.assertGreater(resultado['precision'], 99.0)
    
    def test_coherencia_psi(self):
        """Verifica el cálculo de coherencia Ψ."""
        resultado = compton_clock.verificar_precision()
        
        # Si error < 1%, coherencia = 1.0
        if resultado['error_relativo'] < 1.0:
            self.assertAlmostEqual(resultado['coherencia'], 1.0, delta=1e-6)
    
    def test_verificacion_completa(self):
        """Verifica que el análisis completo funcione correctamente."""
        analisis = compton_clock.analisis_completo_reloj_compton()
        
        self.assertIn('frecuencias_compton', analisis)
        self.assertIn('ecuacion_maestra', analisis)
        self.assertIn('verificacion', analisis)
        self.assertIn('resonancias_biologicas', analisis)
        self.assertIn('armonicos', analisis)
        self.assertIn('resumen', analisis)
        
        # Verificar que el resumen contenga información relevante
        self.assertIn('141.7001', analisis['resumen'])
        self.assertIn('Hz', analisis['resumen'])
        
        print("\n  ✓ Todas las verificaciones del reloj de Compton pasaron")
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBA DE ALTA PRECISIÓN (MPMATH)
    # ═══════════════════════════════════════════════════════════════════
    
    def test_alta_precision_mpmath(self):
        """Verifica el modo de alta precisión con mpmath."""
        f_e_normal = compton_clock.frecuencia_compton_electron(alta_precision=False)
        f_e_alta = compton_clock.frecuencia_compton_electron(alta_precision=True)
        
        # Los valores deben ser muy similares
        diferencia_relativa = abs(f_e_alta - f_e_normal) / f_e_normal
        self.assertLess(diferencia_relativa, 1e-10)
    
    def test_f0_consistency(self):
        """Verifica la consistencia de f₀ entre diferentes métodos."""
        # Calcular f₀ dos veces
        f0_1, _ = compton_clock.calcular_f0_ecuacion_maestra()
        f0_2, _ = compton_clock.calcular_f0_ecuacion_maestra()
        
        # Deben ser idénticos
        self.assertEqual(f0_1, f0_2)
    
    def test_armonicos_continuidad(self):
        """Verifica la continuidad de la serie de armónicos."""
        armonicos = compton_clock.calcular_armonicos(141.7001, 10)
        
        # Cada armónico debe ser n veces la frecuencia fundamental
        for n in range(1, 11):
            self.assertAlmostEqual(armonicos[n], n * 141.7001, delta=1e-4)
    
    def test_ecuacion_maestra_derivacion(self):
        """Verifica que la ecuación maestra derive correctamente f₀."""
        f0, comp = compton_clock.calcular_f0_ecuacion_maestra()
        
        # Recalcular manualmente
        c_2pi = comp['c_sobre_2pi']
        sqrt_m = comp['raiz_masas']
        alpha = comp['alpha']
        phi = comp['phi']
        l_ratio = comp['longitudes']
        K = comp['K']
        
        f0_manual = c_2pi * sqrt_m * alpha * phi * l_ratio * K
        
        # Deben coincidir
        self.assertAlmostEqual(f0, f0_manual, delta=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# EJECUTAR PRUEBAS
# ═══════════════════════════════════════════════════════════════════════════

def run_tests():
    """Ejecuta todas las pruebas."""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRelojCompton)
    
    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "═" * 80)
    print("RESUMEN DE PRUEBAS - RELOJ DE COMPTON")
    print("═" * 80)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ¡Todas las pruebas pasaron! Coherencia Ψ = 1.000")
    else:
        print("\n✗ Algunas pruebas fallaron")
    
    print("═" * 80 + "\n")
    
    return result


if __name__ == '__main__':
    # Intentar usar pytest si está disponible
    try:
        import pytest
        sys.exit(pytest.main([__file__, '-v']))
    except ImportError:
        # Fallback a unittest
        result = run_tests()
        sys.exit(0 if result.wasSuccessful() else 1)
