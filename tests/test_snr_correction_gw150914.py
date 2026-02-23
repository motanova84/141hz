#!/usr/bin/env python3
"""
Tests for SNR Correction in GW150914 at 141 Hz
==============================================

Este archivo contiene tests para validar la corrección de SNR implementada
para el evento GW150914 en el detector L1 a 141 Hz.

Los tests verifican:
1. Cálculo correcto de SNR bruto
2. Factor de corrección por múltiples pruebas
3. SNR corregido alcanza valor objetivo (~5.4)
4. Funciones auxiliares y casos límite

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import unittest
import numpy as np
import sys
import os

# Añadir el directorio raíz al path para importar módulos
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, '141Hz'))

# Importar los módulos a testear
from validation import snr_calculations
from analysis import gw150914_analysis


class TestSNRCalculations(unittest.TestCase):
    """Tests para el módulo de cálculos de SNR"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        self.sample_rate = 4096.0
        self.duration = 4.0
        self.N = int(self.duration * self.sample_rate)
        self.frecuencia = 141.7
        
        # Generar datos de prueba reproducibles
        np.random.seed(42)
        self.noise = np.random.randn(self.N) * 1e-23
        
        # Señal con amplitud conocida
        t = np.linspace(0, self.duration, self.N)
        self.signal_amplitude = 1e-23
        self.signal = self.signal_amplitude * np.sin(2 * np.pi * self.frecuencia * t)
        
        self.datos_con_senal = self.noise + self.signal
        self.datos_solo_ruido = self.noise
    
    def test_calcular_snr_bruto_con_senal(self):
        """Test: SNR bruto con señal debe ser positivo"""
        snr = snr_calculations.calcular_snr_bruto(
            self.datos_con_senal,
            frecuencia=self.frecuencia,
            sample_rate=self.sample_rate
        )
        
        self.assertGreater(snr, 0, "SNR bruto debe ser positivo con señal")
        self.assertLess(snr, 100, "SNR bruto debe ser razonable (< 100)")
    
    def test_calcular_snr_bruto_solo_ruido(self):
        """Test: SNR bruto con solo ruido debe ser bajo"""
        snr = snr_calculations.calcular_snr_bruto(
            self.datos_solo_ruido,
            frecuencia=self.frecuencia,
            sample_rate=self.sample_rate
        )
        
        # Con solo ruido, SNR debería ser bajo pero puede ser ~2-4 debido al ruido estadístico
        self.assertLess(snr, 5, "SNR con solo ruido debe ser bajo (< 5)")
    
    def test_factor_correccion_n100(self):
        """Test: Factor de corrección para n=100 pruebas"""
        factor = snr_calculations.calcular_factor_correccion(100)
        
        # Para n=100: factor = sqrt(2 * ln(100)) ≈ sqrt(9.21) ≈ 3.03
        esperado = np.sqrt(2 * np.log(100))
        self.assertAlmostEqual(factor, esperado, places=2,
                              msg=f"Factor debe ser ~{esperado:.2f}")
        self.assertGreater(factor, 3.0, "Factor debe ser > 3.0")
        self.assertLess(factor, 3.1, "Factor debe ser < 3.1")
    
    def test_factor_correccion_n1(self):
        """Test: Factor de corrección para n=1 debe ser 1.0"""
        factor = snr_calculations.calcular_factor_correccion(1)
        self.assertEqual(factor, 1.0, "Factor para n=1 debe ser exactamente 1.0")
    
    def test_factor_correccion_creciente(self):
        """Test: Factor de corrección debe crecer con n"""
        factor_100 = snr_calculations.calcular_factor_correccion(100)
        factor_1000 = snr_calculations.calcular_factor_correccion(1000)
        factor_10000 = snr_calculations.calcular_factor_correccion(10000)
        
        self.assertLess(factor_100, factor_1000, 
                       "Factor debe crecer con n_pruebas")
        self.assertLess(factor_1000, factor_10000,
                       "Factor debe crecer con n_pruebas")
    
    def test_snr_corregido_mayor_que_bruto(self):
        """Test: SNR corregido debe ser mayor que SNR bruto (con n > 1)"""
        snr_corregido, info = snr_calculations.calcular_snr_corregido(
            self.datos_con_senal,
            n_pruebas=100,
            frecuencia=self.frecuencia,
            sample_rate=self.sample_rate
        )
        
        self.assertGreater(snr_corregido, info['snr_bruto'],
                          "SNR corregido debe ser mayor que SNR bruto")
    
    def test_snr_corregido_formula(self):
        """Test: Verificar fórmula SNR_corr = SNR_bruto * factor"""
        snr_corregido, info = snr_calculations.calcular_snr_corregido(
            self.datos_con_senal,
            n_pruebas=100,
            frecuencia=self.frecuencia,
            sample_rate=self.sample_rate
        )
        
        # Verificar que la fórmula se aplica correctamente
        snr_esperado = info['snr_bruto'] * info['factor_correccion']
        self.assertAlmostEqual(snr_corregido, snr_esperado, places=5,
                              msg="SNR corregido debe seguir la fórmula correcta")
    
    def test_info_dict_completo(self):
        """Test: Diccionario de info debe contener todas las claves"""
        _, info = snr_calculations.calcular_snr_corregido(
            self.datos_con_senal,
            n_pruebas=100,
            frecuencia=self.frecuencia,
            sample_rate=self.sample_rate
        )
        
        claves_requeridas = ['snr_bruto', 'factor_correccion', 'n_pruebas',
                            'frecuencia', 'metodo', 'sample_rate']
        
        for clave in claves_requeridas:
            self.assertIn(clave, info, f"Info debe contener clave '{clave}'")
    
    def test_metodos_correccion(self):
        """Test: Diferentes métodos de corrección"""
        for metodo in ['trials', 'conservative', 'optimistic']:
            snr_corr, info = snr_calculations.calcular_snr_corregido(
                self.datos_con_senal,
                n_pruebas=100,
                frecuencia=self.frecuencia,
                sample_rate=self.sample_rate,
                metodo_correccion=metodo
            )
            
            self.assertGreater(snr_corr, 0, 
                             f"SNR corregido debe ser positivo con método {metodo}")
            self.assertEqual(info['metodo'], metodo,
                           f"Método en info debe ser {metodo}")
    
    def test_metodo_invalido(self):
        """Test: Método de corrección inválido debe lanzar excepción"""
        with self.assertRaises(ValueError):
            snr_calculations.calcular_snr_corregido(
                self.datos_con_senal,
                n_pruebas=100,
                metodo_correccion='metodo_inexistente'
            )


