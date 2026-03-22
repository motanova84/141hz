#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para core.ecuacion_resurreccion — Ecuación de Resurrección
=================================================================

123 pruebas en 10 clases que abarcan constantes, casos límite y flujos
de integración completos.

Clases de prueba
----------------
  TestConstantes            (12 tests) – constantes y valores fundamentales
  TestSepulcroVacio         (14 tests) – I_d = exp(−eff·F₀), límite eff→0
  TestCuerpoGlorioso        (15 tests) – onda e^{iωt+φ}, Phase-Lock, agua EZ
  TestPermisoEspectral      (12 tests) – ζ'(1/2), eje crítico, ceros de Riemann
  TestIntegralDeContorno    (12 tests) – ∮_Ψ numérica, compatibilidad NumPy 2.0
  TestEstadoResurreccion    ( 8 tests) – dataclass EstadoResurreccion
  TestEcuacionResurreccion  (16 tests) – motor integrado, Ψ_ℜ → 1.0
  TestLaserNoetico          (14 tests) – Nodo 5: biología, electricidad, tiempo
  TestAPIPublica            (10 tests) – calcular_resurreccion(), verificar_resurreccion(),
                                         activar_laser_noetico()
  TestIntegracion           (10 tests) – flujos end-to-end
"""

import math
import cmath
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ecuacion_resurreccion import (
    # Constantes
    QCAL_BASE_FREQUENCY,
    PHI,
    ZETA_HALF_PRIME,
    F0,
    # Clases
    SepulcroVacio,
    CuerpoGlorioso,
    PermisoEspectral,
    IntegralDeContorno,
    EstadoResurreccion,
    EcuacionResurreccion,
    ResultadoLaserNoetico,
    LaserNoetico,
    # API pública
    calcular_resurreccion,
    verificar_resurreccion,
    activar_laser_noetico,
)


# ============================================================================
# TestConstantes — 12 tests
# ============================================================================

class TestConstantes(unittest.TestCase):
    """Verifica que las constantes fundamentales tienen los valores correctos."""

    def test_qcal_base_frequency_valor(self):
        """QCAL_BASE_FREQUENCY debe ser 141.7001 Hz."""
        self.assertAlmostEqual(QCAL_BASE_FREQUENCY, 141.7001, places=4)

    def test_qcal_base_frequency_positivo(self):
        self.assertGreater(QCAL_BASE_FREQUENCY, 0)

    def test_f0_igual_qcal_base_frequency(self):
        """F0 debe ser igual a QCAL_BASE_FREQUENCY."""
        self.assertEqual(F0, QCAL_BASE_FREQUENCY)

    def test_phi_valor_aproximado(self):
        """PHI debe ser la proporción áurea ≈ 1.6180."""
        self.assertAlmostEqual(PHI, (1 + math.sqrt(5)) / 2, places=10)

    def test_phi_mayor_que_uno(self):
        self.assertGreater(PHI, 1.6)

    def test_zeta_half_prime_rango(self):
        """ζ'(1/2) debe estar en (−4.0, −3.9)."""
        self.assertGreater(ZETA_HALF_PRIME, -4.0)
        self.assertLess(ZETA_HALF_PRIME, -3.9)

    def test_zeta_half_prime_negativo(self):
        self.assertLess(ZETA_HALF_PRIME, 0)

    def test_zeta_half_prime_precision(self):
        """Debe concordar con −3.9226 hasta 4 decimales."""
        self.assertAlmostEqual(ZETA_HALF_PRIME, -3.9226, places=4)

    def test_omega_derivado(self):
        """ω₀ = 2π·f₀ ≈ 890.33 rad/s."""
        omega = 2.0 * math.pi * F0
        self.assertAlmostEqual(omega, 890.33, places=1)

    def test_periodo_derivado(self):
        """T₀ = 1/F0 ≈ 7.058 ms."""
        T0 = 1.0 / F0
        self.assertAlmostEqual(T0 * 1000, 7.058, places=2)

    def test_phi_cubo(self):
        """φ³ ≈ 4.236."""
        self.assertAlmostEqual(PHI ** 3, 4.2360679, places=6)

    def test_constantes_tipo(self):
        """Todas las constantes deben ser float."""
        self.assertIsInstance(QCAL_BASE_FREQUENCY, float)
        self.assertIsInstance(PHI, float)
        self.assertIsInstance(ZETA_HALF_PRIME, float)
        self.assertIsInstance(F0, float)


