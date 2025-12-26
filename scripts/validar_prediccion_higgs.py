#!/usr/bin/env python3
"""
Validación de Predicción 3: Canal Invisible Modulado en el Higgs
====================================================================

Este script analiza la predicción de modulación azimutal en decaimientos
invisibles del Higgs a través del canal H → ΨΨ.

Predicción:
    BR(H → ΨΨ) ∼ 10⁻¹⁰ - 10⁻⁸
    Modulación azimutal: A₂ o A₄ ≠ 0 con p < 0.01

Autor: José Manuel Mota Burruezo (JMMB Ψ ✧)
Fecha: Diciembre 2025
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Constantes del Higgs
M_HIGGS = 125.0  # GeV
# Producción del Higgs en LHC a 13 TeV por modo relevante:
SIGMA_HIGGS_VBF_SM = 3.8  # pb (Vector Boson Fusion, VBF, aprox. 3.8 pb)
SIGMA_HIGGS_VH_SM = 2.3   # pb (Asociado a bosón vectorial, VH, aprox. 2.3 pb)
SIGMA_HIGGS_SM = SIGMA_HIGGS_VBF_SM + SIGMA_HIGGS_VH_SM  # pb total para canales relevantes
BR_INVISIBLE_SM = 0.001  # Límite actual ~0.1%, usamos conservador


def calcular_armonicos_azimutales(phi_events):
    """
    Calcula los armónicos azimutales A_n de la distribución MET.
    
    A_n = (1/N) Σ cos(n φ_i)
    
    Args:
        phi_events: Array de ángulos azimutales (radianes)
    
    Returns:
        dict: Armónicos A₁, A₂, A₃, A₄
    """
    N = len(phi_events)
    armonicos = {}
    
    for n in [1, 2, 3, 4]:
        A_n = np.sum(np.cos(n * phi_events)) / N
        armonicos[f'A{n}'] = A_n
    
    return armonicos


def generar_eventos_SM(N, seed=42):
    """
    Genera eventos de fondo del Modelo Estándar (isotrópicos).
    
    Args:
        N: Número de eventos
        seed: Semilla para reproducibilidad
    
    Returns:
        array: Ángulos azimutales (radianes)
    """
    np.random.seed(seed)
    phi_SM = np.random.uniform(0, 2*np.pi, N)
    return phi_SM


def generar_eventos_señal_psi(N, A2_signal=0.10, seed=43):
    """
    Genera eventos con modulación del campo Ψ.
    
    Distribución: dN/dφ ∝ 1 + 2A₂cos(2φ)
    
    Args:
        N: Número de eventos
        A2_signal: Amplitud de modulación cuadrupolar
        seed: Semilla para reproducibilidad
    
    Returns:
        array: Ángulos azimutales (radianes)
    """
    np.random.seed(seed)
    
    # Método de aceptación-rechazo
    phi_events = []
    phi_max_density = 1 + 2*abs(A2_signal)
    
    while len(phi_events) < N:
        phi_candidate = np.random.uniform(0, 2*np.pi)
        density = 1 + 2*A2_signal*np.cos(2*phi_candidate)
        accept_prob = density / phi_max_density
        
        if np.random.uniform(0, 1) < accept_prob:
            phi_events.append(phi_candidate)
    
    return np.array(phi_events)


def test_estadistico_chi2(phi_obs, n_bins=16):
    """
    Test χ² para uniformidad azimutal.
    
    Args:
        phi_obs: Ángulos observados (radianes)
        n_bins: Número de bins para histograma
    
    Returns:
        dict: chi2, p_value, dof
    """
    # Histograma observado
    counts, bin_edges = np.histogram(phi_obs, bins=n_bins, range=(0, 2*np.pi))
    
    # Expectativa uniforme
    N_total = len(phi_obs)
    expected = N_total / n_bins
    
    # χ² = Σ (O_i - E_i)² / E_i
    chi2 = np.sum((counts - expected)**2 / expected)
    dof = n_bins - 1
    p_value = 1 - stats.chi2.cdf(chi2, dof)
    
    return {'chi2': chi2, 'p_value': p_value, 'dof': dof}


def estimar_eventos_HL_LHC():
    """
    Estima número de eventos H → invisible en HL-LHC.
    """
    print("\n" + "="*70)
    print("ESTIMACIÓN DE EVENTOS EN HL-LHC")
    print("="*70)
    
    # Parámetros HL-LHC
    luminosidad_total = 3000  # fb⁻¹
    sigma_higgs = 55.0  # pb
    BR_invisible = 0.001  # 0.1% (límite actual conservador)
    eficiencia_seleccion = 0.3  # 30% (VBF, VH channels)
    
    # Cálculo
    N_higgs = luminosidad_total * 1000 * sigma_higgs  # Total Higgs producidos
    N_invisible = N_higgs * BR_invisible * eficiencia_seleccion
    
    print(f"\nParámetros:")
    print(f"  Luminosidad integrada: L = {luminosidad_total} fb⁻¹")
    print(f"  σ(pp → H): {sigma_higgs} pb")
    print(f"  BR(H → invisible) SM: {BR_invisible*100}%")
    print(f"  Eficiencia de selección: {eficiencia_seleccion*100}%")
    
    print(f"\nEventos esperados:")
    print(f"  Total Higgs producidos: {N_higgs:.2e}")
    print(f"  H → invisible detectables: {N_invisible:.0f}")
    
    # Componente Ψ
    BR_psi_range = [1e-10, 1e-9, 1e-8]
    
    print(f"\nContribución del canal H → ΨΨ:")
    for BR_psi in BR_psi_range:
        N_psi = luminosidad_total * 1000 * sigma_higgs * BR_psi * eficiencia_seleccion
        fraction = N_psi / N_invisible if N_invisible > 0 else 0
        print(f"  BR(H → ΨΨ) = {BR_psi:.0e}: N_Ψ = {N_psi:.1f} eventos ({fraction*100:.2f}% del total)")
    
    print("\n" + "="*70)
    
    return int(N_invisible)


def simular_experimento_HL_LHC():
    """
    Simula el experimento de búsqueda en HL-LHC.
    """
    print("\n" + "="*70)
    print("SIMULACIÓN DE EXPERIMENTO HL-LHC")
    print("="*70)
    
    # Escenarios
    N_total = estimar_eventos_HL_LHC()
    
    # Escenario 1: Solo SM (sin señal Ψ)
    print("\nESCENARIO 1: Solo Modelo Estándar")
    phi_SM = generar_eventos_SM(N_total)
    arm_SM = calcular_armonicos_azimutales(phi_SM)
    chi2_SM = test_estadistico_chi2(phi_SM)
    
    print(f"  N_eventos = {N_total}")
    print(f"  Armónicos:")
    for key, val in arm_SM.items():
        print(f"    {key} = {val:.4f}")
    print(f"  Test χ²: χ² = {chi2_SM['chi2']:.2f}, p = {chi2_SM['p_value']:.4f}")
    
    # Escenario 2: SM + señal Ψ (BR = 10⁻⁹, modulación A₂ = 0.10)
    print("\nESCENARIO 2: SM + Señal Ψ (BR ∼ 10⁻⁹, A₂ = 0.10)")
    
    # Eventos de fondo SM
    N_bg = N_total - 50  # Restar eventos Ψ
    phi_bg = generar_eventos_SM(N_bg, seed=42)
    
    # Eventos de señal Ψ
    N_sig = 50
    phi_sig = generar_eventos_señal_psi(N_sig, A2_signal=0.10, seed=43)
    
    # Combinar
    phi_total = np.concatenate([phi_bg, phi_sig])
    arm_total = calcular_armonicos_azimutales(phi_total)
    chi2_total = test_estadistico_chi2(phi_total)
    
    print(f"  N_eventos (total) = {len(phi_total)}")
    print(f"  N_eventos (Ψ) = {N_sig}")
    print(f"  Armónicos:")
    for key, val in arm_total.items():
        print(f"    {key} = {val:.4f}")
    print(f"  Test χ²: χ² = {chi2_total['chi2']:.2f}, p = {chi2_total['p_value']:.4f}")
    
    # Comparación
    print("\nCOMPARACIÓN:")
    print(f"  ΔA₂ = {abs(arm_total['A2'] - arm_SM['A2']):.4f}")
    print(f"  Significancia: {abs(arm_total['A2'])/np.sqrt(1.0/N_total):.2f} σ")
    
    if chi2_total['p_value'] < 0.01:
        print(f"  ✓ Desviación estadísticamente significativa (p < 0.01)")
    else:
        print(f"  ✗ No significativa (p > 0.01)")
    
    print("="*70)
    
    return phi_SM, phi_total


def generar_graficas_analisis():
    """
    Genera gráficas del análisis de modulación azimutal.
    """
    print("\nGenerando gráficas...")
    
    phi_SM, phi_signal = simular_experimento_HL_LHC()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: Distribución azimutal SM
    ax1 = axes[0, 0]
    ax1.hist(phi_SM, bins=24, range=(0, 2*np.pi), alpha=0.7, color='blue', 
             edgecolor='black', label='Modelo Estándar')
    ax1.axhline(len(phi_SM)/24, color='red', linestyle='--', linewidth=2, label='Uniforme')
    ax1.set_xlabel('Ángulo azimutal φ (rad)', fontsize=11)
    ax1.set_ylabel('Número de eventos', fontsize=11)
    ax1.set_title('Distribución SM (isotrópica)', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Distribución azimutal con señal Ψ
    ax2 = axes[0, 1]
    ax2.hist(phi_signal, bins=24, range=(0, 2*np.pi), alpha=0.7, color='green',
             edgecolor='black', label='SM + Señal Ψ')
    ax2.axhline(len(phi_signal)/24, color='red', linestyle='--', linewidth=2, label='Uniforme')
    ax2.set_xlabel('Ángulo azimutal φ (rad)', fontsize=11)
    ax2.set_ylabel('Número de eventos', fontsize=11)
    ax2.set_title('Distribución con Modulación Ψ (A₂ ≠ 0)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Subplot 3: Armónicos azimutales
    ax3 = axes[1, 0]
    arm_SM = calcular_armonicos_azimutales(phi_SM)
    arm_signal = calcular_armonicos_azimutales(phi_signal)
    
    n_values = [1, 2, 3, 4]
    A_SM = [arm_SM[f'A{n}'] for n in n_values]
    A_signal = [arm_signal[f'A{n}'] for n in n_values]
    
    x = np.arange(len(n_values))
    width = 0.35
    
    ax3.bar(x - width/2, A_SM, width, label='SM', color='blue', alpha=0.7)
    ax3.bar(x + width/2, A_signal, width, label='SM + Ψ', color='green', alpha=0.7)
    ax3.axhline(0, color='black', linewidth=0.5)
    ax3.set_xlabel('Armónico n', fontsize=11)
    ax3.set_ylabel('A_n', fontsize=11)
    ax3.set_title('Armónicos Azimutales', fontsize=12, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels([f'A{n}' for n in n_values])
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Subplot 4: Sensibilidad vs BR(H → ΨΨ)
    ax4 = axes[1, 1]
    
    BR_range = np.logspace(-10, -7, 50)
    N_total = len(phi_SM)
    luminosidad = 3000  # fb⁻¹
    sigma_higgs = 55.0  # pb
    eficiencia = 0.3
    
    N_psi = luminosidad * 1000 * sigma_higgs * BR_range * eficiencia
    
    # Significancia aproximada: σ ∼ S/√B
    significance = N_psi / np.sqrt(N_total)
    
    ax4.loglog(BR_range, significance, linewidth=2, color='purple')
    ax4.axhline(3, color='red', linestyle='--', linewidth=2, label='3σ discovery')
    ax4.axhline(5, color='orange', linestyle='--', linewidth=2, label='5σ discovery')
    ax4.set_xlabel('BR(H → ΨΨ)', fontsize=11)
    ax4.set_ylabel('Significancia (σ)', fontsize=11)
    ax4.set_title('Sensibilidad HL-LHC', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Predicción 3: Canal Invisible Modulado en el Higgs',
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('prediccion_higgs_invisible.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfica guardada: prediccion_higgs_invisible.png")
    plt.close()


def protocolo_experimental():
    """
    Describe el protocolo experimental detallado.
    """
    print("\n" + "="*70)
    print("PROTOCOLO EXPERIMENTAL: ATLAS & CMS")
    print("="*70)
    
    print("\n1. SELECCIÓN DE EVENTOS")
    print("   Canal: pp → H + jet(s), H → invisible")
    print("   Topologías:")
    print("     - VBF (Vector Boson Fusion): 2 jets forward")
    print("     - VH (Vector + Higgs): W/Z → leptons, H → invisible")
    print("   Triggers:")
    print("     - MET > 200 GeV")
    print("     - Jets with p_T > 50 GeV")
    
    print("\n2. RECONSTRUCCIÓN")
    print("   - Energía faltante: E_T^miss, p_T^miss")
    print("   - Ángulo azimutal: φ(MET) = atan2(p_y^miss, p_x^miss)")
    print("   - Masa transversa: m_T(H) compatible con 125 GeV")
    
    print("\n3. ANÁLISIS DE MODULACIÓN")
    print("   Para cada evento i:")
    print("     a) Medir φ_i = φ(MET)")
    print("     b) Acumular estadísticas N(φ)")
    print("   Calcular armónicos:")
    print("     A_n = (1/N) Σ cos(n φ_i) para n=1,2,3,4")
    
    print("\n4. TEST ESTADÍSTICO")
    print("   - Hipótesis nula: A_n = 0 (isotrópico)")
    print("   - Test χ² de uniformidad")
    print("   - Significancia: p-value < 0.01 para rechazo")
    
    print("\n5. VALIDACIÓN CRUZADA")
    print("   - Comparar ATLAS vs. CMS")
    print("   - Diferentes períodos de datos (Run 4, Run 5)")
    print("   - Control regions (canales SM puros)")
    
    print("="*70)


def criterio_falsacion():
    """
    Define criterios de falsación.
    """
    print("\n" + "="*70)
    print("CRITERIO DE FALSACIÓN")
    print("="*70)
    
    print("\n❌ La predicción es REFUTADA si:")
    print("   1. Con L = 3000 fb⁻¹ completos (HL-LHC)")
    print("   2. Análisis en ambas colaboraciones (ATLAS y CMS)")
    print("   3. Armónicos A₂ y A₄ consistentes con cero:")
    print("      |A_n| < 0.02 con p > 0.05")
    print("   4. No hay desviación del patrón isotrópico SM")
    print("   5. Sistemáticos bajo control (detector, pileup, etc.)")
    
    print("\n✓ La predicción es CONFIRMADA si:")
    print("   1. A₂ o A₄ significativamente ≠ 0 (p < 0.01)")
    print("   2. Reproducido independientemente en ATLAS y CMS")
    print("   3. Sistemáticos descartados como origen")
    print("   4. Consistencia en diferentes canales (VBF, VH)")
    
    print("\n" + "="*70)


def main():
    """
    Función principal de validación.
    """
    print("="*70)
    print("VALIDACIÓN: PREDICCIÓN 3 - CANAL INVISIBLE DEL HIGGS")
    print("Marco: QCAL ∞³")
    print("="*70)
    
    # 1. Estimación de eventos
    estimar_eventos_HL_LHC()
    
    # 2. Simulación
    simular_experimento_HL_LHC()
    
    # 3. Gráficas
    generar_graficas_analisis()
    
    # 4. Protocolo experimental
    protocolo_experimental()
    
    # 5. Criterio de falsación
    criterio_falsacion()
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE PREDICCIÓN 3")
    print("="*70)
    print("\n✓ PREDICCIÓN:")
    print("  BR(H → ΨΨ) ∼ 10⁻¹⁰ - 10⁻⁸")
    print("  Modulación azimutal: A₂ o A₄ ≠ 0")
    
    print("\n✓ PLATAFORMA:")
    print("  HL-LHC (ATLAS & CMS) con 3000 fb⁻¹")
    
    print("\n✓ FACTIBILIDAD:")
    print("  Media - Requiere dataset completo HL-LHC (~2030)")
    print("  Análisis estándar de MET, alta estadística")
    
    print("\n✓ NOTA:")
    print("  El canal H → ΨΨ es fenomenológicamente similar a")
    print("  H → invisible del SM, pero con firma distintiva")
    print("  en la distribución azimutal del MET.")
    
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
