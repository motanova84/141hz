#!/usr/bin/env python3
"""
Tests for physics.fluido_holografico_kss

Validates the KSS holographic fluid model: at Ψ = 0.999999, the cytoplasmic
EZ water transitions to a Perfect Holographic Fluid whose shear viscosity/entropy
density ratio approaches the universal Kovtun-Son-Starinets bound:

    η/s  ≥  ℏ / (4π k_B)  ≈  6.08 × 10⁻¹³  K·s

References:
    Kovtun, Son & Starinets, Phys. Rev. Lett. 94, 111601 (2005).
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.fluido_holografico_kss import (
    ConstantesKSS,
    ViscosidadRotoresMoleculares,
    DensidadEntropiaUPE,
    FluidoHolografico,
    MicrotubuloCavidadKK,
    ValidacionKSS,
    SistemaKSSHolografico,
    ResultadoKSS,
    fluido_holografico_kss_activar,
    _KSS_LIMITE,
    _PSI_HOLOGRAFICO,
    _F_PICO,
    _F0_HZ,
    _ETA_EZ_NORMAL,
    _S_CITOPLASMA,
    _ETA_KSS_MIN,
)


class TestConstantesKSS(unittest.TestCase):
    """Tests for ConstantesKSS class."""

    def setUp(self):
        self.ck = ConstantesKSS()

    def test_kss_limite_valor(self):
        """KSS limit must be ℏ/(4π·k_B) ≈ 6.08×10⁻¹³ K·s."""
        expected = 1.054571817e-34 / (4.0 * math.pi * 1.380649e-23)
        self.assertEqual(self.ck.kss_limite, expected)

    def test_kss_limite_orden_magnitud(self):
        """KSS limit must be in the range 6×10⁻¹³ to 7×10⁻¹³ K·s."""
        self.assertGreater(self.ck.kss_limite, 6.0e-13)
        self.assertLess(self.ck.kss_limite, 7.0e-13)

    def test_hbar_valor(self):
        """ℏ must be 1.054571817×10⁻³⁴ J·s."""
        self.assertEqual(self.ck.hbar, 1.054571817e-34)

    def test_k_boltzmann_valor(self):
        """k_B must be 1.380649×10⁻²³ J/K."""
        self.assertEqual(self.ck.k_b, 1.380649e-23)

    def test_f_pico(self):
        """Spectral peak frequency must be 2002.89 Hz."""
        self.assertAlmostEqual(self.ck.f_pico, 2002.89, places=2)

    def test_f0(self):
        """Fundamental QCAL frequency must be 141.7001 Hz."""
        self.assertAlmostEqual(self.ck.f0, 141.7001, places=4)

    def test_escala_espectral(self):
        """Spectral scale f_pico/f₀ must be ~14.13."""
        scale = self.ck.escala_espectral
        self.assertGreater(scale, 14.0)
        self.assertLess(scale, 15.0)
        self.assertAlmostEqual(scale, _F_PICO / _F0_HZ, places=8)

    def test_kss_en_unidades_si(self):
        """kss_en_unidades_si() must return a string with KSS value."""
        s = self.ck.kss_en_unidades_si()
        self.assertIsInstance(s, str)
        self.assertIn("K·s", s)
        self.assertIn("ℏ", s)

    def test_repr(self):
        """repr must contain 'ConstantesKSS'."""
        self.assertIn("ConstantesKSS", repr(self.ck))


class TestViscosidadRotoresMoleculares(unittest.TestCase):
    """Tests for ViscosidadRotoresMoleculares class."""

    def setUp(self):
        self.vrm = ViscosidadRotoresMoleculares()

    def test_eta_ez_normal(self):
        """EZ water normal viscosity must be 1.2×10⁻³ Pa·s."""
        self.assertAlmostEqual(self.vrm.eta_ez_normal, 1.2e-3, places=6)

    def test_eta_kss_min_positiva(self):
        """Minimum KSS viscosity must be positive."""
        self.assertGreater(self.vrm.eta_kss_min, 0.0)

    def test_eta_kss_min_menor_que_ez(self):
        """KSS minimum viscosity must be less than normal EZ water viscosity."""
        self.assertLess(self.vrm.eta_kss_min, self.vrm.eta_ez_normal)

    def test_viscosidad_coherente_psi_cero(self):
        """At Ψ=0, viscosity must equal η_EZ_normal."""
        eta = self.vrm.viscosidad_coherente(0.0)
        self.assertAlmostEqual(eta, self.vrm.eta_ez_normal, places=10)

    def test_viscosidad_coherente_psi_uno(self):
        """At Ψ=1, viscosity must equal η_KSS_min."""
        eta = self.vrm.viscosidad_coherente(1.0)
        self.assertAlmostEqual(eta, self.vrm.eta_kss_min, places=15)

    def test_viscosidad_coherente_psi_holografico(self):
        """At Ψ=0.999999, effective viscosity must be close to η_KSS_min."""
        eta = self.vrm.viscosidad_coherente(_PSI_HOLOGRAFICO)
        # Must be near η_KSS_min within 0.1%
        delta = abs(eta - self.vrm.eta_kss_min) / self.vrm.eta_kss_min
        self.assertLess(delta, 0.001)

    def test_viscosidad_coherente_monotona(self):
        """Viscosity must decrease monotonically with increasing Ψ."""
        psi_values = [0.0, 0.5, 0.9, 0.999, 0.9999, 0.99999, 0.999999, 1.0]
        etas = [self.vrm.viscosidad_coherente(p) for p in psi_values]
        for i in range(len(etas) - 1):
            self.assertGreaterEqual(etas[i], etas[i + 1])

    def test_viscosidad_coherente_invalida_negativa(self):
        """Negative Ψ must raise ValueError."""
        with self.assertRaises(ValueError):
            self.vrm.viscosidad_coherente(-0.1)

    def test_viscosidad_coherente_invalida_mayor_uno(self):
        """Ψ > 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            self.vrm.viscosidad_coherente(1.1)

    def test_lifetime_rotor_referencia(self):
        """At η = η₀_ref, lifetime must be τ₀."""
        tau = self.vrm.lifetime_rotor(self.vrm.eta_0_ref)
        self.assertEqual(tau, self.vrm.tau_0)

    def test_lifetime_rotor_inversa(self):
        """viscosidad_desde_lifetime must invert lifetime_rotor."""
        for eta_test in [1e-4, 1e-3, 1e-2]:
            tau = self.vrm.lifetime_rotor(eta_test)
            eta_recovered = self.vrm.viscosidad_desde_lifetime(tau)
            self.assertAlmostEqual(eta_recovered, eta_test, places=12)

    def test_lifetime_rotor_invalido(self):
        """Non-positive η must raise ValueError in lifetime_rotor."""
        with self.assertRaises(ValueError):
            self.vrm.lifetime_rotor(0.0)
        with self.assertRaises(ValueError):
            self.vrm.lifetime_rotor(-1e-3)

    def test_lifetime_desde_invalido(self):
        """Non-positive τ must raise ValueError in viscosidad_desde_lifetime."""
        with self.assertRaises(ValueError):
            self.vrm.viscosidad_desde_lifetime(0.0)

    def test_repr(self):
        """repr must contain 'ViscosidadRotoresMoleculares'."""
        self.assertIn("ViscosidadRotoresMoleculares", repr(self.vrm))


