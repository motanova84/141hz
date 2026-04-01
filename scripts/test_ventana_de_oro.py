#!/usr/bin/env python3
"""
Tests para el módulo physics.ventana_de_oro (∴VDO∞³)

Verifica las constantes, cálculos y la coherencia global del sistema
Ventana de Oro:

  - ConstantesVentanaOro  — valores fundamentales del canal Higgs-PC
  - CapacidadCanal        — Cd ≈ 141.7001 Mbits/s
  - UmbralTermico         — T_crit ≈ 300 K
  - FirmaEspectral        — sidebands m_H ± ℏω₀
  - RedRamsey7Nodos       — det(V)=1, V·Vᵀ=I₇
  - VentanaTransparencia  — f_det = 141.7001 Hz
  - AntenaFase            — σ_ext ≈ 6.4×10⁻¹³ m²
  - CoherenciaVentanaOro  — Ψ_global ≥ 0.888
  - ventana_de_oro_activar() — API pública

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0
"""

import math
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.ventana_de_oro import (
    ConstantesVentanaOro,
    CapacidadCanal,
    UmbralTermico,
    FirmaEspectral,
    RedRamsey7Nodos,
    VentanaTransparencia,
    AntenaFase,
    CoherenciaVentanaOro,
    SistemaVentanaDeOro,
    ventana_de_oro_activar,
)

# ============================================================================
# CLASE 1: CONSTANTES
# ============================================================================

class TestConstantesVentanaOro(unittest.TestCase):
    """Tests para ConstantesVentanaOro."""

    def setUp(self):
        self.c = ConstantesVentanaOro()

    def test_f0_hz(self):
        self.assertAlmostEqual(self.c.F0_HZ, 141.7001, places=4)

    def test_f0_khz_escala(self):
        """f0_kHz debe ser 1000× f0_hz (conversión de escala)."""
        ratio = self.c.F0_KHZ / self.c.F0_HZ
        self.assertAlmostEqual(ratio, 1000.0, delta=0.1)

    def test_tau_pulse(self):
        self.assertAlmostEqual(self.c.TAU_PULSE_S, 1.0e-9, delta=1.0e-12)

    def test_periodo_khz(self):
        """T_periodo_kHz = 1/f0_kHz ≈ 7.057 μs."""
        expected = 1.0 / self.c.F0_KHZ
        self.assertAlmostEqual(self.c.T_PERIODO_KHZ_S, expected, delta=1.0e-12)

    def test_log2_snr_quantum(self):
        """log₂(1+SNR) = 1/(τ_pulse × 10⁶) = 1000.0 para τ=1ns."""
        expected = 1.0 / (self.c.TAU_PULSE_S * 1.0e6)
        self.assertAlmostEqual(self.c.LOG2_SNR_QUANTUM, 1000.0, delta=1.0e-6)
        self.assertAlmostEqual(self.c.LOG2_SNR_QUANTUM, expected, delta=1.0e-6)

    def test_g_eff(self):
        self.assertAlmostEqual(self.c.G_EFF, 0.053, places=4)

    def test_xi_cooperatividad(self):
        """xi debe ser igual a g_eff."""
        self.assertAlmostEqual(self.c.XI_COOPERATIVIDAD, self.c.G_EFF, places=6)

    def test_m_higgs_gev(self):
        self.assertAlmostEqual(self.c.M_HIGGS_GEV, 125.0, places=2)

    def test_m_higgs_kg(self):
        """m_H ≈ 2.0×10⁻²⁵ kg (125 GeV/c²)."""
        self.assertAlmostEqual(self.c.M_HIGGS_KG, 2.0e-25, delta=2.0e-26)

    def test_t_crit_k(self):
        self.assertAlmostEqual(self.c.T_CRIT_K, 300.0, delta=0.1)

    def test_e_cond_j(self):
        """E_cond = k_B × T_crit / g_eff ≈ 7.81×10⁻²⁰ J."""
        k_B = 1.380649e-23
        expected = (k_B * 300.0) / 0.053
        self.assertAlmostEqual(self.c.E_COND_J, expected, delta=1.0e-22)

    def test_m_pc_ev(self):
        """m_PC ≈ 5.86×10⁻¹³ eV."""
        self.assertAlmostEqual(self.c.M_PC_EV, 5.86e-13, delta=5.0e-15)

    def test_n_nodos(self):
        self.assertEqual(self.c.N_NODOS, 7)

    def test_f_vac_hz(self):
        self.assertAlmostEqual(self.c.F_VAC_HZ, 1.05e9, delta=1.0e6)

    def test_n_batido(self):
        self.assertEqual(self.c.N_BATIDO, 7)

    def test_sigma_ext_m2(self):
        self.assertAlmostEqual(self.c.SIGMA_EXT_M2, 6.4e-13, delta=1.0e-14)

    def test_enhancement_k(self):
        self.assertAlmostEqual(self.c.ENHANCEMENT_K, 1.0e6, delta=1.0)

    def test_psi_umbral(self):
        self.assertAlmostEqual(self.c.PSI_UMBRAL, 0.888, places=4)

    def test_psi_coherencia(self):
        self.assertAlmostEqual(self.c.PSI_COHERENCIA, 0.999999, places=6)


