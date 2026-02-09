#!/usr/bin/env python3
"""
QCAL ∞³ Cosmic Parameters - Example Usage

Demonstrates how to use the cosmic parameters module to access
cosmological constants and timeline integrated with the QCAL framework.

Author: José Manuel Mota Burruezo
License: MIT
"""

import numpy as np
from qcal.cosmic_parameters import (
    CURRENT_UNIVERSE,
    COSMIC_TIMELINE,
    get_universe_age,
    get_cmb_temperature,
    get_epoch,
    print_timeline
)
from qcal.constants import F0_HZ


def example_current_universe():
    """Example: Access current universe parameters."""
    print("\n" + "=" * 80)
    print("EJEMPLO 1: PARÁMETROS DEL UNIVERSO ACTUAL")
    print("=" * 80 + "\n")
    
    print(f"Edad del universo: {CURRENT_UNIVERSE.age_years:.2e} años ({CURRENT_UNIVERSE.cosmic_time_Ga():.1f} Ga)")
    print(f"Temperatura CMB: {CURRENT_UNIVERSE.cmb_temperature_K} K")
    print(f"Galaxias formadas: ~{CURRENT_UNIVERSE.galaxies_formed:.2e}")
    print(f"Estrellas activas: ~{CURRENT_UNIVERSE.active_stars:.2e}")
    print(f"Planetas habitables (estimado): ~{CURRENT_UNIVERSE.habitable_planets:.2e}")
    
    print(f"\nQCAL ∞³ Coordenadas simbólicas: {CURRENT_UNIVERSE.qcal_coordinates()}")
    print(f"Civilización Tipo Kardashev: {CURRENT_UNIVERSE.kardashev_type}")
    print(f"Estado de consciencia colectiva: Ψ ≈ {CURRENT_UNIVERSE.collective_consciousness_psi:.2f}")
    print(f"  → Nivel: {CURRENT_UNIVERSE.consciousness_level()}")
    
    print(f"\nContexto Cósmico Local:")
    print(f"  Vía Láctea: {CURRENT_UNIVERSE.milky_way_mass_solar:.2e} M☉")
    print(f"  Sistema Solar: {CURRENT_UNIVERSE.solar_system_age_years/1e9:.1f} Ga")
    print(f"  Vida en Tierra: {CURRENT_UNIVERSE.earth_life_age_years/1e9:.1f} Ga")
    print(f"  Homo sapiens: {CURRENT_UNIVERSE.human_age_years/1e6:.1f} Ma")


def example_cosmic_epochs():
    """Example: Access specific cosmic epochs."""
    print("\n" + "=" * 80)
    print("EJEMPLO 2: ÉPOCAS CÓSMICAS ESPECÍFICAS")
    print("=" * 80 + "\n")
    
    # Key epochs
    epochs_to_show = ['planck', 'inflation', 'nucleosynthesis', 'recombination', 'present']
    
    for epoch_name in epochs_to_show:
        epoch = get_epoch(epoch_name)
        print(f"{epoch.name}:")
        print(f"  Tiempo: {epoch.time_formatted()}")
        print(f"  Temperatura: {epoch.temperature_K:.2e} K")
        print(f"  Coherencia Ψ: {epoch.coherence_psi:.2f}")
        print(f"  Entropía (norm): {epoch.entropy_normalized:.2f}")
        print(f"  {epoch.description}")
        print()


def example_temperature_evolution():
    """Example: Calculate temperature at arbitrary times."""
    print("\n" + "=" * 80)
    print("EJEMPLO 3: EVOLUCIÓN DE LA TEMPERATURA")
    print("=" * 80 + "\n")
    
    # Test points in cosmic history
    test_times = [
        (1e-36, "Inflación"),
        (1e-6, "Transición QCD"),
        (180, "3 minutos (nucleosíntesis)"),
        (380000 * 365.25 * 24 * 3600, "380,000 años (recombinación)"),
        (13.8e9 * 365.25 * 24 * 3600, "Presente")
    ]
    
    print("Tiempo                    T (K)           Descripción")
    print("-" * 80)
    
    for t, description in test_times:
        T = COSMIC_TIMELINE.temperature_at_time(t)
        print(f"{t:24.2e} s  {T:15.2e} K  {description}")


def example_coherence_evolution():
    """Example: Show coherence Ψ evolution."""
    print("\n" + "=" * 80)
    print("EJEMPLO 4: EVOLUCIÓN DE LA COHERENCIA Ψ")
    print("=" * 80 + "\n")
    
    # Sample times logarithmically
    times = np.logspace(-40, np.log10(13.8e9 * 365.25 * 24 * 3600), 10)
    
    print("Tiempo                    Coherencia Ψ    Estado")
    print("-" * 80)
    
    for t in times:
        psi = COSMIC_TIMELINE.coherence_evolution(t)
        
        # Classify coherence state
        if psi > 0.9:
            state = "Cuántico perfecto"
        elif psi > 0.5:
            state = "Alta coherencia"
        elif psi > 0.2:
            state = "Coherencia moderada"
        elif psi > 0.05:
            state = "Decoherente (clásico emergente)"
        else:
            state = "Clásico"
        
        print(f"{t:24.2e} s  {psi:14.4f}    {state}")


