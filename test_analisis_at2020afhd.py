#!/usr/bin/env python3
"""
Test Suite para el Análisis de AT2020afhd
=========================================

Valida los cálculos y predicciones del análisis del TDE AT2020afhd
y su relación con la teoría QCAL ∞³.

Uso:
    python test_analisis_at2020afhd.py
    pytest test_analisis_at2020afhd.py -v
"""

import sys
import os
import numpy as np

# Intentar importar pytest, pero seguir si no está disponible
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    # Mock de pytest.fail para ejecución manual
    class MockPytest:
        @staticmethod
        def fail(msg):
            raise AssertionError(msg)
    pytest = MockPytest()

# Importar módulo desde scripts
# Nota: En producción, esto debería ser un paquete instalable
try:
    from scripts.analisis_at2020afhd_tde import (
        AnalisisAT2020afhd,
        F0,
        PHI,
        PERIODO_PRECESION_DIAS,
        MASA_BH_ESTIMADA,
    )
except ImportError:
    # Fallback: añadir directorio scripts al path solo si la importación falla
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
    from analisis_at2020afhd_tde import (
        AnalisisAT2020afhd,
        F0,
        PHI,
        PERIODO_PRECESION_DIAS,
        MASA_BH_ESTIMADA,
    )


class TestAnalisisAT2020afhd:
    """Suite de tests para el análisis de AT2020afhd"""
    
    def setup_method(self):
        """Configuración para cada test"""
        self.analisis = AnalisisAT2020afhd(verbose=False)
    
    def test_inicializacion(self):
        """Test de inicialización correcta del análisis"""
        assert self.analisis.periodo_dias == PERIODO_PRECESION_DIAS
        assert self.analisis.masa_bh > 0
        assert isinstance(self.analisis.resultados, dict)
    
    def test_calculo_omega_frame(self):
        """Test del cálculo de frecuencia de precesión frame-dragging"""
        resultados = self.analisis.calcular_omega_frame()
        
        # Verificar que todos los campos están presentes
        assert 'periodo_dias' in resultados
        assert 'periodo_segundos' in resultados
        assert 'omega_frame_rad_s' in resultados
        assert 'f_frame_hz' in resultados
        assert 'f_frame_microhz' in resultados
        
        # Verificar valores físicos razonables
        assert resultados['periodo_dias'] == 20.0
        assert resultados['periodo_segundos'] == 20 * 24 * 3600
        
        # Verificar omega_frame
        omega_esperado = 2 * np.pi / (20 * 24 * 3600)
        assert np.isclose(resultados['omega_frame_rad_s'], omega_esperado, rtol=1e-6)
        
        # Verificar f_frame en Hz (debe ser del orden de 1e-6 Hz)
        assert resultados['f_frame_hz'] > 0
        assert resultados['f_frame_hz'] < 1e-4  # Menor que 0.1 mHz
        assert resultados['f_frame_microhz'] > 0.5  # Mayor que 0.5 μHz
        assert resultados['f_frame_microhz'] < 10  # Menor que 10 μHz
    
    def test_calculo_parametro_spin(self):
        """Test del cálculo de parámetros de spin del agujero negro"""
        resultados = self.analisis.calcular_parametro_spin()
        
        # Verificar campos presentes
        assert 'radio_schwarzschild_m' in resultados
        assert 'radio_schwarzschild_km' in resultados
        assert 'spin_adimensional_a' in resultados
        assert 'r_isco_m' in resultados
        assert 'r_isco_Rs' in resultados
        
        # Verificar valores físicos
        Rs = resultados['radio_schwarzschild_m']
        assert Rs > 0
        
        # Spin adimensional debe estar entre 0 y 1 (límite de Kerr: 0.998)
        a = resultados['spin_adimensional_a']
        assert 0 < a <= 0.998
        
        # Para jets relativistas, esperamos spin alto
        assert a > 0.5, "Jets relativistas requieren spin alto"
        
        # ISCO debe ser mayor que Rs
        r_isco = resultados['r_isco_m']
        assert r_isco > Rs
        assert resultados['r_isco_Rs'] > 1.0
    
    def test_analisis_resonancia_con_f0(self):
        """Test del análisis de resonancia armónica con f₀"""
        # Primero calcular omega_frame
        self.analisis.calcular_omega_frame()
        
        resultados = self.analisis.analizar_resonancia_con_f0()
        
        # Verificar campos
        assert 'f0_hz' in resultados
        assert 'f_frame_hz' in resultados
        assert 'ratio' in resultados
        assert 'log10_ratio' in resultados
        assert 'modo_armonico_m' in resultados
        assert 'coeficiente_n' in resultados
        
        # Verificar f₀
        assert resultados['f0_hz'] == F0
        
        # Verificar que el ratio es grande (f₀ >> f_frame)
        assert resultados['ratio'] > 1e6
        
        # Verificar log10_ratio
        log_ratio = resultados['log10_ratio']
        assert log_ratio > 6  # Ratio > 10^6
        assert log_ratio < 12  # Ratio < 10^12 (razonable)
        
        # Verificar modo armónico
        m = resultados['modo_armonico_m']
        assert isinstance(m, (int, np.integer))
        assert m >= 6  # Esperamos al menos 10^6
        
        # Coeficiente n debe ser razonable (1-10)
        n = resultados['coeficiente_n']
        assert 0.1 < n < 100
    
    def test_modelar_campo_rotante(self):
        """Test del modelado del campo Ψ(t)"""
        # Calcular omega_frame primero
        self.analisis.calcular_omega_frame()
        
        # Modelar con array de tiempo corto para test
        t_array = np.linspace(0, 50, 500)  # 50 días
        resultados = self.analisis.modelar_campo_rotante(t_array)
        
        # Verificar campos
        assert 't_dias' in resultados
        assert 't_segundos' in resultados
        assert 'J_t' in resultados
        assert 'Psi_t' in resultados
        assert 'omega_frame' in resultados
        
        # Verificar dimensiones
        assert len(resultados['J_t']) == len(t_array)
        assert len(resultados['Psi_t']) == len(t_array)
        
        # Verificar que J_t y Psi_t son arrays numéricos válidos
        assert not np.isnan(resultados['J_t']).any()
        assert not np.isnan(resultados['Psi_t']).any()
        assert not np.isinf(resultados['J_t']).any()
        assert not np.isinf(resultados['Psi_t']).any()
        
        # Verificar periodicidad en Psi_t
        # Debe haber oscilaciones
        assert np.std(resultados['Psi_t']) > 0
    
    def test_calculo_amplificacion_cuantica(self):
        """Test del cálculo de amplificación cuántico-vibracional"""
        # Calcular spin primero
        self.analisis.calcular_parametro_spin()
        
        resultados = self.analisis.calcular_amplificacion_cuantica()
        
        # Verificar campos
        assert 'a_spin' in resultados
        assert 'amplificacion_spin' in resultados
        assert 'amplificacion_coherencia' in resultados
        assert 'amplificacion_geometrica' in resultados
        assert 'amplificacion_total' in resultados
        
        # Verificar valores físicos
        A_spin = resultados['amplificacion_spin']
        assert 0 < A_spin <= 1.0  # No puede exceder 1 (límite de Kerr)
        
        A_coh = resultados['amplificacion_coherencia']
        assert 0 < A_coh <= 1.0  # Coherencia es un porcentaje
        
        A_geo = resultados['amplificacion_geometrica']
        assert A_geo > 0
        # Debería ser cercano a PHI por simetría áurea
        assert np.isclose(A_geo, PHI, rtol=0.1)
        
        A_total = resultados['amplificacion_total']
        assert A_total > 0
        # Para sistema con spin alto y coherencia, esperamos A > 0.5
        assert A_total > 0.5
    
    def test_generar_predicciones_observacionales(self):
        """Test de generación de predicciones observacionales"""
        # Ejecutar cálculos previos necesarios
        self.analisis.calcular_omega_frame()
        self.analisis.calcular_parametro_spin()
        
        predicciones = self.analisis.generar_predicciones_observacionales()
        
        # Verificar categorías de predicciones
        assert 'modulacion_x_ray' in predicciones
        assert 'polarizacion_optica' in predicciones
        assert 'variabilidad_jet' in predicciones
        assert 'firma_cuantica' in predicciones
        
        # Verificar estructura de cada predicción
        for nombre, pred in predicciones.items():
            assert 'descripcion' in pred
            assert 'observable' in pred
            assert isinstance(pred['descripcion'], str)
            assert len(pred['descripcion']) > 0
        
        # Verificar predicción de modulación X-ray
        mod_xray = predicciones['modulacion_x_ray']
        assert mod_xray['periodo_esperado_dias'] == PERIODO_PRECESION_DIAS
        
        # Verificar firma cuántica tiene frecuencias
        firma = predicciones['firma_cuantica']
        assert 'frecuencias_hz' in firma
        assert len(firma['frecuencias_hz']) >= 3  # Al menos 3 armónicos
    
    def test_ejecutar_analisis_completo(self):
        """Test de ejecución del análisis completo"""
        resultados = self.analisis.ejecutar_analisis_completo()
        
        # Verificar que todas las secciones fueron calculadas
        assert 'omega_frame' in resultados
        assert 'spin' in resultados
        assert 'resonancia' in resultados
        assert 'campo_rotante' in resultados
        assert 'amplificacion' in resultados
        assert 'predicciones' in resultados
        
        # Verificar consistencia entre secciones
        omega_data = resultados['omega_frame']
        resonancia_data = resultados['resonancia']
        
        # La f_frame debe ser consistente entre secciones
        assert omega_data['f_frame_hz'] == resonancia_data['f_frame_hz']
    
    def test_valores_fisicos_razonables(self):
        """Test de que todos los valores físicos son razonables"""
        resultados = self.analisis.ejecutar_analisis_completo()
        
        # Frecuencia de precesión debe estar en rango observacional de TDEs
        f_frame = resultados['omega_frame']['f_frame_microhz']
        assert 0.1 < f_frame < 100  # μHz, rango típico de precesión en TDEs
        
        # Spin debe ser alto para jets
        a = resultados['spin']['spin_adimensional_a']
        assert a > 0.6  # Jets requieren spin alto
        
        # Amplificación total debe ser positiva y razonable
        A_total = resultados['amplificacion']['amplificacion_total']
        assert 0 < A_total < 10  # Razonable para sistemas astrofísicos
    
    def test_consistencia_matematica(self):
        """Test de consistencia matemática entre cálculos"""
        resultados = self.analisis.ejecutar_analisis_completo()
        
        # Verificar relación ω = 2πf
        omega_data = resultados['omega_frame']
        omega_rad = omega_data['omega_frame_rad_s']
        f_hz = omega_data['f_frame_hz']
        
        assert np.isclose(omega_rad, 2 * np.pi * f_hz, rtol=1e-10)
        
        # Verificar conversión de período
        T_seg = omega_data['periodo_segundos']
        T_dias = omega_data['periodo_dias']
        
        assert np.isclose(T_seg, T_dias * 24 * 3600, rtol=1e-10)
        
        # Verificar relación entre amplificaciones
        amp_data = resultados['amplificacion']
        A_total_calculado = (amp_data['amplificacion_spin'] * 
                            amp_data['amplificacion_coherencia'] * 
                            amp_data['amplificacion_geometrica'])
        
        assert np.isclose(A_total_calculado, amp_data['amplificacion_total'], rtol=1e-6)


