#!/usr/bin/env python3
"""
Tests for physics.quantum_scaling — Escalado Cuántico Topológico QST∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesQuantumScaling  – constantes físicas del sistema
  - DimensionCuantica         – dimensión adélica d̃₆ y Kac-Moody d_j
  - PesoConforme              – peso conforme h_j = j(j+1)/(k+2)
  - FactorEscalaAdelica       – √(k+c₇) / c₇^(1/3)
  - AcoplamientoQuiral        – (c₇²−1)/(2(k+2)) = 4/3
  - RutaTransmisionSchumann   – f₂ = f_S·d̃₆·escala·acoplamiento
  - CoherenciaTopologica      – Ψ_top = 1 − |f₂ − F₀|/F₀ ≥ 0.888
  - SistemaQuantumScaling     – orquestador con activar()
  - ResultadoQuantumScaling   – dataclass de resultados
  - calcular_f2_topologico()  – API pública (frecuencia)
  - quantum_scaling_activar() – API pública (dict completo)

Invariantes clave verificados:
  - k=16, c7=7, j=6, f_S=7.83 Hz
  - d̃₆ = sin(7π/18) / sin(π/18) ≈ 5.411
  - h₆ = 7/3 ≈ 2.333
  - escala = √23 / 7^(1/3) ≈ 2.507
  - acoplamiento = 4/3 ≈ 1.333
  - f₂ ≈ 141.64 Hz  (error < 0.05 % respecto a F₀=141.7001 Hz)
  - Ψ_top ≥ 0.888 → sello QST∞³ ACTIVO

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0 (compatible con MIT)
Date: 2026-03-27
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.quantum_scaling import (
    # Constantes de módulo
    _F0,
    _F_SCHUMANN,
    _K,
    _C7,
    _J,
    _K2,
    _PSI_UMBRAL,
    _DIM_6,
    _H6,
    _ESCALA,
    _ACOPLAMIENTO,
    _F2,
    _PSI_TOPOLOGICA,
    # Clases
    ConstantesQuantumScaling,
    DimensionCuantica,
    PesoConforme,
    FactorEscalaAdelica,
    AcoplamientoQuiral,
    RutaTransmisionSchumann,
    CoherenciaTopologica,
    SistemaQuantumScaling,
    ResultadoQuantumScaling,
    # API pública
    calcular_f2_topologico,
    quantum_scaling_activar,
)


# ============================================================================
# TestModuleConstants – constantes de módulo
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_f_schumann_value(self):
        """_F_SCHUMANN debe ser 7.83 Hz."""
        self.assertAlmostEqual(_F_SCHUMANN, 7.83, places=4)

    def test_k_value(self):
        """Nivel k de Kac-Moody debe ser 16."""
        self.assertEqual(_K, 16)

    def test_c7_value(self):
        """Parámetro del heptágono c7 debe ser 7."""
        self.assertEqual(_C7, 7)

    def test_j_value(self):
        """Espín j debe ser 6."""
        self.assertEqual(_J, 6)

    def test_k2_value(self):
        """k+2 debe ser 18."""
        self.assertEqual(_K2, 18)

    def test_psi_umbral_value(self):
        """Umbral de coherencia debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_dim_6_value(self):
        """Dimensión adélica d̃₆ ≈ 5.411."""
        expected = math.sin(7 * math.pi / 18) / math.sin(math.pi / 18)
        self.assertAlmostEqual(_DIM_6, expected, places=10)
        self.assertAlmostEqual(_DIM_6, 5.411, places=2)

    def test_h6_value(self):
        """Peso conforme h₆ = 7/3 ≈ 2.333."""
        self.assertAlmostEqual(_H6, 7.0 / 3.0, places=10)

    def test_escala_value(self):
        """Factor de escala ≈ 2.507."""
        expected = math.sqrt(23) / (7 ** (1.0 / 3.0))
        self.assertAlmostEqual(_ESCALA, expected, places=10)
        self.assertAlmostEqual(_ESCALA, 2.507, places=2)

    def test_acoplamiento_value(self):
        """Acoplamiento quiral = 4/3."""
        self.assertAlmostEqual(_ACOPLAMIENTO, 4.0 / 3.0, places=10)

    def test_f2_value(self):
        """f₂ ≈ 141.64 Hz."""
        self.assertAlmostEqual(_F2, 141.64, delta=0.10)

    def test_psi_topologica_value(self):
        """Ψ_top ≥ 0.999."""
        self.assertGreater(_PSI_TOPOLOGICA, 0.999)

    def test_f2_close_to_f0(self):
        """f₂ debe estar a menos del 0.1% de F₀."""
        error_pct = abs(_F2 - _F0) / _F0 * 100
        self.assertLess(error_pct, 0.1)


