#!/usr/bin/env python3
"""
Tests para el script de validación del radio cuántico RΨ

Este script verifica que la validación numérica del radio cuántico
funciona correctamente y produce resultados consistentes.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import os
import sys
import numpy as np
from pathlib import Path

# Constantes fundamentales (CODATA 2022)
c = 2.99792458e8    # m/s (velocidad de la luz)
l_p = 1.616255e-35  # m (longitud de Planck)
f0 = 141.7001       # Hz (frecuencia fundamental)

# Get repository root dynamically
REPO_ROOT = Path(__file__).parent.parent.resolve()


def get_repo_root():
    """
    Obtiene el directorio raíz del repositorio de forma dinámica.
    
    Busca el directorio raíz navegando hacia arriba desde la ubicación del script
    hasta encontrar el directorio padre de 'scripts' o un marcador como '.git'.
    
    strategy:
        1. Si el script está en un directorio llamado 'scripts', usa su padre como raíz
        2. Si no, busca un directorio '.git' navegando hacia arriba (hasta 5 niveles)
        3. Como fallback, asume que el script está un nivel debajo de la raíz
    
    Retorna:
        str: Ruta absoluta al directorio raíz del repositorio
    
    Nota:
        El método de fallback asume que el script está en el primer nivel de subdirectorios.
        Esto es apropiado para la estructura actual del repositorio donde los tests
        están en 'scripts/'.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Verificar que estamos en el directorio 'scripts'
    if os.path.basename(script_dir) == 'scripts':
        repo_root = os.path.dirname(script_dir)
        return repo_root
    
    # Si no estamos en scripts/, buscar hacia arriba por el directorio .git
    current_dir = script_dir
    for _ in range(5):  # Limitar búsqueda a 5 niveles
        if os.path.exists(os.path.join(current_dir, '.git')):
            return current_dir
        parent = os.path.dirname(current_dir)
        if parent == current_dir:  # Llegamos a la raíz del sistema
            break
        current_dir = parent
    
    # Fallback: asumir que estamos un nivel debajo de la raíz
    # Esto funciona para la estructura estándar del repositorio (scripts/)
    return os.path.dirname(script_dir)


