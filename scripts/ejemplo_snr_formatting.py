#!/usr/bin/env python3
"""
Ejemplo: Corrección del error TypeError en formateo de SNR
============================================================

Este script demuestra el error común que ocurre al intentar formatear
valores de SNR que son arrays de numpy, y muestra la solución correcta.

Error original:
    TypeError: unsupported format string passed to numpy.ndarray.__format__

Ocurre cuando se intenta:
    snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
    print(f"SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}")
"""
import numpy as np
import sys
import os

# Ajustar path antes de importar (necesario para imports locales)
sys.path.insert(0, os.path.dirname(__file__))

# Importar utilidades de SNR
from snr_utils import safe_format_snr, print_snr_result, calculate_snr_safe  # noqa: E402


def ejemplo_problema_original():
    """
    Reproduce el problema original del TypeError
    """
    print("=" * 70)
    print("❌ PROBLEMA: Intento de formatear array de numpy directamente")
    print("=" * 70)
    print()
    
    # Parámetros típicos de análisis gravitacional
    F_eff = np.array([0.5])      # Factor de eficiencia del detector
    h_rss = np.array([1e-21])    # Amplitud RMS de la señal
    Sn_f0 = np.array([1e-46])    # Densidad espectral de ruido
    ifo = "H1"                    # Detector (Hanford)
    
    # Cálculo SNR estándar
    snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
    
    print(f"Tipo de snr: {type(snr)}")
    print(f"Valor de snr: {snr}")
    print(f"Shape de snr: {snr.shape}")
    print()
    
    # Intentar imprimir con formato (esto causaría TypeError)
    print("Intentando: print(f'SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}')")
    print()
    
    try:
        # Esto causará TypeError
        resultado = f"SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}"
        print(resultado)
    except TypeError as e:
        print(f"⚠️  ERROR CAPTURADO: {e}")
        print(f"    Tipo: {type(e).__name__}")
        print()


def ejemplo_solucion_1():
    """
    Solución 1: Usar safe_format_snr
    """
    print("=" * 70)
    print("✅ SOLUCIÓN 1: Usar safe_format_snr()")
    print("=" * 70)
    print()
    
    # Mismos parámetros
    F_eff = np.array([0.5])
    h_rss = np.array([1e-21])
    Sn_f0 = np.array([1e-46])
    ifo = "H1"
    
    # Cálculo SNR
    snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
    
    # Convertir a escalar de forma segura
    snr_safe = safe_format_snr(snr)
    
    print(f"Tipo de snr original: {type(snr)}")
    print(f"Tipo de snr_safe: {type(snr_safe)}")
    print()
    
    # Ahora sí podemos formatear
    print(f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}")
    print()
    
    # Código completo:
    print("Código:")
    print("-------")
    print("from snr_utils import safe_format_snr")
    print("snr = (F_eff * h_rss) / np.sqrt(Sn_f0)")
    print("snr_safe = safe_format_snr(snr)")
    print("print(f'SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}')")
    print()


def ejemplo_solucion_2():
    """
    Solución 2: Usar print_snr_result
    """
    print("=" * 70)
    print("✅ SOLUCIÓN 2: Usar print_snr_result()")
    print("=" * 70)
    print()
    
    # Mismos parámetros
    F_eff = np.array([0.5])
    h_rss = np.array([1e-21])
    Sn_f0 = np.array([1e-46])
    ifo = "H1"
    
    # Cálculo SNR
    snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
    
    # Usar la función helper que maneja el formateo automáticamente
    print_snr_result(snr, ifo, 141.7)
    print()
    
    # Código completo:
    print("Código:")
    print("-------")
    print("from snr_utils import print_snr_result")
    print("snr = (F_eff * h_rss) / np.sqrt(Sn_f0)")
    print("print_snr_result(snr, ifo, 141.7)")
    print()