# ============================================================================
# TestConstantesQuantumScaling – Clase 1
# ============================================================================

class TestConstantesQuantumScaling(unittest.TestCase):
    """Tests para ConstantesQuantumScaling."""

    def setUp(self):
        self.c = ConstantesQuantumScaling()

    def test_default_f0(self):
        """f0 por defecto = 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_default_f_schumann(self):
        """f_schumann por defecto = 7.83 Hz."""
        self.assertAlmostEqual(self.c.f_schumann, 7.83, places=4)

    def test_default_k(self):
        """k por defecto = 16."""
        self.assertEqual(self.c.k, 16)

    def test_default_c7(self):
        """c7 por defecto = 7."""
        self.assertEqual(self.c.c7, 7)

    def test_default_j(self):
        """j por defecto = 6."""
        self.assertEqual(self.c.j, 6)

    def test_default_psi_umbral(self):
        """psi_umbral por defecto = 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_k2_property(self):
        """k2 = k+2 = 18."""
        self.assertEqual(self.c.k2, 18)

    def test_nombre_property(self):
        """nombre contiene parámetros del sistema."""
        nombre = self.c.nombre
        self.assertIn("16", nombre)
        self.assertIn("6", nombre)
        self.assertIn("7", nombre)

    def test_custom_k(self):
        """Se puede instanciar con k personalizado."""
        c = ConstantesQuantumScaling(k=10)
        self.assertEqual(c.k, 10)
        self.assertEqual(c.k2, 12)

    def test_custom_c7(self):
        """Se puede instanciar con c7 personalizado."""
        c = ConstantesQuantumScaling(c7=5)
        self.assertEqual(c.c7, 5)

    def test_invalid_k_raises(self):
        """k < 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            ConstantesQuantumScaling(k=0)

    def test_invalid_c7_raises(self):
        """c7 < 3 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            ConstantesQuantumScaling(c7=2)

    def test_invalid_j_raises(self):
        """j < 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            ConstantesQuantumScaling(j=-1)

    def test_invalid_f_schumann_raises(self):
        """f_schumann ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            ConstantesQuantumScaling(f_schumann=0.0)


# ============================================================================
# TestDimensionCuantica – Clase 2
# ============================================================================

class TestDimensionCuantica(unittest.TestCase):
    """Tests para DimensionCuantica."""

    def setUp(self):
        self.d = DimensionCuantica()

    def test_dim_adelica_value(self):
        """Dimensión adélica d̃₆ ≈ 5.411."""
        self.assertAlmostEqual(self.d.dim_adelica, 5.411, places=2)

    def test_dim_adelica_formula(self):
        """d̃₆ = sin(7π/18) / sin(π/18)."""
        expected = math.sin(7 * math.pi / 18) / math.sin(math.pi / 18)
        self.assertAlmostEqual(self.d.dim_adelica, expected, places=10)

    def test_dim_kac_moody_value(self):
        """Dimensión Kac-Moody d_6 ≈ 4.411."""
        self.assertAlmostEqual(self.d.dim_kac_moody, 4.411, places=2)

    def test_dim_kac_moody_formula(self):
        """d_j = sin(13π/18) / sin(π/18)."""
        expected = math.sin(13 * math.pi / 18) / math.sin(math.pi / 18)
        self.assertAlmostEqual(self.d.dim_kac_moody, expected, places=10)

    def test_dim_adelica_positive(self):
        """La dimensión adélica debe ser positiva."""
        self.assertGreater(self.d.dim_adelica, 0.0)

    def test_dim_kac_moody_positive(self):
        """La dimensión Kac-Moody debe ser positiva."""
        self.assertGreater(self.d.dim_kac_moody, 0.0)

    def test_custom_k_changes_dim(self):
        """Cambiar k cambia la dimensión adélica."""
        c_other = ConstantesQuantumScaling(k=8)
        d_other = DimensionCuantica(c_other)
        self.assertNotAlmostEqual(d_other.dim_adelica, self.d.dim_adelica, places=2)