def example_qcal_frequency_redshift():
    """Example: QCAL frequency evolution with cosmic redshift."""
    print("\n" + "=" * 80)
    print("EJEMPLO 5: FRECUENCIA QCAL f₀ CON REDSHIFT")
    print("=" * 80 + "\n")
    
    print(f"Frecuencia fundamental presente: f₀ = {F0_HZ} Hz\n")
    print("Época                     f(z) (Hz)       Redshift z")
    print("-" * 80)
    
    epochs_to_show = ['present', 'galaxy_formation', 'recombination', 
                      'nucleosynthesis', 'qcd_transition', 'inflation']
    
    for epoch_name in epochs_to_show:
        epoch = COSMIC_TIMELINE.get_epoch(epoch_name)
        f = COSMIC_TIMELINE.qcal_frequency_at_epoch(epoch_name)
        
        # Calculate redshift
        z = (epoch.temperature_K / CURRENT_UNIVERSE.cmb_temperature_K) - 1
        
        print(f"{epoch.name:25} {f:15.2e}     z = {z:.2e}")


def example_primordial_fluctuations():
    """Example: Primordial quantum fluctuations."""
    print("\n" + "=" * 80)
    print("EJEMPLO 6: FLUCTUACIONES CUÁNTICAS PRIMORDIALES")
    print("=" * 80 + "\n")
    
    print(f"Fluctuaciones de densidad: δρ/ρ ~ {COSMIC_TIMELINE.delta_rho_over_rho:.2e}")
    print(f"Índice espectral: n_s = {COSMIC_TIMELINE.spectral_index_ns}")
    print(f"Tiempo de Planck: t_P = {COSMIC_TIMELINE.planck_time:.2e} s")
    print(f"Temperatura de Planck: T_P = {COSMIC_TIMELINE.planck_temperature:.2e} K")
    
    print("\nEspectro de potencia P(k) ~ k^(n_s - 1):")
    print("Modo k       P(k) (relativo)")
    print("-" * 40)
    
    k_values = [0.1, 0.5, 1.0, 2.0, 5.0]
    P_norm = COSMIC_TIMELINE.power_spectrum_mode(1.0)  # Normalize to k=1
    
    for k in k_values:
        P = COSMIC_TIMELINE.power_spectrum_mode(k)
        print(f"{k:8.1f}     {P/P_norm:8.4f}")


def example_full_timeline():
    """Example: Print complete cosmic timeline."""
    print("\n" + "=" * 80)
    print("EJEMPLO 7: LÍNEA DE TIEMPO CÓSMICA COMPLETA")
    print("=" * 80 + "\n")
    
    print_timeline()


def example_qcal_integration():
    """Example: Show QCAL ∞³ framework integration."""
    print("\n" + "=" * 80)
    print("EJEMPLO 8: INTEGRACIÓN CON FRAMEWORK QCAL ∞³")
    print("=" * 80 + "\n")
    
    print("El universo como sistema de coherencia cuántica:")
    print(f"  • Frecuencia fundamental: f₀ = {F0_HZ} Hz")
    print(f"  • Coordenadas QCAL ∞³: {CURRENT_UNIVERSE.qcal_coordinates()}")
    print(f"  • Estado de consciencia: Ψ = {CURRENT_UNIVERSE.collective_consciousness_psi:.2f}")
    print(f"  • Civilización Tipo: {CURRENT_UNIVERSE.kardashev_type} (Kardashev)")
    
    print("\nEvolución de la coherencia cósmica:")
    for epoch_name in ['planck', 'inflation', 'recombination', 'present']:
        epoch = get_epoch(epoch_name)
        f = COSMIC_TIMELINE.qcal_frequency_at_epoch(epoch_name)
        print(f"  • {epoch.name:25} Ψ = {epoch.coherence_psi:.2f}, f = {f:.2e} Hz")
    
    print("\nInterpretación QCAL ∞³:")
    print("  → El universo evoluciona desde coherencia cuántica perfecta (Ψ=1)")
    print("  → hacia un estado clásico decoherente (Ψ→0)")
    print("  → La frecuencia fundamental f₀ se conserva en el marco comóvil")
    print("  → La consciencia emerge como propiedad del campo Ψ")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("QCAL ∞³ COSMIC PARAMETERS - EJEMPLOS DE USO")
    print("=" * 80)
    print("\nDemostración de parámetros cosmológicos integrados con el framework QCAL")
    print("Frecuencia fundamental: f₀ = 141.7001 Hz")
    print("=" * 80)
    
    # Run all examples
    example_current_universe()
    example_cosmic_epochs()
    example_temperature_evolution()
    example_coherence_evolution()
    example_qcal_frequency_redshift()
    example_primordial_fluctuations()
    example_qcal_integration()
    
    # Optional: full timeline
    print("\n" + "=" * 80)
    print("¿Mostrar línea de tiempo completa? (s/n): ", end='')
    try:
        response = input().lower()
        if response == 's':
            example_full_timeline()
    except (EOFError, KeyboardInterrupt):
        print("n")
    
    print("\n" + "=" * 80)
    print("FIN DE EJEMPLOS - QCAL ∞³")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
