#!/usr/bin/env python3
"""
Tests para el Protocolo de Validación Experimental QCAL

Verifica el correcto funcionamiento de todas las fases del protocolo.

Autor: José Manuel Mota Burruezo (JMMB)
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from experimental import (
    # Fase I
    extraer_estado_psi,
    calcular_coherencia,
    test_estructura_grupo_SU,
    analizar_geodesicas,
    analisis_estadistico_SU,
    # Fase II
    construir_campo_emocional,
    calcular_tensor_stress_energia,
    calcular_curvatura_emocional,
    # Fase III
    experimento_red_social,
    analizar_efectos_red,
    # Fase IV
    meta_analisis_QCAL,
    generar_roadmap_validacion
)


class TestFase1SuPsi(unittest.TestCase):
    """Tests para Fase I: Validación de SU(Ψ)"""
    
    def setUp(self):
        """Configuración inicial"""
        np.random.seed(42)
        self.señal_eeg = np.random.randn(4, 100)
    
    def test_extraer_estado_psi(self):
        """Test extracción de estado cuántico"""
        psi = extraer_estado_psi(self.señal_eeg, n_componentes=4)
        
        # Verificar forma
        self.assertEqual(psi.shape, (4,))
        
        # Verificar que es complejo
        self.assertTrue(np.iscomplexobj(psi))
        
        # Verificar normalización
        norma = np.linalg.norm(psi)
        self.assertAlmostEqual(norma, 1.0, places=5)
    
    def test_calcular_coherencia(self):
        """Test cálculo de coherencia"""
        psi = extraer_estado_psi(self.señal_eeg)
        coherencia = calcular_coherencia(psi)
        
        # Coherencia debe estar en [0, 1]
        self.assertGreaterEqual(coherencia, 0.0)
        self.assertLessEqual(coherencia, 1.0)
    
    def test_estructura_grupo_SU(self):
        """Test verificación de estructura de grupo SU(n)"""
        # Generar trayectoria
        trayectoria = []
        for i in range(10):
            señal = np.random.randn(4, 100)
            psi = extraer_estado_psi(señal)
            trayectoria.append(psi)
        
        # Test de estructura
        resultado = test_estructura_grupo_SU(trayectoria)
        
        # Verificar claves esperadas
        self.assertIn('preservacion_norma', resultado)
        self.assertIn('unitariedad', resultado)
        self.assertIn('cerradura', resultado)
        self.assertIn('algebra_lie', resultado)
        self.assertIn('cumple_SU_n', resultado)
        
        # Verificar que preservación de norma es booleano
        self.assertIsInstance(resultado['preservacion_norma'], bool)
    
    def test_analizar_geodesicas(self):
        """Test análisis de geodésicas"""
        # Generar trayectoria
        trayectoria = []
        for i in range(5):
            señal = np.random.randn(4, 100)
            psi = extraer_estado_psi(señal)
            trayectoria.append(psi)
        
        resultado = analizar_geodesicas(trayectoria)
        
        # Verificar claves
        self.assertIn('curvatura_media', resultado)
        self.assertIn('es_geodesica', resultado)
        self.assertIn('longitud_camino', resultado)
        
        # Verificar tipos
        self.assertIsInstance(resultado['es_geodesica'], bool)
        self.assertGreaterEqual(resultado['longitud_camino'], 0)
    
    def test_analisis_estadistico(self):
        """Test análisis estadístico comparativo"""
        # Generar datos
        datos_control = []
        datos_meditadores = []
        
        for _ in range(3):
            traj_control = [extraer_estado_psi(np.random.randn(4, 100)) for _ in range(5)]
            traj_meditador = [extraer_estado_psi(np.random.randn(4, 100)) for _ in range(5)]
            datos_control.append(traj_control)
            datos_meditadores.append(traj_meditador)
        
        resultado = analisis_estadistico_SU(datos_control, datos_meditadores)
        
        # Verificar estructura
        self.assertIn('coherencia', resultado)
        self.assertIn('estabilidad_SU', resultado)
        self.assertIn('conclusion', resultado)


class TestFase2TensorStress(unittest.TestCase):
    """Tests para Fase II: Validación de T_μν(Φ)"""
    
    def setUp(self):
        """Configuración inicial"""
        np.random.seed(42)
        self.datos_multisensor = {
            'eda': np.random.rand(100),
            'hrv': np.random.rand(100),
            'amigdala': np.random.rand(100),
            'autorreporte': np.random.rand(100)
        }
    
    def test_construir_campo_emocional(self):
        """Test construcción de campo emocional"""
        Phi = construir_campo_emocional(self.datos_multisensor)
        
        # Verificar forma
        self.assertEqual(len(Phi), 100)
        
        # Verificar que está normalizado
        self.assertGreaterEqual(np.min(Phi), 0.0)
        self.assertLessEqual(np.max(Phi), 1.0)
    
    def test_calcular_tensor_stress_energia(self):
        """Test cálculo del tensor T_μν"""
        Phi = construir_campo_emocional(self.datos_multisensor)
        Phi_3d = Phi.reshape(-1, 1, 1)
        
        T_μν = calcular_tensor_stress_energia(Phi_3d)
        
        # Verificar forma: (4, 4, tiempo, x, y)
        self.assertEqual(T_μν.shape[0], 4)
        self.assertEqual(T_μν.shape[1], 4)
        
        # Verificar simetría
        for mu in range(4):
            for nu in range(4):
                np.testing.assert_array_almost_equal(
                    T_μν[mu, nu],
                    T_μν[nu, mu]
                )
    
    def test_calcular_curvatura_emocional(self):
        """Test cálculo de curvatura"""
        Phi = construir_campo_emocional(self.datos_multisensor)
        Phi_2d = Phi.reshape(-1, 1)
        
        resultado = calcular_curvatura_emocional(Phi_2d)
        
        # Verificar claves
        self.assertIn('curvatura', resultado)
        self.assertIn('singularidades', resultado)
        self.assertIn('num_singularidades', resultado)
        self.assertIn('max_curvatura', resultado)
        
        # Verificar tipos
        self.assertIsInstance(resultado['num_singularidades'], (int, np.integer))
        self.assertGreaterEqual(resultado['num_singularidades'], 0)


class TestFase3RedSocial(unittest.TestCase):
    """Tests para Fase III: Validación a Nivel Colectivo"""
    
    def test_experimento_red_social(self):
        """Test creación de experimento de red"""
        red, protocolo, simulador = experimento_red_social()
        
        # Verificar red
        self.assertEqual(len(red.nodes()), 100)
        self.assertGreater(len(red.edges()), 0)
        
        # Verificar protocolo
        self.assertIsInstance(protocolo, str)
        self.assertIn('141.7 Hz', protocolo)
        
        # Verificar que simulador es callable
        self.assertTrue(callable(simulador))
    
    def test_simular_propagacion(self):
        """Test simulación de propagación"""
        red, _, simulador = experimento_red_social()
        
        # Ejecutar simulación corta
        historia = simulador(red, num_pasos=10)
        
        # Verificar historia
        self.assertEqual(len(historia), 10)
        self.assertEqual(len(historia[0]), 100)  # 100 nodos
    
    def test_analizar_efectos_red(self):
        """Test análisis de efectos de red"""
        red, _, simulador = experimento_red_social()
        historia = simulador(red, num_pasos=20)
        
        resultado = analizar_efectos_red(historia, red)
        
        # Verificar claves
        self.assertIn('T00_reduccion_experimental', resultado)
        self.assertIn('T00_reduccion_control', resultado)
        self.assertIn('distancia_influencia_caracteristica', resultado)
        self.assertIn('interpretacion', resultado)
        
        # Verificar valores razonables
        self.assertGreater(resultado['T00_reduccion_experimental'], 0)
        self.assertGreater(resultado['T00_reduccion_control'], 0)


class TestFase4MetaAnalisis(unittest.TestCase):
    """Tests para Fase IV: Meta-Análisis y Síntesis"""
    
    def test_meta_analisis_QCAL(self):
        """Test meta-análisis"""
        resultado = meta_analisis_QCAL()
        
        # Verificar claves principales
        self.assertIn('efecto_combinado_d', resultado)
        self.assertIn('IC_95', resultado)
        self.assertIn('heterogeneidad_I2', resultado)
        self.assertIn('N_total', resultado)
        self.assertIn('conclusion_final', resultado)
        
        # Verificar valores razonables
        self.assertGreater(resultado['efecto_combinado_d'], 0)
        self.assertEqual(len(resultado['IC_95']), 2)
        self.assertGreaterEqual(resultado['heterogeneidad_I2'], 0)
        self.assertLessEqual(resultado['heterogeneidad_I2'], 100)
    
    def test_generar_roadmap(self):
        """Test generación de roadmap"""
        roadmap = generar_roadmap_validacion()
        
        # Verificar estructura
        self.assertIn('Año_1', roadmap)
        self.assertIn('Año_2', roadmap)
        self.assertIn('Año_3', roadmap)
        self.assertIn('presupuesto_total', roadmap)
        self.assertIn('duracion_total', roadmap)
        
        # Verificar que cada año tiene fases
        self.assertIn('Q1', roadmap['Año_1'])
        self.assertIn('Q2', roadmap['Año_1'])


class TestIntegracion(unittest.TestCase):
    """Tests de integración del protocolo completo"""
    
    def test_flujo_completo_simplificado(self):
        """Test del flujo completo con datos mínimos"""
        np.random.seed(42)
        
        # Fase I - datos mínimos
        trayectoria = [
            extraer_estado_psi(np.random.randn(4, 100))
            for _ in range(5)
        ]
        resultado_fase1 = test_estructura_grupo_SU(trayectoria)
        self.assertIsNotNone(resultado_fase1)
        
        # Fase II - datos mínimos
        datos_sensor = {
            'eda': np.random.rand(50),
            'hrv': np.random.rand(50),
            'amigdala': np.random.rand(50),
            'autorreporte': np.random.rand(50)
        }
        Phi = construir_campo_emocional(datos_sensor)
        self.assertEqual(len(Phi), 50)
        
        # Fase III - simulación mínima
        red, _, simulador = experimento_red_social()
        historia = simulador(red, num_pasos=5)
        resultado_fase3 = analizar_efectos_red(historia, red)
        self.assertIsNotNone(resultado_fase3)
        
        # Fase IV - meta-análisis
        meta = meta_analisis_QCAL()
        self.assertGreater(meta['efecto_combinado_d'], 0)
        
        print("\n✅ Test de integración completado exitosamente")


def run_tests():
    """Ejecuta todos los tests"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestFase1SuPsi))
    suite.addTests(loader.loadTestsFromTestCase(TestFase2TensorStress))
    suite.addTests(loader.loadTestsFromTestCase(TestFase3RedSocial))
    suite.addTests(loader.loadTestsFromTestCase(TestFase4MetaAnalisis))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    import sys
    sys.exit(run_tests())