def ejemplo_solucion_3():
    """
    Solución 3: Usar calculate_snr_safe
    """
    print("=" * 70)
    print("✅ SOLUCIÓN 3: Usar calculate_snr_safe()")
    print("=" * 70)
    print()
    
    # Mismos parámetros
    F_eff = np.array([0.5])
    h_rss = np.array([1e-21])
    Sn_f0 = np.array([1e-46])
    ifo = "H1"
    
    # Usar la función segura para calcular SNR
    snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
    
    # Formatear con safe_format_snr
    snr_safe = safe_format_snr(snr)
    print(f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}")
    print()
    
    # Código completo:
    print("Código:")
    print("-------")
    print("from snr_utils import calculate_snr_safe, safe_format_snr")
    print("snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)")
    print("snr_safe = safe_format_snr(snr)")
    print("print(f'SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}')")
    print()


def ejemplo_multiples_detectores():
    """
    Ejemplo con múltiples detectores
    """
    print("=" * 70)
    print("📊 EJEMPLO: Análisis de múltiples detectores")
    print("=" * 70)
    print()
    
    # Parámetros para diferentes detectores
    detectores = {
        'H1': {'F_eff': 0.5, 'Sn_f0': 1e-46},
        'L1': {'F_eff': 0.45, 'Sn_f0': 1.2e-46},
        'V1': {'F_eff': 0.3, 'Sn_f0': 2e-46}
    }
    
    h_rss = 1e-21  # Amplitud de la señal (común)
    
    print("Análisis de SNR en 141.7 Hz para múltiples detectores:")
    print()
    
    for ifo, params in detectores.items():
        # Calcular SNR (estos son arrays de numpy típicamente)
        F_eff = np.array([params['F_eff']])
        Sn_f0 = np.array([params['Sn_f0']])
        
        snr = calculate_snr_safe(F_eff, np.array([h_rss]), Sn_f0)
        
        # Imprimir resultado usando print_snr_result
        print("  ", end="")
        print_snr_result(snr, ifo, 141.7)
    
    print()


def ejemplo_mejores_practicas():
    """
    Mejores prácticas para trabajar con SNR
    """
    print("=" * 70)
    print("📚 MEJORES PRÁCTICAS")
    print("=" * 70)
    print()
    
    print("1. ✅ Siempre usa safe_format_snr() antes de formatear:")
    print("   snr_safe = safe_format_snr(snr)")
    print("   print(f'SNR: {snr_safe:.2f}')")
    print()
    
    print("2. ✅ O usa print_snr_result() directamente:")
    print("   print_snr_result(snr, 'H1', 141.7)")
    print()
    
    print("3. ✅ Para cálculos, usa calculate_snr_safe():")
    print("   snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)")
    print()
    
    print("4. ❌ Evita formatear arrays directamente:")
    print("   # MALO: print(f'{snr:.2f}')  # TypeError si snr es array")
    print()
    
    print("5. ✅ Si tienes múltiples valores, itera sobre ellos:")
    print("   for i, s in enumerate(snr_array):")
    print("       print(f'SNR[{i}] = {safe_format_snr(s):.2f}')")
    print()


def main():
    """
    Ejecuta todos los ejemplos
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Ejemplo: Corrección del error TypeError en formateo de SNR  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Mostrar el problema
    ejemplo_problema_original()
    print()
    
    # Mostrar las soluciones
    ejemplo_solucion_1()
    ejemplo_solucion_2()
    ejemplo_solucion_3()
    
    # Ejemplo más complejo
    ejemplo_multiples_detectores()
    
    # Mejores prácticas
    ejemplo_mejores_practicas()
    
    print("=" * 70)
    print("✅ Todos los ejemplos completados exitosamente")
    print("=" * 70)
    print()
    print("📖 Para más información, consulta:")
    print("   - scripts/snr_utils.py")
    print("   - scripts/test_snr_utils.py")
    print()


if __name__ == "__main__":
    main()
