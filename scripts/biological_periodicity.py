#!/usr/bin/env python3
"""
Biological periodicity analysis for multiple species.

This module extends the 141Hz quantum resonance framework to analyze
periodic behaviors in various biological organisms, particularly:
- Arabidopsis thaliana (circadian rhythms)
- Trichogramma wasps (developmental cycles)
- Other periodic species

References:
- McClung, C.R. (2006). Plant Circadian Rhythms. Plant Cell 18(4): 792-803
- Cônsoli, F.L. & Parra, J.R.P. (1999). Trichogramma biology and development
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime, timedelta


class BiologicalRhythmAnalyzer:
    """Analyze biological rhythms and their potential resonance with 141Hz."""
    
    # Known biological periodicities (in hours)
    KNOWN_PERIODS = {
        'arabidopsis': {
            'circadian': 24.0,  # Circadian clock period
            'ultradian_short': 3.0,  # Short ultradian rhythms
            'ultradian_medium': 8.0,  # Medium ultradian rhythms
            'photoperiod_response': 12.0,  # Light/dark response
        },
        'trichogramma': {
            'egg_larva': 24.0,  # Egg to larva transition (~1 day)
            'larva_pupa': 48.0,  # Larva to pupa (~2 days)
            'pupa_adult': 96.0,  # Pupa to adult (~4 days)
            'complete_cycle': 168.0,  # Complete development (~7 days)
        },
        'human': {
            'circadian': 24.0,
            'ultradian': 1.5,  # REM cycle
            'heart_rate': 1/60.0,  # ~60 bpm
        }
    }
    
    # 141Hz quantum resonance frequency
    F0_HZ = 141.7001
    F0_PERIOD_SEC = 1 / F0_HZ  # ~0.00706 seconds
    
    def __init__(self, species: str = 'arabidopsis'):
        """
        Initialize biological rhythm analyzer.
        
        Args:
            species: Species name ('arabidopsis', 'trichogramma', 'human')
        """
        self.species = species
        self.periods = self.KNOWN_PERIODS.get(species, {})
        
    def calculate_harmonic_relationship(
        self,
        biological_period_hours: float
    ) -> Dict:
        """
        Calculate harmonic relationship between biological period and 141Hz.
        
        The 141Hz frequency corresponds to a period of ~7.06ms. We examine
        if biological periods are harmonic multiples of this fundamental.
        
        Args:
            biological_period_hours: Biological period in hours
            
        Returns:
            Dictionary with harmonic analysis results
        """
        # Convert biological period to seconds
        bio_period_sec = biological_period_hours * 3600
        
        # Calculate frequency
        bio_freq_hz = 1 / bio_period_sec
        
        # Calculate harmonic ratio
        harmonic_ratio = self.F0_HZ / bio_freq_hz
        
        # Find nearest integer harmonic
        nearest_harmonic = round(harmonic_ratio)
        
        # Calculate deviation from perfect harmonic
        harmonic_deviation = abs(harmonic_ratio - nearest_harmonic) / nearest_harmonic
        
        # Expected frequency if perfectly harmonic
        expected_freq = self.F0_HZ / nearest_harmonic
        expected_period_sec = 1 / expected_freq
        expected_period_hours = expected_period_sec / 3600
        
        return {
            'biological_period_hours': biological_period_hours,
            'biological_period_sec': bio_period_sec,
            'biological_freq_hz': bio_freq_hz,
            'f0_hz': self.F0_HZ,
            'f0_period_sec': self.F0_PERIOD_SEC,
            'harmonic_ratio': harmonic_ratio,
            'nearest_harmonic': nearest_harmonic,
            'harmonic_deviation_percent': harmonic_deviation * 100,
            'expected_period_hours': expected_period_hours,
            'is_harmonic': harmonic_deviation < 0.01  # Within 1%
        }
    
    def analyze_all_periods(self) -> Dict:
        """
        Analyze all known periods for the species.
        
        Returns:
            Dictionary with analysis for all periods
        """
        results = {
            'species': self.species,
            'f0_hz': self.F0_HZ,
            'periods': {}
        }
        
        for rhythm_name, period_hours in self.periods.items():
            analysis = self.calculate_harmonic_relationship(period_hours)
            results['periods'][rhythm_name] = analysis
            
        return results
    
    def find_resonant_frequencies(
        self,
        max_harmonic: int = 1000000
    ) -> List[Dict]:
        """
        Find frequencies that are harmonic divisions of 141Hz.
        
        Args:
            max_harmonic: Maximum harmonic to check
            
        Returns:
            List of resonant frequencies with biological relevance
        """
        resonances = []
        
        for n in range(1, max_harmonic + 1):
            freq_hz = self.F0_HZ / n
            period_sec = 1 / freq_hz
            period_hours = period_sec / 3600
            
            # Check if this matches any known biological rhythm
            # (within 1% tolerance)
            for rhythm_name, known_period in self.periods.items():
                deviation = abs(period_hours - known_period) / known_period
                if deviation < 0.01:
                    resonances.append({
                        'harmonic': n,
                        'frequency_hz': freq_hz,
                        'period_hours': period_hours,
                        'period_sec': period_sec,
                        'rhythm_name': rhythm_name,
                        'known_period_hours': known_period,
                        'deviation_percent': deviation * 100
                    })
                    
        return resonances


class ArabidopsisAnalyzer(BiologicalRhythmAnalyzer):
    """Specialized analyzer for Arabidopsis thaliana circadian rhythms."""
    
    def __init__(self):
        super().__init__(species='arabidopsis')
        
    def analyze_gene_expression_periodicity(
        self,
        expression_data: np.ndarray,
        time_points: np.ndarray
    ) -> Dict:
        """
        Analyze gene expression data for periodic patterns.
        
        Args:
            expression_data: Gene expression levels (arbitrary units)
            time_points: Time points in hours
            
        Returns:
            Periodicity analysis results
        """
        # Perform FFT to find dominant frequencies
        from scipy import signal
        
        # Detrend data
        detrended = signal.detrend(expression_data)
        
        # Calculate power spectrum
        freq = np.fft.fftfreq(len(time_points), d=np.mean(np.diff(time_points)))
        power = np.abs(np.fft.fft(detrended))**2
        
        # Find peaks
        peaks, _ = signal.find_peaks(power[1:len(power)//2])
        
        # Get dominant frequencies
        peak_freqs = freq[peaks + 1]
        peak_powers = power[peaks + 1]
        
        # Sort by power
        sorted_idx = np.argsort(peak_powers)[::-1]
        dominant_freqs = peak_freqs[sorted_idx[:5]]  # Top 5 frequencies
        
        # Convert to periods
        periods = 1 / dominant_freqs
        
        results = {
            'dominant_periods_hours': periods.tolist(),
            'dominant_frequencies_hz': dominant_freqs.tolist(),
            'harmonics_with_141hz': []
        }
        
        # Check harmonic relationship with 141Hz
        for period in periods:
            harmonic_analysis = self.calculate_harmonic_relationship(period)
            results['harmonics_with_141hz'].append(harmonic_analysis)
            
        return results


class TrichogrammaAnalyzer(BiologicalRhythmAnalyzer):
    """Specialized analyzer for Trichogramma wasp development cycles."""
    
    def __init__(self):
        super().__init__(species='trichogramma')
        
    def analyze_developmental_stages(
        self,
        temperature_celsius: float = 25.0
    ) -> Dict:
        """
        Analyze developmental stage durations at given temperature.
        
        Trichogramma development is temperature-dependent. This analyzes
        the relationship between development time and 141Hz resonance.
        
        Args:
            temperature_celsius: Ambient temperature
            
        Returns:
            Analysis of developmental stages
        """
        # Temperature coefficient (simplified model)
        # Development rate increases with temperature
        # Base periods are at 25°C
        temp_factor = 1.0 + 0.05 * (temperature_celsius - 25.0)
        
        results = {
            'temperature_celsius': temperature_celsius,
            'stages': {}
        }
        
        for stage_name, base_period in self.periods.items():
            # Adjust period for temperature
            adjusted_period = base_period / temp_factor
            
            # Analyze harmonic relationship
            harmonic_analysis = self.calculate_harmonic_relationship(adjusted_period)
            harmonic_analysis['temperature_adjusted'] = True
            
            results['stages'][stage_name] = harmonic_analysis
            
        return results


def compare_species_periodicities() -> Dict:
    """
    Compare periodicities across multiple species.
    
    Returns:
        Comparison results across species
    """
    species_list = ['arabidopsis', 'trichogramma', 'human']
    
    results = {
        'f0_hz': BiologicalRhythmAnalyzer.F0_HZ,
        'species_comparison': {}
    }
    
    for species in species_list:
        analyzer = BiologicalRhythmAnalyzer(species)
        species_analysis = analyzer.analyze_all_periods()
        results['species_comparison'][species] = species_analysis
        
    # Find common harmonics
    all_harmonics = []
    for species in species_list:
        analyzer = BiologicalRhythmAnalyzer(species)
        for period_name, period_hours in analyzer.periods.items():
            analysis = analyzer.calculate_harmonic_relationship(period_hours)
            if analysis['is_harmonic']:
                all_harmonics.append({
                    'species': species,
                    'rhythm': period_name,
                    'harmonic': analysis['nearest_harmonic']
                })
    
    results['harmonic_resonances'] = all_harmonics
    
    return results


if __name__ == "__main__":
    print("=== Biological Periodicity Analysis ===\n")
    
    # Analyze Arabidopsis
    print("--- Arabidopsis thaliana ---")
    arabidopsis = ArabidopsisAnalyzer()
    arab_results = arabidopsis.analyze_all_periods()
    print(json.dumps(arab_results, indent=2))
    
    print("\n--- Trichogramma ---")
    trichogramma = TrichogrammaAnalyzer()
    trich_results = trichogramma.analyze_developmental_stages(temperature_celsius=25.0)
    print(json.dumps(trich_results, indent=2))
    
    print("\n--- Cross-Species Comparison ---")
    comparison = compare_species_periodicities()
    print(f"Total species analyzed: {len(comparison['species_comparison'])}")
    print(f"Harmonic resonances found: {len(comparison['harmonic_resonances'])}")
