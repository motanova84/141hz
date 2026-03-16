#!/usr/bin/env python3
"""
Tests for physics.simetria_pt_resonancia

Validates the PT-symmetry resonance bridge (QCAL-SYMBIO-1) between Riemann
spectral geometry and biological coherence.

Key assertions:
- H = Hᵀ (complex symmetric PT condition)
- Eigenvalues are real for ε ≪ |Δλ|/2
- Ψ_EZ = F0/(F0+γ_EZ) ≈ 0.993262
- Ψ_global = 0.5·Ψ_esp + 0.3·Ψ_EZ + 0.2·Ψ_Riemann ≈ 0.998
- Decoherence (large ε) produces complex eigenvalues (falsifiability)
Validates the PT-symmetry resonance simulation (Protocolo QCAL-SYMBIO-1):
- Non-Hermitian operator with PT symmetry produces real eigenvalues at Ψ → 1.
- Eigenvalue stability collapses to the Riemann critical line under high coherence.
"""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.simetria_pt_resonancia import (
    ConstantesPT,
    OperadorNHPT,
    EspectroPTReal,
    RiemannLineaCritica,
    CitoplasmaHolografico,
    EstabilizadorPT,
    SistemaResonanciaPT,
    ResultadoPT,
    simetria_pt_resonancia_activar,
    simular_resonancia_pt,
    _PESO_PSI_ESPECTRAL,
    _PESO_PSI_EZ,
    _PESO_PSI_RIEMANN,
)

# Small-gap zeros used across multiple tests to trigger PT breaking (ε > gap).
# gap = |1.1 − 1.0| / 2 = 0.05; psi=0.9 → ε=0.1 > 0.05 → PT broken.
_SMALL_GAP_ZEROS = [1.0, 1.1]


# ============================================================================
# ConstantesPT
# ============================================================================

class TestConstantesPT(unittest.TestCase):
    """Tests for ConstantesPT class."""

    def setUp(self):
        self.c = ConstantesPT()

    def test_f0_valor(self):
        """F0 must be 141.7001 Hz."""
        self.assertAlmostEqual(self.c.F0, 141.7001, places=4)

    def test_umbral_pt(self):
        """UMBRAL_PT must be 0.888."""
        self.assertAlmostEqual(self.c.UMBRAL_PT, 0.888, places=3)

    def test_zeros_riemann_count(self):
        """Must have exactly 10 Riemann zeros."""
        self.assertEqual(len(self.c.zeros_riemann), 10)

    def test_zeros_riemann_first(self):
        """First Riemann zero must be ≈ 14.134725."""
        self.assertAlmostEqual(self.c.zeros_riemann[0], 14.134725, places=5)

    def test_zeros_riemann_last(self):
        """Tenth Riemann zero must be ≈ 49.773832."""
        self.assertAlmostEqual(self.c.zeros_riemann[-1], 49.773832, places=5)

    def test_zeros_riemann_ascending(self):
        """Riemann zeros must be in strictly ascending order."""
        zs = self.c.zeros_riemann
        for i in range(len(zs) - 1):
            self.assertLess(zs[i], zs[i + 1])

    def test_gamma_ez_positivo(self):
        """γ_EZ must be positive."""
        self.assertGreater(self.c.gamma_EZ, 0.0)

    def test_gamma_ez_da_psi_ez(self):
        """γ_EZ calibration must yield Ψ_EZ ≈ 0.993262."""
        psi_ez = self.c.F0 / (self.c.F0 + self.c.gamma_EZ)
        self.assertAlmostEqual(psi_ez, 0.993262, places=5)

    def test_repr(self):
        """__repr__ must contain F0 and n_zeros."""
        r = repr(self.c)
        self.assertIn("141.7001", r)
        self.assertIn("10", r)


# ============================================================================
# OperadorNHPT
# ============================================================================

