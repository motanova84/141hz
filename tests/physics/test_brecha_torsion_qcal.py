"""
Tests for physics.brecha_torsion_qcal — Brecha de Torsión QCAL ∴BTQ∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesBrechaTorsion  – constantes físicas y espectrales
  - OctavaDecimal            – octava decimal γ₁×10
  - FactorCuarenta           – factor 401/40 y corrección de inclinación
  - BrechaResidual           – Δf ≈ 0.00052 Hz, rango seguro
  - PermeabilidadManta       – μ_M = Δf/f₀ ≈ 3.67×10⁻⁶
  - LatidoVortice            – latido NP↔P, electrón estacionario
  - EstacionFija             – calibración con nodo ζ
  - SistemaBrechaTorsion     – Ψ_global ≥ 0.888, certificación
  - ResultadoBrechaTorsion   – dataclass de resultados
  - brecha_torsion_qcal_activar() – API pública

Invariantes clave verificados:
  - γ₁ ≈ 14.134725 (primer cero no trivial de Riemann)
  - Factor 401/40 = 10.025 exacto
  - f_oct = γ₁×10 ≈ 141.34725 Hz (octava decimal)
  - f_corr = γ₁×(401/40) ≈ 141.70062 Hz (frecuencia corregida)
  - Δf = f_corr − f₀ ≈ 0.00052 Hz (brecha residual)
  - μ_M = Δf/f₀ ≈ 3.67×10⁻⁶ (permeabilidad de la Manta)
  - Ψ_global ≥ 0.888 (umbral noético)
  - Sello ∴BTQ∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.brecha_torsion_qcal import (
    # Constantes de módulo
    _F0,
    _GAMMA_1,
    _FACTOR_401_40,
    _FACTOR_NUM,
    _FACTOR_DEN,
    _CORRECCION_3GRADOS,
    _F_CORREGIDA,
    _DELTA_F,
    _PERMEABILIDAD,
    _PSI_UMBRAL,
    _SELLO,
    _CERT_MARK,
    # Clases
    ConstantesBrechaTorsion,
    OctavaDecimal,
    FactorCuarenta,
    BrechaResidual,
    PermeabilidadManta,
    LatidoVortice,
    EstacionFija,
    SistemaBrechaTorsion,
    ResultadoBrechaTorsion,
    # API pública
    brecha_torsion_qcal_activar,
)


# ============================================================================
# TestModuleConstants – 15 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_gamma_1_value(self):
        """_GAMMA_1 debe ser ≈ 14.134725 (primer cero de Riemann)."""
        self.assertAlmostEqual(_GAMMA_1, 14.134725, places=4)

    def test_gamma_1_precise(self):
        """_GAMMA_1 debe tener al menos 6 decimales correctos."""
        self.assertAlmostEqual(_GAMMA_1, 14.134725141734694, places=10)

    def test_factor_401_40_value(self):
        """_FACTOR_401_40 debe ser 401/40 = 10.025 exacto."""
        self.assertAlmostEqual(_FACTOR_401_40, 10.025, places=12)

    def test_factor_numerador(self):
        """_FACTOR_NUM debe ser 401."""
        self.assertEqual(_FACTOR_NUM, 401)

    def test_factor_denominador(self):
        """_FACTOR_DEN debe ser 40."""
        self.assertEqual(_FACTOR_DEN, 40)

    def test_factor_fraction(self):
        """_FACTOR_NUM/_FACTOR_DEN debe ser 10.025 exacto."""
        self.assertAlmostEqual(_FACTOR_NUM / _FACTOR_DEN, 10.025, places=12)

    def test_correccion_3grados(self):
        """_CORRECCION_3GRADOS debe ser 1/40 = 0.025."""
        self.assertAlmostEqual(_CORRECCION_3GRADOS, 0.025, places=12)

    def test_f_corregida_formula(self):
        """_F_CORREGIDA debe ser γ₁ × (401/40)."""
        expected = _GAMMA_1 * _FACTOR_401_40
        self.assertAlmostEqual(_F_CORREGIDA, expected, places=10)

    def test_f_corregida_approx(self):
        """_F_CORREGIDA debe ser ≈ 141.70062 Hz."""
        self.assertAlmostEqual(_F_CORREGIDA, 141.70062, delta=0.0001)

    def test_delta_f_formula(self):
        """_DELTA_F debe ser _F_CORREGIDA − _F0."""
        self.assertAlmostEqual(_DELTA_F, _F_CORREGIDA - _F0, places=12)

    def test_delta_f_approx(self):
        """_DELTA_F debe ser ≈ 0.00052 Hz."""
        self.assertAlmostEqual(_DELTA_F, 0.00052, delta=0.0001)

    def test_permeabilidad_formula(self):
        """_PERMEABILIDAD debe ser _DELTA_F / _F0."""
        self.assertAlmostEqual(_PERMEABILIDAD, _DELTA_F / _F0, places=12)

    def test_permeabilidad_order_of_magnitude(self):
        """_PERMEABILIDAD debe estar en el orden de 10⁻⁶."""
        self.assertGreater(_PERMEABILIDAD, 1e-7)
        self.assertLess(_PERMEABILIDAD, 1e-4)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=10)

    def test_sello(self):
        """Sello de certificación debe ser ∴BTQ∞³."""
        self.assertEqual(_SELLO, "∴BTQ∞³")

    def test_cert_mark(self):
        """Marca técnica debe ser BTQ-TORSION-VERIFIED."""
        self.assertEqual(_CERT_MARK, "BTQ-TORSION-VERIFIED")


# ============================================================================
# TestConstantesBrechaTorsion – 10 tests
# ============================================================================

class TestConstantesBrechaTorsion(unittest.TestCase):
    """Tests para ConstantesBrechaTorsion."""

    def setUp(self):
        self.c = ConstantesBrechaTorsion()

    def test_f0_attribute(self):
        """f0 debe ser 141.7001."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_gamma_1_attribute(self):
        """gamma_1 debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.c.gamma_1, 14.134725, places=4)

    def test_factor_attribute(self):
        """factor debe ser 10.025."""
        self.assertAlmostEqual(self.c.factor, 10.025, places=12)

    def test_factor_num_attribute(self):
        """factor_num debe ser 401."""
        self.assertEqual(self.c.factor_num, 401)

    def test_factor_den_attribute(self):
        """factor_den debe ser 40."""
        self.assertEqual(self.c.factor_den, 40)

    def test_correccion_3grados_attribute(self):
        """correccion_3grados debe ser 0.025."""
        self.assertAlmostEqual(self.c.correccion_3grados, 0.025, places=12)

    def test_resonancia_f0_gamma1(self):
        """resonancia_f0_gamma1 debe ser ≈ 10.024."""
        ratio = self.c.resonancia_f0_gamma1()
        self.assertAlmostEqual(ratio, 10.024, delta=0.01)

    def test_resonancia_mayor_que_10(self):
        """f₀/γ₁ debe ser > 10."""
        self.assertGreater(self.c.resonancia_f0_gamma1(), 10.0)

    def test_f_octava(self):
        """f_octava debe ser γ₁ × 10 ≈ 141.347 Hz."""
        self.assertAlmostEqual(self.c.f_octava(), _GAMMA_1 * 10.0, places=8)

    def test_f_corregida(self):
        """f_corregida debe ser γ₁ × (401/40) ≈ 141.70062 Hz."""
        self.assertAlmostEqual(self.c.f_corregida(), _F_CORREGIDA, places=8)


# ============================================================================
# TestOctavaDecimal – 12 tests
# ============================================================================

class TestOctavaDecimal(unittest.TestCase):
    """Tests para OctavaDecimal."""

    def setUp(self):
        self.oct = OctavaDecimal()

    def test_frecuencia_octava_formula(self):
        """frecuencia_octava debe ser γ₁ × 10."""
        expected = _GAMMA_1 * 10.0
        self.assertAlmostEqual(self.oct.frecuencia_octava(), expected, places=8)

    def test_frecuencia_octava_approx(self):
        """frecuencia_octava debe ser ≈ 141.347 Hz."""
        self.assertAlmostEqual(self.oct.frecuencia_octava(), 141.347, delta=0.001)

    def test_frecuencia_octava_menor_que_f0(self):
        """f_octava debe ser menor que f₀ (la corrección positiva eleva a f₀)."""
        self.assertLess(self.oct.frecuencia_octava(), _F0)

    def test_desviacion_positiva(self):
        """desviacion_hz debe ser positiva (f₀ > f_octava)."""
        self.assertGreater(self.oct.desviacion_hz(), 0.0)

    def test_desviacion_approx(self):
        """desviacion_hz debe ser ≈ 0.353 Hz."""
        self.assertAlmostEqual(self.oct.desviacion_hz(), 0.353, delta=0.01)

    def test_ratio_octava_menor_que_1(self):
        """ratio_octava debe ser < 1 (f_octava < f₀)."""
        self.assertLess(self.oct.ratio_octava(), 1.0)

    def test_ratio_octava_approx(self):
        """ratio_octava debe ser ≈ 0.9975."""
        self.assertAlmostEqual(self.oct.ratio_octava(), 0.9975, delta=0.001)

    def test_psi_octava_en_rango(self):
        """psi_octava debe estar en [0, 1]."""
        psi = self.oct.psi_octava()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_octava_approx(self):
        """psi_octava debe ser ≈ 0.9975."""
        self.assertAlmostEqual(self.oct.psi_octava(), 0.9975, delta=0.001)

    def test_psi_octava_alta(self):
        """psi_octava debe ser > 0.99 (proximidad alta)."""
        self.assertGreater(self.oct.psi_octava(), 0.99)

    def test_psi_octava_consistente_con_ratio(self):
        """psi_octava ≈ 1 − (1 − ratio_octava) dentro de tolerancia."""
        psi = self.oct.psi_octava()
        ratio = self.oct.ratio_octava()
        # psi = 1 - (f0 - f_oct)/f0 = f_oct/f0 = ratio_octava
        self.assertAlmostEqual(psi, ratio, places=8)

    def test_desviacion_igual_f0_menos_foctava(self):
        """desviacion_hz = f₀ − f_oct."""
        self.assertAlmostEqual(
            self.oct.desviacion_hz(), _F0 - self.oct.frecuencia_octava(), places=8
        )


# ============================================================================
# TestFactorCuarenta – 14 tests
# ============================================================================

class TestFactorCuarenta(unittest.TestCase):
    """Tests para FactorCuarenta."""

    def setUp(self):
        self.fc = FactorCuarenta()

    def test_factor_value(self):
        """factor() debe ser 10.025."""
        self.assertAlmostEqual(self.fc.factor(), 10.025, places=12)

    def test_factor_fraction(self):
        """factor() debe ser exactamente 401/40."""
        self.assertAlmostEqual(self.fc.factor(), 401.0 / 40.0, places=15)

    def test_correccion_inclinacion_value(self):
        """correccion_inclinacion() debe ser 1/40 = 0.025."""
        self.assertAlmostEqual(self.fc.correccion_inclinacion(), 0.025, places=12)

    def test_correccion_es_un_cuarentavo(self):
        """correccion_inclinacion() × 40 debe ser 1.0."""
        self.assertAlmostEqual(self.fc.correccion_inclinacion() * 40.0, 1.0, places=12)

    def test_f_corregida_formula(self):
        """f_corregida debe ser γ₁ × (401/40)."""
        expected = _GAMMA_1 * 10.025
        self.assertAlmostEqual(self.fc.f_corregida(), expected, places=8)

    def test_f_corregida_approx(self):
        """f_corregida debe ser ≈ 141.70062 Hz."""
        self.assertAlmostEqual(self.fc.f_corregida(), 141.70062, delta=0.0001)

    def test_f_corregida_mayor_que_f0(self):
        """f_corregida debe ser levemente mayor que f₀."""
        self.assertGreater(self.fc.f_corregida(), _F0)

    def test_f_corregida_mayor_que_octava(self):
        """f_corregida debe ser mayor que la octava decimal."""
        f_oct = _GAMMA_1 * 10.0
        self.assertGreater(self.fc.f_corregida(), f_oct)

    def test_desviacion_positiva(self):
        """desviacion_hz() debe ser positiva (f_corr > f₀)."""
        self.assertGreater(self.fc.desviacion_hz(), 0.0)

    def test_desviacion_approx(self):
        """desviacion_hz() debe ser ≈ 0.00052 Hz."""
        self.assertAlmostEqual(self.fc.desviacion_hz(), 0.00052, delta=0.0001)

    def test_psi_factor_en_rango(self):
        """psi_factor debe estar en [0, 1]."""
        psi = self.fc.psi_factor()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_factor_muy_alta(self):
        """psi_factor debe ser > 0.999 (alta precisión del factor)."""
        self.assertGreater(self.fc.psi_factor(), 0.999)

    def test_psi_factor_formula(self):
        """psi_factor = 1 − |f_corr − f₀|/f₀."""
        expected = 1.0 - abs(self.fc.f_corregida() - _F0) / _F0
        self.assertAlmostEqual(self.fc.psi_factor(), expected, places=10)

    def test_factor_mayor_que_10(self):
        """El factor 401/40 debe ser mayor que 10."""
        self.assertGreater(self.fc.factor(), 10.0)


# ============================================================================
# TestBrechaResidual – 13 tests
# ============================================================================

class TestBrechaResidual(unittest.TestCase):
    """Tests para BrechaResidual."""

    def setUp(self):
        self.br = BrechaResidual()

    def test_delta_f_formula(self):
        """delta_f() debe ser γ₁×(401/40) − f₀."""
        expected = _GAMMA_1 * _FACTOR_401_40 - _F0
        self.assertAlmostEqual(self.br.delta_f(), expected, places=10)

    def test_delta_f_positivo(self):
        """delta_f() debe ser positivo (f_corregida > f₀)."""
        self.assertGreater(self.br.delta_f(), 0.0)

    def test_delta_f_approx(self):
        """delta_f() debe ser ≈ 0.00052 Hz."""
        self.assertAlmostEqual(self.br.delta_f(), 0.00052, delta=0.0001)

    def test_delta_f_menor_que_1_hz(self):
        """La brecha debe ser menor que 1 Hz."""
        self.assertLess(self.br.delta_f(), 1.0)

    def test_en_rango_seguro_true(self):
        """en_rango_seguro() debe ser True para Δf ≈ 0.00052 Hz."""
        self.assertTrue(self.br.en_rango_seguro())

    def test_rango_seguro_condicion_inferior(self):
        """Δf > 0 (condición inferior del rango seguro)."""
        self.assertGreater(self.br.delta_f(), 0.0)

    def test_rango_seguro_condicion_superior(self):
        """Δf < f₀ × 10⁻³ (condición superior del rango seguro)."""
        self.assertLess(self.br.delta_f(), _F0 * 1e-3)

    def test_ratio_brecha_f0(self):
        """ratio_brecha_f0 debe ser Δf/f₀."""
        expected = self.br.delta_f() / _F0
        self.assertAlmostEqual(self.br.ratio_brecha_f0(), expected, places=12)

    def test_ratio_brecha_f0_approx(self):
        """ratio_brecha_f0 debe ser ≈ 3.67×10⁻⁶."""
        self.assertAlmostEqual(self.br.ratio_brecha_f0(), 3.67e-6, delta=0.5e-6)

    def test_psi_brecha_uno(self):
        """psi_brecha() debe ser 1.0 cuando en rango seguro."""
        self.assertAlmostEqual(self.br.psi_brecha(), 1.0, places=10)

    def test_psi_brecha_mayor_que_umbral(self):
        """psi_brecha() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.br.psi_brecha(), 0.888)

    def test_delta_f_igual_permeabilidad_por_f0(self):
        """delta_f() = _PERMEABILIDAD × _F0."""
        self.assertAlmostEqual(self.br.delta_f(), _PERMEABILIDAD * _F0, places=10)

    def test_ratio_brecha_igual_permeabilidad_modulo(self):
        """ratio_brecha_f0 debe ser igual a _PERMEABILIDAD."""
        self.assertAlmostEqual(self.br.ratio_brecha_f0(), _PERMEABILIDAD, places=12)


