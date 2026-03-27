#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el módulo physics/topc_lagrangiano.py
=================================================

Valida el sistema TOPC Lagrangiano (Tejido de Onda Piloto Coherente):

- ConstantesTopc       → constantes físicas del sistema TOPC
- LagrangianoTopc      → componentes ℒ_tejido, ℒ_EM, ℒ_int
- CampoEscalarPsi      → condensado ψ(t) = ψ₀ cos(2πf₀t)
- EcuacionFoton        → Maxwell modificado por ℒ_int
- BirrefringenciaCircular → índices n_L/R y Δn
- DesfasePolarizacion  → observable Δθ(t)
- CoherenciaTopc       → Ψ_global del sistema
- SistemaTopc          → orquestador principal
- topc_lagrangiano_activar() → API pública

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-03
Framework: QCAL ∞³
"""

import math
import unittest

import numpy as np

from physics.topc_lagrangiano import (
    # Constantes del módulo
    G_NEWTON,
    H_PLANCK,
    EV_A_J,
    M_PLANCK_KG,
    ALFA_EM,
    RHO_DM_GEV_CM3,
    M_PSI_KG,
    M_PSI_EV,
    LAMBDA_SELF,
    G_AGG,
    F_A_EV,
    OMEGA_0,
    FRACCION_DOPPLER_SIDEREO,
    PERIODO_SIDEREO_S,
    L_REF_M,
    AMPLITUD_ESPERADA_RAD,
    SELLO_TOPC,
    RAM_TOPC,
    # Clases
    ConstantesTopc,
    LagrangianoTopc,
    CampoEscalarPsi,
    EcuacionFoton,
    BirrefringenciaCircular,
    DesfasePolarizacion,
    CoherenciaTopc,
    SistemaTopc,
    # API pública
    topc_lagrangiano_activar,
)
from qcal.constants import F0_HZ, C

# Tolerancias
REL_TOL = 1.0e-6
ABS_TOL = 1.0e-30


# ============================================================================
# CLASE 1 — ConstantesTopc
# ============================================================================

class TestConstantesTopc(unittest.TestCase):
    """Tests para ConstantesTopc."""

    def setUp(self):
        self.c = ConstantesTopc()

    def test_f0_coincide_con_qcal(self):
        """f₀ debe coincidir con la constante canónica QCAL."""
        self.assertAlmostEqual(self.c.f0, F0_HZ, places=4)

    def test_f888_es_888(self):
        """f₈₈₈ debe ser 888 Hz."""
        self.assertAlmostEqual(self.c.f888, 888.0, places=6)

    def test_omega0_formula(self):
        """ω₀ = 2π f₀."""
        self.assertAlmostEqual(self.c.omega0, 2.0 * math.pi * F0_HZ, delta=REL_TOL)

    def test_m_psi_ev_orden(self):
        """m_ψ ≈ 5.86×10⁻¹³ eV (dentro del 5 %)."""
        self.assertAlmostEqual(self.c.m_psi_ev / 5.86e-13, 1.0, delta=0.05)

    def test_lambda_self_orden(self):
        """λ ≈ 4.8×10⁻⁴¹ (dentro del 10 %)."""
        self.assertAlmostEqual(self.c.lambda_self / 4.8e-41, 1.0, delta=0.10)

    def test_g_agg_positivo(self):
        """g_aγγ debe ser positivo."""
        self.assertGreater(self.c.g_agg, 0.0)

    def test_psi0_ev_positivo(self):
        """ψ₀ debe ser un número real positivo."""
        self.assertGreater(self.c.psi0_ev, 0.0)

    def test_psi0_escala_con_rho(self):
        """ψ₀ ∝ √(ρ_DM): duplicar ρ da ψ₀ × √2."""
        c1 = ConstantesTopc(rho_dm=0.3)
        c2 = ConstantesTopc(rho_dm=0.6)
        self.assertAlmostEqual(c2.psi0_ev / c1.psi0_ev, math.sqrt(2.0), delta=1.0e-6)

    def test_rho_dm_por_defecto(self):
        """Densidad DM por defecto es 0.3 GeV cm⁻³."""
        self.assertAlmostEqual(self.c.rho_dm, 0.3)

    def test_L_m_por_defecto(self):
        """Longitud de brazo por defecto es 100 km."""
        self.assertAlmostEqual(self.c.L_m, 100.0e3)

    def test_f0_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            ConstantesTopc(f0=-1.0)

    def test_f888_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            ConstantesTopc(f888=0.0)

    def test_rho_dm_cero_lanza_error(self):
        with self.assertRaises(ValueError):
            ConstantesTopc(rho_dm=0.0)

    def test_f_a_ev_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            ConstantesTopc(f_a_ev=-1.0)

    def test_L_m_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            ConstantesTopc(L_m=0.0)

    def test_resumen_contiene_claves(self):
        """resumen() debe devolver un dict con las claves principales."""
        r = self.c.resumen()
        for clave in ["f0_Hz", "f888_Hz", "omega0_rad_s", "m_psi_eV",
                      "lambda_self", "g_agg_GeV-1", "psi0_eV", "sello", "ram"]:
            self.assertIn(clave, r)

    def test_sello_en_resumen(self):
        """El resumen debe incluir el sello ∴TOPC∞³."""
        self.assertEqual(self.c.resumen()["sello"], SELLO_TOPC)


# ============================================================================
# CLASE 2 — LagrangianoTopc
# ============================================================================

class TestLagrangianoTopc(unittest.TestCase):
    """Tests para LagrangianoTopc."""

    def setUp(self):
        self.lag = LagrangianoTopc()

    def test_densidad_gravedad_espacio_plano(self):
        """En espacio plano (R=0), ℒ_gravedad = 0."""
        self.assertAlmostEqual(self.lag.densidad_gravedad(0.0), 0.0)

    def test_densidad_gravedad_positiva_para_R_positivo(self):
        """Para R > 0, ℒ_gravedad > 0."""
        self.assertGreater(self.lag.densidad_gravedad(1.0), 0.0)

    def test_densidad_em_vacio(self):
        """En el vacío (E=B=0), ℒ_EM = 0."""
        self.assertAlmostEqual(self.lag.densidad_em(0.0, 0.0), 0.0)

    def test_densidad_em_signo_E(self):
        """Campo E puro: ℒ_EM > 0 (ya que −¼ F² = ½ε₀ E² > 0)."""
        self.assertGreater(self.lag.densidad_em(E_sq=1.0, B_sq=0.0), 0.0)

    def test_densidad_tejido_cero_en_vacio(self):
        """Con ψ=0 y ∂ψ=0, ℒ_tejido = 0."""
        result = self.lag.densidad_tejido(0.0, 0.0, 0.0)
        self.assertAlmostEqual(result, 0.0, delta=ABS_TOL)

    def test_densidad_tejido_cinetico_positivo(self):
        """Término cinético ½ (∂_t ψ)² ≥ 0."""
        result = self.lag.densidad_tejido(0.0, 0.0, dpsi_dt=1.0)
        # ℒ_tejido = ½ × 1² − ½ × ω₀² × 0 = 0.5 (sin potencial pues ψ=0)
        self.assertAlmostEqual(result, 0.5, delta=1.0e-10)

    def test_densidad_tejido_potencial_negativo(self):
        """Término de masa −½ ω₀² |ψ|² < 0 (ψ ≠ 0, dpsi_dt = 0)."""
        lag = LagrangianoTopc()
        omega0 = lag.constantes.omega0
        psi = 1.0   # eV
        result = lag.densidad_tejido(psi, 0.0, dpsi_dt=0.0)
        esperado = -0.5 * omega0**2 * psi**2
        self.assertAlmostEqual(result, esperado, delta=abs(esperado) * 1.0e-9)

    def test_densidad_interaccion_cero_sin_campo(self):
        """ℒ_int = 0 cuando psi_re = 0."""
        self.assertAlmostEqual(self.lag.densidad_interaccion(0.0, F_dual=1.0), 0.0)

    def test_densidad_interaccion_cero_sin_dual(self):
        """ℒ_int = 0 cuando F_dual = 0."""
        self.assertAlmostEqual(self.lag.densidad_interaccion(1.0, F_dual=0.0), 0.0)

    def test_densidad_total_es_suma(self):
        """ℒ_total = sum de componentes."""
        psi_re = 1.0
        dpsi_dt = 2.0
        R = 0.5
        total = self.lag.densidad_total(psi_re, 0.0, dpsi_dt, R_escalar=R)
        grav = self.lag.densidad_gravedad(R)
        tej = self.lag.densidad_tejido(psi_re, 0.0, dpsi_dt)
        em = self.lag.densidad_em(0.0, 0.0)
        inter = self.lag.densidad_interaccion(psi_re, 0.0)
        self.assertAlmostEqual(total, grav + tej + em + inter, delta=1.0e-20)


# ============================================================================
# CLASE 3 — CampoEscalarPsi
# ============================================================================

class TestCampoEscalarPsi(unittest.TestCase):
    """Tests para CampoEscalarPsi."""

    def setUp(self):
        self.campo = CampoEscalarPsi()

    def test_psi_en_t0(self):
        """ψ(0) = ψ₀."""
        psi0 = self.campo.constantes.psi0_ev
        self.assertAlmostEqual(self.campo.psi(0.0), psi0, delta=psi0 * 1.0e-10)

    def test_psi_en_cuarto_periodo(self):
        """ψ(T/4) ≈ 0 (dentro de la precisión float64 relativa a ψ₀)."""
        T_cuarto = 1.0 / (4.0 * F0_HZ)
        psi0 = self.campo.constantes.psi0_ev
        # ψ(T/4) = ψ₀ cos(π/2) ≈ 0; residuo es ruido numérico ∼ ε_machine × ψ₀
        self.assertAlmostEqual(self.campo.psi(T_cuarto), 0.0, delta=psi0 * 1.0e-15)

    def test_dpsi_dt_en_t0(self):
        """∂_t ψ(0) = 0."""
        self.assertAlmostEqual(self.campo.dpsi_dt(0.0), 0.0, delta=1.0e-10)

    def test_dpsi_dt_en_cuarto_periodo(self):
        """∂_t ψ(T/4) = −ψ₀ ω₀."""
        T_cuarto = 1.0 / (4.0 * F0_HZ)
        psi0 = self.campo.constantes.psi0_ev
        omega0 = self.campo.constantes.omega0
        esperado = -psi0 * omega0
        resultado = self.campo.dpsi_dt(T_cuarto)
        self.assertAlmostEqual(resultado / esperado, 1.0, delta=1.0e-6)

    def test_conservacion_energia(self):
        """½ (∂_t ψ)² + ½ ω₀² ψ² = ½ ψ₀² ω₀² (constante)."""
        psi0 = self.campo.constantes.psi0_ev
        omega0 = self.campo.constantes.omega0
        E_esperado = 0.5 * psi0**2 * omega0**2
        for t in [0.0, 0.1, 0.5, 1.0]:
            E = self.campo.energia_total(t)
            self.assertAlmostEqual(E / E_esperado, 1.0, delta=1.0e-8)

    def test_serie_temporal_forma(self):
        """serie_temporal devuelve array de la misma forma que t_array."""
        t = np.linspace(0, 1, 200)
        resultado = self.campo.serie_temporal(t)
        self.assertEqual(resultado.shape, t.shape)

    def test_serie_temporal_en_t0(self):
        """ψ(0) = ψ₀ en la serie temporal."""
        t = np.array([0.0])
        psi0 = self.campo.constantes.psi0_ev
        np.testing.assert_allclose(self.campo.serie_temporal(t), [psi0], rtol=1.0e-10)

    def test_derivada_serie_temporal_forma(self):
        """derivada_temporal_serie devuelve array de la misma forma."""
        t = np.linspace(0, 1, 100)
        resultado = self.campo.derivada_temporal_serie(t)
        self.assertEqual(resultado.shape, t.shape)


# ============================================================================
# CLASE 4 — EcuacionFoton
# ============================================================================

class TestEcuacionFoton(unittest.TestCase):
    """Tests para EcuacionFoton."""

    def setUp(self):
        self.foton = EcuacionFoton()

    def test_fuente_maxwell_cero_sin_campo(self):
        """fuente_maxwell = 0 cuando dpsi_dt = 0."""
        self.assertAlmostEqual(self.foton.fuente_maxwell(0.0, curl_E=1.0), 0.0)

    def test_fuente_maxwell_cero_sin_rotor(self):
        """fuente_maxwell = 0 cuando curl_E = 0."""
        self.assertAlmostEqual(self.foton.fuente_maxwell(1.0, curl_E=0.0), 0.0)

    def test_fuente_maxwell_signo(self):
        """fuente_maxwell es negativa para dpsi_dt > 0 y curl_E > 0."""
        resultado = self.foton.fuente_maxwell(1.0, curl_E=1.0)
        self.assertLess(resultado, 0.0)

    def test_dispersion_espacio_plano(self):
        """En el vacío ω = ck: desviación ≈ 0."""
        omega = 3.55e15  # láser verde 532 nm
        k = omega / C
        dev = self.foton.verificar_dispersion(omega, k)
        self.assertAlmostEqual(dev, 0.0, delta=1.0e-10)

    def test_dispersion_fuera_de_masa(self):
        """Cuando ω ≠ ck, la desviación es no nula."""
        omega = 3.55e15
        k = omega / C * 1.001   # 0.1 % fuera de masa
        dev = self.foton.verificar_dispersion(omega, k)
        self.assertNotAlmostEqual(dev, 0.0, delta=1.0e-6)


# ============================================================================
# CLASE 5 — BirrefringenciaCircular
# ============================================================================

class TestBirrefringenciaCircular(unittest.TestCase):
    """Tests para BirrefringenciaCircular."""

    def setUp(self):
        self.birr = BirrefringenciaCircular()
        self.omega_laser = 2.0 * math.pi * C / 532.0e-9   # láser verde

    def test_indices_proximos_a_unidad(self):
        """n_L y n_R deben estar cerca de 1."""
        dpsi_max = self.birr.constantes.psi0_ev * self.birr.constantes.omega0
        n_L, n_R = self.birr.indices_refraccion(dpsi_max, self.omega_laser)
        self.assertAlmostEqual(n_L, 1.0, delta=1.0)
        self.assertAlmostEqual(n_R, 1.0, delta=1.0)

    def test_n_L_mayor_n_R_para_dpsi_positivo(self):
        """Para ψ̇ > 0: n_L > n_R (usando dpsi grande para superar precisión float64)."""
        # g_aγγ ≈ 1.84e-28 eV⁻¹; necesitamos dpsi · g / ω > ε_machine
        # Con dpsi = 1e30: delta_n ≈ 2.6e-14  (claramente representable)
        n_L, n_R = self.birr.indices_refraccion(1.0e30, self.omega_laser)
        self.assertGreater(n_L, n_R)

    def test_diferencia_indices_formula(self):
        """Δn ∝ ψ̇: duplicar ψ̇ duplica Δn (verificación de proporcionalidad)."""
        # Se usa dpsi grande para superar la precisión float64
        # La resta (1+δ)-(1-δ) con δ≈2.6e-14 introduce ~0.2% de error numérico
        dpsi = 1.0e30
        dn1 = self.birr.diferencia_indices(dpsi, self.omega_laser)
        dn2 = self.birr.diferencia_indices(2.0 * dpsi, self.omega_laser)
        # Δn debe ser proporcional a ψ̇ (tolerancia holgada por cancelación float64)
        self.assertAlmostEqual(dn2 / dn1, 2.0, delta=0.01)

    def test_diferencia_indices_cero_para_dpsi_cero(self):
        """Δn = 0 cuando ψ̇ = 0."""
        dn = self.birr.diferencia_indices(0.0, self.omega_laser)
        self.assertAlmostEqual(dn, 0.0, delta=ABS_TOL)

    def test_longitud_coherencia_positiva(self):
        """L_coh debe ser positiva."""
        L_coh = self.birr.longitud_coherencia(self.omega_laser)
        self.assertGreater(L_coh, 0.0)


# ============================================================================
# CLASE 6 — DesfasePolarizacion
# ============================================================================

class TestDesfasePolarizacion(unittest.TestCase):
    """Tests para DesfasePolarizacion."""

    def setUp(self):
        self.dp = DesfasePolarizacion()

    def test_amplitud_positiva(self):
        """Δθ_amp debe ser positivo."""
        self.assertGreater(self.dp.amplitud(), 0.0)

    def test_amplitud_orden_magnitud(self):
        """Amplitud ~10⁻¹⁹ rad (dentro de 2 órdenes de magnitud)."""
        A = self.dp.amplitud()
        self.assertGreater(A, 1.0e-21)
        self.assertLess(A, 1.0e-17)

    def test_amplitud_escala_con_L(self):
        """Δθ_amp ∝ L: duplicar L duplica la amplitud."""
        A1 = self.dp.amplitud(L=100.0e3)
        A2 = self.dp.amplitud(L=200.0e3)
        self.assertAlmostEqual(A2 / A1, 2.0, delta=1.0e-9)

    def test_desfase_en_t0_es_cero(self):
        """Δθ(0) = Δθ_amp · sin(0) = 0."""
        self.assertAlmostEqual(self.dp.desfase(0.0), 0.0, delta=ABS_TOL)

    def test_desfase_formula(self):
        """Δθ(t) = Δθ_amp · sin(2π f₀ t)."""
        t = 0.37 / F0_HZ
        A = self.dp.amplitud()
        esperado = A * math.sin(2.0 * math.pi * F0_HZ * t)
        self.assertAlmostEqual(self.dp.desfase(t), esperado, delta=abs(esperado) * 1.0e-9)

    def test_desfase_acotado_por_amplitud(self):
        """|Δθ(t)| ≤ Δθ_amp."""
        A = self.dp.amplitud()
        for t in np.linspace(0, 10.0 / F0_HZ, 100):
            self.assertLessEqual(abs(self.dp.desfase(t)), A * 1.0000001)

    def test_doppler_distinto_sin_doppler(self):
        """Con Doppler, la serie difiere de la sin Doppler."""
        t = np.linspace(0, 1.0 / F0_HZ, 500)
        s_plain = self.dp.serie_temporal(t, incluir_doppler=False)
        s_dopp = self.dp.serie_temporal(t, incluir_doppler=True)
        self.assertGreater(np.max(np.abs(s_plain - s_dopp)), 0.0)

    def test_serie_temporal_forma(self):
        """serie_temporal devuelve array de misma forma."""
        t = np.linspace(0, 1, 300)
        resultado = self.dp.serie_temporal(t)
        self.assertEqual(resultado.shape, t.shape)

    def test_serie_temporal_cero_en_t0(self):
        """Δθ(0) = 0 en la serie."""
        t = np.array([0.0])
        resultado = self.dp.serie_temporal(t)
        self.assertAlmostEqual(resultado[0], 0.0, delta=ABS_TOL)


# ============================================================================
# CLASE 7 — CoherenciaTopc
# ============================================================================

class TestCoherenciaTopc(unittest.TestCase):
    """Tests para CoherenciaTopc."""

    def setUp(self):
        self.coh = CoherenciaTopc()

    def test_harmonico_888_entero(self):
        """El harmónico debe ser un entero positivo."""
        h = self.coh.harmonico_888
        self.assertIsInstance(h, int)
        self.assertGreater(h, 0)

    def test_psi_global_en_rango(self):
        """Ψ_global ∈ [0, 1]."""
        psi = self.coh.psi_global
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_evaluacion_contiene_claves(self):
        """evaluar_coherencia() devuelve dict con claves esperadas."""
        r = self.coh.evaluar_coherencia()
        for clave in ["f0_Hz", "f888_Hz", "harmonico", "psi_global", "coherente", "sello"]:
            self.assertIn(clave, r)

    def test_sello_en_coherencia(self):
        """El sello ∴TOPC∞³ debe estar en la evaluación."""
        r = self.coh.evaluar_coherencia()
        self.assertEqual(r["sello"], SELLO_TOPC)

    def test_coherencia_sello_propiedad(self):
        """coherencia_sello devuelve la cadena del sello."""
        self.assertEqual(self.coh.coherencia_sello, SELLO_TOPC)

    def test_psi_global_igual_para_f0_exacto(self):
        """Si f₀ = f₈₈₈ / n exactamente, Ψ_global = 1."""
        f0_test = 888.0 / 6.0    # 148 Hz → harmónico 6
        c = ConstantesTopc(f0=f0_test, f888=888.0)
        coh = CoherenciaTopc(c)
        self.assertAlmostEqual(coh.psi_global, 1.0, delta=1.0e-10)

    def test_coherente_flag(self):
        """El flag 'coherente' es True cuando Ψ_global ≥ 0.5."""
        r = self.coh.evaluar_coherencia()
        self.assertEqual(r["coherente"], r["psi_global"] >= 0.5)


# ============================================================================
# CLASE 8 — SistemaTopc
# ============================================================================

class TestSistemaTopc(unittest.TestCase):
    """Tests para SistemaTopc."""

    def setUp(self):
        self.sistema = SistemaTopc()

    def test_acceso_subsistemas(self):
        """Los subsistemas deben ser accesibles como propiedades."""
        self.assertIsInstance(self.sistema.lagrangiano, LagrangianoTopc)
        self.assertIsInstance(self.sistema.campo, CampoEscalarPsi)
        self.assertIsInstance(self.sistema.foton, EcuacionFoton)
        self.assertIsInstance(self.sistema.birrefringencia, BirrefringenciaCircular)
        self.assertIsInstance(self.sistema.desfase, DesfasePolarizacion)
        self.assertIsInstance(self.sistema.coherencia, CoherenciaTopc)

    def test_calcular_estado_contiene_claves(self):
        """calcular_estado devuelve dict con claves principales."""
        estado = self.sistema.calcular_estado(0.0)
        for clave in [
            "t_s", "psi_eV", "dpsi_dt_eV_s", "L_tejido", "L_int",
            "n_L", "n_R", "delta_n", "amplitud_delta_theta_rad",
            "delta_theta_rad", "psi_global", "coherente", "sello",
        ]:
            self.assertIn(clave, estado)

    def test_calcular_estado_sello(self):
        """Estado contiene el sello ∴TOPC∞³."""
        estado = self.sistema.calcular_estado(0.0)
        self.assertEqual(estado["sello"], SELLO_TOPC)

    def test_calcular_estado_amplitud_positiva(self):
        """Amplitud de señal positiva."""
        estado = self.sistema.calcular_estado(0.0)
        self.assertGreater(estado["amplitud_delta_theta_rad"], 0.0)

    def test_activar_contiene_claves(self):
        """activar() devuelve dict con claves de resumen."""
        resultado = self.sistema.activar()
        for clave in ["estado", "sello", "ram", "constantes", "coherencia"]:
            self.assertIn(clave, resultado)

    def test_activar_estado_es_activado(self):
        """El estado del sistema debe ser 'ACTIVADO'."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado["estado"], "ACTIVADO")

    def test_activar_amplitud_orden_correcto(self):
        """La amplitud debe estar en el orden de magnitud esperado."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado["amplitud_orden_correcto"])

    def test_activar_ram(self):
        """El RAM del sistema debe coincidir con RAM_TOPC."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado["ram"], RAM_TOPC)


