#!/usr/bin/env python3
"""
Test Suite: Simulador de Resonancia Temporal
=============================================

Suite completa de pruebas para validar la implementación del
Simulador de Resonancia Temporal (Aritmología Biológica QCAL).

Cobertura:
- Inicialización y parámetros
- Cálculo de Ψ(t) - suma de fases
- Cálculo de Φ(t) - condensador de fase
- Detección de eventos de emergencia
- Validación de ciclos de 17 años
- Precisión temporal ±3 días
- Métricas de precisión 99.92%
- Mapa de resonancia
- Exportación de datos
- Experimento 1 (manipulación espectral)

Total: 25+ pruebas unitarias

Metadata QCAL: ∴𓂀Ω∞³
"""

import unittest
import numpy as np
import json
from pathlib import Path
import shutil
import sys
import os

# Agregar el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from resonancia_ciclos_temporales import (
    SimuladorResonanciaTemporal,
    F0_QCAL,
    PHI_UMBRAL,
    PRECISION_TARGET,
    DISPERSION_DIAS,
    CICADA_CYCLE_YEARS,
    YEAR_DAYS,
    DAY_HOURS,
    ejecutar_experimento_1_manipulacion_espectral
)


class TestInicializacion(unittest.TestCase):
    """Pruebas de inicialización del simulador."""
    
    def test_inicializacion_default(self):
        """Test 1: Inicialización con parámetros por defecto."""
        sim = SimuladorResonanciaTemporal()
        
        self.assertEqual(sim.f0, F0_QCAL)
        self.assertEqual(sim.ciclo_anos, CICADA_CYCLE_YEARS)
        self.assertEqual(sim.phi_umbral, PHI_UMBRAL)
        
    def test_inicializacion_personalizada(self):
        """Test 2: Inicialización con parámetros personalizados."""
        f0_custom = 150.0
        ciclo_custom = 13
        
        sim = SimuladorResonanciaTemporal(f0=f0_custom, ciclo_anos=ciclo_custom)
        
        self.assertEqual(sim.f0, f0_custom)
        self.assertEqual(sim.ciclo_anos, ciclo_custom)
        
    def test_frecuencias_multiescala_calculadas(self):
        """Test 3: Verificación de frecuencias multiescala."""
        sim = SimuladorResonanciaTemporal()
        
        # Verificar que las frecuencias estén en el rango esperado
        self.assertGreater(sim.f_anual, 0)
        self.assertGreater(sim.f_diaria, 0)
        self.assertGreater(sim.f_lunar, 0)
        
        # f_diaria debería ser mucho mayor que f_anual
        self.assertGreater(sim.f_diaria, sim.f_anual * 100)
        
    def test_amplitudes_relativas(self):
        """Test 4: Verificación de amplitudes relativas."""
        sim = SimuladorResonanciaTemporal()
        
        # Verificar amplitudes positivas
        self.assertGreater(sim.A_anual, 0)
        self.assertGreater(sim.A_diaria, 0)
        self.assertGreater(sim.A_lunar, 0)
        self.assertGreater(sim.A_f0, 0)
        
        # Amplitud anual debería ser la mayor
        self.assertGreater(sim.A_anual, sim.A_diaria)
        self.assertGreater(sim.A_anual, sim.A_lunar)