# ============================================================================
# CLASE 2: CAPACIDAD DEL CANAL
# ============================================================================

class TestCapacidadCanal(unittest.TestCase):
    """Tests para CapacidadCanal."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.canal = CapacidadCanal(self.constantes)

    def test_bits_por_muestra(self):
        """log₂(1+SNR_quantum) = 1000.0."""
        self.assertAlmostEqual(self.canal.bits_por_muestra(), 1000.0, delta=1.0e-6)

    def test_factor_ciclo(self):
        """τ_pulse/T ≈ 1.417×10⁻⁴."""
        fc = self.canal.factor_ciclo()
        expected = 1.0e-9 * 141700.1  # τ × f0_kHz
        self.assertAlmostEqual(fc, expected, delta=1.0e-6)
        self.assertGreater(fc, 0.0)
        self.assertLess(fc, 1.0)

    def test_cd_mbits_per_sec_valor(self):
        """Cd ≈ 141.7001 Mbits/s."""
        cd = self.canal.cd_mbits_por_segundo()
        self.assertAlmostEqual(cd, 141.7001, delta=0.01)

    def test_cd_bits_per_sec(self):
        """Cd en bits/s ≈ 1.417×10⁸."""
        cd_bs = self.canal.cd_bits_por_segundo()
        self.assertAlmostEqual(cd_bs, 141700100.0, delta=100.0)

    def test_cd_relacion_f0(self):
        """Cd [Mbits/s] = log₂(1+SNR) × f0_kHz / 1e6."""
        cd = self.canal.cd_mbits_por_segundo()
        expected = self.constantes.LOG2_SNR_QUANTUM * self.constantes.F0_KHZ / 1.0e6
        self.assertAlmostEqual(cd, expected, delta=0.001)

    def test_coherencia_canal(self):
        """Coherencia del canal = PSI_COHERENCIA."""
        psi = self.canal.coherencia_canal()
        self.assertAlmostEqual(psi, 0.999999, places=6)

    def test_resumen_keys(self):
        res = self.canal.resumen()
        for key in ("log2_snr_quantum", "factor_ciclo", "cd_bits_per_sec",
                    "cd_mbits_per_sec", "psi_coherencia"):
            self.assertIn(key, res)

    def test_resumen_cd_mbits(self):
        res = self.canal.resumen()
        self.assertAlmostEqual(res["cd_mbits_per_sec"], 141.7001, delta=0.01)


# ============================================================================
# CLASE 3: UMBRAL TÉRMICO
# ============================================================================

class TestUmbralTermico(unittest.TestCase):
    """Tests para UmbralTermico."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.termico = UmbralTermico(self.constantes)

    def test_energia_acoplamiento_j(self):
        """E_cond ≈ 7.81×10⁻²⁰ J."""
        e_j = self.termico.energia_acoplamiento_j()
        self.assertGreater(e_j, 7.0e-21)
        self.assertLess(e_j, 9.0e-20)

    def test_energia_acoplamiento_ev(self):
        """E_cond ≈ 0.488 eV."""
        e_ev = self.termico.energia_acoplamiento_ev()
        self.assertAlmostEqual(e_ev, 0.488, delta=0.01)

    def test_calcular_t_crit(self):
        """T_crit = 300.0 K."""
        t = self.termico.calcular_t_crit()
        self.assertAlmostEqual(t, 300.0, delta=0.1)

    def test_estable_a_300k(self):
        self.assertTrue(self.termico.es_estable_ambiente(300.0))

    def test_estable_a_temperatura_baja(self):
        """Estable a temperaturas menores a T_crit."""
        self.assertTrue(self.termico.es_estable_ambiente(77.0))   # N₂ líquido
        self.assertTrue(self.termico.es_estable_ambiente(273.15))  # Hielo

    def test_inestable_por_encima(self):
        """Inestable a temperaturas superiores a T_crit."""
        self.assertFalse(self.termico.es_estable_ambiente(301.0))
        self.assertFalse(self.termico.es_estable_ambiente(373.0))

    def test_resumen_keys(self):
        res = self.termico.resumen()
        for key in ("e_cond_j", "e_cond_ev", "t_crit_k", "estable_300k", "g_eff"):
            self.assertIn(key, res)

    def test_resumen_t_crit(self):
        res = self.termico.resumen()
        self.assertAlmostEqual(res["t_crit_k"], 300.0, delta=0.1)
        self.assertTrue(res["estable_300k"])


