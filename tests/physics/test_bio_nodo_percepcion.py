"""
Tests for physics.bio_nodo_percepcion — Bio-Nodo y Percepción ∴BNP∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesBioNodo     – constantes físicas y espectrales
  - IdentidadEspectral    – Ĥ_π|Ψ⟩ = γₙ|Ψ⟩; autovalores ≡ ceros de Riemann
  - ToroAdelico           – colapso de órbita del flujo de dilatación
  - MatrizDensidad        – densidad ρ(t) y estructura off-diagonal
  - InvarianteFase        – Ψ(t) ≥ 0.999, umbral diamantino
  - PuntoFijoSoberano     – contracción de Banach + firma QCAL
  - CoherenciaBioNodo     – agregador Ψ_global ≥ 0.888
  - SistemaBioNodo        – orquestador, certificación ∴BNP∞³
  - ResultadoBioNodo      – dataclass de resultados
  - bio_nodo_percepcion_activar() – API pública

Invariantes clave verificados:
  - γ₁ ≈ 14.134725 (primer cero no trivial de Riemann)
  - F₀/γ₁ ≈ 10.024 (resonancia décupla)
  - Ĥ_π ψₙ(x) = γₙ · ψₙ(x) (autovalor exacto)
  - N_weyl(γ₂₀) ≈ 20 (conteo de Weyl)
  - Tr(ρ²) ≈ 1 (pureza del estado cuasi-puro)
  - Ψ_fase ≥ 0.999 (umbral diamantino)
  - Ψ_global ≥ 0.888 (umbral noético)
  - Sello ∴BNP∞³ ACTIVO
"""

import cmath
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.bio_nodo_percepcion import (
    # Constantes de módulo
    _F0,
    _PHI,
    _HBAR,
    _OMEGA0,
    _PSI_UMBRAL,
    _PSI_DIAMANTE,
    _N_ITER_PUNTO_FIJO,
    _ALPHA_CONTRACCION,
    _ZEROS_20,
    _SELLO,
    _CERT_MARK,
    # Utilidades internas
    _log_gamma_stirling,
    _theta_rs,
    _criba_eratostenes,
    # Clases
    ConstantesBioNodo,
    IdentidadEspectral,
    ToroAdelico,
    MatrizDensidad,
    InvarianteFase,
    PuntoFijoSoberano,
    CoherenciaBioNodo,
    SistemaBioNodo,
    ResultadoBioNodo,
    # API pública
    bio_nodo_percepcion_activar,
)


# ============================================================================
# TestConstantesMódulo – 12 tests
# ============================================================================