# ============================================================================
# API PÚBLICA — topc_lagrangiano_activar
# ============================================================================

class TestTopcLagrangianoActivar(unittest.TestCase):
    """Tests para la función de API pública topc_lagrangiano_activar()."""

    def test_devuelve_dict(self):
        """topc_lagrangiano_activar() debe devolver un dict."""
        resultado = topc_lagrangiano_activar()
        self.assertIsInstance(resultado, dict)

    def test_estado_activado(self):
        """El estado debe ser 'ACTIVADO'."""
        resultado = topc_lagrangiano_activar()
        self.assertEqual(resultado["estado"], "ACTIVADO")

    def test_sello_correcto(self):
        """El sello debe ser ∴TOPC∞³."""
        resultado = topc_lagrangiano_activar()
        self.assertEqual(resultado["sello"], SELLO_TOPC)

    def test_f0_por_defecto(self):
        """f₀ por defecto = F0_HZ."""
        resultado = topc_lagrangiano_activar()
        self.assertAlmostEqual(resultado["f0_Hz"], F0_HZ, places=4)

    def test_f0_personalizado(self):
        """f₀ personalizado se aplica correctamente."""
        resultado = topc_lagrangiano_activar(f0=200.0)
        self.assertAlmostEqual(resultado["f0_Hz"], 200.0, places=6)

    def test_rho_dm_personalizado(self):
        """rho_dm personalizado se refleja en las constantes."""
        resultado = topc_lagrangiano_activar(rho_dm=0.6)
        self.assertAlmostEqual(resultado["constantes"]["rho_dm_GeV_cm3"], 0.6)

    def test_L_m_personalizado(self):
        """L_m personalizado se refleja en el resultado."""
        resultado = topc_lagrangiano_activar(L_m=50.0e3)
        self.assertAlmostEqual(resultado["L_m"], 50.0e3)

    def test_amplitud_escala_con_L(self):
        """Amplitud ∝ L: duplicar L duplica la amplitud."""
        r1 = topc_lagrangiano_activar(L_m=100.0e3)
        r2 = topc_lagrangiano_activar(L_m=200.0e3)
        A1 = r1["amplitud_delta_theta_rad"]
        A2 = r2["amplitud_delta_theta_rad"]
        self.assertAlmostEqual(A2 / A1, 2.0, delta=1.0e-9)


