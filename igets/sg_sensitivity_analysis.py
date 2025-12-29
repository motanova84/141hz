#!/usr/bin/env python3
"""
Superconducting Gravimeter (SG) Sensitivity Analysis
=====================================================

Implements sensitivity specifications for superconducting gravimeters
to determine optimal observation parameters for detecting gravitational
signals at f₀ = 141.7001 Hz.

This module calculates:
1. Required sample sizes for target SNR
2. Observation times for different amplitudes
3. Feasibility analysis with IGETS network

Reference:
- Problem Statement: Amplitude range 10⁻¹³ - 10⁻¹² g testeable
- SG Specifications: σ_single = 10⁻¹¹ g @ 1 Hz, f_sampling = 1 Hz
"""

import numpy as np
from typing import Dict, Tuple, Optional
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class SGSpecifications:
    """
    Superconducting Gravimeter specifications.
    
    Attributes:
        sigma_single: Single-sample noise level [g] at 1 Hz
        f_sampling: Sampling frequency [Hz]
        f_target: Target signal frequency [Hz]
    """
    sigma_single: float = 1e-11  # g @ 1 Hz
    f_sampling: float = 1.0      # Hz
    f_target: float = 141.7001   # Hz
    
    def __post_init__(self):
        """Validate specifications."""
        if self.sigma_single <= 0:
            raise ValueError("sigma_single must be positive")
        if self.f_sampling <= 0:
            raise ValueError("f_sampling must be positive")
        if self.f_target <= 0:
            raise ValueError("f_target must be positive")