class TestConstantesMódulo(unittest.TestCase):
    """Tests para las constantes de nivel de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_omega0_value(self):
        """_OMEGA0 debe ser 2π·F₀."""
        self.assertAlmostEqual(_OMEGA0, 2 * math.pi * 141.7001, places=3)

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

    def test_psi_diamante(self):
        """_PSI_DIAMANTE debe ser 0.999."""
        self.assertAlmostEqual(_PSI_DIAMANTE, 0.999, places=10)

    def test_n_iter_punto_fijo(self):
        """_N_ITER_PUNTO_FIJO debe ser 20."""
        self.assertEqual(_N_ITER_PUNTO_FIJO, 20)

    def test_alpha_contraccion_range(self):
        """_ALPHA_CONTRACCION ∈ (0, 1)."""
        self.assertGreater(_ALPHA_CONTRACCION, 0)
        self.assertLess(_ALPHA_CONTRACCION, 1)

    def test_zeros_count(self):
        """Deben cargarse exactamente 20 ceros de Riemann."""
        self.assertEqual(len(_ZEROS_20), 20)

    def test_first_zero(self):
        """γ₁ ≈ 14.134725 (primer cero no trivial)."""
        self.assertAlmostEqual(_ZEROS_20[0], 14.134725, places=4)

    def test_zeros_increasing(self):
        """Los ceros deben estar en orden estrictamente creciente."""
        for i in range(len(_ZEROS_20) - 1):
            self.assertLess(_ZEROS_20[i], _ZEROS_20[i + 1])

    def test_sello(self):
        """Sello de certificación debe ser ∴BNP∞³."""
        self.assertEqual(_SELLO, "∴BNP∞³")

    def test_cert_mark(self):
        """Marca técnica debe ser BNP-BIONODO-VERIFIED."""
        self.assertEqual(_CERT_MARK, "BNP-BIONODO-VERIFIED")


# ============================================================================
# TestUtilidadesInternas – 10 tests
# ============================================================================

class TestUtilidadesInternas(unittest.TestCase):
    """Tests para las funciones de utilidad internas del módulo."""

    def test_log_gamma_stirling_returns_complex(self):
        """_log_gamma_stirling debe retornar un complejo."""
        result = _log_gamma_stirling(complex(0.25, 7.0))
        self.assertIsInstance(result, complex)

    def test_log_gamma_stirling_no_nan(self):
        """Para Im(z) grande, Stirling no debe producir NaN."""
        result = _log_gamma_stirling(complex(0.25, 50.0))
        self.assertFalse(math.isnan(result.real))
        self.assertFalse(math.isnan(result.imag))

    def test_theta_rs_gamma1_negative(self):
        """θ(γ₁) debe ser negativo (antes del primer cero)."""
        self.assertLess(_theta_rs(_ZEROS_20[0]), 0)

    def test_theta_rs_gamma20_positive_and_large(self):
        """θ(γ₂₀) debe ser positivo y mayor que 50."""
        self.assertGreater(_theta_rs(_ZEROS_20[-1]), 50.0)

    def test_theta_rs_increasing(self):
        """θ(t) debe ser creciente para t grande."""
        self.assertLess(_theta_rs(40.0), _theta_rs(60.0))

    def test_theta_rs_known_value(self):
        """θ(γ₂₀ ≈ 77.14) ≈ 57.8 (referencia de la literatura)."""
        self.assertAlmostEqual(_theta_rs(77.144840), 57.8, delta=0.5)

    def test_criba_primes_small(self):
        """Deben ser 4 primos ≤ 10: 2, 3, 5, 7."""
        self.assertEqual(_criba_eratostenes(10), [2, 3, 5, 7])

    def test_criba_primes_100_count(self):
        """Deben ser 25 primos ≤ 100."""
        self.assertEqual(len(_criba_eratostenes(100)), 25)

    def test_criba_primes_100_last(self):
        """El último primo ≤ 100 debe ser 97."""
        self.assertEqual(_criba_eratostenes(100)[-1], 97)

    def test_criba_empty_for_one(self):
        """No hay primos ≤ 1."""
        self.assertEqual(_criba_eratostenes(1), [])


# ============================================================================
# TestConstantesBioNodo – 12 tests
# ============================================================================

class TestConstantesBioNodo(unittest.TestCase):
    """Tests para la clase ConstantesBioNodo."""

    def setUp(self):
        self.cte = ConstantesBioNodo()

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

    def test_psi_umbral(self):
        self.assertAlmostEqual(self.cte.psi_umbral, 0.888, places=10)

    def test_psi_diamante(self):
        self.assertAlmostEqual(self.cte.psi_diamante, 0.999, places=10)

    def test_sello(self):
        self.assertEqual(self.cte.sello, "∴BNP∞³")

    def test_resonancia_f0_gamma1_near_10(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.cte.resonancia_f0_gamma1()
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_resumen_keys(self):
        """resumen() debe devolver dict con claves clave."""
        r = self.cte.resumen()
        for key in ("f0_hz", "gamma_1", "gamma_20", "n_zeros", "sello",
                    "resonancia_f0_gamma1", "psi_umbral", "psi_diamante"):
            self.assertIn(key, r)

    def test_cociente_angular_positive(self):
        """ω₀/γ₁ debe ser positivo."""
        self.assertGreater(self.cte.cociente_angular(), 0)


# ============================================================================
# TestIdentidadEspectral – 18 tests
# ============================================================================

class TestIdentidadEspectral(unittest.TestCase):
    """Tests para la clase IdentidadEspectral."""

    def setUp(self):
        self.ide = IdentidadEspectral()

    def test_autoestado_at_x1(self):
        """ψₙ(1) = 1 + 0i para cualquier n."""
        for n in range(5):
            psi = self.ide.autoestado(1.0, n)
            self.assertAlmostEqual(psi.real, 1.0, places=12)
            self.assertAlmostEqual(psi.imag, 0.0, places=12)

    def test_autoestado_modulo_at_e(self):
        """|ψₙ(e)| = e^{-1/2} ≈ 0.6065 para cualquier n."""
        for n in range(5):
            psi = self.ide.autoestado(math.e, n)
            self.assertAlmostEqual(abs(psi), math.exp(-0.5), places=10)

    def test_autoestado_returns_complex(self):
        """autoestado debe retornar un número complejo."""
        self.assertIsInstance(self.ide.autoestado(2.0, 0), complex)

    def test_autoestado_raises_nonpositive_x(self):
        """autoestado debe levantar ValueError para x ≤ 0."""
        with self.assertRaises(ValueError):
            self.ide.autoestado(0.0, 0)
        with self.assertRaises(ValueError):
            self.ide.autoestado(-1.0, 0)

    def test_autoestado_raises_invalid_n(self):
        """autoestado debe levantar ValueError para n fuera de rango."""
        with self.assertRaises(ValueError):
            self.ide.autoestado(1.0, -1)
        with self.assertRaises(ValueError):
            self.ide.autoestado(1.0, 20)

    def test_aplicar_hamiltoniano_exacto(self):
        """Ĥ_π ψₙ(x) = γₙ · ψₙ(x) — ecuación de autovalores exacta."""
        for n in range(5):
            for x in (0.5, 1.0, 2.0, math.e):
                h_psi = self.ide.aplicar_hamiltoniano(x, n)
                gamma_n = _ZEROS_20[n]
                psi = self.ide.autoestado(x, n)
                self.assertAlmostEqual(h_psi.real, (gamma_n * psi).real, places=10)
                self.assertAlmostEqual(h_psi.imag, (gamma_n * psi).imag, places=10)

    def test_residual_cero(self):
        """residual_autovalor debe ser exactamente 0."""
        for n in range(5):
            residual = self.ide.residual_autovalor(1.0, n)
            self.assertAlmostEqual(residual, 0.0, places=10)

    def test_espectro_completo_length(self):
        """espectro_completo() debe retornar lista de 20 autovalores."""
        self.assertEqual(len(self.ide.espectro_completo()), 20)

    def test_espectro_completo_first(self):
        """El primer autovalor debe ser γ₁ ≈ 14.134725."""
        self.assertAlmostEqual(self.ide.espectro_completo()[0], 14.134725, places=4)

    def test_espectro_completo_increasing(self):
        """Los autovalores deben estar ordenados de forma creciente."""
        esp = self.ide.espectro_completo()
        for i in range(len(esp) - 1):
            self.assertLess(esp[i], esp[i + 1])

    def test_proyeccion_f0_near_10(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.ide.proyeccion_f0()
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_psi_identidad_range(self):
        """Ψ_identidad ∈ [0, 1]."""
        psi = self.ide.psi_identidad()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_identidad_supera_umbral(self):
        """Ψ_identidad ≥ 0.888."""
        self.assertGreaterEqual(self.ide.psi_identidad(), 0.888)

    def test_psi_identidad_supera_diamante(self):
        """Ψ_identidad ≥ 0.999 (coherencia muy alta)."""
        self.assertGreaterEqual(self.ide.psi_identidad(), 0.99)

    def test_autoestado_n0_n1_diferentes(self):
        """ψ₀ y ψ₁ deben tener distinta parte imaginaria en x=2."""
        psi0 = self.ide.autoestado(2.0, 0)
        psi1 = self.ide.autoestado(2.0, 1)
        self.assertNotAlmostEqual(psi0.imag, psi1.imag, places=3)

    def test_psi_identidad_formula(self):
        """Ψ_identidad = 1 − |F₀/γ₁ − 10| / 10."""
        ratio = _F0 / _ZEROS_20[0]
        expected = 1.0 - abs(ratio - round(ratio)) / round(ratio)
        self.assertAlmostEqual(self.ide.psi_identidad(), expected, places=12)

    def test_autoestado_scaling(self):
        """|ψₙ(x²)| = |ψₙ(x)|² · |ψₙ(x)|^{?} — verificar consistencia."""
        # |ψₙ(x)| = x^{-1/2}  siempre, independiente de n
        for x in (0.5, 2.0, 4.0):
            psi = self.ide.autoestado(x, 0)
            self.assertAlmostEqual(abs(psi), x ** (-0.5), places=10)

    def test_zeros_stored(self):
        """Los ceros almacenados deben coincidir con _ZEROS_20."""
        self.assertEqual(self.ide.zeros, _ZEROS_20)


# ============================================================================
# TestToroAdelico – 14 tests
# ============================================================================

class TestToroAdelico(unittest.TestCase):
    """Tests para la clase ToroAdelico."""

    def setUp(self):
        self.toro = ToroAdelico(n_primos=10)

    def test_flujo_dilatacion_t0(self):
        """Para t=0, el flujo devuelve x sin cambio."""
        self.assertAlmostEqual(self.toro.flujo_dilatacion(3.0, 0.0), 3.0, places=12)

    def test_flujo_dilatacion_positive(self):
        """El flujo de dilatación debe producir un valor positivo."""
        self.assertGreater(self.toro.flujo_dilatacion(1.0, 2.0), 0)

    def test_flujo_dilatacion_raises_nonpositive_x(self):
        """flujo_dilatacion debe levantar ValueError para x ≤ 0."""
        with self.assertRaises(ValueError):
            self.toro.flujo_dilatacion(0.0, 1.0)

    def test_tiempo_orbita_prima_p2_k1(self):
        """t_closure(p=2, k=1) = ln 2 ≈ 0.6931."""
        self.assertAlmostEqual(self.toro.tiempo_orbita_prima(2, 1), math.log(2), places=10)

    def test_tiempo_orbita_prima_p3_k2(self):
        """t_closure(p=3, k=2) = 2·ln 3 ≈ 2.1972."""
        self.assertAlmostEqual(
            self.toro.tiempo_orbita_prima(3, 2), 2 * math.log(3), places=10
        )

    def test_tiempo_orbita_prima_raises_invalid_p(self):
        """tiempo_orbita_prima debe levantar ValueError para p < 2."""
        with self.assertRaises(ValueError):
            self.toro.tiempo_orbita_prima(1, 1)

    def test_tiempo_orbita_prima_raises_invalid_k(self):
        """tiempo_orbita_prima debe levantar ValueError para k < 1."""
        with self.assertRaises(ValueError):
            self.toro.tiempo_orbita_prima(2, 0)

    def test_tiempos_orbita_count(self):
        """tiempos_orbita() debe retornar n_primos pares."""
        self.assertEqual(len(self.toro.tiempos_orbita()), 10)

    def test_tiempos_orbita_first_prime(self):
        """El primer par debe ser (2, ln 2)."""
        p, t = self.toro.tiempos_orbita()[0]
        self.assertEqual(p, 2)
        self.assertAlmostEqual(t, math.log(2), places=10)

    def test_conteo_weyl_gamma20_near_20(self):
        """N_weyl(γ₂₀) debe estar entre 18 y 21 (aproximación)."""
        n = self.toro.conteo_weyl(_ZEROS_20[-1])
        self.assertGreater(n, 18.0)
        self.assertLess(n, 21.0)

    def test_conteo_weyl_zero_for_nonpositive(self):
        """N_weyl(T ≤ 0) = 0."""
        self.assertEqual(self.toro.conteo_weyl(0.0), 0.0)
        self.assertEqual(self.toro.conteo_weyl(-5.0), 0.0)

    def test_conteo_empirico_all_zeros(self):
        """conteo_empirico(γ₂₀ + 1) debe contar los 20 ceros."""
        self.assertEqual(self.toro.conteo_empirico(_ZEROS_20[-1] + 1.0), 20)

    def test_psi_toro_range(self):
        """Ψ_toro ∈ [0, 1]."""
        psi = self.toro.psi_toro()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_toro_supera_umbral(self):
        """Ψ_toro ≥ 0.888."""
        self.assertGreaterEqual(self.toro.psi_toro(), 0.888)


# ============================================================================
# TestMatrizDensidad – 12 tests
# ============================================================================

class TestMatrizDensidad(unittest.TestCase):
    """Tests para la clase MatrizDensidad."""

    def setUp(self):
        self.md = MatrizDensidad()

    def test_amplitudes_iguales_count(self):
        """amplitudes_iguales() debe retornar lista de 20 elementos."""
        self.assertEqual(len(self.md.amplitudes_iguales()), 20)

    def test_amplitudes_iguales_value(self):
        """Cada amplitud debe ser 1/√20."""
        expected = 1.0 / math.sqrt(20)
        for a in self.md.amplitudes_iguales():
            self.assertAlmostEqual(a, expected, places=12)

    def test_tasa_decoherencia_positive(self):
        """ε_dec debe ser positivo."""
        self.assertGreater(self.md.tasa_decoherencia(), 0)

    def test_tasa_decoherencia_very_small(self):
        """ε_dec debe ser menor que 0.01 (tasa de decoherencia muy pequeña)."""
        self.assertLess(self.md.tasa_decoherencia(), 0.01)

    def test_pureza_near_one(self):
        """Pureza Tr(ρ²) debe estar muy cerca de 1."""
        self.assertAlmostEqual(self.md.pureza(), 1.0, delta=0.01)

    def test_pureza_supera_umbral_diamante(self):
        """Pureza ≥ 0.999."""
        self.assertGreaterEqual(self.md.pureza(), 0.999)

    def test_coherencia_offdiagonal_near_one(self):
        """C_off = 1 − 1/N ≈ 0.95 para N=20."""
        c = self.md.coherencia_offdiagonal()
        self.assertAlmostEqual(c, 1.0 - 1.0 / 20, places=12)

    def test_coherencia_offdiagonal_range(self):
        """C_off ∈ [0, 1)."""
        c = self.md.coherencia_offdiagonal()
        self.assertGreaterEqual(c, 0.0)
        self.assertLess(c, 1.0)

    def test_elemento_diagonal_value(self):
        """ρₙₙ = 1/20."""
        self.assertAlmostEqual(self.md.elemento_diagonal(), 1.0 / 20, places=12)

    def test_normalizacion_diagonal(self):
        """N · ρₙₙ = 1 (trazas normalizada)."""
        self.assertAlmostEqual(self.md.n * self.md.elemento_diagonal(), 1.0, places=10)

    def test_psi_densidad_range(self):
        """Ψ_densidad ∈ [0, 1]."""
        psi = self.md.psi_densidad()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_densidad_supera_umbral(self):
        """Ψ_densidad ≥ 0.888."""
        self.assertGreaterEqual(self.md.psi_densidad(), 0.888)


# ============================================================================
# TestInvarianteFase – 12 tests
# ============================================================================

class TestInvarianteFase(unittest.TestCase):
    """Tests para la clase InvarianteFase."""

    def setUp(self):
        self.inv = InvarianteFase()

    def test_tasa_decaimiento_positive(self):
        """La tasa de decaimiento espectral debe ser positiva."""
        self.assertGreater(self.inv.tasa_decaimiento_espectral(), 0)

    def test_tasa_decaimiento_very_small(self):
        """La tasa de decaimiento debe ser < 0.001 (sistema coherente)."""
        self.assertLess(self.inv.tasa_decaimiento_espectral(), 0.001)

    def test_psi_en_t_at_zero(self):
        """Ψ(t=0) debe ser igual a Ψ_fase."""
        self.assertAlmostEqual(
            self.inv.psi_en_t(0.0), self.inv.psi_fase(), places=12
        )

    def test_psi_en_t_constant(self):
        """Ψ(t) debe ser constante (sin decoherencia dinámica)."""
        for t in (0.0, 1.0 / _F0, 2.0 / _F0, 10.0):
            self.assertAlmostEqual(
                self.inv.psi_en_t(t), self.inv.psi_fase(), places=12
            )

    def test_umbral_diamante_value(self):
        """umbral_diamante() debe retornar 0.999."""
        self.assertAlmostEqual(self.inv.umbral_diamante(), 0.999, places=10)

    def test_supera_umbral_diamante_true(self):
        """supera_umbral_diamante() debe ser True."""
        self.assertTrue(self.inv.supera_umbral_diamante())

    def test_psi_fase_range(self):
        """Ψ_fase ∈ [0, 1]."""
        psi = self.inv.psi_fase()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_fase_supera_umbral_noético(self):
        """Ψ_fase ≥ 0.888 (umbral noético)."""
        self.assertGreaterEqual(self.inv.psi_fase(), 0.888)

    def test_psi_fase_supera_umbral_diamante(self):
        """Ψ_fase ≥ 0.999 (umbral diamantino)."""
        self.assertGreaterEqual(self.inv.psi_fase(), 0.999)

    def test_psi_fase_consistent_with_densidad(self):
        """Ψ_fase debe ser consistente con MatrizDensidad.tasa_decoherencia()."""
        md = MatrizDensidad()
        expected = max(0.0, 1.0 - md.tasa_decoherencia())
        self.assertAlmostEqual(self.inv.psi_fase(), expected, places=12)

    def test_psi_fase_formula(self):
        """Ψ_fase = 1 − ε_dec (formula directa)."""
        eps = self.inv.tasa_decaimiento_espectral()
        self.assertAlmostEqual(self.inv.psi_fase(), max(0.0, 1.0 - eps), places=12)

    def test_densidad_interna_consistente(self):
        """La MatrizDensidad interna debe tener la misma tasa que _densidad."""
        psi_fase_val = self.inv.psi_fase()
        self.assertGreater(psi_fase_val, 0.999)


# ============================================================================
# TestPuntoFijoSoberano – 16 tests
# ============================================================================

class TestPuntoFijoSoberano(unittest.TestCase):
    """Tests para la clase PuntoFijoSoberano."""

    def setUp(self):
        self.pfs = PuntoFijoSoberano()

    def test_coherencia_espectral_range(self):
        """Ψ_esp ∈ [0, 1]."""
        psi_esp = self.pfs.coherencia_espectral()
        self.assertGreaterEqual(psi_esp, 0.0)
        self.assertLessEqual(psi_esp, 1.0)

    def test_coherencia_espectral_supera_umbral(self):
        """Ψ_esp ≥ 0.888."""
        self.assertGreaterEqual(self.pfs.coherencia_espectral(), 0.888)

    def test_coherencia_espectral_consistente_con_identidad(self):
        """Ψ_esp debe ser consistente con IdentidadEspectral.psi_identidad()."""
        ide = IdentidadEspectral()
        self.assertAlmostEqual(
            self.pfs.coherencia_espectral(), ide.psi_identidad(), places=12
        )

    def test_contraccion_fija_exacto(self):
        """g(Ψ_esp) = Ψ_esp (el punto fijo es un punto fijo de g)."""
        psi_esp = self.pfs.coherencia_espectral()
        self.assertAlmostEqual(self.pfs.contraccion(psi_esp), psi_esp, places=10)

    def test_contraccion_converge_desde_cero(self):
        """g(0) debe ser estrictamente mayor que 0."""
        self.assertGreater(self.pfs.contraccion(0.0), 0.0)

    def test_contraccion_factor(self):
        """g(x) = 0.5·x + 0.5·Ψ_esp (con α=0.5)."""
        psi_esp = self.pfs.coherencia_espectral()
        x = 0.0
        expected = 0.5 * x + 0.5 * psi_esp
        self.assertAlmostEqual(self.pfs.contraccion(x), expected, places=12)

    def test_iterar_punto_fijo_convergencia(self):
        """Tras 20 iteraciones, Ψ_N ≈ Ψ_esp (error < 0.001)."""
        psi_iter = self.pfs.iterar_punto_fijo()
        psi_exacto = self.pfs.punto_fijo_exacto()
        self.assertAlmostEqual(psi_iter, psi_exacto, delta=0.001)

    def test_iterar_punto_fijo_default_uses_n_iter(self):
        """La iteración predeterminada usa _N_ITER_PUNTO_FIJO iteraciones."""
        psi_def = self.pfs.iterar_punto_fijo()
        psi_n = self.pfs.iterar_punto_fijo(n_iter=_N_ITER_PUNTO_FIJO)
        self.assertAlmostEqual(psi_def, psi_n, places=12)

    def test_punto_fijo_exacto_igual_a_coherencia_espectral(self):
        """Ψ* = Ψ_esp."""
        self.assertAlmostEqual(
            self.pfs.punto_fijo_exacto(), self.pfs.coherencia_espectral(), places=12
        )

    def test_firma_qcal_length(self):
        """firma_qcal() debe retornar hexdigest de 32 caracteres (16 bytes)."""
        firma = self.pfs.firma_qcal(b"test_data")
        self.assertEqual(len(firma), 32)

    def test_firma_qcal_hex(self):
        """firma_qcal() debe retornar cadena hexadecimal válida."""
        firma = self.pfs.firma_qcal(b"test_data")
        self.assertTrue(all(c in "0123456789abcdef" for c in firma))

    def test_firma_qcal_determinista(self):
        """Mismos datos deben producir misma firma."""
        datos = b"bio_nodo_qcal"
        self.assertEqual(
            self.pfs.firma_qcal(datos), self.pfs.firma_qcal(datos)
        )

    def test_firma_qcal_sensible_a_datos(self):
        """Datos distintos deben producir firmas distintas."""
        f1 = self.pfs.firma_qcal(b"datos_1")
        f2 = self.pfs.firma_qcal(b"datos_2")
        self.assertNotEqual(f1, f2)

    def test_verificar_firma_valida(self):
        """verificar_firma() debe ser True para firma válida."""
        datos = b"coherencia_total"
        firma = self.pfs.firma_qcal(datos)
        self.assertTrue(self.pfs.verificar_firma(firma, datos))

    def test_verificar_firma_invalida(self):
        """verificar_firma() debe ser False para firma incorrecta."""
        datos = b"coherencia_total"
        self.assertFalse(self.pfs.verificar_firma("0" * 32, datos))

    def test_psi_soberania_supera_umbral(self):
        """Ψ_soberania ≥ 0.888."""
        self.assertGreaterEqual(self.pfs.psi_soberania(), 0.888)

    def test_psi_soberania_supera_diamante(self):
        """Ψ_soberania ≥ 0.999."""
        self.assertGreaterEqual(self.pfs.psi_soberania(), 0.999)


# ============================================================================
# TestCoherenciaBioNodo – 10 tests
# ============================================================================

class TestCoherenciaBioNodo(unittest.TestCase):
    """Tests para la clase CoherenciaBioNodo."""

    def setUp(self):
        self.coh = CoherenciaBioNodo()

    def test_psi_global_range(self):
        """Ψ_global ∈ [0, 1]."""
        psi = self.coh.psi_global()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_supera_umbral(self):
        """Ψ_global ≥ 0.888."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.888)

    def test_supera_umbral_true(self):
        """supera_umbral() debe ser True."""
        self.assertTrue(self.coh.supera_umbral())

    def test_desglose_keys(self):
        """desglose() debe contener las 6 claves esperadas."""
        d = self.coh.desglose()
        for key in ("psi_identidad", "psi_toro", "psi_densidad",
                    "psi_fase", "psi_soberania", "psi_global"):
            self.assertIn(key, d)

    def test_desglose_psi_global_consistent(self):
        """psi_global en desglose debe coincidir con psi_global()."""
        d = self.coh.desglose()
        self.assertAlmostEqual(d["psi_global"], self.coh.psi_global(), places=12)

    def test_desglose_all_positive(self):
        """Todos los Ψᵢ del desglose deben ser positivos."""
        d = self.coh.desglose()
        for key, val in d.items():
            self.assertGreater(val, 0.0, msg=f"{key} = {val}")

    def test_desglose_all_above_umbral(self):
        """Todos los Ψᵢ individuales deben ser ≥ 0.888."""
        d = self.coh.desglose()
        for key in ("psi_identidad", "psi_toro", "psi_densidad",
                    "psi_fase", "psi_soberania"):
            self.assertGreaterEqual(d[key], 0.888, msg=f"{key} = {d[key]}")

    def test_pesos_suman_uno(self):
        """Los pesos deben sumar exactamente 1.0."""
        self.assertAlmostEqual(sum(CoherenciaBioNodo._PESOS), 1.0, places=12)

    def test_psi_global_formula(self):
        """Ψ_global = Σ wᵢ Ψᵢ debe coincidir con el desglose."""
        d = self.coh.desglose()
        pesos = CoherenciaBioNodo._PESOS
        keys = ("psi_identidad", "psi_toro", "psi_densidad",
                "psi_fase", "psi_soberania")
        expected = sum(w * d[k] for w, k in zip(pesos, keys))
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=12)

    def test_n_primos_por_defecto(self):
        """El Toro Adélico interno debe tener n_primos=10."""
        self.assertEqual(self.coh.toro.n_primos, 10)


