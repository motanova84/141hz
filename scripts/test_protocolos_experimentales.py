#!/usr/bin/env python3
"""
Tests para Protocolos Experimentales de Validación de f₀ = 141.7001 Hz

Tests unitarios para:
- ExperimentoResonanciaNeuronal
- ExperimentoModulacionMasa
- ExperimentoEntrelazamientoDistancia
"""

import sys
import os
import unittest
import numpy as np
import json
from pathlib import Path

# Añadir directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from protocolos_experimentales import (
    ExperimentoResonanciaNeuronal,
    ExperimentoModulacionMasa,
    ExperimentoEntrelazamientoDistancia,
    ejecutar_todos_experimentos,
    ResultadoExperimental,
    F0, F0_2ND_HARMONIC, F0_3RD_HARMONIC, LAMBDA_PSI
)


class TestExperimentoResonanciaNeuronal(unittest.TestCase):
    """Tests para Experimento 1: Resonancia Neuronal"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.exp = ExperimentoResonanciaNeuronal(sampling_rate=1000)
    
    def test_inicializacion(self):
        """Test inicialización del experimento"""
        self.assertEqual(self.exp.sampling_rate, 1000)
        self.assertEqual(len(self.exp.frecuencias_objetivo), 3)
        self.assertIn(F0, self.exp.frecuencias_objetivo)
        self.assertIn(F0_2ND_HARMONIC, self.exp.frecuencias_objetivo)
        self.assertIn(F0_3RD_HARMONIC, self.exp.frecuencias_objetivo)
    
    def test_sampling_rate_minimo(self):
        """Test que sampling rate debe ser >= 1000 Hz"""
        with self.assertRaises(ValueError):
            ExperimentoResonanciaNeuronal(sampling_rate=500)
    
    def test_generar_datos_meditacion(self):
        """Test generación de datos de meditación"""
        senal = self.exp.generar_datos_simulados(
            duracion=10.0,
            tipo="meditacion",
            snr_objetivo=8.0
        )
        
        # Verificar longitud correcta
        esperado = int(10.0 * 1000)
        self.assertEqual(len(senal), esperado)
        
        # Verificar que no es todo ceros
        self.assertGreater(np.std(senal), 0)
    
    def test_generar_datos_control(self):
        """Test generación de datos de control"""
        senal = self.exp.generar_datos_simulados(
            duracion=10.0,
            tipo="control",
            snr_objetivo=8.0
        )
        
        self.assertEqual(len(senal), 10000)
        self.assertGreater(np.std(senal), 0)
    
    def test_analizar_espectro_detecta_f0(self):
        """Test que el análisis espectral detecta f₀"""
        # Generar señal con f₀ fuerte
        senal = self.exp.generar_datos_simulados(
            duracion=60.0,
            tipo="meditacion",
            snr_objetivo=10.0
        )
        
        # Analizar
        resultado = self.exp.analizar_espectro(senal)
        
        # Verificar estructura
        self.assertIn("resultados_frecuencias", resultado)
        self.assertIn("espectro_completo", resultado)
        
        # Verificar detección de f₀
        self.assertIn("f141", resultado["resultados_frecuencias"])
        
        # Verificar que SNR es alto
        snr_f0 = resultado["resultados_frecuencias"]["f141"]["snr"]
        self.assertGreater(snr_f0, 5.0)
    
    def test_analizar_espectro_detecta_armonicos(self):
        """Test que detecta armónicos"""
        senal = self.exp.generar_datos_simulados(
            duracion=60.0,
            tipo="meditacion",
            snr_objetivo=10.0
        )
        
        resultado = self.exp.analizar_espectro(senal)
        
        # Verificar armónicos
        self.assertIn("f283", resultado["resultados_frecuencias"])
        self.assertIn("f425", resultado["resultados_frecuencias"])
    
    def test_ejecutar_protocolo_completo(self):
        """Test ejecución completa del protocolo"""
        resultado = self.exp.ejecutar_protocolo(duracion=10.0, n_sujetos=5)
        
        # Verificar tipo
        self.assertIsInstance(resultado, ResultadoExperimental)
        
        # Verificar campos
        self.assertEqual(resultado.experimento, "Resonancia Neuronal")
        self.assertIsInstance(resultado.exito, bool)
        self.assertIn("metricas", resultado.__dict__)
        self.assertIn("datos", resultado.__dict__)
        
        # Verificar métricas
        self.assertIn("snr_meditacion", resultado.metricas)
        self.assertIn("snr_control", resultado.metricas)
        self.assertIn("ratio_amplitud", resultado.metricas)
        
        # Verificar que SNR meditación > control
        self.assertGreater(
            resultado.metricas["snr_meditacion"],
            resultado.metricas["snr_control"]
        )
    
    def test_criterio_exito_ratio_amplitud(self):
        """Test criterio de éxito: ratio > 10"""
        resultado = self.exp.ejecutar_protocolo(duracion=30.0, n_sujetos=10)
        
        # El protocolo debe generar ratio > 10 por diseño
        self.assertGreater(resultado.metricas["ratio_amplitud"], 10.0)
    
    def test_criterio_exito_snr(self):
        """Test criterio de éxito: SNR > 5"""
        resultado = self.exp.ejecutar_protocolo(duracion=30.0, n_sujetos=10)
        
        # SNR meditación debe ser > 5
        self.assertGreater(resultado.metricas["snr_meditacion"], 5.0)


class TestExperimentoModulacionMasa(unittest.TestCase):
    """Tests para Experimento 2: Modulación de Masa"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.exp = ExperimentoModulacionMasa()
    
    def test_inicializacion(self):
        """Test inicialización del experimento"""
        # Verificar constantes físicas
        self.assertAlmostEqual(self.exp.h_bar, 1.054571817e-34, places=40)
        self.assertAlmostEqual(self.exp.k_B, 1.380649e-23, places=30)
        self.assertGreater(self.exp.m_Rb87, 0)
        self.assertGreater(self.exp.E_psi, 0)
    
    def test_calcular_frecuencia_oscilacion(self):
        """Test cálculo de frecuencia de oscilación"""
        freq = self.exp.calcular_frecuencia_oscilacion(
            masa_efectiva=self.exp.m_Rb87,
            omega_trap=2 * np.pi * 100
        )
        
        # Debe dar aproximadamente 100 Hz
        self.assertAlmostEqual(freq, 100.0, places=1)
    
    def test_simular_bec_coherente(self):
        """Test simulación de BEC coherente"""
        resultado = self.exp.simular_bec_coherente(
            n_atomos=10000,
            temperatura=100e-9,
            coherencia=0.9
        )
        
        # Verificar estructura
        self.assertIn("masa_efectiva", resultado)
        self.assertIn("delta_m_relativo", resultado)
        self.assertIn("frecuencia_oscilacion", resultado)
        self.assertIn("coherencia", resultado)
        
        # Verificar valores
        self.assertEqual(resultado["coherencia"], 0.9)
        self.assertGreater(resultado["masa_efectiva"], 0)
        self.assertGreater(resultado["frecuencia_oscilacion"], 0)
    
    def test_simular_gas_termico(self):
        """Test simulación de gas térmico"""
        resultado = self.exp.simular_gas_termico(
            n_atomos=10000,
            temperatura=1e-6
        )
        
        # Verificar que coherencia es 0
        self.assertEqual(resultado["coherencia"], 0.0)
        
        # delta_m debe ser mucho menor que en BEC
        self.assertLess(abs(resultado["delta_m_relativo"]), 1e-20)
    
    def test_comparacion_bec_vs_gas(self):
        """Test comparación BEC vs gas térmico"""
        bec = self.exp.simular_bec_coherente(coherencia=0.9)
        gas = self.exp.simular_gas_termico()
        
        # BEC debe tener mayor delta_m que gas
        self.assertGreater(
            abs(bec["delta_m_relativo"]),
            abs(gas["delta_m_relativo"])
        )
    
    def test_ejecutar_protocolo_completo(self):
        """Test ejecución completa del protocolo"""
        resultado = self.exp.ejecutar_protocolo(n_mediciones=100)
        
        # Verificar tipo
        self.assertIsInstance(resultado, ResultadoExperimental)
        
        # Verificar campos
        self.assertEqual(resultado.experimento, "Modulación de Masa")
        self.assertIsInstance(resultado.exito, bool)
        
        # Verificar métricas
        self.assertIn("delta_m_relativo", resultado.metricas)
        self.assertIn("delta_m_predicho", resultado.metricas)
        self.assertIn("delta_frecuencia_hz", resultado.metricas)
    
    def test_orden_magnitud_delta_m(self):
        """Test que delta_m está en el orden correcto"""
        resultado = self.exp.ejecutar_protocolo()
        
        delta_m = resultado.metricas["delta_m_relativo"]
        
        # Debe estar en el rango razonable para un BEC real
        # Con 10^6 átomos a 100 nK, esperamos ~10^-8
        self.assertGreater(delta_m, 1e-10)
        self.assertLess(delta_m, 1e-6)


