"""
Tests for physics.hamiltoniano_riemann_adelico — Hamiltoniano Riemann Adélico ∴HRA∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesRiemannAdelico  – constantes físicas y espectrales
  - EspacioHilbertAdelico     – medida de Haar, Parseval, dimensión de Weyl
  - OperadorDilatacion        – autofunciones, H·ψ=Eψ, resonancia F₀/γ₁
  - PotencialPrimos           – criba, función Mangoldt, suma ponderada
  - MatrizDispersion          – theta RS, fase δ, unitaridad |S|=1
  - FormulaTraza              – densidad Weyl, espaciado empírico vs teórico
  - NucleoResolvente          – densidad espectral, conteo integrado
  - SistemaRiemannAdelico     – Ψ_global ≥ 0.888, certificación
  - ResultadoRiemannAdelico   – dataclass de resultados
  - hamiltoniano_riemann_adelico_activar() – API pública

Invariantes clave verificados:
  - γ₁ ≈ 14.134725 (primer cero no trivial de Riemann)
  - F₀/γ₁ ≈ 10.024 (resonancia décupla)
  - ‖U(λ)f‖² = ‖f‖² (invarianza de Haar)
  - H ψ_E = E ψ_E (autoadjunción exacta)
  - |S(t)| = 1 (unitaridad de la matriz S)
  - Ψ_global ≥ 0.888 (umbral noético)
  - Sello ∴HRA∞³ ACTIVO
"""

import cmath
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.hamiltoniano_riemann_adelico import (
    # Constantes de módulo
    _F0,
    _PHI,
    _HBAR,
    _PSI_UMBRAL,
    _ZEROS_20,
    _SELLO,
    _CERT_MARK,
    # Utilidades internas
    _log_gamma_stirling,
    _theta_rs,
    _criba_eratostenes,
    _potencias_primas,
    # Clases
    ConstantesRiemannAdelico,
    EspacioHilbertAdelico,
    OperadorDilatacion,
    PotencialPrimos,
    MatrizDispersion,
    FormulaTraza,
    NucleoResolvente,
    SistemaRiemannAdelico,
    ResultadoRiemannAdelico,
    # API pública
    hamiltoniano_riemann_adelico_activar,
)


# ============================================================================
# TestModuleConstants – 10 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_phi_value(self):
        """_PHI debe ser la razón áurea φ ≈ 1.618034."""
        self.assertAlmostEqual(_PHI, (1 + math.sqrt(5)) / 2, places=12)

    def test_hbar_positive(self):
        """_HBAR debe ser positivo."""
        self.assertGreater(_HBAR, 0)

    def test_hbar_codata(self):
        """_HBAR debe estar cerca del valor CODATA 1.054571817e-34."""
        self.assertAlmostEqual(_HBAR, 1.054571817e-34, delta=1e-44)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=10)

    def test_zeros_count(self):
        """Deben cargarse exactamente 20 ceros de Riemann."""
        self.assertEqual(len(_ZEROS_20), 20)

    def test_first_zero(self):
        """γ₁ ≈ 14.134725 (primer cero no trivial)."""
        self.assertAlmostEqual(_ZEROS_20[0], 14.134725, places=4)

    def test_last_zero(self):
        """γ₂₀ ≈ 77.144840 (vigésimo cero no trivial)."""
        self.assertAlmostEqual(_ZEROS_20[-1], 77.144840, places=4)

    def test_zeros_increasing(self):
        """Los ceros deben estar en orden estrictamente creciente."""
        for i in range(len(_ZEROS_20) - 1):
            self.assertLess(_ZEROS_20[i], _ZEROS_20[i + 1])

    def test_sello(self):
        """Sello de certificación debe ser ∴HRA∞³."""
        self.assertEqual(_SELLO, "∴HRA∞³")

    def test_cert_mark(self):
        """Marca técnica debe ser HRA-RIEMANN-VERIFIED."""
        self.assertEqual(_CERT_MARK, "HRA-RIEMANN-VERIFIED")


# ============================================================================
# TestUtilidades – 15 tests
# ============================================================================