# ============================================================================
# TestPesoConforme – Clase 3
# ============================================================================

class TestPesoConforme(unittest.TestCase):
    """Tests para PesoConforme."""

    def setUp(self):
        self.p = PesoConforme()

    def test_h_j_value(self):
        """h_j = j(j+1)/(k+2) = 42/18 = 7/3."""
        self.assertAlmostEqual(self.p.h_j, 7.0 / 3.0, places=10)

    def test_doble_peso(self):
        """2·h_j = 14/3."""
        self.assertAlmostEqual(self.p.doble_peso, 14.0 / 3.0, places=10)

    def test_numerador(self):
        """Numerador j(j+1) = 42."""
        self.assertEqual(self.p.numerador, 42)

    def test_denominador(self):
        """Denominador k+2 = 18."""
        self.assertEqual(self.p.denominador, 18)

    def test_h_j_positive(self):
        """h_j debe ser positivo."""
        self.assertGreater(self.p.h_j, 0.0)

    def test_custom_j(self):
        """h_j con j=1, k=16: h = 2/18 = 1/9."""
        c = ConstantesQuantumScaling(j=1)
        p = PesoConforme(c)
        self.assertAlmostEqual(p.h_j, 2.0 / 18.0, places=10)


# ============================================================================
# TestFactorEscalaAdelica – Clase 4
# ============================================================================

class TestFactorEscalaAdelica(unittest.TestCase):
    """Tests para FactorEscalaAdelica."""

    def setUp(self):
        self.fa = FactorEscalaAdelica()

    def test_escala_value(self):
        """Escala ≈ 2.507."""
        self.assertAlmostEqual(self.fa.escala, 2.507, places=2)

    def test_escala_formula(self):
        """escala = √23 / 7^(1/3)."""
        expected = math.sqrt(23) / (7 ** (1.0 / 3.0))
        self.assertAlmostEqual(self.fa.escala, expected, places=10)

    def test_k_mas_c7(self):
        """k + c7 = 23."""
        self.assertEqual(self.fa.k_mas_c7, 23)

    def test_raiz_cuadrada(self):
        """√(k+c7) = √23."""
        self.assertAlmostEqual(self.fa.raiz_cuadrada, math.sqrt(23), places=10)

    def test_raiz_cubica_c7(self):
        """c7^(1/3) = 7^(1/3)."""
        self.assertAlmostEqual(self.fa.raiz_cubica_c7, 7 ** (1.0 / 3.0), places=10)

    def test_escala_positive(self):
        """La escala debe ser positiva."""
        self.assertGreater(self.fa.escala, 0.0)


# ============================================================================
# TestAcoplamientoQuiral – Clase 5
# ============================================================================

class TestAcoplamientoQuiral(unittest.TestCase):
    """Tests para AcoplamientoQuiral."""

    def setUp(self):
        self.aq = AcoplamientoQuiral()

    def test_acoplamiento_value(self):
        """Acoplamiento = 4/3."""
        self.assertAlmostEqual(self.aq.acoplamiento, 4.0 / 3.0, places=10)

    def test_acoplamiento_formula(self):
        """(c7²−1)/(2*(k+2)) = 48/36 = 4/3."""
        self.assertAlmostEqual(self.aq.acoplamiento, 48.0 / 36.0, places=10)

    def test_numerador(self):
        """Numerador c7²−1 = 48."""
        self.assertEqual(self.aq.numerador, 48)

    def test_denominador(self):
        """Denominador 2*(k+2) = 36."""
        self.assertEqual(self.aq.denominador, 36)

    def test_es_cuatro_tercios(self):
        """El acoplamiento debe ser exactamente 4/3."""
        self.assertTrue(self.aq.es_cuatro_tercios)

    def test_acoplamiento_positive(self):
        """El acoplamiento debe ser positivo."""
        self.assertGreater(self.aq.acoplamiento, 0.0)

    def test_custom_c7_changes_acoplamiento(self):
        """Cambiar c7 cambia el acoplamiento."""
        c = ConstantesQuantumScaling(c7=5)
        aq = AcoplamientoQuiral(c)
        # (25-1)/(2*18) = 24/36 = 2/3
        self.assertAlmostEqual(aq.acoplamiento, 2.0 / 3.0, places=10)


