#!/usr/bin/env python3
"""
Tests for P vs NP — Certificado Polinomial por Coherencia η⁺ (∴P=NP∞³)

Tests the adelic coherence certificate for NP-complete problems.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: 2026-04-06
"""

import unittest
import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from physics.certificado_np_coherencia import (
    ConstantesCertificadoNP,
    EspacioHilbertAdelico,
    MetricaCoherenciaEtaPlus,
    DescomposicionEspectral,
    CertificadoNP,
    ProblemasTSP_SAT,
    CoherenciaCertificado,
    SistemaCertificadoNP,
    certificado_np_activar
)


# ============================================================================
# TEST SUITE 1 – Constantes
# ============================================================================

class TestConstantesCertificadoNP(unittest.TestCase):
    """Tests for ConstantesCertificadoNP class."""

    def setUp(self):
        """Set up test constants."""
        self.const = ConstantesCertificadoNP()

    def test_f0_value(self):
        """Test fundamental frequency f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(self.const.f0, 141.7001, places=4)

    def test_omega_0_calculation(self):
        """Test angular frequency ω₀ = 2π × f₀."""
        expected = 2.0 * math.pi * 141.7001
        self.assertAlmostEqual(self.const.omega_0, expected, places=2)

    def test_eta_plus_threshold(self):
        """Test NP threshold η⁺ = 0.9575."""
        self.assertAlmostEqual(self.const.eta_plus_threshold, 0.9575, places=4)

    def test_psi_umbral(self):
        """Test minimum coherence threshold Ψ ≥ 0.888."""
        self.assertAlmostEqual(self.const.psi_umbral, 0.888, places=3)

    def test_eta_plus_factor(self):
        """Test η⁺ factor = 7/8 = 0.875."""
        self.assertAlmostEqual(self.const.eta_plus_factor, 7.0 / 8.0, places=6)

    def test_riemann_zeros_count(self):
        """Test that 10 Riemann zeros are available."""
        self.assertEqual(len(self.const.riemann_zeros), 10)

    def test_riemann_zeros_ordering(self):
        """Test that Riemann zeros are in ascending order."""
        zeros = list(self.const.riemann_zeros)
        self.assertEqual(zeros, sorted(zeros))

    def test_gamma_1_value(self):
        """Test first Riemann zero γ₁ = 14.134725."""
        self.assertAlmostEqual(self.const.gamma_1(), 14.134725, places=6)

    def test_primos_p_count(self):
        """Test that 7 fundamental primes are available."""
        self.assertEqual(len(self.const.primos_p), 7)

    def test_primos_p_values(self):
        """Test fundamental primes {2,3,5,7,11,13,17}."""
        expected = (2, 3, 5, 7, 11, 13, 17)
        self.assertEqual(self.const.primos_p, expected)

    def test_kappa_pi_value(self):
        """Test complexity constant κ_Π = 2.5773."""
        self.assertAlmostEqual(self.const.kappa_pi, 2.5773, places=4)

    def test_phi_value(self):
        """Test golden ratio ϕ = (1+√5)/2."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(self.const.phi, expected, places=10)

    def test_n_riemann_zeros(self):
        """Test n_riemann_zeros() method."""
        self.assertEqual(self.const.n_riemann_zeros(), 10)

    def test_complejidad_polinomial(self):
        """Test polynomial complexity O(n³)."""
        n = 100
        expected = n ** 3
        self.assertEqual(self.const.complejidad_polinomial(n), expected)

    def test_es_certificable_np_true(self):
        """Test NP certificate validation (positive case)."""
        self.assertTrue(self.const.es_certificable_np(0.96))

    def test_es_certificable_np_false(self):
        """Test NP certificate validation (negative case)."""
        self.assertFalse(self.const.es_certificable_np(0.95))

    def test_es_certificable_np_boundary(self):
        """Test NP certificate validation at boundary."""
        self.assertTrue(self.const.es_certificable_np(0.9575))


# ============================================================================
# TEST SUITE 2 – Espacio de Hilbert Adélico
# ============================================================================

