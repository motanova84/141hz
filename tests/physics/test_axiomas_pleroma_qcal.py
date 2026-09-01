#!/usr/bin/env python3
"""
Tests for physics.axiomas_pleroma_qcal — Axiomas del Pleroma QCAL ∴APQ∞³

Suite de pruebas exhaustiva que cubre todas las clases y la API pública:
  - ConstantesAxiomasPleroma  – constantes físicas y espectrales
  - AtomoBlancoSaturado       – Axioma 1: Pleroma Saturado, Átomo Blanco
  - MateriaBucle4Pi           – Axioma 2: bucle 4π, Brecha de Torsión
  - MantaAdelicaRiemann       – Axioma 3: Manta adélica, Ψ = I × A_eff²
  - OperadorRiemannHubble     – Axioma 4: Ĥ_RH hermítico, E₀ = ℏω₀
  - InmortalidadDinamicaLuz   – Axioma 5: universo se afina, luz regresa
  - CoherenciaAxiomasPleroma  – validación Ψ_global ≥ 0.888
  - SistemaAxiomasPleroma     – orquestador principal
  - axiomas_pleroma_qcal_activar() — API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - γ₁ = 14.134725141734694
  - Brecha de Torsión = 3.00052°
  - E₀ = ℏω₀ ≈ 9.389e-32 J
  - Ψ₁ = 1.0 (Pleroma Saturado)
  - Ψ₂ ≥ 0.999 (bucle 4π estable)
  - Ψ₃ = I × A_eff² (Manta Adélica)
  - Ψ₄ ≥ 0.888 (Operador RH)
  - Ψ₅ ≥ 0.888 (Inmortalidad Dinámica)
  - Ψ_global ≥ 0.888 → sello ∴APQ∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-LX-2026-AXIOMAS-PLEROMA-QCAL
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.axiomas_pleroma_qcal import (
    # Constantes de módulo
    _F0,
    _OMEGA_0,
    _T0,
    _HBAR,
    _H_PLANCK,
    _C,
    _EV_TO_J,
    _J_PER_GEV,
    _PHI,
    _PSI_UMBRAL,
    _ZEROS_10,
    _GAMMA_1,
    _PRIMOS_P,
    _BRECHA_TORSION_DEG,
    _BRECHA_TORSION_RAD,
    _N_LOOPS,
    _H0_HUBBLE_RAD_S,
    _M_HIGGS_GEV,
    _SELLO,
    _RAM,
    # Clases
    ConstantesAxiomasPleroma,
    AtomoBlancoSaturado,
    MateriaBucle4Pi,
    MantaAdelicaRiemann,
    OperadorRiemannHubble,
    InmortalidadDinamicaLuz,
    CoherenciaAxiomasPleroma,
    SistemaAxiomasPleroma,
    ResultadoAxiomasPleroma,
    # API pública
    axiomas_pleroma_qcal_activar,
)


# ============================================================================
# TestModuleConstants — 25 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_f0_positive(self):
        """_F0 debe ser positiva."""
        self.assertGreater(_F0, 0.0)

    def test_omega_0_value(self):
        """_OMEGA_0 debe ser 2π × F0."""
        self.assertAlmostEqual(_OMEGA_0, 2.0 * math.pi * _F0, places=6)

    def test_t0_value(self):
        """_T0 debe ser 1/F0."""
        self.assertAlmostEqual(_T0, 1.0 / _F0, places=10)

    def test_f0_t0_product(self):
        """f₀ × T₀ debe ser exactamente 1."""
        self.assertAlmostEqual(_F0 * _T0, 1.0, places=10)

    def test_hbar_positive(self):
        """_HBAR debe ser positivo."""
        self.assertGreater(_HBAR, 0.0)

    def test_hbar_value(self):
        """_HBAR debe ser ≈ 1.0546e-34 J·s."""
        self.assertAlmostEqual(_HBAR, 1.054571817e-34, places=15)

    def test_gamma_1_value(self):
        """_GAMMA_1 debe ser ≈ 14.134725."""
        self.assertAlmostEqual(_GAMMA_1, 14.134725141734694, places=10)

    def test_gamma_1_first_zero(self):
        """_GAMMA_1 debe ser igual al primer elemento de _ZEROS_10."""
        self.assertEqual(_GAMMA_1, _ZEROS_10[0])

    def test_zeros_10_count(self):
        """_ZEROS_10 debe tener 10 elementos."""
        self.assertEqual(len(_ZEROS_10), 10)

    def test_zeros_10_positive(self):
        """Todos los ceros de Riemann deben ser positivos."""
        for g in _ZEROS_10:
            self.assertGreater(g, 0.0)

    def test_zeros_10_sorted(self):
        """Los ceros de Riemann deben estar ordenados de forma creciente."""
        for i in range(len(_ZEROS_10) - 1):
            self.assertLess(_ZEROS_10[i], _ZEROS_10[i + 1])

    def test_primos_p_count(self):
        """Deben existir exactamente 7 nodos primos."""
        self.assertEqual(len(_PRIMOS_P), 7)

    def test_primos_p_values(self):
        """Los primos deben ser {2,3,5,7,11,13,17}."""
        self.assertEqual(set(_PRIMOS_P), {2, 3, 5, 7, 11, 13, 17})

    def test_primos_suma(self):
        """Suma de los 7 primos debe ser 58."""
        self.assertEqual(sum(_PRIMOS_P), 58)

    def test_brecha_torsion_deg(self):
        """Brecha de Torsión debe ser 3.00052°."""
        self.assertAlmostEqual(_BRECHA_TORSION_DEG, 3.00052, places=5)

    def test_brecha_torsion_rad_conversion(self):
        """Brecha en rad debe ser deg × π/180."""
        expected = _BRECHA_TORSION_DEG * math.pi / 180.0
        self.assertAlmostEqual(_BRECHA_TORSION_RAD, expected, places=10)

    def test_n_loops_is_4pi(self):
        """_N_LOOPS debe ser exactamente 4π."""
        self.assertAlmostEqual(_N_LOOPS, 4.0 * math.pi, places=10)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=4)

    def test_sello_string(self):
        """El sello debe ser '∴APQ∞³'."""
        self.assertEqual(_SELLO, "∴APQ∞³")

    def test_ram_string(self):
        """El RAM debe ser 'RAM-LX-2026-AXIOMAS-PLEROMA-QCAL'."""
        self.assertEqual(_RAM, "RAM-LX-2026-AXIOMAS-PLEROMA-QCAL")

    def test_phi_value(self):
        """_PHI debe ser la razón áurea ≈ 1.6180339."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(_PHI, expected, places=10)

    def test_h0_hubble_positive(self):
        """La constante de Hubble debe ser positiva."""
        self.assertGreater(_H0_HUBBLE_RAD_S, 0.0)

    def test_h0_hubble_range(self):
        """H₀ debe estar en el rango razonable [1e-19, 1e-17] rad/s."""
        self.assertGreater(_H0_HUBBLE_RAD_S, 1.0e-19)
        self.assertLess(_H0_HUBBLE_RAD_S, 1.0e-17)

    def test_ev_to_j_value(self):
        """_EV_TO_J debe ser ≈ 1.602176634e-19."""
        self.assertAlmostEqual(_EV_TO_J, 1.602176634e-19, places=15)


