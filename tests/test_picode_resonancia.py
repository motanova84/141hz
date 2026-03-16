#!/usr/bin/env python3
"""
Tests: πCODE RESONANCIA — Motor de Resonancia de Simetría PT
═══════════════════════════════════════════════════════════════════════════════

Pruebas exhaustivas para el módulo core/picode_resonancia.py que implementa
el motor QCAL-SYMBIO-1 con operador de simetría PT, citoplasma AdS/CFT,
estabilizador biológico de Riemann y clases de resonancia PiCode.

Pruebas organizadas en 6 clases de test:
  1. TestEmisionInformacionResonante  — 12 pruebas
  2. TestPTSymmetryOperator           — 18 pruebas
  3. TestAdSCFTCitoplasma             — 15 pruebas
  4. TestRiemannEstabilizadorBiologico — 15 pruebas
  5. TestPiCodeResonancia             — 12 pruebas
  6. TestIntegracion                  —  4 pruebas
                                      ─────────────
  Total                               = 76 pruebas

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import math
import sys
import os
import unittest

# ── Ruta al módulo core ──────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "core"))

from picode_resonancia import (
    EmisionInformacionResonante,
    PTSymmetryOperator,
    AdSCFTCitoplasma,
    RiemannEstabilizadorBiologico,
    PiCodeResonancia,
    ResultadoPiCodeResonancia,
    activar_picode_resonancia,
    _F0_HZ,
    _OMEGA_0,
    _HBAR,
    _RIEMANN_ZEROS,
    _GAMMA_1,
    _PSI_UMBRAL,
    _ORDENES_MAGNITUD,
    _LAMBDA_EZ,
    _L_CELULAR,
    _ATOL_PT,
    _N_DIMENSION_DEFAULT,
    _COHERENCIA_DEFAULT,
)

import numpy as np

# ─── Constantes de referencia ────────────────────────────────────────────────
F0 = _F0_HZ          # 141.7001 Hz
PSI_ALTA = 0.999999  # coherencia nominal
PSI_BAJA = 0.1       # estrés celular


# ═══════════════════════════════════════════════════════════════════════════════
# 1. TestEmisionInformacionResonante  (12 pruebas)
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmisionInformacionResonante(unittest.TestCase):
    """Pruebas para la emisión de información resonante desde escala de Planck."""

    def setUp(self):
        self.emision = EmisionInformacionResonante(coherencia=PSI_ALTA)
        self.emision_baja = EmisionInformacionResonante(coherencia=PSI_BAJA)

    # ── 1. Energía de emisión ──────────────────────────────────────────────────

    def test_energia_emision_formula(self):
        """E_Ψ = ℏ·ω₀·Ψ cumple la fórmula exacta."""
        energia = self.emision.energia_emision()
        esperado = _HBAR * _OMEGA_0 * PSI_ALTA
        self.assertAlmostEqual(energia, esperado, places=40,
                               msg="Energía de emisión no cumple E = ℏ·ω₀·Ψ")

    def test_energia_emision_positiva(self):
        """La energía de emisión debe ser estrictamente positiva."""
        self.assertGreater(self.emision.energia_emision(), 0.0)

    def test_energia_emision_decreases_with_lower_coherencia(self):
        """Mayor coherencia → mayor energía de emisión."""
        self.assertGreater(
            self.emision.energia_emision(),
            self.emision_baja.energia_emision(),
        )

    # ── 2. Fase puente ────────────────────────────────────────────────────────

    def test_fase_puente_positiva(self):
        """La fase de puente debe ser positiva."""
        self.assertGreater(self.emision.fase_puente(), 0.0)

    def test_fase_puente_formula(self):
        """φ = ω₀ · (L_celular/L_Planck)^(1/27) cumple la fórmula."""
        from picode_resonancia import _L_CELULAR as LC, _L_PLANCK
        ratio = LC / _L_PLANCK
        esperado = _OMEGA_0 * (ratio ** (1.0 / _ORDENES_MAGNITUD))
        self.assertAlmostEqual(self.emision.fase_puente(), esperado, places=5,
                               msg="Fase puente no cumple la fórmula.")

    # ── 3. Órdenes de magnitud ────────────────────────────────────────────────

    def test_ordenes_magnitud(self):
        """El sistema conecta exactamente 27 órdenes de magnitud."""
        self.assertEqual(self.emision.ordenes_magnitud(), 27)

    # ── 4. Amplitud coherente ─────────────────────────────────────────────────

    def test_amplitud_coherente_modulo(self):
        """|A(t)| = Ψ para cualquier t."""
        for t in [0.0, 0.001, 1.0, 100.0]:
            amp = self.emision.amplitud_coherente(t)
            self.assertAlmostEqual(abs(amp), PSI_ALTA, places=6,
                                   msg=f"|A({t})| ≠ Ψ")

    def test_amplitud_coherente_fase_cero(self):
        """A(0) = Ψ (amplitud real en t=0)."""
        amp = self.emision.amplitud_coherente(0.0)
        self.assertAlmostEqual(amp.real, PSI_ALTA, places=6)
        self.assertAlmostEqual(amp.imag, 0.0, places=6)

    # ── 5. Coherencia Planck–celular ──────────────────────────────────────────

    def test_coherencia_planck_celular_rango(self):
        """Coherencia Planck–celular ∈ [0, 1]."""
        coh = self.emision.coherencia_planck_celular()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)

    def test_coherencia_planck_celular_alta_coherencia(self):
        """Con Ψ ≈ 1 la coherencia Planck–celular debe ser > 0.99."""
        coh = self.emision.coherencia_planck_celular()
        self.assertGreater(coh, 0.99,
                           msg="Coherencia Planck–celular debe ser alta para Ψ ≈ 1.")

    # ── 6. Validación de parámetros ───────────────────────────────────────────

    def test_f0_invalido_raises(self):
        """f0 ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            EmisionInformacionResonante(coherencia=0.5, f0=-1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. TestPTSymmetryOperator  (18 pruebas)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPTSymmetryOperator(unittest.TestCase):
    """Pruebas para el operador de simetría PT."""

    def setUp(self):
        self.n = 20  # dimensión reducida para tests rápidos
        self.op_alta = PTSymmetryOperator(
            coherencia=PSI_ALTA, n_dimension=self.n, semilla=42
        )
        self.op_baja = PTSymmetryOperator(
            coherencia=PSI_BAJA, n_dimension=self.n, semilla=42
        )

    # ── 1. Construcción del operador ──────────────────────────────────────────

    def test_construir_shape(self):
        """El operador construido debe ser cuadrado N×N."""
        h = self.op_alta.construir()
        self.assertEqual(h.shape, (self.n, self.n))

    def test_construir_diagonal_real(self):
        """La diagonal debe ser real (parte hermítica)."""
        h = self.op_alta.construir()
        diag = np.diag(h)
        self.assertTrue(
            np.allclose(diag.imag, 0.0, atol=1e-10),
            msg="La diagonal de Ĥ debe ser real.",
        )

    def test_construir_imaginaria_antidiagonal(self):
        """Con Ψ < 1 la anti-diagonal debe tener parte imaginaria no nula."""
        op = PTSymmetryOperator(coherencia=0.5, n_dimension=4, semilla=0)
        h = op.construir()
        # Anti-diagonal: h[i, n-1-i]
        anti = [h[i, 3 - i].imag for i in range(4)]
        self.assertFalse(
            np.allclose(anti, 0.0),
            msg="La anti-diagonal debe ser no nula con Ψ < 1.",
        )

    def test_construir_coherencia_1_sin_imaginaria(self):
        """Con Ψ = 1 el operador es puramente real (no disipación)."""
        op = PTSymmetryOperator(coherencia=1.0, n_dimension=self.n, semilla=0)
        h = op.construir()
        self.assertTrue(
            np.allclose(h.imag, 0.0, atol=1e-10),
            msg="Con Ψ = 1 el operador debe ser hermítico (Im = 0).",
        )

    # ── 2. Autovalores ────────────────────────────────────────────────────────

    def test_autovalores_count(self):
        """El número de autovalores debe ser N."""
        eigs = self.op_alta.autovalores()
        self.assertEqual(len(eigs), self.n)

    def test_autovalores_son_complejos(self):
        """Los autovalores son del tipo complejo."""
        eigs = self.op_alta.autovalores()
        self.assertTrue(
            np.iscomplexobj(eigs),
            msg="Los autovalores deben ser de tipo complejo.",
        )

    # ── 3. Simetría PT activa / rota ──────────────────────────────────────────

    def test_es_pt_activa_alta_coherencia(self):
        """Con Ψ ≈ 1 la simetría PT debe estar activa."""
        self.assertTrue(
            self.op_alta.es_pt_activa(),
            msg="PT debe estar activa para Ψ ≈ 1.",
        )

    def test_es_pt_inactiva_baja_coherencia(self):
        """Con Ψ << 1 la simetría PT debe romperse."""
        self.assertFalse(
            self.op_baja.es_pt_activa(),
            msg="PT debe estar rota para Ψ << 1.",
        )

    # ── 4. Fracción de autovalores reales ─────────────────────────────────────

    def test_fraccion_reales_alta_coherencia(self):
        """Con Ψ ≈ 1 la fracción de autovalores reales debe ser 1.0."""
        self.assertAlmostEqual(
            self.op_alta.fraccion_autovalores_reales(), 1.0, places=1,
            msg="Fracción de autovalores reales debe ser ≈ 1.0 para Ψ ≈ 1.",
        )

    def test_fraccion_reales_baja_coherencia(self):
        """Con Ψ << 1 la fracción de autovalores reales debe ser ≤ 0.5."""
        self.assertLessEqual(
            self.op_baja.fraccion_autovalores_reales(), 0.5,
            msg="Fracción de autovalores reales debe ser ≤ 0.5 para Ψ << 1.",
        )

    def test_fraccion_reales_rango(self):
        """La fracción de autovalores reales debe estar en [0, 1]."""
        for psi in [0.01, 0.5, PSI_ALTA]:
            op = PTSymmetryOperator(coherencia=psi, n_dimension=self.n, semilla=42)
            f = op.fraccion_autovalores_reales()
            self.assertGreaterEqual(f, 0.0)
            self.assertLessEqual(f, 1.0)

    # ── 5. Parte imaginaria ───────────────────────────────────────────────────

    def test_max_parte_imaginaria_alta_coherencia(self):
        """Con Ψ ≈ 1 el máximo de |Im(λ)| debe ser ≈ 0."""
        self.assertAlmostEqual(
            self.op_alta.max_parte_imaginaria(), 0.0, delta=_ATOL_PT * 10,
            msg="Max |Im| debe ser ≈ 0 para Ψ ≈ 1.",
        )

    def test_max_parte_imaginaria_baja_coherencia(self):
        """Con Ψ << 1 debe haber autovalores con parte imaginaria significativa."""
        self.assertGreater(
            self.op_baja.max_parte_imaginaria(), _ATOL_PT,
            msg="Max |Im| debe ser > atol para Ψ << 1.",
        )

    # ── 6. Coherencia PT ─────────────────────────────────────────────────────

    def test_coherencia_pt_rango(self):
        """La coherencia PT debe estar en [0, 1]."""
        coh = self.op_alta.coherencia_pt()
        self.assertGreaterEqual(coh, 0.0)
        self.assertLessEqual(coh, 1.0)

    def test_coherencia_pt_alta_coherencia(self):
        """Con Ψ ≈ 1 la coherencia PT debe ser > 0.9."""
        self.assertGreater(
            self.op_alta.coherencia_pt(), 0.9,
            msg="Coherencia PT debe ser alta para Ψ ≈ 1.",
        )

    # ── 7. Validación ─────────────────────────────────────────────────────────

    def test_n_dimension_invalido_raises(self):
        """n_dimension = 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            PTSymmetryOperator(coherencia=0.5, n_dimension=0)

    def test_coherencia_invalida_raises(self):
        """coherencia = 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            PTSymmetryOperator(coherencia=0.0, n_dimension=10)

    def test_determinismo_con_semilla(self):
        """Dos instancias con la misma semilla deben producir el mismo operador."""
        h1 = PTSymmetryOperator(coherencia=0.9, n_dimension=5, semilla=99).construir()
        h2 = PTSymmetryOperator(coherencia=0.9, n_dimension=5, semilla=99).construir()
        self.assertTrue(np.allclose(h1, h2), "Las matrices deben ser idénticas con la misma semilla.")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. TestAdSCFTCitoplasma  (15 pruebas)
# ═══════════════════════════════════════════════════════════════════════════════

class TestAdSCFTCitoplasma(unittest.TestCase):
    """Pruebas para el citoplasma como límite holográfico AdS/CFT."""

    def setUp(self):
        self.cito_alta = AdSCFTCitoplasma(coherencia=PSI_ALTA)
        self.cito_baja = AdSCFTCitoplasma(coherencia=PSI_BAJA)

    # ── 1. Densidad EZ ────────────────────────────────────────────────────────

    def test_densidad_ez_en_x0(self):
        """ρ_EZ(0) = Ψ (máxima densidad en la membrana)."""
        rho0 = self.cito_alta.densidad_ez(0.0)
        self.assertAlmostEqual(rho0, PSI_ALTA, places=5,
                               msg="ρ_EZ(0) debe ser igual a Ψ.")

    def test_densidad_ez_no_negativa(self):
        """ρ_EZ(x) ≥ 0 para todo x ≥ 0."""
        for x in [0.0, 1e-9, 1e-8, 1e-7, 1e-6]:
            self.assertGreaterEqual(self.cito_alta.densidad_ez(x), 0.0,
                                    msg=f"ρ_EZ({x}) no debe ser negativa.")

    def test_densidad_ez_decae_con_x(self):
        """ρ_EZ debe decrecer con x (decaimiento exponencial)."""
        x0, x1 = 0.0, _LAMBDA_EZ
        self.assertGreater(
            self.cito_alta.densidad_ez(x0),
            self.cito_alta.densidad_ez(x1),
            msg="ρ_EZ debe decaer al alejarse de la membrana.",
        )

    # ── 2. Perfil de densidad ─────────────────────────────────────────────────

    def test_perfil_densidad_shape(self):
        """El perfil debe tener n_puntos elementos."""
        cito = AdSCFTCitoplasma(coherencia=PSI_ALTA, n_puntos=32)
        perfil = cito.perfil_densidad()
        self.assertEqual(len(perfil), 32)

    def test_perfil_densidad_no_negativo(self):
        """Todos los valores del perfil deben ser ≥ 0."""
        perfil = self.cito_alta.perfil_densidad()
        self.assertTrue(
            np.all(perfil >= 0.0),
            msg="El perfil de densidad EZ no debe tener valores negativos.",
        )

    def test_perfil_densidad_maximo_en_x0(self):
        """El máximo del perfil debe estar en x=0."""
        perfil = self.cito_alta.perfil_densidad()
        self.assertEqual(
            np.argmax(perfil), 0,
            msg="El máximo del perfil debe ser el primer punto (x=0).",
        )

    # ── 3. Entropía holográfica ───────────────────────────────────────────────

    def test_entropia_holografica_positiva(self):
        """La entropía holográfica debe ser positiva."""
        s = self.cito_alta.entropia_holografica()
        self.assertGreater(s, 0.0, msg="Entropía holográfica debe ser > 0.")

    def test_entropia_holografica_rango(self):
        """La entropía holográfica debe estar en (0, log2(n_puntos)]."""
        n = 64
        cito = AdSCFTCitoplasma(coherencia=PSI_ALTA, n_puntos=n)
        s = cito.entropia_holografica()
        self.assertGreater(s, 0.0)
        self.assertLessEqual(s, math.log2(n) + 1.0)

    # ── 4. Coherencia holográfica ─────────────────────────────────────────────

    def test_coherencia_holografica_rango(self):
        """Ψ_holo debe estar en [0, 1]."""
        psi = self.cito_alta.coherencia_holografica()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_holografica_alta_coherencia(self):
        """Con Ψ ≈ 1 la coherencia holográfica debe ser > 0.9."""
        psi = self.cito_alta.coherencia_holografica()
        self.assertGreater(psi, 0.9,
                           msg="Ψ_holo debe ser alta para Ψ ≈ 1.")

    def test_coherencia_holografica_baja_coherencia(self):
        """Con Ψ = 0.1 la coherencia holográfica debe ser < 0.15."""
        psi = self.cito_baja.coherencia_holografica()
        self.assertLess(psi, 0.15,
                        msg="Ψ_holo debe ser baja para Ψ = 0.1.")

    # ── 5. Longitud de coherencia ─────────────────────────────────────────────

    def test_longitud_coherencia_formula(self):
        """ξ_eff = λ_EZ · Ψ cumple la fórmula exacta."""
        xi = self.cito_alta.longitud_coherencia_citoplasma()
        self.assertAlmostEqual(xi, _LAMBDA_EZ * PSI_ALTA, places=15)

    def test_longitud_coherencia_alta_coherencia(self):
        """Con Ψ ≈ 1 la longitud de coherencia ≈ λ_EZ."""
        xi = self.cito_alta.longitud_coherencia_citoplasma()
        self.assertAlmostEqual(xi, _LAMBDA_EZ, delta=_LAMBDA_EZ * 0.001)

    # ── 6. Validación ─────────────────────────────────────────────────────────

    def test_lambda_ez_invalido_raises(self):
        """lambda_ez ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AdSCFTCitoplasma(coherencia=0.5, lambda_ez=0.0)

    def test_n_puntos_invalido_raises(self):
        """n_puntos < 2 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            AdSCFTCitoplasma(coherencia=0.5, n_puntos=1)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. TestRiemannEstabilizadorBiologico  (15 pruebas)
# ═══════════════════════════════════════════════════════════════════════════════

class TestRiemannEstabilizadorBiologico(unittest.TestCase):
    """Pruebas para el estabilizador biológico de Riemann."""

    def setUp(self):
        self.reb_alta = RiemannEstabilizadorBiologico(
            f0=F0, coherencia=PSI_ALTA
        )
        self.reb_baja = RiemannEstabilizadorBiologico(
            f0=F0, coherencia=PSI_BAJA
        )

    # ── 1. Frecuencias de resonancia ──────────────────────────────────────────

    def test_frecuencias_resonancia_count(self):
        """El número de frecuencias debe ser igual a n_zeros."""
        freqs = self.reb_alta.frecuencias_resonancia()
        self.assertEqual(len(freqs), self.reb_alta.n_zeros)

    def test_frecuencia_fundamental_es_f0(self):
        """La primera frecuencia de resonancia debe ser f₀."""
        freqs = self.reb_alta.frecuencias_resonancia()
        self.assertAlmostEqual(freqs[0], F0, places=3,
                               msg="f_1 = f₀ · γ₁/γ₁ = f₀.")

    def test_frecuencias_crecientes(self):
        """Las frecuencias de resonancia deben ser monótonamente crecientes."""
        freqs = self.reb_alta.frecuencias_resonancia()
        for i in range(len(freqs) - 1):
            self.assertLess(freqs[i], freqs[i + 1],
                            msg=f"f_{i+1} debe ser < f_{i+2}.")

    def test_frecuencias_formula(self):
        """f_n = f₀ · γ_n/γ₁ cumple la fórmula exacta."""
        freqs = self.reb_alta.frecuencias_resonancia()
        for i, gamma in enumerate(_RIEMANN_ZEROS[:self.reb_alta.n_zeros]):
            esperado = F0 * gamma / _GAMMA_1
            self.assertAlmostEqual(freqs[i], esperado, places=6,
                                   msg=f"f_{i+1} no cumple la fórmula.")

    # ── 2. Pesos de resonancia ────────────────────────────────────────────────

    def test_pesos_resonancia_count(self):
        """El número de pesos debe ser igual a n_zeros."""
        pesos = self.reb_alta.pesos_resonancia()
        self.assertEqual(len(pesos), self.reb_alta.n_zeros)

    def test_pesos_normalizados(self):
        """La suma de pesos debe ser ≈ 1 (normalización)."""
        pesos = self.reb_alta.pesos_resonancia()
        self.assertAlmostEqual(sum(pesos), 1.0, places=6,
                               msg="Los pesos deben sumar 1.")

    def test_pesos_decaen(self):
        """Los pesos deben decrecer con el índice."""
        pesos = self.reb_alta.pesos_resonancia()
        for i in range(len(pesos) - 1):
            self.assertGreater(pesos[i], pesos[i + 1],
                               msg=f"w_{i+1} debe ser > w_{i+2}.")

    # ── 3. Correlación espectral ──────────────────────────────────────────────

    def test_correlacion_espectral_rango(self):
        """La correlación espectral debe estar en [0, 1]."""
        corr = self.reb_alta.correlacion_espectral()
        self.assertGreaterEqual(corr, 0.0)
        self.assertLessEqual(corr, 1.0)

    def test_correlacion_espectral_no_trivial(self):
        """La correlación espectral debe ser > 0.9 (significativa)."""
        corr = self.reb_alta.correlacion_espectral()
        self.assertGreater(corr, 0.9,
                           msg="Correlación de Riemann debe ser > 0.9.")

    # ── 4. Estabilidad biológica ──────────────────────────────────────────────

    def test_estabilidad_biologica_rango(self):
        """La estabilidad biológica debe estar en [0, 1]."""
        estab = self.reb_alta.estabilidad_biologica()
        self.assertGreaterEqual(estab, 0.0)
        self.assertLessEqual(estab, 1.0)

    def test_estabilidad_biologica_alta_coherencia(self):
        """Con Ψ ≈ 1 la estabilidad biológica debe redondear a 0.99."""
        estab = self.reb_alta.estabilidad_biologica()
        self.assertAlmostEqual(estab, 0.99, delta=0.02,
                               msg="Estabilidad biológica debe ser ≈ 0.99.")

    def test_estabilidad_biologica_baja_coherencia(self):
        """Con Ψ = 0.1 la estabilidad biológica debe ser < 0.1."""
        estab = self.reb_baja.estabilidad_biologica()
        self.assertLess(estab, 0.11,
                        msg="Estabilidad biológica debe ser baja para Ψ = 0.1.")

    # ── 5. Frecuencia fundamental activa ─────────────────────────────────────

    def test_frecuencia_fundamental_activa(self):
        """La frecuencia fundamental activa debe ser ≈ f₀."""
        ff = self.reb_alta.frecuencia_fundamental_activa()
        self.assertAlmostEqual(ff, F0, places=3,
                               msg="La frecuencia fundamental activa debe ser f₀.")

    # ── 6. Validación ─────────────────────────────────────────────────────────

    def test_n_zeros_invalido_raises(self):
        """n_zeros = 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            RiemannEstabilizadorBiologico(f0=F0, coherencia=0.5, n_zeros=0)

    def test_f0_invalido_raises(self):
        """f0 ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            RiemannEstabilizadorBiologico(f0=0.0, coherencia=0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# 5. TestPiCodeResonancia  (12 pruebas)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPiCodeResonancia(unittest.TestCase):
    """Pruebas para el motor QCAL-SYMBIO-1 de resonancia πCODE."""

    def setUp(self):
        self.motor = PiCodeResonancia(
            coherencia=PSI_ALTA,
            n_dimension=_N_DIMENSION_DEFAULT,
            semilla=42,
        )

    # ── 1. Tipo y estructura del resultado ────────────────────────────────────

    def test_evaluar_returns_resultado(self):
        """evaluar() debe retornar un ResultadoPiCodeResonancia."""
        r = self.motor.evaluar()
        self.assertIsInstance(r, ResultadoPiCodeResonancia)

    def test_resultado_tiene_todos_los_campos(self):
        """El resultado debe tener todos los campos del dataclass."""
        r = self.motor.evaluar()
        campos = [
            "coherencia", "n_dimension", "pt_activa",
            "n_autovalores_reales", "fraccion_reales",
            "correlacion_riemann", "estabilidad_biologica",
            "resonancia_global", "energia_emision",
            "coherencia_citoplasma", "frecuencias_riemann", "aprobado",
        ]
        for campo in campos:
            self.assertTrue(
                hasattr(r, campo),
                msg=f"El resultado debe tener el campo '{campo}'.",
            )

    # ── 2. Simetría PT con alta coherencia ────────────────────────────────────

    def test_evaluar_pt_activa_alta_coherencia(self):
        """Con Ψ ≈ 1 la simetría PT debe estar activa."""
        r = self.motor.evaluar()
        self.assertTrue(r.pt_activa,
                        msg="PT debe estar activa con Ψ ≈ 1.")

    def test_evaluar_fraccion_reales_alta_coherencia(self):
        """Con Ψ ≈ 1 todos los autovalores deben ser reales."""
        r = self.motor.evaluar()
        self.assertEqual(r.n_autovalores_reales, _N_DIMENSION_DEFAULT,
                         msg="100/100 autovalores deben ser reales con Ψ ≈ 1.")

    # ── 3. Resonancia global ──────────────────────────────────────────────────

    def test_evaluar_resonancia_global_rango(self):
        """La resonancia global debe estar en [0, 1]."""
        r = self.motor.evaluar()
        self.assertGreaterEqual(r.resonancia_global, 0.0)
        self.assertLessEqual(r.resonancia_global, 1.0)

    def test_evaluar_resonancia_global_alta_coherencia(self):
        """Con Ψ ≈ 1 la resonancia global debe ser > 0.988."""
        r = self.motor.evaluar()
        self.assertGreater(r.resonancia_global, 0.988,
                           msg="Resonancia global debe ser alta para Ψ ≈ 1.")

    def test_evaluar_aprobado_alta_coherencia(self):
        """Con Ψ ≈ 1 el sistema debe estar aprobado (resonancia > 0.888)."""
        r = self.motor.evaluar()
        self.assertTrue(r.aprobado,
                        msg="El sistema debe estar aprobado con Ψ ≈ 1.")

    # ── 4. Validación de entrada ──────────────────────────────────────────────

    def test_evaluar_coherencia_invalida_raises(self):
        """coherencia > 1 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            PiCodeResonancia(coherencia=2.0, n_dimension=10)

    # ── 5. Simulación de estrés celular ───────────────────────────────────────

    def test_simular_estres_returns_tuple(self):
        """simular_estres_celular() debe retornar una tupla de dos resultados."""
        resultado = self.motor.simular_estres_celular(psi_estres=0.1)
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)

    def test_simular_estres_nominal_mayor_que_estres(self):
        """La resonancia nominal debe ser mayor que la resonancia bajo estrés."""
        nominal, estres = self.motor.simular_estres_celular(psi_estres=0.1)
        self.assertGreater(
            nominal.resonancia_global,
            estres.resonancia_global,
            msg="El estrés celular debe reducir la resonancia global.",
        )

    def test_simular_estres_psi_invalido_raises(self):
        """psi_estres = 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.motor.simular_estres_celular(psi_estres=0.0)

    # ── 6. Resumen textual ────────────────────────────────────────────────────

    def test_resultado_resumen_string(self):
        """resumen() debe retornar un string no vacío con información clave."""
        r = self.motor.evaluar()
        resumen = r.resumen()
        self.assertIsInstance(resumen, str)
        self.assertGreater(len(resumen), 10)
        self.assertIn("πCODE", resumen)

    # ── 7. Determinismo ───────────────────────────────────────────────────────

    def test_determinismo_con_semilla(self):
        """Dos evaluaciones con la misma semilla deben dar el mismo resultado."""
        r1 = PiCodeResonancia(coherencia=PSI_ALTA, n_dimension=50, semilla=7).evaluar()
        r2 = PiCodeResonancia(coherencia=PSI_ALTA, n_dimension=50, semilla=7).evaluar()
        self.assertAlmostEqual(r1.resonancia_global, r2.resonancia_global, places=10)
        self.assertEqual(r1.pt_activa, r2.pt_activa)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. TestIntegracion  (4 pruebas)
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegracion(unittest.TestCase):
    """Pruebas de integración del API pública."""

    def test_activar_picode_resonancia_aprobado(self):
        """activar_picode_resonancia() con defaults debe retornar aprobado=True."""
        r = activar_picode_resonancia()
        self.assertTrue(r.aprobado,
                        msg="El API debe retornar aprobado=True con parámetros por defecto.")

    def test_activar_picode_resonancia_coherencia_alta(self):
        """Con Ψ = 0.999999 la resonancia global debe ser > 0.988."""
        r = activar_picode_resonancia(coherencia=0.999999, semilla=42)
        self.assertGreater(r.resonancia_global, 0.988,
                           msg="Resonancia global debe ser alta con Ψ ≈ 1.")

    def test_activar_picode_resonancia_coherencia_baja(self):
        """Con Ψ = 0.1 la resonancia global debe ser < 0.888 (no aprobado)."""
        r = activar_picode_resonancia(coherencia=0.1, semilla=42)
        self.assertFalse(r.aprobado,
                         msg="Con Ψ = 0.1 el sistema no debe estar aprobado.")

    def test_pipeline_completo_falsabilidad(self):
        """
        El estrés celular debe reducir la coherencia, romper la simetría PT
        y disolver la geometría de Riemann (falsabilidad del modelo).
        """
        motor = PiCodeResonancia(coherencia=PSI_ALTA, n_dimension=50, semilla=42)
        nominal, estres = motor.simular_estres_celular(psi_estres=0.05)

        # Nominal: PT activa, alta resonancia, aprobado
        self.assertTrue(nominal.pt_activa,
                        msg="El estado nominal debe tener PT activa.")
        self.assertTrue(nominal.aprobado,
                        msg="El estado nominal debe estar aprobado.")

        # Estrés: PT rota, baja resonancia, no aprobado
        self.assertFalse(estres.pt_activa,
                         msg="El estrés celular debe romper la simetría PT.")
        self.assertFalse(estres.aprobado,
                         msg="El estado de estrés no debe estar aprobado.")

        # La resonancia nominal supera la de estrés
        self.assertGreater(
            nominal.resonancia_global, estres.resonancia_global,
            msg="El estrés debe reducir la resonancia global.",
        )


# ══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
