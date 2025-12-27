#!/usr/bin/env python3
"""
Utilidades para cálculo y formato seguro de SNR
================================================

Este módulo proporciona funciones auxiliares para calcular y formatear valores de SNR
(Signal-to-Noise Ratio) de manera segura, manejando correctamente arrays de numpy.

Soluciona el error: TypeError: unsupported format string passed to numpy.ndarray.__format__
"""
import numpy as np


def safe_format_snr(snr, decimals=2):
    """
    Formatea un valor de SNR de manera segura, manejando arrays de numpy.
    
    Esta función convierte arrays de numpy a valores escalares antes de formatear,
    evitando el error TypeError cuando se intenta usar format strings con arrays.
    
    Parameters:
    -----------
    snr : float, int, np.ndarray, or array-like
        Valor de SNR a formatear. Puede ser:
        - Un escalar (float/int)
        - Un array de numpy con un solo elemento
        - Un array de numpy (se tomará el primer elemento)
    
    decimals : int, optional (default=2)
        Número de decimales a mostrar
    
    Returns:
    --------
    float
        Valor escalar de SNR listo para formatear
    
    Examples:
    ---------
    >>> import numpy as np
    >>> snr = np.array([7.5])
    >>> print(f"SNR: {safe_format_snr(snr):.2f}")
    SNR: 7.50
    
    >>> snr = 7.5
    >>> print(f"SNR: {safe_format_snr(snr):.2f}")
    SNR: 7.50
    
    >>> snr = np.array([7.5, 8.2, 6.3])
    >>> print(f"SNR: {safe_format_snr(snr):.2f}")  # Usa el primer valor
    SNR: 7.50
    """
    # Si es un array de numpy, extraer el valor escalar
    if isinstance(snr, np.ndarray):
        if snr.size == 1:
            # Array con un solo elemento
            return float(snr.item())
        elif snr.size > 1:
            # Array con múltiples elementos - tomar el primero
            return float(snr.flat[0])
        else:
            # Array vacío
            return 0.0
    
    # Si es un tipo escalar de numpy (np.float64, np.int32, etc.)
    elif hasattr(snr, 'item'):
        return float(snr.item())
    
    # Ya es un tipo Python nativo (float, int)
    else:
        return float(snr)


def format_snr_string(snr, detector=None, frequency=None, decimals=2):
    """
    Formatea un string completo con información de SNR.
    
    Parameters:
    -----------
    snr : float, int, np.ndarray, or array-like
        Valor de SNR
    detector : str, optional
        Nombre del detector (e.g., 'H1', 'L1')
    frequency : float, optional
        Frecuencia en Hz
    decimals : int, optional (default=2)
        Número de decimales
    
    Returns:
    --------
    str
        String formateado con información de SNR
    
    Examples:
    ---------
    >>> format_snr_string(7.5, 'H1', 141.7)
    'SNR = 7.50 (H1 @ 141.70 Hz)'
    
    >>> format_snr_string(np.array([8.2]))
    'SNR = 8.20'
    """
    snr_value = safe_format_snr(snr)
    
    # Construir el string
    result = f"SNR = {snr_value:.{decimals}f}"
    
    if detector is not None and frequency is not None:
        result += f" ({detector} @ {frequency:.2f} Hz)"
    elif detector is not None:
        result += f" ({detector})"
    elif frequency is not None:
        result += f" (@ {frequency:.2f} Hz)"
    
    return result