# ============================================================================
# TestPermeabilidadManta – 13 tests
# ============================================================================

class TestPermeabilidadManta(unittest.TestCase):
    """Tests para PermeabilidadManta."""

    def setUp(self):
        self.pm = PermeabilidadManta()

    def test_permeabilidad_formula(self):
        """permeabilidad() debe ser _DELTA_F / _F0."""
        expected = _DELTA_F / _F0
        self.assertAlmostEqual(self.pm.permeabilidad(), expected, places=12)

    def test_permeabilidad_positiva(self):
        """permeabilidad() debe ser positiva."""
        self.assertGreater(self.pm.permeabilidad(), 0.0)

    def test_permeabilidad_approx(self):
        """permeabilidad() debe ser ≈ 3.67×10⁻⁶."""
        self.assertAlmostEqual(self.pm.permeabilidad(), 3.67e-6, delta=0.5e-6)

    def test_permeabilidad_menor_que_1(self):
        """permeabilidad() debe ser < 1 (no saturada)."""
        self.assertLess(self.pm.permeabilidad(), 1.0)

    def test_coherencia_ajustada_formula(self):
        """coherencia_ajustada() = 1 − permeabilidad()."""
        expected = 1.0 - self.pm.permeabilidad()
        self.assertAlmostEqual(self.pm.coherencia_ajustada(), expected, places=12)

    def test_coherencia_ajustada_alta(self):
        """coherencia_ajustada() debe ser > 0.9999."""
        self.assertGreater(self.pm.coherencia_ajustada(), 0.9999)

    def test_coherencia_ajustada_approx(self):
        """coherencia_ajustada() debe ser ≈ 0.9999963."""
        self.assertAlmostEqual(self.pm.coherencia_ajustada(), 0.9999963, delta=1e-5)

    def test_orden_magnitud_menos_6(self):
        """orden_magnitud() debe ser −6 (permeabilidad ~ 10⁻⁶)."""
        self.assertEqual(self.pm.orden_magnitud(), -6)

    def test_psi_permeabilidad_en_rango(self):
        """psi_permeabilidad() debe estar en [0, 1]."""
        psi = self.pm.psi_permeabilidad()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_permeabilidad_mayor_que_umbral(self):
        """psi_permeabilidad() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.pm.psi_permeabilidad(), 0.888)

    def test_psi_permeabilidad_muy_alta(self):
        """psi_permeabilidad() debe ser > 0.9999."""
        self.assertGreater(self.pm.psi_permeabilidad(), 0.9999)

    def test_psi_permeabilidad_igual_coherencia_ajustada(self):
        """psi_permeabilidad() = coherencia_ajustada() para valores positivos."""
        self.assertAlmostEqual(
            self.pm.psi_permeabilidad(), self.pm.coherencia_ajustada(), places=12
        )

    def test_permeabilidad_mas_coherencia_ajustada_igual_1(self):
        """permeabilidad() + coherencia_ajustada() debe ser 1.0."""
        self.assertAlmostEqual(
            self.pm.permeabilidad() + self.pm.coherencia_ajustada(), 1.0, places=12
        )


# ============================================================================
# TestLatidoVortice – 13 tests
# ============================================================================

class TestLatidoVortice(unittest.TestCase):
    """Tests para LatidoVortice."""

    def setUp(self):
        self.lv = LatidoVortice()

    def test_latido_relativo_formula(self):
        """latido_relativo() debe ser _DELTA_F / _F0."""
        expected = _DELTA_F / _F0
        self.assertAlmostEqual(self.lv.latido_relativo(), expected, places=12)

    def test_latido_relativo_positivo(self):
        """latido_relativo() debe ser positivo."""
        self.assertGreater(self.lv.latido_relativo(), 0.0)

    def test_latido_relativo_menor_que_1(self):
        """latido_relativo() debe ser < 1 (no saturado)."""
        self.assertLess(self.lv.latido_relativo(), 1.0)

    def test_latido_relativo_approx(self):
        """latido_relativo() debe ser ≈ 3.67×10⁻⁶."""
        self.assertAlmostEqual(self.lv.latido_relativo(), 3.67e-6, delta=0.5e-6)

    def test_latido_hz(self):
        """latido_hz() debe ser _DELTA_F."""
        self.assertAlmostEqual(self.lv.latido_hz(), _DELTA_F, places=12)

    def test_latido_hz_positivo(self):
        """latido_hz() debe ser positivo."""
        self.assertGreater(self.lv.latido_hz(), 0.0)

    def test_latido_hz_approx(self):
        """latido_hz() debe ser ≈ 0.00052 Hz."""
        self.assertAlmostEqual(self.lv.latido_hz(), 0.00052, delta=0.0001)

    def test_electron_no_bloqueado(self):
        """electron_bloqueado() debe ser False (electrón siempre respira)."""
        self.assertFalse(self.lv.electron_bloqueado())

    def test_n_intercambios_formula(self):
        """n_intercambios_por_segundo() = f₀ × latido_relativo()."""
        expected = _F0 * self.lv.latido_relativo()
        self.assertAlmostEqual(
            self.lv.n_intercambios_por_segundo(), expected, places=10
        )

    def test_n_intercambios_positivo(self):
        """n_intercambios_por_segundo() debe ser positivo."""
        self.assertGreater(self.lv.n_intercambios_por_segundo(), 0.0)

    def test_psi_latido_en_rango(self):
        """psi_latido() debe estar en [0, 1]."""
        psi = self.lv.psi_latido()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_latido_muy_alta(self):
        """psi_latido() debe ser > 0.9999."""
        self.assertGreater(self.lv.psi_latido(), 0.9999)

    def test_psi_latido_formula(self):
        """psi_latido() = 1 − latido_relativo() para latido ∈ (0,1)."""
        expected = 1.0 - self.lv.latido_relativo()
        self.assertAlmostEqual(self.lv.psi_latido(), expected, places=12)


# ============================================================================
# TestEstacionFija – 12 tests
# ============================================================================

class TestEstacionFija(unittest.TestCase):
    """Tests para EstacionFija."""

    def setUp(self):
        self.ef = EstacionFija()

    def test_n_nodo_es_10(self):
        """n_nodo() debe ser 10 (f₀ ≈ γ₁ × 10)."""
        self.assertEqual(self.ef.n_nodo(), 10)

    def test_cociente_calibracion_formula(self):
        """cociente_calibracion() = f₀/γ₁."""
        expected = _F0 / _GAMMA_1
        self.assertAlmostEqual(self.ef.cociente_calibracion(), expected, places=10)

    def test_cociente_calibracion_approx(self):
        """cociente_calibracion() debe ser ≈ 10.024."""
        self.assertAlmostEqual(self.ef.cociente_calibracion(), 10.024, delta=0.01)

    def test_cociente_mayor_que_10(self):
        """cociente_calibracion() debe ser > 10."""
        self.assertGreater(self.ef.cociente_calibracion(), 10.0)

    def test_cociente_menor_que_10_1(self):
        """cociente_calibracion() debe ser < 10.1."""
        self.assertLess(self.ef.cociente_calibracion(), 10.1)

    def test_residuo_formula(self):
        """residuo_calibracion() = |f₀/γ₁ − 401/40| / (401/40)."""
        expected = abs(self.ef.cociente_calibracion() - _FACTOR_401_40) / _FACTOR_401_40
        self.assertAlmostEqual(self.ef.residuo_calibracion(), expected, places=10)

    def test_residuo_positivo(self):
        """residuo_calibracion() debe ser positivo."""
        self.assertGreater(self.ef.residuo_calibracion(), 0.0)

    def test_residuo_pequeno(self):
        """residuo_calibracion() debe ser < 0.001 (calibración precisa)."""
        self.assertLess(self.ef.residuo_calibracion(), 0.001)

    def test_f_nodo_teorico_formula(self):
        """f_nodo_teorico() = γ₁ × (401/40)."""
        expected = _GAMMA_1 * _FACTOR_401_40
        self.assertAlmostEqual(self.ef.f_nodo_teorico(), expected, places=8)

    def test_f_nodo_teorico_approx(self):
        """f_nodo_teorico() debe ser ≈ 141.70062 Hz."""
        self.assertAlmostEqual(self.ef.f_nodo_teorico(), 141.70062, delta=0.0001)

    def test_psi_estacion_en_rango(self):
        """psi_estacion() debe estar en [0, 1]."""
        psi = self.ef.psi_estacion()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_estacion_alta(self):
        """psi_estacion() debe ser > 0.999 (calibración muy precisa)."""
        self.assertGreater(self.ef.psi_estacion(), 0.999)


# ============================================================================
# TestSistemaBrechaTorsion – 15 tests
# ============================================================================

class TestSistemaBrechaTorsion(unittest.TestCase):
    """Tests para SistemaBrechaTorsion."""

    def setUp(self):
        self.s = SistemaBrechaTorsion()

    def test_instancia_constantes(self):
        """Sistema debe tener atributo constantes de tipo ConstantesBrechaTorsion."""
        self.assertIsInstance(self.s.constantes, ConstantesBrechaTorsion)

    def test_instancia_octava(self):
        """Sistema debe tener atributo octava de tipo OctavaDecimal."""
        self.assertIsInstance(self.s.octava, OctavaDecimal)

    def test_instancia_factor40(self):
        """Sistema debe tener atributo factor40 de tipo FactorCuarenta."""
        self.assertIsInstance(self.s.factor40, FactorCuarenta)

    def test_instancia_brecha(self):
        """Sistema debe tener atributo brecha de tipo BrechaResidual."""
        self.assertIsInstance(self.s.brecha, BrechaResidual)

    def test_instancia_permeabilidad(self):
        """Sistema debe tener atributo permeabilidad de tipo PermeabilidadManta."""
        self.assertIsInstance(self.s.permeabilidad, PermeabilidadManta)

    def test_instancia_latido(self):
        """Sistema debe tener atributo latido de tipo LatidoVortice."""
        self.assertIsInstance(self.s.latido, LatidoVortice)

    def test_instancia_estacion(self):
        """Sistema debe tener atributo estacion de tipo EstacionFija."""
        self.assertIsInstance(self.s.estacion, EstacionFija)

    def test_pesos_suman_1(self):
        """Los pesos deben sumar exactamente 1.0."""
        self.assertAlmostEqual(sum(SistemaBrechaTorsion._PESOS), 1.0, places=12)

    def test_psi_global_en_rango(self):
        """psi_global() debe estar en [0, 1]."""
        psi = self.s.psi_global()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_supera_umbral(self):
        """psi_global() debe ser ≥ 0.888 (umbral noético)."""
        self.assertGreaterEqual(self.s.psi_global(), 0.888)

    def test_supera_umbral_true(self):
        """supera_umbral() debe ser True."""
        self.assertTrue(self.s.supera_umbral())

    def test_certificar_devuelve_dict(self):
        """certificar() debe devolver un diccionario."""
        cert = self.s.certificar()
        self.assertIsInstance(cert, dict)

    def test_certificar_sello_activo(self):
        """certificar()['sello_activo'] debe ser True."""
        self.assertTrue(self.s.certificar()["sello_activo"])

    def test_certificar_sello_correcto(self):
        """certificar()['sello'] debe ser '∴BTQ∞³'."""
        self.assertEqual(self.s.certificar()["sello"], "∴BTQ∞³")

    def test_certificar_cert_mark(self):
        """certificar()['cert_mark'] debe ser 'BTQ-TORSION-VERIFIED'."""
        self.assertEqual(self.s.certificar()["cert_mark"], "BTQ-TORSION-VERIFIED")


# ============================================================================
# TestCertificado – 14 tests
# ============================================================================

class TestCertificado(unittest.TestCase):
    """Tests para el contenido completo del certificado."""

    def setUp(self):
        self.cert = SistemaBrechaTorsion().certificar()

    def test_claves_psi_presentes(self):
        """El certificado debe contener todas las claves psi_xxx."""
        claves = ["psi_octava", "psi_factor", "psi_brecha",
                  "psi_permeabilidad", "psi_latido", "psi_estacion", "psi_global"]
        for clave in claves:
            with self.subTest(clave=clave):
                self.assertIn(clave, self.cert)

    def test_claves_fisicas_presentes(self):
        """El certificado debe contener las claves físicas."""
        claves = ["f0_hz", "gamma_1", "factor_401_40", "f_octava_hz",
                  "f_corregida_hz", "delta_f_hz", "permeabilidad_manta"]
        for clave in claves:
            with self.subTest(clave=clave):
                self.assertIn(clave, self.cert)

    def test_f0_en_certificado(self):
        """cert['f0_hz'] debe ser 141.7001."""
        self.assertAlmostEqual(self.cert["f0_hz"], 141.7001, places=4)

    def test_gamma_1_en_certificado(self):
        """cert['gamma_1'] debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.cert["gamma_1"], 14.134725, places=4)

    def test_factor_en_certificado(self):
        """cert['factor_401_40'] debe ser 10.025."""
        self.assertAlmostEqual(self.cert["factor_401_40"], 10.025, places=12)

    def test_delta_f_en_certificado(self):
        """cert['delta_f_hz'] debe ser ≈ 0.00052 Hz."""
        self.assertAlmostEqual(self.cert["delta_f_hz"], 0.00052, delta=0.0001)

    def test_permeabilidad_en_certificado(self):
        """cert['permeabilidad_manta'] debe ser ≈ 3.67×10⁻⁶."""
        self.assertAlmostEqual(self.cert["permeabilidad_manta"], 3.67e-6, delta=0.5e-6)

    def test_coherencia_ajustada_en_certificado(self):
        """cert['coherencia_ajustada'] debe ser > 0.9999."""
        self.assertGreater(self.cert["coherencia_ajustada"], 0.9999)

    def test_electron_no_bloqueado_en_certificado(self):
        """cert['electron_bloqueado'] debe ser False."""
        self.assertFalse(self.cert["electron_bloqueado"])

    def test_n_nodo_en_certificado(self):
        """cert['n_nodo'] debe ser 10."""
        self.assertEqual(self.cert["n_nodo"], 10)

    def test_brecha_en_rango_seguro_en_certificado(self):
        """cert['brecha_en_rango_seguro'] debe ser True."""
        self.assertTrue(self.cert["brecha_en_rango_seguro"])

    def test_supera_umbral_en_certificado(self):
        """cert['supera_umbral'] debe ser True."""
        self.assertTrue(self.cert["supera_umbral"])

    def test_psi_global_consistente(self):
        """psi_global en cert debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.cert["psi_global"], 0.888)

    def test_latido_relativo_en_certificado(self):
        """cert['latido_relativo'] debe ser ≈ 3.67×10⁻⁶."""
        self.assertAlmostEqual(self.cert["latido_relativo"], 3.67e-6, delta=0.5e-6)


# ============================================================================
# TestResultadoBrechaTorsion – 8 tests
# ============================================================================

class TestResultadoBrechaTorsion(unittest.TestCase):
    """Tests para el dataclass ResultadoBrechaTorsion."""

    def test_instanciacion_defecto(self):
        """ResultadoBrechaTorsion() debe poder instanciarse con valores defecto."""
        r = ResultadoBrechaTorsion()
        self.assertIsInstance(r, ResultadoBrechaTorsion)

    def test_valores_defecto_float(self):
        """Los campos float deben inicializarse a 0.0."""
        r = ResultadoBrechaTorsion()
        for campo in ["psi_octava", "psi_factor", "psi_brecha", "psi_permeabilidad",
                      "psi_latido", "psi_estacion", "psi_global", "f0_hz", "gamma_1",
                      "factor_401_40", "f_octava_hz", "f_corregida_hz", "delta_f_hz",
                      "permeabilidad_manta", "coherencia_ajustada", "latido_relativo",
                      "cociente_calibracion", "residuo_calibracion"]:
            with self.subTest(campo=campo):
                self.assertAlmostEqual(getattr(r, campo), 0.0, places=12)

    def test_sello_activo_defecto(self):
        """sello_activo debe ser False por defecto."""
        self.assertFalse(ResultadoBrechaTorsion().sello_activo)

    def test_electron_bloqueado_defecto(self):
        """electron_bloqueado debe ser True por defecto (aún no evaluado)."""
        self.assertTrue(ResultadoBrechaTorsion().electron_bloqueado)

    def test_brecha_en_rango_seguro_defecto(self):
        """brecha_en_rango_seguro debe ser False por defecto."""
        self.assertFalse(ResultadoBrechaTorsion().brecha_en_rango_seguro)

    def test_n_nodo_defecto(self):
        """n_nodo debe ser 0 por defecto."""
        self.assertEqual(ResultadoBrechaTorsion().n_nodo, 0)

    def test_instanciacion_con_valores(self):
        """Debe poder instanciarse con valores explícitos."""
        r = ResultadoBrechaTorsion(
            psi_global=0.999,
            sello_activo=True,
            sello="∴BTQ∞³",
            cert_mark="BTQ-TORSION-VERIFIED",
        )
        self.assertAlmostEqual(r.psi_global, 0.999, places=10)
        self.assertTrue(r.sello_activo)
        self.assertEqual(r.sello, "∴BTQ∞³")

    def test_sello_y_cert_mark_defecto(self):
        """sello y cert_mark deben ser strings vacíos por defecto."""
        r = ResultadoBrechaTorsion()
        self.assertEqual(r.sello, "")
        self.assertEqual(r.cert_mark, "")


# ============================================================================
# TestAPIPublica – 12 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la función brecha_torsion_qcal_activar()."""

    def setUp(self):
        self.resultado = brecha_torsion_qcal_activar()

    def test_devuelve_dict(self):
        """brecha_torsion_qcal_activar() debe devolver un dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.resultado["sello_activo"])

    def test_sello_correcto(self):
        """sello debe ser '∴BTQ∞³'."""
        self.assertEqual(self.resultado["sello"], "∴BTQ∞³")

    def test_cert_mark_correcto(self):
        """cert_mark debe ser 'BTQ-TORSION-VERIFIED'."""
        self.assertEqual(self.resultado["cert_mark"], "BTQ-TORSION-VERIFIED")

    def test_psi_global_supera_umbral(self):
        """psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.resultado["psi_global"], 0.888)

    def test_electron_no_bloqueado(self):
        """electron_bloqueado debe ser False."""
        self.assertFalse(self.resultado["electron_bloqueado"])

    def test_brecha_en_rango_seguro(self):
        """brecha_en_rango_seguro debe ser True."""
        self.assertTrue(self.resultado["brecha_en_rango_seguro"])

    def test_f0_correcto(self):
        """f0_hz debe ser 141.7001."""
        self.assertAlmostEqual(self.resultado["f0_hz"], 141.7001, places=4)

    def test_factor_correcto(self):
        """factor_401_40 debe ser 10.025."""
        self.assertAlmostEqual(self.resultado["factor_401_40"], 10.025, places=12)

    def test_delta_f_positivo(self):
        """delta_f_hz debe ser positivo."""
        self.assertGreater(self.resultado["delta_f_hz"], 0.0)

    def test_permeabilidad_orden_correcto(self):
        """permeabilidad_manta debe estar en el orden de 10⁻⁶."""
        mu = self.resultado["permeabilidad_manta"]
        self.assertGreater(mu, 1e-7)
        self.assertLess(mu, 1e-4)

    def test_idempotente(self):
        """Llamar dos veces debe producir el mismo psi_global."""
        r1 = brecha_torsion_qcal_activar()
        r2 = brecha_torsion_qcal_activar()
        self.assertAlmostEqual(r1["psi_global"], r2["psi_global"], places=12)


