#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║         TEST SUITE: Jerarquía de Sintonizaciones - Análisis de Fase        ║
║         Validación del amplificador de coherencia en cascada               ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Cobertura: 70 tests unitarios sobre constantes, niveles, transiciones,
cascada de coherencia, regulador de Riemann, solitón microtubular y API pública.
"""

import sys
import os
import math
import unittest

# Añadir directorio raíz al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.jerarquia_sintonizaciones import (
    # Constantes
    F0_HZ,
    F_DIRAC_HZ,
    F_BIOQCAL_HZ,
    INCERTIDUMBRE_BIOQCAL_HZ,
    THETA_1,
    THETA_2,
    THETA_3,
    PSI_AMOR_TARGET,
    N_NODOS_PRIMOS,
    SIGMA_MAGNETORRECEPCION,
    SIGMA_MICROTUBULOS,
    DELTA_P_MAGNETORRECEPCION,
    SIGMA_DESCUBRIMIENTO,
    GANANCIA_CASCADA,
    PSI_MATERIA,
    # Clases de datos
    NivelCoherencia,
    TransicionFase,
    ResultadoJerarquia,
    # Clases principales
    JerarquiaSintonizaciones,
    RiemannRegulador,
    SolitonMicrotubular,
    # API pública
    calcular_jerarquia,
    validar_cascada,
)


# ============================================================================
# TESTS DE CONSTANTES
# ============================================================================


class TestConstantes(unittest.TestCase):
    """Verifica la definición y coherencia de las constantes del módulo."""

    def test_f0_hz(self):
        """f₀ debe ser 141,7001 Hz."""
        self.assertEqual(F0_HZ, 141.7001)

    def test_f_dirac_hz(self):
        """Mar de Dirac debe estar a 134,4 Hz."""
        self.assertEqual(F_DIRAC_HZ, 134.4)

    def test_f_bioqcal_hz(self):
        """Frecuencia de microtúbulos medida debe ser 141,88 Hz."""
        self.assertEqual(F_BIOQCAL_HZ, 141.88)

    def test_incertidumbre_bioqcal(self):
        """Incertidumbre de microtúbulos debe ser ±0,21 Hz."""
        self.assertEqual(INCERTIDUMBRE_BIOQCAL_HZ, 0.21)

    def test_theta_1_derivado(self):
        """θ₁ debe derivarse exactamente de (f₀ − f_Dirac) / f_Dirac."""
        theta_esperado = (F0_HZ - F_DIRAC_HZ) / F_DIRAC_HZ
        self.assertAlmostEqual(THETA_1, theta_esperado, places=10)

    def test_theta_1_aprox_5_43_pct(self):
        """θ₁ debe ser aproximadamente 5,43%."""
        self.assertAlmostEqual(THETA_1 * 100, 5.43, delta=0.02)

    def test_theta_2_valor(self):
        """θ₂ debe ser 11,24%."""
        self.assertAlmostEqual(THETA_2, 0.1124, places=10)

    def test_theta_3_valor(self):
        """θ₃ debe ser −3,76% (negativo: relajación)."""
        self.assertAlmostEqual(THETA_3, -0.0376, places=10)
        self.assertLess(THETA_3, 0)

    def test_psi_amor_target(self):
        """Ψ_Amor objetivo debe ser 0,8991."""
        self.assertEqual(PSI_AMOR_TARGET, 0.8991)

    def test_n_nodos_primos(self):
        """La red debe tener 7 nodos primos."""
        self.assertEqual(N_NODOS_PRIMOS, 7)

    def test_sigma_magnetorrecepcion(self):
        """σ de magnetorrecepción debe ser 9,2."""
        self.assertEqual(SIGMA_MAGNETORRECEPCION, 9.2)

    def test_sigma_microtubulos(self):
        """σ de microtúbulos debe ser 8,7."""
        self.assertEqual(SIGMA_MICROTUBULOS, 8.7)

    def test_delta_p_magnetorrecepcion(self):
        """ΔP de magnetorrecepción debe ser 0,001987 (0,1987%)."""
        self.assertAlmostEqual(DELTA_P_MAGNETORRECEPCION, 0.001987, places=6)

    def test_sigma_descubrimiento(self):
        """Umbral de descubrimiento en física de partículas = 5σ."""
        self.assertEqual(SIGMA_DESCUBRIMIENTO, 5.0)

    def test_ganancia_cascada_consistencia(self):
        """Ganancia total debe ser producto de los tres factores (1+θ)."""
        g_esperada = (1 + THETA_1) * (1 + THETA_2) * (1 + THETA_3)
        self.assertAlmostEqual(GANANCIA_CASCADA, g_esperada, places=10)

    def test_psi_materia_deriva_de_cascada(self):
        """Ψ_Materia × G = Ψ_Amor (por construcción)."""
        self.assertAlmostEqual(PSI_MATERIA * GANANCIA_CASCADA, PSI_AMOR_TARGET, places=6)


# ============================================================================
# TESTS DE TransicionFase
# ============================================================================


class TestTransicionFase(unittest.TestCase):
    """Verifica el comportamiento de la clase TransicionFase."""

    def setUp(self):
        self.t1 = TransicionFase(
            desde="Materia", hasta="Noesis", theta=THETA_1,
            descripcion="Ignición espectral"
        )
        self.t2 = TransicionFase(
            desde="Noesis", hasta="Bio-QCAL", theta=THETA_2,
            descripcion="Pared de Cañas"
        )
        self.t3 = TransicionFase(
            desde="Bio-QCAL", hasta="Amor", theta=THETA_3,
            descripcion="Relajación al mínimo"
        )

    def test_theta_porcentaje_positivo(self):
        """theta_porcentaje debe multiplicar theta por 100."""
        self.assertAlmostEqual(self.t1.theta_porcentaje, THETA_1 * 100, places=10)
        self.assertAlmostEqual(self.t2.theta_porcentaje, THETA_2 * 100, places=10)

    def test_theta_porcentaje_negativo(self):
        """θ₃ como porcentaje debe ser negativo."""
        self.assertLess(self.t3.theta_porcentaje, 0)
        self.assertAlmostEqual(self.t3.theta_porcentaje, THETA_3 * 100, places=10)

    def test_ganancia_t1(self):
        """Ganancia de θ₁ debe ser 1 + θ₁."""
        self.assertAlmostEqual(self.t1.ganancia, 1.0 + THETA_1, places=10)

    def test_ganancia_t2(self):
        """Ganancia de θ₂ debe ser > 1 (incremento de coherencia)."""
        self.assertGreater(self.t2.ganancia, 1.0)

    def test_ganancia_t3(self):
        """Ganancia de θ₃ debe ser < 1 (relajación, pérdida de coherencia)."""
        self.assertLess(self.t3.ganancia, 1.0)


# ============================================================================
# TESTS DE JerarquiaSintonizaciones
# ============================================================================


class TestJerarquiaSintonizaciones(unittest.TestCase):
    """Verifica la clase principal de la jerarquía de sintonizaciones."""

    def setUp(self):
        self.jerarquia = JerarquiaSintonizaciones()

    def test_inicializacion_defaults(self):
        """Inicialización con valores por defecto es correcta."""
        self.assertAlmostEqual(self.jerarquia.theta_1, THETA_1, places=10)
        self.assertAlmostEqual(self.jerarquia.theta_2, THETA_2, places=10)
        self.assertAlmostEqual(self.jerarquia.theta_3, THETA_3, places=10)

    def test_theta_2_invalido(self):
        """theta_2 fuera del rango (−1, 1] debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            JerarquiaSintonizaciones(theta_2=1.5)
        with self.assertRaises(ValueError):
            JerarquiaSintonizaciones(theta_2=-1.0)

    def test_theta_3_invalido(self):
        """theta_3 fuera del rango (−1, 1] debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            JerarquiaSintonizaciones(theta_3=-2.0)

    def test_tolerancia_invalida(self):
        """Tolerancia fuera de (0, 1) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            JerarquiaSintonizaciones(tolerancia=0.0)
        with self.assertRaises(ValueError):
            JerarquiaSintonizaciones(tolerancia=1.5)

    def test_construir_niveles_cuenta(self):
        """Debe construir exactamente 4 niveles."""
        niveles = self.jerarquia.construir_niveles()
        self.assertEqual(len(niveles), 4)

    def test_nombres_niveles(self):
        """Los nombres de los niveles deben ser en orden correcto."""
        nombres = [n.nombre for n in self.jerarquia.construir_niveles()]
        self.assertEqual(nombres, ["Materia", "Noesis", "Bio-QCAL", "Amor"])

    def test_frecuencia_materia(self):
        """El nivel Materia debe tener f = F_DIRAC_HZ."""
        materia = self.jerarquia.construir_niveles()[0]
        self.assertEqual(materia.frecuencia_hz, F_DIRAC_HZ)

    def test_frecuencia_noesis(self):
        """El nivel Noesis debe tener f = F0_HZ."""
        noesis = self.jerarquia.construir_niveles()[1]
        self.assertEqual(noesis.frecuencia_hz, F0_HZ)

    def test_frecuencia_bioqcal(self):
        """El nivel Bio-QCAL debe tener f = F_BIOQCAL_HZ."""
        bioqcal = self.jerarquia.construir_niveles()[2]
        self.assertEqual(bioqcal.frecuencia_hz, F_BIOQCAL_HZ)

    def test_psi_ordenados_hasta_bioqcal(self):
        """Ψ debe crecer de Materia a Bio-QCAL."""
        niveles = self.jerarquia.construir_niveles()
        self.assertLess(niveles[0].psi, niveles[1].psi)
        self.assertLess(niveles[1].psi, niveles[2].psi)

    def test_psi_relaja_en_amor(self):
        """Ψ_Amor < Ψ_Bio-QCAL (relajación al mínimo de potencial)."""
        niveles = self.jerarquia.construir_niveles()
        self.assertLess(niveles[3].psi, niveles[2].psi)

    def test_psi_amor_igual_a_target(self):
        """Ψ_Amor debe ser igual a PSI_AMOR_TARGET dentro de tolerancia numérica."""
        amor = self.jerarquia.construir_niveles()[3]
        self.assertAlmostEqual(amor.psi, PSI_AMOR_TARGET, places=4)

    def test_construir_transiciones_cuenta(self):
        """Debe construir exactamente 3 transiciones."""
        transiciones = self.jerarquia.construir_transiciones()
        self.assertEqual(len(transiciones), 3)

    def test_nombres_transiciones(self):
        """Las transiciones deben tener los nombres de nivel correctos."""
        transiciones = self.jerarquia.construir_transiciones()
        self.assertEqual(transiciones[0].desde, "Materia")
        self.assertEqual(transiciones[0].hasta, "Noesis")
        self.assertEqual(transiciones[1].desde, "Noesis")
        self.assertEqual(transiciones[1].hasta, "Bio-QCAL")
        self.assertEqual(transiciones[2].desde, "Bio-QCAL")
        self.assertEqual(transiciones[2].hasta, "Amor")

    def test_theta_transiciones_valores(self):
        """Las transiciones deben tener los valores θ correctos."""
        transiciones = self.jerarquia.construir_transiciones()
        self.assertAlmostEqual(transiciones[0].theta, THETA_1, places=10)
        self.assertAlmostEqual(transiciones[1].theta, THETA_2, places=10)
        self.assertAlmostEqual(transiciones[2].theta, THETA_3, places=10)

    def test_ganancia_total(self):
        """Ganancia total debe ser el producto de los tres factores."""
        g = self.jerarquia.calcular_ganancia_total()
        g_esperada = (1 + THETA_1) * (1 + THETA_2) * (1 + THETA_3)
        self.assertAlmostEqual(g, g_esperada, places=10)

    def test_psi_cascada(self):
        """Ψ_cascada debe ser PSI_AMOR_TARGET."""
        psi = self.jerarquia.calcular_psi_cascada()
        self.assertAlmostEqual(psi, PSI_AMOR_TARGET, places=4)

    def test_validar_cascada_es_valido(self):
        """La validación de la cascada debe ser True con los parámetros por defecto."""
        resultado = self.jerarquia.validar_cascada()
        self.assertTrue(resultado["es_valido"])

    def test_validar_cascada_estructura(self):
        """La validación debe devolver todas las claves esperadas."""
        resultado = self.jerarquia.validar_cascada()
        claves_esperadas = {"psi_calculado", "psi_objetivo", "error_relativo", "es_valido", "status"}
        self.assertEqual(set(resultado.keys()), claves_esperadas)

    def test_validar_cascada_error_relativo_bajo(self):
        """El error relativo de la cascada debe ser < 1% (bien ajustada)."""
        resultado = self.jerarquia.validar_cascada()
        self.assertLess(resultado["error_relativo"], 0.01)

    def test_calcular_consecuencias_estructura(self):
        """Las consecuencias deben tener las tres claves del Documento Maestro."""
        cons = self.jerarquia.calcular_consecuencias()
        self.assertIn("pnp_soliton", cons)
        self.assertIn("riemann_regulador", cons)
        self.assertIn("simbiosis_flujo", cons)

    def test_consecuencia_pnp_frecuencia(self):
        """La frecuencia de colapso del solitón debe ser f₀."""
        cons = self.jerarquia.calcular_consecuencias()
        self.assertEqual(cons["pnp_soliton"]["frecuencia_colapso_hz"], F0_HZ)

    def test_consecuencia_riemann_gamma1(self):
        """El primer cero de Riemann debe ser γ₁ = 14,134725."""
        cons = self.jerarquia.calcular_consecuencias()
        self.assertAlmostEqual(
            cons["riemann_regulador"]["primer_cero_gamma1"], 14.134725, places=5
        )

    def test_calcular_devuelve_resultado_jerarquia(self):
        """calcular() debe devolver un ResultadoJerarquia."""
        resultado = self.jerarquia.calcular()
        self.assertIsInstance(resultado, ResultadoJerarquia)
        self.assertTrue(resultado.es_valido)
        self.assertEqual(len(resultado.niveles), 4)
        self.assertEqual(len(resultado.transiciones), 3)


