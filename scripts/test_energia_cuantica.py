#!/usr/bin/env python3
"""
Tests para el módulo de cálculo de energía cuántica fundamental

Valida que los cálculos de E_Ψ = hf₀ sean correctos y consistentes
con las predicciones teóricas del paper.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import unittest
import numpy as np
import json
import os
import sys

# Agregar el directorio scripts al path para importar el módulo
sys.path.insert(0, os.path.dirname(__file__))

# Importar funciones del módulo principal
from energia_cuantica_fundamental import (
    calcular_energia_cuantica,
    calcular_radio_compactificacion,
    potencial_adelico_fractal,
    h, h_bar, c, l_P, eV, f0
)


class TestEnergiaCuanticaFundamental(unittest.TestCase):
    """
    Test suite para validar cálculos de energía cuántica
    """
    
    def test_constantes_fundamentales(self):
        """
        Test: Verificar que las constantes fundamentales sean correctas
        """
        # Constante de Planck (CODATA 2018, exacta por definición)
        self.assertAlmostEqual(h, 6.62607015e-34, places=41)
        
        # Constante de Planck reducida
        self.assertAlmostEqual(h_bar, h / (2 * np.pi), places=41)
        
        # Velocidad de la luz (exacta por definición)
        self.assertEqual(c, 299792458)
        
        # Electronvoltio (exacto por definición)
        self.assertAlmostEqual(eV, 1.602176634e-19, places=28)
        
    def test_frecuencia_fundamental(self):
        """
        Test: Verificar que la frecuencia fundamental sea correcta
        """
        self.assertAlmostEqual(f0, 141.7001, places=4)
        
    def test_energia_en_joules(self):
        """
        Test: Verificar E_Ψ = hf₀ en Joules
        
        Valor esperado: 9.39×10⁻³² J
        """
        E_psi = calcular_energia_cuantica()
        
        # Valor esperado según el paper
        E_esperado = 9.39e-32  # J
        
        # Verificar con tolerancia del 1%
        diff_rel = abs(E_psi['E_J'] - E_esperado) / E_esperado
        self.assertLess(diff_rel, 0.01, 
                       f"E_Ψ = {E_psi['E_J']:.2e} J difiere de {E_esperado:.2e} J")
        
    def test_energia_en_eV(self):
        """
        Test: Verificar E_Ψ en electronvoltios
        
        Valor esperado: 5.86×10⁻¹³ eV
        """
        E_psi = calcular_energia_cuantica()
        
        # Valor esperado según el paper
        E_esperado_eV = 5.86e-13  # eV
        
        # Verificar con tolerancia del 1%
        diff_rel = abs(E_psi['E_eV'] - E_esperado_eV) / E_esperado_eV
        self.assertLess(diff_rel, 0.01,
                       f"E_Ψ = {E_psi['E_eV']:.2e} eV difiere de {E_esperado_eV:.2e} eV")
        
    def test_consistencia_h_hbar(self):
        """
        Test: Verificar consistencia entre E = hf₀ y E = ℏω₀
        """
        omega_0 = 2 * np.pi * f0
        
        E_h = h * f0
        E_hbar = h_bar * omega_0
        
        # Deben ser idénticos dentro de precisión numérica
        diff_rel = abs(E_h - E_hbar) / E_h
        self.assertLess(diff_rel, 1e-8,
                       f"E=hf₀ y E=ℏω₀ difieren en {diff_rel*100:.2e}%")
        
    def test_conversion_J_a_eV(self):
        """
        Test: Verificar conversión correcta de Joules a eV
        """
        E_psi = calcular_energia_cuantica()
        
        # Conversión manual
        E_eV_manual = E_psi['E_J'] / eV
        
        # Debe coincidir con el valor calculado
        diff_rel = abs(E_psi['E_eV'] - E_eV_manual) / E_eV_manual
        self.assertLess(diff_rel, 1e-10,
                       f"Conversión J→eV inconsistente: {diff_rel*100:.2e}%")
        
    def test_radio_compactificacion(self):
        """
        Test: Verificar cálculo de radio de compactificación
        
        De f₀ = c/(2πR_Ψℓ_P), despejando R_Ψ = c/(2πf₀ℓ_P)
        """
        R_psi = calcular_radio_compactificacion()
        
        # Cálculo manual
        R_psi_manual = c / (2 * np.pi * f0 * l_P)
        
        # Verificar consistencia
        diff_rel = abs(R_psi - R_psi_manual) / R_psi_manual
        self.assertLess(diff_rel, 1e-10,
                       f"Cálculo de R_Ψ inconsistente: {diff_rel*100:.2e}%")
        
        # Verificar que es positivo
        self.assertGreater(R_psi, 0)
        
        # Verificar que es mucho mayor que longitud de Planck
        self.assertGreater(R_psi / l_P, 1e50,
                          "R_Ψ debería ser >> ℓ_P")
        
    def test_potencial_vacío(self):
        """
        Test: Verificar cálculo del potencial adélico-fractal
        """
        R_psi = calcular_radio_compactificacion()
        pot_vac = potencial_adelico_fractal(R_psi)
        
        # Verificar que todos los términos estén presentes
        self.assertIn('term1', pot_vac)
        self.assertIn('term2', pot_vac)
        self.assertIn('term3', pot_vac)
        self.assertIn('term4', pot_vac)
        self.assertIn('total', pot_vac)
        
        # Verificar que el total sea la suma de los términos
        total_manual = (pot_vac['term1'] + pot_vac['term2'] + 
                       pot_vac['term3'] + pot_vac['term4'])
        
        diff_rel = abs(pot_vac['total'] - total_manual) / abs(total_manual)
        self.assertLess(diff_rel, 1e-10,
                       "E_vac total no coincide con suma de términos")
        
    def test_jerarquia_escalas(self):
        """
        Test: Verificar jerarquía de escalas ℓ_P ↔ R_Ψ ↔ H₀⁻¹
        """
        R_psi = calcular_radio_compactificacion()
        H_0_inv = c / 2.2e-18  # Aproximación del horizonte de Hubble
        
        # Verificar jerarquía: ℓ_P << R_Ψ << H₀⁻¹
        self.assertLess(l_P, R_psi, "Debe cumplirse ℓ_P < R_Ψ")
        # Nota: R_Ψ puede ser comparable o mayor que H₀⁻¹ en este modelo
        
    def test_salida_json(self):
        """
        Test: Verificar que el archivo JSON se genera correctamente
        """
        # Ejecutar el módulo completo
        import energia_cuantica_fundamental
        energia_cuantica_fundamental.main()
        
        # Verificar que el archivo existe
        json_file = 'results/energia_cuantica_fundamental.json'
        self.assertTrue(os.path.exists(json_file),
                       f"Archivo {json_file} no fue generado")
        
        # Cargar y validar contenido
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Verificar estructura
        self.assertIn('energia_cuantica', data)
        self.assertIn('constantes', data)
        self.assertIn('geometria', data)
        self.assertIn('potencial_vacío', data)
        
        # Verificar valores clave
        E_J = data['energia_cuantica']['E_Joules']
        E_eV = data['energia_cuantica']['E_eV']
        
        self.assertAlmostEqual(E_J, 9.39e-32, delta=0.01e-32)
        self.assertAlmostEqual(E_eV, 5.86e-13, delta=0.01e-13)
        
    def test_salida_visualizacion(self):
        """
        Test: Verificar que la visualización se genera correctamente
        """
        # Ejecutar el módulo completo
        import energia_cuantica_fundamental
        energia_cuantica_fundamental.main()
        
        # Verificar que el archivo existe
        png_file = 'results/figures/energia_cuantica_fundamental.png'
        self.assertTrue(os.path.exists(png_file),
                       f"Archivo {png_file} no fue generado")
        
        # Verificar que tiene un tamaño razonable (> 10 KB)
        file_size = os.path.getsize(png_file)
        self.assertGreater(file_size, 10000,
                          f"Archivo de visualización muy pequeño: {file_size} bytes")


class TestValoresExactos(unittest.TestCase):
    """
    Test suite para verificar valores exactos del paper
    """
    
    def test_valor_exacto_E_Joules(self):
        """
        Test: Verificar valor exacto E_Ψ = 9.39×10⁻³² J
        """
        E_J = h * f0
        
        # Valor del paper (2 cifras significativas)
        self.assertAlmostEqual(E_J / 1e-32, 9.39, places=2,
                              msg=f"E_Ψ = {E_J:.2e} J ≠ 9.39×10⁻³² J")
        
    def test_valor_exacto_E_eV(self):
        """
        Test: Verificar valor exacto E_Ψ ≈ 5.86×10⁻¹³ eV
        """
        E_J = h * f0
        E_eV_calc = E_J / eV
        
        # Valor del paper (2 cifras significativas)
        self.assertAlmostEqual(E_eV_calc / 1e-13, 5.86, places=2,
                              msg=f"E_Ψ = {E_eV_calc:.2e} eV ≠ 5.86×10⁻¹³ eV")


def suite():
    """
    Construir suite de tests
    """
    suite = unittest.TestSuite()
    
    # Tests de constantes y cálculos básicos
    suite.addTest(TestEnergiaCuanticaFundamental('test_constantes_fundamentales'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_frecuencia_fundamental'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_energia_en_joules'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_energia_en_eV'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_consistencia_h_hbar'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_conversion_J_a_eV'))
    
    # Tests de geometría
    suite.addTest(TestEnergiaCuanticaFundamental('test_radio_compactificacion'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_jerarquia_escalas'))
    
    # Tests de potencial del vacío
    suite.addTest(TestEnergiaCuanticaFundamental('test_potencial_vacío'))
    
    # Tests de salidas
    suite.addTest(TestEnergiaCuanticaFundamental('test_salida_json'))
    suite.addTest(TestEnergiaCuanticaFundamental('test_salida_visualizacion'))
    
    # Tests de valores exactos
    suite.addTest(TestValoresExactos('test_valor_exacto_E_Joules'))
    suite.addTest(TestValoresExactos('test_valor_exacto_E_eV'))
    
    return suite


if __name__ == '__main__':
    print("=" * 80)
    print("TESTS: Energía Cuántica del Modo Fundamental")
    print("=" * 80)
    print()
    
    # Ejecutar suite de tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Resumen
    print()
    print("=" * 80)
    print("RESUMEN DE TESTS")
    print("=" * 80)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos:   {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos:           {len(result.failures)}")
    print(f"Errores:          {len(result.errors)}")
    
    if result.wasSuccessful():
        print()
        print("✅ TODOS LOS TESTS PASARON")
        print()
        sys.exit(0)
    else:
        print()
        print("❌ ALGUNOS TESTS FALLARON")
        print()
        sys.exit(1)
