#!/usr/bin/env python3
"""
Test Suite para Torre Palma Gravimeter Validation

Valida el script torre_palma_gravimetro.py con datos sintéticos.
"""

import sys
import unittest
import numpy as np
from pathlib import Path

# Añadir directorio scripts al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar módulo a testear
import importlib.util
spec = importlib.util.spec_from_file_location(
    "torre_palma_gravimetro",
    Path(__file__).parent / "torre_palma_gravimetro.py"
)
torre_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(torre_module)

AnalizadorTorreGravimetro = torre_module.AnalizadorTorreGravimetro
TORRES_PALMA = torre_module.TORRES_PALMA
GRAVIMETROS = torre_module.GRAVIMETROS
LAMBDA_DECOH = torre_module.LAMBDA_DECOH
ALPHA_YUKAWA = torre_module.ALPHA_YUKAWA
G0_SURFACE = torre_module.G0_SURFACE


class TestAnalizadorTorreGravimetro(unittest.TestCase):
    """Tests para AnalizadorTorreGravimetro."""
    
    def test_inicializacion_torre_valida(self):
        """Test: Inicializar con torre válida."""
        analyzer = AnalizadorTorreGravimetro('coll_rabassa', 'CG6', verbose=False)
        
        self.assertEqual(analyzer.torre_id, 'coll_rabassa')
        self.assertEqual(analyzer.gravimetro_id, 'CG6')
        self.assertEqual(analyzer.torre['altura'], 380.0)
        
    def test_inicializacion_torre_invalida(self):
        """Test: Rechazar torre inválida."""
        with self.assertRaises(ValueError):
            AnalizadorTorreGravimetro('torre_inexistente', 'CG6', verbose=False)
            
    def test_inicializacion_gravimetro_invalido(self):
        """Test: Rechazar gravímetro inválido."""
        with self.assertRaises(ValueError):
            AnalizadorTorreGravimetro('coll_rabassa', 'INVALID', verbose=False)
            
    def test_generar_datos_sinteticos(self):
        """Test: Generar datos sintéticos."""
        analyzer = AnalizadorTorreGravimetro('coll_rabassa', 'CG6', verbose=False)
        mediciones = analyzer.generar_datos_sinteticos(n_puntos=20, ruido_factor=1.0)
        
        self.assertEqual(len(mediciones), 20)
        self.assertGreater(mediciones[0].gravedad, mediciones[-1].gravedad)
        
        # Verificar que altura aumenta
        for i in range(len(mediciones) - 1):
            self.assertLess(mediciones[i].altura, mediciones[i+1].altura)
            
    def test_fit_yukawa_datos_sinteticos(self):
        """Test: Fit Yukawa con datos sintéticos ideales."""
        analyzer = AnalizadorTorreGravimetro('coll_rabassa', 'CG6', verbose=False)
        analyzer.generar_datos_sinteticos(n_puntos=30, ruido_factor=0.1)
        
        resultado = analyzer.fit_yukawa()
        
        # Verificar parámetros recuperados
        self.assertAlmostEqual(resultado.g0_fit, G0_SURFACE, delta=0.01)
        self.assertAlmostEqual(resultado.alpha_fit, ALPHA_YUKAWA, delta=0.01)
        self.assertAlmostEqual(resultado.lambda_fit, LAMBDA_DECOH, delta=50.0)
        
        # Verificar calidad del fit
        self.assertGreater(resultado.r_squared, 0.95)
        self.assertLess(resultado.p_value, 0.05)
        
    def test_deteccion_confirmada_senal_fuerte(self):
        """Test: Detección confirmada con señal fuerte."""
        analyzer = AnalizadorTorreGravimetro('coll_rabassa', 'CG6', verbose=False)
        
        # Generar datos con muy poco ruido
        analyzer.generar_datos_sinteticos(n_puntos=40, ruido_factor=0.01)
        
        resultado = analyzer.fit_yukawa()
        
        self.assertTrue(resultado.deteccion_confirmada)
        self.assertGreater(resultado.alpha_fit, 0.01)
        self.assertGreater(resultado.significancia_sigma, 3.0)
        
    def test_todas_las_torres(self):
        """Test: Probar todas las torres disponibles."""
        for torre_id in TORRES_PALMA.keys():
            analyzer = AnalizadorTorreGravimetro(torre_id, 'CG6', verbose=False)
            mediciones = analyzer.generar_datos_sinteticos(n_puntos=15)
            
            self.assertEqual(len(mediciones), 15)
            self.assertGreater(analyzer.torre['altura'], 0)
            
    def test_todos_los_gravimetros(self):
        """Test: Probar todos los gravímetros disponibles."""
        for grav_id in GRAVIMETROS.keys():
            analyzer = AnalizadorTorreGravimetro('coll_rabassa', grav_id, verbose=False)
            mediciones = analyzer.generar_datos_sinteticos(n_puntos=10)
            
            self.assertEqual(len(mediciones), 10)
            self.assertGreater(analyzer.gravimetro['resolucion'], 0)
            
    def test_comparacion_gravimetros(self):
        """Test: Comparar CG6 vs iPhone15."""
        # CG6 (alta resolución)
        analyzer_cg6 = AnalizadorTorreGravimetro('coll_rabassa', 'CG6', verbose=False)
        analyzer_cg6.generar_datos_sinteticos(n_puntos=25, ruido_factor=1.0)
        resultado_cg6 = analyzer_cg6.fit_yukawa()
        
        # iPhone15 (baja resolución)
        analyzer_iphone = AnalizadorTorreGravimetro('coll_rabassa', 'iPhone15', verbose=False)
        analyzer_iphone.generar_datos_sinteticos(n_puntos=25, ruido_factor=1.0)
        resultado_iphone = analyzer_iphone.fit_yukawa()
        
        # CG6 debe tener mejor significancia
        self.assertGreater(resultado_cg6.significancia_sigma, 
                          resultado_iphone.significancia_sigma)
        
    def test_efecto_altura_torre(self):
        """Test: Efecto de altura en señal."""
        # Torre baja
        analyzer_baja = AnalizadorTorreGravimetro('hotel_palma', 'CG6', verbose=False)
        analyzer_baja.generar_datos_sinteticos(n_puntos=20, ruido_factor=1.0)
        resultado_baja = analyzer_baja.fit_yukawa()
        
        # Torre alta (óptima @ 336.7m)
        analyzer_alta = AnalizadorTorreGravimetro('coll_rabassa', 'CG6', verbose=False)
        analyzer_alta.generar_datos_sinteticos(n_puntos=20, ruido_factor=1.0)
        resultado_alta = analyzer_alta.fit_yukawa()
        
        # Torre más alta debe tener mejor cobertura de λ
        self.assertGreater(resultado_alta.r_squared, resultado_baja.r_squared)