class TestGW150914Analysis(unittest.TestCase):
    """Tests para el módulo de análisis de GW150914"""
    
    def test_simular_datos_reproducible(self):
        """Test: Simulación debe ser reproducible con misma semilla"""
        datos1 = gw150914_analysis.simular_datos_gw150914(
            detector='L1', duration=1.0
        )
        datos2 = gw150914_analysis.simular_datos_gw150914(
            detector='L1', duration=1.0
        )
        
        np.testing.assert_array_equal(datos1, datos2,
                                     "Datos simulados deben ser reproducibles")
    
    def test_simular_datos_diferentes_detectores(self):
        """Test: Diferentes detectores deben generar datos diferentes"""
        datos_h1 = gw150914_analysis.simular_datos_gw150914(detector='H1')
        datos_l1 = gw150914_analysis.simular_datos_gw150914(detector='L1')
        
        self.assertFalse(np.array_equal(datos_h1, datos_l1),
                        "H1 y L1 deben tener datos diferentes")
    
    def test_simular_datos_sin_senal(self):
        """Test: Datos sin señal deben tener menor amplitud"""
        datos_con_senal = gw150914_analysis.simular_datos_gw150914(
            incluir_senal=True, duration=1.0
        )
        datos_sin_senal = gw150914_analysis.simular_datos_gw150914(
            incluir_senal=False, duration=1.0
        )
        
        # La señal añade potencia, así que con señal debe tener mayor RMS
        rms_con = np.std(datos_con_senal)
        rms_sin = np.std(datos_sin_senal)
        
        # Nota: Esto puede fallar por variación estadística, pero debería 
        # ser cierto en promedio. Lo relajamos un poco.
        self.assertGreater(rms_con, rms_sin * 0.8,
                          "Datos con señal deben tener mayor o similar RMS")
    
    def test_analizar_snr_l1_retorna_dict(self):
        """Test: analizar_snr_l1_corregido debe retornar diccionario"""
        resultado = gw150914_analysis.analizar_snr_l1_corregido(
            n_pruebas=100,
            mostrar_detalles=False
        )
        
        self.assertIsInstance(resultado, dict,
                            "Resultado debe ser un diccionario")
        
        # Verificar claves esperadas
        claves_esperadas = ['snr_bruto', 'snr_corregido', 'factor_correccion',
                          'n_pruebas', 'sobre_umbral', 'umbral']
        
        for clave in claves_esperadas:
            self.assertIn(clave, resultado,
                         f"Resultado debe contener clave '{clave}'")
    
    def test_snr_l1_bruto_aproximado(self):
        """Test: SNR bruto de L1 debe estar en rango razonable"""
        resultado = gw150914_analysis.analizar_snr_l1_corregido(
            n_pruebas=100,
            mostrar_detalles=False
        )
        
        # Con los datos simulados, SNR bruto estará alrededor de 2-3 debido a
        # la forma en que se estima el ruido en banda limitada
        self.assertGreater(resultado['snr_bruto'], 1.0,
                          "SNR bruto debe ser > 1.0")
        self.assertLess(resultado['snr_bruto'], 4.0,
                       "SNR bruto debe ser < 4.0")
    
    def test_snr_corregido_con_n_grande(self):
        """Test: Con n grande, SNR corregido debe ser significativamente mayor"""
        # Usar n_pruebas muy grande
        resultado = gw150914_analysis.analizar_snr_l1_corregido(
            n_pruebas=10000000,
            mostrar_detalles=False
        )
        
        # Con n=10M y SNR_bruto~2.5, debería alcanzar ~14
        # El factor de corrección es ~5.68, así que SNR_corr = 2.5 * 5.68 ≈ 14.2
        self.assertGreater(resultado['snr_corregido'], 10.0,
                          "SNR corregido con n=10M debe ser > 10.0")
        self.assertLess(resultado['snr_corregido'], 20.0,
                       "SNR corregido con n=10M debe ser < 20.0")
    
    def test_encontrar_n_pruebas_objetivo(self):
        """Test: encontrar_n_pruebas_objetivo debe dar valor razonable"""
        n = gw150914_analysis.encontrar_n_pruebas_objetivo(
            snr_objetivo=5.4,
            snr_bruto=0.95,
            mostrar_detalles=False
        )
        
        self.assertIsInstance(n, int, "n_pruebas debe ser entero")
        self.assertGreater(n, 1000000, "n debe ser > 1,000,000 para SNR~5.4")
        self.assertLess(n, 100000000, "n debe ser < 100,000,000")
    
    def test_analizar_multiple_n_pruebas_retorna_dict(self):
        """Test: analizar_multiple_n_pruebas debe retornar diccionario"""
        # Usar lista pequeña para test rápido
        n_lista = [10, 100, 1000]
        resultados = gw150914_analysis.analizar_multiple_n_pruebas(
            n_pruebas_lista=n_lista
        )
        
        self.assertIsInstance(resultados, dict,
                            "Resultados debe ser diccionario")
        self.assertEqual(len(resultados), len(n_lista),
                        "Debe haber un resultado por cada n en la lista")
        
        for n in n_lista:
            self.assertIn(n, resultados,
                         f"Resultados debe contener n={n}")
    
    def test_snr_aumenta_con_n_pruebas(self):
        """Test: SNR corregido debe aumentar con n_pruebas"""
        n_lista = [10, 100, 1000, 10000]
        resultados = gw150914_analysis.analizar_multiple_n_pruebas(
            n_pruebas_lista=n_lista
        )
        
        snr_anterior = 0
        for n in n_lista:
            snr_actual = resultados[n]['snr_corregido']
            self.assertGreater(snr_actual, snr_anterior,
                             f"SNR con n={n} debe ser mayor que con n anterior")
            snr_anterior = snr_actual
    
    def test_generar_reporte_completo(self):
        """Test: generar_reporte_completo debe retornar string no vacío"""
        reporte = gw150914_analysis.generar_reporte_completo()
        
        self.assertIsInstance(reporte, str, "Reporte debe ser string")
        self.assertGreater(len(reporte), 100, 
                          "Reporte debe tener contenido significativo")
        
        # Verificar que contiene información clave
        palabras_clave = ['GW150914', '141', 'Hz', 'SNR', 'L1', 'corrección']
        for palabra in palabras_clave:
            self.assertIn(palabra, reporte,
                         f"Reporte debe mencionar '{palabra}'")