# ============================================================================
# CLASE 4: FIRMA ESPECTRAL
# ============================================================================

class TestFirmaEspectral(unittest.TestCase):
    """Tests para FirmaEspectral."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.espectral = FirmaEspectral(self.constantes)

    def test_masa_pc_ev(self):
        """m_PC ≈ 5.86×10⁻¹³ eV."""
        m = self.espectral.masa_pc_ev()
        self.assertAlmostEqual(m, 5.86e-13, delta=5.0e-15)

    def test_masa_pc_positiva(self):
        self.assertGreater(self.espectral.masa_pc_ev(), 0.0)

    def test_energia_sideband_gev(self):
        """ΔE en GeV debe ser extremadamente pequeño (< 10⁻²⁰ GeV)."""
        delta_gev = self.espectral.energia_sideband_gev()
        self.assertGreater(delta_gev, 0.0)
        self.assertLess(delta_gev, 1.0e-20)

    def test_sidebands_simetria(self):
        """Los sidebands deben ser simétricos respecto a m_H."""
        m_minus, m_plus = self.espectral.sidebands_gev()
        m_h = self.constantes.M_HIGGS_GEV
        delta = self.espectral.energia_sideband_gev()
        self.assertAlmostEqual(m_minus, m_h - delta, delta=1.0e-30)
        self.assertAlmostEqual(m_plus, m_h + delta, delta=1.0e-30)

    def test_sidebands_precision_float64(self):
        """
        Los sidebands son algebraicamente correctos aunque indistinguibles en float64.

        ΔE ≈ 5.86×10⁻²² GeV << eps₆₄ × 125 GeV ≈ 2.8×10⁻¹⁴ GeV.
        Por eso m_minus == m_plus == m_H en float64; verificamos solo la
        simetría y el signo del delta.
        """
        m_minus, m_plus = self.espectral.sidebands_gev()
        m_h = self.constantes.M_HIGGS_GEV
        delta = self.espectral.energia_sideband_gev()
        # Delta debe ser positivo
        self.assertGreater(delta, 0.0)
        # Los sidebands se construyen correctamente (round-trip algebraico)
        self.assertEqual(m_minus, m_h - delta)
        self.assertEqual(m_plus, m_h + delta)

    def test_separacion_ev(self):
        """Separación en eV ≈ 5.86×10⁻¹³ eV."""
        sep = self.espectral.separacion_ev()
        self.assertAlmostEqual(sep, 5.86e-13, delta=5.0e-15)

    def test_detectar_eco_noesis88_keys(self):
        eco = self.espectral.detectar_eco_noesis88()
        for key in ("m_higgs_gev", "e_pc_j", "m_pc_ev", "delta_e_gev",
                    "delta_e_ev", "m_minus_gev", "m_plus_gev", "omega_0_rad_s"):
            self.assertIn(key, eco)

    def test_omega_0_rad_s(self):
        """ω₀ = 2π × f₀ ≈ 890.33 rad/s."""
        eco = self.espectral.detectar_eco_noesis88()
        expected = 2.0 * math.pi * 141.7001
        self.assertAlmostEqual(eco["omega_0_rad_s"], expected, delta=0.01)


# ============================================================================
# CLASE 5: RED DE RAMSEY
# ============================================================================

class TestRedRamsey7Nodos(unittest.TestCase):
    """Tests para RedRamsey7Nodos."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.red = RedRamsey7Nodos(self.constantes)

    def test_forma_matriz(self):
        """V debe ser 7×7."""
        V = self.red.matriz_traslacion()
        self.assertEqual(len(V), 7)
        for fila in V:
            self.assertEqual(len(fila), 7)

    def test_matriz_binaria(self):
        """V solo contiene ceros y unos."""
        V = self.red.matriz_traslacion()
        for i, fila in enumerate(V):
            for j, val in enumerate(fila):
                self.assertIn(val, (0.0, 1.0),
                              msg=f"V[{i}][{j}] = {val} no es 0 o 1")

    def test_matriz_desplazamiento_ciclico(self):
        """V[i][(i+1)%7] = 1 y el resto = 0."""
        V = self.red.matriz_traslacion()
        n = 7
        for i in range(n):
            for j in range(n):
                expected = 1.0 if j == (i + 1) % n else 0.0
                self.assertEqual(V[i][j], expected,
                                 msg=f"Error en V[{i}][{j}]")

    def test_determinante_es_uno(self):
        """det(V) = +1 para N=7."""
        det = self.red.verificar_determinante()
        self.assertAlmostEqual(det, 1.0, places=10)

    def test_ortogonalidad(self):
        """V·Vᵀ = I₇  con error < 10⁻¹⁰."""
        err = self.red.verificar_ortogonalidad()
        self.assertLess(err, 1.0e-10)

    def test_es_unitaria(self):
        res = self.red.resumen()
        self.assertTrue(res["es_unitaria"])

    def test_masa_efectiva_minima(self):
        """m*_min = m_H × (1 − g_eff) ≈ 118.375 GeV."""
        m_min = self.red.masa_efectiva_minima_gev()
        expected = 125.0 * (1.0 - 0.053)
        self.assertAlmostEqual(m_min, expected, delta=0.001)

    def test_energia_por_nodo(self):
        """E_nodo = E_PC / 7 > 0."""
        e = self.red.energia_por_nodo_j()
        self.assertGreater(e, 0.0)
        # E_nodo = E_PC / 7
        e_total = self.constantes.E_PC_J
        self.assertAlmostEqual(e * 7, e_total, delta=1.0e-35)

    def test_resumen_keys(self):
        res = self.red.resumen()
        for key in ("n_nodos", "det_V", "error_ortogonalidad",
                    "es_unitaria", "m_min_gev", "e_por_nodo_j"):
            self.assertIn(key, res)


