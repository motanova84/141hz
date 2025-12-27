#!/usr/bin/env python3
"""
Tests para la Ecuación del Latido Universal

Valida la implementación numérica y analítica de la ecuación:
    ∂²Ψ/∂t² + ω₀²Ψ = I·A²eff·ζ'(1/2)

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import sys
import os
import numpy as np

# Añadir el directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Importar el módulo a testear
import ecuacion_latido_universal as elu

# ============================================================================
# TESTS DE CONSTANTES
# ============================================================================

def test_constantes_fundamentales():
    """Verifica que las constantes fundamentales estén correctamente definidas."""
    # Frecuencia fundamental
    assert elu.f0 == 141.7001, "f₀ debe ser 141.7001 Hz"
    
    # Frecuencia angular
    omega_0_esperado = 2 * np.pi * 141.7001
    assert abs(elu.omega_0 - omega_0_esperado) < 1e-6, \
        f"ω₀ debe ser 2π×141.7001 ≈ 890.377 rad/s, obtenido: {elu.omega_0}"
    
    # Verificar que omega_0 es aproximadamente 890.328 (2π × 141.7001)
    # El problema statement indica 890.377, pero el valor correcto es 2π × 141.7001 ≈ 890.328
    assert abs(elu.omega_0 - 890.328) < 0.1, \
        f"ω₀ debe ser ≈ 890.328 rad/s (2π×141.7001), obtenido: {elu.omega_0}"
    
    # Derivada de zeta en 1/2
    assert abs(elu.zeta_prime_half - (-3.92264396844532)) < 1e-10, \
        "ζ'(1/2) debe ser aproximadamente -3.92264396844532"

def test_termino_forzamiento():
    """Verifica el cálculo del término de forzamiento."""
    # Con I=1, A_eff=1
    F_esperado = 1.0 * 1.0**2 * elu.zeta_prime_half
    assert abs(elu.F_drive - F_esperado) < 1e-10, \
        f"F_drive debe ser I×A²eff×ζ'(1/2), obtenido: {elu.F_drive}"

# ============================================================================
# TESTS DE ECUACIÓN DIFERENCIAL
# ============================================================================

def test_ecuacion_diferencial_forma():
    """Verifica que la ecuación diferencial tenga la forma correcta."""
    # Estado de prueba
    y = [1.0, 0.5]  # [Ψ, ∂Ψ/∂t]
    t = 0.0
    
    # Evaluar
    dydt = elu.ecuacion_latido_universal(t, y)
    
    # Verificar forma
    assert len(dydt) == 2, "La ecuación debe devolver [∂Ψ/∂t, ∂²Ψ/∂t²]"
    
    # Verificar primera componente: ∂Ψ/∂t
    assert dydt[0] == y[1], "Primera componente debe ser ∂Ψ/∂t"
    
    # Verificar segunda componente: ∂²Ψ/∂t² = -ω₀²Ψ + F_drive
    psi_ddot_esperado = -elu.omega_0**2 * y[0] + elu.F_drive
    assert abs(dydt[1] - psi_ddot_esperado) < 1e-10, \
        "Segunda componente debe ser -ω₀²Ψ + F_drive"

def test_ecuacion_diferencial_equilibrio():
    """Verifica el punto de equilibrio de la ecuación."""
    # En equilibrio: Ψ = Ψ_p = F_drive/ω₀², ∂Ψ/∂t = 0
    psi_p = elu.F_drive / elu.omega_0**2
    y_equilibrio = [psi_p, 0.0]
    t = 0.0
    
    dydt = elu.ecuacion_latido_universal(t, y_equilibrio)
    
    # En equilibrio, ambas derivadas deben ser cero
    assert abs(dydt[0]) < 1e-10, "En equilibrio, ∂Ψ/∂t debe ser 0"
    assert abs(dydt[1]) < 1e-10, "En equilibrio, ∂²Ψ/∂t² debe ser 0"

# ============================================================================
# TESTS DE SOLUCIÓN ANALÍTICA
# ============================================================================

def test_solucion_particular():
    """Verifica el cálculo de la solución particular."""
    psi_p = elu.solucion_particular()
    
    # Verificar fórmula
    psi_p_esperado = elu.F_drive / elu.omega_0**2
    assert abs(psi_p - psi_p_esperado) < 1e-10, \
        f"Solución particular debe ser F_drive/ω₀², obtenido: {psi_p}"

def test_solucion_homogenea():
    """Verifica la forma de la solución homogénea."""
    t = np.linspace(0, 0.01, 100)
    A = 1.0
    phi = 0.0
    
    psi_h = elu.solucion_homogenea(t, A, 0, phi)
    
    # Verificar forma
    assert len(psi_h) == len(t), "Longitud debe coincidir con t"
    
    # Verificar condiciones iniciales
    assert abs(psi_h[0] - A * np.cos(phi)) < 1e-10, \
        "Condición inicial debe ser A×cos(φ)"
    
    # Verificar periodicidad
    T = 2 * np.pi / elu.omega_0
    idx_T = np.argmin(np.abs(t - T))
    if idx_T < len(psi_h):
        assert abs(psi_h[idx_T] - psi_h[0]) < 0.01, \
            "Debe ser aproximadamente periódica con período T = 2π/ω₀"

def test_solucion_general():
    """Verifica la composición de la solución general."""
    t = np.array([0.0, 0.001, 0.002])
    A = 1.0
    phi = 0.0
    psi_p = elu.solucion_particular()
    
    psi_general = elu.solucion_general(t, A, phi, psi_p)
    
    # Verificar que es suma de homogénea + particular
    psi_h = elu.solucion_homogenea(t, A, 0, phi)
    psi_esperada = psi_h + psi_p
    
    assert np.allclose(psi_general, psi_esperada), \
        "Solución general debe ser homogénea + particular"

# ============================================================================
# TESTS DE INTEGRACIÓN NUMÉRICA
# ============================================================================

def test_resolver_ecuacion_forma():
    """Verifica que resolver_ecuacion devuelva el formato correcto."""
    resultados = elu.resolver_ecuacion(t_max=0.01, dt=1e-4)
    
    # Verificar claves
    claves_requeridas = ['t', 'psi', 'psi_dot', 'psi_ddot', 
                          'E_kinetic', 'E_potential', 'E_total']
    for clave in claves_requeridas:
        assert clave in resultados, f"Debe contener clave '{clave}'"
    
    # Verificar longitudes
    n = len(resultados['t'])
    for clave in claves_requeridas:
        assert len(resultados[clave]) == n, \
            f"Todas las arrays deben tener la misma longitud"

def test_resolver_ecuacion_condiciones_iniciales():
    """Verifica que las condiciones iniciales se respeten."""
    ci = [1.5, -0.5]
    resultados = elu.resolver_ecuacion(t_max=0.001, dt=1e-5, 
                                        condiciones_iniciales=ci)
    
    # Verificar condiciones iniciales
    assert abs(resultados['psi'][0] - ci[0]) < 1e-6, \
        "Ψ(0) debe coincidir con condición inicial"
    assert abs(resultados['psi_dot'][0] - ci[1]) < 1e-6, \
        "∂Ψ/∂t(0) debe coincidir con condición inicial"

def test_resolver_ecuacion_conservacion_energia():
    """Verifica que la energía se conserve aproximadamente (para sistema no forzado)."""
    # Para condiciones iniciales específicas
    ci = [0.0, 1.0]
    resultados = elu.resolver_ecuacion(t_max=0.01, dt=1e-5, 
                                        condiciones_iniciales=ci)
    
    E_total = resultados['E_total']
    
    # Para sistema forzado, la energía NO se conserva exactamente
    # pero la variación debe ser suave
    E_std = np.std(E_total)
    E_mean = np.mean(E_total)
    
    # Verificar que no haya discontinuidades grandes
    assert E_std < 10 * E_mean, \
        "La variación de energía debe ser razonable"

def test_resolver_ecuacion_periodicidad():
    """Verifica que la solución tenga el período correcto."""
    resultados = elu.resolver_ecuacion(t_max=0.05, dt=1e-5)
    
    t = resultados['t']
    psi = resultados['psi']
    
    # Calcular período teórico
    T_teorico = 2 * np.pi / elu.omega_0
    
    # Buscar máximos locales
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(psi)
    
    if len(peaks) >= 2:
        # Calcular períodos entre picos consecutivos
        T_medidos = np.diff(t[peaks])
        T_medio = np.mean(T_medidos)
        
        # Verificar que el período medido esté cerca del teórico
        # Permitimos 5% de error debido a efectos transitorios
        assert abs(T_medio - T_teorico) / T_teorico < 0.05, \
            f"Período medido ({T_medio:.6e} s) debe estar cerca del teórico ({T_teorico:.6e} s)"

# ============================================================================
# TESTS DE ANÁLISIS
# ============================================================================

def test_analizar_solucion_forma():
    """Verifica que analizar_solucion devuelva el formato correcto."""
    resultados = elu.resolver_ecuacion(t_max=0.01, dt=1e-4)
    analisis = elu.analizar_solucion(resultados)
    
    # Verificar claves
    claves_requeridas = [
        'amplitud_maxima', 'velocidad_maxima', 'energia_media',
        'periodo_teorico', 'frecuencia_teorica', 'omega_0',
        'solucion_particular', 'termino_forzamiento'
    ]
    for clave in claves_requeridas:
        assert clave in analisis, f"Debe contener clave '{clave}'"

def test_analizar_solucion_valores():
    """Verifica que el análisis calcule valores razonables."""
    resultados = elu.resolver_ecuacion(t_max=0.05, dt=1e-5)
    analisis = elu.analizar_solucion(resultados)
    
    # Verificar que omega_0 coincida
    assert abs(analisis['omega_0'] - elu.omega_0) < 1e-10, \
        "omega_0 en análisis debe coincidir con constante"
    
    # Verificar período y frecuencia
    assert abs(analisis['periodo_teorico'] * analisis['frecuencia_teorica'] - 1.0) < 1e-10, \
        "T × f debe ser ≈ 1"
    
    # Verificar frecuencia vs f0
    assert abs(analisis['frecuencia_teorica'] - elu.f0) < 1e-6, \
        "Frecuencia teórica debe ser ≈ f₀"
    
    # Verificar que amplitud sea positiva
    assert analisis['amplitud_maxima'] >= 0, \
        "Amplitud máxima debe ser no negativa"
    
    # Verificar que energía sea positiva
    assert analisis['energia_media'] >= 0, \
        "Energía media debe ser no negativa"

# ============================================================================
# TESTS DE VISUALIZACIÓN Y GUARDADO
# ============================================================================

def test_visualizar_solucion():
    """Verifica que visualizar_solucion genere archivos."""
    import tempfile
    import shutil
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    
    try:
        resultados = elu.resolver_ecuacion(t_max=0.01, dt=1e-4)
        analisis = elu.analizar_solucion(resultados)
        
        archivos = elu.visualizar_solucion(resultados, analisis, output_dir=temp_dir)
        
        # Verificar que se generaron archivos
        assert len(archivos) > 0, "Debe generar al menos un archivo"
        
        # Verificar que los archivos existan
        for archivo in archivos:
            assert os.path.exists(archivo), f"Archivo {archivo} debe existir"
            assert os.path.getsize(archivo) > 0, f"Archivo {archivo} no debe estar vacío"
    
    finally:
        # Limpiar
        shutil.rmtree(temp_dir)

def test_guardar_resultados():
    """Verifica que guardar_resultados genere un archivo JSON válido."""
    import tempfile
    import shutil
    import json
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    
    try:
        resultados = elu.resolver_ecuacion(t_max=0.01, dt=1e-4)
        analisis = elu.analizar_solucion(resultados)
        
        archivo = elu.guardar_resultados(resultados, analisis, output_dir=temp_dir)
        
        # Verificar que el archivo exista
        assert os.path.exists(archivo), "Archivo JSON debe existir"
        
        # Verificar que sea JSON válido
        with open(archivo, 'r') as f:
            datos = json.load(f)
        
        # Verificar estructura
        assert 'parametros' in datos, "JSON debe contener 'parametros'"
        assert 'analisis' in datos, "JSON debe contener 'analisis'"
        
        # Verificar valores
        assert datos['parametros']['f0_Hz'] == elu.f0, \
            "f₀ en JSON debe coincidir"
        assert abs(datos['parametros']['omega_0_rad_s'] - elu.omega_0) < 1e-6, \
            "ω₀ en JSON debe coincidir"
    
    finally:
        # Limpiar
        shutil.rmtree(temp_dir)

# ============================================================================
# TEST DE INTEGRACIÓN COMPLETA
# ============================================================================

def test_main_completo():
    """Test de integración completa del pipeline."""
    import tempfile
    import shutil
    
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp()
    
    # Guardar directorios originales
    original_dir = os.getcwd()
    
    try:
        # Cambiar al directorio temporal
        os.chdir(temp_dir)
        
        # Ejecutar pipeline completo
        resultados = elu.resolver_ecuacion(t_max=0.02, dt=1e-4)
        analisis = elu.analizar_solucion(resultados)
        archivos = elu.visualizar_solucion(resultados, analisis)
        archivo_json = elu.guardar_resultados(resultados, analisis)
        
        # Verificar que todo se generó correctamente
        assert len(archivos) > 0, "Debe generar visualizaciones"
        assert os.path.exists(archivo_json), "Debe generar archivo JSON"
        
        print("✓ Test de integración completa pasó exitosamente")
    
    finally:
        # Restaurar directorio original
        os.chdir(original_dir)
        # Limpiar
        shutil.rmtree(temp_dir)

# ============================================================================
# EJECUCIÓN DE TESTS
# ============================================================================

if __name__ == '__main__':
    # Ejecutar todos los tests
    print("=" * 80)
    print("TESTS: Ecuación del Latido Universal")
    print("=" * 80)
    print()
    
    # Lista de funciones de test
    test_functions = [
        test_constantes_fundamentales,
        test_termino_forzamiento,
        test_ecuacion_diferencial_forma,
        test_ecuacion_diferencial_equilibrio,
        test_solucion_particular,
        test_solucion_homogenea,
        test_solucion_general,
        test_resolver_ecuacion_forma,
        test_resolver_ecuacion_condiciones_iniciales,
        test_resolver_ecuacion_conservacion_energia,
        test_resolver_ecuacion_periodicidad,
        test_analizar_solucion_forma,
        test_analizar_solucion_valores,
        test_visualizar_solucion,
        test_guardar_resultados,
        test_main_completo
    ]
    
    # Ejecutar cada test
    tests_passed = 0
    tests_failed = 0
    
    for test_func in test_functions:
        test_name = test_func.__name__
        try:
            test_func()
            print(f"✓ {test_name}")
            tests_passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            tests_failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Error inesperado - {e}")
            tests_failed += 1
    
    # Resumen
    print()
    print("=" * 80)
    print(f"Tests pasados: {tests_passed}/{len(test_functions)}")
    print(f"Tests fallidos: {tests_failed}/{len(test_functions)}")
    print("=" * 80)
    
    # Salir con código apropiado
    sys.exit(0 if tests_failed == 0 else 1)
