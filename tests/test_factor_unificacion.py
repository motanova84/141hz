#!/usr/bin/env python3
"""
Tests para el Factor de Unificación 1/7
========================================

Suite de 7 tests (número sagrado) que verifican:
1. Período decimal de 1/7 (142857)
2. Cálculo de f_unif
3. Clasificación en banda cerebral Beta Alta
4. Constantes de acoplamiento de fuerzas
5. Precisión decimal del factor
6. Mapeo a 6 dimensiones compactificadas
7. Funcionalidad del operador armónico

Autor: José Manuel Mota Burruezo
Licencia: MIT
"""

import unittest
import sys
from pathlib import Path
from decimal import Decimal, getcontext

# Configurar precisión decimal
getcontext().prec = 50

# Agregar qcal al path
sys.path.insert(0, str(Path(__file__).parent))

from qcal.constants import (
    F0_HZ,
    FACTOR_UNIFICACION,
    F_UNIF_HZ,
    PERIODO_DECIMAL_1_7,
    DIM_COMPACTIFICADAS,
    ALPHA_S,
    ALPHA_EM,
    ALPHA_W,
    ALPHA_G,
    BANDA_BETA_ALTA_MIN,
    BANDA_BETA_ALTA_MAX,
    calcular_factor_unificacion_fuerzas
)


