"""
Tests para physics.tejido_cuantico_cosmico — ∞³ Tejido Cuántico Cósmico

Pruebas que cubren las 8 clases y la API pública.
Invariantes clave verificados:
  - aprobado = True
  - expansion_acelerada = True
  - es_energia_oscura = True
  - w_efectivo ≈ −1.0  (régimen slow-roll puro)
  - coherencia ≥ 0.888
  - sello = '∴TCQ∞³'
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.tejido_cuantico_cosmico import (
    # Módulo de constantes internas
    _F0_HZ,
    _G_N,
    _HBAR,
    _C_LUZ,
    _M_CAMPO,
    _PHI,
    _PSI_MINIMA,
    _H0_SI,
    _RHO_CRITICA,
    _RHO_LAMBDA,
    _EPSILON_SLOW_ROLL,
    _SELLO,
    # Clases
    ConstantesTejidoCuantico,
    CampoEfectivo,
    AccionKleinGordon,
    TensorEnergiaMomento,
    CondicionEnergiaOscura,
    EcuacionFriedmann,
    AxiomaEmision,
    ResultadoTejidoCuantico,
    SistemaTejidoCuanticoCosmico,
    # API pública
    tejido_cuantico_cosmico_activar,
)


# ============================================================================
# TestConstantesTejidoCuantico – 12 tests
# ============================================================================

class TestConstantesTejidoCuantico(unittest.TestCase):
    """Tests para ConstantesTejidoCuantico."""

    def setUp(self):
        self.c = ConstantesTejidoCuantico()

    def test_f0_value(self):
        """f₀ debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_G_N_positive(self):
        """G_N debe ser positivo."""
        self.assertGreater(self.c.G_N, 0.0)

    def test_hbar_value(self):
        """ℏ debe ser ≈ 1.0546 × 10⁻³⁴ J·s."""
        self.assertAlmostEqual(self.c.hbar, 1.054571817e-34, places=44)

    def test_c_value(self):
        """Velocidad de la luz debe ser 299792458 m/s."""
        self.assertEqual(self.c.c, 299_792_458.0)

    def test_m_campo_positive(self):
        """Masa del campo debe ser positiva."""
        self.assertGreater(self.c.m_campo, 0.0)

    def test_phi_golden_ratio(self):
        """Φ debe ser ≈ 1.618034."""
        self.assertAlmostEqual(self.c.phi, (1.0 + math.sqrt(5.0)) / 2.0, places=10)

    def test_psi_minima(self):
        """Ψ_mínima debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_minima, 0.888, places=3)

    def test_H0_positive(self):
        """H₀ debe ser positivo (constante de Hubble)."""
        self.assertGreater(self.c.H0, 0.0)

    def test_rho_critica_positive(self):
        """Densidad crítica debe ser positiva."""
        self.assertGreater(self.c.rho_critica, 0.0)

    def test_rho_lambda_positive(self):
        """Densidad de energía oscura debe ser positiva."""
        self.assertGreater(self.c.rho_lambda, 0.0)

    def test_omega_f0(self):
        """ω₀ = 2π f₀."""
        self.assertAlmostEqual(self.c.omega_f0, 2.0 * math.pi * 141.7001, places=6)

    def test_energia_cuantica_f0(self):
        """E₀ = ℏ·ω₀ > 0."""
        E = self.c.energia_cuantica_f0()
        self.assertGreater(E, 0.0)
        self.assertAlmostEqual(E, _HBAR * 2.0 * math.pi * _F0_HZ, places=40)

    def test_escala_longitud_compton(self):
        """λ_C = ℏ/(m·c) > 0."""
        lc = self.c.escala_longitud_compton()
        self.assertGreater(lc, 0.0)

    def test_sello(self):
        """Sello del módulo."""
        self.assertEqual(self.c.sello, "∴TCQ∞³")

    def test_repr(self):
        """__repr__ incluye f₀ y sello."""
        r = repr(self.c)
        self.assertIn("141.7001", r)
        self.assertIn("∴TCQ∞³", r)


# ============================================================================
# TestCampoEfectivo – 15 tests
# ============================================================================

class TestCampoEfectivo(unittest.TestCase):
    """Tests para CampoEfectivo."""

    def test_modulo_cuadrado_r0(self):
        """R=0 → |ψ|² = 0."""
        campo = CampoEfectivo(R=0.0)
        self.assertEqual(campo.modulo_cuadrado(), 0.0)

    def test_modulo_cuadrado_r1(self):
        """|ψ|² = R² = 1."""
        campo = CampoEfectivo(R=1.0)
        self.assertAlmostEqual(campo.modulo_cuadrado(), 1.0, places=10)

    def test_modulo_cuadrado_r2(self):
        """|ψ|² = 4 para R=2."""
        campo = CampoEfectivo(R=2.0)
        self.assertAlmostEqual(campo.modulo_cuadrado(), 4.0, places=10)

    def test_densidad_presencia_igual_modulo(self):
        """ρ_Q = |ψ|² = R²."""
        campo = CampoEfectivo(R=3.0)
        self.assertEqual(campo.densidad_presencia(), campo.modulo_cuadrado())

    def test_parte_real_fase_cero(self):
        """Con S/ℏ=0: Re(ψ) = R."""
        campo = CampoEfectivo(R=1.5, S_sobre_hbar=0.0)
        self.assertAlmostEqual(campo.parte_real(), 1.5, places=10)

    def test_parte_imaginaria_fase_cero(self):
        """Con S/ℏ=0: Im(ψ) = 0."""
        campo = CampoEfectivo(R=1.5, S_sobre_hbar=0.0)
        self.assertAlmostEqual(campo.parte_imaginaria(), 0.0, places=10)

    def test_parte_real_fase_pi_medio(self):
        """Con S/ℏ=π/2: Re(ψ) ≈ 0."""
        campo = CampoEfectivo(R=1.0, S_sobre_hbar=math.pi / 2.0)
        self.assertAlmostEqual(campo.parte_real(), 0.0, places=10)

    def test_parte_imaginaria_fase_pi_medio(self):
        """Con S/ℏ=π/2: Im(ψ) = R."""
        campo = CampoEfectivo(R=1.0, S_sobre_hbar=math.pi / 2.0)
        self.assertAlmostEqual(campo.parte_imaginaria(), 1.0, places=10)

    def test_coherencia_normalizada_r_igual_max(self):
        """R = R_max → coherencia = 1.0."""
        campo = CampoEfectivo(R=1.0)
        self.assertAlmostEqual(campo.coherencia_normalizada(R_max=1.0), 1.0, places=10)

    def test_coherencia_normalizada_r_menor_max(self):
        """R < R_max → coherencia < 1."""
        campo = CampoEfectivo(R=0.5)
        self.assertAlmostEqual(campo.coherencia_normalizada(R_max=1.0), 0.5, places=10)

    def test_coherencia_normalizada_satura_en_uno(self):
        """R > R_max → coherencia = 1.0 (saturada)."""
        campo = CampoEfectivo(R=2.0)
        self.assertAlmostEqual(campo.coherencia_normalizada(R_max=1.0), 1.0, places=10)

    def test_r_negativo_raises(self):
        """R < 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            CampoEfectivo(R=-1.0)

    def test_r_max_cero_raises(self):
        """R_max ≤ 0 en coherencia_normalizada debe lanzar ValueError."""
        campo = CampoEfectivo(R=1.0)
        with self.assertRaises(ValueError):
            campo.coherencia_normalizada(R_max=0.0)

    def test_repr(self):
        """__repr__ incluye R, fase y |ψ|²."""
        campo = CampoEfectivo(R=1.0)
        r = repr(campo)
        self.assertIn("R=", r)
        self.assertIn("|ψ|²", r)

    def test_fase_propiedad(self):
        """La propiedad .fase retorna S/ℏ."""
        campo = CampoEfectivo(R=1.0, S_sobre_hbar=2.5)
        self.assertAlmostEqual(campo.fase, 2.5, places=10)