class TestUtilidades(unittest.TestCase):
    """Tests para las funciones de utilidad internas."""

    def test_log_gamma_stirling_returns_complex(self):
        """_log_gamma_stirling debe retornar un complejo."""
        z = complex(0.25, 7.0)
        result = _log_gamma_stirling(z)
        self.assertIsInstance(result, complex)

    def test_log_gamma_stirling_large_t(self):
        """Para Im(z) grande, Stirling debe ser preciso."""
        # ln Γ(1/4 + 50i) — Stirling es bueno aquí
        z = complex(0.25, 50.0)
        result = _log_gamma_stirling(z)
        self.assertFalse(math.isnan(result.real))
        self.assertFalse(math.isnan(result.imag))

    def test_theta_rs_gamma1_negative(self):
        """θ(γ₁) debe ser negativo (antes del primer cero)."""
        theta = _theta_rs(_ZEROS_20[0])
        self.assertLess(theta, 0)

    def test_theta_rs_gamma20_positive(self):
        """θ(γ₂₀) debe ser positivo y grande."""
        theta = _theta_rs(_ZEROS_20[-1])
        self.assertGreater(theta, 50.0)

    def test_theta_rs_increasing(self):
        """θ(t) debe ser creciente para t grande."""
        t1, t2 = 40.0, 60.0
        self.assertLess(_theta_rs(t1), _theta_rs(t2))

    def test_theta_rs_known_approx(self):
        """θ(γ₂₀ ≈ 77.14) ≈ 57.8 (valor de referencia de la literatura)."""
        theta = _theta_rs(77.144840)
        self.assertAlmostEqual(theta, 57.8, delta=0.5)

    def test_criba_primes_10(self):
        """Deben ser 4 primos ≤ 10: 2, 3, 5, 7."""
        self.assertEqual(_criba_eratostenes(10), [2, 3, 5, 7])

    def test_criba_primes_100_count(self):
        """Deben ser 25 primos ≤ 100."""
        self.assertEqual(len(_criba_eratostenes(100)), 25)

    def test_criba_primes_100_last(self):
        """El último primo ≤ 100 debe ser 97."""
        self.assertEqual(_criba_eratostenes(100)[-1], 97)

    def test_criba_empty(self):
        """No hay primos ≤ 1."""
        self.assertEqual(_criba_eratostenes(1), [])

    def test_potencias_primas_basic(self):
        """Para Λ=10 deben aparecer 2,3,4,5,7,8,9."""
        pairs = _potencias_primas(10.0)
        pks = [p for p, _ in pairs]
        self.assertIn(2.0, pks)
        self.assertIn(4.0, pks)
        self.assertIn(8.0, pks)
        self.assertIn(3.0, pks)
        self.assertIn(9.0, pks)
        self.assertIn(5.0, pks)
        self.assertIn(7.0, pks)

    def test_potencias_primas_weights_positive(self):
        """Todos los pesos ln(p)/p^{k/2} deben ser positivos."""
        for _, w in _potencias_primas(50.0):
            self.assertGreater(w, 0)

    def test_potencias_primas_sorted(self):
        """Las potencias de primos deben estar ordenadas de menor a mayor."""
        pairs = _potencias_primas(100.0)
        for i in range(len(pairs) - 1):
            self.assertLessEqual(pairs[i][0], pairs[i + 1][0])

    def test_potencias_primas_bound(self):
        """No debe haber ninguna potencia p^k > Λ."""
        Lambda = 50.0
        for pk, _ in _potencias_primas(Lambda):
            self.assertLessEqual(pk, Lambda)

    def test_potencias_primas_weight_p2_k1(self):
        """Peso para p=2, k=1: ln(2)/√2 ≈ 0.4901."""
        pairs = dict(_potencias_primas(3.0))
        self.assertAlmostEqual(pairs[2.0], math.log(2) / math.sqrt(2), places=10)


# ============================================================================
# TestConstantesRiemannAdelico – 10 tests
# ============================================================================