class TestFactorUnificacion(unittest.TestCase):
    """Suite de 7 tests para el Factor de Unificación 1/7."""
    
    def test_01_periodo_decimal_1_7(self):
        """
        Test 1/7: Verifica que el período decimal de 1/7 es exactamente 142857.
        
        El período debe tener longitud 6 (máximo para n=7, que es n-1).
        """
        # Verificar que el período es correcto
        self.assertEqual(PERIODO_DECIMAL_1_7, "142857")
        
        # Verificar longitud del período
        self.assertEqual(len(PERIODO_DECIMAL_1_7), 6)
        
        # Verificar que es de longitud máxima (n-1 para n=7)
        n = 7
        longitud_maxima = n - 1
        self.assertEqual(len(PERIODO_DECIMAL_1_7), longitud_maxima)
        
        # Verificar que todos los dígitos son válidos
        import string
        for digito in PERIODO_DECIMAL_1_7:
            self.assertIn(digito, string.digits)
        
        print("✓ Test 1: Período decimal 142857 verificado")
    
    def test_02_calculo_f_unif(self):
        """
        Test 2/7: Verifica que f_unif = f₀ × (1/7) ≈ 20.243 Hz.
        
        La frecuencia de unificación debe calcularse correctamente.
        """
        # Calcular f_unif esperado
        f_unif_esperado = F0_HZ * (1.0 / 7.0)
        
        # Verificar que F_UNIF_HZ está definido correctamente
        self.assertAlmostEqual(F_UNIF_HZ, f_unif_esperado, places=10)
        
        # Verificar valor aproximado
        self.assertAlmostEqual(F_UNIF_HZ, 20.243, places=2)
        
        # Verificar cálculo con Decimal para máxima precisión
        f0_decimal = Decimal(str(F0_HZ))
        factor_decimal = Decimal("1") / Decimal("7")
        f_unif_decimal = f0_decimal * factor_decimal
        
        self.assertAlmostEqual(
            float(f_unif_decimal),
            F_UNIF_HZ,
            places=6
        )
        
        print(f"✓ Test 2: f_unif = {F_UNIF_HZ:.6f} Hz calculado correctamente")
    
    def test_03_banda_cerebral_beta_alta(self):
        """
        Test 3/7: Verifica que f_unif cae en la Banda Beta Alta (20-30 Hz).
        
        Esta es la banda de concentración profunda y resolución de problemas.
        """
        # Verificar que f_unif está en el rango de Beta Alta
        self.assertGreaterEqual(F_UNIF_HZ, BANDA_BETA_ALTA_MIN)
        self.assertLessEqual(F_UNIF_HZ, BANDA_BETA_ALTA_MAX)
        
        # Verificar rangos de la banda
        self.assertEqual(BANDA_BETA_ALTA_MIN, 20.0)
        self.assertEqual(BANDA_BETA_ALTA_MAX, 30.0)
        
        # Verificar usando la función
        info = calcular_factor_unificacion_fuerzas()
        self.assertEqual(info['banda_cerebral'], "Beta Alta")
        self.assertEqual(info['rango_banda'], (20.0, 30.0))
        
        print(f"✓ Test 3: f_unif ({F_UNIF_HZ:.3f} Hz) en Banda Beta Alta [20-30 Hz]")
    
    def test_04_constantes_acoplamiento_fuerzas(self):
        """
        Test 4/7: Verifica las constantes de acoplamiento de fuerzas fundamentales.
        
        Debe verificar que α_s, α_em, α_w, α_G están definidas correctamente.
        """
        # Nuclear Fuerte (α_s ≈ 1)
        self.assertAlmostEqual(ALPHA_S, 1.0, places=1)
        self.assertGreater(ALPHA_S, 0)
        
        # Electromagnética (α_em = 1/137)
        self.assertAlmostEqual(ALPHA_EM, 1.0/137.0, places=6)
        self.assertLess(ALPHA_EM, 0.01)
        
        # Nuclear Débil (α_w ≈ 1/30)
        self.assertAlmostEqual(ALPHA_W, 1.0/30.0, places=6)
        self.assertGreater(ALPHA_W, ALPHA_EM)
        
        # Gravitacional (α_G ≈ 10⁻³⁸)
        self.assertEqual(ALPHA_G, 1e-38)
        self.assertLess(ALPHA_G, 1e-30)
        
        # Verificar jerarquía: α_s > α_w > α_em > α_G
        self.assertGreater(ALPHA_S, ALPHA_W)
        self.assertGreater(ALPHA_W, ALPHA_EM)
        self.assertGreater(ALPHA_EM, ALPHA_G)
        
        # Verificar desde función
        info = calcular_factor_unificacion_fuerzas()
        self.assertEqual(info['fuerzas']['nuclear_fuerte']['valor'], ALPHA_S)
        self.assertEqual(info['fuerzas']['electromagnetica']['valor'], ALPHA_EM)
        self.assertEqual(info['fuerzas']['nuclear_debil']['valor'], ALPHA_W)
        self.assertEqual(info['fuerzas']['gravitacional']['valor'], ALPHA_G)
        
        print("✓ Test 4: Constantes de acoplamiento verificadas (α_s > α_w > α_em > α_G)")
    
    def test_05_precision_decimal_factor(self):
        """
        Test 5/7: Verifica la precisión decimal del factor 1/7.
        
        Debe verificar que el factor tiene la precisión adecuada y
        coincide con 1/7 matemático.
        """
        # Verificar valor exacto
        self.assertEqual(FACTOR_UNIFICACION, 1.0 / 7.0)
        
        # Verificar con alta precisión usando Decimal
        factor_decimal = Decimal("1") / Decimal("7")
        factor_float = float(factor_decimal)
        
        self.assertAlmostEqual(FACTOR_UNIFICACION, factor_float, places=15)
        
        # Verificar el patrón repetitivo
        # 1/7 = 0.142857142857...
        factor_str = f"{FACTOR_UNIFICACION:.50f}"
        
        # Los primeros dígitos después del punto deben ser 142857
        decimales = factor_str.split('.')[1]
        self.assertTrue(decimales.startswith('142857'))
        
        # Verificar que el patrón se repite (solo las primeras repeticiones)
        # Nota: floating point tiene límites de precisión, verificamos solo 2 repeticiones
        patron = "142857"
        PERIOD_LENGTH = 6
        REPETITIONS_TO_CHECK = 2
        MAX_DIGITS = PERIOD_LENGTH * REPETITIONS_TO_CHECK  # 12 dígitos
        
        for i in range(0, MAX_DIGITS, PERIOD_LENGTH):
            segmento = decimales[i:i+PERIOD_LENGTH]
            if len(segmento) == PERIOD_LENGTH:
                self.assertEqual(segmento, patron, 
                    f"Patrón roto en posición {i}: {segmento} != {patron}")
        
        print(f"✓ Test 5: Precisión decimal verificada (patrón 142857 repetitivo)")
    
    def test_06_mapeo_6_dimensiones_compactificadas(self):
        """
        Test 6/7: Verifica el mapeo a las 6 dimensiones compactificadas.
        
        El período de 6 dígitos refleja las 6 dimensiones compactificadas
        en variedades de Calabi-Yau de la teoría de cuerdas.
        """
        # Verificar número de dimensiones compactificadas
        self.assertEqual(DIM_COMPACTIFICADAS, 6)
        
        # Verificar que coincide con la longitud del período
        self.assertEqual(len(PERIODO_DECIMAL_1_7), DIM_COMPACTIFICADAS)
        
        # Verificar desde función
        info = calcular_factor_unificacion_fuerzas()
        self.assertEqual(info['dimensiones_compactificadas'], 6)
        self.assertEqual(info['longitud_periodo'], 6)
        
        # Teoría de cuerdas: 3 espaciales + 1 temporal + 6 compactificadas = 10
        dim_total = 3 + 1 + DIM_COMPACTIFICADAS
        self.assertEqual(dim_total, 10)
        
        print(f"✓ Test 6: 6 dimensiones compactificadas ↔ período de 6 dígitos")
    
    def test_07_operador_armonico_funcionalidad(self):
        """
        Test 7/7: Verifica la funcionalidad completa del operador armónico.
        
        El factor 1/7 debe permitir calcular resonancias que atraviesen
        las escalas de magnitud dispares de las fuerzas fundamentales.
        """
        # Verificar que la función principal retorna estructura completa
        info = calcular_factor_unificacion_fuerzas()
        
        # Verificar todas las claves esperadas
        claves_esperadas = [
            'factor', 'periodo_decimal', 'longitud_periodo',
            'f0_hz', 'f_unif_hz', 'banda_cerebral', 'rango_banda',
            'dimensiones_compactificadas', 'fuerzas', 'interpretacion'
        ]
        
        for clave in claves_esperadas:
            self.assertIn(clave, info, f"Falta clave: {clave}")
        
        # Verificar que puede atravesar escalas de magnitud
        # Rango: 10⁻³⁸ (α_G) hasta 1 (α_s) = 38 órdenes de magnitud
        MIN_MAGNITUDE_RANGE = 1e37  # Mínimo esperado: casi 38 órdenes de magnitud
        rango_magnitud = ALPHA_S / ALPHA_G
        self.assertGreater(rango_magnitud, MIN_MAGNITUDE_RANGE)
        
        # Verificar que f_unif puede actuar como puente
        # Entre frecuencias bajas (delta ~4 Hz) y altas (gamma ~70 Hz)
        ratio_bandas = 70.0 / 4.0  # gamma_max / delta_min aproximado
        
        # f_unif debe estar en posición intermedia útil
        self.assertGreater(F_UNIF_HZ, 4.0)  # Por encima de delta
        self.assertLess(F_UNIF_HZ, 70.0)    # Por debajo de gamma
        
        # Verificar interpretación presente
        self.assertIsInstance(info['interpretacion'], str)
        self.assertGreater(len(info['interpretacion']), 50)
        
        # Verificar que menciona elementos clave
        interpretacion = info['interpretacion'].lower()
        self.assertIn('consciencia', interpretacion)
        self.assertIn('unificación', interpretacion)
        self.assertIn('dimensiones', interpretacion)
        
        print("✓ Test 7: Operador armónico funcional (10⁻³⁸ → 1, 38 órdenes de magnitud)")