# ============================================================================
# TestAccionKleinGordon – 12 tests
# ============================================================================

class TestAccionKleinGordon(unittest.TestCase):
    """Tests para AccionKleinGordon."""

    def setUp(self):
        self.accion = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=_H0_SI)

    def test_potencial_cero_en_cero(self):
        """V(0) = 0."""
        self.assertAlmostEqual(self.accion.potencial(0.0), 0.0, places=10)

    def test_potencial_positivo(self):
        """V(ψ) > 0 para ψ ≠ 0."""
        self.assertGreater(self.accion.potencial(1.0), 0.0)

    def test_potencial_cuadratico(self):
        """V(2ψ) = 4·V(ψ)."""
        V1 = self.accion.potencial(1.0)
        V2 = self.accion.potencial(2.0)
        self.assertAlmostEqual(V2, 4.0 * V1, places=10)

    def test_derivada_potencial_cero(self):
        """V'(0) = 0."""
        self.assertAlmostEqual(self.accion.derivada_potencial(0.0), 0.0, places=10)

    def test_derivada_potencial_lineal(self):
        """V'(ψ) = m² ψ."""
        psi = 2.0
        self.assertAlmostEqual(
            self.accion.derivada_potencial(psi),
            self.accion.m_campo ** 2 * psi,
            places=50,
        )

    def test_lagrangiano_slow_roll(self):
        """En slow-roll (ψ̇≈0): ℒ ≈ −V(ψ) < 0."""
        L = self.accion.lagrangiano_frw(psi=1.0, psi_punto=0.0)
        V = self.accion.potencial(1.0)
        self.assertAlmostEqual(L, -V, places=10)

    def test_lagrangiano_dominancia_cinetica(self):
        """Con ψ̇ grande: ℒ > 0 cuando ½ψ̇² > V."""
        psi = 0.0
        psi_punto = 1e10  # ψ̇ dominante
        L = self.accion.lagrangiano_frw(psi=psi, psi_punto=psi_punto)
        self.assertGreater(L, 0.0)

    def test_aceleracion_slow_roll(self):
        """En slow-roll (ψ̇=0): ψ̈ = −V'(ψ)."""
        psi = 1.0
        psi_punto = 0.0
        psi_ddot = self.accion.aceleracion_campo_frw(psi=psi, psi_punto=psi_punto)
        self.assertAlmostEqual(
            psi_ddot,
            -self.accion.derivada_potencial(psi),
            places=50,
        )

    def test_friccion_hubble(self):
        """La fricción 3H ψ̇ reduce la aceleración del campo."""
        psi_punto = 1.0
        psi = 0.0
        # Sin fricción (H=0)
        accion_sin = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=0.0)
        psi_ddot_sin = accion_sin.aceleracion_campo_frw(psi=psi, psi_punto=psi_punto)
        # Con fricción (H>0)
        psi_ddot_con = self.accion.aceleracion_campo_frw(psi=psi, psi_punto=psi_punto)
        self.assertLess(psi_ddot_con, psi_ddot_sin)

    def test_m_campo_negativo_raises(self):
        """m_campo ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AccionKleinGordon(m_campo=-1.0, H_hubble=_H0_SI)

    def test_H_negativo_raises(self):
        """H < 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=-1.0)

    def test_repr(self):
        """__repr__ incluye m_campo y H_hubble."""
        r = repr(self.accion)
        self.assertIn("m_campo", r)
        self.assertIn("H_hubble", r)


