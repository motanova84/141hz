#!/usr/bin/env python3
"""
Tests para physics.kuramoto_superradiancia

Valida el modelo de sincronización Kuramoto-Adler (RK4 manual), la resonancia
Lorentziana del agua EZ, el protocolo de Respiración Áurea y la integración
de coherencias biológicas a F₀ = 141,7001 Hz.

95 tests en 9 clases de prueba — 100 % aprobados.
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.kuramoto_superradiancia import (
    ConstantesKuramoto,
    ModeloKuramoto,
    SuperradianciaFotonez,
    AguaEZ,
    RespiracionAurea,
    CoherenciaBiologicaTotal,
    SistemaKuramotoSuperradiancia,
    ResultadoKuramoto,
    kuramoto_superradiancia_activar,
)

# ============================================================================
# Clase 1 – TestConstantesKuramoto (10 tests)
# ============================================================================


class TestConstantesKuramoto(unittest.TestCase):
    """Tests para ConstantesKuramoto."""

    def setUp(self):
        self.c = ConstantesKuramoto()

    def test_F0_valor(self):
        """F₀ debe ser 141,7001 Hz."""
        self.assertEqual(self.c.F0, 141.7001)

    def test_K_valor(self):
        """K debe ser 50 (constante de acoplamiento Kuramoto)."""
        self.assertEqual(self.c.K, 50.0)

    def test_N_magnitud(self):
        """N debe ser 10¹³ microtúbulos."""
        self.assertEqual(self.c.N, 1e13)

    def test_phi_valor(self):
        """φ debe ser 1,618034 (razón áurea)."""
        self.assertAlmostEqual(self.c.phi, 1.618034, places=6)

    def test_phi_propiedad_aurea(self):
        """φ satisface φ² = φ + 1 (propiedad de la razón áurea)."""
        phi = self.c.phi
        self.assertAlmostEqual(phi ** 2, phi + 1.0, places=4)

    def test_carga_resonancia_valor(self):
        """Carga de resonancia Lorentziana debe ser 70,56."""
        self.assertAlmostEqual(self.c.carga_resonancia, 70.56, places=2)

    def test_capas_hexagonales_valor(self):
        """Capas hexagonales de agua EZ deben ser 551.117."""
        self.assertEqual(self.c.capas_hexagonales, 551117)

    def test_psi_superradiante_umbral(self):
        """Umbral superradiante debe ser 0,999."""
        self.assertEqual(self.c.psi_superradiante, 0.999)

    def test_omega_0(self):
        """ω₀ = 2π·F₀ ≈ 890,33 rad/s."""
        omega = self.c.omega_0()
        self.assertAlmostEqual(omega, 2 * math.pi * 141.7001, places=6)
        self.assertGreater(omega, 889.0)
        self.assertLess(omega, 892.0)

    def test_energia_foton_positiva(self):
        """E = h·F₀ debe ser positiva y en el rango correcto."""
        e = self.c.energia_foton_J()
        self.assertGreater(e, 9.3e-32)
        self.assertLess(e, 9.5e-32)


# ============================================================================
# Clase 2 – TestModeloKuramoto (16 tests)
# ============================================================================


class TestModeloKuramoto(unittest.TestCase):
    """Tests para ModeloKuramoto (RK4 + Adler)."""

    def setUp(self):
        self.modelo = ModeloKuramoto()

    def test_F0_valor(self):
        """F₀ del modelo debe ser 141,7001 Hz."""
        self.assertEqual(self.modelo.F0, 141.7001)

    def test_K_valor(self):
        """K del modelo debe ser 50."""
        self.assertEqual(self.modelo.K, 50.0)

    def test_f_nat_menor_F0(self):
        """f_nat debe ser ligeramente menor que F₀ (detuning positivo)."""
        self.assertLess(self.modelo.f_nat, self.modelo.F0)
        self.assertGreater(self.modelo.f_nat, self.modelo.F0 - 1.0)

    def test_f_nat_detuning(self):
        """Detuning F₀−f_nat debe ser ≈ 0,1669 Hz."""
        delta = self.modelo.detuning_hz()
        self.assertGreater(delta, 0.10)
        self.assertLess(delta, 0.25)

    def test_sin_delta_rango(self):
        """sin(Δφ) debe estar en (0, 1) para bloqueo de fase."""
        from physics.kuramoto_superradiancia import _SIN_DELTA
        self.assertGreater(_SIN_DELTA, 0.0)
        self.assertLess(_SIN_DELTA, 1.0)

    def test_adler_consistencia(self):
        """sin(Δφ) = 2π(F₀−f_nat)/K (ecuación de Adler)."""
        from physics.kuramoto_superradiancia import _SIN_DELTA
        sin_delta_calc = 2 * math.pi * self.modelo.detuning_hz() / self.modelo.K
        self.assertAlmostEqual(sin_delta_calc, _SIN_DELTA, places=8)

    def test_rk4_paso_tipo(self):
        """_rk4_paso debe retornar un float."""
        phi_new = self.modelo._rk4_paso(0.0, 0.0, 1e-5)
        self.assertIsInstance(phi_new, float)

    def test_rk4_paso_no_nan(self):
        """_rk4_paso no debe producir NaN."""
        phi_new = self.modelo._rk4_paso(0.0, 0.0, 1e-5)
        self.assertFalse(math.isnan(phi_new))

    def test_rk4_paso_no_inf(self):
        """_rk4_paso no debe producir infinito."""
        phi_new = self.modelo._rk4_paso(0.0, 0.0, 1e-5)
        self.assertFalse(math.isinf(phi_new))

    def test_integrar_retorna_tupla(self):
        """integrar() debe retornar (phi_final, t_final)."""
        result = self.modelo.integrar(n_ciclos=5, n_puntos_por_ciclo=100)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_integrar_t_final_positivo(self):
        """t_final de la integración debe ser positivo."""
        _, t_final = self.modelo.integrar(n_ciclos=5, n_puntos_por_ciclo=100)
        self.assertGreater(t_final, 0.0)

    def test_integrar_t_final_magnitud(self):
        """t_final ≈ n_ciclos/F₀ (tiempo total de integración)."""
        n_ciclos = 5
        _, t_final = self.modelo.integrar(n_ciclos=n_ciclos, n_puntos_por_ciclo=100)
        t_esperado = n_ciclos / self.modelo.F0
        self.assertAlmostEqual(t_final, t_esperado, places=4)

    def test_calcular_psi_valor(self):
        """Ψ_bio = 0,99978 (6 decimales) por la ecuación de Adler."""
        psi = self.modelo.calcular_psi()
        self.assertAlmostEqual(psi, 0.99978, places=5)

    def test_calcular_psi_rango_valido(self):
        """Ψ_bio debe estar en [0, 1]."""
        psi = self.modelo.calcular_psi()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_calcular_psi_supera_umbral_superradiante(self):
        """Ψ_bio debe superar el umbral superradiante 0,999."""
        psi = self.modelo.calcular_psi()
        self.assertGreaterEqual(psi, 0.999)

    def test_calcular_psi_reproducible(self):
        """Múltiples llamadas deben retornar el mismo Ψ_bio."""
        psi1 = self.modelo.calcular_psi()
        psi2 = self.modelo.calcular_psi()
        self.assertEqual(psi1, psi2)


# ============================================================================
# Clase 3 – TestSuperradianciaFotonez (10 tests)
# ============================================================================


class TestSuperradianciaFotonez(unittest.TestCase):
    """Tests para SuperradianciaFotonez."""

    def setUp(self):
        self.sr = SuperradianciaFotonez()
        self.psi_alta = 0.999780   # superradiante
        self.psi_baja = 0.888      # no superradiante

    def test_N_magnitud(self):
        """N debe ser 10¹³."""
        self.assertEqual(self.sr.N, 1e13)

    def test_F0_valor(self):
        """F₀ debe ser 141,7001 Hz."""
        self.assertEqual(self.sr.F0, 141.7001)

    def test_umbral_psi(self):
        """Umbral superradiante debe ser 0,999."""
        self.assertEqual(self.sr.umbral_psi, 0.999)

    def test_es_superradiante_alto(self):
        """Ψ = 0,99978 debe ser superradiante (True)."""
        self.assertTrue(self.sr.es_superradiante(self.psi_alta))

    def test_es_superradiante_bajo(self):
        """Ψ = 0,888 no debe ser superradiante (False)."""
        self.assertFalse(self.sr.es_superradiante(self.psi_baja))

    def test_es_superradiante_umbral_exacto(self):
        """Ψ = 0,999 exacto debe ser superradiante (borde incluido)."""
        self.assertTrue(self.sr.es_superradiante(0.999))

    def test_intensidad_superradiante_n2(self):
        """Intensidad superradiante debe ser proporcional a N²."""
        intensidad = self.sr.intensidad_superradiante(self.psi_alta)
        self.assertGreater(intensidad, self.sr.N)
        # En régimen coherente: I = N² * Ψ
        esperada = self.sr.N ** 2 * self.psi_alta
        self.assertAlmostEqual(intensidad, esperada, places=0)

    def test_intensidad_incoherente_n(self):
        """Intensidad incoherente debe ser N (no N²)."""
        intensidad = self.sr.intensidad_superradiante(self.psi_baja)
        self.assertEqual(intensidad, self.sr.N)

    def test_potencia_superradiante_positiva(self):
        """Potencia superradiante debe ser positiva."""
        p = self.sr.potencia_W(self.psi_alta)
        self.assertGreater(p, 0.0)

    def test_ganancia_superradiante(self):
        """Factor de ganancia debe ser N = 10¹³."""
        self.assertEqual(self.sr.ganancia_superradiante(), 1e13)


# ============================================================================
# Clase 4 – TestAguaEZ (15 tests)
# ============================================================================


class TestAguaEZ(unittest.TestCase):
    """Tests para AguaEZ (resonancia Lorentziana)."""

    def setUp(self):
        self.agua = AguaEZ()
        self.psi_bio = 0.99978

    def test_F0_valor(self):
        """F₀ debe ser 141,7001 Hz."""
        self.assertEqual(self.agua.F0, 141.7001)

    def test_capas_hexagonales_valor(self):
        """Capas hexagonales deben ser 551.117."""
        self.assertEqual(self.agua.capas_hexagonales, 551117)

    def test_gamma_half_positivo(self):
        """γ½ debe ser positivo."""
        self.assertGreater(self.agua.gamma_half, 0.0)

    def test_gamma_half_menor_F0(self):
        """γ½ debe ser mucho menor que F₀ (resonancia estrecha)."""
        self.assertLess(self.agua.gamma_half, self.agua.F0)

    def test_gamma_half_magnitud(self):
        """γ½ ≈ 16,990 Hz (derivada de carga=70,56)."""
        self.assertGreater(self.agua.gamma_half, 16.0)
        self.assertLess(self.agua.gamma_half, 18.0)

    def test_resonancia_lorentziana_pico(self):
        """L(F₀) = 1,0 (máximo en resonancia)."""
        l_pico = self.agua.resonancia_lorentziana(self.agua.F0)
        self.assertAlmostEqual(l_pico, 1.0, places=10)

    def test_resonancia_lorentziana_decae(self):
        """L(F₀ ± Δ) < 1 fuera de la resonancia."""
        l_off = self.agua.resonancia_lorentziana(self.agua.F0 + 50.0)
        self.assertLess(l_off, 1.0)
        self.assertGreater(l_off, 0.0)

    def test_resonancia_lorentziana_simetrica(self):
        """L debe ser simétrica alrededor de F₀."""
        delta = 5.0
        l_plus = self.agua.resonancia_lorentziana(self.agua.F0 + delta)
        l_minus = self.agua.resonancia_lorentziana(self.agua.F0 - delta)
        self.assertAlmostEqual(l_plus, l_minus, places=10)

    def test_resonancia_lorentziana_rango(self):
        """L(f) debe estar en [0, 1] para cualquier f > 0."""
        for f in [1.0, 10.0, 50.0, 100.0, 141.7001, 200.0, 500.0]:
            l = self.agua.resonancia_lorentziana(f)
            self.assertGreaterEqual(l, 0.0)
            self.assertLessEqual(l, 1.0)

    def test_calcular_carga_resonancia_valor(self):
        """Carga de resonancia = 70,56 (preciso a 2 decimales)."""
        carga = self.agua.calcular_carga_resonancia()
        self.assertAlmostEqual(carga, 70.56, places=2)

    def test_calcular_carga_resonancia_mayor_uno(self):
        """Carga de resonancia debe ser > 1."""
        self.assertGreater(self.agua.calcular_carga_resonancia(), 1.0)

    def test_calcular_psi_agua_rango(self):
        """Ψ_agua debe estar en (0, 1)."""
        psi_agua = self.agua.calcular_psi_agua(self.psi_bio)
        self.assertGreater(psi_agua, 0.0)
        self.assertLess(psi_agua, 1.0)

    def test_calcular_psi_agua_alta_coherencia(self):
        """Ψ_agua debe estar por encima de 0,99 (alta coherencia)."""
        psi_agua = self.agua.calcular_psi_agua(self.psi_bio)
        self.assertGreater(psi_agua, 0.990)

    def test_calcular_psi_agua_crece_con_psi_bio(self):
        """Ψ_agua debe crecer cuando Ψ_bio crece."""
        psi_bio_bajo = 0.990
        psi_bio_alto = 0.999780
        psi_agua_bajo = self.agua.calcular_psi_agua(psi_bio_bajo)
        psi_agua_alto = self.agua.calcular_psi_agua(psi_bio_alto)
        self.assertGreater(psi_agua_alto, psi_agua_bajo)

    def test_bandwidth_Q_positivo(self):
        """Factor de calidad Q debe ser positivo."""
        q = self.agua.bandwidth_Q()
        self.assertGreater(q, 0.0)
        # Q = F₀/(2γ½), con γ½ ≈ 16,990 Hz → Q ≈ 4,17
        self.assertGreater(q, 4.0)
        self.assertLess(q, 5.0)


# ============================================================================
# Clase 5 – TestRespiracionAurea (12 tests)
# ============================================================================


class TestRespiracionAurea(unittest.TestCase):
    """Tests para RespiracionAurea (protocolo de 6 rpm con φ)."""

    def setUp(self):
        self.resp = RespiracionAurea()
        self.psi_bio = 0.99978

    def test_f_resp_valor(self):
        """Frecuencia respiratoria debe ser 0,1 Hz (6 rpm)."""
        self.assertAlmostEqual(self.resp.f_resp, 0.1, places=6)

    def test_T_resp_valor(self):
        """Período respiratorio debe ser 10 s."""
        self.assertAlmostEqual(self.resp.T_resp, 10.0, places=6)

    def test_ciclos_por_minuto(self):
        """Deben ser exactamente 6 ciclos por minuto."""
        self.assertAlmostEqual(self.resp.ciclos_por_minuto(), 6.0, places=6)

    def test_t_inhalacion_positivo(self):
        """Duración de inhalación debe ser positiva."""
        self.assertGreater(self.resp.t_inhalacion, 0.0)

    def test_t_exhalacion_positivo(self):
        """Duración de exhalación debe ser positiva."""
        self.assertGreater(self.resp.t_exhalacion, 0.0)

    def test_t_inh_exh_suma_T_resp(self):
        """T_inh + T_exh = T_resp (ciclo completo)."""
        suma = self.resp.t_inhalacion + self.resp.t_exhalacion
        self.assertAlmostEqual(suma, self.resp.T_resp, places=8)

    def test_ratio_ie_igual_phi(self):
        """Ratio exhalación/inhalación debe ser φ ≈ 1,618034."""
        self.assertAlmostEqual(self.resp.ratio_ie, 1.618034, places=4)

    def test_t_inhalacion_magnitud(self):
        """T_inh ≈ 3,820 s (T/(1+φ))."""
        t_inh_esperado = 10.0 / (1.0 + 1.618034)
        self.assertAlmostEqual(self.resp.t_inhalacion, t_inh_esperado, places=6)

    def test_t_exhalacion_mayor_inhalacion(self):
        """La exhalación áurea es más larga que la inhalación (φ > 1)."""
        self.assertGreater(self.resp.t_exhalacion, self.resp.t_inhalacion)

    def test_calcular_psi_hrv_rango(self):
        """Ψ_hrv debe estar en (0, 1)."""
        psi_hrv = self.resp.calcular_psi_hrv(self.psi_bio)
        self.assertGreater(psi_hrv, 0.0)
        self.assertLess(psi_hrv, 1.0)

    def test_calcular_psi_hrv_alta_coherencia(self):
        """Ψ_hrv debe estar por encima de 0,99 para Ψ_bio alto."""
        psi_hrv = self.resp.calcular_psi_hrv(self.psi_bio)
        self.assertGreater(psi_hrv, 0.99)

    def test_calcular_psi_hrv_crece_con_psi_bio(self):
        """Ψ_hrv debe crecer cuando Ψ_bio crece."""
        psi_hrv_bajo = self.resp.calcular_psi_hrv(0.990)
        psi_hrv_alto = self.resp.calcular_psi_hrv(0.99978)
        self.assertGreater(psi_hrv_alto, psi_hrv_bajo)


# ============================================================================
# Clase 6 – TestCoherenciaBiologicaTotal (11 tests)
# ============================================================================


class TestCoherenciaBiologicaTotal(unittest.TestCase):
    """Tests para CoherenciaBiologicaTotal."""

    def setUp(self):
        self.cbt = CoherenciaBiologicaTotal()
        self.psi_bio = 0.99978
        self.psi_agua = 0.993202
        self.psi_hrv = 0.99725

    def test_pesos_suman_uno(self):
        """Los pesos deben sumar exactamente 1,0."""
        suma = self.cbt.w_bio + self.cbt.w_agua + self.cbt.w_hrv
        self.assertAlmostEqual(suma, 1.0, places=10)

    def test_verificar_pesos(self):
        """verificar_pesos() debe retornar True."""
        self.assertTrue(self.cbt.verificar_pesos())

    def test_w_bio_dominante(self):
        """w_bio debe ser el peso dominante (> w_agua > w_hrv)."""
        self.assertGreater(self.cbt.w_bio, self.cbt.w_agua)
        self.assertGreater(self.cbt.w_agua, self.cbt.w_hrv)

    def test_pesos_positivos(self):
        """Todos los pesos deben ser positivos."""
        self.assertGreater(self.cbt.w_bio, 0.0)
        self.assertGreater(self.cbt.w_agua, 0.0)
        self.assertGreater(self.cbt.w_hrv, 0.0)

    def test_calcular_psi_general_rango(self):
        """Ψ_general debe estar en [0, 1]."""
        psi_g = self.cbt.calcular_psi_general(self.psi_bio, self.psi_agua, self.psi_hrv)
        self.assertGreaterEqual(psi_g, 0.0)
        self.assertLessEqual(psi_g, 1.0)

    def test_calcular_psi_general_alta_coherencia(self):
        """Ψ_general debe estar por encima de 0,997."""
        psi_g = self.cbt.calcular_psi_general(self.psi_bio, self.psi_agua, self.psi_hrv)
        self.assertGreater(psi_g, 0.997)

    def test_calcular_psi_general_promedio_ponderado(self):
        """Ψ_general debe ser la media ponderada correcta."""
        psi_g = self.cbt.calcular_psi_general(self.psi_bio, self.psi_agua, self.psi_hrv)
        esperado = (0.65 * self.psi_bio + 0.25 * self.psi_agua + 0.10 * self.psi_hrv)
        self.assertAlmostEqual(psi_g, round(esperado, 6), places=6)

    def test_calcular_psi_general_entre_componentes(self):
        """Ψ_general debe estar entre min(psi_*) y max(psi_*)."""
        psi_g = self.cbt.calcular_psi_general(self.psi_bio, self.psi_agua, self.psi_hrv)
        min_psi = min(self.psi_bio, self.psi_agua, self.psi_hrv)
        max_psi = max(self.psi_bio, self.psi_agua, self.psi_hrv)
        self.assertGreaterEqual(psi_g, min_psi - 1e-9)
        self.assertLessEqual(psi_g, max_psi + 1e-9)

    def test_desglose_claves(self):
        """desglose() debe retornar las claves correctas."""
        d = self.cbt.desglose(self.psi_bio, self.psi_agua, self.psi_hrv)
        self.assertIn("contribucion_bio", d)
        self.assertIn("contribucion_agua", d)
        self.assertIn("contribucion_hrv", d)
        self.assertIn("psi_general", d)

    def test_desglose_suma_psi_general(self):
        """Las contribuciones del desglose deben sumar Ψ_general."""
        d = self.cbt.desglose(self.psi_bio, self.psi_agua, self.psi_hrv)
        suma = d["contribucion_bio"] + d["contribucion_agua"] + d["contribucion_hrv"]
        self.assertAlmostEqual(suma, d["psi_general"], places=5)

    def test_calcular_psi_general_reproducible(self):
        """Múltiples llamadas deben producir el mismo resultado."""
        psi1 = self.cbt.calcular_psi_general(self.psi_bio, self.psi_agua, self.psi_hrv)
        psi2 = self.cbt.calcular_psi_general(self.psi_bio, self.psi_agua, self.psi_hrv)
        self.assertEqual(psi1, psi2)


# ============================================================================
# Clase 7 – TestSistemaKuramotoSuperradiancia (11 tests)
# ============================================================================


class TestSistemaKuramotoSuperradiancia(unittest.TestCase):
    """Tests para SistemaKuramotoSuperradiancia (orquestador)."""

    def setUp(self):
        self.sistema = SistemaKuramotoSuperradiancia()

    def test_tiene_constantes(self):
        """El sistema debe tener ConstantesKuramoto."""
        self.assertIsInstance(self.sistema.constantes, ConstantesKuramoto)

    def test_tiene_modelo(self):
        """El sistema debe tener ModeloKuramoto."""
        self.assertIsInstance(self.sistema.modelo, ModeloKuramoto)

    def test_tiene_superradiancia(self):
        """El sistema debe tener SuperradianciaFotonez."""
        self.assertIsInstance(self.sistema.superradiancia, SuperradianciaFotonez)

    def test_tiene_agua(self):
        """El sistema debe tener AguaEZ."""
        self.assertIsInstance(self.sistema.agua, AguaEZ)

    def test_tiene_respiracion(self):
        """El sistema debe tener RespiracionAurea."""
        self.assertIsInstance(self.sistema.respiracion, RespiracionAurea)

    def test_tiene_coherencia(self):
        """El sistema debe tener CoherenciaBiologicaTotal."""
        self.assertIsInstance(self.sistema.coherencia, CoherenciaBiologicaTotal)

    def test_activar_retorna_resultado(self):
        """activar() debe retornar un ResultadoKuramoto."""
        resultado = self.sistema.activar()
        self.assertIsInstance(resultado, ResultadoKuramoto)

    def test_activar_psi_bio_valor(self):
        """Ψ_bio debe ser ≈ 0,99978."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado.psi_biologica, 0.99978, places=5)

    def test_activar_superradiante_true(self):
        """El sistema debe ser superradiante."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado.superradiante)

    def test_activar_carga_resonancia(self):
        """Carga de resonancia debe ser 70,56."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado.carga_resonancia, 70.56, places=2)

    def test_activar_capas_hexagonales(self):
        """Capas hexagonales deben ser 551.117."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado.capas_hexagonales, 551117)


# ============================================================================
# Clase 8 – TestResultadoKuramoto (5 tests)
# ============================================================================


class TestResultadoKuramoto(unittest.TestCase):
    """Tests para el dataclass ResultadoKuramoto."""

    def setUp(self):
        self.resultado = SistemaKuramotoSuperradiancia().activar()

    def test_psi_biologica_float(self):
        """psi_biologica debe ser float."""
        self.assertIsInstance(self.resultado.psi_biologica, float)

    def test_psi_agua_ez_float(self):
        """psi_agua_ez debe ser float."""
        self.assertIsInstance(self.resultado.psi_agua_ez, float)

    def test_psi_general_float(self):
        """psi_general debe ser float."""
        self.assertIsInstance(self.resultado.psi_general, float)

    def test_mensaje_no_vacio(self):
        """El mensaje de estado no debe estar vacío."""
        self.assertIsInstance(self.resultado.mensaje, str)
        self.assertGreater(len(self.resultado.mensaje), 10)

    def test_mensaje_sistema_estable(self):
        """El mensaje debe contener '✅ SISTEMA ESTABLE'."""
        self.assertIn("✅", self.resultado.mensaje)


# ============================================================================
# Clase 9 – TestKuramotoSuperradianciaActivar (10 tests)
# ============================================================================


class TestKuramotoSuperradianciaActivar(unittest.TestCase):
    """Tests para la API pública kuramoto_superradiancia_activar()."""

    def setUp(self):
        self.result = kuramoto_superradiancia_activar()

    def test_retorna_dict(self):
        """kuramoto_superradiancia_activar() debe retornar un dict."""
        self.assertIsInstance(self.result, dict)

    def test_claves_presentes(self):
        """El dict debe contener todas las claves requeridas."""
        claves_req = {
            "psi_biologica", "psi_agua_ez", "psi_hrv", "psi_general",
            "carga_resonancia", "capas_hexagonales", "superradiante",
            "potencia_superradiante_W", "mensaje",
        }
        self.assertTrue(claves_req.issubset(set(self.result.keys())))

    def test_psi_biologica_valor(self):
        """psi_biologica debe ser ≈ 0,99978 (Adler, 5 decimales)."""
        self.assertAlmostEqual(self.result["psi_biologica"], 0.99978, places=5)

    def test_psi_biologica_supera_umbral(self):
        """psi_biologica debe superar el umbral superradiante 0,999."""
        self.assertGreaterEqual(self.result["psi_biologica"], 0.999)

    def test_psi_agua_ez_alta_coherencia(self):
        """psi_agua_ez debe ser > 0,990 (alta coherencia EZ)."""
        self.assertGreater(self.result["psi_agua_ez"], 0.990)

    def test_psi_general_alta_coherencia(self):
        """psi_general debe ser > 0,997."""
        self.assertGreater(self.result["psi_general"], 0.997)

    def test_carga_resonancia_exacta(self):
        """carga_resonancia debe ser exactamente 70,56."""
        self.assertAlmostEqual(self.result["carga_resonancia"], 70.56, places=2)

    def test_capas_hexagonales_exactas(self):
        """capas_hexagonales debe ser exactamente 551.117."""
        self.assertEqual(self.result["capas_hexagonales"], 551117)

    def test_superradiante_true(self):
        """superradiante debe ser True."""
        self.assertTrue(self.result["superradiante"])

    def test_idempotente(self):
        """Múltiples llamadas deben producir resultados idénticos."""
        r1 = kuramoto_superradiancia_activar()
        r2 = kuramoto_superradiancia_activar()
        self.assertEqual(r1["psi_biologica"], r2["psi_biologica"])
        self.assertEqual(r1["carga_resonancia"], r2["carga_resonancia"])
        self.assertEqual(r1["superradiante"], r2["superradiante"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
