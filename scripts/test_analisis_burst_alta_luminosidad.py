#!/usr/bin/env python3
"""
Tests para Análisis de Bursts de Alta Luminosidad en HL-LHC
============================================================

Tests unitarios para validar el módulo analisis_burst_alta_luminosidad.py
"""

import unittest
import numpy as np
from scipy import stats
import sys
import os

# Añadir directorio scripts al path
sys.path.insert(0, os.path.dirname(__file__))

from analisis_burst_alta_luminosidad import AnalisisBurstAltaLuminosidad


class TestAnalisisBurstAltaLuminosidad(unittest.TestCase):
    """Tests para la clase AnalisisBurstAltaLuminosidad"""
    
    def setUp(self):
        """Configurar instancia de análisis para tests"""
        self.analisis = AnalisisBurstAltaLuminosidad(
            luminosidad_integrada=3000.0,
            duracion_anos=10.0,
            n_eventos_total=300000
        )
    
    def test_inicializacion(self):
        """Test de inicialización correcta"""
        self.assertEqual(self.analisis.luminosidad_integrada, 3000.0)
        self.assertEqual(self.analisis.duracion_anos, 10.0)
        self.assertEqual(self.analisis.n_eventos_total, 300000)
        self.assertAlmostEqual(self.analisis.f0, 141.7001, places=4)
        self.assertAlmostEqual(self.analisis.T0 * 1000, 7.06, places=2)
    
    def test_calcular_tasa_eventos(self):
        """Test de cálculo de tasa de eventos"""
        tasa = self.analisis.calcular_tasa_eventos()
        
        # Verificar que la tasa es aproximadamente 10⁻³ Hz
        self.assertIsNotNone(tasa['tasa_hz'])
        self.assertAlmostEqual(tasa['tasa_hz'], 1e-3, delta=1e-4)
        
        # Verificar tiempo entre eventos (~1000 s)
        self.assertAlmostEqual(tasa['tiempo_entre_eventos_s'], 1000, delta=100)
        
        # Verificar que todos los campos requeridos están presentes
        self.assertIn('eventos_por_segundo', tasa)
        self.assertIn('eventos_por_hora', tasa)
        self.assertIn('eventos_por_dia', tasa)
    
    def test_probabilidad_n_eventos_burst(self):
        """Test de probabilidad de Poisson para n eventos"""
        # Para burst de 100 ms con tasa 10⁻³ Hz
        # λ = 10⁻³ × 0.1 = 10⁻⁴
        
        # P(N=0) debe ser muy cercano a 1
        p_0 = self.analisis.probabilidad_n_eventos_burst(0, 100.0)
        self.assertGreater(p_0, 0.999)
        
        # P(N=1) debe ser muy pequeño
        p_1 = self.analisis.probabilidad_n_eventos_burst(1, 100.0)
        self.assertLess(p_1, 0.001)
        
        # P(N=2) debe ser extremadamente pequeño
        p_2 = self.analisis.probabilidad_n_eventos_burst(2, 100.0)
        self.assertLess(p_2, 1e-6)
        
        # La suma de probabilidades debe acercarse a 1
        suma = sum(self.analisis.probabilidad_n_eventos_burst(n, 100.0) 
                  for n in range(10))
        self.assertAlmostEqual(suma, 1.0, places=6)
    
    def test_probabilidad_multiples_eventos(self):
        """Test de probabilidad de 2+ eventos"""
        probs = self.analisis.probabilidad_multiples_eventos(100.0)
        
        # Verificar que lambda es correcto (10⁻³ × 0.1 = 10⁻⁴)
        self.assertAlmostEqual(probs['lambda'], 1e-4, delta=1e-5)
        
        # P(≥2) debe ser aproximadamente (λ²/2) según el problem statement
        # Para λ ≈ 10⁻⁴: (λ)² / 2 ≈ 5×10⁻⁹
        self.assertAlmostEqual(probs['p_ge_2_aproximacion'], 5e-9, delta=1e-9)
        
        # Verificar que la suma P(0) + P(1) + P(≥2) = 1
        suma = probs['p_0_eventos'] + probs['p_1_evento'] + probs['p_ge_2_eventos']
        self.assertAlmostEqual(suma, 1.0, places=10)
        
        # P(≥2) debe ser consistente con la aproximación
        self.assertLess(abs(probs['p_ge_2_eventos'] - probs['p_ge_2_aproximacion']), 1e-10)
    
    def test_calcular_numero_bursts(self):
        """Test de cálculo del número de bursts"""
        bursts = self.analisis.calcular_numero_bursts(100.0)
        
        # 10 años / 100 ms ≈ 3×10⁹ bursts
        self.assertIsNotNone(bursts['n_bursts'])
        self.assertAlmostEqual(bursts['n_bursts'], 3e9, delta=2e8)
        
        # Verificar que duración está correcta
        self.assertEqual(bursts['duracion_burst_ms'], 100.0)
        self.assertEqual(bursts['duracion_burst_s'], 0.1)
        
        # Verificar bursts por día
        self.assertGreater(bursts['bursts_por_dia'], 8e5)  # ~864,000
    
    def test_eventos_esperados_coincidentes(self):
        """Test de eventos esperados con coincidencias"""
        coincidencias = self.analisis.eventos_esperados_coincidentes(100.0)
        
        # N_expected = N_bursts × P(≥2)
        # ≈ 3×10⁹ × 5×10⁻⁹ ≈ 15
        self.assertIsNotNone(coincidencias['n_esperado_coincidencias'])
        self.assertAlmostEqual(coincidencias['n_esperado_coincidencias'], 15, delta=2)
        
        # Verificar campos
        self.assertIn('n_bursts_total', coincidencias)
        self.assertIn('p_ge_2_eventos', coincidencias)
        self.assertEqual(coincidencias['duracion_burst_ms'], 100.0)
    
    def test_correlacion_psi_inducida(self):
        """Test de correlación Ψ en Δt = 7.06 ms"""
        correlacion = self.analisis.correlacion_psi_inducida(100.0)
        
        # Verificar que T₀ = 7.06 ms
        self.assertAlmostEqual(correlacion['T0_ms'], 7.06, places=2)
        
        # Verificar que N_correlated está calculado
        self.assertIsNotNone(correlacion['n_eventos_correlacionados'])
        self.assertGreater(correlacion['n_eventos_correlacionados'], 0)
        
        # Verificar que p-value está presente
        self.assertIn('p_value_significancia', correlacion)
        self.assertGreaterEqual(correlacion['p_value_significancia'], 0)
        self.assertLessEqual(correlacion['p_value_significancia'], 1)
        
        # Verificar campos de significancia
        self.assertIn('significativo_3sigma', correlacion)
        self.assertIn('significativo_5sigma', correlacion)
    
    def test_correlacion_psi_probabilidad_custom(self):
        """Test con probabilidad de correlación personalizada"""
        # Probar con diferentes probabilidades
        for p_corr in [0.1, 0.5, 1.0]:
            correlacion = self.analisis.correlacion_psi_inducida(
                100.0, 
                probabilidad_correlacion=p_corr
            )
            
            self.assertAlmostEqual(
                correlacion['probabilidad_correlacion'], 
                p_corr, 
                places=6
            )
            
            # N_correlated debe escalar con probabilidad
            if p_corr > 0:
                self.assertGreater(correlacion['n_eventos_correlacionados'], 0)
    
    def test_analisis_completo_estructura(self):
        """Test de estructura del análisis completo"""
        resultados = self.analisis.analisis_completo(duracion_burst_ms=100.0)
        
        # Verificar que todas las secciones están presentes
        self.assertIn('tasa_eventos', resultados)
        self.assertIn('probabilidades_burst', resultados)
        self.assertIn('numero_bursts', resultados)
        self.assertIn('coincidencias_esperadas', resultados)
        self.assertIn('correlacion_psi', resultados)
        
        # Verificar coherencia entre secciones
        tasa = resultados['tasa_eventos']['tasa_hz']
        self.assertAlmostEqual(tasa, 1e-3, places=3)
    
    def test_scan_duraciones_burst(self):
        """Test de scan de duraciones"""
        duraciones = np.array([10.0, 50.0, 100.0, 200.0])
        resultados = self.analisis.scan_duraciones_burst(duraciones)
        
        # Verificar estructura
        self.assertIn('duraciones_ms', resultados)
        self.assertIn('n_esperados', resultados)
        self.assertIn('n_correlacionados', resultados)
        self.assertIn('p_values', resultados)
        
        # Verificar tamaños
        self.assertEqual(len(resultados['n_esperados']), len(duraciones))
        self.assertEqual(len(resultados['n_correlacionados']), len(duraciones))
        self.assertEqual(len(resultados['p_values']), len(duraciones))
        
        # Verificar que N_esperados crece con duración
        self.assertLess(resultados['n_esperados'][0], resultados['n_esperados'][-1])
    
    def test_valores_problem_statement(self):
        """Test específico de valores del problem statement"""
        # Verificar cálculos exactos del problem statement
        
        # 1. Tasa ≈ 10⁻³ Hz
        tasa = self.analisis.calcular_tasa_eventos()
        self.assertAlmostEqual(tasa['tasa_hz'], 1e-3, delta=1e-4)
        
        # 2. P(≥2 eventos en 100 ms) ≈ 5×10⁻⁹
        probs = self.analisis.probabilidad_multiples_eventos(100.0)
        self.assertAlmostEqual(probs['p_ge_2_aproximacion'], 5e-9, delta=1e-9)
        
        # 3. N_bursts en 10 años ≈ 3×10⁹
        bursts = self.analisis.calcular_numero_bursts(100.0)
        self.assertAlmostEqual(bursts['n_bursts'], 3e9, delta=2e8)
        
        # 4. N_expected ≈ 15
        coincidencias = self.analisis.eventos_esperados_coincidentes(100.0)
        self.assertAlmostEqual(coincidencias['n_esperado_coincidencias'], 15, delta=2)
    
    def test_limites_duracion_burst(self):
        """Test de comportamiento en límites de duración"""
        # Burst muy corto (1 ms)
        probs_corto = self.analisis.probabilidad_multiples_eventos(1.0)
        self.assertLess(probs_corto['lambda'], 1e-5)
        
        # Burst muy largo (1000 ms = 1 s)
        probs_largo = self.analisis.probabilidad_multiples_eventos(1000.0)
        self.assertGreater(probs_largo['lambda'], 1e-4)
        
        # Burst igual al período T₀ (7.06 ms)
        probs_t0 = self.analisis.probabilidad_multiples_eventos(
            self.analisis.T0 * 1000
        )
        self.assertIsNotNone(probs_t0['p_ge_2_eventos'])
    
    def test_consistencia_estadistica(self):
        """Test de consistencia estadística general"""
        # Para múltiples duraciones, verificar que:
        # - Probabilidades suman 1
        # - N_esperados es positivo y finito
        # - p-values están en [0, 1]
        
        duraciones = [10.0, 50.0, 100.0, 200.0]
        
        for dur in duraciones:
            # Probabilidades
            probs = self.analisis.probabilidad_multiples_eventos(dur)
            suma = (probs['p_0_eventos'] + 
                   probs['p_1_evento'] + 
                   probs['p_ge_2_eventos'])
            self.assertAlmostEqual(suma, 1.0, places=10)
            
            # Eventos esperados
            coincidencias = self.analisis.eventos_esperados_coincidentes(dur)
            self.assertGreater(coincidencias['n_esperado_coincidencias'], 0)
            self.assertTrue(np.isfinite(coincidencias['n_esperado_coincidencias']))
            
            # P-values
            correlacion = self.analisis.correlacion_psi_inducida(dur)
            p_val = correlacion['p_value_significancia']
            self.assertGreaterEqual(p_val, 0)
            self.assertLessEqual(p_val, 1)
    
    def test_propiedades_fisica(self):
        """Test de propiedades físicas razonables"""
        # f₀ = 141.7001 Hz debe dar T₀ ≈ 7.06 ms
        self.assertAlmostEqual(1000.0 / self.analisis.f0, 7.06, places=2)
        
        # Duración total debe ser 10 años en segundos
        self.assertAlmostEqual(
            self.analisis.duracion_total_s,
            10 * 3.15e7,
            delta=1e6
        )
        
        # Tasa × tiempo total = número de eventos
        tasa_calculada = self.analisis.n_eventos_total / self.analisis.duracion_total_s
        self.assertAlmostEqual(self.analisis.tasa_hz, tasa_calculada, places=10)


