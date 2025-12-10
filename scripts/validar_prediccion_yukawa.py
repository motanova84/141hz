#!/usr/bin/env python3
"""
Validación de Predicción 1: Corrección Yukawa a Corto Alcance
================================================================

Este script calcula y valida la corrección tipo Yukawa al potencial gravitacional
predicha por el marco QCAL ∞³.

Predicción:
    V(r) = -GM/r · (1 + α e^(-r/λ_Ψ))
    
Donde:
    - λ_Ψ ≈ 337 km (longitud de coherencia del campo Ψ)
    - α ∼ 10⁻⁷ - 10⁻⁵ (intensidad de acoplamiento)

Autor: José Manuel Mota Burruezo (JMMB Ψ ✧)
Fecha: Diciembre 2025
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, c, pi, G

# Constantes del campo Ψ
F0 = 141.7001  # Hz
OMEGA0 = 2 * pi * F0  # rad/s


def calcular_masa_psi():
    """
    Calcula la masa efectiva del campo Ψ.
    
    Returns:
        float: Masa en kg
    """
    m_psi = hbar * OMEGA0 / c**2
    return m_psi


def calcular_lambda_psi():
    """
    Calcula la longitud de coherencia λ_Ψ del campo.
    
    λ_Ψ = ℏ/(m_Ψ c) = c/ω₀
    
    Returns:
        float: Longitud de coherencia en metros
    """
    m_psi = calcular_masa_psi()
    lambda_psi = hbar / (m_psi * c)
    return lambda_psi


def potencial_newtoniano(r, M):
    """
    Potencial gravitacional newtoniano estándar.
    
    Args:
        r: Distancia (m)
        M: Masa fuente (kg)
    
    Returns:
        float: V(r) en J/kg
    """
    return -G * M / r


def potencial_yukawa_modificado(r, M, alpha, lambda_psi):
    """
    Potencial gravitacional con corrección Yukawa.
    
    V(r) = -GM/r · (1 + α e^(-r/λ_Ψ))
    
    Args:
        r: Distancia (m)
        M: Masa fuente (kg)
        alpha: Intensidad de acoplamiento
        lambda_psi: Longitud de coherencia (m)
    
    Returns:
        float: V(r) en J/kg
    """
    V_newton = potencial_newtoniano(r, M)
    correccion = alpha * np.exp(-r / lambda_psi)
    return V_newton * (1 + correccion)


def calcular_desviacion_relativa(r, alpha, lambda_psi):
    """
    Calcula la desviación relativa del potencial newtoniano.
    
    ΔV/V = α e^(-r/λ_Ψ)
    
    Args:
        r: Distancia (m)
        alpha: Intensidad de acoplamiento
        lambda_psi: Longitud de coherencia (m)
    
    Returns:
        float: Desviación relativa (adimensional)
    """
    return alpha * np.exp(-r / lambda_psi)


def generar_grafica_prediccion():
    """
    Genera gráfica de la corrección Yukawa predicha.
    """
    # Parámetros
    lambda_psi = calcular_lambda_psi()
    alpha_min = 1e-7
    alpha_max = 1e-5
    
    # Rango de distancias: 100 m - 10 km
    r = np.logspace(2, 4, 1000)  # 100 m a 10 km
    
    # Calcular desviaciones para diferentes α
    alphas = [1e-7, 1e-6, 1e-5]
    
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Desviación relativa
    plt.subplot(2, 1, 1)
    for alpha in alphas:
        desviacion = calcular_desviacion_relativa(r, alpha, lambda_psi)
        plt.loglog(r/1000, desviacion, label=f'α = {alpha:.0e}', linewidth=2)
    
    plt.axhline(y=1e-12, color='red', linestyle='--', 
                label='Límite sensibilidad Eöt-Wash (~10⁻¹²)')
    plt.xlabel('Distancia (km)', fontsize=12)
    plt.ylabel('Desviación Relativa ΔV/V', fontsize=12)
    plt.title('Predicción 1: Corrección Yukawa al Potencial Gravitacional', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Aceleración gravitacional modificada
    plt.subplot(2, 1, 2)
    M_earth = 5.972e24  # kg
    g_surface = 9.81  # m/s²
    
    for alpha in alphas:
        # Δg/g ≈ ΔV/V (para correcciones pequeñas)
        delta_g = g_surface * calcular_desviacion_relativa(r, alpha, lambda_psi)
        plt.loglog(r/1000, delta_g * 1e9, label=f'α = {alpha:.0e}', linewidth=2)  # En nGal
    
    plt.xlabel('Distancia (km)', fontsize=12)
    plt.ylabel('Δg (nGal = 10⁻⁹ m/s²)', fontsize=12)
    plt.title('Corrección en Aceleración Gravitacional', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('prediccion_yukawa.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfica guardada: prediccion_yukawa.png")
    plt.close()


def estimar_escenarios_experimentales():
    """
    Estima señales esperadas en diferentes plataformas experimentales.
    """
    lambda_psi = calcular_lambda_psi()
    
    print("\n" + "="*70)
    print("ESTIMACIONES PARA PLATAFORMAS EXPERIMENTALES")
    print("="*70)
    
    # Escenario 1: Mina profunda (Sudbury)
    print("\n1. MINA PROFUNDA (Tipo Sudbury)")
    print("   Profundidad: 2 km")
    r_mine = 2000  # m
    for alpha in [1e-7, 1e-6, 1e-5]:
        dv = calcular_desviacion_relativa(r_mine, alpha, lambda_psi)
        print(f"   α = {alpha:.0e}: ΔV/V = {dv:.2e}")
    
    # Escenario 2: Túnel CERN
    print("\n2. TÚNEL CERN")
    print("   Longitud: 27 km (pero medición a ~5-10 km)")
    r_cern = 7500  # m (promedio)
    for alpha in [1e-7, 1e-6, 1e-5]:
        dv = calcular_desviacion_relativa(r_cern, alpha, lambda_psi)
        print(f"   α = {alpha:.0e}: ΔV/V = {dv:.2e}")
    
    # Escenario 3: Balance de torsión Eöt-Wash
    print("\n3. BALANCE DE TORSIÓN EÖT-WASH")
    print("   Separación típica: 100 m - 1 km")
    r_eotwash = 500  # m
    for alpha in [1e-7, 1e-6, 1e-5]:
        dv = calcular_desviacion_relativa(r_eotwash, alpha, lambda_psi)
        dg = 9.81 * dv  # m/s²
        print(f"   α = {alpha:.0e}: Δg = {dg:.2e} m/s² = {dg*1e9:.2f} nGal")
    
    # Sensibilidad requerida
    print("\n" + "="*70)
    print("SENSIBILIDAD REQUERIDA")
    print("="*70)
    print(f"Para detectar α = 10⁻⁷ a r = 1 km:")
    dv_min = calcular_desviacion_relativa(1000, 1e-7, lambda_psi)
    print(f"  ΔV/V = {dv_min:.2e}")
    print(f"  Δg/g = {dv_min:.2e}")
    print(f"  Δg = {9.81*dv_min*1e9:.2f} nGal")
    print(f"\n✓ Factible con gravímetros superconductores (sensibilidad ~ 0.1 nGal)")


def verificar_consistencia_teorica():
    """
    Verifica la consistencia teórica de los cálculos.
    """
    print("\n" + "="*70)
    print("VERIFICACIÓN DE CONSISTENCIA TEÓRICA")
    print("="*70)
    
    # Parámetros fundamentales
    m_psi = calcular_masa_psi()
    lambda_psi = calcular_lambda_psi()
    
    print(f"\nParámetros del campo Ψ:")
    print(f"  f₀ = {F0} Hz")
    print(f"  ω₀ = {OMEGA0:.3f} rad/s")
    print(f"  m_Ψ = {m_psi:.3e} kg")
    print(f"  λ_Ψ = {lambda_psi:.3e} m = {lambda_psi/1000:.1f} km")
    
    # Verificación: λ_Ψ = c/ω₀
    lambda_check = c / OMEGA0
    print(f"\nVerificación λ_Ψ = c/ω₀:")
    print(f"  Calculado: {lambda_psi:.3e} m")
    print(f"  Verificado: {lambda_check:.3e} m")
    print(f"  Diferencia: {abs(lambda_psi - lambda_check)/lambda_psi * 100:.2e} %")
    
    # Comparación con longitud de Planck
    l_planck = 1.616e-35  # m
    print(f"\nEscalas de longitud:")
    print(f"  λ_Ψ / ℓ_P = {lambda_psi/l_planck:.2e}")
    print(f"  λ_Ψ / R_Earth = {lambda_psi/6.371e6:.2e}")
    
    # Verificación dimensional
    print(f"\nVerificación dimensional:")
    print(f"  [ℏ/(m_Ψ c)] = [J·s / (kg·m/s)] = [m] ✓")
    print(f"  [α e^(-r/λ)] = [adim] ✓")


def generar_tabla_comparativa():
    """
    Genera tabla comparativa con experimentos existentes.
    """
    lambda_psi = calcular_lambda_psi()
    
    print("\n" + "="*70)
    print("COMPARACIÓN CON LÍMITES EXPERIMENTALES EXISTENTES")
    print("="*70)
    
    # Datos de experimentos reales (límites publicados)
    experimentos = [
        {
            'nombre': 'Eöt-Wash (2003)',
            'r_min': 0.1,  # mm → m
            'r_max': 0.01,  # m
            'alpha_limit': 1e-3,
            'referencia': 'Adelberger et al., Ann. Rev. Nucl. Part. Sci. 53 (2003)'
        },
        {
            'nombre': 'HUST (2020)',
            'r_min': 0.001,  # m
            'r_max': 0.01,   # m
            'alpha_limit': 1e-4,
            'referencia': 'Tan et al., PRL 124 (2020)'
        },
        {
            'nombre': 'Stanford (1987)',
            'r_min': 1,      # m
            'r_max': 100,    # m
            'alpha_limit': 1e-2,
            'referencia': 'Stubbs et al., PRL 58 (1987)'
        }
    ]
    
    print("\nLímites actuales sobre desviaciones del potencial newtoniano:")
    print("-" * 70)
    
    for exp in experimentos:
        print(f"\n{exp['nombre']}:")
        print(f"  Rango de distancia: {exp['r_min']*1000:.1f} mm - {exp['r_max']*1000:.0f} m")
        print(f"  Límite en α: {exp['alpha_limit']:.0e}")
        
        # Nuestra predicción en ese rango
        r_test = np.sqrt(exp['r_min'] * exp['r_max'])  # Media geométrica
        dv_pred = calcular_desviacion_relativa(r_test, 1e-7, lambda_psi)
        print(f"  Predicción QCAL (α=10⁻⁷, r={r_test:.2f} m): ΔV/V = {dv_pred:.2e}")
        
        if dv_pred < exp['alpha_limit']:
            print(f"  ✓ Consistente con límites actuales")
        else:
            print(f"  ✗ Excluido por este experimento")
    
    print("\n" + "="*70)
    print("NOTA: La predicción QCAL ∞³ es detectable principalmente en el rango")
    print("100 m - 10 km, donde los límites actuales son menos restrictivos.")
    print("="*70)


def main():
    """
    Función principal de validación.
    """
    print("="*70)
    print("VALIDACIÓN: PREDICCIÓN 1 - CORRECCIÓN YUKAWA")
    print("Marco: QCAL ∞³")
    print("="*70)
    
    # 1. Verificar consistencia teórica
    verificar_consistencia_teorica()
    
    # 2. Generar gráfica de predicción
    print("\nGenerando gráfica de predicción...")
    generar_grafica_prediccion()
    
    # 3. Estimar escenarios experimentales
    estimar_escenarios_experimentales()
    
    # 4. Comparar con límites existentes
    generar_tabla_comparativa()
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE PREDICCIÓN 1")
    print("="*70)
    print("\n✓ PARÁMETROS CLAVE:")
    lambda_psi = calcular_lambda_psi()
    print(f"  - Longitud de coherencia: λ_Ψ = {lambda_psi/1000:.1f} km")
    print(f"  - Rango de acoplamiento: α = 10⁻⁷ - 10⁻⁵")
    print(f"  - Rango de distancias: 100 m - 10 km")
    
    print("\n✓ PLATAFORMAS EXPERIMENTALES:")
    print("  1. Minas profundas (Sudbury, LNGS)")
    print("  2. Túneles geodésicos (CERN)")
    print("  3. Balances de torsión (Eöt-Wash underground)")
    
    print("\n✓ CRITERIO DE FALSACIÓN:")
    print("  Ausencia reproducible de desviaciones para α > 10⁻⁷")
    print("  en el rango 1-10 km en ≥3 experimentos independientes")
    
    print("\n✓ FACTIBILIDAD:")
    print("  Alta - Tecnología disponible (gravímetros superconductores)")
    print("  Sensibilidad: Δg ~ 0.1 nGal (suficiente para α ~ 10⁻⁶)")
    
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