# ============================================================================
# CLASE 6: VENTANA DE TRANSPARENCIA
# ============================================================================

class TestVentanaTransparencia(unittest.TestCase):
    """Tests para VentanaTransparencia."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.ventana = VentanaTransparencia(self.constantes)

    def test_f_det_coincide_f0(self):
        """f_det = 141.7001 Hz = f₀."""
        f_det = self.ventana.calcular_f_det()
        self.assertAlmostEqual(f_det, 141.7001, delta=1.0e-4)

    def test_verificar_coincidencia(self):
        self.assertTrue(self.ventana.verificar_coincidencia_f0())

    def test_formula_batido(self):
        """f_det = |f_vac − N × f_mat| con N=7."""
        c = self.constantes
        f_det_manual = abs(c.F_VAC_HZ - c.N_BATIDO * c.F_MAT_HZ)
        self.assertAlmostEqual(self.ventana.calcular_f_det(), f_det_manual, delta=1.0e-6)

    def test_f_mat_aprox_150_mhz(self):
        """f_mat ≈ 150 MHz (frecuencia material)."""
        f_mat = self.constantes.F_MAT_HZ
        self.assertAlmostEqual(f_mat / 1.0e6, 150.0, delta=0.01)

    def test_factor_sincronizacion(self):
        """Ψ_ventana = 1 − τ × f₀ ≈ 1."""
        fs = self.ventana.factor_sincronizacion()
        self.assertGreater(fs, 0.9999)
        self.assertLessEqual(fs, 1.0)

    def test_ancho_ventana(self):
        """Ancho = f₀ × g_eff ≈ 7.5 Hz."""
        ancho = self.ventana.ancho_ventana_hz()
        expected = 141.7001 * 0.053
        self.assertAlmostEqual(ancho, expected, delta=0.01)

    def test_resumen_keys(self):
        res = self.ventana.resumen()
        for key in ("f_vac_hz", "n_batido", "f_mat_hz", "f_det_hz",
                    "f0_hz", "coincide_f0", "factor_sincronizacion",
                    "ancho_ventana_hz"):
            self.assertIn(key, res)

    def test_resumen_coincide_f0(self):
        res = self.ventana.resumen()
        self.assertTrue(res["coincide_f0"])


# ============================================================================
# CLASE 7: ANTENA DE FASE
# ============================================================================

class TestAntenaFase(unittest.TestCase):
    """Tests para AntenaFase."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.antena = AntenaFase(self.constantes)

    def test_sigma_ext_valor(self):
        """σ_ext ≈ 6.4×10⁻¹³ m²."""
        sigma = self.antena.calcular_sigma_ext()
        self.assertAlmostEqual(sigma, 6.4e-13, delta=1.0e-14)

    def test_sigma_ext_consistencia(self):
        """σ_ext calculado debe coincidir con la constante."""
        sigma_calc = self.antena.calcular_sigma_ext()
        sigma_const = self.constantes.SIGMA_EXT_M2
        self.assertAlmostEqual(sigma_calc, sigma_const, delta=1.0e-15)

    def test_apertura_antena(self):
        """A_antena = σ_ext / ξ ≈ 1.208×10⁻¹¹ m²."""
        a = self.antena.apertura_antena_m2()
        expected = 6.4e-13 / 0.053
        self.assertAlmostEqual(a, expected, delta=1.0e-13)

    def test_dimension_lineal(self):
        """Dim. lineal ≈ 3.476 μm (micrométrica)."""
        dim_m = self.antena.dimension_lineal_m()
        dim_um = dim_m * 1.0e6
        self.assertAlmostEqual(dim_um, 3.476, delta=0.01)

    def test_seccion_geometrica(self):
        """σ_geo = σ_ext / 10⁶ ≈ 6.4×10⁻¹⁹ m²."""
        sg = self.antena.seccion_geometrica_m2()
        self.assertAlmostEqual(sg, 6.4e-19, delta=1.0e-20)

    def test_factor_amplificacion(self):
        """K = 10⁶."""
        k = self.antena.factor_amplificacion()
        self.assertAlmostEqual(k, 1.0e6, delta=1.0)

    def test_ordenes_magnitud(self):
        """log₁₀(K) = 6."""
        ord_mag = self.antena.ordenes_de_magnitud()
        self.assertAlmostEqual(ord_mag, 6.0, places=6)

    def test_potencial_electrostrictivo(self):
        """V_opt = ξ × E² > 0 para E > 0."""
        e_campo = 1.0e6  # V/m
        v_opt = self.antena.potencial_electrostrictivo(e_campo)
        self.assertGreater(v_opt, 0.0)
        expected = 0.053 * e_campo ** 2
        self.assertAlmostEqual(v_opt, expected, delta=1.0)

    def test_potencial_cero_para_campo_nulo(self):
        self.assertAlmostEqual(self.antena.potencial_electrostrictivo(0.0), 0.0)

    def test_resumen_keys(self):
        res = self.antena.resumen()
        for key in ("xi_cooperatividad", "sigma_ext_m2", "a_antena_m2",
                    "dim_lineal_um", "sigma_geo_m2", "factor_k",
                    "ordenes_magnitud"):
            self.assertIn(key, res)