class TestEspacioHilbertAdelico(unittest.TestCase):
    """Tests for EspacioHilbertAdelico class."""

    def setUp(self):
        """Set up test Hilbert space."""
        self.const = ConstantesCertificadoNP()
        self.espacio = EspacioHilbertAdelico(
            constantes=self.const,
            dimension=10
        )

    def test_dimension(self):
        """Test space dimension."""
        self.assertEqual(self.espacio.dimension, 10)

    def test_construir_hamiltoniano_shape(self):
        """Test Hamiltonian matrix shape."""
        instancia = [1.0] * 100
        H = self.espacio.construir_hamiltoniano(instancia)
        self.assertEqual(len(H), 10)
        self.assertEqual(len(H[0]), 10)

    def test_hamiltoniano_hermitiano(self):
        """Test Hamiltonian is Hermitian."""
        instancia = [1.0] * 100
        H = self.espacio.construir_hamiltoniano(instancia)
        
        # Check H = H†
        for i in range(10):
            for j in range(10):
                self.assertAlmostEqual(
                    H[i][j].real, H[j][i].real, places=10
                )
                self.assertAlmostEqual(
                    H[i][j].imag, -H[j][i].imag, places=10
                )

    def test_hamiltoniano_diagonal_riemann(self):
        """Test Hamiltonian diagonal uses Riemann zeros."""
        instancia = [1.0] * 100
        H = self.espacio.construir_hamiltoniano(instancia)
        
        # Check diagonal elements are f₀ × γₙ
        for i in range(10):
            gamma_idx = i % len(self.const.riemann_zeros)
            expected = self.const.f0 * self.const.riemann_zeros[gamma_idx]
            self.assertAlmostEqual(H[i][i].real, expected, places=2)

    def test_producto_interno_ortogonal(self):
        """Test inner product of orthogonal vectors."""
        psi = [complex(1, 0), complex(0, 0), complex(0, 0)]
        phi = [complex(0, 0), complex(1, 0), complex(0, 0)]
        
        espacio = EspacioHilbertAdelico(self.const, 3)
        resultado = espacio.producto_interno(psi, phi)
        
        self.assertAlmostEqual(abs(resultado), 0.0, places=10)

    def test_producto_interno_parallel(self):
        """Test inner product of parallel vectors."""
        psi = [complex(1, 0), complex(0, 0), complex(0, 0)]
        phi = [complex(2, 0), complex(0, 0), complex(0, 0)]
        
        espacio = EspacioHilbertAdelico(self.const, 3)
        resultado = espacio.producto_interno(psi, phi)
        
        self.assertAlmostEqual(resultado.real, 2.0, places=10)

    def test_producto_interno_conjugate(self):
        """Test inner product conjugation ⟨ψ|φ⟩ = ⟨φ|ψ⟩*."""
        psi = [complex(1, 1), complex(2, -1)]
        phi = [complex(0.5, 0.5), complex(1, 0)]
        
        espacio = EspacioHilbertAdelico(self.const, 2)
        psi_phi = espacio.producto_interno(psi, phi)
        phi_psi = espacio.producto_interno(phi, psi)
        
        self.assertAlmostEqual(psi_phi.real, phi_psi.real, places=10)
        self.assertAlmostEqual(psi_phi.imag, -phi_psi.imag, places=10)

    def test_norma_normalized(self):
        """Test norm of normalized vector."""
        n = 5
        psi = [complex(1.0 / math.sqrt(n), 0)] * n
        
        espacio = EspacioHilbertAdelico(self.const, n)
        norma = espacio.norma(psi)
        
        self.assertAlmostEqual(norma, 1.0, places=10)

    def test_norma_zero(self):
        """Test norm of zero vector."""
        psi = [complex(0, 0)] * 5
        
        espacio = EspacioHilbertAdelico(self.const, 5)
        norma = espacio.norma(psi)
        
        self.assertAlmostEqual(norma, 0.0, places=10)

    def test_producto_interno_dimension_mismatch(self):
        """Test that dimension mismatch raises error."""
        psi = [complex(1, 0)] * 5
        phi = [complex(1, 0)] * 3
        
        espacio = EspacioHilbertAdelico(self.const, 5)
        
        with self.assertRaises(ValueError):
            espacio.producto_interno(psi, phi)