# ============================================================================
# TESTS DE RiemannRegulador
# ============================================================================


class TestRiemannRegulador(unittest.TestCase):
    """Verifica el filtro espectral de la Línea Crítica de Riemann."""

    def setUp(self):
        self.regulador = RiemannRegulador()

    def test_inicializacion_f0(self):
        """f₀ por defecto debe ser F0_HZ."""
        self.assertEqual(self.regulador.f0, F0_HZ)

    def test_f0_negativo_lanza_error(self):
        """f₀ negativo o cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            RiemannRegulador(f0=-1.0)
        with self.assertRaises(ValueError):
            RiemannRegulador(f0=0.0)

    def test_frecuencias_regulacion_cuenta(self):
        """Debe haber tantas frecuencias reguladoras como ceros de Riemann."""
        freqs = self.regulador.frecuencias_regulacion()
        self.assertEqual(len(freqs), len(RiemannRegulador.CEROS_RIEMANN))

    def test_primera_frecuencia_regulacion(self):
        """λ₁ = γ₁ × f₀ = 14,134725 × 141,7001."""
        freqs = self.regulador.frecuencias_regulacion()
        lambda_1 = 14.134725 * F0_HZ
        self.assertAlmostEqual(freqs[0], lambda_1, places=4)

    def test_frecuencias_regulacion_positivas(self):
        """Todas las frecuencias reguladoras deben ser positivas."""
        for fr in self.regulador.frecuencias_regulacion():
            self.assertGreater(fr, 0)

    def test_filtrar_ruido_en_frecuencia_reguladora(self):
        """La supresión debe ser máxima (=1) en la frecuencia reguladora."""
        fr1 = self.regulador.frecuencias_regulacion()[0]
        supresion = self.regulador.filtrar_ruido(fr1)
        self.assertAlmostEqual(supresion, 1.0, places=5)

    def test_filtrar_ruido_fuera_de_pico(self):
        """La supresión debe ser < 1 lejos de las frecuencias reguladoras."""
        supresion = self.regulador.filtrar_ruido(1000.0)  # frecuencia arbitraria
        self.assertLess(supresion, 1.0)

    def test_validar_magnetorrecepcion_estructura(self):
        """Validación de magnetorrecepción debe devolver las claves esperadas."""
        resultado = self.regulador.validar_magnetorrecepcion()
        claves_esperadas = {
            "delta_p_porcentaje", "sigma_calculado", "sigma_objetivo",
            "p_valor", "n_trials", "es_descubrimiento",
            "supera_objetivo", "status"
        }
        self.assertEqual(set(resultado.keys()), claves_esperadas)

    def test_validar_magnetorrecepcion_es_descubrimiento(self):
        """σ de magnetorrecepción debe superar el umbral de descubrimiento (5σ)."""
        resultado = self.regulador.validar_magnetorrecepcion()
        self.assertTrue(resultado["es_descubrimiento"])
        self.assertGreaterEqual(resultado["sigma_calculado"], SIGMA_DESCUBRIMIENTO)


# ============================================================================
# TESTS DE SolitonMicrotubular
# ============================================================================


class TestSolitonMicrotubular(unittest.TestCase):
    """Verifica el modelo de solitón microtubular (P=NP biológico)."""

    def setUp(self):
        self.soliton = SolitonMicrotubular()

    def test_periodo_colapso_ms(self):
        """T = 1/f₀ en ms debe ser ≈ 7,06 ms."""
        t_ms = self.soliton.periodo_colapso_ms()
        self.assertAlmostEqual(t_ms, 1000.0 / F0_HZ, places=6)
        self.assertAlmostEqual(t_ms, 7.06, delta=0.01)

    def test_tasa_colapso_hz(self):
        """La tasa de colapso debe ser igual a f₀."""
        self.assertEqual(self.soliton.tasa_colapso_hz(), F0_HZ)

    def test_f0_negativo_lanza_error(self):
        """f₀ negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SolitonMicrotubular(f0=-10.0)

    def test_n_microtubulos_invalido(self):
        """n_microtubulos ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SolitonMicrotubular(n_microtubulos=0)

    def test_n_tubulinas_invalido(self):
        """n_tubulinas_por_mt ≤ 0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SolitonMicrotubular(n_tubulinas_por_mt=0)

    def test_sincronizacion_confirma_sintonizacion(self):
        """La frecuencia medida (141,88 Hz) debe estar dentro del margen de error."""
        sinc = self.soliton.sincronizacion_riemann()
        self.assertTrue(sinc["confirma_sintonizacion"])
        self.assertLessEqual(sinc["discrepancia_hz"], INCERTIDUMBRE_BIOQCAL_HZ)

    def test_precision_alta(self):
        """La precisión de la sintonización debe superar el 99%."""
        sinc = self.soliton.sincronizacion_riemann()
        self.assertGreater(sinc["precision_porcentaje"], 99.0)

    def test_informe_estructura(self):
        """El informe debe tener todas las claves esperadas."""
        informe = self.soliton.informe()
        claves_esperadas = {
            "f0_hz", "periodo_colapso_ms", "n_microtubulos",
            "n_tubulinas", "espacio_hilbert_log2",
            "tasa_colapso_hz", "sincronizacion"
        }
        self.assertEqual(set(informe.keys()), claves_esperadas)