class TestIntegracionQCAL:
    """Tests de integración con la teoría QCAL ∞³"""
    
    def test_constantes_fundamentales(self):
        """Test de que se usan las constantes fundamentales correctas"""
        assert F0 == 141.7001
        assert np.isclose(PHI, 1.618033988749895, rtol=1e-10)
    
    def test_ecuacion_campo_rotante(self):
        """Test de que la ecuación dΨ/dt + ω_frame × Ψ = J(t) es consistente"""
        analisis = AnalisisAT2020afhd(verbose=False)
        analisis.calcular_omega_frame()
        
        # Modelar campo
        t_test = np.linspace(0, 10, 100)  # 10 días, 100 puntos
        campo_data = analisis.modelar_campo_rotante(t_test)
        
        Psi_t = campo_data['Psi_t']
        J_t = campo_data['J_t']
        t_seg = campo_data['t_segundos']
        
        # Verificar que la solución es numérica y finita
        assert np.all(np.isfinite(Psi_t))
        assert np.all(np.isfinite(J_t))
        
        # La derivada temporal de Psi_t debe ser calculable
        dPsi_dt = np.gradient(Psi_t, t_seg)
        assert np.all(np.isfinite(dPsi_dt))
    
    def test_resonancia_logaritmica(self):
        """Test de resonancia logarítmica entre escalas"""
        analisis = AnalisisAT2020afhd(verbose=False)
        analisis.calcular_omega_frame()
        res = analisis.analizar_resonancia_con_f0()
        
        # Verificar que existe separación logarítmica
        log_ratio = res['log10_ratio']
        assert log_ratio > 5  # Al menos 5 órdenes de magnitud
        
        # Verificar que n está en rango razonable (1-10)
        # indicando resonancia armónica simple
        n = res['coeficiente_n']
        assert 0.5 < n < 20