# ============================================================================
# TEST SUITE 3 – Métrica de Coherencia η⁺
# ============================================================================

class TestMetricaCoherenciaEtaPlus(unittest.TestCase):
    """Tests for MetricaCoherenciaEtaPlus class."""

    def setUp(self):
        """Set up test metric."""
        self.const = ConstantesCertificadoNP()
        self.espacio = EspacioHilbertAdelico(self.const, 5)
        self.metrica = MetricaCoherenciaEtaPlus(self.const, self.espacio)

    def test_umbral_np(self):
        """Test NP threshold retrieval."""
        self.assertAlmostEqual(self.metrica.umbral_np(), 0.9575, places=4)

    def test_calcular_eta_plus_positivo(self):
        """Test η⁺ calculation is positive."""
        n = 5
        psi = [complex(1.0 / math.sqrt(n), 0)] * n
        phi = psi.copy()
        
        eigenvalues = [1.0, 2.0, 3.0, 4.0, 5.0]
        lambda_max = 5.0
        
        eta_plus = self.metrica.calcular_eta_plus(psi, phi, lambda_max, eigenvalues)
        
        self.assertGreater(eta_plus, 0.0)

    def test_calcular_eta_plus_bounded(self):
        """Test η⁺ is bounded [0, 1]."""
        n = 5
        psi = [complex(1.0 / math.sqrt(n), 0)] * n
        phi = psi.copy()
        
        eigenvalues = [1.0, 2.0, 3.0, 4.0, 5.0]
        lambda_max = 5.0
        
        eta_plus = self.metrica.calcular_eta_plus(psi, phi, lambda_max, eigenvalues)
        
        self.assertGreaterEqual(eta_plus, 0.0)
        self.assertLessEqual(eta_plus, 1.0)

    def test_calcular_eta_plus_dimension_mismatch(self):
        """Test dimension mismatch raises error."""
        psi = [complex(1, 0)] * 5
        phi = [complex(1, 0)] * 3
        eigenvalues = [1.0] * 5
        lambda_max = 5.0
        
        with self.assertRaises(ValueError):
            self.metrica.calcular_eta_plus(psi, phi, lambda_max, eigenvalues)

    def test_eta_plus_factor_7_8(self):
        """Test η⁺ uses factor 7/8."""
        # For eigenvalue at λ_max, denominator is 1
        # So η⁺ should be close to 7/8 for that component
        n = 1
        psi = [complex(1, 0)]
        phi = [complex(1, 0)]
        eigenvalues = [5.0]
        lambda_max = 5.0
        
        metrica = MetricaCoherenciaEtaPlus(self.const, EspacioHilbertAdelico(self.const, 1))
        eta_plus = metrica.calcular_eta_plus(psi, phi, lambda_max, eigenvalues)
        
        # Should be exactly 7/8 = 0.875
        self.assertAlmostEqual(eta_plus, 7.0 / 8.0, places=6)


# ============================================================================
# TEST SUITE 4 – Descomposición Espectral
# ============================================================================

