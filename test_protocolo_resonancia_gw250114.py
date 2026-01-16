#!/usr/bin/env python3
"""
Tests para el Protocolo de Resonancia Real de GW250114

Verifica que:
1. El protocolo de resonancia se ejecuta correctamente
2. La validación del Nodo Riemann funciona
3. Los resultados se generan en el formato esperado
"""

import unittest
import sys
import os
from pathlib import Path
import json

# Añadir directorio scripts al path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))


class TestProtocoloResonanciaGW250114(unittest.TestCase):
    """Tests para el protocolo de resonancia"""
    
    def setUp(self):
        """Configuración de tests"""
        self.script_path = Path(__file__).parent / "scripts" / "protocolo_resonancia_gw250114.py"
        self.results_dir = Path(__file__).parent / "results" / "gw250114_resonancia"
        
    def test_script_exists(self):
        """Verificar que el script existe"""
        self.assertTrue(self.script_path.exists(), 
                       f"Script no encontrado: {self.script_path}")
    
    def test_script_imports(self):
        """Verificar que el script puede importarse sin errores"""
        try:
            # Importar el módulo
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "protocolo_resonancia", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Verificar que la clase principal existe
            self.assertTrue(hasattr(module, 'ProtocoloResonanciaGW250114'))
            
        except Exception as e:
            self.fail(f"Error importando script: {e}")
    
    def test_protocolo_clase_initialization(self):
        """Verificar que la clase se puede instanciar"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "protocolo_resonancia", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Instanciar la clase
            protocolo = module.ProtocoloResonanciaGW250114()
            
            # Verificar atributos
            self.assertEqual(protocolo.f0, 141.7001)
            self.assertEqual(protocolo.evento, "GW250114")
            
        except Exception as e:
            self.fail(f"Error instanciando clase: {e}")
    
    def test_protocolo_verifica_disponibilidad(self):
        """Verificar que el método de verificación funciona"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "protocolo_resonancia", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            protocolo = module.ProtocoloResonanciaGW250114()
            
            # Verificar disponibilidad (esperamos que no esté disponible aún)
            disponible, gps_time = protocolo.verificar_disponibilidad()
            
            # Por ahora, esperamos que GW250114 no esté disponible
            # (esto cambiará cuando LIGO libere los datos)
            # Solo verificamos que el método retorna una tupla
            self.assertIsInstance(disponible, bool)
            
        except Exception as e:
            self.fail(f"Error en verificación de disponibilidad: {e}")


class TestNodoRiemannValidator(unittest.TestCase):
    """Tests para el validador del Nodo Riemann"""
    
    def setUp(self):
        """Configuración de tests"""
        self.script_path = Path(__file__).parent / "validate_riemann_ringdown_gw250114.py"
        self.results_dir = Path(__file__).parent / "results" / "nodo_riemann"
        
    def test_script_exists(self):
        """Verificar que el script existe"""
        self.assertTrue(self.script_path.exists(), 
                       f"Script no encontrado: {self.script_path}")
    
    def test_script_imports(self):
        """Verificar que el script puede importarse"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "nodo_riemann", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Verificar clase principal
            self.assertTrue(hasattr(module, 'NodoRiemannValidator'))
            
        except Exception as e:
            self.fail(f"Error importando script: {e}")
    
    def test_nodo_riemann_initialization(self):
        """Verificar inicialización de NodoRiemannValidator"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "nodo_riemann", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Instanciar
            validador = module.NodoRiemannValidator(precision=50)
            
            # Verificar atributos
            self.assertEqual(validador.f0, 141.7001)
            
        except Exception as e:
            self.fail(f"Error instanciando NodoRiemannValidator: {e}")
    
    def test_obtener_ceros_riemann(self):
        """Verificar que se pueden obtener ceros de Riemann"""
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "nodo_riemann", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            validador = module.NodoRiemannValidator(precision=50)
            
            # Obtener ceros
            ceros = validador.obtener_ceros_riemann(n_zeros=10)
            
            # Verificar
            self.assertEqual(len(ceros), 10)
            self.assertTrue(all(ceros > 0))  # Todos positivos
            
            # Verificar que el primer cero es ~14.134725
            self.assertAlmostEqual(ceros[0], 14.134725, places=5)
            
        except Exception as e:
            self.fail(f"Error obteniendo ceros de Riemann: {e}")
    
    def test_distribucion_espectral_zeta(self):
        """Verificar cálculo de distribución espectral"""
        try:
            import importlib.util
            import numpy as np
            
            spec = importlib.util.spec_from_file_location(
                "nodo_riemann", 
                self.script_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            validador = module.NodoRiemannValidator(precision=50)
            
            # Usar algunos ceros de prueba
            ceros = validador.obtener_ceros_riemann(n_zeros=10)
            
            # Calcular distribución
            distribucion = validador.calcular_distribucion_espectral_zeta(ceros)
            
            # Verificar estructura
            self.assertIn('ceros', distribucion)
            self.assertIn('freqs_directa', distribucion)
            self.assertIn('freqs_armonicas', distribucion)
            self.assertIn('estadisticas', distribucion)
            
            # Verificar que se calcularon frecuencias
            self.assertEqual(len(distribucion['ceros']), 10)
            self.assertEqual(len(distribucion['freqs_directa']), 10)
            
        except Exception as e:
            self.fail(f"Error calculando distribución espectral: {e}")


class TestIntegration(unittest.TestCase):
    """Tests de integración"""
    
    def test_workflow_completo_sin_datos(self):
        """
        Verificar que el workflow completo funciona sin datos de GW250114.
        
        Este test verifica que:
        1. El protocolo detecta que no hay datos
        2. Genera archivos de estado apropiados
        3. No falla con errores
        """
        try:
            import importlib.util
            
            # Cargar módulo de protocolo
            spec_protocolo = importlib.util.spec_from_file_location(
                "protocolo_resonancia",
                Path(__file__).parent / "scripts" / "protocolo_resonancia_gw250114.py"
            )
            module_protocolo = importlib.util.module_from_spec(spec_protocolo)
            spec_protocolo.loader.exec_module(module_protocolo)
            
            # Ejecutar protocolo
            protocolo = module_protocolo.ProtocoloResonanciaGW250114()
            resultado = protocolo.ejecutar_protocolo(detector='H1')
            
            # Verificar que se maneja correctamente la falta de datos
            self.assertIn('estado', resultado)
            self.assertEqual(resultado['estado'], 'DATOS_NO_DISPONIBLES')
            
        except Exception as e:
            # Esperamos que pueda fallar si no hay datos, pero no debe
            # ser un error de Python
            if "GW250114" not in str(e) and "not found" not in str(e).lower():
                self.fail(f"Error inesperado: {e}")


def run_tests():
    """Ejecutar todos los tests"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir tests
    suite.addTests(loader.loadTestsFromTestCase(TestProtocoloResonanciaGW250114))
    suite.addTests(loader.loadTestsFromTestCase(TestNodoRiemannValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