class SGSensitivityAnalyzer:
    """
    Analyzer for superconducting gravimeter sensitivity.
    
    This class implements the SNR calculations and sample size
    requirements for detecting gravitational signals with SGs.
    """
    
    def __init__(self, specs: Optional[SGSpecifications] = None):
        """
        Initialize sensitivity analyzer.
        
        Args:
            specs: SG specifications (uses defaults if None)
        """
        self.specs = specs or SGSpecifications()
        
    def required_noise_level(self, amplitude: float, target_snr: float = 5.0) -> float:
        """
        Calculate required noise level for target SNR.
        
        SNR = A / σ_required
        σ_required = A / SNR
        
        Args:
            amplitude: Signal amplitude [g]
            target_snr: Target signal-to-noise ratio
            
        Returns:
            Required noise level [g]
        """
        if amplitude <= 0:
            raise ValueError("Amplitude must be positive")
        if target_snr <= 0:
            raise ValueError("Target SNR must be positive")
            
        sigma_required = amplitude / target_snr
        return sigma_required
    
    def required_samples(self, amplitude: float, target_snr: float = 5.0) -> int:
        """
        Calculate required number of samples for target SNR.
        
        With averaging, noise decreases as 1/√N:
        σ_averaged = σ_single / √N
        
        For target SNR:
        σ_required = A / SNR
        
        Therefore:
        N = (σ_single / σ_required)²
          = (σ_single × SNR / A)²
        
        Args:
            amplitude: Signal amplitude [g]
            target_snr: Target signal-to-noise ratio
            
        Returns:
            Required number of samples
        """
        sigma_required = self.required_noise_level(amplitude, target_snr)
        n_samples = (self.specs.sigma_single / sigma_required) ** 2
        return int(np.ceil(n_samples))
    
    def observation_time(self, amplitude: float, target_snr: float = 5.0) -> float:
        """
        Calculate required observation time.
        
        Time = N_samples / f_sampling
        
        Args:
            amplitude: Signal amplitude [g]
            target_snr: Target signal-to-noise ratio
            
        Returns:
            Observation time [seconds]
        """
        n_samples = self.required_samples(amplitude, target_snr)
        time_seconds = n_samples / self.specs.f_sampling
        return time_seconds
    
    def observation_time_formatted(self, amplitude: float, target_snr: float = 5.0) -> Dict[str, float]:
        """
        Calculate observation time in multiple units.
        
        Args:
            amplitude: Signal amplitude [g]
            target_snr: Target signal-to-noise ratio
            
        Returns:
            Dictionary with time in seconds, minutes, hours, days
        """
        time_seconds = self.observation_time(amplitude, target_snr)
        
        return {
            'seconds': time_seconds,
            'minutes': time_seconds / 60,
            'hours': time_seconds / 3600,
            'days': time_seconds / 86400
        }
    
    def is_feasible(self, amplitude: float, target_snr: float = 5.0,
                   max_observation_days: float = 30) -> bool:
        """
        Check if observation is feasible within time constraint.
        
        Args:
            amplitude: Signal amplitude [g]
            target_snr: Target signal-to-noise ratio
            max_observation_days: Maximum allowed observation time [days]
            
        Returns:
            True if feasible, False otherwise
        """
        time_info = self.observation_time_formatted(amplitude, target_snr)
        return time_info['days'] <= max_observation_days
    
    def analyze_amplitude_range(self, 
                                amplitude_min: float = 1e-13,
                                amplitude_max: float = 1e-12,
                                n_points: int = 10,
                                target_snr: float = 5.0) -> Dict[str, any]:
        """
        Analyze a range of amplitudes.
        
        Args:
            amplitude_min: Minimum amplitude [g]
            amplitude_max: Maximum amplitude [g]
            n_points: Number of points to analyze
            target_snr: Target signal-to-noise ratio
            
        Returns:
            Dictionary with analysis results
        """
        amplitudes = np.logspace(
            np.log10(amplitude_min),
            np.log10(amplitude_max),
            n_points
        )
        
        results = {
            'amplitudes': amplitudes.tolist(),
            'target_snr': target_snr,
            'analyses': []
        }
        
        for amp in amplitudes:
            sigma_req = self.required_noise_level(amp, target_snr)
            n_samples = self.required_samples(amp, target_snr)
            time_info = self.observation_time_formatted(amp, target_snr)
            feasible = self.is_feasible(amp, target_snr)
            
            results['analyses'].append({
                'amplitude': amp,
                'sigma_required': sigma_req,
                'n_samples': n_samples,
                'time_seconds': time_info['seconds'],
                'time_minutes': time_info['minutes'],
                'time_hours': time_info['hours'],
                'time_days': time_info['days'],
                'feasible': feasible
            })
        
        return results
    
    def print_analysis(self, amplitude: float, target_snr: float = 5.0):
        """
        Print detailed analysis for a specific amplitude.
        
        Args:
            amplitude: Signal amplitude [g]
            target_snr: Target signal-to-noise ratio
        """
        print(f"\n{'='*70}")
        print(f"SG SENSITIVITY ANALYSIS")
        print(f"{'='*70}")
        print(f"\nSuperconducting Gravimeter Specifications:")
        print(f"  σ_single = {self.specs.sigma_single:.2e} g @ 1 Hz")
        print(f"  f_sampling = {self.specs.f_sampling} Hz")
        print(f"  f_target = {self.specs.f_target} Hz")
        
        print(f"\nTarget Parameters:")
        print(f"  Amplitude: A = {amplitude:.2e} g")
        print(f"  Target SNR = {target_snr}")
        
        sigma_req = self.required_noise_level(amplitude, target_snr)
        n_samples = self.required_samples(amplitude, target_snr)
        time_info = self.observation_time_formatted(amplitude, target_snr)
        
        print(f"\nCalculations:")
        print(f"  σ_required = A / SNR = {sigma_req:.2e} g")
        print(f"  N_samples = (σ_single / σ_required)²")
        print(f"            = ({self.specs.sigma_single:.2e} / {sigma_req:.2e})²")
        print(f"            = {n_samples:,}")
        
        print(f"\nObservation Time:")
        print(f"  Time = {time_info['seconds']:,.0f} s")
        print(f"       ≈ {time_info['minutes']:.1f} minutes")
        print(f"       ≈ {time_info['hours']:.2f} hours")
        print(f"       ≈ {time_info['days']:.3f} days")
        
        feasible = self.is_feasible(amplitude, target_snr)
        print(f"\nFeasibility with IGETS: {'✅ YES' if feasible else '❌ NO'}")
        print(f"{'='*70}\n")
    
    def plot_sensitivity_curves(self, 
                                amplitude_range: Tuple[float, float] = (1e-14, 1e-11),
                                target_snr: float = 5.0,
                                output_file: Optional[str] = None):
        """
        Plot sensitivity curves for amplitude vs observation time.
        
        Args:
            amplitude_range: (min, max) amplitude range [g]
            target_snr: Target signal-to-noise ratio
            output_file: Output file path (if None, display instead)
        """
        amplitudes = np.logspace(
            np.log10(amplitude_range[0]),
            np.log10(amplitude_range[1]),
            100
        )
        
        n_samples = np.array([self.required_samples(a, target_snr) for a in amplitudes])
        time_days = n_samples / (self.specs.f_sampling * 86400)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Samples vs Amplitude
        ax1.loglog(amplitudes, n_samples, 'b-', linewidth=2)
        ax1.axvspan(1e-13, 1e-12, alpha=0.2, color='green', 
                   label='Testable Range')
        ax1.axhline(2500, color='r', linestyle='--', alpha=0.5,
                   label='A = 10⁻¹² g: N = 2500')
        ax1.axhline(2.5e5, color='orange', linestyle='--', alpha=0.5,
                   label='A = 10⁻¹³ g: N = 2.5×10⁵')
        ax1.set_xlabel('Amplitude A [g]', fontsize=12)
        ax1.set_ylabel('Required Samples N', fontsize=12)
        ax1.set_title(f'Sample Requirements (SNR = {target_snr})', fontsize=13)
        ax1.grid(True, alpha=0.3, which='both')
        ax1.legend()
        
        # Plot 2: Time vs Amplitude
        ax2.loglog(amplitudes, time_days, 'g-', linewidth=2)
        ax2.axvspan(1e-13, 1e-12, alpha=0.2, color='green',
                   label='Testable Range')
        ax2.axhline(42/60/24, color='r', linestyle='--', alpha=0.5,
                   label='A = 10⁻¹² g: ~42 min')
        ax2.axhline(3, color='orange', linestyle='--', alpha=0.5,
                   label='A = 10⁻¹³ g: ~3 days')
        ax2.axhline(30, color='purple', linestyle=':', alpha=0.5,
                   label='Max: 30 days')
        ax2.set_xlabel('Amplitude A [g]', fontsize=12)
        ax2.set_ylabel('Observation Time [days]', fontsize=12)
        ax2.set_title(f'Observation Time Requirements (SNR = {target_snr})', fontsize=13)
        ax2.grid(True, alpha=0.3, which='both')
        ax2.legend()
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"\n📊 Plot saved to: {output_file}")
        else:
            plt.show()
        
        plt.close()