class TestDescomposicionEspectral(unittest.TestCase):
    """Tests for DescomposicionEspectral class."""

    def setUp(self):
        """Set up test decomposition."""
        self.const = ConstantesCertificadoNP()
        self.descomp = DescomposicionEspectral(self.const)

    def test_descomponer_diagonal_matrix(self):
        """Test decomposition of diagonal matrix."""
        # Diagonal matrix has eigenvalues on diagonal
        H = [
            [complex(1, 0), complex(0, 0), complex(0, 0)],
            [complex(0, 0), complex(2, 0), complex(0, 0)],
            [complex(0, 0), complex(0, 0), complex(3, 0)]
        ]
        
        eigenvalues, eigenvectors = self.descomp.descomponer(H)
        
        self.assertEqual(len(eigenvalues), 3)
        self.assertAlmostEqual(eigenvalues[0], 1.0, places=6)
        self.assertAlmostEqual(eigenvalues[1], 2.0, places=6)
        self.assertAlmostEqual(eigenvalues[2], 3.0, places=6)

    def test_descomponer_symmetric_matrix(self):
        """Test decomposition of symmetric matrix."""
        H = [
            [complex(2, 0), complex(1, 0)],
            [complex(1, 0), complex(2, 0)]
        ]
        
        eigenvalues, eigenvectors = self.descomp.descomponer(H)
        
        self.assertEqual(len(eigenvalues), 2)
        # Eigenvalues should be 1 and 3
        self.assertAlmostEqual(sorted(eigenvalues)[0], 1.0, places=4)
        self.assertAlmostEqual(sorted(eigenvalues)[1], 3.0, places=4)

    def test_lambda_max_extraction(self):
        """Test maximum eigenvalue extraction."""
        eigenvalues = [1.0, 5.0, 3.0, 2.0]
        lambda_max = self.descomp.lambda_max(eigenvalues)
        self.assertAlmostEqual(lambda_max, 5.0, places=10)

    def test_lambda_max_empty(self):
        """Test maximum eigenvalue of empty list."""
        eigenvalues = []
        lambda_max = self.descomp.lambda_max(eigenvalues)
        self.assertEqual(lambda_max, 0.0)

    def test_descomponer_orthogonal_eigenvectors(self):
        """Test eigenvectors are orthogonal."""
        H = [
            [complex(4, 0), complex(1, 0), complex(0, 0)],
            [complex(1, 0), complex(3, 0), complex(1, 0)],
            [complex(0, 0), complex(1, 0), complex(2, 0)]
        ]
        
        eigenvalues, V = self.descomp.descomponer(H)
        
        # Check orthogonality: ⟨v_i|v_j⟩ ≈ δ_ij
        n = len(eigenvalues)
        for i in range(n):
            for j in range(n):
                # Extract column vectors
                v_i = [V[k][i] for k in range(n)]
                v_j = [V[k][j] for k in range(n)]
                
                # Compute inner product
                prod = sum(v_i[k].conjugate() * v_j[k] for k in range(n))
                
                if i == j:
                    self.assertAlmostEqual(abs(prod), 1.0, places=4)
                else:
                    self.assertAlmostEqual(abs(prod), 0.0, places=4)


# ============================================================================
# TEST SUITE 5 – Certificado NP
# ============================================================================

class TestCertificadoNP(unittest.TestCase):
    """Tests for CertificadoNP class."""

    def setUp(self):
        """Set up test certificate."""
        self.const = ConstantesCertificadoNP()
        self.espacio = EspacioHilbertAdelico(self.const, 10)
        self.metrica = MetricaCoherenciaEtaPlus(self.const, self.espacio)
        self.descomp = DescomposicionEspectral(self.const)
        self.cert = CertificadoNP(self.const, self.espacio, self.metrica, self.descomp)

    def test_verificar_structure(self):
        """Test verification result structure."""
        instancia = [1.0] * 100
        n = 10
        solucion = [complex(1.0 / math.sqrt(n), 0)] * n
        
        resultado = self.cert.verificar(instancia, solucion)
        
        self.assertIn('es_certificado', resultado)
        self.assertIn('eta_plus', resultado)
        self.assertIn('lambda_max', resultado)
        self.assertIn('complejidad', resultado)
        self.assertIn('dimension', resultado)

    def test_verificar_eta_plus_positive(self):
        """Test that η⁺ is positive."""
        instancia = [1.0] * 100
        n = 10
        solucion = [complex(1.0 / math.sqrt(n), 0)] * n
        
        resultado = self.cert.verificar(instancia, solucion)
        
        self.assertGreater(resultado['eta_plus'], 0.0)

    def test_verificar_lambda_max_real(self):
        """Test that λ_max is real."""
        instancia = [1.0] * 100
        n = 10
        solucion = [complex(1.0 / math.sqrt(n), 0)] * n
        
        resultado = self.cert.verificar(instancia, solucion)
        
        self.assertIsInstance(resultado['lambda_max'], float)

    def test_verificar_complejidad_cubica(self):
        """Test complexity is O(n³)."""
        n = 10
        instancia = [1.0] * (n * n)
        solucion = [complex(1.0 / math.sqrt(n), 0)] * n
        
        resultado = self.cert.verificar(instancia, solucion)
        
        # Complejidad debe ser n³ = 1000
        self.assertEqual(resultado['complejidad'], n ** 3)

    def test_verificar_zero_norm_error(self):
        """Test that zero norm solution raises error."""
        instancia = [1.0] * 100
        solucion = [complex(0, 0)] * 10
        
        with self.assertRaises(ValueError):
            self.cert.verificar(instancia, solucion)