class TestCasosEspeciales(unittest.TestCase):
    """Tests para casos especiales y edge cases"""
    
    def test_analisis_diferentes_luminosidades(self):
        """Test con diferentes luminosidades integradas"""
        luminosidades = [1000.0, 3000.0, 6000.0]
        
        for lumi in luminosidades:
            analisis = AnalisisBurstAltaLuminosidad(
                luminosidad_integrada=lumi,
                duracion_anos=10.0,
                n_eventos_total=100000 * (lumi / 1000.0)  # Escalar con lumi
            )
            
            tasa = analisis.calcular_tasa_eventos()
            self.assertGreater(tasa['tasa_hz'], 0)
    
    def test_analisis_diferentes_duraciones(self):
        """Test con diferentes duraciones del experimento"""
        duraciones = [5.0, 10.0, 20.0]
        
        for dur_anos in duraciones:
            analisis = AnalisisBurstAltaLuminosidad(
                luminosidad_integrada=3000.0,
                duracion_anos=dur_anos,
                n_eventos_total=300000
            )
            
            # Tasa debe escalar inversamente con duración (eventos fijos)
            tasa = analisis.calcular_tasa_eventos()
            expected_rate = 300000 / (dur_anos * 3.15e7)
            self.assertAlmostEqual(tasa['tasa_hz'], expected_rate, delta=1e-5)
            
            # Pero número de bursts debe escalar con duración
            bursts = analisis.calcular_numero_bursts(100.0)
            # Bursts = (duracion_total_s) / (duracion_burst_s)
            # = (dur_anos * 3.15e7) / (0.1)
            expected_bursts = (dur_anos * 3.15e7) / 0.1
            self.assertAlmostEqual(
                bursts['n_bursts'],
                expected_bursts,
                delta=2e8
            )
    
    def test_robustez_numerica(self):
        """Test de robustez numérica con valores extremos"""
        analisis = AnalisisBurstAltaLuminosidad()
        
        # Burst extremadamente corto
        probs_mini = analisis.probabilidad_multiples_eventos(0.001)  # 1 μs
        self.assertTrue(np.isfinite(probs_mini['lambda']))
        
        # Burst muy largo
        probs_maxi = analisis.probabilidad_multiples_eventos(10000.0)  # 10 s
        self.assertTrue(np.isfinite(probs_maxi['lambda']))


def run_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("TESTS - Análisis de Bursts de Alta Luminosidad HL-LHC")
    print("="*70 + "\n")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir tests
    suite.addTests(loader.loadTestsFromTestCase(TestAnalisisBurstAltaLuminosidad))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosEspeciales))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("\n❌ ALGUNOS TESTS FALLARON")
        return 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