# ============================================================================
# TestSepulcroVacio — 14 tests
# ============================================================================

class TestSepulcroVacio(unittest.TestCase):
    """Verifica SepulcroVacio: I_d = exp(−eff·F₀)."""

    def setUp(self):
        self.sv0 = SepulcroVacio(eff=0.0)
        self.sv_small = SepulcroVacio(eff=1e-6)
        self.sv_large = SepulcroVacio(eff=0.1)

    def test_eff_cero_factor_inercia_uno(self):
        """I_d = 1.0 cuando eff=0."""
        self.assertEqual(self.sv0.factor_inercia, 1.0)

    def test_eff_cero_vida_indestructible(self):
        """vida_indestructible=True cuando eff=0."""
        self.assertTrue(self.sv0.vida_indestructible)

    def test_eff_positivo_factor_menor_uno(self):
        """I_d < 1.0 cuando eff > 0."""
        self.assertLess(self.sv_large.factor_inercia, 1.0)

    def test_formula_factor_inercia(self):
        """I_d = exp(−eff·F₀)."""
        eff = 0.01
        sv = SepulcroVacio(eff=eff)
        esperado = math.exp(-eff * F0)
        self.assertAlmostEqual(sv.factor_inercia, esperado, places=12)

    def test_limite_eff_cero_siempre_uno(self):
        """limite_eff_cero() siempre devuelve 1.0."""
        self.assertEqual(self.sv_large.limite_eff_cero(), 1.0)

    def test_calcular_para_eff_cero(self):
        self.assertEqual(self.sv0.calcular_para(0.0), 1.0)

    def test_calcular_para_eff_positivo(self):
        resultado = self.sv0.calcular_para(0.01)
        esperado = math.exp(-0.01 * F0)
        self.assertAlmostEqual(resultado, esperado, places=12)

    def test_calcular_para_eff_negativo_excepcion(self):
        with self.assertRaises(ValueError):
            self.sv0.calcular_para(-0.001)

    def test_eff_negativo_excepcion(self):
        with self.assertRaises(ValueError):
            SepulcroVacio(eff=-0.1)

    def test_f0_negativo_excepcion(self):
        with self.assertRaises(ValueError):
            SepulcroVacio(eff=0.0, f0=-1.0)

    def test_f0_cero_excepcion(self):
        with self.assertRaises(ValueError):
            SepulcroVacio(eff=0.0, f0=0.0)

    def test_info_devuelve_dict(self):
        info = self.sv0.info()
        self.assertIsInstance(info, dict)
        self.assertIn("eff", info)
        self.assertIn("factor_inercia", info)
        self.assertIn("vida_indestructible", info)

    def test_info_valores_correctos(self):
        info = self.sv0.info()
        self.assertEqual(info["eff"], 0.0)
        self.assertEqual(info["factor_inercia"], 1.0)
        self.assertTrue(info["vida_indestructible"])

    def test_factor_monotonico_decreciente(self):
        """I_d debe decrecer conforme eff aumenta."""
        effs = [0.0, 1e-5, 1e-4, 1e-3, 0.01, 0.1]
        factores = [SepulcroVacio(eff=e).factor_inercia for e in effs]
        for i in range(len(factores) - 1):
            self.assertGreaterEqual(factores[i], factores[i + 1])


# ============================================================================
# TestCuerpoGlorioso — 14 tests
# ============================================================================

