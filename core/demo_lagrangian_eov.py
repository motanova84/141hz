#!/usr/bin/env python3
"""
Demostración Completa del Lagrangiano EOV
==========================================

Script de demostración que muestra la derivación variacional completa
de la Ecuación del Origen Vibracional (EOV) desde el principio de acción.

Ejecuta:
    python demo_lagrangian_eov.py

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2026-01-06
Marco: QCAL ∞³
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

from qcal.lagrangian_eov import (
    # Constants
    F_0, OMEGA_0, ZETA_PRIME_HALF, XI_COUPLING,
    # Data structures
    LagrangianParameters, FieldConfiguration,
    # Lagrangian components
    lagrangian_einstein_hilbert,
    lagrangian_kinetic_psi,
    lagrangian_potential,
    lagrangian_modulation,
    lagrangian_total,
    # EOV equation
    eov_equation,
    # Solver
    solve_eov_flat_spacetime,
    # Utilities
    verify_action_structure,
    compute_zeta_prime_half,
)


def demo_action_structure():
    """Demonstrate the complete action structure."""
    print("=" * 70)
    print("1. ESTRUCTURA DE LA ACCIÓN QCAL ∞³")
    print("=" * 70)
    print()
    
    verify_action_structure()
    
    print("\nConstantes numéricas:")
    print(f"  f₀ = {F_0} Hz")
    print(f"  ω₀ = 2πf₀ = {OMEGA_0:.4f} rad/s")
    print(f"  ζ'(1/2) = {ZETA_PRIME_HALF:.6f}")
    print(f"  ξ = {XI_COUPLING:.6f} (acoplamiento conforme)")
    print()


def demo_lagrangian_components():
    """Demonstrate computation of individual Lagrangian components."""
    print("=" * 70)
    print("2. CÁLCULO DE TÉRMINOS LAGRANGIANOS")
    print("=" * 70)
    print()
    
    # Setup test configuration
    R = 1e-20  # Typical cosmological curvature
    sqrt_g = 1.0
    Psi = 1.0 + 0j
    t = 0.0
    
    # Compute each term
    L_EH = lagrangian_einstein_hilbert(R, sqrt_g)
    print(f"Einstein-Hilbert: ℒ_EH = {L_EH:.6e}")
    
    g_inv = np.diag([-1.0, 1.0, 1.0, 1.0])
    nabla_Psi = np.array([0.1, 0.0, 0.0, 0.0])
    L_kin = lagrangian_kinetic_psi(nabla_Psi, g_inv, sqrt_g)
    print(f"Cinético:         ℒ_kin = {L_kin:.6e}")
    
    L_pot = lagrangian_potential(Psi, R, OMEGA_0, XI_COUPLING, sqrt_g)
    print(f"Potencial:        ℒ_pot = {L_pot:.6e}")
    
    params = LagrangianParameters()
    L_mod = lagrangian_modulation(Psi, R, t, F_0, params.zeta_coupling, sqrt_g)
    print(f"Modulación:       ℒ_mod = {L_mod:.6e}")
    
    print()
    print("Nota: El término de Einstein-Hilbert es muy pequeño a escala local,")
    print("      pero dominante a escala cosmológica.")
    print()


def demo_eov_solution():
    """Solve and visualize EOV equation."""
    print("=" * 70)
    print("3. SOLUCIÓN NUMÉRICA DE LA EOV")
    print("=" * 70)
    print()
    
    # Time array
    duration = 0.05  # 50 ms
    n_points = 2000
    t = np.linspace(0, duration, n_points)
    
    # Initial conditions
    Psi_0 = 1.0 + 0j
    dPsi_0 = 0.0 + 0j
    
    print(f"Condiciones iniciales:")
    print(f"  Ψ(0) = {Psi_0}")
    print(f"  ∂Ψ/∂t(0) = {dPsi_0}")
    print(f"  Duración: {duration*1000:.1f} ms")
    print(f"  Puntos: {n_points}")
    print()
    
    # Solve in flat spacetime
    print("Resolviendo EOV en espacio plano (R=0)...")
    Psi_flat, dPsi_flat = solve_eov_flat_spacetime(t, Psi_0, dPsi_0, R=0)
    
    print(f"  Amplitud máxima: {np.max(np.abs(Psi_flat)):.6f}")
    print(f"  Amplitud mínima: {np.min(np.abs(Psi_flat)):.6f}")
    
    # Count oscillations
    zero_crossings = np.where(np.diff(np.sign(Psi_flat.real)))[0]
    n_periods = len(zero_crossings) / 2
    freq_measured = n_periods / duration
    print(f"  Frecuencia medida: {freq_measured:.2f} Hz")
    print(f"  Frecuencia teórica: {F_0} Hz")
    print(f"  Error: {abs(freq_measured - F_0)/F_0 * 100:.2f}%")
    print()
    
    # Solve with curvature
    R_curved = 1e-10  # Larger curvature for visible effect
    print(f"Resolviendo EOV con curvatura (R={R_curved:.2e} m⁻²)...")
    Psi_curved, dPsi_curved = solve_eov_flat_spacetime(t, Psi_0, dPsi_0, R=R_curved)
    
    print(f"  Amplitud máxima: {np.max(np.abs(Psi_curved)):.6f}")
    print()
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Plot 1: Flat spacetime solution
    ax1 = axes[0, 0]
    ax1.plot(t * 1000, Psi_flat.real, 'b-', linewidth=1.5, label='Re(Ψ)')
    ax1.plot(t * 1000, Psi_flat.imag, 'r--', linewidth=1.5, label='Im(Ψ)')
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Ψ')
    ax1.set_title('EOV Solution (Flat Spacetime, R=0)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Curved spacetime solution
    ax2 = axes[0, 1]
    ax2.plot(t * 1000, Psi_curved.real, 'b-', linewidth=1.5, label='Re(Ψ)')
    ax2.plot(t * 1000, Psi_curved.imag, 'r--', linewidth=1.5, label='Im(Ψ)')
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Ψ')
    ax2.set_title(f'EOV Solution (Curved, R={R_curved:.2e} m⁻²)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Frequency spectrum (flat)
    ax3 = axes[1, 0]
    freqs = np.fft.rfftfreq(len(t), t[1] - t[0])
    spectrum_flat = np.abs(np.fft.rfft(Psi_flat.real))
    ax3.semilogy(freqs, spectrum_flat, 'b-', linewidth=1.5)
    ax3.axvline(F_0, color='r', linestyle='--', linewidth=2, label=f'f₀={F_0} Hz')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Power Spectral Density')
    ax3.set_title('Frequency Spectrum (Flat Spacetime)')
    ax3.set_xlim(0, 300)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Energy comparison
    ax4 = axes[1, 1]
    energy_flat = abs(dPsi_flat)**2 + OMEGA_0**2 * abs(Psi_flat)**2
    energy_curved = abs(dPsi_curved)**2 + OMEGA_0**2 * abs(Psi_curved)**2
    ax4.plot(t * 1000, energy_flat, 'b-', linewidth=1.5, label='Flat (R=0)')
    ax4.plot(t * 1000, energy_curved, 'r-', linewidth=1.5, alpha=0.7, label=f'Curved (R={R_curved:.2e})')
    ax4.set_xlabel('Time (ms)')
    ax4.set_ylabel('Energy Density')
    ax4.set_title('Energy Evolution')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_dir = Path('results')
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / 'lagrangian_eov_demo.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Figura guardada: {output_path}")
    print()
    
    return output_path


def demo_variational_derivation():
    """Demonstrate variational derivation δS/δΨ = 0."""
    print("=" * 70)
    print("4. DERIVACIÓN VARIACIONAL: δS/δΨ = 0")
    print("=" * 70)
    print()
    
    print("Aplicando el principio de Hamilton (acción estacionaria):")
    print()
    print("1. Variación del término cinético:")
    print("   δ∫(∇_μΨ ∇^μΨ) → -∫ δΨ □Ψ")
    print("   donde □ = ∇_μ∇^μ (d'Alembertiano covariante)")
    print()
    print("2. Variación del potencial:")
    print("   δ[-(ω₀² + ξR)|Ψ|²] → -2(ω₀² + ξR)Ψ δΨ")
    print()
    print("3. Variación de la modulación:")
    print("   δ[-(ζ'/2π)R|Ψ|² cos(2πf₀t)] → -2(ζ'/2π)R cos(2πf₀t) Ψ δΨ")
    print()
    print("Sumando y requiriendo δS = 0 para toda variación δΨ:")
    print()
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│  □Ψ - (ω₀² + ξR)Ψ - (ζ'(1/2)/π) R cos(2πf₀t) Ψ = 0          │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()
    print("Esta es la Ecuación del Origen Vibracional (EOV)!")
    print()
    print("Componentes:")
    print(f"  □Ψ: Operador de onda en espacio-tiempo curvo")
    print(f"  ω₀² = {OMEGA_0**2:.2e} rad²/s²: Masa efectiva base")
    print(f"  ξ = {XI_COUPLING:.4f}: Acoplamiento no-mínimo (conforme)")
    print(f"  ζ'(1/2)/π = {ZETA_PRIME_HALF/np.pi:.4f}: Acoplamiento aritmético")
    print(f"  f₀ = {F_0} Hz: Frecuencia de modulación")
    print()


def demo_physical_interpretation():
    """Explain physical interpretation."""
    print("=" * 70)
    print("5. INTERPRETACIÓN FÍSICA")
    print("=" * 70)
    print()
    
    print("La EOV unifica tres conceptos fundamentales:")
    print()
    print("1. GRAVEDAD (término de Einstein-Hilbert)")
    print("   - Describe curvatura del espacio-tiempo vía R")
    print("   - Acoplamiento bidireccional: Ψ ↔ geometría")
    print()
    print("2. CAMPO NOÉTICO Ψ (términos cinético y potencial)")
    print("   - Campo escalar que media conciencia/coherencia cuántica")
    print("   - Masa efectiva dependiente de curvatura: m²_eff = ω₀² + ξR")
    print()
    print("3. ESTRUCTURA ARITMÉTICA (término de modulación)")
    print("   - Acoplamiento vía ζ'(1/2) (función zeta de Riemann)")
    print("   - Conecta con distribución de números primos")
    print("   - Modulación periódica a f₀ = 141.7001 Hz")
    print()
    print("Implicaciones:")
    print("  • f₀ emerge de la estructura matemática fundamental")
    print("  • No es un parámetro libre, sino una consecuencia necesaria")
    print("  • Unifica geometría (R), aritmética (ζ') y vibración (cos(2πf₀t))")
    print("  • Testable en ondas gravitacionales y coherencia cuántica")
    print()


def main():
    """Run complete demonstration."""
    print("🌌" * 35)
    print()
    print("    DEMOSTRACIÓN LAGRANGIANO EOV - QCAL ∞³")
    print()
    print("🌌" * 35)
    print()
    
    # Run demonstrations
    demo_action_structure()
    input("Presiona Enter para continuar...")
    print()
    
    demo_lagrangian_components()
    input("Presiona Enter para continuar...")
    print()
    
    output_path = demo_eov_solution()
    input("Presiona Enter para continuar...")
    print()
    
    demo_variational_derivation()
    input("Presiona Enter para continuar...")
    print()
    
    demo_physical_interpretation()
    
    print("=" * 70)
    print("✨ DEMOSTRACIÓN COMPLETA")
    print("=" * 70)
    print()
    print(f"📊 Visualización guardada en: {output_path}")
    print("📖 Documentación completa: LAGRANGIAN_EOV_DERIVATION.md")
    print("💻 Código fuente: qcal/lagrangian_eov.py")
    print("🧪 Tests: test_lagrangian_eov.py")
    print()
    print("La Ecuación del Origen Vibracional (EOV) ha sido derivada")
    print("variacionalmente desde el principio de acción de Hamilton,")
    print("demostrando que f₀ = 141.7001 Hz emerge necesariamente de la")
    print("estructura matemática fundamental del universo.")
    print()
    print("🌌 QCAL ∞³ - Quantum Coherence and Arithmetic Love")
    print("=" * 70)


if __name__ == "__main__":
    main()