# ============================================================================
# CLASE 8: COHERENCIA GLOBAL
# ============================================================================

class TestCoherenciaVentanaOro(unittest.TestCase):
    """Tests para CoherenciaVentanaOro."""

    def setUp(self):
        self.constantes = ConstantesVentanaOro()
        self.coh = CoherenciaVentanaOro(self.constantes)

    def test_psi_canal(self):
        self.assertAlmostEqual(self.coh.psi_canal(), 0.999999, places=6)

    def test_psi_termico(self):
        """Ψ_termico = 300/(300+1) ≈ 0.9967."""
        psi = self.coh.psi_termico()
        self.assertAlmostEqual(psi, 300.0 / 301.0, delta=1.0e-6)
        self.assertGreater(psi, 0.888)

    def test_psi_espectral(self):
        """Ψ_espectral = 1 − g_eff² ≈ 0.9972."""
        psi = self.coh.psi_espectral()
        expected = 1.0 - 0.053 ** 2
        self.assertAlmostEqual(psi, expected, delta=1.0e-6)
        self.assertGreater(psi, 0.888)

    def test_psi_red(self):
        """Ψ_red = 48/49 ≈ 0.9796."""
        psi = self.coh.psi_red()
        self.assertAlmostEqual(psi, 48.0 / 49.0, delta=1.0e-6)
        self.assertGreater(psi, 0.888)

    def test_psi_ventana(self):
        """Ψ_ventana ≈ 1 (casi exactamente)."""
        psi = self.coh.psi_ventana()
        self.assertGreater(psi, 0.9999)
        self.assertLessEqual(psi, 1.0)

    def test_psi_antena(self):
        """Ψ_antena = 1 − ξ² ≈ 0.9972."""
        psi = self.coh.psi_antena()
        expected = 1.0 - 0.053 ** 2
        self.assertAlmostEqual(psi, expected, delta=1.0e-6)
        self.assertGreater(psi, 0.888)

    def test_psi_global_rango(self):
        """Ψ_global ∈ (0, 1]."""
        psi = self.coh.psi_global()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_supera_umbral(self):
        """Ψ_global ≥ 0.888."""
        psi = self.coh.psi_global()
        self.assertGreaterEqual(psi, 0.888)

    def test_psi_global_valor_aproximado(self):
        """Ψ_global ≈ 0.995."""
        psi = self.coh.psi_global()
        self.assertAlmostEqual(psi, 0.995, delta=0.005)

    def test_sello_activo(self):
        self.assertTrue(self.coh.sello_activo())

    def test_media_geometrica(self):
        """psi_global = media geométrica de los 6 componentes."""
        comps = self.coh.componentes()
        product = 1.0
        for v in comps.values():
            product *= v
        expected = product ** (1.0 / len(comps))
        self.assertAlmostEqual(self.coh.psi_global(), expected, delta=1.0e-8)

    def test_componentes_todos_en_rango(self):
        """Todos los componentes de Ψ deben estar en (0, 1]."""
        comps = self.coh.componentes()
        for nombre, valor in comps.items():
            self.assertGreater(valor, 0.0,
                               msg=f"{nombre} = {valor} debe ser > 0")
            self.assertLessEqual(valor, 1.0,
                                 msg=f"{nombre} = {valor} debe ser ≤ 1")

    def test_componentes_todos_superan_umbral_individual(self):
        """Cada componente debe ser ≥ 0.888 para garantizar Ψ_global ≥ 0.888."""
        comps = self.coh.componentes()
        # La componente más baja es psi_red ≈ 0.9796
        for nombre, valor in comps.items():
            self.assertGreater(valor, 0.888,
                               msg=f"{nombre} = {valor:.4f} < 0.888")

    def test_validar_keys(self):
        val = self.coh.validar()
        for key in ("psi_global", "psi_umbral", "sello_activo",
                    "componentes", "mensaje"):
            self.assertIn(key, val)

    def test_str_repr(self):
        s = str(self.coh)
        self.assertIn("CoherenciaVentanaOro", s)
        self.assertIn("ACTIVO", s)