class TestCuerpoGlorioso(unittest.TestCase):
    """Verifica CuerpoGlorioso: onda e^{i(ωt+φ)}, Phase-Lock, agua EZ."""

    def setUp(self):
        self.cg = CuerpoGlorioso()
        self.cg_fase = CuerpoGlorioso(phi=math.pi / 4)

    def test_onda_modulo_uno(self):
        """|e^{iωt}| = 1 para todo t."""
        for t in [0.0, 0.001, 0.01, 1.0]:
            self.assertAlmostEqual(abs(self.cg.onda(t)), 1.0, places=12)

    def test_onda_t0_real_uno(self):
        """e^{i·0} = 1 + 0j."""
        onda = self.cg.onda(0.0)
        self.assertAlmostEqual(onda.real, 1.0, places=12)
        self.assertAlmostEqual(onda.imag, 0.0, places=12)

    def test_onda_con_fase(self):
        """e^{i·φ} = cos(φ) + i·sin(φ) en t=0."""
        phi = math.pi / 3
        cg = CuerpoGlorioso(phi=phi)
        onda = cg.onda(0.0)
        self.assertAlmostEqual(onda.real, math.cos(phi), places=12)
        self.assertAlmostEqual(onda.imag, math.sin(phi), places=12)

    def test_omega_derivado(self):
        """ω = 2π·f₀."""
        self.assertAlmostEqual(self.cg.omega, 2.0 * math.pi * F0, places=10)

    def test_phase_locked_por_defecto(self):
        """ez_coherence=0.9995 → phase_locked=True."""
        self.assertTrue(self.cg.phase_locked)

    def test_phase_locked_falso_con_baja_coherencia(self):
        cg_baja = CuerpoGlorioso(ez_coherence=0.5)
        self.assertFalse(cg_baja.phase_locked)

    def test_phase_locked_umbral(self):
        """Umbral exacto: 0.888."""
        cg_umbral = CuerpoGlorioso(ez_coherence=0.888)
        self.assertTrue(cg_umbral.phase_locked)
        cg_bajo = CuerpoGlorioso(ez_coherence=0.8879)
        self.assertFalse(cg_bajo.phase_locked)

    def test_ez_coherence_por_defecto(self):
        self.assertAlmostEqual(self.cg.ez_coherence, 0.9995, places=4)

    def test_onda_array_shape(self):
        t = np.linspace(0, 1.0 / F0, 100)
        onda = self.cg.onda_array(t)
        self.assertEqual(onda.shape, (100,))

    def test_onda_array_modulo_uno(self):
        t = np.linspace(0, 1.0 / F0, 200)
        onda = self.cg.onda_array(t)
        np.testing.assert_allclose(np.abs(onda), 1.0, atol=1e-12)

    def test_coherencia_agua_ez_dict(self):
        info = self.cg.coherencia_agua_ez()
        self.assertIsInstance(info, dict)
        self.assertIn("ez_coherence", info)
        self.assertIn("phase_locked", info)
        self.assertIn("estructura", info)

    def test_coherencia_agua_ez_hexagonal(self):
        info = self.cg.coherencia_agua_ez()
        self.assertEqual(info["estructura"], "hexagonal")

    def test_coherencia_agua_ez_parcial(self):
        cg_parcial = CuerpoGlorioso(ez_coherence=0.95)
        info = cg_parcial.coherencia_agua_ez()
        self.assertEqual(info["estructura"], "parcial")

    def test_f0_cero_excepcion(self):
        with self.assertRaises(ValueError):
            CuerpoGlorioso(f0=0.0)

    def test_ez_coherence_fuera_rango_excepcion(self):
        with self.assertRaises(ValueError):
            CuerpoGlorioso(ez_coherence=1.5)
        with self.assertRaises(ValueError):
            CuerpoGlorioso(ez_coherence=-0.1)


# ============================================================================
# TestPermisoEspectral — 12 tests
# ============================================================================

