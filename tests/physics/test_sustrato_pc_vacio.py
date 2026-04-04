#!/usr/bin/env python3
"""
Tests for physics.sustrato_pc_vacio — Sustrato PC-Vacío ∴SPC∞³

Suite de pruebas exhaustiva que cubre todas las clases y la API pública:
  - ConstantesSustrato        – constantes físicas (F₀, primos, fase Berry)
  - VacioSuperfluido          – superfluido de Bose-Einstein, ν→0
  - RedRamsey                 – red C₇, 7 nodos primos, frecuencia heterodina
  - AcoplamientoHiggsPC       – ℒ_int, masa efectiva m*(t), Destello de Masa
  - FotonPaqueteFase          – R_symb, cooperatividad ξ, sincronización Dicke
  - FirmaEspectral            – sidebands de masa, oscilación σ, transparencia
  - CoherenciaSustrato        – validación Ψ ≥ 0.888
  - SistemaSustratoPCVacio    – orquestador principal
  - sustrato_pc_vacio_activar() — API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - Primos P = {2,3,5,7,11,13,17}
  - Fase Berry Φ = π/8 rad
  - Suma primos = 58
  - g_eff = 0.053 (perturbativo)
  - Reducción de inercia = 5.3 %
  - R_symb ≈ 991.9 kpps
  - Ψ_global ≥ 0.888 → sello ∴SPC∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
RAM: RAM-XLVIII-2026-SUSTRATO-PC-VACIO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.sustrato_pc_vacio import (
    # Constantes de módulo
    _F0,
    _OMEGA_0,
    _T0,
    _PRIMOS_P,
    _FASE_BERRY_RAD,
    _N_NODOS,
    _G_EFF,
    _XI_COOPER,
    _KAPPA_PI,
    _A_EFF_HZ,
    _DELTA_INERCIA,
    _N_SUPERRAD,
    _R_SYMB_TARGET,
    _PSI_UMBRAL,
    _M_HIGGS_GEV,
    _GAMMA_1_RIEMANN,
    _PHI,
    # Clases
    ConstantesSustrato,
    VacioSuperfluido,
    RedRamsey,
    AcoplamientoHiggsPC,
    FotonPaqueteFase,
    FirmaEspectral,
    CoherenciaSustrato,
    SistemaSustratoPCVacio,
    # API pública
    sustrato_pc_vacio_activar,
)


# ============================================================================
# TestModuleConstants – 20 tests
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

    def test_primos_p_count(self):
        """Deben existir exactamente 7 nodos primos."""
        self.assertEqual(len(_PRIMOS_P), 7)

    def test_primos_p_values(self):
        """Los primos deben ser {2,3,5,7,11,13,17}."""
        self.assertEqual(set(_PRIMOS_P), {2, 3, 5, 7, 11, 13, 17})

    def test_primos_p_are_prime(self):
        """Todos los elementos de _PRIMOS_P deben ser primos."""
        def es_primo(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        for p in _PRIMOS_P:
            with self.subTest(p=p):
                self.assertTrue(es_primo(p), f"{p} no es primo")

    def test_fase_berry_rad(self):
        """_FASE_BERRY_RAD debe ser π/8."""
        self.assertAlmostEqual(_FASE_BERRY_RAD, math.pi / 8.0, places=10)

    def test_n_nodos(self):
        """_N_NODOS debe ser 7."""
        self.assertEqual(_N_NODOS, 7)

    def test_g_eff_value(self):
        """_G_EFF debe ser 0.053."""
        self.assertAlmostEqual(_G_EFF, 0.053, places=5)

    def test_g_eff_perturbativo(self):
        """_G_EFF debe ser perturbativo (< 0.1)."""
        self.assertLess(_G_EFF, 0.1)

    def test_xi_cooper_value(self):
        """_XI_COOPER debe ser ≈ 0.053."""
        self.assertAlmostEqual(_XI_COOPER, 0.053, places=5)

    def test_kappa_pi_value(self):
        """_KAPPA_PI debe ser ≈ 0.053."""
        self.assertAlmostEqual(_KAPPA_PI, 0.053, places=5)

    def test_delta_inercia_value(self):
        """_DELTA_INERCIA debe ser 0.053 (5.3 %)."""
        self.assertAlmostEqual(_DELTA_INERCIA, 0.053, places=5)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_m_higgs_gev(self):
        """_M_HIGGS_GEV debe ser 125.25 GeV."""
        self.assertAlmostEqual(_M_HIGGS_GEV, 125.25, places=2)

    def test_gamma_1_riemann(self):
        """_GAMMA_1_RIEMANN debe ser ≈ 14.134725."""
        self.assertAlmostEqual(_GAMMA_1_RIEMANN, 14.134725, places=4)

    def test_phi_golden_ratio(self):
        """_PHI debe ser la proporción áurea (1+√5)/2."""
        self.assertAlmostEqual(_PHI, (1.0 + math.sqrt(5.0)) / 2.0, places=10)

    def test_r_symb_target(self):
        """_R_SYMB_TARGET debe ser ≈ 991.9 kpps."""
        self.assertAlmostEqual(_R_SYMB_TARGET / 1.0e3, 991.9, places=0)

    def test_a_eff_hz(self):
        """_A_EFF_HZ debe ser igual a _F0."""
        self.assertAlmostEqual(_A_EFF_HZ, _F0, places=4)


# ============================================================================
# TestConstantesSustrato – 15 tests
# ============================================================================

class TestConstantesSustrato(unittest.TestCase):
    """Tests para la clase ConstantesSustrato."""

    def setUp(self):
        self.c = ConstantesSustrato()

    def test_f0(self):
        """f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_omega_0(self):
        """omega_0 debe ser 2π × f0."""
        self.assertAlmostEqual(self.c.omega_0, 2.0 * math.pi * self.c.f0, places=5)

    def test_t0(self):
        """t0 debe ser 1/f0."""
        self.assertAlmostEqual(self.c.t0, 1.0 / self.c.f0, places=10)

    def test_primos_count(self):
        """Deben existir 7 primos."""
        self.assertEqual(len(self.c.primos_p), 7)

    def test_n_nodos(self):
        """n_nodos debe ser 7."""
        self.assertEqual(self.c.n_nodos, 7)

    def test_fase_berry_rad(self):
        """Fase de Berry debe ser π/8."""
        self.assertAlmostEqual(self.c.fase_berry_rad, math.pi / 8.0, places=10)

    def test_fase_berry_total(self):
        """Fase total debe ser 7 × π/8."""
        self.assertAlmostEqual(
            self.c.fase_berry_total(), 7.0 * math.pi / 8.0, places=10
        )

    def test_suma_primos(self):
        """Suma de primos {2+3+5+7+11+13+17} = 58."""
        self.assertEqual(self.c.suma_primos(), 58)

    def test_producto_primos(self):
        """Producto de los 7 primos."""
        expected = 2 * 3 * 5 * 7 * 11 * 13 * 17
        self.assertEqual(self.c.producto_primos(), expected)

    def test_g_eff(self):
        """g_eff debe ser 0.053."""
        self.assertAlmostEqual(self.c.g_eff, 0.053, places=5)

    def test_es_perturbativo(self):
        """g_eff debe ser perturbativo."""
        self.assertTrue(self.c.es_perturbativo())

    def test_psi_umbral(self):
        """Umbral debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_m_higgs_gev(self):
        """Masa de Higgs debe ser 125.25 GeV."""
        self.assertAlmostEqual(self.c.m_higgs_gev, 125.25, places=2)

    def test_hbar_positive(self):
        """ℏ debe ser positivo."""
        self.assertGreater(self.c.hbar, 0.0)

    def test_c_speed_of_light(self):
        """Velocidad de la luz debe ser ~3×10⁸ m/s."""
        self.assertAlmostEqual(self.c.c / 3.0e8, 1.0, places=1)


# ============================================================================
# TestVacioSuperfluido – 15 tests
# ============================================================================

class TestVacioSuperfluido(unittest.TestCase):
    """Tests para la clase VacioSuperfluido."""

    def setUp(self):
        self.vs = VacioSuperfluido()

    def test_es_superfluido_default(self):
        """El vacío por defecto debe ser superfluido (ν < 1e-10)."""
        self.assertTrue(self.vs.es_superfluido())

    def test_no_es_superfluido_alta_viscosidad(self):
        """Con ν=0.1, no debe ser superfluido."""
        vs_alto = VacioSuperfluido(viscosidad_nu=0.1)
        self.assertFalse(vs_alto.es_superfluido())

    def test_fraccion_pc(self):
        """Fracción PC debe ser 0.95."""
        self.assertAlmostEqual(self.vs.fraccion_pc, 0.95, places=5)

    def test_fuerza_ramsey_cero(self):
        """F_Ramsey con gradiente cero debe ser cero."""
        self.assertAlmostEqual(self.vs.fuerza_ramsey(0.0), 0.0, places=10)

    def test_fuerza_ramsey_sign(self):
        """F_Ramsey con gradiente positivo debe ser negativa."""
        self.assertLess(self.vs.fuerza_ramsey(1.0), 0.0)

    def test_velocidad_de_fase(self):
        """Velocidad de fase debe ser igual a c."""
        vf = self.vs.velocidad_de_fase(_F0)
        self.assertAlmostEqual(vf, 299792458.0, delta=1.0)

    def test_numero_mach_cuantico_pequeño(self):
        """M_q para v=1 m/s debe ser muy pequeño."""
        mach = self.vs.numero_mach_cuantico(1.0)
        self.assertLess(mach, 1.0e-8)

    def test_entropia_vacio_pequeña(self):
        """Entropía del vacío superfluido debe ser ≈ 0."""
        self.assertLess(self.vs.entropia_vacio(), 1.0e-10)

    def test_psi_superfluido_alta(self):
        """Ψ_sf debe ser ≈ 0.95 en límite superfluido."""
        self.assertAlmostEqual(self.vs.psi_superfluido(), 0.95, places=5)

    def test_psi_superfluido_positivo(self):
        """Ψ_sf debe ser positivo."""
        self.assertGreater(self.vs.psi_superfluido(), 0.0)

    def test_psi_superfluido_maximo_one(self):
        """Ψ_sf debe ser ≤ 1.0."""
        self.assertLessEqual(self.vs.psi_superfluido(), 1.0)

    def test_densidad_rho_default(self):
        """Densidad ρ por defecto debe ser 1.0."""
        self.assertAlmostEqual(self.vs.densidad_rho, 1.0, places=5)

    def test_viscosidad_nu_muy_pequeña(self):
        """Viscosidad ν por defecto debe ser ≈ 1e-15."""
        self.assertAlmostEqual(self.vs.viscosidad_nu, 1.0e-15, places=20)

    def test_fuerza_ramsey_proporcional(self):
        """F_Ramsey debe ser proporcional al gradiente."""
        f1 = self.vs.fuerza_ramsey(2.0)
        f2 = self.vs.fuerza_ramsey(4.0)
        self.assertAlmostEqual(f2, 2.0 * f1, places=10)

    def test_repr_contiene_nu(self):
        """__repr__ debe mencionar ν."""
        r = repr(self.vs)
        self.assertIn("ν", r)


# ============================================================================
# TestRedRamsey – 20 tests
# ============================================================================

class TestRedRamsey(unittest.TestCase):
    """Tests para la clase RedRamsey."""

    def setUp(self):
        self.red = RedRamsey()

    def test_n_nodos(self):
        """n_nodos debe ser 7."""
        self.assertEqual(self.red.n_nodos(), 7)

    def test_primos_count(self):
        """El ciclo debe tener 7 nodos primos."""
        self.assertEqual(len(self.red.primos), 7)

    def test_primos_values(self):
        """Primos deben ser {2,3,5,7,11,13,17}."""
        self.assertEqual(set(self.red.primos), {2, 3, 5, 7, 11, 13, 17})

    def test_fase_berry(self):
        """Fase de Berry debe ser π/8."""
        self.assertAlmostEqual(self.red.fase_berry, math.pi / 8.0, places=10)

    def test_fase_berry_acumulada(self):
        """Fase acumulada debe ser 7π/8."""
        self.assertAlmostEqual(
            self.red.fase_berry_acumulada(), 7.0 * math.pi / 8.0, places=10
        )

    def test_integral_aharanov_bohm(self):
        """∮ A_Berry·dℓ debe ser 7π/8."""
        self.assertAlmostEqual(
            self.red.integral_aharanov_bohm(), 7.0 * math.pi / 8.0, places=10
        )

    def test_contribucion_chern_simons_positiva(self):
        """La contribución CS debe ser positiva (ω₀ > 7π/8)."""
        cs = self.red.contribucion_chern_simons()
        self.assertGreater(cs, 0.0)

    def test_contribucion_chern_simons_completa(self):
        """Berry + CS debe dar ω₀."""
        total = self.red.integral_aharanov_bohm() + self.red.contribucion_chern_simons()
        omega_0 = 2.0 * math.pi * _F0
        self.assertAlmostEqual(total, omega_0, places=5)

    def test_frecuencia_heterodina(self):
        """La frecuencia heterodina debe ser exactamente f₀."""
        f_het = self.red.frecuencia_heterodina_hz()
        self.assertAlmostEqual(f_het, _F0, places=4)

    def test_frecuencia_heterodina_141hz(self):
        """La frecuencia heterodina debe ser ≈ 141.7001 Hz."""
        self.assertAlmostEqual(self.red.frecuencia_heterodina_hz(), 141.7001, places=4)

    def test_es_linea_critica_riemann(self):
        """La línea crítica de Riemann debe estar activa."""
        self.assertTrue(self.red.es_linea_critica_riemann())

    def test_modos_resonantes_count(self):
        """Deben existir 7 modos resonantes."""
        modos = self.red.modos_resonantes_hz()
        self.assertEqual(len(modos), 7)

    def test_modos_resonantes_primer_modo(self):
        """El primer modo resonante debe ser f₀ = 141.7001 Hz."""
        modos = self.red.modos_resonantes_hz()
        self.assertAlmostEqual(modos[0], _F0, places=4)

    def test_modos_resonantes_crecientes(self):
        """Los modos resonantes deben ser crecientes."""
        modos = self.red.modos_resonantes_hz()
        for i in range(len(modos) - 1):
            self.assertLess(modos[i], modos[i + 1])

    def test_psi_red_valor(self):
        """Coherencia de la red debe ser 1.0 (f_hetero = f₀ por construcción)."""
        psi = self.red.psi_red()
        self.assertAlmostEqual(psi, 1.0, places=6)

    def test_psi_red_rango(self):
        """Ψ_red debe estar en [0, 1]."""
        psi = self.red.psi_red()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_fase_berry_por_nodo(self):
        """Fase Berry por nodo debe ser π/8."""
        self.assertAlmostEqual(self.red.fase_berry, math.pi / 8.0, places=10)

    def test_suma_primos_coherencia(self):
        """Suma de primos × fase_berry/2π debe dar una frecuencia coherente."""
        # Solo verificamos que la suma de primos es consistente
        suma = sum(self.red.primos)
        self.assertEqual(suma, 58)

    def test_repr_contiene_f0(self):
        """__repr__ debe mencionar la frecuencia."""
        r = repr(self.red)
        self.assertIn("141", r)

    def test_modos_resonantes_positivos(self):
        """Todos los modos resonantes deben ser positivos."""
        modos = self.red.modos_resonantes_hz()
        for f in modos:
            self.assertGreater(f, 0.0)


# ============================================================================
# TestAcoplamientoHiggsPC – 20 tests
# ============================================================================

class TestAcoplamientoHiggsPC(unittest.TestCase):
    """Tests para la clase AcoplamientoHiggsPC."""

    def setUp(self):
        self.ac = AcoplamientoHiggsPC()

    def test_m0_gev(self):
        """Masa en reposo debe ser 125.25 GeV/c²."""
        self.assertAlmostEqual(self.ac.m0_gev, 125.25, places=2)

    def test_g_eff(self):
        """g_eff debe ser 0.053."""
        self.assertAlmostEqual(self.ac.g_eff, 0.053, places=5)

    def test_kappa_pi(self):
        """κ_Π debe ser 0.053."""
        self.assertAlmostEqual(self.ac.kappa_pi, 0.053, places=5)

    def test_f0_hz(self):
        """f₀ debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.ac.f0_hz, 141.7001, places=4)

    def test_lagrangiano_int_negativo(self):
        """ℒ_int = -g_eff ψ̄ψ H debe ser negativo."""
        self.assertLess(self.ac.lagrangiano_int(1.0, 1.0), 0.0)

    def test_lagrangiano_int_formula(self):
        """ℒ_int debe ser -g_eff × psi_densidad × h_campo."""
        val = self.ac.lagrangiano_int(2.0, 3.0)
        self.assertAlmostEqual(val, -0.053 * 2.0 * 3.0, places=8)

    def test_masa_efectiva_menor_m0(self):
        """m* debe ser menor que m₀ (Destello reduce la masa)."""
        m_star = self.ac.masa_efectiva_gev()
        self.assertLess(m_star, self.ac.m0_gev)

    def test_masa_efectiva_reduccion_5pct(self):
        """La reducción de m* debe ser ≈ 5.3 %."""
        m_star = self.ac.masa_efectiva_gev()
        reduccion = (self.ac.m0_gev - m_star) / self.ac.m0_gev
        self.assertAlmostEqual(reduccion, 0.053, places=5)

    def test_masa_efectiva_valor(self):
        """m* debe ser ≈ 125.25 × 0.947 ≈ 118.61 GeV."""
        m_star = self.ac.masa_efectiva_gev()
        expected = 125.25 * (1.0 - 0.053)
        self.assertAlmostEqual(m_star, expected, places=3)

    def test_reduccion_inercia_valor(self):
        """Reducción de inercia debe ser ≈ 0.053."""
        red = self.ac.reduccion_inercia()
        self.assertAlmostEqual(red, 0.053, places=5)

    def test_reduccion_inercia_pct(self):
        """Reducción de inercia debe ser 5.3 %."""
        red_pct = self.ac.reduccion_inercia() * 100.0
        self.assertAlmostEqual(red_pct, 5.3, places=4)

    def test_es_destello_activo(self):
        """El Destello de Masa debe estar activo (reducción ≥ 5 %)."""
        self.assertTrue(self.ac.es_destello_activo())

    def test_sideband_masa_n1(self):
        """Sidebands de orden 1 deben ser simétricas."""
        sb_low, sb_up = self.ac.sideband_masa_gev(n=1)
        media = (sb_low + sb_up) / 2.0
        self.assertAlmostEqual(media, self.ac.m0_gev, places=5)

    def test_sideband_masa_delta_simetrico(self):
        """Δm_lower = Δm_upper."""
        sb_low, sb_up = self.ac.sideband_masa_gev(n=1)
        delta_low = self.ac.m0_gev - sb_low
        delta_up = sb_up - self.ac.m0_gev
        self.assertAlmostEqual(delta_low, delta_up, places=10)

    def test_sideband_n2_mayor_n1(self):
        """Los sidebands de orden 2 deben estar más lejos que los de orden 1."""
        sb1_low, sb1_up = self.ac.sideband_masa_gev(n=1)
        sb2_low, sb2_up = self.ac.sideband_masa_gev(n=2)
        self.assertLessEqual(sb2_low, sb1_low)
        self.assertGreaterEqual(sb2_up, sb1_up)

    def test_psi_acoplamiento_alta(self):
        """Ψ_acoplamiento debe ser ≈ 1.0 (régimen perturbativo)."""
        psi = self.ac.psi_acoplamiento()
        self.assertGreater(psi, 0.999)

    def test_psi_acoplamiento_rango(self):
        """Ψ_acoplamiento debe estar en [0, 1]."""
        psi = self.ac.psi_acoplamiento()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_lagrangiano_int_cero_campo(self):
        """ℒ_int con H=0 debe ser cero."""
        val = self.ac.lagrangiano_int(1.0, 0.0)
        self.assertAlmostEqual(val, 0.0, places=10)

    def test_lagrangiano_int_cero_densidad(self):
        """ℒ_int con ψ=0 debe ser cero."""
        val = self.ac.lagrangiano_int(0.0, 1.0)
        self.assertAlmostEqual(val, 0.0, places=10)

    def test_repr_contiene_masa(self):
        """__repr__ debe mencionar la masa."""
        r = repr(self.ac)
        self.assertIn("125", r)


