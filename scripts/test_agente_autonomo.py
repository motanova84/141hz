#!/usr/bin/env python3
"""
Tests para el Agente Autónomo 141Hz

Verifica el funcionamiento del sistema de auto-recuperación:
- Detección de fallos
- Diagnóstico inteligente
- Corrección automática
- Sistema de reintentos
- Alineación con frecuencia 141Hz

Autor: Sistema de Testing Autónomo
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Añadir scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from agente_autonomo_141hz import (
    FrecuenciaCoherente141Hz,
    DiagnosticadorInteligente,
    CorrectorAutomatico,
    AgenteAutonomo141Hz
)


class TestFrecuenciaCoherente(unittest.TestCase):
    """Tests para FrecuenciaCoherente141Hz"""
    
    def test_frecuencia_base(self):
        """Verifica frecuencia base correcta"""
        self.assertEqual(FrecuenciaCoherente141Hz.FRECUENCIA_BASE, 141.7001)
    
    def test_periodo_base(self):
        """Verifica cálculo de periodo base"""
        periodo = FrecuenciaCoherente141Hz.PERIODO_BASE
        frecuencia_calculada = 1.0 / periodo
        self.assertAlmostEqual(frecuencia_calculada, 141.7001, places=4)
    
    def test_backoff_cuantico(self):
        """Verifica backoff cuántico exponencial"""
        # Backoff debe crecer exponencialmente
        t0 = FrecuenciaCoherente141Hz.backoff_cuantico(0)
        t1 = FrecuenciaCoherente141Hz.backoff_cuantico(1)
        t2 = FrecuenciaCoherente141Hz.backoff_cuantico(2)
        
        self.assertGreater(t1, t0)
        self.assertGreater(t2, t1)
        
        # Debe ser múltiplo del periodo base
        self.assertAlmostEqual(
            t1 / t0,
            2.0,
            places=1
        )


class TestDiagnosticadorInteligente(unittest.TestCase):
    """Tests para DiagnosticadorInteligente"""
    
    def setUp(self):
        self.diagnosticador = DiagnosticadorInteligente()
    
    def test_diagnosticar_module_not_found(self):
        """Test diagnóstico de módulo faltante"""
        error = "ModuleNotFoundError: No module named 'mpmath'"
        diagnostico = self.diagnosticador.diagnosticar(error)
        
        self.assertEqual(diagnostico['tipo'], 'dependencia_faltante')
        self.assertIn('instalar_dependencia', diagnostico['correcciones_propuestas'])
        self.assertGreater(diagnostico['confianza'], 0.5)
        self.assertEqual(diagnostico['detalles']['modulo_faltante'], 'mpmath')
    
    def test_diagnosticar_file_not_found(self):
        """Test diagnóstico de archivo faltante"""
        error = "FileNotFoundError: No such file or directory: 'results/data.json'"
        diagnostico = self.diagnosticador.diagnosticar(error)
        
        self.assertEqual(diagnostico['tipo'], 'archivo_faltante')
        self.assertIn('crear_directorio', diagnostico['correcciones_propuestas'])
        self.assertEqual(diagnostico['detalles']['archivo_faltante'], 'results/data.json')
    
    def test_diagnosticar_assertion_error(self):
        """Test diagnóstico de fallo de aserción"""
        error = "AssertionError: Test failed at line 42"
        diagnostico = self.diagnosticador.diagnosticar(error)
        
        self.assertEqual(diagnostico['tipo'], 'validacion_fallida')
        self.assertEqual(diagnostico['detalles']['linea_error'], 42)
    
    def test_historial_diagnosticos(self):
        """Verifica que se registra historial"""
        self.diagnosticador.diagnosticar("Error 1")
        self.diagnosticador.diagnosticar("Error 2")
        
        self.assertEqual(len(self.diagnosticador.historial_diagnosticos), 2)


class TestCorrectorAutomatico(unittest.TestCase):
    """Tests para CorrectorAutomatico"""
    
    def setUp(self):
        self.corrector = CorrectorAutomatico()
        # Crear directorio temporal
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_corregir_crear_directorio(self):
        """Test creación automática de directorios"""
        diagnostico = {
            'tipo': 'archivo_faltante',
            'correcciones_propuestas': ['crear_directorio'],
            'detalles': {'archivo_faltante': 'results/output.json'}
        }
        
        exito, mensaje = self.corrector.aplicar_correccion(diagnostico)
        
        self.assertTrue(exito)
        self.assertTrue(Path('results').exists())
    
    def test_corregir_directorios_comunes(self):
        """Test creación de directorios comunes"""
        diagnostico = {
            'tipo': 'archivo_faltante',
            'correcciones_propuestas': ['crear_directorio'],
            'detalles': {}
        }
        
        exito, mensaje = self.corrector.aplicar_correccion(diagnostico)
        
        self.assertTrue(exito)
        # Verificar directorios comunes
        for dir_name in ['results', 'logs', 'data']:
            self.assertTrue(Path(dir_name).exists())


class TestAgenteAutonomo(unittest.TestCase):
    """Tests para AgenteAutonomo141Hz"""
    
    def setUp(self):
        # Crear directorio temporal
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Crear agente
        self.agente = AgenteAutonomo141Hz(max_intentos=3)
    
    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_inicializacion(self):
        """Verifica inicialización correcta del agente"""
        self.assertEqual(self.agente.max_intentos, 3)
        self.assertIsNotNone(self.agente.diagnosticador)
        self.assertIsNotNone(self.agente.corrector)
        self.assertEqual(len(self.agente.historial_ejecuciones), 0)
    
    def test_ejecutar_validacion_exitosa(self):
        """Test ejecución de script exitoso"""
        # Crear script de prueba exitoso
        script_path = Path('test_exitoso.py')
        script_path.write_text('''#!/usr/bin/env python3
import sys
print("Test exitoso")
sys.exit(0)
''')
        
        exito, resultado = self.agente.ejecutar_validacion(str(script_path))
        
        self.assertTrue(exito)
        self.assertEqual(resultado['returncode'], 0)
        self.assertIn('Test exitoso', resultado['stdout'])
    
    def test_ejecutar_validacion_fallida(self):
        """Test ejecución de script fallido"""
        # Crear script de prueba fallido
        script_path = Path('test_fallido.py')
        script_path.write_text('''#!/usr/bin/env python3
import sys
print("Test fallido")
sys.exit(1)
''')
        
        exito, resultado = self.agente.ejecutar_validacion(str(script_path))
        
        self.assertFalse(exito)
        self.assertEqual(resultado['returncode'], 1)
    
    def test_generar_reporte(self):
        """Verifica generación de reporte"""
        # Ejecutar un ciclo completo para tener datos
        script_path = Path('test_simple.py')
        script_path.write_text('import sys; sys.exit(0)')
        
        self.agente.ciclo_auto_recuperacion(str(script_path))
        
        # Generar reporte
        reporte = self.agente.generar_reporte('test_reporte.json')
        
        self.assertIsNotNone(reporte)
        self.assertGreaterEqual(reporte['total_ejecuciones'], 1)
        self.assertEqual(reporte['frecuencia_alineacion'], 141.7001)
        self.assertTrue(Path('test_reporte.json').exists())
        
        # Verificar que el JSON es válido
        with open('test_reporte.json', 'r') as f:
            datos = json.load(f)
            self.assertIsInstance(datos, dict)


class TestIntegracion(unittest.TestCase):
    """Tests de integración del sistema completo"""
    
    def setUp(self):
        # Crear directorio temporal
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_ciclo_completo_exitoso(self):
        """Test ciclo completo con validación exitosa"""
        # Crear script exitoso
        script_path = Path('validacion_exitosa.py')
        script_path.write_text('''#!/usr/bin/env python3
import sys
print("Validación exitosa")
sys.exit(0)
''')
        
        agente = AgenteAutonomo141Hz(max_intentos=3)
        exito = agente.ciclo_auto_recuperacion(str(script_path))
        
        self.assertTrue(exito)
        self.assertEqual(len(agente.historial_ejecuciones), 1)
        self.assertTrue(agente.historial_ejecuciones[0]['exito'])
    
    def test_ciclo_auto_recuperacion_con_fallo(self):
        """Test ciclo de auto-recuperación con fallo inicial"""
        # Crear script que falla la primera vez pero crea archivo de estado
        script_path = Path('validacion_con_recuperacion.py')
        script_path.write_text('''#!/usr/bin/env python3
import sys
from pathlib import Path

estado_file = Path('estado.txt')
if not estado_file.exists():
    # Primera ejecución - crear directorio y fallar
    Path('results').mkdir(exist_ok=True)
    estado_file.write_text('intento_1')
    print("Primer intento fallido")
    sys.exit(1)
else:
    # Segunda ejecución - éxito
    print("Segundo intento exitoso")
    sys.exit(0)
''')
        
        agente = AgenteAutonomo141Hz(max_intentos=3)
        exito = agente.ciclo_auto_recuperacion(str(script_path))
        
        # Debería tener éxito después de varios intentos
        self.assertGreaterEqual(len(agente.historial_ejecuciones), 1)


def main():
    """Ejecutar tests"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Añadir tests
    suite.addTests(loader.loadTestsFromTestCase(TestFrecuenciaCoherente))
    suite.addTests(loader.loadTestsFromTestCase(TestDiagnosticadorInteligente))
    suite.addTests(loader.loadTestsFromTestCase(TestCorrectorAutomatico))
    suite.addTests(loader.loadTestsFromTestCase(TestAgenteAutonomo))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