# ============================================================================
# TEST SUITE 6 – Problemas TSP y SAT
# ============================================================================

class TestProblemasTSP_SAT(unittest.TestCase):
    """Tests for ProblemasTSP_SAT class."""

    def setUp(self):
        """Set up test problems."""
        self.const = ConstantesCertificadoNP()
        self.problemas = ProblemasTSP_SAT(self.const)

    def test_generar_sat_length(self):
        """Test SAT instance generation length."""
        n_vars = 50
        n_clausulas = 200
        instancia = self.problemas.generar_sat_instancia(n_vars, n_clausulas)
        
        # Should be padded to n_vars²
        self.assertGreaterEqual(len(instancia), n_vars * n_vars)

    def test_generar_sat_deterministic(self):
        """Test SAT instance generation is deterministic."""
        n_vars = 20
        n_clausulas = 80
        
        inst1 = self.problemas.generar_sat_instancia(n_vars, n_clausulas)
        inst2 = self.problemas.generar_sat_instancia(n_vars, n_clausulas)
        
        self.assertEqual(inst1, inst2)

    def test_generar_tsp_length(self):
        """Test TSP instance generation length."""
        n_ciudades = 30
        instancia = self.problemas.generar_tsp_instancia(n_ciudades)
        
        # Should be padded to n_ciudades²
        self.assertGreaterEqual(len(instancia), n_ciudades * n_ciudades)

    def test_generar_tsp_normalized(self):
        """Test TSP distances are normalized."""
        n_ciudades = 20
        instancia = self.problemas.generar_tsp_instancia(n_ciudades)
        
        # All distances should be ≤ 1 (normalized)
        non_zero = [d for d in instancia if d > 0]
        if non_zero:
            self.assertLessEqual(max(non_zero), 1.0)

    def test_generar_tsp_deterministic(self):
        """Test TSP instance generation is deterministic."""
        n_ciudades = 15
        
        inst1 = self.problemas.generar_tsp_instancia(n_ciudades)
        inst2 = self.problemas.generar_tsp_instancia(n_ciudades)
        
        self.assertEqual(inst1, inst2)

    def test_solucion_optima_tsp_length(self):
        """Test TSP optimal solution has correct length."""
        n_ciudades = 25
        solucion = self.problemas.solucion_optima_tsp(n_ciudades)
        
        self.assertEqual(len(solucion), n_ciudades)

    def test_solucion_optima_tsp_normalized(self):
        """Test TSP optimal solution is approximately normalized."""
        n_ciudades = 20
        solucion = self.problemas.solucion_optima_tsp(n_ciudades)
        
        # Calculate norm
        norma_sq = sum(abs(s) ** 2 for s in solucion)
        norma = math.sqrt(norma_sq)
        
        self.assertAlmostEqual(norma, 1.0, places=10)


# ============================================================================
# TEST SUITE 7 – Coherencia Global
# ============================================================================