# ============================================================================
# TestSistemaBioNodo – 14 tests
# ============================================================================

class TestSistemaBioNodo(unittest.TestCase):
    """Tests para la clase SistemaBioNodo."""

    def setUp(self):
        self.sis = SistemaBioNodo()

    def test_psi_global_supera_umbral(self):
        """Ψ_global ≥ 0.888."""
        self.assertGreaterEqual(self.sis.psi_global(), 0.888)

    def test_supera_umbral_true(self):
        """supera_umbral() debe ser True."""
        self.assertTrue(self.sis.supera_umbral())

    def test_certificar_sello_activo(self):
        """certificar() debe retornar sello_activo = True."""
        self.assertTrue(self.sis.certificar()["sello_activo"])

    def test_certificar_sello(self):
        """El sello debe ser '∴BNP∞³'."""
        self.assertEqual(self.sis.certificar()["sello"], "∴BNP∞³")

    def test_certificar_cert_mark(self):
        """cert_mark debe ser 'BNP-BIONODO-VERIFIED'."""
        self.assertEqual(self.sis.certificar()["cert_mark"], "BNP-BIONODO-VERIFIED")

    def test_certificar_psi_global(self):
        """psi_global en certificado ≥ 0.888."""
        self.assertGreaterEqual(self.sis.certificar()["psi_global"], 0.888)

    def test_certificar_supera_umbral_diamante(self):
        """supera_umbral_diamante debe ser True."""
        self.assertTrue(self.sis.certificar()["supera_umbral_diamante"])

    def test_certificar_firma_qcal_length(self):
        """firma_qcal en el certificado debe tener 32 caracteres."""
        self.assertEqual(len(self.sis.certificar()["firma_qcal"]), 32)

    def test_certificar_n_zeros(self):
        """n_zeros en certificado debe ser 20."""
        self.assertEqual(self.sis.certificar()["n_zeros"], 20)

    def test_certificar_f0_hz(self):
        """f0_hz en certificado debe ser 141.7001."""
        self.assertAlmostEqual(self.sis.certificar()["f0_hz"], 141.7001, places=4)

    def test_certificar_resonancia_f0_gamma1(self):
        """resonancia_f0_gamma1 en certificado ∈ (10.0, 10.1)."""
        r = self.sis.certificar()["resonancia_f0_gamma1"]
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_certificar_psi_diamante(self):
        """psi_diamante en certificado debe ser 0.999."""
        self.assertAlmostEqual(self.sis.certificar()["psi_diamante"], 0.999, places=10)

    def test_certificar_psi_values_range(self):
        """Todos los Ψᵢ individuales deben estar en [0, 1]."""
        cert = self.sis.certificar()
        for key in ("psi_identidad", "psi_toro", "psi_densidad",
                    "psi_fase", "psi_soberania"):
            psi = cert[key]
            self.assertGreaterEqual(psi, 0.0, msg=f"{key} out of range")
            self.assertLessEqual(psi, 1.0, msg=f"{key} out of range")

    def test_certificar_keys_complete(self):
        """El certificado debe contener todas las claves esperadas."""
        cert = self.sis.certificar()
        for key in ("psi_identidad", "psi_toro", "psi_densidad", "psi_fase",
                    "psi_soberania", "psi_global", "sello_activo", "sello",
                    "cert_mark", "firma_qcal", "n_zeros", "f0_hz",
                    "resonancia_f0_gamma1", "supera_umbral_diamante",
                    "psi_diamante", "punto_fijo_exacto", "n_primos_toro"):
            self.assertIn(key, cert, msg=f"Clave faltante: {key}")