class TestExperimentoEntrelazamientoDistancia(unittest.TestCase):
    """Tests para Experimento 3: Entrelazamiento a Distancia"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.exp = ExperimentoEntrelazamientoDistancia()
    
    def test_inicializacion(self):
        """Test inicialización del experimento"""
        self.assertEqual(len(self.exp.distancias_prueba), 5)
        self.assertIn(2000, self.exp.distancias_prueba)
        self.assertEqual(self.exp.lambda_psi, LAMBDA_PSI)
    
    def test_calcular_tiempo_decoherencia_con_psi(self):
        """Test cálculo de tiempo con efecto Ψ"""
        # Antes de λ_Ψ
        tau_antes = self.exp.calcular_tiempo_decoherencia(1000, "con_psi")
        
        # Después de λ_Ψ
        tau_despues = self.exp.calcular_tiempo_decoherencia(5000, "con_psi")
        
        # Debe haber diferencia significativa
        self.assertGreater(tau_antes, tau_despues)
    
    def test_calcular_tiempo_decoherencia_qft(self):
        """Test cálculo de tiempo QFT estándar"""
        tau_100 = self.exp.calcular_tiempo_decoherencia(100, "qft_estandar")
        tau_5000 = self.exp.calcular_tiempo_decoherencia(5000, "qft_estandar")
        
        # Debe decrecer con distancia
        self.assertGreater(tau_100, tau_5000)
    
    def test_salto_en_lambda_psi(self):
        """Test que hay salto cerca de λ_Ψ"""
        # Medir τ antes, en, y después de λ_Ψ
        tau_1000 = self.exp.calcular_tiempo_decoherencia(1000, "con_psi")
        tau_2000 = self.exp.calcular_tiempo_decoherencia(2000, "con_psi")
        tau_5000 = self.exp.calcular_tiempo_decoherencia(5000, "con_psi")
        
        # Razón de cambio
        razon_antes_despues = tau_1000 / tau_5000
        
        # Debe haber un salto significativo
        self.assertGreater(razon_antes_despues, 2.0)
    
    def test_ejecutar_protocolo_completo(self):
        """Test ejecución completa del protocolo"""
        resultado = self.exp.ejecutar_protocolo(n_mediciones_por_distancia=20)
        
        # Verificar tipo
        self.assertIsInstance(resultado, ResultadoExperimental)
        
        # Verificar campos
        self.assertEqual(resultado.experimento, "Entrelazamiento a Distancia")
        
        # Verificar métricas
        self.assertIn("tau_antes_2000km", resultado.metricas)
        self.assertIn("tau_despues_2000km", resultado.metricas)
        self.assertIn("razon_salto", resultado.metricas)
        
        # Verificar datos para todas las distancias
        self.assertIn("con_efecto_psi", resultado.datos)
        for dist in self.exp.distancias_prueba:
            self.assertIn(dist, resultado.datos["con_efecto_psi"])
    
    def test_criterio_exito_salto(self):
        """Test criterio de éxito: razón de salto > 2"""
        resultado = self.exp.ejecutar_protocolo(n_mediciones_por_distancia=50)
        
        # La razón de salto debe ser > 2
        self.assertGreater(resultado.metricas["razon_salto"], 2.0)
    
    def test_distancias_correctas(self):
        """Test que todas las distancias están cubiertas"""
        resultado = self.exp.ejecutar_protocolo()
        
        distancias_medidas = list(resultado.datos["con_efecto_psi"].keys())
        
        for dist in [100, 500, 1000, 2000, 5000]:
            self.assertIn(dist, distancias_medidas)


class TestEjecucionCompleta(unittest.TestCase):
    """Tests para ejecución de todos los experimentos"""
    
    def test_ejecutar_todos_experimentos(self):
        """Test ejecución de los 3 experimentos"""
        # Ejecutar sin guardar archivo
        resultados = ejecutar_todos_experimentos(guardar_resultados=False)
        
        # Verificar estructura
        self.assertEqual(len(resultados), 3)
        self.assertIn("resonancia_neuronal", resultados)
        self.assertIn("modulacion_masa", resultados)
        self.assertIn("entrelazamiento_distancia", resultados)
        
        # Verificar tipos
        for key, resultado in resultados.items():
            self.assertIsInstance(resultado, ResultadoExperimental)
            self.assertIsInstance(resultado.exito, bool)
    
    def test_guardar_resultados_json(self):
        """Test guardado de resultados en JSON"""
        import tempfile
        
        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as tmpdir:
            ruta_salida = os.path.join(tmpdir, "resultados_test.json")
            
            # Ejecutar con guardado
            resultados = ejecutar_todos_experimentos(
                guardar_resultados=True,
                ruta_salida=ruta_salida
            )
            
            # Verificar que se creó el archivo
            self.assertTrue(os.path.exists(ruta_salida))
            
            # Verificar contenido del JSON
            with open(ruta_salida, 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
            
            self.assertEqual(len(datos_json), 3)
            self.assertIn("resonancia_neuronal", datos_json)
            
            # Verificar estructura de cada experimento
            for key in datos_json:
                self.assertIn("experimento", datos_json[key])
                self.assertIn("timestamp", datos_json[key])
                self.assertIn("exito", datos_json[key])
                self.assertIn("metricas", datos_json[key])


class TestConstantesFundamentales(unittest.TestCase):
    """Tests para constantes fundamentales"""
    
    def test_frecuencia_fundamental(self):
        """Test valor de f₀"""
        self.assertAlmostEqual(F0, 141.7001, places=4)
    
    def test_armonicos(self):
        """Test valores de armónicos"""
        self.assertAlmostEqual(F0_2ND_HARMONIC, 2 * F0, places=3)
        self.assertAlmostEqual(F0_3RD_HARMONIC, 3 * F0, places=3)
    
    def test_lambda_psi(self):
        """Test valor de λ_Ψ"""
        self.assertEqual(LAMBDA_PSI, 2000.0)
        
        # Verificar relación aproximada λ ≈ c/f
        c = 299792458  # m/s
        lambda_calculada = (c / F0) / 1000  # en km
        
        # Debe estar cerca de 2000 km (orden de magnitud)
        self.assertAlmostEqual(lambda_calculada, LAMBDA_PSI, delta=200)


def run_tests():
    """Ejecutar todos los tests"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestExperimentoResonanciaNeuronal))
    suite.addTests(loader.loadTestsFromTestCase(TestExperimentoModulacionMasa))
    suite.addTests(loader.loadTestsFromTestCase(TestExperimentoEntrelazamientoDistancia))
    suite.addTests(loader.loadTestsFromTestCase(TestEjecucionCompleta))
    suite.addTests(loader.loadTestsFromTestCase(TestConstantesFundamentales))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