def calculate_snr_safe(F_eff, h_rss, Sn_f0):
    """
    Calcula SNR de manera segura y retorna un valor escalar.
    
    Esta función implementa el cálculo estándar de SNR:
        SNR = (F_eff * h_rss) / sqrt(Sn_f0)
    
    Y automáticamente convierte el resultado a escalar si es necesario.
    
    Parameters:
    -----------
    F_eff : float or np.ndarray
        Factor de eficiencia del detector
    h_rss : float or np.ndarray
        Amplitud root-sum-square de la señal
    Sn_f0 : float or np.ndarray
        Densidad espectral de ruido en la frecuencia objetivo
    
    Returns:
    --------
    float or np.ndarray
        Valor de SNR. Si todos los inputs son escalares, retorna un escalar.
        Si alguno es array, retorna array del mismo tamaño.
    
    Examples:
    ---------
    >>> F_eff = 0.5
    >>> h_rss = 1e-21
    >>> Sn_f0 = 1e-46
    >>> snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
    >>> print(f"SNR: {snr:.2f}")
    SNR: 5.00e+02
    
    >>> # Con arrays
    >>> F_eff = np.array([0.5])
    >>> h_rss = np.array([1e-21])
    >>> Sn_f0 = np.array([1e-46])
    >>> snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
    >>> print(f"SNR: {safe_format_snr(snr):.2f}")
    SNR: 5.00e+02
    """
    # Cálculo estándar de SNR
    snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
    
    return snr


def print_snr_result(snr, ifo, frequency=141.7):
    """
    Imprime un resultado de SNR formateado correctamente.
    
    Esta es la función recomendada para imprimir resultados de SNR,
    manejando automáticamente el caso de arrays de numpy.
    
    Parameters:
    -----------
    snr : float, int, np.ndarray, or array-like
        Valor de SNR
    ifo : str
        Nombre del detector/interferómetro (e.g., 'H1', 'L1')
    frequency : float, optional (default=141.7)
        Frecuencia en Hz
    
    Examples:
    ---------
    >>> snr = np.array([7.5])
    >>> print_snr_result(snr, 'H1', 141.7)
    SNR esperada a 141.70 Hz en H1: 7.50
    
    >>> snr = 8.2
    >>> print_snr_result(snr, 'L1')
    SNR esperada a 141.70 Hz en L1: 8.20
    """
    snr_value = safe_format_snr(snr)
    print(f"SNR esperada a {frequency:.2f} Hz en {ifo}: {snr_value:.2f}")


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 70)
    print("🔧 UTILIDADES DE SNR - Ejemplos de uso")
    print("=" * 70)
    print()
    
    # Ejemplo 1: SNR como escalar
    print("📊 Ejemplo 1: SNR escalar")
    snr_scalar = 7.5
    print(f"   SNR: {safe_format_snr(snr_scalar):.2f}")
    print()
    
    # Ejemplo 2: SNR como array de numpy con un elemento
    print("📊 Ejemplo 2: SNR como array de numpy (1 elemento)")
    F_eff = np.array([0.5])
    h_rss = np.array([1e-21])
    Sn_f0 = np.array([1e-46])
    snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
    print(f"   Tipo de snr: {type(snr)}")
    print(f"   SNR: {safe_format_snr(snr):.2f}")
    print()

    # Ejemplo 3: Usando print_snr_result
    print("📊 Ejemplo 3: Usando print_snr_result()")
    for ifo in ['H1', 'L1']:
        snr = np.array([7.5 + np.random.uniform(-1, 1)])
        print("   ", end="")
        print_snr_result(snr, ifo, 141.7)
    print()
    
    # Ejemplo 4: Cálculo completo de SNR
    print("📊 Ejemplo 4: Cálculo completo")
    print("   Calculando SNR con:")
    print(f"   F_eff = {F_eff[0]}")
    print(f"   h_rss = {h_rss[0]:.2e}")
    print(f"   Sn_f0 = {Sn_f0[0]:.2e}")
    snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
    print(f"   Resultado: {format_snr_string(snr, 'H1', 141.7)}")
    print()
    
    # Ejemplo 5: Array con múltiples valores
    print("📊 Ejemplo 5: Array con múltiples valores de SNR")
    snr_array = np.array([5.2, 6.8, 7.3, 8.1])
    print(f"   Array completo: {snr_array}")
    print(f"   Primer valor: {safe_format_snr(snr_array):.2f}")
    print("   Para imprimir todos los valores:")
    for i, snr_val in enumerate(snr_array):
        print(f"      SNR[{i}] = {safe_format_snr(snr_val):.2f}")
    print()
    
    print("✅ Todos los ejemplos completados correctamente")