class TestOperadorNHPT(unittest.TestCase):
    """Tests for OperadorNHPT class."""

    def setUp(self):
        self.c = ConstantesPT()

    def test_simetria_compleja_psi_1(self):
        """H = H^T must hold for psi=1.0 (ε=0)."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=1.0)
        self.assertTrue(op.verificar_simetria())

    def test_simetria_compleja_psi_parcial(self):
        """H = H^T must hold for psi=0.9."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.9)
        self.assertTrue(op.verificar_simetria())

    def test_simetria_compleja_psi_pequena(self):
        """H = H^T must hold for psi=0.001 (large ε)."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.001)
        self.assertTrue(op.verificar_simetria())

    def test_epsilon_es_complemento(self):
        """epsilon must equal 1 - psi."""
        psi = 0.75
        op = OperadorNHPT(self.c.zeros_riemann, psi=psi)
        self.assertAlmostEqual(op.epsilon, 1.0 - psi, places=12)

    def test_diagonal_son_zeros_riemann(self):
        """Real part of H diagonal must equal Riemann zeros."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.999)
        diag_real = np.diag(op.H).real
        np.testing.assert_allclose(diag_real, self.c.zeros_riemann, rtol=1e-10)

    def test_forma_matriz(self):
        """H must be a square matrix of size N×N."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.5)
        N = len(self.c.zeros_riemann)
        self.assertEqual(op.H.shape, (N, N))

    def test_psi_invalido_menor_cero(self):
        """psi < 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorNHPT(self.c.zeros_riemann, psi=-0.1)

    def test_psi_invalido_mayor_uno(self):
        """psi > 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorNHPT(self.c.zeros_riemann, psi=1.1)

    def test_anti_diagonal_imaginaria(self):
        """Off-diagonal anti-diagonal entries must be imaginary."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.5)
        N = len(self.c.zeros_riemann)
        for j in range(N):
            k = N - 1 - j
            if j != k:
                # entry must be purely imaginary
                self.assertAlmostEqual(op.H[j, k].real, 0.0, places=10)
                self.assertAlmostEqual(op.H[j, k].imag, op.epsilon, places=10)

    def test_repr(self):
        """__repr__ must contain N and psi."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.9)
        r = repr(op)
        self.assertIn("10", r)
        self.assertIn("0.9", r)


# ============================================================================
# EspectroPTReal
# ============================================================================

class TestEspectroPTReal(unittest.TestCase):
    """Tests for EspectroPTReal class."""

    def setUp(self):
        self.c = ConstantesPT()

    def test_espectro_real_psi_1(self):
        """All eigenvalues must be real for psi=1.0."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=1.0)
        esp = EspectroPTReal(op)
        self.assertTrue(esp.es_real())

    def test_espectro_real_psi_alto(self):
        """All eigenvalues must be real for psi=0.999999 (ε ≪ min_gap)."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.999999)
        esp = EspectroPTReal(op)
        self.assertTrue(esp.es_real())

    def test_espectro_real_psi_medio(self):
        """Eigenvalues must remain real for psi=0.9 (ε=0.1 < min_gap≈2.33)."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.9)
        esp = EspectroPTReal(op)
        self.assertTrue(esp.es_real())

    def test_espectro_complejo_psi_muy_bajo(self):
        """Eigenvalues must become complex for psi close to 0 (ε > min_gap)."""
        # ε = 1 - 0.001 = 0.999 > min_gap ≈ 2.33 is still not broken
        # Need ε > min_gap ≈ 2.33, so psi < 1 - 2.33 = -1.33 (impossible).
        # Test PT breaking requires artificial small-gap zeros since standard
        # Riemann zeros have min_gap ≈ 2.326 > ε_max = 1.0.
        op = OperadorNHPT(_SMALL_GAP_ZEROS, psi=0.9)  # gap=0.05, ε=0.1 > 0.05
        esp = EspectroPTReal(op)
        self.assertFalse(esp.es_real())

    def test_psi_espectral_total_para_real(self):
        """calcular_psi_espectral() must return 1.0 when all eigenvalues are real."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=1.0)
        esp = EspectroPTReal(op)
        self.assertAlmostEqual(esp.calcular_psi_espectral(), 1.0, places=6)

    def test_psi_espectral_parcial(self):
        """calcular_psi_espectral() returns fraction when some eigenvalues complex."""
        op = OperadorNHPT(_SMALL_GAP_ZEROS, psi=0.9)  # gap=0.05, ε=0.1 → complex pair
        esp = EspectroPTReal(op)
        psi_esp = esp.calcular_psi_espectral()
        self.assertGreaterEqual(psi_esp, 0.0)
        self.assertLessEqual(psi_esp, 1.0)

    def test_n_eigenvalues(self):
        """Number of eigenvalues must equal N (number of Riemann zeros)."""
        N = len(self.c.zeros_riemann)
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.5)
        esp = EspectroPTReal(op)
        self.assertEqual(len(esp.eigenvalues), N)

    def test_eigenvalues_approximately_riemann_zeros(self):
        """For psi=1.0 (ε=0), eigenvalues must be exactly the Riemann zeros."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=1.0)
        esp = EspectroPTReal(op)
        sorted_eig = np.sort(esp.eigenvalues.real)
        sorted_zeros = np.sort(self.c.zeros_riemann)
        np.testing.assert_allclose(sorted_eig, sorted_zeros, rtol=1e-8)

    def test_imag_cerca_cero_psi_alto(self):
        """For psi=0.999999, imaginary parts must be < 1e-5."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=0.999999)
        esp = EspectroPTReal(op)
        self.assertTrue(np.allclose(esp.eigenvalues.imag, 0, atol=1e-5))

    def test_repr(self):
        """__repr__ must contain N and es_real."""
        op = OperadorNHPT(self.c.zeros_riemann, psi=1.0)
        esp = EspectroPTReal(op)
        r = repr(esp)
        self.assertIn("10", r)


# ============================================================================
# RiemannLineaCritica
# ============================================================================

class TestRiemannLineaCritica(unittest.TestCase):
    """Tests for RiemannLineaCritica class."""

    def setUp(self):
        self.c = ConstantesPT()
        op = OperadorNHPT(self.c.zeros_riemann, psi=1.0)
        esp = EspectroPTReal(op)
        self.rl = RiemannLineaCritica(esp, self.c.zeros_riemann)

    def test_psi_riemann_es_uno(self):
        """calcular_psi_riemann() must return 1.0."""
        self.assertAlmostEqual(self.rl.calcular_psi_riemann(), 1.0, places=10)

    def test_puntos_criticos_forma(self):
        """puntos_criticos must have N elements."""
        self.assertEqual(len(self.rl.puntos_criticos), len(self.c.zeros_riemann))

    def test_parte_real_de_puntos_es_media(self):
        """All critical points must have Re(s) = 0.5."""
        np.testing.assert_allclose(
            self.rl.puntos_criticos.real,
            0.5,
            atol=1e-10,
        )

    def test_verificar_linea_critica_psi_1(self):
        """verificar_linea_critica() must be True for psi=1.0."""
        self.assertTrue(self.rl.verificar_linea_critica())

    def test_parte_imaginaria_puntos_son_eigenvalues(self):
        """Imaginary parts of critical points must match eigenvalues."""
        np.testing.assert_allclose(
            self.rl.puntos_criticos.imag,
            self.rl.eigenvalues,
            rtol=1e-10,
        )

    def test_repr(self):
        """__repr__ must contain psi_riemann."""
        r = repr(self.rl)
        self.assertIn("1.0", r)


# ============================================================================
# CitoplasmaHolografico
# ============================================================================

class TestCitoplasmaHolografico(unittest.TestCase):
    """Tests for CitoplasmaHolografico class."""

    def setUp(self):
        self.c = ConstantesPT()
        self.cito = CitoplasmaHolografico(self.c.F0, self.c.gamma_EZ)

    def test_psi_ez_aproximado(self):
        """Ψ_EZ must be ≈ 0.993262."""
        self.assertAlmostEqual(self.cito.psi_ez, 0.993262, places=5)

    def test_calcular_psi_ez(self):
        """calcular_psi_ez() must return the same value as psi_ez attribute."""
        self.assertAlmostEqual(self.cito.calcular_psi_ez(), self.cito.psi_ez, places=12)

    def test_psi_ez_en_rango(self):
        """Ψ_EZ must be strictly between 0 and 1."""
        self.assertGreater(self.cito.psi_ez, 0.0)
        self.assertLess(self.cito.psi_ez, 1.0)

    def test_f0_positivo_invalido(self):
        """f0 ≤ 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            CitoplasmaHolografico(f0=0.0)

    def test_gamma_ez_negativo_invalido(self):
        """gamma_ez < 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            CitoplasmaHolografico(f0=141.7001, gamma_ez=-1.0)

    def test_gamma_ez_cero_da_psi_1(self):
        """γ_EZ = 0 must give Ψ_EZ = 1.0."""
        cito = CitoplasmaHolografico(f0=141.7001, gamma_ez=0.0)
        self.assertAlmostEqual(cito.psi_ez, 1.0, places=12)

    def test_formula_psi_ez(self):
        """Ψ_EZ = f0/(f0 + gamma_ez) must hold exactly."""
        expected = self.c.F0 / (self.c.F0 + self.c.gamma_EZ)
        self.assertAlmostEqual(self.cito.psi_ez, expected, places=12)

    def test_repr(self):
        """__repr__ must contain f0 and psi_ez."""
        r = repr(self.cito)
        self.assertIn("141.7001", r)
        self.assertIn("psi_ez", r)


# ============================================================================
# EstabilizadorPT
# ============================================================================

class TestEstabilizadorPT(unittest.TestCase):
    """Tests for EstabilizadorPT class."""

    def setUp(self):
        self.c = ConstantesPT()

    def _make_estabilizador(self, psi):
        op = OperadorNHPT(self.c.zeros_riemann, psi=psi)
        esp = EspectroPTReal(op)
        return EstabilizadorPT(op, esp)

    def test_estable_psi_1(self):
        """System must be PT stable for psi=1.0 (ε=0)."""
        est = self._make_estabilizador(1.0)
        self.assertTrue(est.es_pt_estable())

    def test_estable_psi_alto(self):
        """System must be PT stable for psi=0.999999."""
        est = self._make_estabilizador(0.999999)
        self.assertTrue(est.es_pt_estable())

    def test_estable_psi_medio(self):
        """System must be PT stable for psi=0.9 (ε=0.1 < min_gap≈2.326)."""
        est = self._make_estabilizador(0.9)
        self.assertTrue(est.es_pt_estable())

    def test_inestable_gap_pequeno(self):
        """System must be PT unstable when ε > min_gap."""
        op = OperadorNHPT(_SMALL_GAP_ZEROS, psi=0.9)  # gap=0.05, ε=0.1 > 0.05
        esp = EspectroPTReal(op)
        est = EstabilizadorPT(op, esp)
        self.assertFalse(est.es_pt_estable())

    def test_min_gap_positivo(self):
        """min_gap must be positive for distinct Riemann zeros."""
        est = self._make_estabilizador(0.5)
        self.assertGreater(est.min_gap, 0.0)

    def test_min_gap_valor(self):
        """min_gap must be ≈ 2.326 (half of smallest adjacent-pair difference)."""
        est = self._make_estabilizador(0.5)
        # Pair (4,5): |32.935062 - 37.586178| / 2 ≈ 2.3256
        self.assertAlmostEqual(est.min_gap, 2.3256, places=3)

    def test_diagnosticar_claves(self):
        """diagnosticar() must return all required keys."""
        est = self._make_estabilizador(1.0)
        diag = est.diagnosticar()
        for key in ("estable", "epsilon", "min_gap", "espectro_real", "margen"):
            self.assertIn(key, diag)

    def test_diagnosticar_estable_psi_1(self):
        """diagnosticar()['estable'] must be True for psi=1.0."""
        est = self._make_estabilizador(1.0)
        self.assertTrue(est.diagnosticar()["estable"])

    def test_diagnosticar_margen_positivo_psi_alto(self):
        """margen must be positive for psi=0.9 (PT stable)."""
        est = self._make_estabilizador(0.9)
        self.assertGreater(est.diagnosticar()["margen"], 0.0)

    def test_repr(self):
        """__repr__ must contain epsilon and min_gap."""
        est = self._make_estabilizador(0.9)
        r = repr(est)
        self.assertIn("epsilon", r)
        self.assertIn("min_gap", r)


# ============================================================================
# SistemaResonanciaPT
# ============================================================================

class TestSistemaResonanciaPT(unittest.TestCase):
    """Tests for SistemaResonanciaPT class."""

    def setUp(self):
        self.sistema = SistemaResonanciaPT(psi_coherencia=1.0)
        self.resultado = self.sistema.evaluar()

    def test_psi_global_approx(self):
        """Ψ_global must be ≈ 0.998 for default coherencia=1.0."""
        self.assertAlmostEqual(self.resultado.psi_global, 0.998, places=3)

    def test_espectro_real(self):
        """espectro_real must be True for psi_coherencia=1.0."""
        self.assertTrue(self.resultado.espectro_real)

    def test_simetria_pt_verificada(self):
        """simetria_pt_verificada must be True."""
        self.assertTrue(self.resultado.simetria_pt_verificada)

    def test_aprobado(self):
        """aprobado must be True (Ψ_global > 0.888)."""
        self.assertTrue(self.resultado.aprobado)

    def test_psi_espectral_es_1(self):
        """psi_espectral must be 1.0 for psi_coherencia=1.0."""
        self.assertAlmostEqual(self.resultado.psi_espectral, 1.0, places=6)

    def test_psi_ez_aproximado(self):
        """psi_ez must be ≈ 0.993262."""
        self.assertAlmostEqual(self.resultado.psi_ez, 0.993262, places=5)

    def test_psi_riemann_es_1(self):
        """psi_riemann must be 1.0."""
        self.assertAlmostEqual(self.resultado.psi_riemann, 1.0, places=10)

    def test_formula_psi_global(self):
        """Ψ_global formula: _PESO_PSI_ESPECTRAL·Ψ_esp + _PESO_PSI_EZ·Ψ_EZ + _PESO_PSI_RIEMANN·Ψ_Riemann."""
        r = self.resultado
        expected = round(
            _PESO_PSI_ESPECTRAL * r.psi_espectral
            + _PESO_PSI_EZ * r.psi_ez
            + _PESO_PSI_RIEMANN * r.psi_riemann,
            4,
        )
        self.assertAlmostEqual(r.psi_global, expected, places=4)

    def test_mensaje_contiene_f0(self):
        """mensaje must contain F0 value."""
        self.assertIn("141.7001", self.resultado.mensaje)

    def test_resultado_es_dataclass(self):
        """evaluar() must return a ResultadoPT instance."""
        self.assertIsInstance(self.resultado, ResultadoPT)

    def test_psi_coherencia_bajo_reduce_psi_global(self):
        """Lower psi_coherencia (more decoherence) should give lower Ψ_global."""
        # For the standard 10 Riemann zeros, min_gap ≈ 2.326 > ε_max = 1.0, so
        # PT cannot be broken. Use _SMALL_GAP_ZEROS to verify psi_espectral drops.
        op1 = OperadorNHPT(_SMALL_GAP_ZEROS, psi=1.0)
        op2 = OperadorNHPT(_SMALL_GAP_ZEROS, psi=0.9)  # ε=0.1 > gap=0.05
        esp1 = EspectroPTReal(op1)
        esp2 = EspectroPTReal(op2)
        self.assertGreater(
            esp1.calcular_psi_espectral(),
            esp2.calcular_psi_espectral(),
        )

    def test_repr(self):
        """__repr__ must contain F0 and N_zeros."""
        r = repr(self.sistema)
        self.assertIn("141.7001", r)
        self.assertIn("10", r)


# ============================================================================
# ResultadoPT
# ============================================================================

class TestResultadoPT(unittest.TestCase):
    """Tests for ResultadoPT dataclass."""

    def setUp(self):
        self.r = simetria_pt_resonancia_activar()

    def test_tiene_psi_global(self):
        """ResultadoPT must have psi_global attribute."""
        self.assertTrue(hasattr(self.r, "psi_global"))

    def test_tiene_espectro_real(self):
        """ResultadoPT must have espectro_real attribute."""
        self.assertTrue(hasattr(self.r, "espectro_real"))

    def test_tiene_simetria_pt_verificada(self):
        """ResultadoPT must have simetria_pt_verificada attribute."""
        self.assertTrue(hasattr(self.r, "simetria_pt_verificada"))

    def test_tiene_aprobado(self):
        """ResultadoPT must have aprobado attribute."""
        self.assertTrue(hasattr(self.r, "aprobado"))

    def test_psi_global_es_float(self):
        """psi_global must be a float."""
        self.assertIsInstance(self.r.psi_global, float)


# ============================================================================
# API: simetria_pt_resonancia_activar
# ============================================================================

class TestSimetriaPTResonanciaActivar(unittest.TestCase):
    """Tests for the simetria_pt_resonancia_activar() API function."""

    def setUp(self):
        self.resultado = simetria_pt_resonancia_activar()

    def test_retorna_resultado_pt(self):
        """Must return a ResultadoPT instance."""
        self.assertIsInstance(self.resultado, ResultadoPT)

    def test_psi_global(self):
        """psi_global must be 0.998 (rounded to 4 decimal places)."""
        self.assertAlmostEqual(self.resultado.psi_global, 0.998, places=3)

    def test_espectro_real_true(self):
        """espectro_real must be True."""
        self.assertTrue(self.resultado.espectro_real)

    def test_simetria_pt_verificada_true(self):
        """simetria_pt_verificada must be True."""
        self.assertTrue(self.resultado.simetria_pt_verificada)

    def test_aprobado_true(self):
        """aprobado must be True."""
        self.assertTrue(self.resultado.aprobado)

    def test_mensaje_no_vacio(self):
        """mensaje must not be empty."""
        self.assertTrue(len(self.resultado.mensaje) > 0)


# ============================================================================
# API: simular_resonancia_pt
# ============================================================================

class TestSimularResonanciaPT(unittest.TestCase):
    """Tests for the simular_resonancia_pt() API function."""

    def test_retorna_ndarray(self):
        """Must return a numpy ndarray."""
        espectro = simular_resonancia_pt(coherencia=0.999999)
        self.assertIsInstance(espectro, np.ndarray)

    def test_longitud_espectro(self):
        """Spectrum must have 10 eigenvalues (one per Riemann zero)."""
        espectro = simular_resonancia_pt(coherencia=0.999999)
        self.assertEqual(len(espectro), 10)

    def test_espectro_real_psi_alto(self):
        """For coherencia=0.999999, all eigenvalues must have imag ≈ 0 (atol=1e-5)."""
        espectro = simular_resonancia_pt(coherencia=0.999999)
        self.assertTrue(np.allclose(espectro.imag, 0, atol=1e-5))

    def test_espectro_real_psi_1(self):
        """For coherencia=1.0 (ε=0), eigenvalues must be exactly real."""
        espectro = simular_resonancia_pt(coherencia=1.0)
        self.assertTrue(np.allclose(espectro.imag, 0, atol=1e-12))

    def test_espectro_contiene_riemann_zeros(self):
        """For coherencia=1.0, sorted real parts must match the 10 Riemann zeros."""
        espectro = simular_resonancia_pt(coherencia=1.0)
        c = ConstantesPT()
        sorted_eig = np.sort(espectro.real)
        sorted_zeros = np.sort(c.zeros_riemann)
        np.testing.assert_allclose(sorted_eig, sorted_zeros, rtol=1e-8)

    def test_decoherencia_alta_produce_complejos(self):
        """Small-gap test: high decoherence produces complex eigenvalues."""
        # The 10 Riemann zeros have min_gap ≈ 2.326 > ε_max = 1.0, so PT cannot
        # be broken with those zeros.  Use zeros with gap=0.01 < ε=0.1 instead.
        tiny_gap_zeros = [0.0, 0.02]  # min_gap = 0.01; ε=0.1 breaks PT
        op = OperadorNHPT(tiny_gap_zeros, psi=0.9)
        esp = EspectroPTReal(op)
        # At least one eigenvalue should have non-negligible imaginary part
        self.assertFalse(np.allclose(esp.eigenvalues.imag, 0, atol=1e-8))

    def test_coherencia_invalida_raise(self):
        """coherencia outside [0,1] must raise ValueError."""
        with self.assertRaises(ValueError):
            simular_resonancia_pt(coherencia=1.5)

    def test_coherencia_default(self):
        """Default coherencia=0.999999 must produce a real-ish spectrum."""
        espectro = simular_resonancia_pt()
        self.assertTrue(np.allclose(espectro.imag, 0, atol=1e-5))


# ============================================================================
# Integration: problem statement example
# ============================================================================

class TestProblemStatementQCALSYMBIO1(unittest.TestCase):
    """Integration tests mirroring the exact QCAL-SYMBIO-1 problem statement examples."""

    def test_simular_resonancia_imag_allclose(self):
        """QCAL-SYMBIO-1: np.allclose(espectro.imag, 0, atol=1e-5) must be True."""
        espectro = simular_resonancia_pt(coherencia=0.999999)
        self.assertTrue(np.allclose(espectro.imag, 0, atol=1e-5))

    def test_activar_psi_global(self):
        """QCAL-SYMBIO-1: psi_global must be ≈ 0.9980."""
        resultado = simetria_pt_resonancia_activar()
        self.assertAlmostEqual(resultado.psi_global, 0.9980, places=3)

    def test_activar_espectro_real(self):
        """QCAL-SYMBIO-1: espectro_real must be True."""
        resultado = simetria_pt_resonancia_activar()
        self.assertTrue(resultado.espectro_real)

    def test_activar_simetria_pt_verificada(self):
        """QCAL-SYMBIO-1: simetria_pt_verificada must be True."""
        resultado = simetria_pt_resonancia_activar()
        self.assertTrue(resultado.simetria_pt_verificada)

    def test_physics_package_import(self):
        """All classes must be importable from physics package."""
        from physics import (
            ConstantesPT,
            OperadorNHPT,
            EspectroPTReal,
            RiemannLineaCritica,
            CitoplasmaHolografico,
            EstabilizadorPT,
            SistemaResonanciaPT,
            ResultadoPT,
            simetria_pt_resonancia_activar,
            simular_resonancia_pt,
        )
        self.assertIsNotNone(ConstantesPT)
    BaseRiemann,
    EspectroEigenvalores,
    MotorResonanciaPT,
    OperadorPT,
    ResultadoResonanciaPT,
    activar_protocolo_qcal_symbio_1,
    simular_resonancia_pt,
)


class TestBaseRiemann(unittest.TestCase):
    """Tests for BaseRiemann spectral proxy."""

    def test_shape(self):
        """Generated array must have exactly n elements."""
        b = BaseRiemann(50, semilla=0)
        self.assertEqual(b.valores.shape, (50,))

    def test_ordenado(self):
        """Values must be sorted in ascending order."""
        b = BaseRiemann(100, semilla=42)
        self.assertTrue(np.all(b.valores[:-1] <= b.valores[1:]))

    def test_diagonal_shape(self):
        """como_diagonal() must return an N×N matrix."""
        b = BaseRiemann(10, semilla=1)
        d = b.como_diagonal()
        self.assertEqual(d.shape, (10, 10))

    def test_diagonal_values(self):
        """Diagonal entries must match the sorted values array."""
        b = BaseRiemann(10, semilla=2)
        d = b.como_diagonal()
        np.testing.assert_array_equal(np.diag(d), b.valores)

    def test_n_invalido(self):
        """n < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            BaseRiemann(0)

    def test_reproducibilidad(self):
        """Same seed must produce identical values."""
        b1 = BaseRiemann(30, semilla=99)
        b2 = BaseRiemann(30, semilla=99)
        np.testing.assert_array_equal(b1.valores, b2.valores)

    def test_semillas_distintas(self):
        """Different seeds should produce different values (with overwhelming probability)."""
        b1 = BaseRiemann(30, semilla=1)
        b2 = BaseRiemann(30, semilla=2)
        self.assertFalse(np.array_equal(b1.valores, b2.valores))