class TestPermisoEspectral(unittest.TestCase):
    """Verifica PermisoEspectral: ζ'(1/2), eje crítico, ceros de Riemann."""

    def setUp(self):
        self.pe = PermisoEspectral()

    def test_zeta_prime_por_defecto(self):
        """ζ'(1/2) por defecto debe ser ZETA_HALF_PRIME."""
        self.assertEqual(self.pe.zeta_prime, ZETA_HALF_PRIME)

    def test_eje_critico_medio(self):
        """Re(s) = 0.5."""
        self.assertEqual(self.pe.eje_critico, 0.5)

    def test_permiso_espectral_activo(self):
        """Con ζ'(1/2) ≈ −3.9226 el permiso debe estar activo."""
        self.assertTrue(self.pe.permiso_espectral)

    def test_permiso_espectral_fuera_rango(self):
        pe_mal = PermisoEspectral(zeta_prime=-2.0)
        self.assertFalse(pe_mal.permiso_espectral)

    def test_verificar_eje_critico_correcto(self):
        self.assertTrue(self.pe.verificar_eje_critico(0.5))

    def test_verificar_eje_critico_incorrecto(self):
        self.assertFalse(self.pe.verificar_eje_critico(0.6))
        self.assertFalse(self.pe.verificar_eje_critico(0.0))

    def test_ceros_riemann_lista(self):
        """Debe haber exactamente 10 ceros de Riemann listados."""
        self.assertEqual(len(PermisoEspectral.CEROS_RIEMANN), 10)

    def test_primer_cero_riemann(self):
        """Primer cero: γ₁ ≈ 14.1347."""
        self.assertAlmostEqual(PermisoEspectral.CEROS_RIEMANN[0], 14.1347, places=4)

    def test_ceros_riemann_positivos(self):
        for cero in PermisoEspectral.CEROS_RIEMANN:
            self.assertGreater(cero, 0)

    def test_correlacion_riemann_resultado_en_rango(self):
        resultado = self.pe.correlacion_riemann(100.0)
        self.assertGreaterEqual(resultado, 0.0)
        self.assertLessEqual(resultado, 1.0)

    def test_info_devuelve_dict(self):
        info = self.pe.info()
        self.assertIsInstance(info, dict)
        self.assertIn("zeta_prime_half", info)
        self.assertIn("eje_critico", info)
        self.assertIn("permiso_espectral", info)

    def test_info_n_ceros(self):
        info = self.pe.info()
        self.assertEqual(info["n_ceros_riemann"], 10)


# ============================================================================
# TestIntegralDeContorno — 12 tests
# ============================================================================