# ============================================================================
# TestRutaTransmisionSchumann – Clase 6
# ============================================================================

class TestRutaTransmisionSchumann(unittest.TestCase):
    """Tests para RutaTransmisionSchumann."""

    def setUp(self):
        self.ruta = RutaTransmisionSchumann()

    def test_f2_hz_value(self):
        """f₂ ≈ 141.64 Hz."""
        self.assertAlmostEqual(self.ruta.f2_hz, 141.64, delta=0.10)

    def test_f2_hz_positive(self):
        """f₂ debe ser positivo."""
        self.assertGreater(self.ruta.f2_hz, 0.0)

    def test_error_relativo(self):
        """Error relativo debe ser < 0.001 (0.1%)."""
        self.assertLess(self.ruta.error_relativo, 0.001)

    def test_error_porcentual(self):
        """Error porcentual debe ser < 0.1%."""
        self.assertLess(self.ruta.error_porcentual, 0.1)

    def test_es_ley_de_escala(self):
        """La ruta estándar debe satisfacer la Ley de Escala."""
        self.assertTrue(self.ruta.es_ley_de_escala)

    def test_f2_close_to_f0(self):
        """f₂ debe estar a menos de 1 Hz de F₀."""
        self.assertAlmostEqual(self.ruta.f2_hz, 141.7001, delta=1.0)

    def test_f2_formula_manual(self):
        """Verificación manual de la fórmula completa."""
        f_s = 7.83
        k, c7 = 16, 7
        k2 = k + 2
        dim = math.sin(c7 * math.pi / k2) / math.sin(math.pi / k2)
        escala = math.sqrt(k + c7) / (c7 ** (1.0 / 3.0))
        acop = (c7**2 - 1) / (2 * k2)
        f2_manual = f_s * dim * escala * acop
        self.assertAlmostEqual(self.ruta.f2_hz, f2_manual, places=10)


# ============================================================================
# TestCoherenciaTopologica – Clase 7
# ============================================================================

class TestCoherenciaTopologica(unittest.TestCase):
    """Tests para CoherenciaTopologica."""

    def setUp(self):
        self.coh = CoherenciaTopologica()

    def test_psi_topologica_value(self):
        """Ψ_top ≥ 0.999."""
        self.assertGreater(self.coh.psi_topologica, 0.999)

    def test_psi_topologica_above_umbral(self):
        """Ψ_top ≥ 0.888 (umbral mínimo)."""
        self.assertGreaterEqual(self.coh.psi_topologica, 0.888)

    def test_psi_topologica_le_one(self):
        """Ψ_top ≤ 1.0."""
        self.assertLessEqual(self.coh.psi_topologica, 1.0)

    def test_sello_activo(self):
        """El sello QST∞³ debe estar activo con parámetros estándar."""
        self.assertTrue(self.coh.sello_activo)

    def test_mensaje_activo_contains_activo(self):
        """El mensaje de sello activo debe contener 'ACTIVO'."""
        self.assertIn("ACTIVO", self.coh.mensaje)

    def test_mensaje_contains_psi_value(self):
        """El mensaje debe contener el valor de Ψ_top."""
        self.assertIn("Ψ_top", self.coh.mensaje)

    def test_psi_topologica_formula(self):
        """Ψ_top = 1 − |f₂ − F₀|/F₀."""
        f0 = 141.7001
        f2 = 7.83 * _DIM_6 * _ESCALA * _ACOPLAMIENTO
        expected = 1.0 - abs(f2 - f0) / f0
        self.assertAlmostEqual(self.coh.psi_topologica, expected, places=10)


# ============================================================================
# TestSistemaQuantumScaling – Clase 8
# ============================================================================

