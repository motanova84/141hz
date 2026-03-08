#!/usr/bin/env python3
"""
Validación del Nodo QCAL Pragmático

Este script valida el funcionamiento del NodoQCAL, verificando:
1. Inicialización correcta con f₀ = 141.7001 Hz
2. Registro de experiencias y cálculo de impacto
3. Resonancia con frecuencias externas
4. Transformación de incertidumbre
5. Activación del modo abrazo y constante C = 244.360433 Hz

Author: José Manuel Mota Burruezo
Institution: Instituto Consciencia Cuántica QCAL ∞³
"""

import sys
import math
from pathlib import Path
from unittest.mock import patch

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.nodo_qcal import NodoQCAL

# QCAL constants
F0 = 141.7001       # Hz - La frecuencia del amor
CONSTANTE_C = 244.360433  # Hz - La constante C

results = {}


def create_nodo(nombre: str = "Validador") -> NodoQCAL:
    """Create a NodoQCAL with suppressed output."""
    with patch("time.sleep"):
        with patch("builtins.print"):
            return NodoQCAL(nombre)


def check_1_inicializacion():
    """Verifica que el nodo se inicializa con los parámetros correctos."""
    nodo = create_nodo()
    assert abs(nodo.frecuencia_base - F0) < 1e-4, f"f₀ esperado: {F0}, obtenido: {nodo.frecuencia_base}"
    assert nodo.campo_amor == 0.0, "campo_amor debe iniciar en 0"
    assert nodo.transformaciones == 0, "transformaciones debe iniciar en 0"
    assert len(nodo.experiencias) == 0, "experiencias debe iniciar vacía"
    assert nodo.estado_actual == "despierto", "estado_actual debe ser 'despierto'"
    print("✅ Check 1: Inicialización correcta con f₀ = 141.7001 Hz")
    return True


def check_2_experimentar():
    """Verifica el registro de experiencias y cálculo de impacto."""
    nodo = create_nodo()
    with patch("builtins.print"):
        resultado = nodo.experimentar("amor crear compartir")
    assert "accion" in resultado
    assert "impacto_practico" in resultado
    assert "frecuencia_resultante" in resultado
    assert "variacion_Hz" in resultado
    assert "timestamp" in resultado
    assert "aprendizaje" in resultado
    assert len(nodo.experiencias) == 1
    assert resultado["impacto_practico"] > 0
    print("✅ Check 2: Registro de experiencias y cálculo de impacto correcto")
    return True


def check_3_impacto_palabras_poder():
    """Verifica que las palabras de poder aumentan el impacto."""
    nodo = create_nodo()
    # Average multiple runs to reduce randomness
    base_impacts = [nodo._calcular_impacto_pragmatico("xyz xyz xyz") for _ in range(50)]
    power_impacts = [nodo._calcular_impacto_pragmatico("amor amor amor") for _ in range(50)]
    avg_base = sum(base_impacts) / len(base_impacts)
    avg_power = sum(power_impacts) / len(power_impacts)
    assert avg_power > avg_base, f"Impacto con palabras de poder ({avg_power:.3f}) debe ser mayor que sin ellas ({avg_base:.3f})"
    print(f"✅ Check 3: Palabras de poder aumentan impacto ({avg_base:.3f} → {avg_power:.3f})")
    return True


def check_4_aprendizaje_thresholds():
    """Verifica los umbrales de aprendizaje."""
    nodo = create_nodo()
    high = nodo._extraer_aprendizaje("action", 0.6)
    medium = nodo._extraer_aprendizaje("action", 0.3)
    low = nodo._extraer_aprendizaje("action", 0.1)
    assert "vida" in high, f"Impacto alto debe mencionar 'vida': {high}"
    assert "potencial" in medium, f"Impacto medio debe mencionar 'potencial': {medium}"
    assert "enfoque" in low, f"Impacto bajo debe mencionar 'enfoque': {low}"
    print("✅ Check 4: Umbrales de aprendizaje correctos (alto/medio/bajo)")
    return True


def check_5_resonancia_frecuencia():
    """Verifica el cálculo de resonancia con frecuencias externas."""
    nodo = create_nodo()
    freq_base = nodo.frecuencia_base
    freq_externa = 200.0
    expected_freq = freq_base * 0.7 + freq_externa * 0.3

    with patch("builtins.print"):
        nueva_freq, mensaje = nodo.resonar_con_otros(freq_externa)

    assert abs(nueva_freq - expected_freq) < 1e-6, f"Frecuencia esperada: {expected_freq}, obtenida: {nueva_freq}"
    assert abs(nodo.frecuencia_base - expected_freq) < 1e-6, "frecuencia_base debe actualizarse"
    print(f"✅ Check 5: Resonancia correcta ({freq_base:.4f} + {freq_externa:.1f} → {nueva_freq:.4f} Hz)")
    return True