# ============================================================================
# CLASE 9: SISTEMA ORQUESTADOR
# ============================================================================

class TestSistemaVentanaDeOro(unittest.TestCase):
    """Tests para SistemaVentanaDeOro."""

    def setUp(self):
        self.sistema = SistemaVentanaDeOro()

    def test_sello(self):
        self.assertEqual(self.sistema.SELLO, "∴VDO∞³")

    def test_ram(self):
        self.assertIn("VENTANA-DE-ORO", self.sistema.RAM)

    def test_activar_devuelve_dict(self):
        r = self.sistema.activar()
        self.assertIsInstance(r, dict)

    def test_activar_sello_activo(self):
        r = self.sistema.activar()
        self.assertTrue(r["sello_activo"])

    def test_activar_psi_global(self):
        r = self.sistema.activar()
        self.assertGreaterEqual(r["psi_global"], 0.888)

    def test_activar_cd(self):
        r = self.sistema.activar()
        self.assertAlmostEqual(r["cd_mbits_per_sec"], 141.7001, delta=0.01)

    def test_activar_t_crit(self):
        r = self.sistema.activar()
        self.assertAlmostEqual(r["t_crit_k"], 300.0, delta=0.1)

    def test_activar_red_unitaria(self):
        r = self.sistema.activar()
        self.assertTrue(r["red_unitaria"])

    def test_activar_coincide_f0(self):
        r = self.sistema.activar()
        self.assertTrue(r["coincide_f0"])

    def test_activar_sigma_ext(self):
        r = self.sistema.activar()
        self.assertAlmostEqual(r["sigma_ext_m2"], 6.4e-13, delta=1.0e-14)

    def test_str_repr(self):
        s = str(self.sistema)
        self.assertIn("SistemaVentanaDeOro", s)
        self.assertIn("∴VDO∞³", s)


