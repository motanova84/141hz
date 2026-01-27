#!/usr/bin/env python3
"""
Tests unitarios para el análisis de AT2020afhd.

Valida los cálculos de:
- Conversión de periodo a frecuencia
- Relación armónica con f₀ = 141.70001 Hz
- Cálculo de octavas
- Detección de periodo principal

Autor: José Manuel Mota Burruezo (JMMB Ψ ∞³)
"""

import sys
import unittest
import numpy as np
from pathlib import Path

# Importar funciones del script de análisis
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from analizar_at2020afhd import (
    calcular_frecuencia_observada,
    verificar_relacion_armonica,
    detectar_periodo_principal,
    F0_QCAL,
    EXPECTED_PERIOD,
    EXPECTED_OCTAVES,
    SECONDS_PER_DAY
)


class TestAnalisisAT2020afhd(unittest.TestCase):
    """Tests para el análisis de AT2020afhd."""
    
    def test_calcular_frecuencia_observada(self):
        """Test: Conversión de periodo (días) a frecuencia (Hz)."""
        # Test con el periodo esperado de 19.6 días
        periodo = 19.6  # días
        f_obs = calcular_frecuencia_observada(periodo)
        
        # Calcular frecuencia esperada
        periodo_segundos = 19.6 * SECONDS_PER_DAY
        f_esperada = 1.0 / periodo_segundos
        
        # Verificar que coinciden
        self.assertAlmostEqual(f_obs, f_esperada, places=10)
        
        # Verificar orden de magnitud correcto (~ 5.9e-7 Hz)
        self.assertGreater(f_obs, 5.8e-7)
        self.assertLess(f_obs, 6.0e-7)
    
    def test_verificar_relacion_armonica_caso_ideal(self):
        """Test: Relación armónica en caso ideal (19.6 días exactos)."""
        # Frecuencia para periodo de 19.6 días
        f_obs = calcular_frecuencia_observada(19.6)
        
        # Verificar relación armónica
        ratio, n_octavas, error_pct = verificar_relacion_armonica(f_obs, F0_QCAL)
        
        # Verificar que el ratio es del orden correcto (~ 2.4e8)
        self.assertGreater(ratio, 2.3e8)
        self.assertLess(ratio, 2.5e8)
        
        # Verificar que las octavas están cerca del valor esperado
        self.assertAlmostEqual(n_octavas, EXPECTED_OCTAVES, places=1)
        
        # Verificar que el error es muy pequeño (< 1%)
        self.assertLess(error_pct, 1.0)
    
    def test_verificar_relacion_armonica_precision(self):
        """Test: Precisión del cálculo de octavas."""
        # Test con frecuencias conocidas
        # f₀ = 141.70001 Hz
        # f₁ = f₀ / 2 = 70.850005 Hz -> 1 octava
        # f₂ = f₀ / 4 = 35.4250025 Hz -> 2 octavas
        
        test_cases = [
            (F0_QCAL / 2, 1.0),     # 1 octava
            (F0_QCAL / 4, 2.0),     # 2 octavas
            (F0_QCAL / 8, 3.0),     # 3 octavas
            (F0_QCAL / 16, 4.0),    # 4 octavas
            (F0_QCAL / 1024, 10.0), # 10 octavas
        ]
        
        for f_test, octavas_esperadas in test_cases:
            ratio, n_octavas, error_pct = verificar_relacion_armonica(f_test, F0_QCAL)
            
            # Verificar que el cálculo de octavas es correcto
            self.assertAlmostEqual(n_octavas, octavas_esperadas, places=10,
                                 msg=f"Fallo en f={f_test} Hz, esperado {octavas_esperadas} octavas")
    
    def test_detectar_periodo_principal(self):
        """Test: Detección del periodo principal en un periodograma."""
        # Crear periodograma sintético con pico en 19.6 días
        periodos = np.linspace(10, 30, 100)
        
        # Crear potencias con pico gaussiano en 19.6 días
        potencias = 10.0 * np.exp(-0.5 * ((periodos - 19.6) / 0.5)**2) + np.random.random(100) * 0.5
        
        # Detectar periodo principal
        periodo_pico, potencia_pico, idx_pico = detectar_periodo_principal(periodos, potencias)
        
        # Verificar que el periodo detectado está cerca de 19.6 días
        self.assertAlmostEqual(periodo_pico, 19.6, places=0,
                             msg="El periodo detectado debe estar cerca de 19.6 días")
        
        # Verificar que la potencia del pico es mayor que la media
        self.assertGreater(potencia_pico, np.mean(potencias),
                          msg="La potencia del pico debe ser mayor que la media")
        
        # Verificar que el índice es válido
        self.assertGreaterEqual(idx_pico, 0)
        self.assertLess(idx_pico, len(periodos))
    
    def test_verificacion_completa_at2020afhd(self):
        """Test: Verificación completa del análisis de AT2020afhd."""
        # Simular el análisis completo
        periodo_observado = 19.6  # días (valor publicado)
        
        # Calcular frecuencia observada
        f_obs = calcular_frecuencia_observada(periodo_observado)
        
        # Verificar relación armónica
        ratio, n_octavas, error_pct = verificar_relacion_armonica(f_obs, F0_QCAL)
        
        # Verificaciones del modelo QCAL ∞³
        # 1. La frecuencia debe ser muy pequeña (escala de días)
        self.assertLess(f_obs, 1e-6, 
                       "La frecuencia observada debe ser < 1e-6 Hz para periodos de días")
        
        # 2. El ratio debe ser enorme (muchas octavas de separación)
        self.assertGreater(ratio, 1e8,
                          "El ratio f₀/f_obs debe ser > 1e8")
        
        # 3. Las octavas deben estar entre 27 y 28
        self.assertGreater(n_octavas, 27.0,
                          "Deben ser más de 27 octavas de separación")
        self.assertLess(n_octavas, 28.5,
                       "Deben ser menos de 28.5 octavas de separación")
        
        # 4. El error debe ser muy pequeño (< 1% para confirmación)
        self.assertLess(error_pct, 1.0,
                       "El error debe ser < 1% para confirmar el modelo QCAL ∞³")
        
        # 5. Verificación específica: debe estar muy cerca de 27.84 octavas
        self.assertAlmostEqual(n_octavas, 27.84, places=1,
                              msg="Las octavas calculadas deben coincidir con 27.84")
    
    def test_rango_de_periodos_validos(self):
        """Test: Verificar que el análisis funciona con rango de periodos."""
        # El paper reporta 19.6 ± 0.5 días
        periodos_test = [19.1, 19.6, 20.1]  # Rango de incertidumbre
        
        for periodo in periodos_test:
            f_obs = calcular_frecuencia_observada(periodo)
            ratio, n_octavas, error_pct = verificar_relacion_armonica(f_obs, F0_QCAL)
            
            # Para cualquier periodo en el rango, las octavas deben estar
            # muy cerca de 27.84 (error < 0.1 octavas)
            error_octavas = abs(n_octavas - EXPECTED_OCTAVES)
            self.assertLess(error_octavas, 0.1,
                          f"Para periodo={periodo} días, error en octavas debe ser < 0.1")
    
    def test_constantes_del_modelo(self):
        """Test: Verificar que las constantes del modelo son correctas."""
        # Verificar constantes físicas
        self.assertEqual(SECONDS_PER_DAY, 86400.0,
                        "Segundos por día debe ser 86400")
        
        # Verificar frecuencia fundamental QCAL ∞³
        self.assertAlmostEqual(F0_QCAL, 141.70001, places=5,
                              msg="Frecuencia fundamental debe ser 141.70001 Hz")
        
        # Verificar periodo esperado
        self.assertAlmostEqual(EXPECTED_PERIOD, 19.6, places=1,
                              msg="Periodo esperado debe ser 19.6 días")
        
        # Verificar octavas esperadas
        self.assertAlmostEqual(EXPECTED_OCTAVES, 27.84, places=2,
                              msg="Octavas esperadas deben ser 27.84")


