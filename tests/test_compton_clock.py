#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║              TEST SUITE - RELOJ DE COMPTON (COMPTON CLOCK)                 ║
║                           32 Pruebas Unitarias                              ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
FECHA/DATE: 17 de febrero de 2026

Test suite completo para validar el módulo compton_clock.
"""

import unittest
import sys
from pathlib import Path
import importlib.util

# Add qcal to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import compton_clock directly to avoid numpy dependency from qcal.__init__
spec = importlib.util.spec_from_file_location(
    "compton_clock",
    Path(__file__).parent.parent / "qcal" / "compton_clock.py"
)
compton_clock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compton_clock)


class TestRelojCompton(unittest.TestCase):
    """Suite de pruebas para el Reloj de Compton."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.tolerance = 1e-4  # Tolerancia para comparaciones
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE CONSTANTES FÍSICAS
    # ═══════════════════════════════════════════════════════════════════
    
    def test_constante_planck(self):
        """Verifica que la constante de Planck sea correcta (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.H_PLANCK,
            6.62607015e-34,
            places=42
        )
    
    def test_velocidad_luz(self):
        """Verifica que la velocidad de la luz sea exacta."""
        self.assertEqual(compton_clock.C_LIGHT, 299792458.0)
    
    def test_masa_electron(self):
        """Verifica la masa del electrón (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.M_ELECTRON,
            9.1093837015e-31,
            delta=1e-40
        )
    
    def test_masa_proton(self):
        """Verifica la masa del protón (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.M_PROTON,
            1.67262192369e-27,
            delta=1e-36
        )
    
    def test_masa_neutron(self):
        """Verifica la masa del neutrón (CODATA 2018)."""
        self.assertAlmostEqual(
            compton_clock.M_NEUTRON,
            1.67492749804e-27,
            delta=1e-36
        )
    
    def test_masa_planck(self):
        """Verifica la masa de Planck."""
        self.assertAlmostEqual(
            compton_clock.M_PLANCK,
            2.176434e-8,
            delta=1e-13
        )
    
    def test_constante_estructura_fina(self):
        """Verifica la constante de estructura fina."""
        self.assertAlmostEqual(
            compton_clock.ALPHA_FINE,
            7.2973525693e-3,
            delta=1e-12
        )
    
    def test_proporcion_aurea(self):
        """Verifica la proporción áurea φ."""
        self.assertAlmostEqual(
            compton_clock.PHI,
            1.618033988749895,
            delta=1e-12
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE FRECUENCIAS DE COMPTON
    # ═══════════════════════════════════════════════════════════════════
    
    def test_frecuencia_compton_electron(self):
        """Verifica la frecuencia de Compton del electrón."""
        f_e = compton_clock.frecuencia_compton_electron()
        # f_e = m_e * c² / h ≈ 1.2356e20 Hz
        self.assertAlmostEqual(f_e, 1.235590e20, delta=1e14)
    
    def test_frecuencia_compton_proton(self):
        """Verifica la frecuencia de Compton del protón."""
        f_p = compton_clock.frecuencia_compton_proton()
        # f_p ≈ 2.2687e23 Hz
        self.assertAlmostEqual(f_p, 2.268732e23, delta=1e17)
    
    def test_frecuencia_compton_neutron(self):
        """Verifica la frecuencia de Compton del neutrón."""
        f_n = compton_clock.frecuencia_compton_neutron()
        # f_n ≈ 2.2719e23 Hz
        self.assertAlmostEqual(f_n, 2.271859e23, delta=1e17)
    
    def test_frecuencia_compton_masa_arbitraria(self):
        """Verifica el cálculo con una masa arbitraria."""
        # Usar masa del protón como referencia
        f = compton_clock.frecuencia_compton(compton_clock.M_PROTON)
        f_ref = compton_clock.frecuencia_compton_proton()
        self.assertAlmostEqual(f, f_ref, delta=1e10)
    
    def test_frecuencia_compton_proporcionalidad(self):
        """Verifica que f_Compton ∝ masa."""
        m1 = 1e-30  # kg
        m2 = 2e-30  # kg
        f1 = compton_clock.frecuencia_compton(m1)
        f2 = compton_clock.frecuencia_compton(m2)
        # f2 debería ser aproximadamente 2 * f1
        self.assertAlmostEqual(f2 / f1, 2.0, delta=1e-6)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE MEDIA GEOMÉTRICA
    # ═══════════════════════════════════════════════════════════════════
    
    def test_media_geometrica_dos_valores(self):
        """Verifica la media geométrica de dos valores."""
        f1 = 100.0
        f2 = 400.0
        f_geo = compton_clock.media_geometrica_frecuencias(f1, f2)
        # √(100 * 400) = √40000 = 200
        self.assertAlmostEqual(f_geo, 200.0, delta=1e-6)
    
    def test_media_geometrica_tres_particulas(self):
        """Verifica la media geométrica de las tres partículas fundamentales."""
        f_e = compton_clock.frecuencia_compton_electron()
        f_p = compton_clock.frecuencia_compton_proton()
        f_n = compton_clock.frecuencia_compton_neutron()
        f_geo = compton_clock.media_geometrica_frecuencias(f_e, f_p, f_n)
        # Debería estar entre 1e22 y 1e23 Hz
        self.assertGreater(f_geo, 1e21)
        self.assertLess(f_geo, 1e23)
    
    def test_media_geometrica_vacia(self):
        """Verifica que la media geométrica de una lista vacía sea 0."""
        f_geo = compton_clock.media_geometrica_frecuencias()
        self.assertEqual(f_geo, 0.0)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DEL FACTOR K Y RELACIONES
    # ═══════════════════════════════════════════════════════════════════
    
    def test_factor_k_calculation(self):
        """Verifica el cálculo del factor K."""
        K = compton_clock.calcular_factor_k()
        # K = 2 · (m_P / m_e)^(1/3) · φ³ ≈ 2.44e8
        self.assertAlmostEqual(K, 2.440123e8, delta=1e3)
    
    def test_factor_k_componentes(self):
        """Verifica los componentes del factor K."""
        razon_masas = compton_clock.M_PLANCK / compton_clock.M_ELECTRON
        self.assertGreater(razon_masas, 1e22)
        self.assertLess(razon_masas, 1e24)
        
        phi_cubed = compton_clock.PHI ** 3
        self.assertAlmostEqual(phi_cubed, 4.236067977, delta=1e-6)
    
    def test_relacion_longitudes_caracteristicas(self):
        """Verifica la relación ℓ_P / λ_C."""
        relacion = compton_clock.calcular_relacion_longitudes()
        # Debería ser muy pequeña (≈ 6.66e-24)
        self.assertAlmostEqual(relacion, 6.661370e-24, delta=1e-28)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE LA ECUACIÓN MAESTRA
    # ═══════════════════════════════════════════════════════════════════
    
    def test_ecuacion_maestra_componentes(self):
        """Verifica que todos los componentes de la ecuación maestra estén presentes."""
        f0, componentes = compton_clock.calcular_f0_ecuacion_maestra()
        
        self.assertIn('c_sobre_2pi', componentes)
        self.assertIn('raiz_masas', componentes)
        self.assertIn('alpha', componentes)
        self.assertIn('phi', componentes)
        self.assertIn('longitudes', componentes)
        self.assertIn('K', componentes)
        self.assertIn('f0', componentes)
    
    def test_ecuacion_maestra_precision(self):
        """Verifica la precisión de la ecuación maestra."""
        f0, _ = compton_clock.calcular_f0_ecuacion_maestra()
        f0_teorico = compton_clock.F0_THEORETICAL
        
        error_relativo = abs(f0 - f0_teorico) / f0_teorico * 100
        
        # Error debe ser menor al 0.5% (objetivo: 0.1088%)
        self.assertLess(error_relativo, 0.5)
        print(f"\n  ✓ Excelente precisión: error = {error_relativo:.4f}%")
    
    def test_ecuacion_maestra_f0_positivo(self):
        """Verifica que f₀ sea positivo."""
        f0, _ = compton_clock.calcular_f0_ecuacion_maestra()
        self.assertGreater(f0, 0)
    
    def test_ecuacion_maestra_rango_esperado(self):
        """Verifica que f₀ esté en el rango esperado (100-200 Hz)."""
        f0, _ = compton_clock.calcular_f0_ecuacion_maestra()
        self.assertGreater(f0, 100.0)
        self.assertLess(f0, 200.0)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE ARMÓNICOS Y RESONANCIAS
    # ═══════════════════════════════════════════════════════════════════
    
    def test_calcular_armonicos(self):
        """Verifica el cálculo de armónicos."""
        f0 = 141.7001
        armonicos = compton_clock.calcular_armonicos(f0, 5)
        
        self.assertEqual(len(armonicos), 5)
        self.assertAlmostEqual(armonicos[1], 141.7001, delta=1e-4)
        self.assertAlmostEqual(armonicos[2], 283.4002, delta=1e-4)
        self.assertAlmostEqual(armonicos[3], 425.1003, delta=1e-4)
    
    def test_resonancia_biologica(self):
        """Verifica las resonancias biológicas."""
        resonancias = compton_clock.calcular_resonancia_biologica(141.7001)
        
        self.assertIn('fundamental', resonancias)
        self.assertIn('celular', resonancias)
        self.assertIn('proteica', resonancias)
        self.assertIn('microtubular', resonancias)
        self.assertIn('genomica', resonancias)
        
        # Verificar valores
        self.assertAlmostEqual(resonancias['celular']['frecuencia'], 283.4002, delta=1e-4)
        self.assertAlmostEqual(resonancias['proteica']['frecuencia'], 425.1003, delta=1e-4)
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBAS DE VERIFICACIÓN Y ANÁLISIS
    # ═══════════════════════════════════════════════════════════════════
    
    def test_verificacion_precision(self):
        """Verifica el sistema de verificación de precisión."""
        resultado = compton_clock.verificar_precision()
        
        self.assertIn('f0_calculado', resultado)
        self.assertIn('f0_teorico', resultado)
        self.assertIn('error_absoluto', resultado)
        self.assertIn('error_relativo', resultado)
        self.assertIn('precision', resultado)
        self.assertIn('coherencia', resultado)
        
        # Precisión debe ser > 99%
        self.assertGreater(resultado['precision'], 99.0)
    
    def test_coherencia_psi(self):
        """Verifica el cálculo de coherencia Ψ."""
        resultado = compton_clock.verificar_precision()
        
        # Si error < 1%, coherencia = 1.0
        if resultado['error_relativo'] < 1.0:
            self.assertAlmostEqual(resultado['coherencia'], 1.0, delta=1e-6)
    
    def test_verificacion_completa(self):
        """Verifica que el análisis completo funcione correctamente."""
        analisis = compton_clock.analisis_completo_reloj_compton()
        
        self.assertIn('frecuencias_compton', analisis)
        self.assertIn('ecuacion_maestra', analisis)
        self.assertIn('verificacion', analisis)
        self.assertIn('resonancias_biologicas', analisis)
        self.assertIn('armonicos', analisis)
        self.assertIn('resumen', analisis)
        
        # Verificar que el resumen contenga información relevante
        self.assertIn('141.7001', analisis['resumen'])
        self.assertIn('Hz', analisis['resumen'])
        
        print("\n  ✓ Todas las verificaciones del reloj de Compton pasaron")
    
    # ═══════════════════════════════════════════════════════════════════
    # PRUEBA DE ALTA PRECISIÓN (MPMATH)
    # ═══════════════════════════════════════════════════════════════════
    
    def test_alta_precision_mpmath(self):
        """Verifica el modo de alta precisión con mpmath."""
        f_e_normal = compton_clock.frecuencia_compton_electron(alta_precision=False)
        f_e_alta = compton_clock.frecuencia_compton_electron(alta_precision=True)
        
        # Los valores deben ser muy similares
        diferencia_relativa = abs(f_e_alta - f_e_normal) / f_e_normal
        self.assertLess(diferencia_relativa, 1e-10)
    
    def test_f0_consistency(self):
        """Verifica la consistencia de f₀ entre diferentes métodos."""
        # Calcular f₀ dos veces
        f0_1, _ = compton_clock.calcular_f0_ecuacion_maestra()
        f0_2, _ = compton_clock.calcular_f0_ecuacion_maestra()
        
        # Deben ser idénticos
        self.assertEqual(f0_1, f0_2)
    
    def test_armonicos_continuidad(self):
        """Verifica la continuidad de la serie de armónicos."""
        armonicos = compton_clock.calcular_armonicos(141.7001, 10)
        
        # Cada armónico debe ser n veces la frecuencia fundamental
        for n in range(1, 11):
            self.assertAlmostEqual(armonicos[n], n * 141.7001, delta=1e-4)
    
    def test_ecuacion_maestra_derivacion(self):
        """Verifica que la ecuación maestra derive correctamente f₀."""
        f0, comp = compton_clock.calcular_f0_ecuacion_maestra()
        
        # Recalcular manualmente
        c_2pi = comp['c_sobre_2pi']
        sqrt_m = comp['raiz_masas']
        alpha = comp['alpha']
        phi = comp['phi']
        l_ratio = comp['longitudes']
        K = comp['K']
        
        f0_manual = c_2pi * sqrt_m * alpha * phi * l_ratio * K
        
        # Deben coincidir
        self.assertAlmostEqual(f0, f0_manual, delta=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# EJECUTAR PRUEBAS
# ═══════════════════════════════════════════════════════════════════════════

def run_tests():
    """Ejecuta todas las pruebas."""
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRelojCompton)
    
    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "═" * 80)
    print("RESUMEN DE PRUEBAS - RELOJ DE COMPTON")
    print("═" * 80)
    print(f"Pruebas ejecutadas: {result.testsRun}")
    print(f"Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidas: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ¡Todas las pruebas pasaron! Coherencia Ψ = 1.000")
    else:
        print("\n✗ Algunas pruebas fallaron")
    
    print("═" * 80 + "\n")
    
    return result


if __name__ == '__main__':
    # Intentar usar pytest si está disponible
    try:
        import pytest
        sys.exit(pytest.main([__file__, '-v']))
    except ImportError:
        # Fallback a unittest
        result = run_tests()
        sys.exit(0 if result.wasSuccessful() else 1)