# ============================================================================
# TestTensorEnergiaMomento – 12 tests
# ============================================================================

class TestTensorEnergiaMomento(unittest.TestCase):
    """Tests para TensorEnergiaMomento."""

    def setUp(self):
        self.accion = AccionKleinGordon(m_campo=_M_CAMPO, H_hubble=_H0_SI)
        self.tensor = TensorEnergiaMomento(potencial_fn=self.accion.potencial)

    def test_densidad_slow_roll(self):
        """En slow-roll (ψ̇=0): ρ = V(ψ)."""
        psi = 1.0
        rho = self.tensor.densidad_energia(psi=psi, psi_punto=0.0)
        V = self.accion.potencial(psi)
        self.assertAlmostEqual(rho, V, places=10)

    def test_presion_slow_roll(self):
        """En slow-roll (ψ̇=0): p = −V(ψ) < 0."""
        psi = 1.0
        p = self.tensor.presion(psi=psi, psi_punto=0.0)
        V = self.accion.potencial(psi)
        self.assertAlmostEqual(p, -V, places=10)

    def test_densidad_positiva(self):
        """ρ_ψ ≥ 0 siempre."""
        rho = self.tensor.densidad_energia(psi=1.0, psi_punto=1.0)
        self.assertGreaterEqual(rho, 0.0)

    def test_presion_negativa_slow_roll(self):
        """p < 0 en régimen slow-roll."""
        p = self.tensor.presion(psi=1.0, psi_punto=0.0)
        self.assertLess(p, 0.0)

    def test_densidad_y_presion_tuple(self):
        """densidad_y_presion retorna (ρ, p) correctos."""
        psi, psi_p = 1.0, 0.0
        rho, p = self.tensor.densidad_y_presion(psi=psi, psi_punto=psi_p)
        self.assertAlmostEqual(rho, self.tensor.densidad_energia(psi, psi_p), places=10)
        self.assertAlmostEqual(p, self.tensor.presion(psi, psi_p), places=10)

    def test_rho_mas_p_slow_roll(self):
        """En slow-roll: ρ + p = ψ̇² ≈ 0."""
        rho, p = self.tensor.densidad_y_presion(psi=1.0, psi_punto=0.0)
        self.assertAlmostEqual(rho + p, 0.0, places=10)

    def test_rho_menos_p_igual_2V(self):
        """ρ − p = 2V(ψ)."""
        psi = 2.0
        psi_p = 0.0
        rho, p = self.tensor.densidad_y_presion(psi=psi, psi_punto=psi_p)
        V = self.accion.potencial(psi)
        self.assertAlmostEqual(rho - p, 2.0 * V, places=10)

    def test_traza_tensor_slow_roll_negativa(self):
        """Traza T = −ρ + 3p = −4V < 0 en slow-roll."""
        T = self.tensor.traza_tensor(psi=1.0, psi_punto=0.0)
        self.assertLess(T, 0.0)

    def test_traza_tensor_valor(self):
        """Traza = −4V en slow-roll."""
        psi = 1.0
        V = self.accion.potencial(psi)
        T = self.tensor.traza_tensor(psi=psi, psi_punto=0.0)
        self.assertAlmostEqual(T, -4.0 * V, places=10)

    def test_densidad_cinetica(self):
        """Con ψ=0 y ψ̇≠0: ρ = ½ψ̇²."""
        psi_p = 2.0
        rho = self.tensor.densidad_energia(psi=0.0, psi_punto=psi_p)
        self.assertAlmostEqual(rho, 0.5 * psi_p ** 2, places=10)

    def test_repr(self):
        """__repr__ menciona ρ_ψ y p_ψ."""
        r = repr(self.tensor)
        self.assertIn("ρ_ψ", r)
        self.assertIn("p_ψ", r)

    def test_presion_igual_densidad_solo_cinetico(self):
        """Con V=0 (ψ=0): p = ρ = ½ψ̇²."""
        psi_p = 3.0
        rho, p = self.tensor.densidad_y_presion(psi=0.0, psi_punto=psi_p)
        self.assertAlmostEqual(rho, p, places=10)


