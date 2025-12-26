#!/usr/bin/env python3
"""
Ecuación del Latido Universal (Universal Heartbeat Equation)

Implementa la solución numérica y análisis de la ecuación diferencial:

    ∂²Ψ/∂t² + ω₀²Ψ = I·A²eff·ζ'(1/2)

donde:
    ω₀ = 2π(141.7001 Hz) = 890.377 rad/s
    ζ'(1/2) = derivada de la función zeta de Riemann en s=1/2
    I = intensidad del campo (parámetro)
    A_eff = área efectiva (parámetro)

Esta ecuación describe el latido universal del campo noético Ψ, una oscilación
forzada armónica con término de forzamiento derivado de la estructura adélica
del espacio de moduli.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Octubre 2025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.special import zeta as scipy_zeta
import os
import json

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Frecuencia fundamental (predicción falsable)
f0 = 141.7001  # Hz

# Frecuencia angular fundamental
omega_0 = 2 * np.pi * f0  # rad/s

# Derivada de zeta de Riemann en s=1/2 (valor numérico)
# ζ'(1/2) ≈ -3.92264...
zeta_prime_half = -3.92264396844532

# ============================================================================
# PARÁMETROS FÍSICOS
# ============================================================================

# Intensidad del campo (normalizada)
I = 1.0

# Área efectiva (normalizada)
A_eff = 1.0

# Término de forzamiento
F_drive = I * A_eff**2 * zeta_prime_half

# ============================================================================
# ECUACIÓN DIFERENCIAL
# ============================================================================

def ecuacion_latido_universal(t, y):
    """
    Sistema de ecuaciones diferenciales de primer orden equivalente a:
    
        ∂²Ψ/∂t² + ω₀²Ψ = F_drive
    
    Definiendo y = [Ψ, ∂Ψ/∂t], el sistema se convierte en:
        ∂Ψ/∂t = ∂Ψ/∂t
        ∂(∂Ψ/∂t)/∂t = -ω₀²Ψ + F_drive
    
    Args:
        t (float): Tiempo
        y (array): [Ψ, ∂Ψ/∂t]
    
    Returns:
        array: [∂Ψ/∂t, ∂²Ψ/∂t²]
    """
    psi, psi_dot = y
    
    # Ecuación diferencial: ∂²Ψ/∂t² = -ω₀²Ψ + F_drive
    psi_ddot = -omega_0**2 * psi + F_drive
    
    return [psi_dot, psi_ddot]

# Versión para odeint (orden de argumentos diferente)
def ecuacion_latido_universal_odeint(y, t):
    """Versión compatible con odeint."""
    return ecuacion_latido_universal(t, y)

# ============================================================================
# SOLUCIÓN ANALÍTICA (CASO PARTICULAR)
# ============================================================================

def solucion_particular():
    """
    Solución particular de la ecuación no homogénea.
    
    Para ∂²Ψ/∂t² + ω₀²Ψ = F_drive (constante):
        Ψ_p = F_drive / ω₀²
    
    Returns:
        float: Solución particular
    """
    return F_drive / omega_0**2

def solucion_homogenea(t, A, B, phi):
    """
    Solución general de la ecuación homogénea:
        Ψ_h(t) = A·cos(ω₀·t + φ)
    
    Args:
        t (array): Tiempo
        A (float): Amplitud
        B (float): No usado (compatibilidad)
        phi (float): Fase inicial
    
    Returns:
        array: Solución homogénea
    """
    return A * np.cos(omega_0 * t + phi)

def solucion_general(t, A, phi, psi_p):
    """
    Solución general = solución homogénea + solución particular:
        Ψ(t) = A·cos(ω₀·t + φ) + Ψ_p
    
    Args:
        t (array): Tiempo
        A (float): Amplitud
        phi (float): Fase inicial
        psi_p (float): Solución particular
    
    Returns:
        array: Solución general
    """
    return A * np.cos(omega_0 * t + phi) + psi_p

# ============================================================================
# RESOLVER LA ECUACIÓN
# ============================================================================

def resolver_ecuacion(t_max=0.1, dt=1e-5, condiciones_iniciales=None):
    """
    Resuelve numéricamente la ecuación del latido universal.
    
    Args:
        t_max (float): Tiempo máximo de integración (segundos)
        dt (float): Paso de tiempo para output
        condiciones_iniciales (list): [Ψ(0), ∂Ψ/∂t(0)]. Si None, usa [0, 0]
    
    Returns:
        dict: Resultados de la integración
    """
    # Condiciones iniciales por defecto
    if condiciones_iniciales is None:
        condiciones_iniciales = [0.0, 0.0]  # Ψ(0) = 0, ∂Ψ/∂t(0) = 0
    
    # Vector de tiempos
    t_span = (0, t_max)
    t_eval = np.arange(0, t_max, dt)
    
    # Resolver usando solve_ivp (más robusto)
    sol = solve_ivp(
        ecuacion_latido_universal,
        t_span,
        condiciones_iniciales,
        t_eval=t_eval,
        method='RK45',
        rtol=1e-10,
        atol=1e-12
    )
    
    # Extraer resultados
    t = sol.t
    psi = sol.y[0]
    psi_dot = sol.y[1]
    
    # Calcular derivada segunda
    psi_ddot = -omega_0**2 * psi + F_drive
    
    # Calcular energía
    E_kinetic = 0.5 * psi_dot**2
    E_potential = 0.5 * omega_0**2 * psi**2
    E_total = E_kinetic + E_potential
    
    return {
        't': t,
        'psi': psi,
        'psi_dot': psi_dot,
        'psi_ddot': psi_ddot,
        'E_kinetic': E_kinetic,
        'E_potential': E_potential,
        'E_total': E_total
    }

# ============================================================================
# ANÁLISIS DE RESULTADOS
# ============================================================================

def analizar_solucion(resultados):
    """
    Analiza la solución numérica y extrae propiedades importantes.
    
    Args:
        resultados (dict): Resultados de resolver_ecuacion()
    
    Returns:
        dict: Análisis de la solución
    """
    t = resultados['t']
    psi = resultados['psi']
    psi_dot = resultados['psi_dot']
    E_total = resultados['E_total']
    
    # Amplitud máxima
    psi_max = np.max(np.abs(psi))
    
    # Velocidad máxima
    psi_dot_max = np.max(np.abs(psi_dot))
    
    # Energía media
    E_mean = np.mean(E_total)
    
    # Variación de energía (para verificar conservación)
    E_std = np.std(E_total)
    E_variation = (np.max(E_total) - np.min(E_total)) / E_mean if E_mean > 0 else 0
    
    # Período de oscilación (teórico)
    T_teorico = 2 * np.pi / omega_0
    
    # Frecuencia (teórica)
    f_teorico = 1 / T_teorico
    
    # Solución particular (valor de equilibrio)
    psi_particular = solucion_particular()
    
    # Análisis de fase
    fase_inicial = np.arctan2(-psi_dot[0], psi[0] - psi_particular) if len(psi) > 0 else 0
    
    analisis = {
        'amplitud_maxima': psi_max,
        'velocidad_maxima': psi_dot_max,
        'energia_media': E_mean,
        'energia_std': E_std,
        'energia_variacion_relativa': E_variation,
        'periodo_teorico': T_teorico,
        'frecuencia_teorica': f_teorico,
        'omega_0': omega_0,
        'solucion_particular': psi_particular,
        'fase_inicial': fase_inicial,
        'termino_forzamiento': F_drive
    }
    
    return analisis

# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def visualizar_solucion(resultados, analisis, output_dir='results/figures'):
    """
    Crea visualizaciones de la solución.
    
    Args:
        resultados (dict): Resultados de resolver_ecuacion()
        analisis (dict): Análisis de analizar_solucion()
        output_dir (str): Directorio de salida
    
    Returns:
        list: Lista de archivos generados
    """
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    t = resultados['t']
    psi = resultados['psi']
    psi_dot = resultados['psi_dot']
    psi_ddot = resultados['psi_ddot']
    E_kinetic = resultados['E_kinetic']
    E_potential = resultados['E_potential']
    E_total = resultados['E_total']
    
    archivos_generados = []
    
    # ========================================================================
    # Figura 1: Solución Ψ(t)
    # ========================================================================
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    
    # Subplot 1: Ψ(t)
    axes[0].plot(t * 1000, psi, 'b-', linewidth=1.5, label='Ψ(t)')
    axes[0].axhline(y=analisis['solucion_particular'], color='r', 
                    linestyle='--', linewidth=1, label=f'Ψ_p = {analisis["solucion_particular"]:.2e}')
    axes[0].set_ylabel('Ψ(t)', fontsize=12)
    axes[0].set_title('Ecuación del Latido Universal: Solución Numérica', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right')
    
    # Subplot 2: ∂Ψ/∂t
    axes[1].plot(t * 1000, psi_dot, 'g-', linewidth=1.5, label='∂Ψ/∂t')
    axes[1].axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
    axes[1].set_ylabel('∂Ψ/∂t (s⁻¹)', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right')
    
    # Subplot 3: ∂²Ψ/∂t²
    axes[2].plot(t * 1000, psi_ddot, 'r-', linewidth=1.5, label='∂²Ψ/∂t²')
    axes[2].axhline(y=F_drive, color='orange', linestyle='--', 
                    linewidth=1, label=f'F_drive = {F_drive:.2e}')
    axes[2].set_xlabel('Tiempo (ms)', fontsize=12)
    axes[2].set_ylabel('∂²Ψ/∂t² (s⁻²)', fontsize=12)
    axes[2].grid(True, alpha=0.3)
    axes[2].legend(loc='upper right')
    
    plt.tight_layout()
    
    filename1 = os.path.join(output_dir, 'latido_universal_solucion.png')
    plt.savefig(filename1, dpi=150, bbox_inches='tight')
    plt.close()
    archivos_generados.append(filename1)
    
    # ========================================================================
    # Figura 2: Análisis de Energía
    # ========================================================================
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Subplot 1: Componentes de energía
    axes[0].plot(t * 1000, E_kinetic, 'b-', linewidth=1.5, label='E_cinética', alpha=0.7)
    axes[0].plot(t * 1000, E_potential, 'r-', linewidth=1.5, label='E_potencial', alpha=0.7)
    axes[0].plot(t * 1000, E_total, 'k-', linewidth=2, label='E_total')
    axes[0].set_ylabel('Energía', fontsize=12)
    axes[0].set_title('Análisis de Energía del Campo Ψ', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right')
    
    # Subplot 2: Espacio de fases
    axes[1].plot(psi, psi_dot, 'b-', linewidth=1, alpha=0.7)
    axes[1].plot(psi[0], psi_dot[0], 'go', markersize=10, label='Inicio', zorder=5)
    axes[1].plot(psi[-1], psi_dot[-1], 'ro', markersize=10, label='Final', zorder=5)
    axes[1].set_xlabel('Ψ', fontsize=12)
    axes[1].set_ylabel('∂Ψ/∂t (s⁻¹)', fontsize=12)
    axes[1].set_title('Espacio de Fases', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right')
    
    plt.tight_layout()
    
    filename2 = os.path.join(output_dir, 'latido_universal_energia.png')
    plt.savefig(filename2, dpi=150, bbox_inches='tight')
    plt.close()
    archivos_generados.append(filename2)
    
    # ========================================================================
    # Figura 3: Espectro de Frecuencias
    # ========================================================================
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # FFT de Ψ(t)
    dt = t[1] - t[0]
    n = len(psi)
    freqs = np.fft.fftfreq(n, dt)
    fft_psi = np.fft.fft(psi - analisis['solucion_particular'])
    power = np.abs(fft_psi)**2
    
    # Solo frecuencias positivas
    mask = freqs > 0
    freqs_pos = freqs[mask]
    power_pos = power[mask]
    
    # Graficar
    ax.semilogy(freqs_pos, power_pos, 'b-', linewidth=1.5)
    ax.axvline(x=f0, color='r', linestyle='--', linewidth=2, 
               label=f'f₀ = {f0} Hz')
    ax.set_xlabel('Frecuencia (Hz)', fontsize=12)
    ax.set_ylabel('Potencia Espectral', fontsize=12)
    ax.set_title('Espectro de Frecuencias de Ψ(t)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_xlim([0, 300])
    
    plt.tight_layout()
    
    filename3 = os.path.join(output_dir, 'latido_universal_espectro.png')
    plt.savefig(filename3, dpi=150, bbox_inches='tight')
    plt.close()
    archivos_generados.append(filename3)
    
    return archivos_generados

# ============================================================================
# GUARDAR RESULTADOS
# ============================================================================

def guardar_resultados(resultados, analisis, output_dir='results'):
    """
    Guarda los resultados en formato JSON.
    
    Args:
        resultados (dict): Resultados de resolver_ecuacion()
        analisis (dict): Análisis de analizar_solucion()
        output_dir (str): Directorio de salida
    
    Returns:
        str: Ruta del archivo generado
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Preparar datos para JSON (convertir arrays a listas)
    datos_json = {
        'parametros': {
            'f0_Hz': f0,
            'omega_0_rad_s': omega_0,
            'zeta_prime_half': zeta_prime_half,
            'I': I,
            'A_eff': A_eff,
            'F_drive': F_drive
        },
        'analisis': analisis,
        'estadisticas': {
            'n_puntos': len(resultados['t']),
            't_inicial': float(resultados['t'][0]),
            't_final': float(resultados['t'][-1]),
            'dt': float(resultados['t'][1] - resultados['t'][0])
        }
    }
    
    filename = os.path.join(output_dir, 'latido_universal_resultados.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(datos_json, f, indent=2, ensure_ascii=False)
    
    return filename

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal: resuelve, analiza y visualiza la ecuación del latido universal.
    """
    print("=" * 80)
    print("ECUACIÓN DEL LATIDO UNIVERSAL")
    print("=" * 80)
    print()
    print("Resolviendo la ecuación diferencial:")
    print()
    print("    ∂²Ψ/∂t² + ω₀²Ψ = I·A²eff·ζ'(1/2)")
    print()
    print("Parámetros:")
    print(f"    f₀ = {f0} Hz")
    print(f"    ω₀ = 2πf₀ = {omega_0:.4f} rad/s")
    print(f"    ζ'(1/2) = {zeta_prime_half:.8f}")
    print(f"    I = {I}")
    print(f"    A_eff = {A_eff}")
    print(f"    F_drive = I·A²eff·ζ'(1/2) = {F_drive:.8f}")
    print()
    
    # Resolver la ecuación
    print("Resolviendo ecuación numéricamente...")
    resultados = resolver_ecuacion(t_max=0.05, dt=1e-5)
    print(f"    ✓ Integración completada ({len(resultados['t'])} puntos)")
    print()
    
    # Analizar la solución
    print("Analizando solución...")
    analisis = analizar_solucion(resultados)
    print(f"    Amplitud máxima: {analisis['amplitud_maxima']:.6e}")
    print(f"    Velocidad máxima: {analisis['velocidad_maxima']:.6e} s⁻¹")
    print(f"    Energía media: {analisis['energia_media']:.6e}")
    print(f"    Período teórico: {analisis['periodo_teorico']*1000:.4f} ms")
    print(f"    Frecuencia teórica: {analisis['frecuencia_teorica']:.4f} Hz")
    print(f"    Solución particular: Ψ_p = {analisis['solucion_particular']:.6e}")
    print(f"    Variación energía: {analisis['energia_variacion_relativa']*100:.4f}%")
    print()
    
    # Visualizar
    print("Generando visualizaciones...")
    archivos = visualizar_solucion(resultados, analisis)
    for archivo in archivos:
        print(f"    ✓ {archivo}")
    print()
    
    # Guardar resultados
    print("Guardando resultados...")
    archivo_json = guardar_resultados(resultados, analisis)
    print(f"    ✓ {archivo_json}")
    print()
    
    print("=" * 80)
    print("✓ Análisis completado exitosamente")
    print("=" * 80)

if __name__ == '__main__':
    main()