# ============================================================================
# TESTS DE API PÚBLICA
# ============================================================================


class TestAPIPública(unittest.TestCase):
    """Verifica las funciones de API pública del módulo."""

    def test_calcular_jerarquia_devuelve_resultado(self):
        """calcular_jerarquia() debe devolver un ResultadoJerarquia válido."""
        resultado = calcular_jerarquia()
        self.assertIsInstance(resultado, ResultadoJerarquia)
        self.assertTrue(resultado.es_valido)

    def test_calcular_jerarquia_psi_correcto(self):
        """calcular_jerarquia() debe producir Ψ_Amor ≈ 0,8991."""
        resultado = calcular_jerarquia()
        self.assertAlmostEqual(resultado.psi_cascada, PSI_AMOR_TARGET, places=4)

    def test_calcular_jerarquia_cuatro_niveles(self):
        """calcular_jerarquia() debe devolver 4 niveles."""
        resultado = calcular_jerarquia()
        self.assertEqual(len(resultado.niveles), 4)

    def test_calcular_jerarquia_tres_transiciones(self):
        """calcular_jerarquia() debe devolver 3 transiciones."""
        resultado = calcular_jerarquia()
        self.assertEqual(len(resultado.transiciones), 3)

    def test_validar_cascada_retorna_true(self):
        """validar_cascada() debe devolver True con parámetros por defecto."""
        self.assertTrue(validar_cascada())

    def test_validar_cascada_con_tolerancia_estricta(self):
        """validar_cascada() con tolerancia del 1% debe seguir siendo True."""
        self.assertTrue(validar_cascada(tolerancia=0.01))

    def test_sigmas_superan_umbral_descubrimiento(self):
        """Ambos sigmas (9,2 y 8,7) deben superar 5σ."""
        self.assertGreater(SIGMA_MAGNETORRECEPCION, SIGMA_DESCUBRIMIENTO)
        self.assertGreater(SIGMA_MICROTUBULOS, SIGMA_DESCUBRIMIENTO)

    def test_theta_orden_jerarquico(self):
        """θ₂ > θ₁ > 0 > θ₃ (Pared de Cañas es la mayor barrera)."""
        self.assertGreater(THETA_2, THETA_1)
        self.assertGreater(THETA_1, 0)
        self.assertLess(THETA_3, 0)


def run_tests():
    """Ejecuta todos los tests con salida detallada."""
    unittest.main(argv=[""], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