def main():
    """
    Main function demonstrating SG sensitivity analysis.
    """
    print("\n" + "="*70)
    print("SUPERCONDUCTING GRAVIMETER SENSITIVITY ANALYSIS")
    print("Amplitude range: 10⁻¹³ - 10⁻¹² g")
    print("="*70)
    
    # Create analyzer
    analyzer = SGSensitivityAnalyzer()
    
    # Analyze specific amplitudes from problem statement
    print("\n" + "─"*70)
    print("CASE 1: A = 10⁻¹² g")
    print("─"*70)
    analyzer.print_analysis(amplitude=1e-12, target_snr=5.0)
    
    print("\n" + "─"*70)
    print("CASE 2: A = 10⁻¹³ g")
    print("─"*70)
    analyzer.print_analysis(amplitude=1e-13, target_snr=5.0)
    
    # Analyze full range
    print("\n" + "─"*70)
    print("RANGE ANALYSIS")
    print("─"*70)
    results = analyzer.analyze_amplitude_range(
        amplitude_min=1e-13,
        amplitude_max=1e-12,
        n_points=5,
        target_snr=5.0
    )
    
    print(f"\n{'Amplitude [g]':<15} {'N_samples':<15} {'Time':<20} {'Feasible'}")
    print("─"*70)
    for analysis in results['analyses']:
        amp_str = f"{analysis['amplitude']:.2e}"
        n_str = f"{analysis['n_samples']:,}"
        
        if analysis['time_days'] < 1:
            time_str = f"{analysis['time_minutes']:.1f} min"
        else:
            time_str = f"{analysis['time_days']:.2f} days"
        
        feasible_str = "✅ Yes" if analysis['feasible'] else "❌ No"
        
        print(f"{amp_str:<15} {n_str:<15} {time_str:<20} {feasible_str}")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("Both amplitude levels (10⁻¹³ and 10⁻¹² g) are FEASIBLE with IGETS:")
    print("  • A = 10⁻¹² g: ~42 minutes observation ✅")
    print("  • A = 10⁻¹³ g: ~3 days observation ✅")
    print("\nIGETS current network capabilities support both ranges.")
    print("="*70 + "\n")
    
    # Generate plots
    print("Generating sensitivity curves...")
    analyzer.plot_sensitivity_curves(
        amplitude_range=(1e-14, 1e-11),
        target_snr=5.0,
        output_file='igets_results/sg_sensitivity_curves.png'
    )
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