class TestSistemaQuantumScaling(unittest.TestCase):
    """Tests para SistemaQuantumScaling."""

    def setUp(self):
        self.sistema = SistemaQuantumScaling()
        self.resultado = self.sistema.activar()

    def test_activar_returns_resultado(self):
        """activar() debe retornar ResultadoQuantumScaling."""
        self.assertIsInstance(self.resultado, ResultadoQuantumScaling)

    def test_resultado_f_schumann(self):
        """Resultado contiene f_schumann_hz = 7.83."""
        self.assertAlmostEqual(self.resultado.f_schumann_hz, 7.83, places=4)

    def test_resultado_k(self):
        """Resultado contiene k = 16."""
        self.assertEqual(self.resultado.k, 16)

    def test_resultado_c7(self):
        """Resultado contiene c7 = 7."""
        self.assertEqual(self.resultado.c7, 7)

    def test_resultado_j(self):
        """Resultado contiene j = 6."""
        self.assertEqual(self.resultado.j, 6)

    def test_resultado_dim_adelica(self):
        """Resultado dim_adelica ≈ 5.411."""
        self.assertAlmostEqual(self.resultado.dim_adelica, 5.411, places=2)

    def test_resultado_dim_kac_moody(self):
        """Resultado dim_kac_moody ≈ 4.411."""
        self.assertAlmostEqual(self.resultado.dim_kac_moody, 4.411, places=2)

    def test_resultado_h_j(self):
        """Resultado h_j = 7/3."""
        self.assertAlmostEqual(self.resultado.h_j, 7.0 / 3.0, places=10)

    def test_resultado_escala(self):
        """Resultado escala ≈ 2.507."""
        self.assertAlmostEqual(self.resultado.escala, 2.507, places=2)

    def test_resultado_acoplamiento(self):
        """Resultado acoplamiento = 4/3."""
        self.assertAlmostEqual(self.resultado.acoplamiento, 4.0 / 3.0, places=10)

    def test_resultado_f2_hz(self):
        """Resultado f2_hz ≈ 141.64 Hz."""
        self.assertAlmostEqual(self.resultado.f2_hz, 141.64, delta=0.10)

    def test_resultado_error_porcentual(self):
        """Resultado error_porcentual < 0.1%."""
        self.assertLess(self.resultado.error_porcentual, 0.1)

    def test_resultado_psi_topologica(self):
        """Resultado psi_topologica ≥ 0.999."""
        self.assertGreater(self.resultado.psi_topologica, 0.999)

    def test_resultado_sello_activo(self):
        """Resultado sello_activo = True."""
        self.assertTrue(self.resultado.sello_activo)

    def test_resultado_mensaje_activo(self):
        """Resultado mensaje contiene 'ACTIVO'."""
        self.assertIn("ACTIVO", self.resultado.mensaje)

    def test_custom_sistema(self):
        """Sistema con parámetros personalizados funciona correctamente."""
        c = ConstantesQuantumScaling(k=8, c7=5)
        s = SistemaQuantumScaling(c)
        r = s.activar()
        self.assertIsInstance(r, ResultadoQuantumScaling)
        self.assertEqual(r.k, 8)
        self.assertEqual(r.c7, 5)
        self.assertGreater(r.f2_hz, 0.0)


# ============================================================================
# TestCalcularF2Topologico – API pública
# ============================================================================