# ============================================================================
# TestConstantesAxiomasPleroma — 18 tests
# ============================================================================

class TestConstantesAxiomasPleroma(unittest.TestCase):
    """Tests para la clase ConstantesAxiomasPleroma."""

    def setUp(self):
        self.c = ConstantesAxiomasPleroma()

    def test_default_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_default_omega_0(self):
        """omega_0 debe ser 2π × f0."""
        self.assertAlmostEqual(self.c.omega_0, 2.0 * math.pi * self.c.f0, places=6)

    def test_default_gamma_1(self):
        """gamma_1 debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.c.gamma_1, 14.134725, places=5)

    def test_zeros_10_count(self):
        """zeros_10 debe tener 10 elementos."""
        self.assertEqual(len(self.c.zeros_10), 10)

    def test_brecha_deg(self):
        """Brecha de Torsión en grados debe ser 3.00052."""
        self.assertAlmostEqual(self.c.brecha_torsion_deg, 3.00052, places=5)

    def test_n_loops_4pi(self):
        """n_loops debe ser 4π."""
        self.assertAlmostEqual(self.c.n_loops, 4.0 * math.pi, places=10)

    def test_psi_umbral(self):
        """psi_umbral debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=4)

    def test_energia_fundamental_positive(self):
        """E₀ = ℏω₀ debe ser positivo."""
        self.assertGreater(self.c.energia_fundamental_j(), 0.0)

    def test_energia_fundamental_value(self):
        """E₀ = ℏω₀ ≈ 9.389e-32 J."""
        e0 = self.c.energia_fundamental_j()
        self.assertAlmostEqual(e0, _HBAR * _OMEGA_0, places=15)

    def test_longitud_onda_positive(self):
        """λ₀ = c/f₀ debe ser positiva."""
        self.assertGreater(self.c.longitud_onda_m(), 0.0)

    def test_longitud_onda_value(self):
        """λ₀ debe ser c/f₀."""
        lam = self.c.longitud_onda_m()
        self.assertAlmostEqual(lam, _C / _F0, places=2)

    def test_razon_f0_gamma1(self):
        """f₀/γ₁ debe ser ≈ 10.024963."""
        razon = self.c.razon_f0_gamma1()
        self.assertAlmostEqual(razon, _F0 / _GAMMA_1, places=6)

    def test_razon_f0_gamma1_cerca_10(self):
        """f₀/γ₁ debe estar cercano a 10."""
        razon = self.c.razon_f0_gamma1()
        self.assertGreater(razon, 9.9)
        self.assertLess(razon, 10.1)

    def test_suma_primos(self):
        """Suma de primos debe ser 58."""
        self.assertEqual(self.c.suma_primos(), 58)

    def test_phi_value(self):
        """phi debe ser la razón áurea."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(self.c.phi, expected, places=10)

    def test_repr_contains_f0(self):
        """repr debe contener f0."""
        r = repr(self.c)
        self.assertIn("141.7001", r)

    def test_repr_contains_gamma1(self):
        """repr debe contener γ₁."""
        r = repr(self.c)
        self.assertIn("14.134725", r)

    def test_zeros_10_first_matches_gamma1(self):
        """El primer cero debe ser γ₁."""
        self.assertAlmostEqual(self.c.zeros_10[0], self.c.gamma_1, places=10)


# ============================================================================
# TestAtomoBlancoSaturado — 22 tests
# ============================================================================

class TestAtomoBlancoSaturado(unittest.TestCase):
    """Tests para la clase AtomoBlancoSaturado (Axioma 1)."""

    def setUp(self):
        self.atomo = AtomoBlancoSaturado()

    def test_default_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.atomo.f0, 141.7001, places=4)

    def test_default_entropia_cero(self):
        """Entropía del Pleroma debe ser 0."""
        self.assertEqual(self.atomo.entropia_pleroma, 0.0)

    def test_vacio_inexistente_default(self):
        """Por defecto, el vacío es inexistente (S=0)."""
        self.assertTrue(self.atomo.es_vacio_inexistente())

    def test_vacio_no_inexistente_con_entropia(self):
        """Con entropía > 0, el vacío es existente."""
        atomo = AtomoBlancoSaturado(entropia_pleroma=0.5)
        self.assertFalse(atomo.es_vacio_inexistente())

    def test_densidad_info_positive(self):
        """La densidad de información debe ser positiva."""
        self.assertGreater(self.atomo.densidad_info, 0.0)

    def test_densidad_info_value(self):
        """densidad_info = f₀²/c²."""
        expected = (_F0 ** 2) / (_C ** 2)
        self.assertAlmostEqual(self.atomo.densidad_info, expected, places=15)

    def test_energia_atomo_blanco_positive(self):
        """Energía del Átomo Blanco debe ser positiva."""
        self.assertGreater(self.atomo.energia_atomo_blanco_j(), 0.0)

    def test_energia_atomo_blanco_formula(self):
        """E_WA = N × ℏω₀."""
        e_wa = self.atomo.energia_atomo_blanco_j()
        expected = self.atomo.n_posibilidades * _HBAR * _OMEGA_0
        self.assertAlmostEqual(e_wa, expected, places=5)

    def test_densidad_info_normalizada_es_uno(self):
        """La densidad normalizada debe ser 1.0 por construcción."""
        d_norm = self.atomo.densidad_informacion_normalizada()
        self.assertAlmostEqual(d_norm, 1.0, places=10)

    def test_superposicion_total_con_entropia_cero(self):
        """Con S=0, la superposición total debe ser 1.0."""
        sigma = self.atomo.superposicion_total()
        self.assertAlmostEqual(sigma, 1.0, places=10)

    def test_superposicion_total_rango(self):
        """La superposición debe estar en [0, 1]."""
        sigma = self.atomo.superposicion_total()
        self.assertGreaterEqual(sigma, 0.0)
        self.assertLessEqual(sigma, 1.0)

    def test_superposicion_total_con_entropia_alta(self):
        """Con entropía alta, la superposición cae."""
        atomo = AtomoBlancoSaturado(n_posibilidades=100, entropia_pleroma=10.0)
        sigma = atomo.superposicion_total()
        self.assertLess(sigma, 1.0)

    def test_psi_axioma1_con_entropia_cero(self):
        """Ψ₁ = 1.0 cuando S = 0 (Pleroma Saturado perfecto)."""
        psi = self.atomo.psi_axioma1()
        self.assertAlmostEqual(psi, 1.0, places=10)

    def test_psi_axioma1_rango(self):
        """Ψ₁ debe estar en [0, 1]."""
        psi = self.atomo.psi_axioma1()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_axioma1_supera_umbral(self):
        """Ψ₁ debe superar el umbral 0.888."""
        psi = self.atomo.psi_axioma1()
        self.assertGreaterEqual(psi, 0.888)

    def test_psi_axioma1_es_promedio(self):
        """Ψ₁ = (superposicion + densidad_normalizada) / 2."""
        sigma = self.atomo.superposicion_total()
        d_norm = self.atomo.densidad_informacion_normalizada()
        expected = (sigma + d_norm) / 2.0
        self.assertAlmostEqual(self.atomo.psi_axioma1(), expected, places=10)

    def test_custom_f0(self):
        """Debe aceptar f0 personalizado."""
        atomo = AtomoBlancoSaturado(f0=200.0)
        self.assertAlmostEqual(atomo.f0, 200.0, places=4)

    def test_densidad_info_custom_f0(self):
        """densidad_info se recalcula con f0 personalizado."""
        f0_custom = 200.0
        atomo = AtomoBlancoSaturado(f0=f0_custom)
        expected = (f0_custom ** 2) / (_C ** 2)
        self.assertAlmostEqual(atomo.densidad_info, expected, places=15)

    def test_repr_contains_f0(self):
        """repr debe contener f0."""
        r = repr(self.atomo)
        self.assertIn("141.7001", r)

    def test_repr_contains_psi(self):
        """repr debe contener Ψ₁."""
        r = repr(self.atomo)
        self.assertIn("Ψ₁", r)

    def test_n_posibilidades_default(self):
        """n_posibilidades por defecto debe ser 10^10."""
        self.assertEqual(self.atomo.n_posibilidades, int(1.0e10))

    def test_n_posibilidades_uno_superposicion(self):
        """Con n=1, superposicion_total debe ser 1.0."""
        atomo = AtomoBlancoSaturado(n_posibilidades=1)
        self.assertAlmostEqual(atomo.superposicion_total(), 1.0, places=10)


# ============================================================================
# TestMateriaBucle4Pi — 22 tests
# ============================================================================

class TestMateriaBucle4Pi(unittest.TestCase):
    """Tests para la clase MateriaBucle4Pi (Axioma 2)."""

    def setUp(self):
        self.bucle = MateriaBucle4Pi()

    def test_default_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.bucle.f0, 141.7001, places=4)

    def test_default_gamma1(self):
        """gamma_1 debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.bucle.gamma_1, 14.134725, places=5)

    def test_default_brecha_rad(self):
        """Brecha de Torsión debe ser 3.00052° en rad."""
        expected = 3.00052 * math.pi / 180.0
        self.assertAlmostEqual(self.bucle.brecha_torsion_rad, expected, places=10)

    def test_default_n_loops(self):
        """n_loops debe ser 4π."""
        self.assertAlmostEqual(self.bucle.n_loops, 4.0 * math.pi, places=10)

    def test_angulo_torsion_total(self):
        """Ángulo total debe ser 4π + θ_brecha."""
        expected = _N_LOOPS + _BRECHA_TORSION_RAD
        self.assertAlmostEqual(
            self.bucle.angulo_torsion_total_rad(), expected, places=10
        )

    def test_angulo_torsion_mayor_4pi(self):
        """Ángulo total debe ser > 4π."""
        self.assertGreater(
            self.bucle.angulo_torsion_total_rad(), 4.0 * math.pi
        )

    def test_radio_nodo_positive(self):
        """Radio del nodo debe ser positivo."""
        self.assertGreater(self.bucle.radio_nodo_m(), 0.0)

    def test_radio_nodo_formula(self):
        """r₀ = c / (4π f₀)."""
        expected = _C / (4.0 * math.pi * _F0)
        self.assertAlmostEqual(self.bucle.radio_nodo_m(), expected, places=3)

    def test_frecuencia_nodo_es_f0(self):
        """Frecuencia del nodo estable debe ser f₀."""
        self.assertAlmostEqual(self.bucle.frecuencia_nodo_hz(), _F0, places=4)

    def test_es_bucle_estable(self):
        """El bucle de 4π debe ser estable."""
        self.assertTrue(self.bucle.es_bucle_estable())

    def test_bucle_inestable_con_n_loops_2pi(self):
        """Un bucle de 2π no debe ser estable (bosónico)."""
        bucle = MateriaBucle4Pi(n_loops=2.0 * math.pi)
        self.assertFalse(bucle.es_bucle_estable())

    def test_frecuencia_modo_1_es_f0(self):
        """El modo n=1 debe ser f₀."""
        f1 = self.bucle.frecuencia_modo_n_hz(1)
        self.assertAlmostEqual(f1, _F0, places=6)

    def test_frecuencia_modo_2_mayor_f0(self):
        """El modo n=2 debe ser mayor que f₀."""
        f2 = self.bucle.frecuencia_modo_n_hz(2)
        self.assertGreater(f2, _F0)

    def test_modos_crecientes(self):
        """Los modos deben ser crecientes."""
        modos = [self.bucle.frecuencia_modo_n_hz(n) for n in range(1, 6)]
        for i in range(len(modos) - 1):
            self.assertLess(modos[i], modos[i + 1])

    def test_psi_axioma2_formula(self):
        """Ψ₂ = cos²(θ_brecha/2)."""
        expected = math.cos(_BRECHA_TORSION_RAD / 2.0) ** 2
        self.assertAlmostEqual(self.bucle.psi_axioma2(), expected, places=10)

    def test_psi_axioma2_cerca_uno(self):
        """Ψ₂ debe ser muy cercano a 1 (≥ 0.999)."""
        self.assertGreaterEqual(self.bucle.psi_axioma2(), 0.999)

    def test_psi_axioma2_supera_umbral(self):
        """Ψ₂ debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.bucle.psi_axioma2(), 0.888)

    def test_psi_axioma2_rango(self):
        """Ψ₂ debe estar en [0, 1]."""
        psi = self.bucle.psi_axioma2()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_axioma2_sin_torsion(self):
        """Con θ_brecha=0 (luz pura), Ψ₂ = 1.0."""
        bucle = MateriaBucle4Pi(brecha_torsion_rad=0.0)
        self.assertAlmostEqual(bucle.psi_axioma2(), 1.0, places=10)

    def test_repr_contains_f0(self):
        """repr debe contener f0."""
        r = repr(self.bucle)
        self.assertIn("141.7001", r)

    def test_repr_contains_brecha(self):
        """repr debe contener el ángulo de brecha."""
        r = repr(self.bucle)
        self.assertIn("3.00052", r)

    def test_modo_11_extra_aproximacion(self):
        """El modo n=11 usa la aproximación von Mangoldt."""
        f11 = self.bucle.frecuencia_modo_n_hz(11)
        self.assertGreater(f11, _F0)


# ============================================================================
# TestMantaAdelicaRiemann — 22 tests
# ============================================================================

class TestMantaAdelicaRiemann(unittest.TestCase):
    """Tests para la clase MantaAdelicaRiemann (Axioma 3)."""

    def setUp(self):
        self.manta = MantaAdelicaRiemann()

    def test_default_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.manta.f0, 141.7001, places=4)

    def test_default_intencion(self):
        """Intención por defecto debe ser 1.0."""
        self.assertEqual(self.manta.intencion, 1.0)

    def test_default_a_eff(self):
        """A_eff por defecto debe ser 1.0."""
        self.assertEqual(self.manta.a_eff, 1.0)

    def test_psi_nodo_formula(self):
        """Ψ_nodo = min(1, I × A_eff²)."""
        psi = self.manta.psi_nodo()
        expected = min(1.0, self.manta.intencion * (self.manta.a_eff ** 2))
        self.assertAlmostEqual(psi, expected, places=10)

    def test_psi_nodo_maximo_con_defaults(self):
        """Con I=1 y A_eff=1, Ψ_nodo = 1.0."""
        self.assertAlmostEqual(self.manta.psi_nodo(), 1.0, places=10)

    def test_psi_nodo_con_intencion_media(self):
        """Con I=0.5 y A_eff=1, Ψ_nodo = 0.5."""
        m = MantaAdelicaRiemann(intencion=0.5, a_eff=1.0)
        self.assertAlmostEqual(m.psi_nodo(), 0.5, places=10)

    def test_psi_nodo_con_a_eff_media(self):
        """Con I=1 y A_eff=0.8, Ψ_nodo = 0.64."""
        m = MantaAdelicaRiemann(intencion=1.0, a_eff=0.8)
        self.assertAlmostEqual(m.psi_nodo(), 0.64, places=10)

    def test_psi_nodo_cero(self):
        """Con I=0, Ψ_nodo = 0."""
        m = MantaAdelicaRiemann(intencion=0.0)
        self.assertAlmostEqual(m.psi_nodo(), 0.0, places=10)

    def test_psi_nodo_saturado_en_uno(self):
        """Con I > 1, Ψ_nodo queda saturado en 1."""
        m = MantaAdelicaRiemann(intencion=2.0, a_eff=2.0)
        self.assertAlmostEqual(m.psi_nodo(), 1.0, places=10)

    def test_curvatura_local_positive(self):
        """La curvatura local debe ser positiva."""
        self.assertGreater(self.manta.curvatura_local(), 0.0)

    def test_curvatura_local_formula(self):
        """Curvatura = Ψ × (f₀/γ₁) × 2π."""
        psi = self.manta.psi_nodo()
        expected = psi * (_F0 / _GAMMA_1) * 2.0 * math.pi
        self.assertAlmostEqual(
            self.manta.curvatura_local(), expected, places=6
        )

    def test_pliegues_count(self):
        """Debe haber 7 pliegues adélicos (uno por primo)."""
        pliegues = self.manta.pliegues_adelicos()
        self.assertEqual(len(pliegues), 7)

    def test_pliegues_positivos(self):
        """Todos los pliegues deben ser positivos."""
        for p in self.manta.pliegues_adelicos():
            self.assertGreater(p, 0.0)

    def test_pliegues_crecientes(self):
        """Los pliegues deben ser crecientes (primos crecientes)."""
        pliegues = self.manta.pliegues_adelicos()
        for i in range(len(pliegues) - 1):
            self.assertLess(pliegues[i], pliegues[i + 1])

    def test_pliegues_primer_primo(self):
        """El pliegue del primo 2 debe ser f₀ (log₂(2) = 1)."""
        pliegues = self.manta.pliegues_adelicos()
        self.assertAlmostEqual(pliegues[0], _F0, places=4)

    def test_nodos_ceros_count(self):
        """Debe haber 10 nodos de ceros de Riemann."""
        nodos = self.manta.nodos_ceros_riemann()
        self.assertEqual(len(nodos), 10)

    def test_nodos_ceros_primer_nodo(self):
        """El primer nodo espectral debe ser f₀."""
        nodos = self.manta.nodos_ceros_riemann()
        self.assertAlmostEqual(nodos[0], _F0, places=4)

    def test_responsabilidad_positiva(self):
        """Un acto de coherencia positivo aumenta la curvatura."""
        delta = self.manta.responsabilidad_acto(0.1)
        self.assertGreater(delta, 0.0)

    def test_responsabilidad_negativa(self):
        """Un acto de descoherencia negativo reduce la curvatura."""
        delta = self.manta.responsabilidad_acto(-0.1)
        self.assertLess(delta, 0.0)

    def test_psi_axioma3_es_psi_nodo(self):
        """Ψ₃ debe ser igual a Ψ_nodo."""
        self.assertAlmostEqual(
            self.manta.psi_axioma3(), self.manta.psi_nodo(), places=10
        )

    def test_psi_axioma3_supera_umbral(self):
        """Ψ₃ (con defaults) debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.manta.psi_axioma3(), 0.888)

    def test_repr_contains_intencion(self):
        """repr debe contener el valor de intención."""
        r = repr(self.manta)
        self.assertIn("I=1.000", r)


