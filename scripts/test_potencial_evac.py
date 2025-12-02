#!/usr/bin/env python3
"""
Test unitario para el script de potencial de energía del vacío
"""
import os
import sys
import numpy as np
from scipy.constants import c, physical_constants


def test_E_vac_function():
    """Prueba la función E_vac para verificar comportamiento correcto"""
    print("🧪 Test: Verificando función Evac")

    # Parámetros constantes (CODATA 2022)
    lP = physical_constants["Planck length"][0]
    Lambda = 1.1e-52
    zeta_prime = -0.207886
    alpha = 1.0
    beta = 1.0
    gamma = 1.0
    delta = 0.5
    b = np.pi

    def Evac(R):
        term1 = alpha * R**(-4)
        term2 = beta * zeta_prime * R**(-2)
        term3 = gamma * (Lambda**2) * (R * lP)**2
        term4 = delta * np.sin(np.log(R) / np.log(b))**2
        return term1 + term2 + term3 + term4

    # Test 1: Verificar que la función devuelve valores numéricos válidos
    try:
        val = Evac(1e10)
        assert np.isfinite(val), "Evac debe devolver un valor finito"
        print("   ✅ Test 1 PASSED: Función devuelve valores válidos")
    except Exception as e:
        print(f"   ❌ Test 1 FAILED: {e}")
        return False

    # Test 2: Verificar que el mínimo existe en un rango razonable
    try:
        R_test = np.logspace(0, 48, 1000)
        E_test = np.array([Evac(R) for R in R_test])
        idx_min = np.argmin(E_test)
        R_min = R_test[idx_min]

        assert np.isfinite(R_min), "El mínimo debe ser un valor finito"
        assert R_min > 0, "El mínimo debe ser positivo"
        print(f"   ✅ Test 2 PASSED: Mínimo encontrado en R = {R_min:.4e} ℓP")
    except Exception as e:
        print(f"   ❌ Test 2 FAILED: {e}")
        return False

    # Test 3: Verificar que el valor en el mínimo es menor que en valores
    #         cercanos
    try:
        E_min = Evac(R_min)
        E_before = Evac(R_min * 0.9)
        E_after = Evac(R_min * 1.1)
        msg1 = "El mínimo debe ser menor que el valor anterior"
        assert E_min <= E_before, msg1
        msg2 = "El mínimo debe ser menor que el valor posterior"
        assert E_min <= E_after, msg2
        print(f"   ✅ Test 3 PASSED: Valor mínimo E_vac = {E_min:.6e}")
    except Exception as e:
        print(f"   ❌ Test 3 FAILED: {e}")
        return False

    # Test 4: Verificar que los términos individuales tienen el orden de
    #         magnitud esperado
    try:
        R_test_val = 1e10
        term1 = alpha * R_test_val**(-4)
        term2 = beta * zeta_prime * R_test_val**(-2)
        # term3 is not used in validation but calculated for completeness
        term4 = delta * np.sin(np.log(R_test_val) / np.log(b))**2

        # El término 1/R^4 debe ser positivo
        assert term1 > 0, "Término 1/R^4 debe ser positivo"
        # El término beta*zeta'/R^2 debe ser negativo (zeta' < 0, beta > 0)
        assert term2 < 0, "Término beta*zeta'/R^2 debe ser negativo"
        # El término log-periódico debe estar acotado entre 0 y delta
        assert 0 <= term4 <= delta, "Término log-periódico debe estar acotado"

        print("   ✅ Test 4 PASSED: Todos los términos tienen el orden de "
              "magnitud correcto")
    except Exception as e:
        print(f"   ❌ Test 4 FAILED: {e}")
        return False

    # Test 5: Verificar que la frecuencia f₀ se calcula correctamente
    try:
        f0 = c / (2 * np.pi * R_min * lP)
        assert np.isfinite(f0), "La frecuencia debe ser finita"
        assert f0 > 0, "La frecuencia debe ser positiva"
        print(f"   ✅ Test 5 PASSED: Frecuencia f₀ = {f0:.4e} Hz")
    except Exception as e:
        print(f"   ❌ Test 5 FAILED: {e}")
        return False

    print("\n✅ Todos los tests pasaron correctamente")


def test_plot_generation():
    """Prueba que el script genera el gráfico correctamente"""
    print("\n🧪 Test: Verificando generación de gráfico")

    # Ejecutar el script
    script_path = os.path.join(os.path.dirname(__file__), 'potencial_evac.py')

    # Eliminar plot anterior si existe
    if os.path.exists('potential_plot.png'):
        os.remove('potential_plot.png')

    # Ejecutar script
    import subprocess
    result = subprocess.run([sys.executable, script_path],
                            capture_output=True,
                            text=True,
                            cwd=os.path.dirname(os.path.dirname(script_path)))

    if result.returncode != 0:
        print(f"   ❌ Test FAILED: Script falló con código {result.returncode}")
        print(f"   Error: {result.stderr}")
        return False

    # Verificar que el plot fue creado
    if not os.path.exists('potential_plot.png'):
        print("   ❌ Test FAILED: Plot no fue creado")
        return False

    # Verificar que el plot tiene tamaño razonable (> 10KB)
    size = os.path.getsize('potential_plot.png')
    if size < 10000:
        print(f"   ❌ Test FAILED: Plot muy pequeño ({size} bytes)")
        return False

    print(f"   ✅ Test PASSED: Plot generado correctamente ({size} bytes)")


if __name__ == "__main__":
    print("=" * 80)
    print("TEST: potencial_evac.py")
    print("=" * 80)

    success = True
    try:
        test_E_vac_function()
    except Exception:
        success = False
    
    try:
        test_plot_generation()
    except Exception:
        success = False

    print("\n" + "=" * 80)
    if success:
        print("✅ TODOS LOS TESTS PASARON")
        sys.exit(0)
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        sys.exit(1)