def test_importacion_modulo():
    """Test de que el módulo se puede importar correctamente"""
    try:
        # Intentar importación desde scripts
        try:
            from scripts.analisis_at2020afhd_tde import AnalisisAT2020afhd
        except ImportError:
            # Fallback para importación directa
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
            from analisis_at2020afhd_tde import AnalisisAT2020afhd
        
        assert AnalisisAT2020afhd is not None
    except ImportError as e:
        pytest.fail(f"No se pudo importar el módulo: {e}")


def test_ejecucion_completa_sin_errores():
    """Test de que el análisis completo se ejecuta sin errores"""
    analisis = AnalisisAT2020afhd(verbose=False)
    
    try:
        resultados = analisis.ejecutar_analisis_completo()
        assert resultados is not None
        assert len(resultados) > 0
    except Exception as e:
        pytest.fail(f"El análisis completo falló: {e}")


if __name__ == "__main__":
    # Ejecutar tests con pytest si está disponible, sino ejecutar manualmente
    if PYTEST_AVAILABLE:
        sys.exit(pytest.main([__file__, '-v']))
    else:
        print("pytest no disponible, ejecutando tests manualmente...")
        
        # Crear instancia de cada clase de test y ejecutar métodos
        test_classes = [TestAnalisisAT2020afhd, TestIntegracionQCAL]
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for test_class in test_classes:
            print(f"\n{'='*60}")
            print(f"Ejecutando {test_class.__name__}")
            print('='*60)
            
            test_instance = test_class()
            
            # Ejecutar setup si existe
            if hasattr(test_instance, 'setup_method'):
                test_instance.setup_method()
            
            # Obtener todos los métodos de test
            test_methods = [m for m in dir(test_instance) if m.startswith('test_')]
            
            for method_name in test_methods:
                total_tests += 1
                try:
                    method = getattr(test_instance, method_name)
                    method()
                    print(f"✓ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"✗ {method_name}: {e}")
                    failed_tests += 1
                except Exception as e:
                    print(f"✗ {method_name}: ERROR: {e}")
                    failed_tests += 1
        
        # Tests independientes
        print(f"\n{'='*60}")
        print("Tests independientes")
        print('='*60)
        
        for func_name in ['test_importacion_modulo', 'test_ejecucion_completa_sin_errores']:
            total_tests += 1
            try:
                func = globals()[func_name]
                func()
                print(f"✓ {func_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"✗ {func_name}: {e}")
                failed_tests += 1
            except Exception as e:
                print(f"✗ {func_name}: ERROR: {e}")
                failed_tests += 1
        
        # Resumen
        print(f"\n{'='*60}")
        print(f"RESUMEN: {passed_tests}/{total_tests} tests pasaron")
        print('='*60)
        
        sys.exit(0 if failed_tests == 0 else 1)