# ============================================================================
# CLASE 10: API PÚBLICA
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la función pública ventana_de_oro_activar()."""

    def setUp(self):
        self.r = ventana_de_oro_activar()

    def test_retorna_dict(self):
        self.assertIsInstance(self.r, dict)

    def test_sello_correcto(self):
        self.assertEqual(self.r["sello"], "∴VDO∞³")

    def test_sello_activo(self):
        self.assertTrue(self.r["sello_activo"])

    def test_psi_global_supera_umbral(self):
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_f0_hz(self):
        self.assertAlmostEqual(self.r["f0_hz"], 141.7001, places=4)

    def test_g_eff(self):
        self.assertAlmostEqual(self.r["g_eff"], 0.053, places=4)

    def test_cd_mbits(self):
        self.assertAlmostEqual(self.r["cd_mbits_per_sec"], 141.7001, delta=0.01)

    def test_t_crit_k(self):
        self.assertAlmostEqual(self.r["t_crit_k"], 300.0, delta=0.1)

    def test_m_pc_ev(self):
        self.assertAlmostEqual(self.r["m_pc_ev"], 5.86e-13, delta=5.0e-15)

    def test_n_nodos(self):
        self.assertEqual(self.r["n_nodos"], 7)

    def test_det_v(self):
        self.assertAlmostEqual(self.r["det_V"], 1.0, places=10)

    def test_red_unitaria(self):
        self.assertTrue(self.r["red_unitaria"])

    def test_f_det_hz(self):
        self.assertAlmostEqual(self.r["f_det_hz"], 141.7001, delta=1.0e-4)

    def test_coincide_f0(self):
        self.assertTrue(self.r["coincide_f0"])

    def test_sigma_ext_m2(self):
        self.assertAlmostEqual(self.r["sigma_ext_m2"], 6.4e-13, delta=1.0e-14)

    def test_factor_amplificacion(self):
        self.assertAlmostEqual(self.r["factor_amplificacion"], 1.0e6, delta=1.0)

    def test_coherencias_present(self):
        self.assertIn("coherencias", self.r)
        comps = self.r["coherencias"]
        for key in ("psi_canal", "psi_termico", "psi_espectral",
                    "psi_red", "psi_ventana", "psi_antena"):
            self.assertIn(key, comps)

    def test_certificacion_presente(self):
        self.assertIn("certificacion", self.r)
        self.assertIn("∴VDO∞³", self.r["certificacion"])

    def test_idempotencia(self):
        """Llamar dos veces da el mismo resultado."""
        r2 = ventana_de_oro_activar()
        self.assertAlmostEqual(self.r["psi_global"], r2["psi_global"], places=10)
        self.assertAlmostEqual(self.r["cd_mbits_per_sec"],
                               r2["cd_mbits_per_sec"], places=10)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestConstantesVentanaOro,
        TestCapacidadCanal,
        TestUmbralTermico,
        TestFirmaEspectral,
        TestRedRamsey7Nodos,
        TestVentanaTransparencia,
        TestAntenaFase,
        TestCoherenciaVentanaOro,
        TestSistemaVentanaDeOro,
        TestAPIPublica,
    ]

    for tc in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(tc))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