# ============================================================================
# TestFotonPaqueteFase – 15 tests
# ============================================================================

class TestFotonPaqueteFase(unittest.TestCase):
    """Tests para la clase FotonPaqueteFase."""

    def setUp(self):
        self.fot = FotonPaqueteFase()

    def test_n_emisores(self):
        """Número de emisores debe ser N_SUPERRAD."""
        self.assertEqual(self.fot.n_emisores, _N_SUPERRAD)

    def test_f0_hz(self):
        """f₀ debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.fot.f0_hz, 141.7001, places=4)

    def test_xi_cooper(self):
        """ξ debe ser 0.053."""
        self.assertAlmostEqual(self.fot.xi_cooper, 0.053, places=5)

    def test_tasa_simbolica_pps(self):
        """R_symb en pps debe ser ≈ 991.9 kpps."""
        r_pps = self.fot.tasa_simbolica_pps()
        self.assertAlmostEqual(r_pps / 1.0e3, 991.9, delta=5.0)

    def test_tasa_simbolica_kpps(self):
        """R_symb en kpps debe ser ≈ 991.9."""
        r_kpps = self.fot.tasa_simbolica_kpps()
        self.assertAlmostEqual(r_kpps, 991.9, delta=5.0)

    def test_expansion_seccion_eficaz(self):
        """Factor de expansión debe ser 10⁶."""
        self.assertAlmostEqual(
            self.fot.expansion_seccion_eficaz(), 1.0e6, delta=1.0
        )

    def test_ganancia_superradiante(self):
        """Ganancia superradiante debe ser N² = 49."""
        self.assertAlmostEqual(self.fot.ganancia_superradiante(), 49.0, places=5)

    def test_energia_foton_j(self):
        """Energía del fotón debe ser h × f₀ > 0."""
        e = self.fot.energia_foton_j()
        self.assertGreater(e, 0.0)

    def test_energia_foton_formula(self):
        """E = h × f₀."""
        from qcal.constants import H_PLANCK
        e = self.fot.energia_foton_j()
        self.assertAlmostEqual(e, H_PLANCK * _F0, places=40)

    def test_coherencia_dicke_rango(self):
        """Ψ_Dicke debe estar en [0, 1]."""
        psi_d = self.fot.coherencia_dicke()
        self.assertGreaterEqual(psi_d, 0.0)
        self.assertLessEqual(psi_d, 1.0)

    def test_coherencia_dicke_valor(self):
        """Ψ_Dicke = 1 - 1/N² = 1 - 1/49 ≈ 0.9796."""
        psi_d = self.fot.coherencia_dicke()
        self.assertAlmostEqual(psi_d, 1.0 - 1.0/49.0, places=5)

    def test_psi_transmision_rango(self):
        """Ψ_trans debe estar en [0, 1]."""
        psi_t = self.fot.psi_transmision()
        self.assertGreaterEqual(psi_t, 0.0)
        self.assertLessEqual(psi_t, 1.0)

    def test_psi_transmision_alta(self):
        """Ψ_trans debe ser ≥ 0.888 (alta coherencia)."""
        psi_t = self.fot.psi_transmision()
        self.assertGreaterEqual(psi_t, 0.888)

    def test_tasa_simbolica_positiva(self):
        """R_symb debe ser positiva."""
        self.assertGreater(self.fot.tasa_simbolica_pps(), 0.0)

    def test_repr_contiene_r_symb(self):
        """__repr__ debe mostrar R_symb."""
        r = repr(self.fot)
        self.assertIn("kpps", r)


# ============================================================================
# TestFirmaEspectral – 15 tests
# ============================================================================

class TestFirmaEspectral(unittest.TestCase):
    """Tests para la clase FirmaEspectral."""

    def setUp(self):
        self.fe = FirmaEspectral()

    def test_m_higgs_gev(self):
        """Masa del Higgs debe ser 125.25 GeV."""
        self.assertAlmostEqual(self.fe.m_higgs_gev, 125.25, places=2)

    def test_delta_inercia(self):
        """δ_inercia debe ser 0.053."""
        self.assertAlmostEqual(self.fe.delta_inercia, 0.053, places=5)

    def test_f0_hz(self):
        """f₀ debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.fe.f0_hz, 141.7001, places=4)

    def test_sidebands_count(self):
        """sidebands_gev(3) debe devolver 3 elementos."""
        sbs = self.fe.sidebands_gev(3)
        self.assertEqual(len(sbs), 3)

    def test_sidebands_simetrico(self):
        """Los sidebands deben ser simétricos respecto a m_H."""
        sbs = self.fe.sidebands_gev(3)
        for n, sb_low, sb_up in sbs:
            media = (sb_low + sb_up) / 2.0
            self.assertAlmostEqual(media, self.fe.m_higgs_gev, places=5)

    def test_sidebands_orden(self):
        """Los sidebands deben respetar el índice de orden."""
        sbs = self.fe.sidebands_gev(3)
        deltas = [sb_up - self.fe.m_higgs_gev for _, _, sb_up in sbs]
        for i in range(len(deltas) - 1):
            self.assertLessEqual(deltas[i], deltas[i + 1])

    def test_oscilacion_seccion_eficaz_t0(self):
        """σ(t=0) debe ser 1 + δ_inercia."""
        sigma = self.fe.oscilacion_seccion_eficaz(0.0)
        self.assertAlmostEqual(sigma, 1.0 + self.fe.delta_inercia, places=8)

    def test_oscilacion_seccion_eficaz_media(self):
        """Media temporal de σ(t) debe ser ≈ 1.0."""
        from qcal.constants import F0_HZ
        t_period = 1.0 / F0_HZ
        n = 1000
        sigma_sum = sum(
            self.fe.oscilacion_seccion_eficaz(i * t_period / n)
            for i in range(n)
        )
        self.assertAlmostEqual(sigma_sum / n, 1.0, places=3)

    def test_amplitud_oscilacion_pct(self):
        """Amplitud de oscilación debe ser ≈ 5.3 %."""
        self.assertAlmostEqual(
            self.fe.amplitud_oscilacion_porcentaje(), 5.3, places=4
        )

    def test_ventana_transparencia_hz(self):
        """Ventana de transparencia debe ser f₀."""
        self.assertAlmostEqual(
            self.fe.ventana_transparencia_hz(), _F0, places=4
        )

    def test_coherencia_espectral_valor(self):
        """Ψ_esp = 1 - δ_inercia = 0.947."""
        psi_e = self.fe.coherencia_espectral()
        self.assertAlmostEqual(psi_e, 1.0 - self.fe.delta_inercia, places=8)

    def test_coherencia_espectral_alta(self):
        """Ψ_esp debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.fe.coherencia_espectral(), 0.888)

    def test_coherencia_espectral_rango(self):
        """Ψ_esp debe estar en [0, 1]."""
        psi_e = self.fe.coherencia_espectral()
        self.assertGreaterEqual(psi_e, 0.0)
        self.assertLessEqual(psi_e, 1.0)

    def test_oscilacion_seccion_eficaz_acotada(self):
        """σ(t) debe estar acotada entre (1-δ) y (1+δ)."""
        for t in [0.0, 0.001, 0.002, 0.005]:
            sigma = self.fe.oscilacion_seccion_eficaz(t)
            self.assertGreater(sigma, 1.0 - self.fe.delta_inercia - 1e-10)
            self.assertLess(sigma, 1.0 + self.fe.delta_inercia + 1e-10)

    def test_repr_contiene_pct(self):
        """__repr__ debe mostrar el porcentaje."""
        r = repr(self.fe)
        self.assertIn("%", r)


# ============================================================================
# TestCoherenciaSustrato – 20 tests
# ============================================================================

class TestCoherenciaSustrato(unittest.TestCase):
    """Tests para la clase CoherenciaSustrato."""

    def setUp(self):
        self.coh = CoherenciaSustrato()

    def test_psi_umbral(self):
        """Umbral debe ser 0.888."""
        self.assertAlmostEqual(self.coh.psi_umbral, 0.888, places=3)

    def test_coherencias_individuales_count(self):
        """Deben existir 5 coherencias individuales."""
        ci = self.coh.coherencias_individuales()
        self.assertEqual(len(ci), 5)

    def test_coherencias_keys(self):
        """Las claves deben incluir todos los subsistemas."""
        ci = self.coh.coherencias_individuales()
        keys = set(ci.keys())
        self.assertIn("psi_vacio_superfluido", keys)
        self.assertIn("psi_red_ramsey", keys)
        self.assertIn("psi_acoplamiento_higgspc", keys)
        self.assertIn("psi_transmision_fotonico", keys)
        self.assertIn("psi_firma_espectral", keys)

    def test_psi_vacio_superfluido(self):
        """Ψ_vacio debe ser ≈ 0.95."""
        ci = self.coh.coherencias_individuales()
        self.assertAlmostEqual(ci["psi_vacio_superfluido"], 0.95, places=5)

    def test_psi_red_ramsey(self):
        """Ψ_red debe ser ≈ 1.0."""
        ci = self.coh.coherencias_individuales()
        self.assertAlmostEqual(ci["psi_red_ramsey"], 1.0, places=5)

    def test_psi_acoplamiento_alta(self):
        """Ψ_acoplamiento debe ser ≈ 1.0."""
        ci = self.coh.coherencias_individuales()
        self.assertGreater(ci["psi_acoplamiento_higgspc"], 0.999)

    def test_psi_firma_espectral(self):
        """Ψ_firma debe ser 1 - 0.053 = 0.947."""
        ci = self.coh.coherencias_individuales()
        self.assertAlmostEqual(ci["psi_firma_espectral"], 0.947, places=5)

    def test_coherencias_todas_en_rango(self):
        """Todas las coherencias individuales deben estar en [0, 1]."""
        ci = self.coh.coherencias_individuales()
        for nombre, valor in ci.items():
            with self.subTest(nombre=nombre):
                self.assertGreaterEqual(valor, 0.0, f"{nombre} < 0")
                self.assertLessEqual(valor, 1.0, f"{nombre} > 1")

    def test_psi_global_supera_umbral(self):
        """Ψ_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.888)

    def test_psi_global_rango(self):
        """Ψ_global debe estar en [0, 1]."""
        psi = self.coh.psi_global()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_sello_activo(self):
        """El sello ∴SPC∞³ debe estar activo."""
        self.assertTrue(self.coh.sello_activo())

    def test_validar_estructura(self):
        """validar() debe devolver las claves requeridas."""
        v = self.coh.validar()
        self.assertIn("coherencias", v)
        self.assertIn("psi_global", v)
        self.assertIn("psi_umbral", v)
        self.assertIn("sello_activo", v)

    def test_validar_sello_activo(self):
        """validar()['sello_activo'] debe ser True."""
        v = self.coh.validar()
        self.assertTrue(v["sello_activo"])

    def test_validar_psi_global_consistente(self):
        """psi_global en validar() debe coincidir con psi_global()."""
        v = self.coh.validar()
        self.assertAlmostEqual(v["psi_global"], self.coh.psi_global(), places=10)

    def test_validar_psi_umbral_consistente(self):
        """psi_umbral en validar() debe coincidir con self.psi_umbral."""
        v = self.coh.validar()
        self.assertAlmostEqual(v["psi_umbral"], self.coh.psi_umbral, places=10)

    def test_certificacion_auron_contiene_sello(self):
        """Certificación debe mencionar el sello."""
        cert = self.coh.certificacion_auron()
        self.assertIn("SPC∞³", cert)

    def test_certificacion_auron_contiene_activo(self):
        """Certificación debe indicar que está activo."""
        cert = self.coh.certificacion_auron()
        self.assertIn("ACTIVO", cert)

    def test_psi_global_media_geometrica(self):
        """Ψ_global debe ser la media geométrica de las coherencias."""
        ci = self.coh.coherencias_individuales()
        valores = list(ci.values())
        log_sum = sum(math.log(max(v, 1.0e-30)) for v in valores)
        expected = math.exp(log_sum / len(valores))
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=10)

    def test_repr_contiene_psi_global(self):
        """__repr__ debe mostrar Ψ_global."""
        r = repr(self.coh)
        self.assertIn("Ψ_global", r)

    def test_sello_activo_consistente_con_umbral(self):
        """sello_activo() debe ser equivalente a psi_global() ≥ psi_umbral."""
        activo = self.coh.sello_activo()
        supera = self.coh.psi_global() >= self.coh.psi_umbral
        self.assertEqual(activo, supera)