class TestIntegralDeContorno(unittest.TestCase):
    """Verifica IntegralDeContorno: ∮_Ψ numérica con NumPy 2.0."""

    def setUp(self):
        self.ic = IntegralDeContorno(n_puntos=1000)

    def test_grilla_temporal_shape(self):
        t = self.ic.grilla_temporal()
        self.assertEqual(t.shape, (1000,))

    def test_grilla_temporal_inicio_cero(self):
        t = self.ic.grilla_temporal()
        self.assertEqual(t[0], 0.0)

    def test_grilla_temporal_fin_correcto(self):
        t = self.ic.grilla_temporal()
        self.assertAlmostEqual(t[-1], 1.0 / F0, places=10)

    def test_integrar_constante_real(self):
        """∫₀^T 1 dt ≈ T."""
        t = np.linspace(0.0, 1.0 / F0, 1000)
        integrando = np.ones(1000)
        resultado = self.ic.integrar(integrando, t)
        self.assertAlmostEqual(resultado.real, 1.0 / F0, places=8)
        self.assertAlmostEqual(resultado.imag, 0.0, places=12)

    def test_integrar_constante_compleja(self):
        """∫₀^T (1 + i) dt ≈ T(1 + i)."""
        t = np.linspace(0.0, 1.0, 1000)
        integrando = np.ones(1000, dtype=complex) * (1.0 + 1.0j)
        resultado = self.ic.integrar(integrando, t)
        self.assertAlmostEqual(resultado.real, 1.0, places=6)
        self.assertAlmostEqual(resultado.imag, 1.0, places=6)

    def test_integrar_sin_t_usa_grilla(self):
        """Si t=None debe usar grilla_temporal()."""
        integrando = np.ones(1000)
        resultado = self.ic.integrar(integrando)
        self.assertGreater(abs(resultado), 0)

    def test_integral_psi_tipo_complex(self):
        cuerpo = CuerpoGlorioso()
        sepulcro = SepulcroVacio(eff=0.0)
        resultado = self.ic.integral_psi(cuerpo, sepulcro)
        self.assertIsInstance(resultado, complex)

    def test_integral_psi_eff_cero(self):
        """Con eff=0, I_d=1 y el resultado de ∮ e^{iωt} dt ≈ 0 (período completo)."""
        cuerpo = CuerpoGlorioso()
        sepulcro = SepulcroVacio(eff=0.0)
        resultado = self.ic.integral_psi(cuerpo, sepulcro)
        # Integral de e^{iωt} sobre un período completo → ~0
        self.assertAlmostEqual(abs(resultado), 0.0, places=4)

    def test_n_puntos_personalizado(self):
        ic500 = IntegralDeContorno(n_puntos=500)
        self.assertEqual(ic500.n_puntos, 500)

    def test_t_total_personalizado(self):
        ic = IntegralDeContorno(t_total=1.0)
        self.assertEqual(ic.t_total, 1.0)

    def test_info_devuelve_dict(self):
        info = self.ic.info()
        self.assertIsInstance(info, dict)
        self.assertIn("n_puntos", info)
        self.assertIn("backend", info)

    def test_info_backend_trapezoid(self):
        info = self.ic.info()
        self.assertIn("trapezoid", info["backend"])


# ============================================================================
# TestEstadoResurreccion — 8 tests
# ============================================================================

class TestEstadoResurreccion(unittest.TestCase):
    """Verifica el dataclass EstadoResurreccion."""

    def setUp(self):
        self.estado = EstadoResurreccion(
            psi_r=1.0,
            factor_inercia=1.0,
            integral_contorno=complex(0.0, 0.0),
            coherencia_ez=0.9995,
            permiso_espectral=True,
            vida_indestructible=True,
        )

    def test_psi_r(self):
        self.assertEqual(self.estado.psi_r, 1.0)

    def test_factor_inercia(self):
        self.assertEqual(self.estado.factor_inercia, 1.0)

    def test_integral_contorno_tipo(self):
        self.assertIsInstance(self.estado.integral_contorno, complex)

    def test_coherencia_ez(self):
        self.assertAlmostEqual(self.estado.coherencia_ez, 0.9995, places=4)

    def test_permiso_espectral(self):
        self.assertTrue(self.estado.permiso_espectral)

    def test_vida_indestructible(self):
        self.assertTrue(self.estado.vida_indestructible)

    def test_estado_eff_distinto_cero(self):
        """Con eff>0, vida_indestructible debe ser False."""
        ec = EcuacionResurreccion(eff=0.1)
        estado = ec.calcular()
        self.assertFalse(estado.vida_indestructible)
        self.assertLess(estado.psi_r, 1.0)

    def test_estado_psi_igual_factor_inercia(self):
        """psi_r y factor_inercia deben ser iguales."""
        ec = EcuacionResurreccion(eff=0.0)
        estado = ec.calcular()
        self.assertEqual(estado.psi_r, estado.factor_inercia)


# ============================================================================
# TestEcuacionResurreccion — 16 tests
# ============================================================================