class TestCalcularF2Topologico(unittest.TestCase):
    """Tests para calcular_f2_topologico()."""

    def test_default_returns_141_hz(self):
        """Resultado por defecto ≈ 141.64 Hz."""
        f2 = calcular_f2_topologico()
        self.assertAlmostEqual(f2, 141.64, delta=0.10)

    def test_default_close_to_f0(self):
        """f₂ debe estar a menos de 1 Hz de F₀."""
        f2 = calcular_f2_topologico()
        self.assertAlmostEqual(f2, 141.7001, delta=1.0)

    def test_explicit_default_params(self):
        """Llamada explícita con k=16, c7=7 da el mismo resultado."""
        f2_default = calcular_f2_topologico()
        f2_explicit = calcular_f2_topologico(k=16, c7=7)
        self.assertAlmostEqual(f2_default, f2_explicit, places=10)

    def test_returns_positive(self):
        """El resultado debe ser positivo."""
        self.assertGreater(calcular_f2_topologico(), 0.0)

    def test_invalid_k_raises(self):
        """k=0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            calcular_f2_topologico(k=0)

    def test_invalid_c7_raises(self):
        """c7=1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            calcular_f2_topologico(c7=1)

    def test_different_k_gives_different_f2(self):
        """k diferente produce f₂ diferente."""
        f2_k16 = calcular_f2_topologico(k=16)
        f2_k8 = calcular_f2_topologico(k=8)
        self.assertNotAlmostEqual(f2_k16, f2_k8, places=2)

    def test_different_c7_gives_different_f2(self):
        """c7 diferente produce f₂ diferente."""
        f2_c7 = calcular_f2_topologico(c7=7)
        f2_c5 = calcular_f2_topologico(c7=5)
        self.assertNotAlmostEqual(f2_c7, f2_c5, places=2)

    def test_formula_consistency(self):
        """Resultado es consistente con la fórmula manual."""
        k, c7 = 16, 7
        f_s = 7.83
        k2 = k + 2
        dim = math.sin(c7 * math.pi / k2) / math.sin(math.pi / k2)
        escala = math.sqrt(k + c7) / (c7 ** (1.0 / 3.0))
        acop = (c7**2 - 1) / (2 * k2)
        f2_manual = f_s * dim * escala * acop
        self.assertAlmostEqual(calcular_f2_topologico(), f2_manual, places=10)

    def test_error_below_one_tenth_percent(self):
        """El error debe ser inferior al 0.1%."""
        f2 = calcular_f2_topologico()
        error_pct = abs(f2 - 141.7001) / 141.7001 * 100
        self.assertLess(error_pct, 0.1)


# ============================================================================
# TestQuantumScalingActivar – API pública completa
# ============================================================================

class TestQuantumScalingActivar(unittest.TestCase):
    """Tests para quantum_scaling_activar()."""

    def setUp(self):
        self.r = quantum_scaling_activar()

    def test_returns_dict(self):
        """Debe retornar un diccionario."""
        self.assertIsInstance(self.r, dict)

    def test_all_keys_present(self):
        """El diccionario debe contener todas las claves esperadas."""
        expected_keys = {
            "f_schumann_hz", "k", "c7", "j",
            "dim_adelica", "dim_kac_moody", "h_j",
            "escala", "acoplamiento",
            "f2_hz", "error_porcentual",
            "psi_topologica", "sello_activo", "mensaje",
        }
        self.assertEqual(set(self.r.keys()), expected_keys)

    def test_f_schumann_hz(self):
        """f_schumann_hz = 7.83 Hz."""
        self.assertAlmostEqual(self.r["f_schumann_hz"], 7.83, places=4)

    def test_k(self):
        """k = 16."""
        self.assertEqual(self.r["k"], 16)

    def test_c7(self):
        """c7 = 7."""
        self.assertEqual(self.r["c7"], 7)

    def test_j(self):
        """j = 6."""
        self.assertEqual(self.r["j"], 6)

    def test_dim_adelica(self):
        """dim_adelica ≈ 5.411."""
        self.assertAlmostEqual(self.r["dim_adelica"], 5.411, places=2)

    def test_dim_kac_moody(self):
        """dim_kac_moody ≈ 4.411."""
        self.assertAlmostEqual(self.r["dim_kac_moody"], 4.411, places=2)

    def test_h_j(self):
        """h_j = 7/3."""
        self.assertAlmostEqual(self.r["h_j"], 7.0 / 3.0, places=10)

    def test_escala(self):
        """escala ≈ 2.507."""
        self.assertAlmostEqual(self.r["escala"], 2.507, places=2)

    def test_acoplamiento_is_four_thirds(self):
        """acoplamiento = 4/3."""
        self.assertAlmostEqual(self.r["acoplamiento"], 4.0 / 3.0, places=10)

    def test_f2_hz_close_to_target(self):
        """f2_hz ≈ 141.64 Hz."""
        self.assertAlmostEqual(self.r["f2_hz"], 141.64, delta=0.10)

    def test_error_porcentual_small(self):
        """error_porcentual < 0.1%."""
        self.assertLess(self.r["error_porcentual"], 0.1)

    def test_psi_topologica_high(self):
        """psi_topologica ≥ 0.999."""
        self.assertGreater(self.r["psi_topologica"], 0.999)

    def test_sello_activo(self):
        """sello_activo = True."""
        self.assertTrue(self.r["sello_activo"])

    def test_mensaje_activo(self):
        """mensaje contiene 'ACTIVO'."""
        self.assertIn("ACTIVO", self.r["mensaje"])

    def test_custom_k(self):
        """Funciona con k personalizado."""
        r = quantum_scaling_activar(k=8)
        self.assertEqual(r["k"], 8)
        self.assertGreater(r["f2_hz"], 0.0)

    def test_custom_c7(self):
        """Funciona con c7 personalizado."""
        r = quantum_scaling_activar(c7=5)
        self.assertEqual(r["c7"], 5)
        self.assertGreater(r["f2_hz"], 0.0)

    def test_custom_j(self):
        """Funciona con j personalizado."""
        r = quantum_scaling_activar(j=3)
        self.assertEqual(r["j"], 3)

    def test_custom_f_schumann(self):
        """Funciona con f_schumann personalizado."""
        r = quantum_scaling_activar(f_schumann=8.0)
        self.assertAlmostEqual(r["f_schumann_hz"], 8.0, places=4)
        self.assertGreater(r["f2_hz"], 0.0)

    def test_f2_scales_with_f_schumann(self):
        """f₂ es proporcional a f_schumann."""
        r1 = quantum_scaling_activar(f_schumann=7.83)
        r2 = quantum_scaling_activar(f_schumann=15.66)
        ratio = r2["f2_hz"] / r1["f2_hz"]
        self.assertAlmostEqual(ratio, 2.0, places=8)