# ============================================================================
# TestSistemaSustratoPCVacio – 20 tests
# ============================================================================

class TestSistemaSustratoPCVacio(unittest.TestCase):
    """Tests para la clase SistemaSustratoPCVacio."""

    def setUp(self):
        self.sistema = SistemaSustratoPCVacio()

    def test_activar_devuelve_dict(self):
        """activar() debe devolver un diccionario."""
        r = self.sistema.activar()
        self.assertIsInstance(r, dict)

    def test_activar_sello(self):
        """Sello debe ser ∴SPC∞³."""
        r = self.sistema.activar()
        self.assertEqual(r["sello"], "∴SPC∞³")

    def test_activar_ram(self):
        """RAM debe ser correcto."""
        r = self.sistema.activar()
        self.assertEqual(r["ram"], "RAM-XLVIII-2026-SUSTRATO-PC-VACIO")

    def test_activar_version(self):
        """Versión debe ser 1.0.0."""
        r = self.sistema.activar()
        self.assertEqual(r["version"], "1.0.0")

    def test_activar_f0_hz(self):
        """f₀ en resultado debe ser 141.7001 Hz."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r["f0_hz"], 141.7001, places=4)

    def test_activar_primos_p(self):
        """primos_p debe ser [2,3,5,7,11,13,17]."""
        r = self.sistema.activar()
        self.assertEqual(r["primos_p"], [2, 3, 5, 7, 11, 13, 17])

    def test_activar_suma_primos(self):
        """Suma de primos debe ser 58."""
        r = self.sistema.activar()
        self.assertEqual(r["suma_primos"], 58)

    def test_activar_g_eff(self):
        """g_eff debe ser 0.053."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r["g_eff"], 0.053, places=5)

    def test_activar_es_superfluido(self):
        """El sistema debe ser superfluido."""
        r = self.sistema.activar()
        self.assertTrue(r["es_superfluido"])

    def test_activar_frecuencia_heterodina(self):
        """Frecuencia heterodina debe ser ≈ f₀."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r["frecuencia_heterodina_hz"], _F0, places=4)

    def test_activar_linea_critica(self):
        """Línea crítica de Riemann debe ser True."""
        r = self.sistema.activar()
        self.assertTrue(r["linea_critica_riemann"])

    def test_activar_reduccion_inercia_pct(self):
        """Reducción de inercia debe ser ≈ 5.3 %."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r["reduccion_inercia_pct"], 5.3, places=4)

    def test_activar_destello_activo(self):
        """El Destello de Masa debe estar activo."""
        r = self.sistema.activar()
        self.assertTrue(r["destello_activo"])

    def test_activar_r_symb_kpps(self):
        """R_symb debe ser ≈ 991.9 kpps."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r["r_symb_kpps"], 991.9, delta=5.0)

    def test_activar_psi_global_supera_umbral(self):
        """Ψ_global debe ser ≥ 0.888."""
        r = self.sistema.activar()
        self.assertGreaterEqual(r["psi_global"], 0.888)

    def test_activar_sello_activo(self):
        """sello_activo debe ser True."""
        r = self.sistema.activar()
        self.assertTrue(r["sello_activo"])

    def test_activar_perturbativo(self):
        """Acoplamiento debe ser perturbativo."""
        r = self.sistema.activar()
        self.assertTrue(r["perturbativo"])

    def test_activar_sidebands_count(self):
        """Debe haber 3 sidebands en el resultado."""
        r = self.sistema.activar()
        self.assertEqual(len(r["sidebands_gev"]), 3)

    def test_resumen_contiene_f0(self):
        """Resumen debe mencionar f₀."""
        resumen = self.sistema.resumen()
        self.assertIn("141", resumen)

    def test_repr_contiene_activo(self):
        """__repr__ debe indicar el estado del sello."""
        r = repr(self.sistema)
        self.assertIn("ACTIVO", r)


# ============================================================================
# TestSustratoPCVacioActivar – 25 tests (API pública)
# ============================================================================

class TestSustratoPCVacioActivar(unittest.TestCase):
    """Tests para la función sustrato_pc_vacio_activar() (API pública)."""

    def setUp(self):
        self.resultado = sustrato_pc_vacio_activar()

    def test_devuelve_dict(self):
        """Debe devolver un diccionario."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello(self):
        """Sello debe ser ∴SPC∞³."""
        self.assertEqual(self.resultado["sello"], "∴SPC∞³")

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.resultado["sello_activo"])

    def test_psi_global_umbral(self):
        """Ψ_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.resultado["psi_global"], 0.888)

    def test_f0_hz(self):
        """f₀ debe ser exactamente 141.7001 Hz."""
        self.assertAlmostEqual(self.resultado["f0_hz"], 141.7001, places=4)

    def test_primos_p(self):
        """Nodos primos deben ser [2,3,5,7,11,13,17]."""
        self.assertEqual(self.resultado["primos_p"], [2, 3, 5, 7, 11, 13, 17])

    def test_suma_primos_58(self):
        """Suma de primos debe ser 58."""
        self.assertEqual(self.resultado["suma_primos"], 58)

    def test_g_eff_perturbativo(self):
        """g_eff debe ser perturbativo (< 0.1)."""
        self.assertLess(self.resultado["g_eff"], 0.1)

    def test_fase_berry_pi_sobre_8(self):
        """Fase Berry debe ser π/8."""
        self.assertAlmostEqual(
            self.resultado["fase_berry_rad"], math.pi / 8.0, places=10
        )

    def test_fase_berry_total(self):
        """Fase Berry total debe ser 7π/8."""
        self.assertAlmostEqual(
            self.resultado["fase_berry_total_rad"], 7.0 * math.pi / 8.0, places=10
        )

    def test_es_superfluido(self):
        """Sistema debe ser superfluido."""
        self.assertTrue(self.resultado["es_superfluido"])

    def test_entropia_vacio_pequeña(self):
        """Entropía del vacío debe ser ≈ 0."""
        self.assertLess(self.resultado["entropia_vacio"], 1.0e-10)

    def test_frecuencia_heterodina_f0(self):
        """Frecuencia heterodina debe ser f₀."""
        self.assertAlmostEqual(
            self.resultado["frecuencia_heterodina_hz"], 141.7001, places=4
        )

    def test_modos_resonantes_7(self):
        """Deben existir 7 modos resonantes."""
        self.assertEqual(len(self.resultado["modos_resonantes_hz"]), 7)

    def test_linea_critica_riemann(self):
        """Línea crítica de Riemann debe ser True."""
        self.assertTrue(self.resultado["linea_critica_riemann"])

    def test_reduccion_inercia_5pct(self):
        """Reducción de inercia debe ser ≈ 5.3 %."""
        self.assertAlmostEqual(
            self.resultado["reduccion_inercia_pct"], 5.3, places=4
        )

    def test_destello_activo(self):
        """Destello de Masa debe estar activo."""
        self.assertTrue(self.resultado["destello_activo"])

    def test_r_symb_kpps(self):
        """R_symb debe ser ≈ 991.9 kpps."""
        self.assertAlmostEqual(
            self.resultado["r_symb_kpps"], 991.9, delta=5.0
        )

    def test_ganancia_superradiante(self):
        """Ganancia superradiante debe ser N² = 49."""
        self.assertAlmostEqual(self.resultado["ganancia_superradiante"], 49.0, places=5)

    def test_amplitud_oscilacion_pct(self):
        """Amplitud de oscilación de σ debe ser 5.3 %."""
        self.assertAlmostEqual(
            self.resultado["amplitud_oscilacion_pct"], 5.3, places=4
        )

    def test_frecuencia_transparencia(self):
        """Frecuencia de transparencia debe ser f₀."""
        self.assertAlmostEqual(
            self.resultado["frecuencia_transparencia_hz"], 141.7001, places=4
        )

    def test_coherencias_dict(self):
        """coherencias debe ser un diccionario."""
        self.assertIsInstance(self.resultado["coherencias"], dict)

    def test_perturbativo(self):
        """Sistema debe ser perturbativo."""
        self.assertTrue(self.resultado["perturbativo"])

    def test_certificacion_str(self):
        """Certificación debe ser una cadena."""
        self.assertIsInstance(self.resultado["certificacion"], str)

    def test_certificacion_contiene_sello(self):
        """Certificación debe mencionar el sello."""
        self.assertIn("SPC", self.resultado["certificacion"])


# ============================================================================
# Runner
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