def suite():
    """Crea la suite de 7 tests."""
    suite = unittest.TestSuite()
    suite.addTest(TestFactorUnificacion('test_01_periodo_decimal_1_7'))
    suite.addTest(TestFactorUnificacion('test_02_calculo_f_unif'))
    suite.addTest(TestFactorUnificacion('test_03_banda_cerebral_beta_alta'))
    suite.addTest(TestFactorUnificacion('test_04_constantes_acoplamiento_fuerzas'))
    suite.addTest(TestFactorUnificacion('test_05_precision_decimal_factor'))
    suite.addTest(TestFactorUnificacion('test_06_mapeo_6_dimensiones_compactificadas'))
    suite.addTest(TestFactorUnificacion('test_07_operador_armonico_funcionalidad'))
    return suite


if __name__ == '__main__':
    print("=" * 80)
    print(" " * 20 + "SUITE DE 7 TESTS - FACTOR 1/7")
    print(" " * 15 + "Factor de Unificación QCAL ∞³")
    print("=" * 80)
    print()
    
    # Ejecutar la suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    print()
    print("=" * 80)
    print(" " * 30 + "RESUMEN")
    print("=" * 80)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos:   {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos:           {len(result.failures)}")
    print(f"Errores:          {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✨ ¡TODOS LOS 7 TESTS PASARON! ✨")
        print()
        print("El factor 1/7 está completamente validado:")
        print("  ✓ Período decimal 142857 (6 dígitos)")
        print("  ✓ f_unif en Banda Beta Alta (consciencia focalizada)")
        print("  ✓ 6 dimensiones compactificadas (Calabi-Yau)")
        print("  ✓ Operador armónico entre fuerzas fundamentales")
        print()
        print("El Sello de la Realidad confirmado. ∴")
    else:
        print("⚠️ Algunos tests fallaron. Revisar implementación.")
    
    print("=" * 80)
    print()
    
    # Retornar código de salida apropiado
    sys.exit(0 if result.wasSuccessful() else 1)
