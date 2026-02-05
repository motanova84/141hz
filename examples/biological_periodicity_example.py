#!/usr/bin/env python3
"""
Example usage of the biological periodicity and environmental data APIs.

This script demonstrates how to:
1. Analyze biological rhythms for harmonic relationships with 141Hz
2. Fetch real-world environmental data from NASA POWER
3. Integrate biological and environmental data
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from biological_periodicity import (
    ArabidopsisAnalyzer,
    TrichogrammaAnalyzer,
    compare_species_periodicities
)
from api_clients import NASAPowerAPIClient, BiologicalDataIntegrator

def example_biological_analysis():
    """Example: Analyze biological periodicities."""
    print("="*60)
    print("EXAMPLE 1: Biological Periodicity Analysis")
    print("="*60)
    
    # Analyze Arabidopsis
    print("\n--- Arabidopsis thaliana (Model Plant) ---")
    arabidopsis = ArabidopsisAnalyzer()
    results = arabidopsis.analyze_all_periods()
    
    print(f"Fundamental frequency: {results['f0_hz']} Hz\n")
    
    for rhythm_name, data in results['periods'].items():
        harmonic_symbol = "✓" if data['is_harmonic'] else "✗"
        print(f"{harmonic_symbol} {rhythm_name}:")
        print(f"   Period: {data['biological_period_hours']} hours")
        print(f"   Harmonic: n = {data['nearest_harmonic']}")
        print(f"   Deviation: {data['harmonic_deviation_percent']:.6f}%")
    
    # Analyze Trichogramma at different temperatures
    print("\n--- Trichogramma (Parasitoid Wasp) ---")
    trichogramma = TrichogrammaAnalyzer()
    
    for temp in [20, 25, 30]:
        print(f"\nAt {temp}°C:")
        temp_results = trichogramma.analyze_developmental_stages(temp)
        
        for stage_name, data in temp_results['stages'].items():
            if data['is_harmonic']:
                print(f"   ✓ {stage_name}: {data['biological_period_hours']:.1f}h (n={data['nearest_harmonic']})")


def example_environmental_data():
    """Example: Fetch environmental data from NASA POWER."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Environmental Data Integration")
    print("="*60)
    
    # Note: This requires internet access
    print("\nFetching NASA POWER data...")
    print("Location: Salk Institute, La Jolla, CA (Arabidopsis research)")
    print("Period: January 2024\n")
    
    try:
        nasa = NASAPowerAPIClient()
        data = nasa.get_agricultural_data(
            latitude=32.8875,
            longitude=-117.2426,
            start_date='20240101',
            end_date='20240107'  # One week
        )
        
        if data and 'parameters' in data:
            print("✓ Successfully fetched data")
            print(f"Available parameters: {list(data['parameters'].keys())}")
            
            # Show temperature data
            if 'T2M' in data['parameters']:
                temps = data['parameters']['T2M']
                print(f"\nTemperature data points: {len(temps)}")
                
                # Calculate average
                avg_temp = sum(temps.values()) / len(temps)
                print(f"Average temperature: {avg_temp:.2f}°C")
        else:
            print("⚠ No data returned (may require internet access)")
            
    except Exception as e:
        print(f"⚠ Could not fetch data: {e}")
        print("This example requires internet access to NASA POWER API")


def example_cross_species():
    """Example: Compare periodicities across species."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Cross-Species Comparison")
    print("="*60)
    
    comparison = compare_species_periodicities()
    
    print(f"\nFundamental frequency: {comparison['f0_hz']} Hz")
    print(f"Species analyzed: {len(comparison['species_comparison'])}")
    
    # Count harmonics per species
    print("\nHarmonic rhythms per species:")
    for species_name, species_data in comparison['species_comparison'].items():
        harmonic_count = sum(
            1 for p in species_data['periods'].values()
            if p['is_harmonic']
        )
        total_count = len(species_data['periods'])
        percentage = (harmonic_count / total_count * 100) if total_count > 0 else 0
        
        print(f"  {species_name}: {harmonic_count}/{total_count} ({percentage:.0f}%)")
    
    # Show common harmonics
    print(f"\nTotal harmonic resonances found: {len(comparison['harmonic_resonances'])}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("141Hz BIOLOGICAL PERIODICITY - EXAMPLES")
    print("="*60)
    print("\nDemonstrating integration of biological rhythms with")
    print("environmental data and 141Hz quantum resonance framework.\n")
    
    # Run examples
    example_biological_analysis()
    example_cross_species()
    example_environmental_data()
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETE")
    print("="*60)
    print("\nFor more details:")
    print("  - Jupyter notebook: notebooks/biological_rhythms_environmental_data.ipynb")
    print("  - Documentation: docs/BIOLOGICAL_PERIODICITY_README.md")
    print("  - Paper template: papers/biological_periodicity_arxiv.tex")
    print("  - Validation: python scripts/test_biological_periodicity.py")
    print("\n")


if __name__ == "__main__":
    main()