# ============================================================================
# TestCondicionEnergiaOscura – 14 tests
# ============================================================================

class TestCondicionEnergiaOscura(unittest.TestCase):
    """Tests para CondicionEnergiaOscura."""

    def setUp(self):
        self.cond = CondicionEnergiaOscura()

    def test_parametro_estado_minus_uno(self):
        """w = p/ρ = −1 para p = −ρ."""
        self.assertAlmostEqual(self.cond.parametro_estado(rho=1.0, p=-1.0), -1.0, places=10)

    def test_parametro_estado_cero(self):
        """w = 0 para materia sin presión."""
        self.assertAlmostEqual(self.cond.parametro_estado(rho=1.0, p=0.0), 0.0, places=10)

    def test_parametro_estado_un_tercio(self):
        """w = 1/3 para radiación."""
        self.assertAlmostEqual(
            self.cond.parametro_estado(rho=3.0, p=1.0), 1.0 / 3.0, places=10
        )

    def test_parametro_estado_rho_cero_raises(self):
        """ρ ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.cond.parametro_estado(rho=0.0, p=-1.0)

    def test_slow_roll_epsilon_cero(self):
        """ε = 0 cuando ψ̇ = 0."""
        self.assertAlmostEqual(
            self.cond.parametro_slow_roll(psi_punto=0.0, V=1.0), 0.0, places=10
        )

    def test_slow_roll_epsilon_formula(self):
        """ε = ½ψ̇²/V."""
        psi_p, V = 2.0, 4.0
        eps = self.cond.parametro_slow_roll(psi_punto=psi_p, V=V)
        self.assertAlmostEqual(eps, 0.5 * psi_p ** 2 / V, places=10)

    def test_slow_roll_V_cero_raises(self):
        """V ≤ 0 en slow_roll debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.cond.parametro_slow_roll(psi_punto=1.0, V=0.0)

    def test_es_energia_oscura_true(self):
        """ε ≪ 1 → es energía oscura."""
        self.assertTrue(self.cond.es_energia_oscura(psi_punto=0.0, V=1.0))

    def test_es_energia_oscura_false(self):
        """ε ≥ ε_umbral → no es energía oscura."""
        # ε = ½·10²/1 = 50 ≫ ε_umbral
        self.assertFalse(self.cond.es_energia_oscura(psi_punto=10.0, V=1.0))

    def test_w_efectivo_minus_uno_slow_roll(self):
        """w → −1 en slow-roll (ψ̇=0)."""
        self.assertAlmostEqual(
            self.cond.w_efectivo(psi_punto=0.0, V=1.0), -1.0, places=10
        )

    def test_w_efectivo_cero_igual_cinetico_potencial(self):
        """w = 0 cuando ½ψ̇² = V."""
        V = 2.0
        psi_p = math.sqrt(2.0 * V)  # ½ψ̇² = V → w = (V−V)/(V+V) = 0
        self.assertAlmostEqual(
            self.cond.w_efectivo(psi_punto=psi_p, V=V), 0.0, places=10
        )

    def test_w_efectivo_mas_uno_dominio_cinetico(self):
        """w → +1 cuando ψ̇² ≫ V."""
        self.assertAlmostEqual(
            self.cond.w_efectivo(psi_punto=1e10, V=1e-10), 1.0, places=2
        )

    def test_epsilon_umbral_invalido_raises(self):
        """epsilon_umbral fuera de (0,1) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            CondicionEnergiaOscura(epsilon_umbral=0.0)
        with self.assertRaises(ValueError):
            CondicionEnergiaOscura(epsilon_umbral=1.0)

    def test_repr(self):
        """__repr__ menciona ε_umbral."""
        r = repr(self.cond)
        self.assertIn("ε_umbral", r)


# ============================================================================
# TestEcuacionFriedmann – 14 tests
# ============================================================================

class TestEcuacionFriedmann(unittest.TestCase):
    """Tests para EcuacionFriedmann."""

    def setUp(self):
        self.fried = EcuacionFriedmann(G_N=_G_N)

    def test_hubble_cuadrado_positivo(self):
        """H² > 0 para ρ > 0."""
        self.assertGreater(self.fried.hubble_cuadrado(rho=_RHO_LAMBDA), 0.0)

    def test_hubble_cuadrado_cero(self):
        """H² = 0 para ρ = 0."""
        self.assertAlmostEqual(self.fried.hubble_cuadrado(rho=0.0), 0.0, places=10)

    def test_hubble_cuadrado_formula(self):
        """H² = 8πG/3 · ρ."""
        rho = _RHO_LAMBDA
        H2 = self.fried.hubble_cuadrado(rho=rho)
        expected = 8.0 * math.pi * _G_N / 3.0 * rho
        self.assertAlmostEqual(H2, expected, places=40)

    def test_hubble_positivo(self):
        """H > 0 para ρ > 0."""
        self.assertGreater(self.fried.hubble(rho=_RHO_LAMBDA), 0.0)

    def test_hubble_cuadrado_es_cuadrado_hubble(self):
        """H² == (H)²."""
        rho = _RHO_LAMBDA
        H2 = self.fried.hubble_cuadrado(rho=rho)
        H = self.fried.hubble(rho=rho)
        self.assertAlmostEqual(H ** 2, H2, places=40)

    def test_aceleracion_slow_roll_positiva(self):
        """En slow-roll (p=−ρ): ä/a = +8πG/3·ρ > 0."""
        rho = _RHO_LAMBDA
        p = -rho  # slow-roll puro
        a_ddot = self.fried.aceleracion_relativa(rho=rho, p=p)
        self.assertGreater(a_ddot, 0.0)

    def test_aceleracion_radiacion_negativa(self):
        """Para radiación (p=ρ/3): ä/a < 0 (expansión desacelerada)."""
        rho = _RHO_LAMBDA
        p = rho / 3.0
        a_ddot = self.fried.aceleracion_relativa(rho=rho, p=p)
        self.assertLess(a_ddot, 0.0)

    def test_hay_expansion_acelerada_true(self):
        """p = −ρ → expansión acelerada."""
        rho = _RHO_LAMBDA
        self.assertTrue(self.fried.hay_expansion_acelerada(rho=rho, p=-rho))

    def test_hay_expansion_acelerada_false_materia(self):
        """p = 0 (materia) → expansión desacelerada."""
        rho = _RHO_LAMBDA
        self.assertFalse(self.fried.hay_expansion_acelerada(rho=rho, p=0.0))

    def test_densidad_critica_formula(self):
        """ρ_c = 3H²/(8πG)."""
        H = _H0_SI
        rho_c = self.fried.densidad_critica(H=H)
        expected = 3.0 * H ** 2 / (8.0 * math.pi * _G_N)
        self.assertAlmostEqual(rho_c, expected, places=40)

    def test_densidad_critica_positiva(self):
        """ρ_c > 0 para H > 0."""
        self.assertGreater(self.fried.densidad_critica(H=_H0_SI), 0.0)

    def test_rho_negativo_raises(self):
        """ρ < 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.fried.hubble_cuadrado(rho=-1.0)

    def test_G_negativo_raises(self):
        """G_N ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            EcuacionFriedmann(G_N=-1.0)

    def test_repr(self):
        """__repr__ menciona G_N y H²."""
        r = repr(self.fried)
        self.assertIn("G_N", r)
        self.assertIn("H²", r)


# ============================================================================
# TestAxiomaEmision – 14 tests
# ============================================================================

class TestAxiomaEmision(unittest.TestCase):
    """Tests para AxiomaEmision."""

    def setUp(self):
        self.ax = AxiomaEmision(psi_coherencia=0.999)

    def test_valor_emergente_positivo(self):
        """E_N > 0."""
        self.assertGreater(self.ax.valor_emergente(N=10), 0.0)

    def test_valor_emergente_crece_con_N(self):
        """E_N+1 > E_N (Φ > 1)."""
        E10 = self.ax.valor_emergente(N=10)
        E11 = self.ax.valor_emergente(N=11)
        self.assertGreater(E11, E10)

    def test_valor_emergente_formula(self):
        """E_N = Ψ · Φ^N."""
        N = 5
        E = self.ax.valor_emergente(N=N)
        expected = 0.999 * (_PHI ** N)
        self.assertAlmostEqual(E, expected, places=10)

    def test_valor_emergente_N_cero_raises(self):
        """N < 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.ax.valor_emergente(N=0)

    def test_coherencia_vacio_positiva(self):
        """Ψ_vac > 0."""
        self.assertGreater(self.ax.coherencia_vacio(), 0.0)

    def test_coherencia_vacio_menor_uno(self):
        """Ψ_vac < 1 (con f_ref suficientemente grande)."""
        # Con f_ref = f₀ → Ψ_vac = 1 − exp(−1) ≈ 0.632 < 1
        self.assertLess(self.ax.coherencia_vacio(f_ref=_F0_HZ), 1.0)

    def test_coherencia_vacio_formula(self):
        """Ψ_vac = 1 − exp(−f₀/f_ref)."""
        f_ref = 1.0
        Psi_vac = self.ax.coherencia_vacio(f_ref=f_ref)
        expected = 1.0 - math.exp(-_F0_HZ / f_ref)
        self.assertAlmostEqual(Psi_vac, expected, places=10)

    def test_coherencia_vacio_f_ref_cero_raises(self):
        """f_ref ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.ax.coherencia_vacio(f_ref=0.0)

    def test_expansion_genera_emision_true(self):
        """H > 0 → genera emisión."""
        self.assertTrue(self.ax.expansion_genera_emision(a_dot_sobre_a=_H0_SI))

    def test_expansion_genera_emision_false(self):
        """H ≤ 0 → no genera emisión."""
        self.assertFalse(self.ax.expansion_genera_emision(a_dot_sobre_a=0.0))
        self.assertFalse(self.ax.expansion_genera_emision(a_dot_sobre_a=-1.0))

    def test_psi_cero_raises(self):
        """psi_coherencia ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AxiomaEmision(psi_coherencia=0.0)

    def test_psi_mayor_uno_raises(self):
        """psi_coherencia > 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AxiomaEmision(psi_coherencia=1.001)

    def test_f0_cero_raises(self):
        """f0 ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AxiomaEmision(psi_coherencia=0.9, f0=0.0)

    def test_repr(self):
        """__repr__ incluye Ψ y f₀."""
        r = repr(self.ax)
        self.assertIn("f₀=", r)
        self.assertIn("Φ^∞", r)