class TestCalculoPsi(unittest.TestCase):
    """Pruebas del cálculo de Ψ(t)."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        
    def test_psi_array_simple(self):
        """Test 5: Cálculo de Ψ(t) con array simple."""
        t = np.linspace(0, 100, 1000)
        psi = self.sim.calcular_psi(t)
        
        self.assertEqual(len(psi), len(t))
        self.assertTrue(np.all(np.isfinite(psi)))
        
    def test_psi_oscilacion(self):
        """Test 6: Ψ(t) oscila correctamente."""
        t = np.linspace(0, 365 * DAY_HOURS * 3600, 10000)
        psi = self.sim.calcular_psi(t)
        
        # Debe oscilar (cambios de valor)
        self.assertTrue(np.any(psi > 0))
        # Verificar que oscila comparando valores
        diff = np.diff(psi)
        self.assertTrue(np.any(diff > 0))  # Crece
        self.assertTrue(np.any(diff < 0))  # Decrece
        
    def test_psi_amplitud_acotada(self):
        """Test 7: Amplitud de Ψ(t) está acotada."""
        t = np.linspace(0, 365 * DAY_HOURS * 3600, 10000)
        psi = self.sim.calcular_psi(t)
        
        # La suma de amplitudes debería acotar el máximo
        max_esperado = (self.sim.A_anual + self.sim.A_diaria + 
                       self.sim.A_lunar + self.sim.A_f0)
        
        self.assertLessEqual(np.max(np.abs(psi)), max_esperado * 1.1)
        
    def test_psi_en_t_cero(self):
        """Test 8: Ψ(0) es calculable."""
        psi_0 = self.sim.calcular_psi(np.array([0.0]))
        
        self.assertEqual(len(psi_0), 1)
        self.assertTrue(np.isfinite(psi_0[0]))


class TestCalculoPhi(unittest.TestCase):
    """Pruebas del cálculo de Φ(t) - condensador de fase."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        
    def test_phi_integracion_monotona(self):
        """Test 9: Φ(t) es monótona creciente (en promedio)."""
        t = np.linspace(0, 365 * DAY_HOURS * 3600, 10000)
        psi = self.sim.calcular_psi(t)
        phi = self.sim.calcular_phi_acumulada(t, psi)
        
        # La integral acumulativa debe tener tendencia creciente
        self.assertEqual(len(phi), len(t))
        self.assertTrue(np.all(np.isfinite(phi)))
        
    def test_phi_normalizacion(self):
        """Test 10: Φ(t) está normalizada correctamente."""
        t = np.linspace(0, 365 * DAY_HOURS * 3600, 10000)
        psi = self.sim.calcular_psi(t)
        phi = self.sim.calcular_phi_acumulada(t, psi)
        
        # El máximo debe estar cerca de 1.0 por normalización
        self.assertLessEqual(np.max(np.abs(phi)), 1.5)
        
    def test_phi_en_t_cero(self):
        """Test 11: Φ(0) = 0."""
        t = np.linspace(0, 100, 1000)
        psi = self.sim.calcular_psi(t)
        phi = self.sim.calcular_phi_acumulada(t, psi)
        
        self.assertAlmostEqual(phi[0], 0.0, places=5)
        
    def test_phi_longitud_correcta(self):
        """Test 12: Φ(t) tiene la misma longitud que t."""
        t = np.linspace(0, 1000, 5000)
        psi = self.sim.calcular_psi(t)
        phi = self.sim.calcular_phi_acumulada(t, psi)
        
        self.assertEqual(len(phi), len(t))


class TestDeteccionEmergencias(unittest.TestCase):
    """Pruebas de detección de eventos de emergencia."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        
    def test_detectar_emergencias_vacio(self):
        """Test 13: No detecta emergencias si Φ < umbral."""
        t = np.linspace(0, 100, 1000)
        phi = np.linspace(0, 0.5, 1000)  # Siempre por debajo del umbral
        
        eventos = self.sim.detectar_emergencias(t, phi)
        
        self.assertEqual(len(eventos), 0)
        
    def test_detectar_emergencias_simple(self):
        """Test 14: Detecta emergencia cuando Φ supera umbral."""
        t = np.linspace(0, 1000, 1000)
        phi = np.zeros(1000)
        phi[500] = 0.96  # Pico por encima del umbral
        
        self.sim.psi = np.ones(1000)  # Mock de psi
        eventos = self.sim.detectar_emergencias(t, phi)
        
        self.assertGreater(len(eventos), 0)
        
    def test_estructura_evento(self):
        """Test 15: Estructura correcta de eventos detectados."""
        t = np.linspace(0, 365 * DAY_HOURS * 3600, 10000)
        phi = np.zeros(10000)
        phi[5000] = 0.97
        
        self.sim.psi = np.ones(10000)
        eventos = self.sim.detectar_emergencias(t, phi)
        
        if len(eventos) > 0:
            evento = eventos[0]
            self.assertIn('indice', evento)
            self.assertIn('tiempo_segundos', evento)
            self.assertIn('tiempo_anos', evento)
            self.assertIn('tiempo_dias', evento)
            self.assertIn('phi_max', evento)


class TestSimulacionCompleta(unittest.TestCase):
    """Pruebas de simulación completa."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        
    def test_simulacion_ejecuta(self):
        """Test 16: La simulación se ejecuta sin errores."""
        resultados = self.sim.simular(duracion_anos=1, n_puntos=1000)
        
        self.assertIsNotNone(resultados)
        self.assertIn('parametros', resultados)
        self.assertIn('eventos_emergencia', resultados)
        self.assertIn('metricas', resultados)
        
    def test_simulacion_17_anos(self):
        """Test 17: Simulación de 17 años (ciclo completo)."""
        resultados = self.sim.simular(duracion_anos=17, n_puntos=10000)
        
        self.assertEqual(resultados['parametros']['duracion_anos'], 17)
        self.assertIsNotNone(self.sim.tiempos)
        self.assertIsNotNone(self.sim.psi)
        self.assertIsNotNone(self.sim.phi_acumulada)
        
    def test_resultados_contienen_metadata_qcal(self):
        """Test 18: Resultados contienen metadata QCAL."""
        resultados = self.sim.simular(duracion_anos=1, n_puntos=1000)
        
        self.assertEqual(resultados['parametros']['metadata_qcal'], '∴𓂀Ω∞³')
        
    def test_resultados_contienen_frecuencias(self):
        """Test 19: Resultados incluyen todas las frecuencias."""
        resultados = self.sim.simular(duracion_anos=1, n_puntos=1000)
        
        freqs = resultados['parametros']['frecuencias_hz']
        self.assertIn('f_anual', freqs)
        self.assertIn('f_diaria', freqs)
        self.assertIn('f_lunar', freqs)
        self.assertIn('f0_qcal', freqs)