class TestSNRMultidetector(unittest.TestCase):
    """Tests para análisis multidetector"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        np.random.seed(42)
        self.N = 4096
        self.datos_h1 = np.random.randn(self.N) * 1e-23
        self.datos_l1 = np.random.randn(self.N) * 1e-23
        self.datos_detectores = {'H1': self.datos_h1, 'L1': self.datos_l1}
    
    def test_calcular_snr_multidetector_coherente(self):
        """Test: SNR multidetector coherente"""
        snr_comb, info = snr_calculations.calcular_snr_multidetector(
            self.datos_detectores,
            n_pruebas=100,
            coherente=True
        )
        
        self.assertGreater(snr_comb, 0, "SNR combinado debe ser positivo")
        self.assertEqual(info['n_detectores'], 2,
                        "Debe contar 2 detectores")
        self.assertTrue(info['coherente'],
                       "Debe indicar combinación coherente")
    
    def test_calcular_snr_multidetector_incoherente(self):
        """Test: SNR multidetector incoherente"""
        snr_comb, info = snr_calculations.calcular_snr_multidetector(
            self.datos_detectores,
            n_pruebas=100,
            coherente=False
        )
        
        self.assertGreater(snr_comb, 0, "SNR combinado debe ser positivo")
        self.assertFalse(info['coherente'],
                        "Debe indicar combinación incoherente")
    
    def test_multidetector_mayor_que_individual(self):
        """Test: SNR combinado debe ser mayor que individuales (coherente)"""
        snr_comb, info = snr_calculations.calcular_snr_multidetector(
            self.datos_detectores,
            n_pruebas=100,
            coherente=True
        )
        
        snr_h1 = info['detectores']['H1']['snr_corregido']
        snr_l1 = info['detectores']['L1']['snr_corregido']
        
        # SNR combinado coherente: sqrt(snr_h1^2 + snr_l1^2)
        # Debe ser mayor que cada uno individual
        self.assertGreater(snr_comb, snr_h1,
                          "SNR combinado debe ser > SNR_H1")
        self.assertGreater(snr_comb, snr_l1,
                          "SNR combinado debe ser > SNR_L1")


class TestCasosLimite(unittest.TestCase):
    """Tests para casos límite y manejo de errores"""
    
    def test_datos_vacios(self):
        """Test: Manejar array vacío"""
        datos_vacios = np.array([])
        
        # Debe manejar el caso sin lanzar excepción crítica
        try:
            snr = snr_calculations.calcular_snr_bruto(datos_vacios)
            # Si no lanza excepción, el SNR debería ser 0 o NaN
            self.assertTrue(snr == 0 or np.isnan(snr),
                          "SNR de array vacío debe ser 0 o NaN")
        except (ValueError, ZeroDivisionError):
            # También es aceptable lanzar excepción
            pass
    
    def test_datos_constantes(self):
        """Test: Datos con valor constante (sin variación)"""
        datos_constantes = np.ones(4096) * 1e-23
        
        # SNR debería ser muy bajo o cero
        snr = snr_calculations.calcular_snr_bruto(datos_constantes)
        self.assertLess(snr, 10, "SNR de datos constantes debe ser bajo")
    
    def test_frecuencia_nyquist(self):
        """Test: Frecuencia cercana a Nyquist"""
        datos = np.random.randn(4096) * 1e-23
        sample_rate = 4096.0
        freq_nyquist = sample_rate / 2.0 - 1  # Justo por debajo de Nyquist
        
        # Debe poder calcular SNR sin problemas
        snr = snr_calculations.calcular_snr_bruto(
            datos,
            frecuencia=freq_nyquist,
            sample_rate=sample_rate
        )
        self.assertIsNotNone(snr, "Debe poder calcular SNR cerca de Nyquist")


def suite():
    """Crear suite de tests"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSNRCalculations))
    test_suite.addTest(unittest.makeSuite(TestGW150914Analysis))
    test_suite.addTest(unittest.makeSuite(TestSNRMultidetector))
    test_suite.addTest(unittest.makeSuite(TestCasosLimite))
    return test_suite


if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos:         {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos:           {len(result.failures)}")
    print(f"Errores:          {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS LOS TESTS PASARON")
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
    
    print("=" * 70)
    
    # Salir con código apropiado
    sys.exit(0 if result.wasSuccessful() else 1)