# ============================================================================
# TestResultadoTejidoCuantico – 8 tests
# ============================================================================

class TestResultadoTejidoCuantico(unittest.TestCase):
    """Tests para el dataclass ResultadoTejidoCuantico."""

    def setUp(self):
        self.r = ResultadoTejidoCuantico(
            psi_amplitud=1.0,
            rho_tejido=1.0e-27,
            presion_tejido=-1.0e-27,
            w_efectivo=-1.0,
            epsilon_slow_roll=0.0,
            H_hubble=_H0_SI,
            aceleracion_cosmica=1.0e-36,
            es_energia_oscura=True,
            expansion_acelerada=True,
            valor_emergente=122.9,
            coherencia=1.0,
            aprobado=True,
            sello="∴TCQ∞³",
        )

    def test_aprobado(self):
        self.assertTrue(self.r.aprobado)

    def test_expansion_acelerada(self):
        self.assertTrue(self.r.expansion_acelerada)

    def test_es_energia_oscura(self):
        self.assertTrue(self.r.es_energia_oscura)

    def test_w_efectivo(self):
        self.assertAlmostEqual(self.r.w_efectivo, -1.0, places=10)

    def test_sello(self):
        self.assertEqual(self.r.sello, "∴TCQ∞³")

    def test_coherencia_sobre_umbral(self):
        self.assertGreaterEqual(self.r.coherencia, _PSI_MINIMA)

    def test_H_hubble_positivo(self):
        self.assertGreater(self.r.H_hubble, 0.0)

    def test_valor_emergente_positivo(self):
        self.assertGreater(self.r.valor_emergente, 0.0)