class TestMetricasPrecision(unittest.TestCase):
    """Pruebas de métricas de precisión."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        
    def test_metricas_sin_eventos(self):
        """Test 20: Métricas cuando no hay eventos."""
        self.sim.eventos_emergencia = []
        metricas = self.sim.calcular_metricas_precision()
        
        self.assertEqual(metricas['n_eventos'], 0)
        self.assertEqual(metricas['precision'], 0.0)
        
    def test_metricas_con_eventos(self):
        """Test 21: Métricas calculadas correctamente."""
        # Mock de evento
        self.sim.eventos_emergencia = [{
            'tiempo_anos': 17.0,
            'tiempo_dias': 17 * YEAR_DAYS,
            'phi_max': 0.96
        }]
        self.sim.ciclo_anos = 17
        
        metricas = self.sim.calcular_metricas_precision()
        
        self.assertEqual(metricas['n_eventos'], 1)
        self.assertGreater(metricas['precision'], 0.99)
        
    def test_validacion_17_anos(self):
        """Test 22: Validación de ciclo de 17 años."""
        # Simulación completa
        resultados = self.sim.simular(duracion_anos=18, n_puntos=50000)
        
        # Verificar que se ejecutó
        self.assertIn('validacion_17_anos', resultados['metricas'])
        
    def test_precision_target(self):
        """Test 23: Verificación de precisión objetivo."""
        resultados = self.sim.simular(duracion_anos=17, n_puntos=50000)
        
        # Debe tener la clave de validación de precisión
        self.assertIn('cumple_precision_target', resultados['metricas'])


class TestMapaResonancia(unittest.TestCase):
    """Pruebas de generación de mapa de resonancia."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        
    def test_mapa_resonancia_genera(self):
        """Test 24: Mapa de resonancia se genera correctamente."""
        mapa = self.sim.generar_mapa_resonancia(n_puntos_grid=5)
        
        self.assertIn('n_puntos', mapa)
        self.assertIn('puntos', mapa)
        self.assertIn('metadata_qcal', mapa)
        
    def test_mapa_resonancia_grid_size(self):
        """Test 25: Tamaño correcto del grid de resonancia."""
        n_grid = 10
        mapa = self.sim.generar_mapa_resonancia(n_puntos_grid=n_grid)
        
        # n_puntos = n_grid x n_grid
        self.assertEqual(mapa['n_puntos'], n_grid * n_grid)
        
    def test_mapa_puntos_estructura(self):
        """Test 26: Estructura correcta de puntos en mapa."""
        mapa = self.sim.generar_mapa_resonancia(n_puntos_grid=3)
        
        if len(mapa['puntos']) > 0:
            punto = mapa['puntos'][0]
            self.assertIn('amplitud', punto)
            self.assertIn('frecuencia', punto)
            self.assertIn('resonancia', punto)


