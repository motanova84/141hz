#!/usr/bin/env python3
"""
Test básico para el análisis GW250114
Verifica que el workflow de 6 pasos funciona correctamente
"""

import os
import sys
import subprocess
import unittest

class TestAnalisisGW250114(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial"""
        self.script_path = "scripts/analisis_gw250114.py"
        self.results_dir = "results/gw250114"
    
    def test_script_exists(self):
        """Verifica que el script principal existe"""
        self.assertTrue(os.path.exists(self.script_path))
    
    def test_script_runs(self):
        """Verifica que el script se ejecuta sin errores"""
        # Ejecutar el script usando el venv
        result = subprocess.run([
            './venv/bin/python', self.script_path
        ], capture_output=True, text=True, cwd='.')
        
        # Verificar que no hay errores de Python
        self.assertEqual(result.returncode, 0, 
                        f"Script failed: {result.stderr}")
        
        # Verificar que contiene los pasos esperados
        output = result.stdout
        self.assertIn("PASO 1", output)
        self.assertIn("PASO 2", output) 
        self.assertIn("PASO 3", output)
        self.assertIn("PASO 4", output)
        self.assertIn("PASO 5", output)
        self.assertIn("PASO 6", output)
        self.assertIn("REPORTE FINAL", output)
    
    def test_results_generated(self):
        """Verifica que se generan los resultados"""
        # Ejecutar el script
        subprocess.run(['./venv/bin/python', self.script_path], 
                      cwd='.', check=True)
        
        # Verificar que existe el directorio de resultados
        self.assertTrue(os.path.exists(self.results_dir))
        
        # Verificar que se genera el gráfico
        plot_path = os.path.join(self.results_dir, "analisis_completo.png")
        self.assertTrue(os.path.exists(plot_path))
    
    def test_makefile_target(self):
        """Verifica que el target de Makefile funciona"""
        result = subprocess.run([
            'make', 'analyze-gw250114'
        ], capture_output=True, text=True, cwd='.')
        
        self.assertEqual(result.returncode, 0,
                        f"Makefile target failed: {result.stderr}")

if __name__ == '__main__':
    # Cambiar al directorio raíz del proyecto
    if os.path.basename(os.getcwd()) == 'scripts':
        os.chdir('..')
    
    # Ejecutar tests
    unittest.main(verbosity=2)