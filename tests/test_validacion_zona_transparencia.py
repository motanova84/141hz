#!/usr/bin/env python3
"""
Tests para Validación de Zona de Transparencia del Agua
=======================================================

Tests unitarios para verificar la validación de la zona de transparencia
del agua térmica a 141.7 Hz.
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import validation functions
import importlib.util
spec = importlib.util.spec_from_file_location(
    "validacion_zona_transparencia_agua",
    Path(__file__).parent.parent / "scripts" / "validacion_zona_transparencia_agua.py"
)
validacion_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validacion_module)


class TestZonaTransparencia(unittest.TestCase):
    """Tests para validación de zona de transparencia"""

    def test_f0_en_zona_transparencia(self):
        """Test que f₀ está en zona de transparencia (< 1 kHz)"""
        F0_HZ = validacion_module.F0_HZ
        TRANSPARENCY_ZONE_MAX_HZ = validacion_module.TRANSPARENCY_ZONE_MAX_HZ
        
        self.assertLess(F0_HZ, TRANSPARENCY_ZONE_MAX_HZ,
                       f"f₀ ({F0_HZ} Hz) debe estar por debajo del umbral "
                       f"de transparencia ({TRANSPARENCY_ZONE_MAX_HZ} Hz)")

    def test_constantes_fundamentales(self):
        """Test que las constantes fundamentales están definidas correctamente"""
        # f₀ QCAL
        self.assertEqual(validacion_module.F0_HZ, 141.7001)
        
        # Hidrógeno 21cm
        self.assertEqual(validacion_module.F_HYDROGEN_MHZ, 1420.4056751)
        
        # Zona de transparencia
        self.assertEqual(validacion_module.TRANSPARENCY_ZONE_MAX_HZ, 1000.0)

    def test_bandas_absorcion_agua(self):
        """Test que las bandas de absorción del agua están definidas"""
        bandas = validacion_module.WATER_ABSORPTION_BANDS
        
        # Verificar que existen las bandas principales
        self.assertIn('22_GHz', bandas)
        self.assertIn('183_GHz', bandas)
        
        # Verificar que están en el rango correcto (GHz)
        self.assertGreater(bandas['22_GHz'], 1e9)  # > 1 GHz
        self.assertGreater(bandas['183_GHz'], 1e9)  # > 1 GHz

    def test_f0_muy_por_debajo_bandas_absorcion(self):
        """Test que f₀ está muy por debajo de las bandas de absorción"""
        F0_HZ = validacion_module.F0_HZ
        bandas = validacion_module.WATER_ABSORPTION_BANDS
        
        # f₀ debe estar al menos 6 órdenes de magnitud por debajo de 22 GHz
        ratio = bandas['22_GHz'] / F0_HZ
        self.assertGreater(ratio, 1e6,
                          f"f₀ debe estar al menos 6 órdenes de magnitud "
                          f"por debajo de la banda de 22 GHz (ratio: {ratio:.2e})")

    def test_rango_biologico(self):
        """Test que f₀ está en rango biológico (ELF/VLF)"""
        F0_HZ = validacion_module.F0_HZ
        BIOLOGICAL_FREQ_RANGE = validacion_module.BIOLOGICAL_FREQ_RANGE
        
        freq_min, freq_max = BIOLOGICAL_FREQ_RANGE
        self.assertGreaterEqual(F0_HZ, freq_min)
        self.assertLessEqual(F0_HZ, freq_max)

    def test_rango_microtubulos(self):
        """Test que f₀ está en rango de microtúbulos (100-200 Hz)"""
        F0_HZ = validacion_module.F0_HZ
        
        self.assertGreaterEqual(F0_HZ, 100.0)
        self.assertLessEqual(F0_HZ, 200.0)


class TestRelacionHidrogeno(unittest.TestCase):
    """Tests para validación de relación con hidrógeno"""

    def test_octavas_hidrogeno_f0(self):
        """Test que la relación hidrógeno-f₀ es ~23.257 octavas"""
        import math
        
        F_HYDROGEN_HZ = validacion_module.F_HYDROGEN_HZ
        F0_HZ = validacion_module.F0_HZ
        
        ratio = F_HYDROGEN_HZ / F0_HZ
        octaves = math.log2(ratio)
        
        # Debe estar muy cerca de 23.257
        self.assertAlmostEqual(octaves, 23.257, places=3,
                              msg=f"Octavas calculadas: {octaves:.4f}, "
                                  f"esperadas: 23.257")

    def test_formula_inversa(self):
        """Test que f_H = f₀ × 2^23.257"""
        F_HYDROGEN_HZ = validacion_module.F_HYDROGEN_HZ
        F0_HZ = validacion_module.F0_HZ
        
        # Calcular f_H desde f₀
        octaves = 23.257
        f_h_calculated = F0_HZ * (2 ** octaves)
        
        # Error relativo debe ser < 0.01%
        error_rel = abs(f_h_calculated - F_HYDROGEN_HZ) / F_HYDROGEN_HZ
        self.assertLess(error_rel, 0.0001,
                       f"Error relativo: {error_rel*100:.4f}%")


class TestCoeficienteAbsorcion(unittest.TestCase):
    """Tests para cálculo de coeficiente de absorción"""

    def test_absorcion_baja_en_zona_transparencia(self):
        """Test que la absorción es baja en zona de transparencia"""
        calcular_coeficiente = validacion_module.calcular_coeficiente_absorcion
        
        # A 141.7 Hz, absorción debe ser casi cero
        alpha = calcular_coeficiente(141.7)
        self.assertLess(alpha, 1e-8,
                       f"Absorción a 141.7 Hz debe ser < 1e-8 dB/m, "
                       f"obtenido: {alpha:.2e}")

    def test_absorcion_alta_en_22ghz(self):
        """Test que la absorción es alta cerca de 22 GHz"""
        calcular_coeficiente = validacion_module.calcular_coeficiente_absorcion
        
        # Cerca de 22 GHz, absorción debe ser significativa
        alpha = calcular_coeficiente(22e9)
        self.assertGreater(alpha, 1.0,
                          f"Absorción a 22 GHz debe ser > 1 dB/m, "
                          f"obtenido: {alpha:.2e}")

    def test_absorcion_crece_con_frecuencia(self):
        """Test que la absorción generalmente crece con la frecuencia"""
        calcular_coeficiente = validacion_module.calcular_coeficiente_absorcion
        
        # Verificar que α(1 GHz) > α(1 MHz) > α(1 kHz)
        alpha_1khz = calcular_coeficiente(1e3)
        alpha_1mhz = calcular_coeficiente(1e6)
        alpha_1ghz = calcular_coeficiente(1e9)
        
        self.assertGreater(alpha_1mhz, alpha_1khz)
        self.assertGreater(alpha_1ghz, alpha_1mhz)


class TestValidaciones(unittest.TestCase):
    """Tests de integración para funciones de validación"""

    def test_validar_zona_transparencia(self):
        """Test de validación completa de zona de transparencia"""
        validar = validacion_module.validar_zona_transparencia
        
        resultados = validar()
        
        # Debe validar exitosamente
        self.assertEqual(resultados['validacion'], 'EXITOSA')
        
        # Debe confirmar que f₀ está en zona de transparencia
        self.assertTrue(resultados['en_zona_transparencia'])
        
        # Debe tener distancias a bandas de absorción
        self.assertIn('distancias_bandas_absorcion', resultados)
        self.assertIn('22_GHz', resultados['distancias_bandas_absorcion'])

    def test_validar_relacion_hidrogeno(self):
        """Test de validación de relación armónica con hidrógeno"""
        validar = validacion_module.validar_relacion_hidrogeno
        
        resultados = validar()
        
        # Debe validar exitosamente
        self.assertEqual(resultados['validacion'], 'EXITOSA')
        
        # Error en octavas debe ser < 0.001
        self.assertLess(resultados['error_octaves'], 0.001)

    def test_validar_rango_biologico(self):
        """Test de validación de rango biológico"""
        validar = validacion_module.validar_rango_biologico
        
        resultados = validar()
        
        # Debe validar exitosamente
        self.assertEqual(resultados['validacion'], 'EXITOSA')
        
        # Debe estar en rango biológico
        self.assertTrue(resultados['en_rango_biologico'])
        
        # Debe estar en rango de microtúbulos
        self.assertTrue(resultados['en_rango_microtubulos'])


def suite():
    """Crear suite de tests"""
    suite = unittest.TestSuite()
    
    # Añadir tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestZonaTransparencia))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRelacionHidrogeno))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCoeficienteAbsorcion))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestValidaciones))
    
    return suite


if __name__ == '__main__':
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Exit code
    sys.exit(0 if result.wasSuccessful() else 1)