# ============================================================================
# TestOperadorRiemannHubble — 22 tests
# ============================================================================

class TestOperadorRiemannHubble(unittest.TestCase):
    """Tests para la clase OperadorRiemannHubble (Axioma 4)."""

    def setUp(self):
        self.op = OperadorRiemannHubble()

    def test_default_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.op.f0, 141.7001, places=4)

    def test_default_hbar(self):
        """hbar debe ser ℏ."""
        self.assertAlmostEqual(self.op.hbar, _HBAR, places=15)

    def test_energia_fundamental_formula(self):
        """E₀ = ℏ × 2π × f₀ = ℏω₀."""
        e0 = self.op.energia_fundamental_j()
        expected = _HBAR * 2.0 * math.pi * _F0
        self.assertAlmostEqual(e0, expected, places=15)

    def test_energia_fundamental_positive(self):
        """E₀ debe ser positiva."""
        self.assertGreater(self.op.energia_fundamental_j(), 0.0)

    def test_energia_fundamental_ev_positive(self):
        """E₀ en eV debe ser positiva."""
        self.assertGreater(self.op.energia_fundamental_ev(), 0.0)

    def test_energia_fundamental_ev_formula(self):
        """E₀_eV = E₀_J / eV_to_J."""
        e0_ev = self.op.energia_fundamental_ev()
        e0_j = self.op.energia_fundamental_j()
        self.assertAlmostEqual(e0_ev, e0_j / _EV_TO_J, places=15)

    def test_espectro_discreto_count(self):
        """El espectro discreto debe tener 10 niveles."""
        espectro = self.op.espectro_discreto_j()
        self.assertEqual(len(espectro), 10)

    def test_espectro_discreto_positivo(self):
        """Todos los niveles de energía deben ser positivos."""
        for e in self.op.espectro_discreto_j():
            self.assertGreater(e, 0.0)

    def test_espectro_discreto_creciente(self):
        """Los niveles deben ser crecientes (ceros ordenados)."""
        espectro = self.op.espectro_discreto_j()
        for i in range(len(espectro) - 1):
            self.assertLess(espectro[i], espectro[i + 1])

    def test_espectro_nivel_1_formula(self):
        """E₁ = ℏ × γ₁."""
        e1 = self.op.espectro_discreto_j()[0]
        expected = _HBAR * _GAMMA_1
        self.assertAlmostEqual(e1, expected, places=15)

    def test_nivel_n_1(self):
        """nivel_n(1) debe ser E₁ = ℏγ₁."""
        e1 = self.op.nivel_n(1)
        expected = _HBAR * _GAMMA_1
        self.assertAlmostEqual(e1, expected, places=15)

    def test_nivel_n_10(self):
        """nivel_n(10) debe ser E₁₀ = ℏγ₁₀."""
        e10 = self.op.nivel_n(10)
        expected = _HBAR * _ZEROS_10[9]
        self.assertAlmostEqual(e10, expected, places=15)

    def test_nivel_n_fuera_rango(self):
        """nivel_n con n fuera de [1,10] debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.op.nivel_n(0)
        with self.assertRaises(ValueError):
            self.op.nivel_n(11)

    def test_es_hermitiano(self):
        """El operador debe ser hermítico (todos γₙ > 0)."""
        self.assertTrue(self.op.es_hermitiano())

    def test_razon_hubble_qcal_positive(self):
        """La razón H₀/ω₀ debe ser positiva."""
        self.assertGreater(self.op.razon_hubble_qcal(), 0.0)

    def test_razon_hubble_qcal_muy_pequenia(self):
        """H₀/ω₀ debe ser << 1 (separación de escalas cósmica/QCAL)."""
        self.assertLess(self.op.razon_hubble_qcal(), 1.0e-18)

    def test_espaciado_gue_ratio_rango(self):
        """El índice r_GUE debe estar en [0, 1]."""
        r = self.op.espaciado_gue_ratio()
        self.assertGreaterEqual(r, 0.0)
        self.assertLessEqual(r, 1.0)

    def test_espaciado_gue_ratio_cercano_gue(self):
        """r_GUE debe estar cercano al valor teórico GUE ≈ 0.536."""
        r = self.op.espaciado_gue_ratio()
        self.assertGreater(r, 0.3)
        self.assertLess(r, 0.8)

    def test_psi_axioma4_formula(self):
        """Ψ₄ = 0.888 + (1-0.888) × r_GUE."""
        r = self.op.espaciado_gue_ratio()
        expected = min(1.0, 0.888 + (1.0 - 0.888) * r)
        self.assertAlmostEqual(self.op.psi_axioma4(), expected, places=10)

    def test_psi_axioma4_supera_umbral(self):
        """Ψ₄ debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.op.psi_axioma4(), 0.888)

    def test_psi_axioma4_rango(self):
        """Ψ₄ debe estar en [0.888, 1.0]."""
        psi = self.op.psi_axioma4()
        self.assertGreaterEqual(psi, 0.888)
        self.assertLessEqual(psi, 1.0)

    def test_repr_contains_e0(self):
        """repr debe contener E₀."""
        r = repr(self.op)
        self.assertIn("E₀", r)