class TestCasosLimite(unittest.TestCase):
    """Tests de casos límite y validaciones numéricas."""
    
    def test_periodo_muy_pequeno(self):
        """Test: Periodo muy pequeño (alta frecuencia)."""
        periodo = 0.001  # 0.001 días = 86.4 segundos
        f_obs = calcular_frecuencia_observada(periodo)
        
        # Verificar que la frecuencia es alta
        self.assertGreater(f_obs, 0.01)
        
        # Verificar que las octavas son menores
        ratio, n_octavas, _ = verificar_relacion_armonica(f_obs, F0_QCAL)
        self.assertLess(n_octavas, 27.84)
    
    def test_periodo_muy_grande(self):
        """Test: Periodo muy grande (baja frecuencia)."""
        periodo = 100.0  # 100 días
        f_obs = calcular_frecuencia_observada(periodo)
        
        # Verificar que la frecuencia es muy baja
        self.assertLess(f_obs, 1e-6)
        
        # Verificar que las octavas son mayores
        ratio, n_octavas, _ = verificar_relacion_armonica(f_obs, F0_QCAL)
        self.assertGreater(n_octavas, 27.84)
    
    def test_precision_numerica(self):
        """Test: Verificar precisión numérica en cálculos."""
        # Test de ida y vuelta: periodo -> frecuencia -> periodo
        periodo_original = 19.6
        f = calcular_frecuencia_observada(periodo_original)
        periodo_recalculado = 1.0 / (f * SECONDS_PER_DAY)
        
        # Verificar que recuperamos el periodo original
        self.assertAlmostEqual(periodo_original, periodo_recalculado, places=10)


def suite():
    """Crea la suite de tests."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAnalisisAT2020afhd))
    suite.addTest(unittest.makeSuite(TestCasosLimite))
    return suite


if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    # Salir con código apropiado
    sys.exit(0 if result.wasSuccessful() else 1)