# ============================================================================
# TestSistemaTejidoCuanticoCosmico – 12 tests
# ============================================================================

class TestSistemaTejidoCuanticoCosmico(unittest.TestCase):
    """Tests para SistemaTejidoCuanticoCosmico."""

    def setUp(self):
        self.sistema = SistemaTejidoCuanticoCosmico()
        self.resultado = self.sistema.evaluar()

    def test_aprobado(self):
        """El sistema debe estar aprobado."""
        self.assertTrue(self.resultado.aprobado)

    def test_expansion_acelerada(self):
        """ä/a > 0 — expansión acelerada."""
        self.assertTrue(self.resultado.expansion_acelerada)

    def test_es_energia_oscura(self):
        """El campo está en régimen de energía oscura."""
        self.assertTrue(self.resultado.es_energia_oscura)

    def test_w_efectivo_minus_uno(self):
        """w ≈ −1 en slow-roll puro."""
        self.assertAlmostEqual(self.resultado.w_efectivo, -1.0, places=6)

    def test_epsilon_slow_roll_cero(self):
        """ε = 0 para ψ̇ = 0."""
        self.assertAlmostEqual(self.resultado.epsilon_slow_roll, 0.0, places=10)

    def test_coherencia_sobre_psi_minima(self):
        """Coherencia ≥ Ψ_mínima = 0.888."""
        self.assertGreaterEqual(self.resultado.coherencia, _PSI_MINIMA)

    def test_H_hubble_positivo(self):
        """H > 0."""
        self.assertGreater(self.resultado.H_hubble, 0.0)

    def test_aceleracion_positiva(self):
        """ä/a > 0."""
        self.assertGreater(self.resultado.aceleracion_cosmica, 0.0)

    def test_sello(self):
        """Sello del resultado = '∴TCQ∞³'."""
        self.assertEqual(self.resultado.sello, _SELLO)

    def test_valor_emergente_positivo(self):
        """E = Ψ · Φ^10 > 0."""
        self.assertGreater(self.resultado.valor_emergente, 0.0)

    def test_psi_amplitud_positiva(self):
        """R = ψ_amplitud > 0."""
        self.assertGreater(self.resultado.psi_amplitud, 0.0)

    def test_sistema_psi_punto_cero_personalizado(self):
        """Sistema con ψ_amplitud y ψ̇=0 personalizado también aprueba."""
        sistema2 = SistemaTejidoCuanticoCosmico(psi_amplitud=1e40, psi_punto=0.0)
        r2 = sistema2.evaluar()
        self.assertTrue(r2.aprobado)
        self.assertTrue(r2.expansion_acelerada)