class TestEcuacionResurreccion(unittest.TestCase):
    """Verifica EcuacionResurreccion: motor integrado Ψ_ℜ → 1.0."""

    def setUp(self):
        self.ec0 = EcuacionResurreccion(eff=0.0)
        self.ec_small = EcuacionResurreccion(eff=1e-6)
        self.ec_large = EcuacionResurreccion(eff=0.1)

    def test_psi_r_eff_cero(self):
        """Ψ_ℜ = 1.0 cuando eff=0."""
        self.assertEqual(self.ec0.psi_r, 1.0)

    def test_psi_r_eff_positivo(self):
        """Ψ_ℜ < 1.0 cuando eff > 0."""
        self.assertLess(self.ec_large.psi_r, 1.0)

    def test_calcular_vida_indestructible_eff_cero(self):
        estado = self.ec0.calcular()
        self.assertTrue(estado.vida_indestructible)

    def test_calcular_vida_no_indestructible_eff_grande(self):
        estado = self.ec_large.calcular()
        self.assertFalse(estado.vida_indestructible)

    def test_calcular_permiso_espectral_activo(self):
        estado = self.ec0.calcular()
        self.assertTrue(estado.permiso_espectral)

    def test_calcular_coherencia_ez(self):
        estado = self.ec0.calcular()
        self.assertAlmostEqual(estado.coherencia_ez, 0.9995, places=4)

    def test_calcular_integral_tipo_complex(self):
        estado = self.ec0.calcular()
        self.assertIsInstance(estado.integral_contorno, complex)

    def test_psi_r_formula(self):
        """Ψ_ℜ = exp(−eff·F₀) debe coincidir con la fórmula."""
        eff = 0.005
        ec = EcuacionResurreccion(eff=eff)
        esperado = math.exp(-eff * F0)
        self.assertAlmostEqual(ec.psi_r, esperado, places=12)

    def test_phi_no_afecta_psi_r(self):
        """La fase φ no debe afectar Ψ_ℜ = I_d."""
        ec_phi0 = EcuacionResurreccion(eff=0.0, phi=0.0)
        ec_phi1 = EcuacionResurreccion(eff=0.0, phi=math.pi)
        self.assertEqual(ec_phi0.psi_r, ec_phi1.psi_r)

    def test_componentes_sepulcro(self):
        self.assertIsInstance(self.ec0.sepulcro, SepulcroVacio)

    def test_componentes_cuerpo(self):
        self.assertIsInstance(self.ec0.cuerpo, CuerpoGlorioso)

    def test_componentes_permiso(self):
        self.assertIsInstance(self.ec0.permiso, PermisoEspectral)

    def test_componentes_integral(self):
        self.assertIsInstance(self.ec0.integral, IntegralDeContorno)

    def test_info_devuelve_dict(self):
        info = self.ec0.info()
        self.assertIsInstance(info, dict)
        self.assertIn("psi_r", info)
        self.assertIn("vida_indestructible", info)

    def test_info_psi_r_eff_cero(self):
        info = self.ec0.info()
        self.assertEqual(info["psi_r"], 1.0)
        self.assertTrue(info["vida_indestructible"])

    def test_n_puntos_personalizado(self):
        ec = EcuacionResurreccion(n_puntos=500)
        self.assertEqual(ec.integral.n_puntos, 500)


# ============================================================================
# TestLaserNoetico — 14 tests
# ============================================================================