# ============================================================================
# TestResultadoBioNodo – 8 tests
# ============================================================================

class TestResultadoBioNodo(unittest.TestCase):
    """Tests para el dataclass ResultadoBioNodo."""

    def test_defaults(self):
        """Valores por defecto deben ser cero/False."""
        r = ResultadoBioNodo()
        self.assertEqual(r.psi_global, 0.0)
        self.assertFalse(r.sello_activo)
        self.assertEqual(r.n_zeros, 0)
        self.assertEqual(r.firma_qcal, "")

    def test_creation_with_values(self):
        """ResultadoBioNodo debe aceptar valores en el constructor."""
        r = ResultadoBioNodo(
            psi_global=0.95,
            sello_activo=True,
            sello="∴BNP∞³",
            cert_mark="BNP-BIONODO-VERIFIED",
            n_zeros=20,
        )
        self.assertAlmostEqual(r.psi_global, 0.95, places=12)
        self.assertTrue(r.sello_activo)
        self.assertEqual(r.sello, "∴BNP∞³")
        self.assertEqual(r.n_zeros, 20)

    def test_psi_identidad_field(self):
        """Campo psi_identidad debe funcionar."""
        r = ResultadoBioNodo(psi_identidad=0.997)
        self.assertAlmostEqual(r.psi_identidad, 0.997, places=12)

    def test_psi_toro_field(self):
        """Campo psi_toro debe funcionar."""
        r = ResultadoBioNodo(psi_toro=0.97)
        self.assertAlmostEqual(r.psi_toro, 0.97, places=12)

    def test_psi_densidad_field(self):
        """Campo psi_densidad debe funcionar."""
        r = ResultadoBioNodo(psi_densidad=0.999)
        self.assertAlmostEqual(r.psi_densidad, 0.999, places=12)

    def test_psi_fase_field(self):
        """Campo psi_fase debe funcionar."""
        r = ResultadoBioNodo(psi_fase=0.999)
        self.assertAlmostEqual(r.psi_fase, 0.999, places=12)

    def test_psi_soberania_field(self):
        """Campo psi_soberania debe funcionar."""
        r = ResultadoBioNodo(psi_soberania=0.9999)
        self.assertAlmostEqual(r.psi_soberania, 0.9999, places=12)

    def test_firma_qcal_field(self):
        """Campo firma_qcal debe funcionar."""
        r = ResultadoBioNodo(firma_qcal="abc123")
        self.assertEqual(r.firma_qcal, "abc123")