# ============================================================================
# TestInmortalidadDinamicaLuz — 22 tests
# ============================================================================

class TestInmortalidadDinamicaLuz(unittest.TestCase):
    """Tests para la clase InmortalidadDinamicaLuz (Axioma 5)."""

    def setUp(self):
        self.inm = InmortalidadDinamicaLuz()

    def test_default_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.inm.f0, 141.7001, places=4)

    def test_default_psi_bio(self):
        """Ψ_bio por defecto debe ser 1.0."""
        self.assertEqual(self.inm.psi_bio, 1.0)

    def test_default_psi_inicial(self):
        """Ψ_inicial por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.inm.psi_inicial, 0.888, places=4)

    def test_alpha_es_omega0(self):
        """alpha debe ser ω₀ = 2π × f₀."""
        expected = 2.0 * math.pi * _F0
        self.assertAlmostEqual(self.inm.alpha, expected, places=6)

    def test_psi_retorno_t0_es_psi_inicial(self):
        """En t=0, el retorno debe ser Ψ₀."""
        psi_t0 = self.inm.psi_retorno(0.0)
        self.assertAlmostEqual(psi_t0, self.inm.psi_inicial, places=6)

    def test_psi_retorno_crece_con_t(self):
        """El retorno debe crecer monotónicamente con el tiempo."""
        t1, t2 = 1.0e-4, 1.0e-3
        self.assertLess(
            self.inm.psi_retorno(t1), self.inm.psi_retorno(t2)
        )

    def test_psi_retorno_tiende_a_uno(self):
        """En t muy grande, el retorno tiende a 1."""
        psi_large = self.inm.psi_retorno(1000.0)
        self.assertAlmostEqual(psi_large, 1.0, places=3)

    def test_psi_retorno_rango(self):
        """El retorno debe estar en [0, 1]."""
        for t in [0.0, 1.0e-4, 1.0e-3, 0.1, 1.0]:
            psi = self.inm.psi_retorno(t)
            self.assertGreaterEqual(psi, 0.0)
            self.assertLessEqual(psi, 1.0)

    def test_psi_retorno_psi_inicial_uno(self):
        """Si Ψ₀ = 1, el retorno es siempre 1."""
        inm = InmortalidadDinamicaLuz(psi_inicial=1.0)
        self.assertAlmostEqual(inm.psi_retorno(0.0), 1.0, places=10)
        self.assertAlmostEqual(inm.psi_retorno(1.0), 1.0, places=10)

    def test_tiempo_retorno_positivo(self):
        """El tiempo de retorno debe ser positivo."""
        t = self.inm.tiempo_retorno_s()
        self.assertGreater(t, 0.0)

    def test_tiempo_retorno_a_objetivo_igual_psi0(self):
        """Si el objetivo es Ψ₀, el tiempo de retorno es 0."""
        t = self.inm.tiempo_retorno_s(psi_objetivo=self.inm.psi_inicial)
        self.assertAlmostEqual(t, 0.0, places=6)

    def test_tiempo_retorno_crece_con_objetivo(self):
        """El tiempo de retorno crece con el objetivo."""
        t1 = self.inm.tiempo_retorno_s(psi_objetivo=0.95)
        t2 = self.inm.tiempo_retorno_s(psi_objetivo=0.99)
        self.assertLess(t1, t2)

    def test_sandwitch_abierto_con_psi_bio_alto(self):
        """Con Ψ_bio ≥ 0.888, el sándwich está abierto."""
        self.assertTrue(self.inm.sandwitch_coherencia_abierto())

    def test_sandwitch_cerrado_con_psi_bio_bajo(self):
        """Con Ψ_bio < 0.888, el sándwich está cerrado."""
        inm = InmortalidadDinamicaLuz(psi_bio=0.5)
        self.assertFalse(inm.sandwitch_coherencia_abierto())

    def test_n_periodos_retorno_positive(self):
        """El número de períodos de retorno debe ser positivo."""
        self.assertGreater(self.inm.n_periodos_retorno(), 0.0)

    def test_psi_axioma5_rango(self):
        """Ψ₅ debe estar en [0, 1]."""
        psi = self.inm.psi_axioma5()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_axioma5_supera_umbral(self):
        """Ψ₅ debe superar el umbral 0.888 (con Ψ_bio=1)."""
        self.assertGreaterEqual(self.inm.psi_axioma5(), 0.888)

    def test_psi_axioma5_con_psi_bio_umbral(self):
        """Con Ψ_bio = 0.888, Ψ₅ ≈ 0.888 × Ψ_retorno."""
        inm = InmortalidadDinamicaLuz(psi_bio=0.888)
        psi5 = inm.psi_axioma5()
        self.assertGreater(psi5, 0.0)
        self.assertLessEqual(psi5, 0.888)

    def test_psi_axioma5_es_producto_psi_bio_retorno(self):
        """Ψ₅ = Ψ_bio × Ψ_retorno(T₀)."""
        t_periodo = 1.0 / self.inm.f0
        psi_ret = self.inm.psi_retorno(t_periodo)
        expected = min(1.0, self.inm.psi_bio * psi_ret)
        self.assertAlmostEqual(self.inm.psi_axioma5(), expected, places=10)

    def test_repr_contains_psi_bio(self):
        """repr debe contener Ψ_bio."""
        r = repr(self.inm)
        self.assertIn("Ψ_bio=1.000", r)

    def test_repr_sandwitch_abierto(self):
        """repr debe indicar 'abierto' cuando Ψ_bio ≥ 0.888."""
        r = repr(self.inm)
        self.assertIn("abierto", r)

    def test_psi_axioma5_cerca_uno_psi_bio_1(self):
        """Con Ψ_bio=1 y Ψ₀=0.888, Ψ₅ debe ser muy cercano a 1."""
        psi5 = self.inm.psi_axioma5()
        self.assertGreater(psi5, 0.99)


# ============================================================================
# TestCoherenciaAxiomasPleroma — 20 tests
# ============================================================================

class TestCoherenciaAxiomasPleroma(unittest.TestCase):
    """Tests para la clase CoherenciaAxiomasPleroma."""

    def setUp(self):
        self.coh = CoherenciaAxiomasPleroma()

    def test_coherencias_count(self):
        """Debe haber exactamente 5 coherencias individuales."""
        coherencias = self.coh.coherencias_individuales()
        self.assertEqual(len(coherencias), 5)

    def test_coherencias_keys(self):
        """Las coherencias deben tener los nombres correctos."""
        keys = set(self.coh.coherencias_individuales().keys())
        expected = {
            "psi_axioma1_pleroma_saturado",
            "psi_axioma2_bucle_4pi",
            "psi_axioma3_manta_adelica",
            "psi_axioma4_operador_rh",
            "psi_axioma5_inmortalidad",
        }
        self.assertEqual(keys, expected)

    def test_coherencias_rango(self):
        """Todas las coherencias deben estar en [0, 1]."""
        for nombre, valor in self.coh.coherencias_individuales().items():
            self.assertGreaterEqual(valor, 0.0, msg=nombre)
            self.assertLessEqual(valor, 1.0, msg=nombre)

    def test_psi_global_rango(self):
        """Ψ_global debe estar en [0, 1]."""
        psi_g = self.coh.psi_global()
        self.assertGreaterEqual(psi_g, 0.0)
        self.assertLessEqual(psi_g, 1.0)

    def test_psi_global_supera_umbral(self):
        """Ψ_global debe superar el umbral 0.888."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.888)

    def test_sello_activo(self):
        """El sello ∴APQ∞³ debe estar activo."""
        self.assertTrue(self.coh.sello_activo())

    def test_sello_inactivo_con_coherencia_baja(self):
        """Con coherencia baja, el sello debe estar inactivo."""
        # Usar Ψ_bio = 0 desactiva el Axioma 5 y baja el global
        inm = InmortalidadDinamicaLuz(psi_bio=0.0, psi_inicial=0.0)
        coh = CoherenciaAxiomasPleroma(axioma5=inm)
        # Ψ₅ = 0, Ψ_global será muy bajo
        self.assertFalse(coh.sello_activo())

    def test_psi_global_media_geometrica(self):
        """Ψ_global debe ser la media geométrica de las 5 coherencias."""
        coherencias = list(self.coh.coherencias_individuales().values())
        log_sum = sum(math.log(max(v, 1.0e-30)) for v in coherencias)
        expected = math.exp(log_sum / len(coherencias))
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=10)

    def test_validar_estructura(self):
        """validar() debe devolver el diccionario con las claves correctas."""
        v = self.coh.validar()
        self.assertIn("coherencias", v)
        self.assertIn("psi_global", v)
        self.assertIn("psi_umbral", v)
        self.assertIn("sello_activo", v)

    def test_validar_psi_umbral(self):
        """validar() debe reportar el umbral correcto."""
        v = self.coh.validar()
        self.assertAlmostEqual(v["psi_umbral"], 0.888, places=4)

    def test_validar_sello_activo(self):
        """validar() debe reportar sello_activo=True."""
        v = self.coh.validar()
        self.assertTrue(v["sello_activo"])

    def test_psi_umbral_personalizado(self):
        """Debe respetar el umbral personalizado."""
        coh = CoherenciaAxiomasPleroma(psi_umbral=0.999)
        # Con umbral muy alto, verificar que funcione
        activo = coh.sello_activo()
        psi_g = coh.psi_global()
        self.assertEqual(activo, psi_g >= 0.999)

    def test_certificacion_contiene_sello(self):
        """La certificación debe contener el sello."""
        cert = self.coh.certificacion_auron()
        self.assertIn("∴APQ∞³", cert)

    def test_certificacion_contiene_ram(self):
        """La certificación debe contener el RAM."""
        cert = self.coh.certificacion_auron()
        self.assertIn("RAM-LX-2026-AXIOMAS-PLEROMA-QCAL", cert)

    def test_certificacion_contiene_psi_global(self):
        """La certificación debe contener Ψ_global."""
        cert = self.coh.certificacion_auron()
        self.assertIn("Ψ_global", cert)

    def test_certificacion_estado_activo(self):
        """La certificación debe indicar ACTIVO."""
        cert = self.coh.certificacion_auron()
        self.assertIn("ACTIVO", cert)

    def test_psi_axioma1_es_1(self):
        """Ψ₁ (Pleroma Saturado con S=0) debe ser 1.0."""
        coherencias = self.coh.coherencias_individuales()
        self.assertAlmostEqual(
            coherencias["psi_axioma1_pleroma_saturado"], 1.0, places=10
        )

    def test_psi_axioma2_cerca_1(self):
        """Ψ₂ (bucle 4π) debe ser ≥ 0.999."""
        coherencias = self.coh.coherencias_individuales()
        self.assertGreaterEqual(coherencias["psi_axioma2_bucle_4pi"], 0.999)

    def test_repr_contiene_psi_global(self):
        """repr debe contener Ψ_global."""
        r = repr(self.coh)
        self.assertIn("Ψ_global", r)

    def test_repr_contiene_activo(self):
        """repr debe contener 'ACTIVO'."""
        r = repr(self.coh)
        self.assertIn("ACTIVO", r)