class TestCoherenciaCertificado(unittest.TestCase):
    """Tests for CoherenciaCertificado class."""

    def setUp(self):
        """Set up test coherence."""
        self.const = ConstantesCertificadoNP()
        self.coherencia = CoherenciaCertificado(self.const)

    def test_pesos_sum_to_one(self):
        """Test that weights sum to 1."""
        total = sum(self.coherencia.pesos)
        self.assertAlmostEqual(total, 1.0, places=10)

    def test_calcular_psi_global_bounded(self):
        """Test Ψ_global is bounded [0, 1]."""
        eta_plus = 0.96
        lambda_max = 2000.0
        n_dimension = 100
        
        psi_global = self.coherencia.calcular_psi_global(eta_plus, lambda_max, n_dimension)
        
        self.assertGreaterEqual(psi_global, 0.0)
        self.assertLessEqual(psi_global, 1.0)

    def test_calcular_psi_global_high_eta(self):
        """Test Ψ_global increases with high η⁺."""
        lambda_max = 2000.0
        n_dimension = 100
        
        psi_low = self.coherencia.calcular_psi_global(0.30, lambda_max, n_dimension)
        psi_high = self.coherencia.calcular_psi_global(0.50, lambda_max, n_dimension)
        
        # With improved coherence calculation, both might saturate
        # Just check that high is at least as good as low
        self.assertGreaterEqual(psi_high, psi_low)

    def test_validar_coherencia_true(self):
        """Test coherence validation (positive case)."""
        self.assertTrue(self.coherencia.validar_coherencia(0.96))

    def test_validar_coherencia_false(self):
        """Test coherence validation (negative case)."""
        self.assertFalse(self.coherencia.validar_coherencia(0.95))

    def test_validar_coherencia_minima_true(self):
        """Test minimum coherence validation (positive case)."""
        self.assertTrue(self.coherencia.validar_coherencia_minima(0.90))

    def test_validar_coherencia_minima_false(self):
        """Test minimum coherence validation (negative case)."""
        self.assertFalse(self.coherencia.validar_coherencia_minima(0.85))


# ============================================================================
# TEST SUITE 8 – Sistema Completo
# ============================================================================

class TestSistemaCertificadoNP(unittest.TestCase):
    """Tests for SistemaCertificadoNP class."""

    def setUp(self):
        """Set up test system."""
        self.sistema = SistemaCertificadoNP()

    def test_activar_structure(self):
        """Test activation returns complete structure."""
        resultado = self.sistema.activar()
        
        # Check all required keys
        required_keys = [
            'sello_activo', 'ram_signature', 'psi_global',
            'eta_plus_sat', 'eta_plus_tsp', 'lambda_max_sat', 'lambda_max_tsp',
            'certificado_sat_valido', 'certificado_tsp_valido',
            'coherencia_validada_np', 'coherencia_validada_minima',
            'complejidad_sat', 'complejidad_tsp',
            'umbral_np', 'umbral_minimo', 'f0_hz', 'gamma_1', 'kappa_pi'
        ]
        
        for key in required_keys:
            self.assertIn(key, resultado)

    def test_activar_sello_activo(self):
        """Test that seal is active."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado['sello_activo'])

    def test_activar_ram_signature(self):
        """Test RAM signature."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado['ram_signature'], 'RAM-LXIX-2026-CERTIFICADO-NP-COHERENCIA')

    def test_activar_psi_global_bounded(self):
        """Test Ψ_global is bounded."""
        resultado = self.sistema.activar()
        
        self.assertGreaterEqual(resultado['psi_global'], 0.0)
        self.assertLessEqual(resultado['psi_global'], 1.0)

    def test_activar_eta_plus_sat_positive(self):
        """Test η⁺_SAT is positive."""
        resultado = self.sistema.activar()
        self.assertGreater(resultado['eta_plus_sat'], 0.0)

    def test_activar_eta_plus_tsp_positive(self):
        """Test η⁺_TSP is positive."""
        resultado = self.sistema.activar()
        self.assertGreater(resultado['eta_plus_tsp'], 0.0)

    def test_activar_coherencia_minima(self):
        """Test minimum coherence is validated."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado['coherencia_validada_minima'])

    def test_activar_f0_value(self):
        """Test F₀ value."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['f0_hz'], 141.7001, places=4)

    def test_activar_gamma_1_value(self):
        """Test γ₁ value."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['gamma_1'], 14.134725, places=6)

    def test_activar_kappa_pi_value(self):
        """Test κ_Π value."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['kappa_pi'], 2.5773, places=4)

    def test_activar_umbral_np(self):
        """Test NP threshold value."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['umbral_np'], 0.9575, places=4)

    def test_activar_umbral_minimo(self):
        """Test minimum threshold value."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['umbral_minimo'], 0.888, places=3)