class TestDensidadEntropiaUPE(unittest.TestCase):
    """Tests for DensidadEntropiaUPE class."""

    def setUp(self):
        self.due = DensidadEntropiaUPE()

    def test_s_citoplasma_valor(self):
        """Cytoplasm thermodynamic entropy density must be 3.9×10⁶ J/(K·m³)."""
        self.assertAlmostEqual(self.due.s_citoplasma, 3.9e6, places=0)

    def test_energia_foton_positiva(self):
        """UPE photon energy must be positive."""
        self.assertGreater(self.due.energia_foton_j, 0.0)

    def test_energia_foton_orden_magnitud(self):
        """UPE photon energy at 500 nm must be ~4×10⁻¹⁹ J."""
        self.assertGreater(self.due.energia_foton_j, 3.5e-19)
        self.assertLess(self.due.energia_foton_j, 4.5e-19)

    def test_densidad_entropia_psi_cero(self):
        """At Ψ=0, entropy density must be zero."""
        s = self.due.densidad_entropia(0.0)
        self.assertAlmostEqual(s, 0.0, places=10)

    def test_densidad_entropia_psi_uno(self):
        """At Ψ=1, entropy density must equal s_citoplasma."""
        s = self.due.densidad_entropia(1.0)
        self.assertAlmostEqual(s, self.due.s_citoplasma, places=5)

    def test_densidad_entropia_lineal(self):
        """Entropy density must be linear: s_eff = s_cyto × Ψ."""
        for psi in [0.1, 0.5, 0.75, 0.9, 0.999]:
            s = self.due.densidad_entropia(psi)
            expected = self.due.s_citoplasma * psi
            self.assertAlmostEqual(s, expected, places=5)

    def test_densidad_entropia_monotona(self):
        """Entropy density must increase with Ψ."""
        psi_values = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]
        s_values = [self.due.densidad_entropia(p) for p in psi_values]
        for i in range(len(s_values) - 1):
            self.assertLess(s_values[i], s_values[i + 1])

    def test_densidad_entropia_invalida(self):
        """Ψ outside [0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            self.due.densidad_entropia(-0.1)
        with self.assertRaises(ValueError):
            self.due.densidad_entropia(1.1)

    def test_tasa_upe_positiva(self):
        """UPE rate must be positive for Ψ > 0."""
        r = self.due.tasa_upe(0.5)
        self.assertGreater(r, 0.0)

    def test_tasa_upe_escala_con_psi(self):
        """UPE rate must increase with Ψ."""
        r1 = self.due.tasa_upe(0.5)
        r2 = self.due.tasa_upe(0.999999)
        self.assertLess(r1, r2)

    def test_tasa_upe_invalida(self):
        """tasa_upe must raise ValueError for invalid Ψ or f_pico."""
        with self.assertRaises(ValueError):
            self.due.tasa_upe(-0.1)
        with self.assertRaises(ValueError):
            self.due.tasa_upe(0.5, f_pico=-1.0)

    def test_repr(self):
        """repr must contain 'DensidadEntropiaUPE'."""
        self.assertIn("DensidadEntropiaUPE", repr(self.due))


class TestFluidoHolografico(unittest.TestCase):
    """Tests for FluidoHolografico class."""

    def setUp(self):
        self.fh = FluidoHolografico()

    def test_ratio_eta_s_mayor_o_igual_kss(self):
        """η/s must always be ≥ KSS (KSS is a lower bound)."""
        for psi in [0.1, 0.5, 0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999, 1.0]:
            ratio = self.fh.ratio_eta_s(psi)
            self.assertGreaterEqual(ratio, self.fh.constantes.kss_limite)

    def test_ratio_eta_s_converge_a_kss(self):
        """At Ψ=0.999999, η/s must be within 0.1% of KSS."""
        ratio = self.fh.ratio_eta_s(_PSI_HOLOGRAFICO)
        delta = abs(ratio - _KSS_LIMITE) / _KSS_LIMITE
        self.assertLess(delta, 0.001)

    def test_ratio_eta_s_decrece_con_psi(self):
        """η/s must decrease as Ψ increases (fluid approaches perfect)."""
        psi_values = [0.1, 0.5, 0.9, 0.999, 0.9999, 0.99999, 0.999999]
        ratios = [self.fh.ratio_eta_s(p) for p in psi_values]
        for i in range(len(ratios) - 1):
            self.assertGreater(ratios[i], ratios[i + 1])

    def test_ratio_eta_s_invalido(self):
        """Ψ ≤ 0 must raise ValueError in ratio_eta_s."""
        with self.assertRaises(ValueError):
            self.fh.ratio_eta_s(0.0)
        with self.assertRaises(ValueError):
            self.fh.ratio_eta_s(-0.1)

    def test_distancia_relativa_kss_no_negativa(self):
        """Relative distance to KSS must be ≥ 0 (KSS is a lower bound)."""
        for psi in [0.1, 0.5, 0.9, 0.999, 0.999999]:
            delta = self.fh.distancia_relativa_kss(psi)
            self.assertGreaterEqual(delta, 0.0)

    def test_distancia_relativa_decrece_con_psi(self):
        """Relative distance must decrease as Ψ increases."""
        d1 = self.fh.distancia_relativa_kss(0.5)
        d2 = self.fh.distancia_relativa_kss(0.9999)
        d3 = self.fh.distancia_relativa_kss(_PSI_HOLOGRAFICO)
        self.assertGreater(d1, d2)
        self.assertGreater(d2, d3)

    def test_es_holografico_psi_holografico(self):
        """At Ψ=0.999999, es_holografico must be True."""
        self.assertTrue(self.fh.es_holografico(_PSI_HOLOGRAFICO))

    def test_no_es_holografico_bajo_psi(self):
        """At Ψ=0.5, es_holografico must be False (far from KSS)."""
        self.assertFalse(self.fh.es_holografico(0.5))

    def test_repr(self):
        """repr must contain 'FluidoHolografico' and 'KSS'."""
        r = repr(self.fh)
        self.assertIn("FluidoHolografico", r)
        self.assertIn("KSS", r)


class TestMicrotubuloCavidadKK(unittest.TestCase):
    """Tests for MicrotubuloCavidadKK class."""

    def setUp(self):
        self.mt = MicrotubuloCavidadKK()

    def test_radio_microtubulo(self):
        """Microtubule inner radius must be 7.5 nm."""
        self.assertEqual(self.mt.r_microtubulo, 7.5e-9)

    def test_frecuencia_kk_positiva(self):
        """KK compactification frequency must be positive."""
        self.assertGreater(self.mt.f_kk, 0.0)

    def test_frecuencia_kk_orden_magnitud(self):
        """f_KK at 7.5 nm radius must be ~6.37×10¹⁵ Hz."""
        expected = 299_792_458.0 / (2.0 * math.pi * 7.5e-9)
        self.assertAlmostEqual(self.mt.f_kk, expected, places=3)
        self.assertGreater(self.mt.f_kk, 6.0e15)
        self.assertLess(self.mt.f_kk, 7.0e15)

    def test_escala_kk_f0_positiva(self):
        """f_KK/f₀ ratio must be positive and very large."""
        scale = self.mt.escala_kk_f0
        self.assertGreater(scale, 1.0e13)

    def test_coherencia_informacional_psi_holografico(self):
        """At Ψ=0.999999, KK channel coherence J_KK must be ≥ 0.888."""
        j = self.mt.coherencia_informacional(_PSI_HOLOGRAFICO)
        self.assertGreaterEqual(j, 0.888)

    def test_coherencia_informacional_crece_con_psi(self):
        """J_KK must increase as Ψ increases."""
        j1 = self.mt.coherencia_informacional(0.5)
        j2 = self.mt.coherencia_informacional(0.999)
        j3 = self.mt.coherencia_informacional(_PSI_HOLOGRAFICO)
        self.assertLess(j1, j2)
        self.assertLess(j2, j3)

    def test_coherencia_informacional_acotada(self):
        """J_KK must be in [0, 1]."""
        for psi in [0.1, 0.5, 0.9, 0.999, _PSI_HOLOGRAFICO]:
            j = self.mt.coherencia_informacional(psi)
            self.assertGreaterEqual(j, 0.0)
            self.assertLessEqual(j, 1.0)

    def test_cavidad_activa_psi_holografico(self):
        """At Ψ=0.999999, microtubule must be an active KK cavity."""
        self.assertTrue(self.mt.es_cavidad_activa(_PSI_HOLOGRAFICO))

    def test_repr(self):
        """repr must contain 'MicrotubuloCavidadKK' and 'nm'."""
        r = repr(self.mt)
        self.assertIn("MicrotubuloCavidadKK", r)
        self.assertIn("nm", r)


class TestValidacionKSS(unittest.TestCase):
    """Tests for ValidacionKSS class."""

    def setUp(self):
        self.val = ValidacionKSS()

    def test_validar_psi_holografico_aprobado(self):
        """Validation at Ψ=0.999999 must be approved."""
        result = self.val.validar(_PSI_HOLOGRAFICO)
        self.assertTrue(result["aprobado"])

    def test_validar_claves_presentes(self):
        """Validation result must contain all required keys."""
        result = self.val.validar(_PSI_HOLOGRAFICO)
        required_keys = [
            "eta_s", "kss", "distancia_relativa",
            "kss_no_violado", "es_holografico", "cavidad_activa", "aprobado",
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_validar_kss_no_violado(self):
        """KSS lower bound must not be violated at any coherence."""
        for psi in [0.1, 0.5, 0.9, 0.999, _PSI_HOLOGRAFICO]:
            result = self.val.validar(psi)
            self.assertTrue(result["kss_no_violado"],
                            msg=f"KSS violated at Ψ={psi}")

    def test_validar_kss_value_consistent(self):
        """Validation result KSS value must match module constant."""
        result = self.val.validar(_PSI_HOLOGRAFICO)
        self.assertEqual(result["kss"], _KSS_LIMITE)

    def test_validar_distancia_relativa_pequena(self):
        """At Ψ=0.999999, relative distance must be < 0.1%."""
        result = self.val.validar(_PSI_HOLOGRAFICO)
        self.assertLess(result["distancia_relativa"], 0.001)

    def test_validar_eta_s_coherente(self):
        """Reported η/s must equal kss × (1 + distancia_relativa)."""
        result = self.val.validar(_PSI_HOLOGRAFICO)
        expected_eta_s = result["kss"] * (1.0 + result["distancia_relativa"])
        self.assertAlmostEqual(result["eta_s"], expected_eta_s, places=12)

    def test_repr(self):
        """repr must contain 'ValidacionKSS'."""
        self.assertIn("ValidacionKSS", repr(self.val))


class TestSistemaKSSHolografico(unittest.TestCase):
    """Tests for SistemaKSSHolografico class."""

    def setUp(self):
        self.sistema = SistemaKSSHolografico()

    def test_evaluar_retorna_resultado_kss(self):
        """evaluar() must return a ResultadoKSS instance."""
        resultado = self.sistema.evaluar()
        self.assertIsInstance(resultado, ResultadoKSS)

    def test_evaluar_aprobado(self):
        """At Ψ=0.999999, system evaluation must be approved."""
        resultado = self.sistema.evaluar()
        self.assertTrue(resultado.aprobado)

    def test_evaluar_psi_coherencia(self):
        """Evaluated Ψ must equal the holographic coherence target."""
        resultado = self.sistema.evaluar()
        self.assertEqual(resultado.psi_coherencia, _PSI_HOLOGRAFICO)

    def test_evaluar_frecuencia_pico(self):
        """Peak frequency in result must be 2002.89 Hz."""
        resultado = self.sistema.evaluar()
        self.assertAlmostEqual(resultado.frecuencia_pico, _F_PICO, places=2)

    def test_evaluar_kss_limite(self):
        """KSS limit in result must match module constant."""
        resultado = self.sistema.evaluar()
        self.assertEqual(resultado.kss_limite, _KSS_LIMITE)

    def test_evaluar_eta_s_mayor_kss(self):
        """η/s must be ≥ KSS (lower bound)."""
        resultado = self.sistema.evaluar()
        self.assertGreaterEqual(resultado.ratio_eta_s, resultado.kss_limite)

    def test_evaluar_distancia_relativa_menor_umbral(self):
        """Relative distance must be < 0.1% at Ψ=0.999999."""
        resultado = self.sistema.evaluar()
        self.assertLess(resultado.distancia_relativa, 0.001)

    def test_evaluar_es_fluido_holografico(self):
        """At Ψ=0.999999, es_fluido_holografico must be True."""
        resultado = self.sistema.evaluar()
        self.assertTrue(resultado.es_fluido_holografico)

    def test_evaluar_coherencia_kk_activa(self):
        """KK coherence J_KK must be ≥ 0.888 at Ψ=0.999999."""
        resultado = self.sistema.evaluar()
        self.assertGreaterEqual(resultado.coherencia_kk, 0.888)

    def test_evaluar_mensaje_contiene_exito(self):
        """At Ψ=0.999999, message must contain success indicator."""
        resultado = self.sistema.evaluar()
        self.assertIn("✅", resultado.mensaje)

    def test_evaluar_mensaje_contiene_kss(self):
        """Message must mention KSS."""
        resultado = self.sistema.evaluar()
        self.assertIn("KSS", resultado.mensaje)

    def test_evaluar_consistencia_eta_s(self):
        """Reported η/s must match eta_efectiva / densidad_entropia."""
        resultado = self.sistema.evaluar()
        expected = resultado.eta_efectiva / resultado.densidad_entropia
        self.assertAlmostEqual(resultado.ratio_eta_s, expected, places=15)

    def test_evaluar_idempotente(self):
        """Multiple evaluar() calls must return consistent results."""
        r1 = self.sistema.evaluar()
        r2 = self.sistema.evaluar()
        self.assertEqual(r1.ratio_eta_s, r2.ratio_eta_s)
        self.assertEqual(r1.aprobado, r2.aprobado)
        self.assertEqual(r1.distancia_relativa, r2.distancia_relativa)

    def test_repr(self):
        """repr must contain 'SistemaKSSHolografico'."""
        self.assertIn("SistemaKSSHolografico", repr(self.sistema))


class TestFluidoHolograficoKSSActivar(unittest.TestCase):
    """Tests for the public API function fluido_holografico_kss_activar()."""

    def test_retorna_resultado_kss(self):
        """Must return ResultadoKSS instance."""
        resultado = fluido_holografico_kss_activar()
        self.assertIsInstance(resultado, ResultadoKSS)

    def test_aprobado(self):
        """Result must be approved."""
        resultado = fluido_holografico_kss_activar()
        self.assertTrue(resultado.aprobado)

    def test_psi_coherencia(self):
        """psi_coherencia must equal 0.999999."""
        resultado = fluido_holografico_kss_activar()
        self.assertEqual(resultado.psi_coherencia, 0.999999)

    def test_kss_limite_correcto(self):
        """kss_limite must match ℏ/(4π·k_B)."""
        resultado = fluido_holografico_kss_activar()
        expected = 1.054571817e-34 / (4.0 * math.pi * 1.380649e-23)
        self.assertEqual(resultado.kss_limite, expected)

    def test_distancia_relativa_menor_0_1_porciento(self):
        """Relative distance to KSS must be < 0.1%."""
        resultado = fluido_holografico_kss_activar()
        self.assertLess(resultado.distancia_relativa, 0.001)

    def test_kss_no_violado(self):
        """η/s must be ≥ KSS (lower bound not violated)."""
        resultado = fluido_holografico_kss_activar()
        self.assertGreaterEqual(resultado.ratio_eta_s, resultado.kss_limite)

    def test_es_fluido_holografico(self):
        """es_fluido_holografico must be True."""
        resultado = fluido_holografico_kss_activar()
        self.assertTrue(resultado.es_fluido_holografico)

    def test_frecuencia_pico_2003hz(self):
        """Peak frequency must be ~2003 Hz (LÁSER NOÉTICO peak)."""
        resultado = fluido_holografico_kss_activar()
        self.assertAlmostEqual(resultado.frecuencia_pico, 2002.89, places=2)

    def test_idempotente(self):
        """Multiple calls must return identical results."""
        r1 = fluido_holografico_kss_activar()
        r2 = fluido_holografico_kss_activar()
        self.assertEqual(r1.ratio_eta_s, r2.ratio_eta_s)
        self.assertEqual(r1.aprobado, r2.aprobado)


class TestKSSModuleConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_kss_limite_constante(self):
        """_KSS_LIMITE module constant must match ConstantesKSS value."""
        ck = ConstantesKSS()
        self.assertEqual(_KSS_LIMITE, ck.kss_limite)

    def test_psi_holografico(self):
        """_PSI_HOLOGRAFICO must be 0.999999."""
        self.assertEqual(_PSI_HOLOGRAFICO, 0.999999)

    def test_f_pico(self):
        """_F_PICO must be 2002.89 Hz."""
        self.assertAlmostEqual(_F_PICO, 2002.89, places=2)

    def test_f0_hz(self):
        """_F0_HZ must be 141.7001 Hz."""
        self.assertAlmostEqual(_F0_HZ, 141.7001, places=4)

    def test_eta_kss_min(self):
        """_ETA_KSS_MIN must equal _KSS_LIMITE × _S_CITOPLASMA."""
        expected = _KSS_LIMITE * _S_CITOPLASMA
        self.assertEqual(_ETA_KSS_MIN, expected)

    def test_eta_kss_min_menor_que_ez(self):
        """KSS minimum viscosity must be less than normal EZ water viscosity."""
        self.assertLess(_ETA_KSS_MIN, _ETA_EZ_NORMAL)


def run_tests():
    """Run all KSS holographic fluid tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestConstantesKSS,
        TestViscosidadRotoresMoleculares,
        TestDensidadEntropiaUPE,
        TestFluidoHolografico,
        TestMicrotubuloCavidadKK,
        TestValidacionKSS,
        TestSistemaKSSHolografico,
        TestFluidoHolograficoKSSActivar,
        TestKSSModuleConstants,
    ]

    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == "__main__":
    result = run_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