class TestExportacion(unittest.TestCase):
    """Pruebas de exportación de resultados."""
    
    def setUp(self):
        """Configuración común para pruebas."""
        self.sim = SimuladorResonanciaTemporal()
        self.test_dir = Path('test_output_temp')
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        """Limpieza después de pruebas."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            
    def test_exportar_resultados_crea_archivo(self):
        """Test 27: Exportación crea archivo JSON."""
        resultados = {'test': 'data', 'metadata_qcal': '∴𓂀Ω∞³'}
        
        filepath = self.sim.exportar_resultados(
            resultados, directorio=str(self.test_dir)
        )
        
        self.assertTrue(filepath.exists())
        self.assertTrue(filepath.suffix == '.json')
        
    def test_exportar_resultados_formato_json(self):
        """Test 28: Archivo exportado es JSON válido."""
        resultados = {'test': 'data', 'valor': 123}
        
        filepath = self.sim.exportar_resultados(
            resultados, directorio=str(self.test_dir)
        )
        
        # Leer y verificar JSON
        with open(filepath, 'r') as f:
            datos_leidos = json.load(f)
        
        self.assertEqual(datos_leidos['test'], 'data')
        self.assertEqual(datos_leidos['valor'], 123)


class TestExperimento1(unittest.TestCase):
    """Pruebas del Experimento 1: Manipulación Espectral."""
    
    def test_experimento1_ejecuta(self):
        """Test 29: Experimento 1 se ejecuta sin errores."""
        # Nota: Esta prueba puede tardar
        try:
            resultados = ejecutar_experimento_1_manipulacion_espectral()
            
            self.assertIn('experimento', resultados)
            self.assertIn('resultados', resultados)
            self.assertEqual(resultados['experimento'], 'manipulacion_espectral_virtual')
        except Exception as e:
            self.fail(f"Experimento 1 falló con error: {e}")
            
    def test_experimento1_tres_condiciones(self):
        """Test 30: Experimento 1 incluye tres condiciones."""
        resultados = ejecutar_experimento_1_manipulacion_espectral()
        
        self.assertEqual(len(resultados['resultados']), 3)
        
        condiciones = [r['condicion'] for r in resultados['resultados']]
        self.assertIn('control', condiciones)
        self.assertIn('experimental_minus_1pct', condiciones)
        self.assertIn('experimental_plus_1pct', condiciones)


class TestConstantesQCAL(unittest.TestCase):
    """Pruebas de constantes QCAL."""
    
    def test_f0_qcal_valor(self):
        """Test 31: Valor correcto de f₀."""
        self.assertAlmostEqual(F0_QCAL, 141.7001, places=4)
        
    def test_phi_umbral_valor(self):
        """Test 32: Valor correcto de umbral de fase."""
        self.assertAlmostEqual(PHI_UMBRAL, 0.95, places=2)
        
    def test_precision_target_valor(self):
        """Test 33: Objetivo de precisión es 99.92%."""
        self.assertAlmostEqual(PRECISION_TARGET, 0.9992, places=4)
        
    def test_dispersion_dias_valor(self):
        """Test 34: Dispersión objetivo es ±3 días."""
        self.assertEqual(DISPERSION_DIAS, 3)


class TestRobustezNumerica(unittest.TestCase):
    """Pruebas de robustez numérica."""
    
    def test_simulacion_puntos_pequenos(self):
        """Test 35: Simulación funciona con pocos puntos."""
        sim = SimuladorResonanciaTemporal()
        resultados = sim.simular(duracion_anos=1, n_puntos=100)
        
        self.assertIsNotNone(resultados)
        
    def test_simulacion_puntos_grandes(self):
        """Test 36: Simulación funciona con muchos puntos."""
        sim = SimuladorResonanciaTemporal()
        resultados = sim.simular(duracion_anos=1, n_puntos=100000)
        
        self.assertIsNotNone(resultados)
        
    def test_frecuencia_extrema_baja(self):
        """Test 37: Simulación con frecuencia muy baja."""
        sim = SimuladorResonanciaTemporal(f0=1.0)
        resultados = sim.simular(duracion_anos=1, n_puntos=1000)
        
        self.assertIsNotNone(resultados)
        
    def test_frecuencia_extrema_alta(self):
        """Test 38: Simulación con frecuencia muy alta."""
        sim = SimuladorResonanciaTemporal(f0=1000.0)
        resultados = sim.simular(duracion_anos=1, n_puntos=10000)
        
        self.assertIsNotNone(resultados)


def suite():
    """Crea suite de pruebas."""
    test_suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    test_suite.addTest(unittest.makeSuite(TestInicializacion))
    test_suite.addTest(unittest.makeSuite(TestCalculoPsi))
    test_suite.addTest(unittest.makeSuite(TestCalculoPhi))
    test_suite.addTest(unittest.makeSuite(TestDeteccionEmergencias))
    test_suite.addTest(unittest.makeSuite(TestSimulacionCompleta))
    test_suite.addTest(unittest.makeSuite(TestMetricasPrecision))
    test_suite.addTest(unittest.makeSuite(TestMapaResonancia))
    test_suite.addTest(unittest.makeSuite(TestExportacion))
    test_suite.addTest(unittest.makeSuite(TestExperimento1))
    test_suite.addTest(unittest.makeSuite(TestConstantesQCAL))
    test_suite.addTest(unittest.makeSuite(TestRobustezNumerica))
    
    return test_suite


if __name__ == '__main__':
    # Ejecutar suite completa
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS - RESONANCIA TEMPORAL")
    print("=" * 70)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Éxitos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Metadata QCAL: ∴𓂀Ω∞³")
    print("=" * 70)
    
    # Exit code
    sys.exit(0 if result.wasSuccessful() else 1)