class TestConstantesRiemannAdelico(unittest.TestCase):
    """Tests para la clase ConstantesRiemannAdelico."""

    def setUp(self):
        self.cte = ConstantesRiemannAdelico()

    def test_f0(self):
        self.assertAlmostEqual(self.cte.f0, 141.7001, places=4)

    def test_omega0(self):
        self.assertAlmostEqual(self.cte.omega0, 2 * math.pi * 141.7001, places=3)

    def test_hbar(self):
        self.assertAlmostEqual(self.cte.hbar, 1.054571817e-34, delta=1e-44)

    def test_phi(self):
        self.assertAlmostEqual(self.cte.phi, 1.618033988, places=6)

    def test_n_zeros(self):
        self.assertEqual(self.cte.n_zeros, 20)

    def test_gamma_1(self):
        self.assertAlmostEqual(self.cte.gamma_1, 14.134725, places=4)

    def test_gamma_20(self):
        self.assertAlmostEqual(self.cte.gamma_20, 77.144840, places=4)

    def test_sello(self):
        self.assertEqual(self.cte.sello, "∴HRA∞³")

    def test_resonancia_f0_gamma1(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.cte.resonancia_f0_gamma1()
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_resumen_keys(self):
        """resumen() debe devolver dict con claves clave."""
        r = self.cte.resumen()
        for key in ("f0_hz", "gamma_1", "gamma_20", "n_zeros", "sello",
                    "resonancia_f0_gamma1", "psi_umbral"):
            self.assertIn(key, r)


# ============================================================================
# TestEspacioHilbertAdelico – 12 tests
# ============================================================================

class TestEspacioHilbertAdelico(unittest.TestCase):
    """Tests para la clase EspacioHilbertAdelico."""

    def setUp(self):
        self.esp = EspacioHilbertAdelico(n_puntos=2000)

    def test_n_puntos(self):
        self.assertEqual(self.esp.n_puntos, 2000)

    def test_xs_positive(self):
        """Todos los puntos de la cuadrícula deben ser positivos."""
        self.assertTrue(all(x > 0 for x in self.esp._xs))

    def test_xs_count(self):
        self.assertEqual(len(self.esp._xs), 2000)

    def test_funcion_prueba_positive(self):
        """f(x) = xe^{-x} debe ser positivo."""
        fvals = self.esp._funcion_prueba()
        self.assertTrue(all(v > 0 for v in fvals))

    def test_norma_haar_cuadrado_basic(self):
        """‖f‖² debe ser positivo."""
        fvals = self.esp._funcion_prueba()
        norma = self.esp.norma_haar_cuadrado(fvals)
        self.assertGreater(norma, 0)

    def test_norma_haar_aproxima_exacta(self):
        """‖f‖² numérico debe estar cerca del exacto 0.25."""
        fvals = self.esp._funcion_prueba()
        norma = self.esp.norma_haar_cuadrado(fvals)
        self.assertAlmostEqual(norma, 0.25, delta=0.01)

    def test_norma_exacta(self):
        """norma_exacta() debe retornar 0.25."""
        self.assertAlmostEqual(self.esp.norma_exacta(), 0.25, places=10)

    def test_verificar_haar_lambda2(self):
        """‖U(2)f‖²/‖f‖² ≈ 1.0 para λ=2."""
        ratio = self.esp.verificar_haar(lam=2.0)
        self.assertAlmostEqual(ratio, 1.0, delta=0.005)

    def test_verificar_haar_lambda3(self):
        """‖U(3)f‖²/‖f‖² ≈ 1.0 para λ=3."""
        ratio = self.esp.verificar_haar(lam=3.0)
        self.assertAlmostEqual(ratio, 1.0, delta=0.005)

    def test_psi_hilbert_range(self):
        """Ψ_hilbert ∈ [0, 1]."""
        psi = self.esp.psi_hilbert()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_hilbert_supera_umbral(self):
        """Ψ_hilbert ≥ 0.888."""
        psi = self.esp.psi_hilbert()
        self.assertGreaterEqual(psi, 0.888)

    def test_dimension_weyl(self):
        """N_Weyl(T) debe ser positivo para T grande."""
        dim = self.esp.dimension_weyl(50.0)
        self.assertGreater(dim, 0)

    def test_dimension_weyl_zero_for_nonpositive(self):
        """N_Weyl(T≤0) = 0."""
        self.assertEqual(self.esp.dimension_weyl(0.0), 0.0)
        self.assertEqual(self.esp.dimension_weyl(-5.0), 0.0)


# ============================================================================
# TestOperadorDilatacion – 14 tests
# ============================================================================

class TestOperadorDilatacion(unittest.TestCase):
    """Tests para la clase OperadorDilatacion."""

    def setUp(self):
        self.op = OperadorDilatacion()

    def test_autofuncion_at_x1(self):
        """ψ_E(1) = 1 + 0i para cualquier E."""
        for gamma in _ZEROS_20[:5]:
            psi = self.op.autofuncion(1.0, gamma)
            self.assertAlmostEqual(psi.real, 1.0, places=12)
            self.assertAlmostEqual(psi.imag, 0.0, places=12)

    def test_autofuncion_modulo_at_e(self):
        """|ψ_E(e)| = e^{-1/2} ≈ 0.6065 para cualquier E."""
        for gamma in _ZEROS_20[:5]:
            psi = self.op.autofuncion(math.e, gamma)
            self.assertAlmostEqual(abs(psi), math.exp(-0.5), places=10)

    def test_autofuncion_is_complex(self):
        """autofuncion debe retornar complejo."""
        psi = self.op.autofuncion(2.0, _ZEROS_20[0])
        self.assertIsInstance(psi, complex)

    def test_autofuncion_raises_for_nonpositive(self):
        """autofuncion debe levantar ValueError para x ≤ 0."""
        with self.assertRaises(ValueError):
            self.op.autofuncion(0.0, 14.0)
        with self.assertRaises(ValueError):
            self.op.autofuncion(-1.0, 14.0)

    def test_aplicar_H_equals_E_times_psi(self):
        """Hψ_E(x) = E · ψ_E(x) — autovalor exacto en todos los x."""
        for x in (0.5, 1.0, 2.0, math.e):
            for gamma in _ZEROS_20[:5]:
                H_psi = self.op.aplicar_H(x, gamma)
                E_psi = gamma * self.op.autofuncion(x, gamma)
                self.assertAlmostEqual(H_psi.real, E_psi.real, places=10)
                self.assertAlmostEqual(H_psi.imag, E_psi.imag, places=10)

    def test_resonancia_f0_value(self):
        """F₀/γ₁ ≈ 10.024."""
        r = self.op.resonancia_f0()
        self.assertAlmostEqual(r, 141.7001 / 14.134725, places=5)

    def test_resonancia_f0_near_10(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.op.resonancia_f0()
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_psi_operador_range(self):
        """Ψ_operador ∈ [0, 1]."""
        psi = self.op.psi_operador()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_operador_supera_umbral(self):
        """Ψ_operador ≥ 0.888."""
        psi = self.op.psi_operador()
        self.assertGreaterEqual(psi, 0.888)

    def test_espectro_mellin_count(self):
        """espectro_mellin() debe devolver lista de 20 elementos."""
        espectro = self.op.espectro_mellin()
        self.assertEqual(len(espectro), 20)

    def test_espectro_mellin_values(self):
        """Autovalores de Mellin deben coincidir con los γₙ."""
        espectro = self.op.espectro_mellin()
        for i, gamma in enumerate(_ZEROS_20):
            self.assertAlmostEqual(espectro[i], gamma, places=10)


# ============================================================================
# TestPotencialPrimos – 14 tests
# ============================================================================

class TestPotencialPrimos(unittest.TestCase):
    """Tests para la clase PotencialPrimos."""

    def setUp(self):
        self.pot100 = PotencialPrimos(Lambda=100.0)
        self.pot200 = PotencialPrimos(Lambda=200.0)

    def test_n_potencias_100_positive(self):
        """Debe haber potencias de primos positivas para Λ=100."""
        self.assertGreater(self.pot100.n_potencias_primas(), 0)

    def test_n_potencias_100_value(self):
        """Para Λ=100 deben ser al menos 30 potencias de primos."""
        self.assertGreater(self.pot100.n_potencias_primas(), 30)

    def test_potencias_y_pesos_format(self):
        """potencias_y_pesos debe devolver lista de tuplas (float, float)."""
        pares = self.pot100.potencias_y_pesos()
        self.assertIsInstance(pares, list)
        for pk, w in pares:
            self.assertIsInstance(pk, float)
            self.assertIsInstance(w, float)

    def test_suma_mangoldt_100_positive(self):
        """S(100) debe ser positivo."""
        self.assertGreater(self.pot100.suma_mangoldt_ponderada(), 0)

    def test_suma_mangoldt_100_below_asint(self):
        """S(100) debe ser menor que el asintótico (convergencia lenta)."""
        self.assertLess(
            self.pot100.suma_mangoldt_ponderada(),
            self.pot100.estimacion_asintotica(),
        )

    def test_estimacion_asintotica_100(self):
        """S_asm(100) = 2√100 − 1 = 19.0."""
        self.assertAlmostEqual(self.pot100.estimacion_asintotica(), 19.0, places=10)

    def test_estimacion_asintotica_200(self):
        """S_asm(200) = 2√200 − 1 ≈ 27.28."""
        expected = 2 * math.sqrt(200.0) - 1.0
        self.assertAlmostEqual(self.pot200.estimacion_asintotica(), expected, places=10)

    def test_psi_potencial_100_range(self):
        """Ψ_potencial(Λ=100) ∈ [0, 1]."""
        psi = self.pot100.psi_potencial()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_potencial_200_supera_umbral(self):
        """Ψ_potencial(Λ=200) ≥ 0.888."""
        psi = self.pot200.psi_potencial()
        self.assertGreaterEqual(psi, 0.888)

    def test_suma_200_greater_100(self):
        """S(200) debe ser mayor que S(100)."""
        self.assertGreater(
            self.pot200.suma_mangoldt_ponderada(),
            self.pot100.suma_mangoldt_ponderada(),
        )

    def test_prime_2_present(self):
        """El primo 2 (p^1) debe estar en el peine."""
        pks = [pk for pk, _ in self.pot100.potencias_y_pesos()]
        self.assertIn(2.0, pks)

    def test_prime_power_4_present(self):
        """2^2 = 4 debe estar en el peine."""
        pks = [pk for pk, _ in self.pot100.potencias_y_pesos()]
        self.assertIn(4.0, pks)

    def test_weight_prime_2(self):
        """Peso de p=2, k=1 debe ser ln(2)/√2 ≈ 0.4901."""
        pares = dict(self.pot100.potencias_y_pesos())
        self.assertAlmostEqual(pares[2.0], math.log(2) / math.sqrt(2), places=8)

    def test_lambda_zero(self):
        """Para Λ muy pequeño, la suma debe ser 0."""
        pot_small = PotencialPrimos(Lambda=1.5)
        self.assertEqual(pot_small.suma_mangoldt_ponderada(), 0.0)
        self.assertEqual(pot_small.n_potencias_primas(), 0)


# ============================================================================
# TestMatrizDispersion – 14 tests
# ============================================================================

class TestMatrizDispersion(unittest.TestCase):
    """Tests para la clase MatrizDispersion."""

    def setUp(self):
        self.disp = MatrizDispersion()

    def test_theta_gamma1_negative(self):
        """θ(γ₁) debe ser negativo."""
        self.assertLess(self.disp.theta(_ZEROS_20[0]), 0)

    def test_theta_gamma20_positive(self):
        """θ(γ₂₀) debe ser positivo y mayor que 50."""
        self.assertGreater(self.disp.theta(_ZEROS_20[-1]), 50.0)

    def test_theta_known_value(self):
        """θ(γ₂₀ ≈ 77.14) ≈ 57.8 (referencia de la literatura)."""
        theta = self.disp.theta(77.144840)
        self.assertAlmostEqual(theta, 57.8, delta=0.5)

    def test_theta_increases(self):
        """θ(t) debe ser creciente entre γ₁ y γ₂₀."""
        vals = [self.disp.theta(g) for g in _ZEROS_20]
        for i in range(len(vals) - 1):
            self.assertLess(vals[i], vals[i + 1])

    def test_fase_dispersion_is_negative_theta(self):
        """δ(t) = −θ(t)."""
        for t in (_ZEROS_20[0], _ZEROS_20[-1]):
            self.assertAlmostEqual(
                self.disp.fase_dispersion(t),
                -self.disp.theta(t),
                places=12,
            )

    def test_modulo_S_is_one(self):
        """|S(t)| = 1 para cualquier t (unitaridad exacta)."""
        for gamma in _ZEROS_20:
            self.assertAlmostEqual(self.disp.modulo_S(gamma), 1.0, places=15)

    def test_theta_asintotico_large_t(self):
        """θ_asm(t) debe estar definido para t > 2πe."""
        t = 100.0
        theta_asm = self.disp.theta_asintotico(t)
        self.assertGreater(theta_asm, 0)

    def test_theta_asintotico_small_t(self):
        """θ_asm(t) = 0 para t ≤ 2πe."""
        self.assertEqual(self.disp.theta_asintotico(1.0), 0.0)

    def test_theta_stirling_vs_asint_accuracy(self):
        """En γ₂₀ ≈ 77.14, error relativo |θ_Stirl − θ_asm| / |θ_Stirl| < 2%."""
        t = _ZEROS_20[-1]
        theta_s = self.disp.theta(t)
        theta_a = self.disp.theta_asintotico(t)
        rel_err = abs(theta_s - theta_a) / abs(theta_s)
        self.assertLess(rel_err, 0.02)

    def test_psi_dispersion_range(self):
        """Ψ_dispersion ∈ [0, 1]."""
        psi = self.disp.psi_dispersion()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_dispersion_supera_umbral(self):
        """Ψ_dispersion ≥ 0.888."""
        psi = self.disp.psi_dispersion()
        self.assertGreaterEqual(psi, 0.888)

    def test_zeros_loaded(self):
        """MatrizDispersion debe tener acceso a 20 ceros."""
        self.assertEqual(len(self.disp.zeros), 20)


# ============================================================================
# TestFormulaTraza – 13 tests
# ============================================================================

class TestFormulaTraza(unittest.TestCase):
    """Tests para la clase FormulaTraza."""

    def setUp(self):
        self.traza = FormulaTraza()

    def test_densidad_weyl_positive(self):
        """La densidad de Weyl ρ(T) debe ser positiva para T > 2π."""
        self.assertGreater(self.traza.densidad_weyl(50.0), 0)

    def test_densidad_weyl_zero_small_T(self):
        """ρ(T) = 0 para T ≤ 2π."""
        self.assertEqual(self.traza.densidad_weyl(1.0), 0.0)

    def test_densidad_weyl_increases(self):
        """ρ(T) debe ser creciente."""
        self.assertLess(
            self.traza.densidad_weyl(20.0),
            self.traza.densidad_weyl(100.0),
        )

    def test_N_weyl_50_approx(self):
        """N_W(50) debe estar cerca de 10 (hay 10 ceros ≤ 50)."""
        N = self.traza.N_weyl(50.0)
        self.assertGreater(N, 7)
        self.assertLess(N, 13)

    def test_N_weyl_zero_for_nonpositive(self):
        """N_W(T≤0) = 0."""
        self.assertEqual(self.traza.N_weyl(0.0), 0.0)
        self.assertEqual(self.traza.N_weyl(-10.0), 0.0)

    def test_N_weyl_increases(self):
        """N_W debe ser creciente en T."""
        self.assertLess(self.traza.N_weyl(30.0), self.traza.N_weyl(50.0))

    def test_espaciado_empirico_range(self):
        """Espaciado empírico debe estar en (3.0, 3.5)."""
        d = self.traza.espaciado_medio_empirico()
        self.assertGreater(d, 3.0)
        self.assertLess(d, 3.5)

    def test_espaciado_weyl_range(self):
        """Espaciado teórico de Weyl debe estar en (3.0, 3.5)."""
        d = self.traza.espaciado_medio_weyl()
        self.assertGreater(d, 3.0)
        self.assertLess(d, 3.5)

    def test_espaciado_relative_error(self):
        """Error relativo entre espaciado empírico y Weyl debe ser < 10%."""
        d_emp = self.traza.espaciado_medio_empirico()
        d_weyl = self.traza.espaciado_medio_weyl()
        rel_err = abs(d_emp - d_weyl) / d_weyl
        self.assertLess(rel_err, 0.10)

    def test_psi_traza_range(self):
        """Ψ_traza ∈ [0, 1]."""
        psi = self.traza.psi_traza()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_traza_supera_umbral(self):
        """Ψ_traza ≥ 0.888."""
        psi = self.traza.psi_traza()
        self.assertGreaterEqual(psi, 0.888)

    def test_zeros_loaded(self):
        """FormulaTraza debe tener 20 ceros."""
        self.assertEqual(len(self.traza.zeros), 20)


# ============================================================================
# TestNucleoResolvente – 12 tests
# ============================================================================

class TestNucleoResolvente(unittest.TestCase):
    """Tests para la clase NucleoResolvente."""

    def setUp(self):
        self.nucleo = NucleoResolvente()

    def test_densidad_espectral_positive(self):
        """ρ(t) debe ser positivo para t > 2π."""
        self.assertGreater(self.nucleo.densidad_espectral(50.0), 0)

    def test_densidad_espectral_zero_small(self):
        """ρ(t) = 0 para t ≤ 2π."""
        self.assertEqual(self.nucleo.densidad_espectral(1.0), 0.0)

    def test_densidad_espectral_increases(self):
        """ρ(t) debe ser creciente en t."""
        self.assertLess(
            self.nucleo.densidad_espectral(20.0),
            self.nucleo.densidad_espectral(80.0),
        )

    def test_integrar_densidad_positive(self):
        """∫_{20}^{50} ρ(t) dt debe ser positivo."""
        result = self.nucleo.integrar_densidad(20.0, 50.0)
        self.assertGreater(result, 0)

    def test_integrar_densidad_zero_for_equal_limits(self):
        """Integral con a=b debe ser 0."""
        self.assertEqual(self.nucleo.integrar_densidad(30.0, 30.0), 0.0)

    def test_integrar_densidad_zero_for_inverted_limits(self):
        """Integral con a>b debe ser 0."""
        self.assertEqual(self.nucleo.integrar_densidad(50.0, 20.0), 0.0)

    def test_conteo_integrado_approx_19(self):
        """Conteo integrado [θ(γ₂₀)−θ(γ₁)]/π ≈ 19."""
        N = self.nucleo.conteo_integrado()
        self.assertAlmostEqual(N, 19.0, delta=1.0)

    def test_conteo_integrado_positive(self):
        """Conteo integrado debe ser positivo."""
        self.assertGreater(self.nucleo.conteo_integrado(), 0)

    def test_psi_nucleo_range(self):
        """Ψ_nucleo ∈ [0, 1]."""
        psi = self.nucleo.psi_nucleo()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_nucleo_supera_umbral(self):
        """Ψ_nucleo ≥ 0.888."""
        psi = self.nucleo.psi_nucleo()
        self.assertGreaterEqual(psi, 0.888)

    def test_zeros_loaded(self):
        """NucleoResolvente debe tener 20 ceros."""
        self.assertEqual(len(self.nucleo.zeros), 20)


# ============================================================================
# TestSistemaRiemannAdelico – 15 tests
# ============================================================================

class TestSistemaRiemannAdelico(unittest.TestCase):
    """Tests para la clase SistemaRiemannAdelico."""

    def setUp(self):
        self.sistema = SistemaRiemannAdelico(Lambda=200.0, n_puntos=2000)

    def test_lambda_attribute(self):
        self.assertEqual(self.sistema.Lambda, 200.0)

    def test_subsystems_instantiated(self):
        """Todos los subsistemas deben estar instanciados."""
        self.assertIsNotNone(self.sistema.constantes)
        self.assertIsNotNone(self.sistema.hilbert)
        self.assertIsNotNone(self.sistema.operador)
        self.assertIsNotNone(self.sistema.potencial)
        self.assertIsNotNone(self.sistema.dispersion)
        self.assertIsNotNone(self.sistema.traza)
        self.assertIsNotNone(self.sistema.nucleo)

    def test_psi_global_range(self):
        """Ψ_global ∈ [0, 1]."""
        psi = self.sistema.psi_global()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_supera_umbral(self):
        """Ψ_global ≥ 0.888."""
        self.assertGreaterEqual(self.sistema.psi_global(), 0.888)

    def test_supera_umbral(self):
        """supera_umbral() debe ser True."""
        self.assertTrue(self.sistema.supera_umbral())

    def test_certificar_keys(self):
        """certificar() debe incluir todas las claves esperadas."""
        cert = self.sistema.certificar()
        expected_keys = [
            "psi_hilbert", "psi_operador", "psi_potencial",
            "psi_dispersion", "psi_traza", "psi_nucleo",
            "psi_global", "supera_umbral", "sello_activo",
            "sello", "cert_mark", "n_zeros", "f0_hz",
            "resonancia_f0_gamma1", "Lambda",
        ]
        for key in expected_keys:
            self.assertIn(key, cert)

    def test_certificar_sello_activo(self):
        cert = self.sistema.certificar()
        self.assertTrue(cert["sello_activo"])

    def test_certificar_cert_mark(self):
        cert = self.sistema.certificar()
        self.assertEqual(cert["cert_mark"], "HRA-RIEMANN-VERIFIED")

    def test_certificar_sello(self):
        cert = self.sistema.certificar()
        self.assertEqual(cert["sello"], "∴HRA∞³")

    def test_certificar_psi_values_range(self):
        """Todas las Ψᵢ en el certificado deben estar en [0, 1]."""
        cert = self.sistema.certificar()
        for key in ("psi_hilbert", "psi_operador", "psi_potencial",
                    "psi_dispersion", "psi_traza", "psi_nucleo", "psi_global"):
            v = cert[key]
            self.assertGreaterEqual(v, 0.0, msg=f"{key} = {v} < 0")
            self.assertLessEqual(v, 1.0, msg=f"{key} = {v} > 1")

    def test_pesos_sum_to_one(self):
        """Los pesos del sistema deben sumar 1.0."""
        self.assertAlmostEqual(sum(SistemaRiemannAdelico._PESOS), 1.0, places=10)

    def test_custom_lambda(self):
        """El sistema debe funcionar con Lambda=500."""
        sistema_500 = SistemaRiemannAdelico(Lambda=500.0)
        self.assertGreaterEqual(sistema_500.psi_global(), 0.888)


# ============================================================================
# TestResultadoRiemannAdelico – 6 tests
# ============================================================================

class TestResultadoRiemannAdelico(unittest.TestCase):
    """Tests para el dataclass ResultadoRiemannAdelico."""

    def test_default_values(self):
        """Valores por defecto deben ser 0/False/''."""
        r = ResultadoRiemannAdelico()
        self.assertEqual(r.psi_global, 0.0)
        self.assertFalse(r.sello_activo)
        self.assertEqual(r.sello, "")

    def test_custom_values(self):
        """Debe aceptar valores personalizados."""
        r = ResultadoRiemannAdelico(
            psi_global=0.95,
            sello_activo=True,
            sello="∴HRA∞³",
            cert_mark="HRA-RIEMANN-VERIFIED",
            n_zeros=20,
        )
        self.assertAlmostEqual(r.psi_global, 0.95, places=10)
        self.assertTrue(r.sello_activo)
        self.assertEqual(r.sello, "∴HRA∞³")

    def test_psi_fields(self):
        """Todos los campos psi deben ser float."""
        r = ResultadoRiemannAdelico(
            psi_hilbert=0.99,
            psi_operador=0.98,
            psi_potencial=0.97,
            psi_dispersion=0.99,
            psi_traza=0.95,
            psi_nucleo=0.99,
            psi_global=0.98,
        )
        for field in (r.psi_hilbert, r.psi_operador, r.psi_potencial,
                      r.psi_dispersion, r.psi_traza, r.psi_nucleo, r.psi_global):
            self.assertIsInstance(field, float)

    def test_integer_fields(self):
        """n_zeros y n_potencias_primas deben ser int."""
        r = ResultadoRiemannAdelico(n_zeros=20, n_potencias_primas=50)
        self.assertIsInstance(r.n_zeros, int)
        self.assertIsInstance(r.n_potencias_primas, int)


# ============================================================================
# TestHamiltonianoActivar – 10 tests
# ============================================================================

class TestHamiltonianoActivar(unittest.TestCase):
    """Tests para la API pública hamiltoniano_riemann_adelico_activar()."""

    def test_activar_returns_dict(self):
        """hamiltoniano_riemann_adelico_activar() debe retornar un dict."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertIsInstance(r, dict)

    def test_activar_sello_activo(self):
        """sello_activo debe ser True."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertTrue(r["sello_activo"])

    def test_activar_psi_global_umbral(self):
        """psi_global debe ser ≥ 0.888."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertGreaterEqual(r["psi_global"], 0.888)

    def test_activar_cert_mark(self):
        """cert_mark debe ser HRA-RIEMANN-VERIFIED."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertEqual(r["cert_mark"], "HRA-RIEMANN-VERIFIED")

    def test_activar_sello(self):
        """sello debe ser ∴HRA∞³."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertEqual(r["sello"], "∴HRA∞³")

    def test_activar_n_zeros(self):
        """n_zeros debe ser 20."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertEqual(r["n_zeros"], 20)

    def test_activar_f0_hz(self):
        """f0_hz debe ser 141.7001."""
        r = hamiltoniano_riemann_adelico_activar()
        self.assertAlmostEqual(r["f0_hz"], 141.7001, places=4)

    def test_activar_custom_lambda(self):
        """Debe funcionar con Lambda=500."""
        r = hamiltoniano_riemann_adelico_activar(Lambda=500.0)
        self.assertTrue(r["sello_activo"])
        self.assertGreaterEqual(r["psi_global"], 0.888)

    def test_activar_raises_invalid_lambda(self):
        """Debe levantar ValueError para Lambda ≤ 0."""
        with self.assertRaises(ValueError):
            hamiltoniano_riemann_adelico_activar(Lambda=0.0)
        with self.assertRaises(ValueError):
            hamiltoniano_riemann_adelico_activar(Lambda=-10.0)

    def test_activar_raises_invalid_n_puntos(self):
        """Debe levantar ValueError para n_puntos < 10."""
        with self.assertRaises(ValueError):
            hamiltoniano_riemann_adelico_activar(n_puntos=5)


# ============================================================================
# TestIntegracion – 6 tests
# ============================================================================

class TestIntegracion(unittest.TestCase):
    """Tests de integración: verifica la consistencia entre subsistemas."""

    def test_resonancia_f0_gamma1_consistency(self):
        """F₀/γ₁ debe concordar entre ConstantesRiemannAdelico y OperadorDilatacion."""
        cte = ConstantesRiemannAdelico()
        op = OperadorDilatacion()
        self.assertAlmostEqual(
            cte.resonancia_f0_gamma1(),
            op.resonancia_f0(),
            places=10,
        )

    def test_theta_consistency_dispersion_formula_traza(self):
        """θ(γ₂₀) debe concordar entre MatrizDispersion y FormulaTraza."""
        disp = MatrizDispersion()
        traza = FormulaTraza()
        # N_W(γ₂₀) = θ(γ₂₀)/π + 1
        N_W = traza.N_weyl(_ZEROS_20[-1])
        theta = disp.theta(_ZEROS_20[-1])
        self.assertAlmostEqual(N_W, theta / math.pi + 1, places=10)

    def test_conteo_theta_vs_nucleo(self):
        """conteo_integrado() == [θ(γ₂₀)−θ(γ₁)]/π."""
        disp = MatrizDispersion()
        nucleo = NucleoResolvente()
        conteo = nucleo.conteo_integrado()
        theta_diff = (disp.theta(_ZEROS_20[-1]) - disp.theta(_ZEROS_20[0])) / math.pi
        self.assertAlmostEqual(conteo, theta_diff, places=10)

    def test_sistema_all_psi_above_zero(self):
        """Todas las Ψᵢ individuales deben ser > 0."""
        sistema = SistemaRiemannAdelico()
        cert = sistema.certificar()
        for key in ("psi_hilbert", "psi_operador", "psi_potencial",
                    "psi_dispersion", "psi_traza", "psi_nucleo"):
            self.assertGreater(cert[key], 0.0, msg=f"{key} = {cert[key]}")

    def test_api_matches_sistema(self):
        """La API pública debe retornar los mismos valores que certificar()."""
        sistema = SistemaRiemannAdelico()
        cert = sistema.certificar()
        api = hamiltoniano_riemann_adelico_activar()
        self.assertAlmostEqual(api["psi_global"], cert["psi_global"], places=10)
        self.assertEqual(api["sello_activo"], cert["sello_activo"])

    def test_autofuncion_hilbert_space(self):
        """ψ_E con E=γ₁ y E=γ₅ deben ser funciones diferentes."""
        op = OperadorDilatacion()
        psi1 = op.autofuncion(2.0, _ZEROS_20[0])
        psi5 = op.autofuncion(2.0, _ZEROS_20[4])
        self.assertNotAlmostEqual(psi1.imag, psi5.imag, places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