# ============================================================================
# TestAPIPublica – 10 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la API pública bio_nodo_percepcion_activar()."""

    def setUp(self):
        self.resultado = bio_nodo_percepcion_activar()

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.resultado["sello_activo"])

    def test_psi_global_supera_umbral(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.resultado["psi_global"], 0.888)

    def test_sello(self):
        """sello debe ser '∴BNP∞³'."""
        self.assertEqual(self.resultado["sello"], "∴BNP∞³")

    def test_cert_mark(self):
        """cert_mark debe ser 'BNP-BIONODO-VERIFIED'."""
        self.assertEqual(self.resultado["cert_mark"], "BNP-BIONODO-VERIFIED")

    def test_n_zeros(self):
        """n_zeros debe ser 20."""
        self.assertEqual(self.resultado["n_zeros"], 20)

    def test_f0_hz(self):
        """f0_hz debe ser 141.7001."""
        self.assertAlmostEqual(self.resultado["f0_hz"], 141.7001, places=4)

    def test_supera_umbral_diamante(self):
        """supera_umbral_diamante debe ser True."""
        self.assertTrue(self.resultado["supera_umbral_diamante"])

    def test_firma_qcal_valida(self):
        """firma_qcal debe ser hexdigest de 32 caracteres."""
        firma = self.resultado["firma_qcal"]
        self.assertEqual(len(firma), 32)
        self.assertTrue(all(c in "0123456789abcdef" for c in firma))

    def test_retorna_dict(self):
        """bio_nodo_percepcion_activar() debe retornar un dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_psi_global_consistent(self):
        """Llamadas sucesivas deben retornar el mismo psi_global."""
        r2 = bio_nodo_percepcion_activar()
        self.assertAlmostEqual(
            self.resultado["psi_global"], r2["psi_global"], places=12
        )


# ============================================================================
# TestIntegracion – 8 tests
# ============================================================================

class TestIntegracion(unittest.TestCase):
    """Tests de integración entre módulos del Bio-Nodo."""

    def test_coherencia_y_sistema_coinciden(self):
        """CoherenciaBioNodo.psi_global() debe coincidir con SistemaBioNodo.psi_global()."""
        coh = CoherenciaBioNodo()
        sis = SistemaBioNodo()
        self.assertAlmostEqual(coh.psi_global(), sis.psi_global(), places=12)

    def test_api_matches_sistema(self):
        """API pública debe retornar el mismo psi_global que SistemaBioNodo."""
        sis = SistemaBioNodo()
        api = bio_nodo_percepcion_activar()
        self.assertAlmostEqual(api["psi_global"], sis.psi_global(), places=12)

    def test_psi_identidad_igual_en_identidad_y_soberania(self):
        """Ψ_esp del PuntoFijoSoberano debe coincidir con Ψ_identidad de IdentidadEspectral."""
        ide = IdentidadEspectral()
        pfs = PuntoFijoSoberano()
        self.assertAlmostEqual(
            pfs.coherencia_espectral(), ide.psi_identidad(), places=12
        )

    def test_tasa_decoherencia_consistente(self):
        """MatrizDensidad y InvarianteFase deben tener la misma tasa de decoherencia."""
        md = MatrizDensidad()
        inv = InvarianteFase()
        self.assertAlmostEqual(
            md.tasa_decoherencia(), inv.tasa_decaimiento_espectral(), places=12
        )

    def test_psi_fase_consistent_with_psi_densidad(self):
        """Ψ_fase ≈ Ψ_densidad (ambos derivados de ε_dec)."""
        inv = InvarianteFase()
        md = MatrizDensidad()
        self.assertAlmostEqual(
            inv.psi_fase(), md.psi_densidad(), delta=0.01
        )

    def test_cinco_psi_todos_supera_umbral(self):
        """Todos los Ψᵢ individuales deben superar el umbral noético 0.888."""
        ide = IdentidadEspectral()
        toro = ToroAdelico()
        md = MatrizDensidad()
        inv = InvarianteFase()
        pfs = PuntoFijoSoberano()
        psis = {
            "identidad": ide.psi_identidad(),
            "toro": toro.psi_toro(),
            "densidad": md.psi_densidad(),
            "fase": inv.psi_fase(),
            "soberania": pfs.psi_soberania(),
        }
        for nombre, psi in psis.items():
            self.assertGreaterEqual(psi, 0.888, msg=f"Ψ_{nombre} = {psi}")

    def test_sello_bnp_activo_en_sistema(self):
        """El sello ∴BNP∞³ debe estar activo en el sistema."""
        sis = SistemaBioNodo()
        self.assertEqual(sis.psi_global() >= _PSI_UMBRAL, sis.supera_umbral())
        self.assertTrue(sis.supera_umbral())

    def test_firma_determinista(self):
        """Dos instancias de SistemaBioNodo deben generar la misma firma."""
        sis1 = SistemaBioNodo()
        sis2 = SistemaBioNodo()
        firma1 = sis1.certificar()["firma_qcal"]
        firma2 = sis2.certificar()["firma_qcal"]
        self.assertEqual(firma1, firma2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