# ============================================================================
# TestPhysicsIntegrity – invariantes de integración
# ============================================================================

class TestPhysicsIntegrity(unittest.TestCase):
    """Tests de invariantes físicas del sistema QST∞³."""

    def test_acoplamiento_equals_four_thirds(self):
        """El acoplamiento quiral debe ser exactamente 4/3."""
        self.assertAlmostEqual(_ACOPLAMIENTO, 4.0 / 3.0, places=12)

    def test_h6_equals_seven_thirds(self):
        """El peso conforme h₆ debe ser exactamente 7/3."""
        self.assertAlmostEqual(_H6, 7.0 / 3.0, places=12)

    def test_dim_6_greater_than_5(self):
        """La dimensión adélica d̃₆ debe ser mayor que 5."""
        self.assertGreater(_DIM_6, 5.0)

    def test_dim_6_less_than_6(self):
        """La dimensión adélica d̃₆ debe ser menor que 6."""
        self.assertLess(_DIM_6, 6.0)

    def test_f2_in_141_range(self):
        """f₂ debe estar en el rango [140, 143] Hz."""
        self.assertGreater(_F2, 140.0)
        self.assertLess(_F2, 143.0)

    def test_psi_topologica_above_999(self):
        """Ψ_top debe ser ≥ 0.999."""
        self.assertGreaterEqual(_PSI_TOPOLOGICA, 0.999)

    def test_schumann_times_dim_times_scale_times_coupling_gives_141(self):
        """La fórmula completa debe producir ≈ 141 Hz."""
        result = _F_SCHUMANN * _DIM_6 * _ESCALA * _ACOPLAMIENTO
        self.assertAlmostEqual(result, 141.64, delta=0.10)

    def test_k2_plus_5_equals_23(self):
        """k+2+5 = k+7 = 23 (factor adélico del heptágono)."""
        self.assertEqual(_K2 + 5, 23)

    def test_module_constants_consistent(self):
        """Las constantes de módulo son mutuamente consistentes."""
        dim = math.sin(_C7 * math.pi / _K2) / math.sin(math.pi / _K2)
        escala = math.sqrt(_K + _C7) / (_C7 ** (1.0 / 3.0))
        acop = (_C7**2 - 1) / (2 * _K2)
        f2 = _F_SCHUMANN * dim * escala * acop
        psi = 1.0 - abs(f2 - _F0) / _F0
        self.assertAlmostEqual(_DIM_6, dim, places=10)
        self.assertAlmostEqual(_ESCALA, escala, places=10)
        self.assertAlmostEqual(_ACOPLAMIENTO, acop, places=10)
        self.assertAlmostEqual(_F2, f2, places=10)
        self.assertAlmostEqual(_PSI_TOPOLOGICA, psi, places=10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