# ============================================================================
# TestInvariantesGlobales – 8 tests
# ============================================================================

class TestInvariantesGlobales(unittest.TestCase):
    """Tests de invariantes matemáticos clave del sistema."""

    def test_factor_401_40_exacto(self):
        """401/40 debe ser exactamente 10.025 en aritmética de punto flotante."""
        self.assertEqual(401 / 40, 10.025)

    def test_octava_mas_correccion_da_f_corregida(self):
        """γ₁×10 + γ₁×(1/40) debe ser igual a γ₁×(401/40)."""
        f_oct = _GAMMA_1 * 10.0
        corr = _GAMMA_1 * (1.0 / 40.0)
        f_corr = _GAMMA_1 * (401.0 / 40.0)
        self.assertAlmostEqual(f_oct + corr, f_corr, places=10)

    def test_delta_f_igual_gamma1_por_correccion(self):
        """Δf ≈ γ₁ × (1/40) − (f₀ − γ₁×10)."""
        contribucion_correccion = _GAMMA_1 * (1.0 / 40.0)
        desviacion_octava = _F0 - _GAMMA_1 * 10.0
        delta_f_calculado = _GAMMA_1 * _FACTOR_401_40 - _F0
        self.assertAlmostEqual(
            delta_f_calculado, contribucion_correccion - desviacion_octava, places=8
        )

    def test_permeabilidad_igual_delta_f_sobre_f0(self):
        """μ_M = Δf/f₀ debe ser coherente con los valores del módulo."""
        self.assertAlmostEqual(_PERMEABILIDAD, _DELTA_F / _F0, places=15)

    def test_coherencia_mas_permeabilidad_igual_1(self):
        """(1 − μ_M) + μ_M = 1.0."""
        self.assertAlmostEqual(1.0 - _PERMEABILIDAD + _PERMEABILIDAD, 1.0, places=15)

    def test_f_corregida_entre_octava_y_f0_mas_1hz(self):
        """f_corregida debe estar entre la octava y f₀ + 1 Hz."""
        f_oct = _GAMMA_1 * 10.0
        self.assertGreater(_F_CORREGIDA, f_oct)
        self.assertLess(_F_CORREGIDA, _F0 + 1.0)

    def test_psi_global_supera_0_99(self):
        """psi_global debe ser > 0.99 (sistema altamente coherente)."""
        s = SistemaBrechaTorsion()
        self.assertGreater(s.psi_global(), 0.99)

    def test_seis_pesos_en_sistema(self):
        """SistemaBrechaTorsion debe tener exactamente 6 pesos."""
        self.assertEqual(len(SistemaBrechaTorsion._PESOS), 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