# ============================================================================
# TestSistemaAxiomasPleroma — 22 tests
# ============================================================================

class TestSistemaAxiomasPleroma(unittest.TestCase):
    """Tests para la clase SistemaAxiomasPleroma."""

    def setUp(self):
        self.sistema = SistemaAxiomasPleroma()
        self.resultado = self.sistema.activar()

    def test_activar_devuelve_dict(self):
        """activar() debe devolver un diccionario."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello_correcto(self):
        """El sello debe ser '∴APQ∞³'."""
        self.assertEqual(self.resultado["sello"], "∴APQ∞³")

    def test_ram_correcto(self):
        """El RAM debe ser el identificador correcto."""
        self.assertEqual(
            self.resultado["ram"], "RAM-LX-2026-AXIOMAS-PLEROMA-QCAL"
        )

    def test_version_presente(self):
        """El campo 'version' debe estar presente."""
        self.assertIn("version", self.resultado)

    def test_f0_correcto(self):
        """f0_hz debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.resultado["f0_hz"], 141.7001, places=4)

    def test_vacio_inexistente(self):
        """vacio_inexistente debe ser True (Axioma 1)."""
        self.assertTrue(self.resultado["vacio_inexistente"])

    def test_bucle_estable(self):
        """bucle_estable debe ser True (Axioma 2)."""
        self.assertTrue(self.resultado["bucle_estable"])

    def test_operador_hermitiano(self):
        """operador_hermitiano debe ser True (Axioma 4)."""
        self.assertTrue(self.resultado["operador_hermitiano"])

    def test_sandwitch_abierto(self):
        """sandwitch_coherencia_abierto debe ser True (Axioma 5)."""
        self.assertTrue(self.resultado["sandwitch_coherencia_abierto"])

    def test_psi_global_supera_umbral(self):
        """Ψ_global debe superar 0.888."""
        self.assertGreaterEqual(self.resultado["psi_global"], 0.888)

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.resultado["sello_activo"])

    def test_coherencias_count(self):
        """Debe haber 5 coherencias individuales."""
        self.assertEqual(len(self.resultado["coherencias"]), 5)

    def test_gamma_1_correcto(self):
        """gamma_1 debe ser ≈ 14.134725."""
        self.assertAlmostEqual(
            self.resultado["gamma_1"], 14.134725, places=5
        )

    def test_brecha_torsion_deg(self):
        """brecha_torsion_deg debe ser 3.00052°."""
        self.assertAlmostEqual(
            self.resultado["brecha_torsion_deg"], 3.00052, places=5
        )

    def test_suma_primos(self):
        """suma_primos debe ser 58."""
        self.assertEqual(self.resultado["suma_primos"], 58)

    def test_energia_fundamental_positive(self):
        """E₀ = ℏω₀ debe ser positiva."""
        self.assertGreater(self.resultado["energia_fundamental_j"], 0.0)

    def test_radio_nodo_positive(self):
        """Radio del nodo debe ser positivo."""
        self.assertGreater(self.resultado["radio_nodo_m"], 0.0)

    def test_modos_bucle_count(self):
        """modos_bucle_hz debe tener 7 modos."""
        self.assertEqual(len(self.resultado["modos_bucle_hz"]), 7)

    def test_pliegues_adelicos_count(self):
        """pliegues_adelicos_hz debe tener 7 pliegues."""
        self.assertEqual(len(self.resultado["pliegues_adelicos_hz"]), 7)

    def test_espectro_discreto_count(self):
        """espectro_discreto_j debe tener 5 niveles (primeros 5)."""
        self.assertEqual(len(self.resultado["espectro_discreto_j"]), 5)

    def test_resumen_contiene_sello(self):
        """resumen() debe contener el sello."""
        resumen = self.sistema.resumen()
        self.assertIn("∴APQ∞³", resumen)

    def test_repr_contiene_f0(self):
        """repr debe contener f₀."""
        r = repr(self.sistema)
        self.assertIn("141.7001", r)