class TestLaserNoetico(unittest.TestCase):
    """Verifica LaserNoetico (Nodo 5): biología, electricidad, tiempo."""

    def setUp(self):
        self.laser = LaserNoetico(eff=0.0)
        self.resultado = self.laser.activar()

    def test_activar_devuelve_resultado(self):
        self.assertIsInstance(self.resultado, ResultadoLaserNoetico)

    def test_tres_dominios_activos(self):
        self.assertEqual(self.resultado.sistema["dominios_activos"], 3)

    def test_sistema_nodo_cinco(self):
        self.assertEqual(self.resultado.sistema["nodo"], 5)

    def test_sistema_vida_indestructible(self):
        self.assertTrue(self.resultado.sistema["vida_indestructible"])

    def test_coherencia_sistema(self):
        coherencia = self.resultado.sistema["coherencia"]
        self.assertGreater(coherencia, 0.0)
        self.assertLessEqual(coherencia, 1.0)

    def test_biologia_dominio(self):
        bio = self.resultado.biologia
        self.assertEqual(bio["dominio"], "biologia")
        self.assertTrue(bio["activo"])
        self.assertEqual(bio["estructura"], "hexagonal")

    def test_biologia_phase_locked(self):
        bio = self.resultado.biologia
        self.assertTrue(bio["phase_locked"])

    def test_electricidad_dominio(self):
        elec = self.resultado.electricidad
        self.assertEqual(elec["dominio"], "electricidad")
        self.assertTrue(elec["activo"])
        self.assertTrue(elec["pulso_reinicio"])

    def test_electricidad_frecuencia(self):
        elec = self.resultado.electricidad
        self.assertAlmostEqual(elec["frecuencia_hz"], F0, places=4)

    def test_tiempo_dominio(self):
        tiempo = self.resultado.tiempo
        self.assertEqual(tiempo["dominio"], "tiempo")
        self.assertEqual(tiempo["tipo"], "kairos")
        self.assertTrue(tiempo["activo"])

    def test_tiempo_dilatacion_infinita_eff_cero(self):
        tiempo = self.resultado.tiempo
        self.assertEqual(tiempo["factor_dilatacion"], float("inf"))

    def test_activar_biologia_metodo(self):
        bio = self.laser.activar_biologia()
        self.assertIsInstance(bio, dict)
        self.assertIn("agua_ez_coherencia", bio)

    def test_activar_electricidad_metodo(self):
        elec = self.laser.activar_electricidad()
        self.assertIsInstance(elec, dict)
        self.assertIn("periodo_ms", elec)

    def test_activar_tiempo_metodo(self):
        tiempo = self.laser.activar_tiempo()
        self.assertIsInstance(tiempo, dict)
        self.assertIn("kairos_activo", tiempo)


# ============================================================================
# TestAPIPublica — 10 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Verifica las tres funciones de la API pública."""

    def test_calcular_resurreccion_por_defecto(self):
        estado = calcular_resurreccion()
        self.assertIsInstance(estado, EstadoResurreccion)

    def test_calcular_resurreccion_psi_r_uno(self):
        estado = calcular_resurreccion()
        self.assertEqual(estado.psi_r, 1.0)

    def test_calcular_resurreccion_vida_indestructible(self):
        estado = calcular_resurreccion()
        self.assertTrue(estado.vida_indestructible)

    def test_calcular_resurreccion_con_eff(self):
        estado = calcular_resurreccion(eff=0.01)
        self.assertLess(estado.psi_r, 1.0)
        self.assertFalse(estado.vida_indestructible)

    def test_calcular_resurreccion_con_phi(self):
        """La fase φ no debe afectar el psi_r."""
        estado0 = calcular_resurreccion(phi=0.0)
        estado1 = calcular_resurreccion(phi=math.pi)
        self.assertEqual(estado0.psi_r, estado1.psi_r)

    def test_verificar_resurreccion_devuelve_dict(self):
        resultado = verificar_resurreccion()
        self.assertIsInstance(resultado, dict)

    def test_verificar_resurreccion_todos_verificados(self):
        resultado = verificar_resurreccion()
        self.assertTrue(resultado["resumen"]["todos_verificados"])

    def test_verificar_resurreccion_estado_vida(self):
        resultado = verificar_resurreccion()
        self.assertEqual(resultado["resumen"]["estado"], "VIDA INDESTRUCTIBLE")

    def test_activar_laser_noetico_devuelve_resultado(self):
        resultado = activar_laser_noetico()
        self.assertIsInstance(resultado, ResultadoLaserNoetico)

    def test_activar_laser_noetico_vida_indestructible(self):
        resultado = activar_laser_noetico()
        self.assertTrue(resultado.estado_resurreccion.vida_indestructible)


# ============================================================================
# TestIntegracion — 10 tests
# ============================================================================