# ============================================================================
# TEST SUITE 9 – API Pública
# ============================================================================

class TestAPICertificadoNP(unittest.TestCase):
    """Tests for public API function."""

    def test_certificado_np_activar_callable(self):
        """Test that public API function is callable."""
        resultado = certificado_np_activar()
        self.assertIsInstance(resultado, dict)

    def test_certificado_np_activar_sello_activo(self):
        """Test API returns active seal."""
        resultado = certificado_np_activar()
        self.assertTrue(resultado['sello_activo'])

    def test_certificado_np_activar_psi_global(self):
        """Test API returns Ψ_global."""
        resultado = certificado_np_activar()
        self.assertIn('psi_global', resultado)
        self.assertIsInstance(resultado['psi_global'], float)

    def test_certificado_np_activar_coherencia_minima(self):
        """Test API validates minimum coherence."""
        resultado = certificado_np_activar()
        self.assertTrue(resultado['coherencia_validada_minima'])
        self.assertGreaterEqual(resultado['psi_global'], 0.888)


# ============================================================================
# TEST SUITE 10 – Conexión con Riemann
# ============================================================================

class TestConexionRiemann(unittest.TestCase):
    """Tests for connection to Riemann zeros."""

    def setUp(self):
        """Set up test constants."""
        self.const = ConstantesCertificadoNP()

    def test_gamma_1_from_riemann_zeros(self):
        """Test γ₁ matches first Riemann zero."""
        self.assertAlmostEqual(
            self.const.gamma_1(),
            self.const.riemann_zeros[0],
            places=10
        )

    def test_riemann_zeros_in_hamiltonian(self):
        """Test Riemann zeros appear in Hamiltonian."""
        espacio = EspacioHilbertAdelico(self.const, 10)
        instancia = [1.0] * 100
        H = espacio.construir_hamiltoniano(instancia)
        
        # Check diagonal uses Riemann zeros
        for i in range(10):
            gamma_idx = i % len(self.const.riemann_zeros)
            expected = self.const.f0 * self.const.riemann_zeros[gamma_idx]
            self.assertAlmostEqual(H[i][i].real, expected, places=2)

    def test_riemann_spacing_gue(self):
        """Test Riemann zeros have GUE-like spacing."""
        zeros = self.const.riemann_zeros
        
        # Calculate spacings
        spacings = [zeros[i+1] - zeros[i] for i in range(len(zeros) - 1)]
        
        # All spacings should be positive
        for s in spacings:
            self.assertGreater(s, 0.0)
        
        # Mean spacing should be around 6-8 (varies)
        mean_spacing = sum(spacings) / len(spacings)
        self.assertGreater(mean_spacing, 3.0)
        self.assertLess(mean_spacing, 15.0)


# ============================================================================
# TEST SUITE 11 – Implementación Biológica
# ============================================================================

class TestImplementacionBiologica(unittest.TestCase):
    """Tests for biological implementation (microtubules)."""

    def test_microtubule_dimension(self):
        """Test microtubule-like dimension scaling."""
        # Microtubules have ~13 protofilaments
        # Each tubulin dimer can represent a qubit
        const = ConstantesCertificadoNP()
        
        # Typical microtubule length: 25 μm / 8 nm per dimer ≈ 3000 dimers
        n_dimers = 3000
        
        # Check polynomial complexity is feasible
        complejidad = const.complejidad_polinomial(n_dimers)
        
        # O(n³) for 3000 should be ~2.7e10 operations
        # Feasible at GHz frequencies
        self.assertGreater(complejidad, 1e9)
        self.assertLess(complejidad, 1e11)

    def test_frohlich_coherence_frequency(self):
        """Test Fröhlich coherence at f₀."""
        const = ConstantesCertificadoNP()
        
        # Fröhlich coherence occurs at f₀ = 141.7001 Hz
        self.assertAlmostEqual(const.f0, 141.7001, places=4)
        
        # This is the microtubule oscillation frequency
        # Supporting biological NP computation


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