# ============================================================================
# TestAPIPublica — 20 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la función pública axiomas_pleroma_qcal_activar()."""

    def setUp(self):
        self.r = axiomas_pleroma_qcal_activar()

    def test_devuelve_dict(self):
        """La función debe devolver un diccionario."""
        self.assertIsInstance(self.r, dict)

    def test_sello(self):
        """r['sello'] debe ser '∴APQ∞³'."""
        self.assertEqual(self.r["sello"], "∴APQ∞³")

    def test_sello_activo_true(self):
        """r['sello_activo'] debe ser True."""
        self.assertTrue(self.r["sello_activo"])

    def test_psi_global_supera_umbral(self):
        """r['psi_global'] debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_f0_correcto(self):
        """r['f0_hz'] debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.r["f0_hz"], 141.7001, places=4)

    def test_vacio_inexistente(self):
        """r['vacio_inexistente'] debe ser True."""
        self.assertTrue(self.r["vacio_inexistente"])

    def test_bucle_estable(self):
        """r['bucle_estable'] debe ser True."""
        self.assertTrue(self.r["bucle_estable"])

    def test_operador_hermitiano(self):
        """r['operador_hermitiano'] debe ser True."""
        self.assertTrue(self.r["operador_hermitiano"])

    def test_sandwitch_abierto(self):
        """r['sandwitch_coherencia_abierto'] debe ser True."""
        self.assertTrue(self.r["sandwitch_coherencia_abierto"])

    def test_coherencias_cinco(self):
        """r['coherencias'] debe tener 5 entradas."""
        self.assertEqual(len(self.r["coherencias"]), 5)

    def test_psi_umbral(self):
        """r['psi_umbral'] debe ser 0.888."""
        self.assertAlmostEqual(self.r["psi_umbral"], 0.888, places=4)

    def test_gamma_1(self):
        """r['gamma_1'] debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.r["gamma_1"], 14.134725, places=5)

    def test_brecha_torsion_deg(self):
        """r['brecha_torsion_deg'] debe ser 3.00052."""
        self.assertAlmostEqual(self.r["brecha_torsion_deg"], 3.00052, places=5)

    def test_suma_primos(self):
        """r['suma_primos'] debe ser 58."""
        self.assertEqual(self.r["suma_primos"], 58)

    def test_certificacion_presente(self):
        """r['certificacion'] debe estar presente y ser una cadena."""
        self.assertIn("certificacion", self.r)
        self.assertIsInstance(self.r["certificacion"], str)

    def test_certificacion_contiene_activo(self):
        """La certificación debe indicar ACTIVO."""
        self.assertIn("ACTIVO", self.r["certificacion"])

    def test_energia_fundamental_rango(self):
        """E₀ debe estar en el rango [1e-33, 1e-30] J."""
        e0 = self.r["energia_fundamental_j"]
        self.assertGreater(e0, 1.0e-33)
        self.assertLess(e0, 1.0e-30)

    def test_idempotente(self):
        """Dos llamadas deben dar el mismo resultado."""
        r2 = axiomas_pleroma_qcal_activar()
        self.assertAlmostEqual(self.r["psi_global"], r2["psi_global"], places=10)
        self.assertEqual(self.r["sello_activo"], r2["sello_activo"])

    def test_psi_axioma1_es_1(self):
        """Ψ₁ (Axioma 1) debe ser 1.0."""
        self.assertAlmostEqual(
            self.r["coherencias"]["psi_axioma1_pleroma_saturado"], 1.0, places=10
        )

    def test_psi_axioma2_alto(self):
        """Ψ₂ (Axioma 2) debe ser ≥ 0.999."""
        self.assertGreaterEqual(
            self.r["coherencias"]["psi_axioma2_bucle_4pi"], 0.999
        )


# ============================================================================
# TestResultadoAxiomasPleroma — 8 tests
# ============================================================================

class TestResultadoAxiomasPleroma(unittest.TestCase):
    """Tests para el dataclass ResultadoAxiomasPleroma."""

    def setUp(self):
        self.res = ResultadoAxiomasPleroma(
            sello="∴APQ∞³",
            ram="RAM-LX-2026-AXIOMAS-PLEROMA-QCAL",
            f0_hz=141.7001,
            psi_global=0.990,
            sello_activo=True,
            coherencias={"psi_axioma1": 1.0},
        )

    def test_sello(self):
        """El sello debe ser '∴APQ∞³'."""
        self.assertEqual(self.res.sello, "∴APQ∞³")

    def test_ram(self):
        """El RAM debe ser correcto."""
        self.assertEqual(self.res.ram, "RAM-LX-2026-AXIOMAS-PLEROMA-QCAL")

    def test_f0_hz(self):
        """f0_hz debe ser 141.7001."""
        self.assertAlmostEqual(self.res.f0_hz, 141.7001, places=4)

    def test_psi_global(self):
        """psi_global debe ser 0.990."""
        self.assertAlmostEqual(self.res.psi_global, 0.990, places=4)

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.res.sello_activo)

    def test_coherencias(self):
        """coherencias debe ser un dict."""
        self.assertIsInstance(self.res.coherencias, dict)

    def test_coherencias_value(self):
        """coherencias debe contener los valores correctos."""
        self.assertAlmostEqual(self.res.coherencias["psi_axioma1"], 1.0, places=4)

    def test_instanciable(self):
        """El dataclass debe ser instanciable sin error."""
        res2 = ResultadoAxiomasPleroma(
            sello="test",
            ram="RAM-TEST",
            f0_hz=100.0,
            psi_global=0.5,
            sello_activo=False,
            coherencias={},
        )
        self.assertFalse(res2.sello_activo)


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