class TestIntegracion(unittest.TestCase):
    """Flujos end-to-end de integración completa del sistema."""

    def test_flujo_completo_eff_cero(self):
        """Flujo completo con eff=0: Ψ_ℜ = 1.0."""
        sv = SepulcroVacio(eff=0.0)
        cg = CuerpoGlorioso()
        pe = PermisoEspectral()
        ic = IntegralDeContorno(n_puntos=500)
        self.assertEqual(sv.factor_inercia, 1.0)
        self.assertTrue(cg.phase_locked)
        self.assertTrue(pe.permiso_espectral)
        integral = ic.integral_psi(cg, sv)
        self.assertIsInstance(integral, complex)

    def test_ecuacion_y_laser_coherencia_consistente(self):
        """La coherencia del sistema Laser debe ser consistente con Ψ_ℜ."""
        ec = EcuacionResurreccion(eff=0.0)
        estado = ec.calcular()
        laser = LaserNoetico(eff=0.0)
        resultado = laser.activar()
        # coherencia_total = (ez_coherence + I_d) / 2
        esperada = (estado.coherencia_ez + estado.psi_r) / 2.0
        self.assertAlmostEqual(resultado.sistema["coherencia"], esperada, places=10)

    def test_verificar_resurreccion_seis_componentes(self):
        """verificar_resurreccion debe verificar 6 componentes."""
        resultado = verificar_resurreccion()
        self.assertEqual(resultado["resumen"]["n_verificaciones"], 6)

    def test_activar_laser_con_eff_pequeno(self):
        """Con eff muy pequeño, el sistema debe seguir coherente."""
        resultado = activar_laser_noetico(eff=1e-8)
        self.assertGreater(resultado.sistema["coherencia"], 0.999)

    def test_sepulcro_cuerpo_integral_pipeline(self):
        """Pipeline manual SepulcroVacio → CuerpoGlorioso → IntegralDeContorno."""
        sepulcro = SepulcroVacio(eff=0.0, f0=F0)
        cuerpo = CuerpoGlorioso(f0=F0, phi=0.0)
        integral = IntegralDeContorno(n_puntos=200, t_total=1.0)
        t = integral.grilla_temporal()
        onda = cuerpo.onda_array(t)
        I_t = np.full(len(t), sepulcro.factor_inercia)
        integrando = onda * I_t
        resultado = integral.integrar(integrando, t)
        self.assertIsInstance(resultado, complex)

    def test_calcular_resurreccion_rango_eff(self):
        """Ψ_ℜ debe estar en [0, 1] para cualquier eff ≥ 0."""
        for eff in [0.0, 0.001, 0.01, 0.1, 1.0]:
            estado = calcular_resurreccion(eff=eff)
            self.assertGreaterEqual(estado.psi_r, 0.0)
            self.assertLessEqual(estado.psi_r, 1.0)

    def test_laser_noetico_estado_resurreccion(self):
        """El estado_resurreccion del laser debe ser EstadoResurreccion."""
        resultado = activar_laser_noetico()
        self.assertIsInstance(resultado.estado_resurreccion, EstadoResurreccion)

    def test_laser_f0_personalizado(self):
        """Se puede crear LaserNoetico con f0 personalizado."""
        laser = LaserNoetico(f0=100.0, eff=0.0)
        resultado = laser.activar()
        self.assertEqual(resultado.electricidad["frecuencia_hz"], 100.0)

    def test_permiso_espectral_zeta_consistencia(self):
        """ζ'(1/2) del módulo debe concordar con el permiso espectral."""
        pe = PermisoEspectral(zeta_prime=ZETA_HALF_PRIME)
        self.assertTrue(pe.permiso_espectral)
        self.assertAlmostEqual(pe.zeta_prime, -3.9226, places=4)

    def test_flujo_verificacion_completo(self):
        """verificar_resurreccion debe completarse sin errores."""
        resultado = verificar_resurreccion()
        self.assertIn("sepulcro_vacio", resultado)
        self.assertIn("cuerpo_glorioso", resultado)
        self.assertIn("permiso_espectral", resultado)
        self.assertIn("integral_contorno", resultado)
        self.assertIn("ecuacion_resurreccion", resultado)
        self.assertIn("laser_noetico", resultado)
        self.assertIn("resumen", resultado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