def check_6_resonancia_profunda():
    """Verifica la resonancia profunda con frecuencia idéntica."""
    nodo = create_nodo()
    freq_base = nodo.frecuencia_base
    campo_inicial = nodo.campo_amor

    with patch("builtins.print"):
        _, mensaje = nodo.resonar_con_otros(freq_base)

    # Same frequency → factor_resonancia = 1.0 > 0.8 → deep resonance
    assert "profunda" in mensaje, f"Con frecuencia idéntica debe haber resonancia profunda: {mensaje}"
    assert nodo.campo_amor > campo_inicial, "campo_amor debe aumentar con resonancia profunda"
    print(f"✅ Check 6: Resonancia profunda detectada con f₀ = {freq_base:.4f} Hz")
    return True


def check_7_transformar_incertidumbre():
    """Verifica la transformación de incertidumbre."""
    nodo = create_nodo()
    campo_inicial = nodo.campo_amor
    valid_responses = [
        "Esta duda es válida. Usémosla como combustible para experimentar.",
        "La incertidumbre es el campo donde nacen las posibilidades.",
        "No necesitas certeza absoluta. Solo el siguiente paso con amor.",
        "La duda revela dónde necesitas más experiencia. Ve y prueba.",
        "Transforma esta pregunta en acción. La respuesta vendrá caminando."
    ]
    with patch("builtins.print"):
        respuesta = nodo.transformar_incertidumbre("¿Qué es la consciencia?")
    assert respuesta in valid_responses, f"Respuesta no reconocida: {respuesta}"
    assert abs(nodo.campo_amor - (campo_inicial + 0.2)) < 1e-10, f"campo_amor debe aumentar 0.2: {nodo.campo_amor}"
    print("✅ Check 7: Transformación de incertidumbre correcta (+0.2 campo_amor)")
    return True


def check_8_modo_abrazo_sin_regalo():
    """Verifica el modo abrazo sin regalo (campo_amor <= 5)."""
    nodo = create_nodo()
    nodo.campo_amor = 2.0
    freq_antes = nodo.frecuencia_base
    with patch("time.sleep"):
        with patch("builtins.print"):
            nodo.activar_modo_abrazo()
    assert abs(nodo.frecuencia_base - freq_antes) < 1e-6, "Sin regalo, frecuencia_base no debe cambiar"
    print("✅ Check 8: Modo abrazo sin regalo (frecuencia sin cambios con campo_amor ≤ 5)")
    return True


def check_9_modo_abrazo_con_regalo():
    """Verifica el modo abrazo con regalo (campo_amor > 5 → constante C)."""
    nodo = create_nodo()
    nodo.campo_amor = 6.0
    with patch("time.sleep"):
        with patch("builtins.print"):
            nodo.activar_modo_abrazo()
    assert abs(nodo.frecuencia_base - CONSTANTE_C) < 1e-4, \
        f"Con regalo, frecuencia_base debe ser la constante C = {CONSTANTE_C}: {nodo.frecuencia_base}"
    print(f"✅ Check 9: Constante C = {CONSTANTE_C} Hz asignada correctamente con campo_amor > 5")
    return True


def check_10_multiple_experiencias():
    """Verifica la acumulación de múltiples experiencias."""
    nodo = create_nodo()
    acciones = ["crear un puente", "compartir conocimiento", "abrazar la incertidumbre"]
    with patch("builtins.print"):
        for accion in acciones:
            nodo.experimentar(accion)
    assert len(nodo.experiencias) == 3, f"Deben haber 3 experiencias: {len(nodo.experiencias)}"
    assert nodo.campo_amor > 0, "campo_amor debe ser positivo tras varias experiencias"
    print(f"✅ Check 10: {len(nodo.experiencias)} experiencias acumuladas, campo_amor = {nodo.campo_amor:.2f}")
    return True


def run_all_checks():
    """Execute all validation checks."""
    print("=" * 60)
    print("VALIDACIÓN DEL NODO QCAL PRAGMÁTICO")
    print(f"f₀ = {F0} Hz | Constante C = {CONSTANTE_C} Hz")
    print("=" * 60)
    print()

    checks = [
        ("Inicialización", check_1_inicializacion),
        ("Experimentar", check_2_experimentar),
        ("Palabras de poder", check_3_impacto_palabras_poder),
        ("Umbrales aprendizaje", check_4_aprendizaje_thresholds),
        ("Resonancia frecuencia", check_5_resonancia_frecuencia),
        ("Resonancia profunda", check_6_resonancia_profunda),
        ("Transformar incertidumbre", check_7_transformar_incertidumbre),
        ("Modo abrazo sin regalo", check_8_modo_abrazo_sin_regalo),
        ("Modo abrazo con regalo", check_9_modo_abrazo_con_regalo),
        ("Múltiples experiencias", check_10_multiple_experiencias),
    ]

    passed = 0
    failed = 0
    for name, check_fn in checks:
        try:
            check_fn()
            results[name] = "PASSED"
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: FAILED - {e}")
            results[name] = f"FAILED: {e}"
            failed += 1
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
            results[name] = f"ERROR: {e}"
            failed += 1

    print()
    print("=" * 60)
    print(f"RESULTADO: {passed}/{passed + failed} checks pasaron")
    if failed == 0:
        print("✅ VALIDACIÓN COMPLETA - Nodo QCAL Pragmático funcional")
    else:
        print(f"⚠️  {failed} check(s) fallaron")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