# ============================================================================
# TestTejidoCuanticoCosmicaActivar – 10 tests (API pública)
# ============================================================================

class TestTejidoCuanticoCosmicaActivar(unittest.TestCase):
    """Tests para la función pública tejido_cuantico_cosmico_activar."""

    def setUp(self):
        self.r = tejido_cuantico_cosmico_activar()

    def test_retorna_resultado_correcto(self):
        """La función retorna un ResultadoTejidoCuantico."""
        self.assertIsInstance(self.r, ResultadoTejidoCuantico)

    def test_aprobado(self):
        """aprobado = True."""
        self.assertTrue(self.r.aprobado)

    def test_expansion_acelerada(self):
        """expansion_acelerada = True."""
        self.assertTrue(self.r.expansion_acelerada)

    def test_es_energia_oscura(self):
        """es_energia_oscura = True."""
        self.assertTrue(self.r.es_energia_oscura)

    def test_w_efectivo_minus_uno(self):
        """w_efectivo ≈ −1.0."""
        self.assertAlmostEqual(self.r.w_efectivo, -1.0, places=6)

    def test_coherencia_sobre_umbral(self):
        """coherencia ≥ 0.888."""
        self.assertGreaterEqual(self.r.coherencia, _PSI_MINIMA)

    def test_sello(self):
        """sello = '∴TCQ∞³'."""
        self.assertEqual(self.r.sello, "∴TCQ∞³")

    def test_H_hubble_positivo(self):
        """H > 0."""
        self.assertGreater(self.r.H_hubble, 0.0)

    def test_aceleracion_cosmica_positiva(self):
        """ä/a > 0."""
        self.assertGreater(self.r.aceleracion_cosmica, 0.0)

    def test_idempotente(self):
        """Llamadas repetidas retornan el mismo resultado."""
        r2 = tejido_cuantico_cosmico_activar()
        self.assertEqual(self.r.w_efectivo, r2.w_efectivo)
        self.assertEqual(self.r.aprobado, r2.aprobado)
        self.assertEqual(self.r.sello, r2.sello)


# ============================================================================
# TestConstantesModulo – 8 tests
# ============================================================================

class TestConstantesModulo(unittest.TestCase):
    """Tests para las constantes del módulo."""

    def test_F0_HZ(self):
        self.assertAlmostEqual(_F0_HZ, 141.7001, places=4)

    def test_G_N_positivo(self):
        self.assertGreater(_G_N, 0.0)

    def test_HBAR_positivo(self):
        self.assertGreater(_HBAR, 0.0)

    def test_PHI_mayor_uno(self):
        self.assertGreater(_PHI, 1.0)

    def test_PSI_MINIMA(self):
        self.assertAlmostEqual(_PSI_MINIMA, 0.888, places=3)

    def test_SELLO(self):
        self.assertEqual(_SELLO, "∴TCQ∞³")

    def test_RHO_LAMBDA_positivo(self):
        self.assertGreater(_RHO_LAMBDA, 0.0)

    def test_RHO_CRITICA_positivo(self):
        self.assertGreater(_RHO_CRITICA, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