class TestConstantesTorres(unittest.TestCase):
    """Tests para constantes y configuración de torres."""
    
    def test_torres_palma_estructura(self):
        """Test: Verificar estructura TORRES_PALMA."""
        self.assertIn('coll_rabassa', TORRES_PALMA)
        self.assertIn('tramuntana_1', TORRES_PALMA)
        self.assertIn('hotel_palma', TORRES_PALMA)
        
        for torre in TORRES_PALMA.values():
            self.assertIn('altura', torre)
            self.assertIn('latitud', torre)
            self.assertIn('longitud', torre)
            self.assertGreater(torre['altura'], 0)
            
    def test_gravimetros_estructura(self):
        """Test: Verificar estructura GRAVIMETROS."""
        self.assertIn('CG6', GRAVIMETROS)
        self.assertIn('iPhone15', GRAVIMETROS)
        
        for grav in GRAVIMETROS.values():
            self.assertIn('resolucion', grav)
            self.assertIn('sigma_esperada', grav)
            self.assertGreater(grav['resolucion'], 0)
            self.assertGreater(grav['sigma_esperada'], 0)
            
    def test_coll_rabassa_optima(self):
        """Test: Coll d'en Rabassa es óptima (cerca de 336.7m)."""
        torre = TORRES_PALMA['coll_rabassa']
        
        # Debe estar cerca de λ = 336.7 m
        self.assertLess(abs(torre['altura'] - LAMBDA_DECOH), 100)
        self.assertEqual(torre['status'], 'ÓPTIMO')
        
    def test_cg6_mejor_resolucion(self):
        """Test: CG-6 tiene mejor resolución que iPhone."""
        cg6 = GRAVIMETROS['CG6']
        iphone = GRAVIMETROS['iPhone15']
        
        self.assertLess(cg6['resolucion'], iphone['resolucion'])
        self.assertGreater(cg6['sigma_esperada'], iphone['sigma_esperada'])


class TestModeloFisico(unittest.TestCase):
    """Tests para el modelo físico Yukawa."""
    
    def test_yukawa_decae_con_altura(self):
        """Test: Yukawa decae exponencialmente con altura."""
        alturas = np.array([0, 100, 200, 336.7, 500])
        
        g_valores = G0_SURFACE * (1 + ALPHA_YUKAWA * np.exp(-alturas / LAMBDA_DECOH))
        
        # Debe decrecer monotónicamente
        for i in range(len(g_valores) - 1):
            self.assertGreater(g_valores[i], g_valores[i+1])
            
    def test_yukawa_at_lambda(self):
        """Test: Valor específico @ h=λ."""
        h = LAMBDA_DECOH
        g_lambda = G0_SURFACE * (1 + ALPHA_YUKAWA * np.exp(-1))
        
        # @ h=λ, factor = exp(-1) ≈ 0.368
        factor_esperado = ALPHA_YUKAWA / np.e
        
        self.assertAlmostEqual(
            (g_lambda - G0_SURFACE) / G0_SURFACE,
            factor_esperado,
            places=5
        )
        
    def test_senal_esperada_336m(self):
        """Test: Señal esperada @ 336.7m."""
        h = 336.7
        g_0 = G0_SURFACE
        g_h = G0_SURFACE * (1 + ALPHA_YUKAWA * np.exp(-h / LAMBDA_DECOH))
        
        delta_g = g_h - g_0
        
        # Δg @ 336.7m ≈ 4.98×10⁻⁸ m/s²
        self.assertAlmostEqual(abs(delta_g), 4.98e-8, delta=1e-8)


def run_tests():
    """Ejecutar todos los tests."""
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