class TestOperadorPT(unittest.TestCase):
    """Tests for OperadorPT non-Hermitian Hamiltonian."""

    def setUp(self):
        self.base = BaseRiemann(10, semilla=0)

    def test_shape(self):
        """Constructed matrix must be N×N."""
        op = OperadorPT(self.base, coherencia=0.999999)
        h = op.construir()
        self.assertEqual(h.shape, (10, 10))

    def test_dtype_complejo(self):
        """Matrix must have complex dtype."""
        op = OperadorPT(self.base, coherencia=0.999999)
        h = op.construir()
        self.assertTrue(np.iscomplexobj(h))

    def test_diagonal_real_igual_base(self):
        """Real part of diagonal must match the Riemann base values."""
        op = OperadorPT(self.base, coherencia=0.999999)
        h = op.construir()
        np.testing.assert_allclose(np.diag(h).real, self.base.valores)

    def test_parte_imaginaria_suprimida_con_coherencia_1(self):
        """At coherencia=1.0 the imaginary part must be exactly zero."""
        op = OperadorPT(self.base, coherencia=1.0)
        h = op.construir()
        np.testing.assert_array_equal(h.imag, np.zeros((10, 10)))

    def test_parte_imaginaria_no_nula_coherencia_baja(self):
        """At coherencia=0.5 the imaginary part must not be all zero."""
        op = OperadorPT(self.base, coherencia=0.5)
        h = op.construir()
        self.assertFalse(np.allclose(h.imag, 0))

    def test_coherencia_invalida_negativa(self):
        """Negative coherence must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorPT(self.base, coherencia=-0.1)

    def test_coherencia_invalida_cero(self):
        """coherencia=0 must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorPT(self.base, coherencia=0.0)

    def test_coherencia_invalida_mayor_uno(self):
        """coherencia > 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            OperadorPT(self.base, coherencia=1.001)

    def test_antidiagonal_imaginaria(self):
        """Imaginary coupling must follow fliplr(eye) × (1 − Ψ) pattern."""
        op = OperadorPT(self.base, coherencia=0.9)
        h = op.construir()
        expected_imag = np.fliplr(np.eye(10)) * 0.1
        np.testing.assert_allclose(h.imag, expected_imag)


class TestEspectroEigenvalores(unittest.TestCase):
    """Tests for EspectroEigenvalores spectral analysis."""

    def _operador_alta_coherencia(self, n=20, semilla=0):
        base = BaseRiemann(n, semilla=semilla)
        op = OperadorPT(base, coherencia=0.999999)
        return op.construir()

    def _operador_baja_coherencia(self, n=20, semilla=0):
        base = BaseRiemann(n, semilla=semilla)
        op = OperadorPT(base, coherencia=0.5)
        return op.construir()

    def test_numero_autovalores(self):
        """Number of eigenvalues must equal matrix dimension."""
        h = self._operador_alta_coherencia(n=15)
        esp = EspectroEigenvalores(h)
        self.assertEqual(len(esp.autovalores), 15)

    def test_estable_coherencia_alta(self):
        """High coherence operator must be PT-stable (eigenvalues ≈ real)."""
        h = self._operador_alta_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertTrue(esp.es_estable())

    def test_inestable_coherencia_baja(self):
        """Low coherence operator must NOT be PT-stable."""
        h = self._operador_baja_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertFalse(esp.es_estable())

    def test_media_imaginaria_cerca_cero_alta_coherencia(self):
        """Mean imaginary part must be < atol for high coherence."""
        h = self._operador_alta_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertLess(esp.media_imaginaria(), 1e-5)

    def test_max_imaginario_cerca_cero_alta_coherencia(self):
        """Max imaginary part must be < atol for high coherence."""
        h = self._operador_alta_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertLess(esp.max_imaginario(), 1e-5)

    def test_media_imaginaria_no_nula_baja_coherencia(self):
        """Mean imaginary part must be significant for low coherence."""
        h = self._operador_baja_coherencia()
        esp = EspectroEigenvalores(h)
        self.assertGreater(esp.media_imaginaria(), 1e-3)


class TestMotorResonanciaPT(unittest.TestCase):
    """Tests for MotorResonanciaPT integration engine."""

    def test_resultado_tipo(self):
        """ejecutar() must return a ResultadoResonanciaPT instance."""
        motor = MotorResonanciaPT(n_dimension=10, coherencia=0.999999, semilla=0)
        resultado = motor.ejecutar()
        self.assertIsInstance(resultado, ResultadoResonanciaPT)

    def test_n_dimension_invalida(self):
        """n_dimension < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            MotorResonanciaPT(n_dimension=0)

    def test_coherencia_invalida(self):
        """coherencia outside (0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            MotorResonanciaPT(coherencia=1.5)

    def test_estable_alta_coherencia(self):
        """High coherence must produce a stable (PT-symmetric) result."""
        motor = MotorResonanciaPT(n_dimension=50, coherencia=0.999999, semilla=42)
        resultado = motor.ejecutar()
        self.assertTrue(resultado.estable)

    def test_inestable_baja_coherencia(self):
        """Low coherence must produce an unstable result."""
        motor = MotorResonanciaPT(n_dimension=50, coherencia=0.5, semilla=42)
        resultado = motor.ejecutar()
        self.assertFalse(resultado.estable)

    def test_coherencia_reflejada_en_resultado(self):
        """Result must reflect the coherence parameter used."""
        motor = MotorResonanciaPT(n_dimension=10, coherencia=0.95, semilla=0)
        resultado = motor.ejecutar()
        self.assertAlmostEqual(resultado.coherencia, 0.95)

    def test_n_dimension_reflejada(self):
        """Result n_dimension must match the motor parameter."""
        motor = MotorResonanciaPT(n_dimension=30, coherencia=0.999999, semilla=0)
        resultado = motor.ejecutar()
        self.assertEqual(resultado.n_dimension, 30)
        self.assertEqual(len(resultado.autovalores), 30)

    def test_reproducibilidad_con_semilla(self):
        """Same seed must produce identical eigenvalues."""
        r1 = MotorResonanciaPT(n_dimension=20, coherencia=0.999999, semilla=7).ejecutar()
        r2 = MotorResonanciaPT(n_dimension=20, coherencia=0.999999, semilla=7).ejecutar()
        np.testing.assert_array_equal(r1.autovalores, r2.autovalores)

    def test_metricas_imaginarias_positivas(self):
        """media_imaginaria and max_imaginario must be >= 0."""
        resultado = MotorResonanciaPT(n_dimension=20, semilla=0).ejecutar()
        self.assertGreaterEqual(resultado.media_imaginaria, 0.0)
        self.assertGreaterEqual(resultado.max_imaginario, 0.0)

    def test_max_mayor_o_igual_media(self):
        """max_imaginario must be >= media_imaginaria."""
        resultado = MotorResonanciaPT(n_dimension=20, semilla=0).ejecutar()
        self.assertGreaterEqual(resultado.max_imaginario, resultado.media_imaginaria)


class TestResultadoResonanciaPT(unittest.TestCase):
    """Tests for ResultadoResonanciaPT dataclass."""

    def setUp(self):
        self.resultado = MotorResonanciaPT(n_dimension=10, coherencia=0.999999, semilla=0).ejecutar()

    def test_resumen_contiene_coherencia(self):
        """resumen() must include the coherence value."""
        texto = self.resultado.resumen()
        self.assertIn("0.999999", texto)

    def test_resumen_contiene_umbral_biologico(self):
        """resumen() must include the biological threshold check."""
        texto = self.resultado.resumen()
        self.assertIn("Umbral biológico", texto)

    def test_resumen_contiene_estabilidad(self):
        """resumen() must include PT stability status."""
        texto = self.resultado.resumen()
        self.assertIn("Estabilidad", texto)

    def test_resumen_es_cadena(self):
        """resumen() must return a string."""
        self.assertIsInstance(self.resultado.resumen(), str)


class TestSimularResonanciaPT(unittest.TestCase):
    """Tests for the simular_resonancia_pt public API."""

    def test_retorna_array(self):
        """Must return a numpy array."""
        resultado = simular_resonancia_pt(n_dimension=10, coherencia=0.999999, semilla=0)
        self.assertIsInstance(resultado, np.ndarray)

    def test_longitud_array(self):
        """Length of returned array must equal n_dimension."""
        resultado = simular_resonancia_pt(n_dimension=25, coherencia=0.999999, semilla=0)
        self.assertEqual(len(resultado), 25)

    def test_estabilidad_alta_coherencia(self):
        """Eigenvalues must be approximately real at high coherence."""
        autovalores = simular_resonancia_pt(n_dimension=100, coherencia=0.999999, semilla=0)
        self.assertTrue(np.allclose(autovalores.imag, 0, atol=1e-5))

    def test_inestabilidad_baja_coherencia(self):
        """Eigenvalues must have significant imaginary parts at low coherence."""
        autovalores = simular_resonancia_pt(n_dimension=100, coherencia=0.5, semilla=0)
        self.assertFalse(np.allclose(autovalores.imag, 0, atol=1e-5))

    def test_n_dimension_invalida(self):
        """n_dimension < 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            simular_resonancia_pt(n_dimension=0)

    def test_coherencia_invalida(self):
        """coherencia outside (0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            simular_resonancia_pt(coherencia=0.0)

    def test_valores_default(self):
        """Default parameters (n=100, Ψ=0.999999) must produce stable spectrum."""
        autovalores = simular_resonancia_pt(semilla=0)
        self.assertEqual(len(autovalores), 100)
        self.assertTrue(np.allclose(autovalores.imag, 0, atol=1e-5))


class TestActivarProtocoloQcalSymbio1(unittest.TestCase):
    """Tests for the activar_protocolo_qcal_symbio_1 public API."""

    def test_retorna_resultado(self):
        """Must return a ResultadoResonanciaPT instance."""
        resultado = activar_protocolo_qcal_symbio_1(n_dimension=10, semilla=0)
        self.assertIsInstance(resultado, ResultadoResonanciaPT)

    def test_estabilidad_default(self):
        """Default call must yield PT stability True."""
        resultado = activar_protocolo_qcal_symbio_1(semilla=0)
        self.assertTrue(resultado.estable)

    def test_coherencia_igual_a_parametro(self):
        """Result coherence must match the parameter passed."""
        resultado = activar_protocolo_qcal_symbio_1(coherencia=0.9999, semilla=0)
        self.assertAlmostEqual(resultado.coherencia, 0.9999)


if __name__ == "__main__":
    unittest.main()