class TestValidacionRadioCuantico:
    """Tests para la validación del radio cuántico"""
    
    def test_calculo_basico_r_psi(self):
        """
        Test: Cálculo básico de RΨ = c/(2πf₀·ℓ_p)
        """
        R_psi = c / (2 * np.pi * f0 * l_p)
        
        # Verificar orden de magnitud (debe ser ~10^40)
        assert 1e40 < R_psi < 1e41, \
            f"RΨ debe estar en el rango 10^40, obtenido: {R_psi:.3e}"
        
        # Verificar valor específico con tolerancia del 1%
        expected = 2.083343e40
        rel_error = abs(R_psi - expected) / expected
        assert rel_error < 0.01, \
            f"RΨ = {R_psi:.6e}, esperado ≈ {expected:.6e}, error: {rel_error:.2%}"
    
    def test_verificacion_inversa(self):
        """
        Test: Verificación inversa f₀ = c/(2π·RΨ·ℓ_p)
        """
        # Calcular RΨ
        R_psi = c / (2 * np.pi * f0 * l_p)
        
        # Recuperar f₀
        f0_recovered = c / (2 * np.pi * R_psi * l_p)
        
        # Verificar que recuperamos f₀ con alta precisión
        rel_error = abs(f0_recovered - f0) / f0
        assert rel_error < 1e-10, \
            f"f₀ recuperada: {f0_recovered:.10f} Hz, " \
            f"f₀ original: {f0} Hz, error: {rel_error:.2e}"
    
    def test_consistencia_expresiones(self):
        """
        Test: Verificar que diferentes expresiones de RΨ son equivalentes
        """
        # Expresión 1: RΨ = c/(2πf₀·ℓ_p)
        R_psi_expr1 = c / (2 * np.pi * f0 * l_p)
        
        # Expresión 2: RΨ = (c/ℓ_p)/(2πf₀)
        R_psi_expr2 = (c / l_p) / (2 * np.pi * f0)
        
        # Verificar equivalencia
        rel_diff = abs(R_psi_expr1 - R_psi_expr2) / R_psi_expr1
        assert rel_diff < 1e-14, \
            f"Las expresiones no son equivalentes: diferencia {rel_diff:.2e}"
    
    def test_jerarquia_escalas(self):
        """
        Test: Verificar que RΨ·ℓ_p está en el rango correcto de escalas
        """
        R_psi = c / (2 * np.pi * f0 * l_p)
        R_psi_meters = R_psi * l_p
        
        # RΨ·ℓ_p debe ser ~10^5 metros
        assert 1e5 < R_psi_meters < 1e6, \
            f"RΨ·ℓ_p debe estar en el rango ~10^5 m, obtenido: {R_psi_meters:.3e} m"
        
        # Verificar relación con longitud de onda gravitacional
        lambda_gw = c / f0
        ratio = lambda_gw / R_psi_meters
        
        # El ratio debe ser ~2π (orden de magnitud)
        assert 5 < ratio < 10, \
            f"λ_GW/(RΨ·ℓ_p) debe ser ~2π, obtenido: {ratio:.2f}"
    
    def test_orden_magnitud_correcto(self):
        """
        Test: Verificar que el orden de magnitud es 10^40, no 10^47
        """
        R_psi = c / (2 * np.pi * f0 * l_p)
        
        order_of_magnitude = int(np.floor(np.log10(R_psi)))
        
        assert order_of_magnitude == 40, \
            f"Orden de magnitud debe ser 40, obtenido: {order_of_magnitude}"
    
    def test_sensibilidad_constantes(self):
        """
        Test: Verificar que RΨ tiene la sensibilidad correcta a las constantes
        """
        R_psi_ref = c / (2 * np.pi * f0 * l_p)
        
        # Perturbar c (aumentar 1%)
        c_pert = c * 1.01
        R_psi_c = c_pert / (2 * np.pi * f0 * l_p)
        sens_c = (R_psi_c - R_psi_ref) / R_psi_ref / 0.01
        
        # RΨ ∝ c, entonces sensibilidad debe ser ~1
        assert 0.99 < sens_c < 1.01, \
            f"Sensibilidad a c debe ser ~1, obtenido: {sens_c:.4f}"
        
        # Perturbar ℓ_p (aumentar 1%)
        l_p_pert = l_p * 1.01
        R_psi_lp = c / (2 * np.pi * f0 * l_p_pert)
        sens_lp = (R_psi_lp - R_psi_ref) / R_psi_ref / 0.01
        
        # RΨ ∝ 1/ℓ_p, entonces sensibilidad debe ser ~-1
        assert -1.01 < sens_lp < -0.99, \
            f"Sensibilidad a ℓ_p debe ser ~-1, obtenido: {sens_lp:.4f}"
        
        # Perturbar f₀ (aumentar 1%)
        f0_pert = f0 * 1.01
        R_psi_f0 = c / (2 * np.pi * f0_pert * l_p)
        sens_f0 = (R_psi_f0 - R_psi_ref) / R_psi_ref / 0.01
        
        # RΨ ∝ 1/f₀, entonces sensibilidad debe ser ~-1
        assert -1.01 < sens_f0 < -0.99, \
            f"Sensibilidad a f₀ debe ser ~-1, obtenido: {sens_f0:.4f}"
    
    def test_archivo_resultados_existe(self):
        """
        Test: Verificar que el archivo de resultados JSON se crea
        """
        # Ejecutar el script
        import subprocess
        
        # Obtener el directorio raíz del repositorio
        repo_root = get_repo_root()
        
        result = subprocess.run(
            ['python3', 'scripts/validacion_radio_cuantico.py'],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Verificar que terminó sin errores
        assert result.returncode == 0, \
            f"El script debe ejecutarse sin errores. stderr: {result.stderr}"
        
        # Verificar que se creó el archivo JSON (usando ruta absoluta desde repo_root)
        json_file = os.path.join(repo_root, 'results/validacion_radio_cuantico.json')
        assert os.path.exists(json_file), \
            f"El archivo {json_file} debe existir después de ejecutar el script"
        
        # Verificar que se creó la figura
        fig_file = os.path.join(repo_root, 'results/figures/validacion_radio_cuantico.png')
        assert os.path.exists(fig_file), \
            f"El archivo {fig_file} debe existir después de ejecutar el script"
    
    def test_validacion_json_contenido(self):
        """
        Test: Verificar que el JSON contiene los datos correctos
        """
        import json
        
        # Obtener el directorio raíz del repositorio
        repo_root = get_repo_root()
        
        # Ejecutar el script primero si el archivo no existe
        json_file = os.path.join(repo_root, 'results/validacion_radio_cuantico.json')
        if not os.path.exists(json_file):
            import subprocess
            subprocess.run(
                ['python3', 'scripts/validacion_radio_cuantico.py'],
                cwd=str(REPO_ROOT),
                timeout=60
            )
        
        # Leer el JSON
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Verificar campos principales
        assert 'resultado_principal' in data, "JSON debe contener 'resultado_principal'"
        assert 'constantes' in data, "JSON debe contener 'constantes'"
        assert 'verificacion' in data, "JSON debe contener 'verificacion'"
        
        # Verificar valores
        R_psi = data['resultado_principal']['R_psi_unidades_planck']
        assert 2.0e40 < R_psi < 2.1e40, \
            f"RΨ en JSON debe estar en rango correcto, obtenido: {R_psi:.3e}"
        
        # Verificar que la verificación es consistente
        assert data['verificacion']['consistente'] == True, \
            "La verificación debe marcar como consistente"


def run_tests():
    """Ejecutar todos los tests"""
    print("=" * 80)
    print("EJECUTANDO TESTS DE VALIDACIÓN DEL RADIO CUÁNTICO")
    print("=" * 80)
    print()
    
    # Cambiar al directorio correcto (repository root)
    os.chdir(str(REPO_ROOT))
    
    # Ejecutar tests manualmente
    test_suite = TestValidacionRadioCuantico()
    test_methods = [
        test_suite.test_calculo_basico_r_psi,
        test_suite.test_verificacion_inversa,
        test_suite.test_consistencia_expresiones,
        test_suite.test_jerarquia_escalas,
        test_suite.test_orden_magnitud_correcto,
        test_suite.test_sensibilidad_constantes,
        test_suite.test_archivo_resultados_existe,
        test_suite.test_validacion_json_contenido,
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_method()
            passed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__} FAILED: {e}")
            failed += 1
    
    print()
    print("=" * 80)
    print(f"RESULTADOS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(run_tests())