# ============================================================================
# CONSISTENCIA FÍSICA
# ============================================================================

class TestConsistenciaFisica(unittest.TestCase):
    """Verificaciones de auto-consistencia física."""

    def test_masa_planck_orden(self):
        """M_P ≈ 2.176×10⁻⁸ kg (dentro del 1 %)."""
        self.assertAlmostEqual(M_PLANCK_KG / 2.176e-8, 1.0, delta=0.01)

    def test_m_psi_formula(self):
        """m_ψ = h f₀ / c² debe verificarse."""
        esperado = H_PLANCK * F0_HZ / C**2
        self.assertAlmostEqual(M_PSI_KG / esperado, 1.0, delta=REL_TOL)

    def test_alfa_em_valor(self):
        """α ≈ 1/137."""
        self.assertAlmostEqual(ALFA_EM * 137.0, 1.0, delta=1.0e-3)

    def test_omega0_formula(self):
        """ω₀ = 2π f₀."""
        self.assertAlmostEqual(OMEGA_0, 2.0 * math.pi * F0_HZ, delta=REL_TOL)

    def test_fraccion_doppler_sidereo(self):
        """Fracción Doppler sidéreo = 10⁻³."""
        self.assertAlmostEqual(FRACCION_DOPPLER_SIDEREO, 1.0e-3)

    def test_lambda_self_muy_pequeno(self):
        """λ ≪ 1 (régimen de acoplamiento débil)."""
        self.assertLess(LAMBDA_SELF, 1.0e-30)

    def test_m_psi_mucho_menor_m_planck(self):
        """m_ψ ≪ M_P."""
        self.assertLess(M_PSI_KG / M_PLANCK_KG, 1.0e-30)

    def test_formula_amplitud_desfase(self):
        """Δθ_amp = ½ g_aγγ [eV⁻¹] × ψ₀ [eV] × ω₀ × L / c."""
        c = ConstantesTopc()
        dp = DesfasePolarizacion(c)
        g_inv_eV = c.g_agg * 1.0e-9
        esperado = 0.5 * g_inv_eV * c.psi0_ev * c.omega0 * c.L_m / C
        self.assertAlmostEqual(dp.amplitud() / esperado, 1.0, delta=1.0e-9)

    def test_sello_topc(self):
        """El sello TOPC debe ser ∴TOPC∞³."""
        self.assertEqual(SELLO_TOPC, "∴TOPC∞³")

    def test_ram_topc(self):
        """El RAM debe comenzar con RAM-XLII."""
        self.assertTrue(RAM_TOPC.startswith("RAM-XLII"))

    def test_amplitud_esperada_orden(self):
        """AMPLITUD_ESPERADA_RAD ≈ 10⁻¹⁹ rad."""
        self.assertAlmostEqual(AMPLITUD_ESPERADA_RAD, 1.0e-19)


# ============================================================================
# Runner
# ============================================================================

def ejecutar_tests() -> bool:
    """Ejecuta todos los tests del módulo TOPC Lagrangiano."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for cls in [
        TestConstantesTopc,
        TestLagrangianoTopc,
        TestCampoEscalarPsi,
        TestEcuacionFoton,
        TestBirrefringenciaCircular,
        TestDesfasePolarizacion,
        TestCoherenciaTopc,
        TestSistemaTopc,
        TestTopcLagrangianoActivar,
        TestConsistenciaFisica,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    exito = ejecutar_tests()
    raise SystemExit(0 if exito else 1)
