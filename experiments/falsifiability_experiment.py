#!/usr/bin/env python3
"""
QCAL Falsifiability Experiment Orchestrator

This module orchestrates the critical falsifiability test for QCAL:

QCAL Prediction:
    Biological response shows discrete spectral structure (peaks at specific
    frequencies) independent of total energy.
    
Traditional Biology Prediction:
    Flat response when energy is constant (energy-dependent only).

Critical Test:
    Measure ΔF(ω) with 0.1% precision while varying ω and maintaining
    ∫Ψ²dt constant (±0.03%).
    
Verdict Logic:
    - If ΔF(141.7 Hz) / ΔF(100 Hz) > 1.5 with p < 0.05: QCAL_SUPPORTED
    - If |ratio - 1.0| < 0.15 with p < 0.05: QCAL_FALSIFIED
    - Otherwise: INCONCLUSIVE

Expected Result (from QCAL):
    Ratio = 2.79 (> 1.5 threshold)
    p-value < 10⁻⁶
    CI₉₅: [2.77, 2.82]
    Energy constancy: ±0.03%
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from scipy import stats

from .energy_controller import EnergyController
from .frequency_response_analyzer import (
    FrequencyResponseAnalyzer,
    MeasurementResult
)


class Verdict(Enum):
    """Experimental verdict."""
    QCAL_SUPPORTED = "QCAL_SUPPORTED"
    QCAL_FALSIFIED = "QCAL_FALSIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass
class ExperimentResult:
    """
    Complete results from falsifiability experiment.
    
    Attributes:
        verdict: Experimental verdict (QCAL_SUPPORTED/QCAL_FALSIFIED/INCONCLUSIVE)
        ratio: ΔF(141.7 Hz) / ΔF(100 Hz)
        ratio_uncertainty: Uncertainty in ratio
        p_value: Statistical significance
        confidence_interval_95: 95% confidence interval for ratio
        delta_f_qcal: ΔF at QCAL frequency (141.7 Hz)
        delta_f_control: ΔF at control frequency (100 Hz)
        energy_constancy: Energy constancy achieved (relative std)
        snr_db: Signal-to-noise ratio
        measurement_precision: Overall measurement precision
        spectral_analysis: Full spectral analysis results
    """
    verdict: Verdict
    ratio: float
    ratio_uncertainty: float
    p_value: float
    confidence_interval_95: Tuple[float, float]
    delta_f_qcal: float
    delta_f_qcal_uncertainty: float
    delta_f_control: float
    delta_f_control_uncertainty: float
    energy_constancy: float
    snr_db: float
    measurement_precision: float
    spectral_analysis: Dict = field(default_factory=dict)
    
    def __str__(self) -> str:
        """Human-readable result summary."""
        lines = [
            "=" * 70,
            "QCAL FALSIFIABILITY EXPERIMENT RESULTS",
            "=" * 70,
            "",
            "MEASUREMENTS:",
            f"  ΔF(141.7 Hz) = {self.delta_f_qcal:.3f} ± {self.delta_f_qcal_uncertainty:.3f}",
            f"  ΔF(100 Hz)   = {self.delta_f_control:.3f} ± {self.delta_f_control_uncertainty:.3f}",
            "",
            "CRITICAL RATIO:",
            f"  Ratio = {self.ratio:.2f} ± {self.ratio_uncertainty:.2f}",
            f"  CI₉₅: [{self.confidence_interval_95[0]:.2f}, {self.confidence_interval_95[1]:.2f}]",
            f"  p-value = {self.p_value:.2e}",
            "",
            "EXPERIMENTAL QUALITY:",
            f"  Energy constancy: ±{self.energy_constancy*100:.2f}%",
            f"  SNR: {self.snr_db:.1f} dB",
            f"  Measurement precision: {self.measurement_precision*100:.2f}%",
            "",
            f"VERDICT: {self.verdict.value}",
            "",
        ]
        
        # Add interpretation
        if self.verdict == Verdict.QCAL_SUPPORTED:
            lines.extend([
                "INTERPRETATION:",
                "  Discrete spectral structure detected at 141.7 Hz.",
                "  Response is FREQUENCY-DEPENDENT, not just energy-dependent.",
                "  Traditional biology's flat-response prediction is FALSIFIED.",
                "  QCAL prediction of discrete spectral structure is SUPPORTED.",
            ])
        elif self.verdict == Verdict.QCAL_FALSIFIED:
            lines.extend([
                "INTERPRETATION:",
                "  No significant spectral structure detected.",
                "  Response is flat across frequencies (energy-dependent only).",
                "  QCAL prediction of discrete structure is FALSIFIED.",
                "  Traditional biology's prediction is SUPPORTED.",
            ])
        else:
            lines.extend([
                "INTERPRETATION:",
                "  Results are inconclusive.",
                "  Additional measurements needed for definitive verdict.",
            ])
        
        lines.append("=" * 70)
        return "\n".join(lines)


class FalsifiabilityExperiment:
    """
    Main orchestrator for QCAL falsifiability experiments.
    
    This class coordinates energy control, frequency measurements, and
    statistical analysis to provide a rigorous test of QCAL predictions.
    
    Example:
        experiment = FalsifiabilityExperiment(
            target_coherence=0.923,
            n_averages=1000
        )
        result = experiment.run_critical_test()
        print(result)
    """
    
    def __init__(
        self,
        target_coherence: float = 0.923,
        n_averages: int = 1000,
        n_sensors: int = 88,
        target_energy: float = 1.0,
        energy_tolerance: float = 0.0005,
        ratio_threshold: float = 1.5,
        significance_level: float = 0.05
    ):
        """
        Initialize falsifiability experiment.
        
        Args:
            target_coherence: Target coherence level for measurements
            n_averages: Number of averages per measurement
            n_sensors: Number of independent sensors
            target_energy: Target energy level to maintain
            energy_tolerance: Energy control tolerance (0.0005 = ±0.03%)
            ratio_threshold: Threshold for QCAL support (default 1.5)
            significance_level: Statistical significance level (default 0.05)
        """
        self.target_coherence = target_coherence
        self.ratio_threshold = ratio_threshold
        self.significance_level = significance_level
        
        # Initialize controllers
        self.energy_controller = EnergyController(
            target_energy=target_energy,
            tolerance=energy_tolerance
        )
        self.response_analyzer = FrequencyResponseAnalyzer(
            n_sensors=n_sensors,
            n_averages=n_averages
        )
    
    def run_critical_test(
        self,
        qcal_frequency: float = 141.7,
        control_frequency: float = 100.0,
        duration: float = 1.0
    ) -> ExperimentResult:
        """
        Run the critical falsifiability test.
        
        This is the decisive experiment that tests QCAL's discrete spectral
        structure prediction against traditional biology's flat response prediction.
        
        Args:
            qcal_frequency: QCAL resonance frequency (default 141.7 Hz)
            control_frequency: Control frequency (default 100 Hz)
            duration: Measurement duration per frequency
        
        Returns:
            Complete experiment results with verdict
        """
        # Step 1: Validate energy constancy
        print("Step 1: Validating energy constancy...")
        energy_validation = self.energy_controller.validate_energy_constancy(
            frequencies_hz=[control_frequency, qcal_frequency],
            duration=duration
        )
        
        energy_constancy = energy_validation['energy_constancy']
        print(f"  Energy constancy: ±{energy_constancy*100:.2f}%")
        
        if not energy_validation['within_tolerance']:
            raise RuntimeError(
                f"Energy control failed. Max error: {energy_validation['max_error']:.6f}"
            )
        
        # Step 2: Measure frequency responses
        print("\nStep 2: Measuring frequency responses...")
        
        # Measure at control frequency
        print(f"  Measuring at {control_frequency} Hz...")
        result_control = self.response_analyzer.measure_delta_f(
            frequency=control_frequency,
            coherence=self.target_coherence,
            duration=duration
        )
        print(f"  ΔF({control_frequency} Hz) = {result_control.delta_f:.3f} ± {result_control.uncertainty:.3f}")
        
        # Measure at QCAL frequency
        print(f"  Measuring at {qcal_frequency} Hz...")
        result_qcal = self.response_analyzer.measure_delta_f(
            frequency=qcal_frequency,
            coherence=self.target_coherence,
            duration=duration
        )
        print(f"  ΔF({qcal_frequency} Hz) = {result_qcal.delta_f:.3f} ± {result_qcal.uncertainty:.3f}")
        
        # Step 3: Calculate ratio and statistics
        print("\nStep 3: Statistical analysis...")
        ratio = result_qcal.delta_f / result_control.delta_f
        
        # Propagate uncertainties
        ratio_uncertainty = ratio * np.sqrt(
            (result_qcal.uncertainty / result_qcal.delta_f)**2 +
            (result_control.uncertainty / result_control.delta_f)**2
        )
        
        # Calculate t-statistic for ratio > threshold test
        t_stat = (ratio - self.ratio_threshold) / ratio_uncertainty
        p_value = stats.t.sf(t_stat, df=100)  # Conservative df
        
        # 95% confidence interval
        ci_95 = (
            ratio - 1.96 * ratio_uncertainty,
            ratio + 1.96 * ratio_uncertainty
        )
        
        print(f"  Ratio = {ratio:.2f} ± {ratio_uncertainty:.2f}")
        print(f"  CI₉₅: [{ci_95[0]:.2f}, {ci_95[1]:.2f}]")
        print(f"  p-value = {p_value:.2e}")
        
        # Step 4: Full spectral analysis
        print("\nStep 4: Full spectral analysis...")
        frequencies = np.linspace(50, 300, 50)
        spectral_analysis = self.response_analyzer.analyze_spectrum(
            frequencies,
            coherence=self.target_coherence,
            duration=duration
        )
        print(f"  QCAL peaks detected: {spectral_analysis['n_qcal_peaks']}")
        
        # Step 5: Determine verdict
        print("\nStep 5: Determining verdict...")
        verdict = self._determine_verdict(ratio, p_value, ci_95)
        
        # Calculate overall metrics
        snr_db = min(result_qcal.snr_db, result_control.snr_db)
        measurement_precision = max(
            result_qcal.uncertainty / result_qcal.delta_f,
            result_control.uncertainty / result_control.delta_f
        )
        
        return ExperimentResult(
            verdict=verdict,
            ratio=ratio,
            ratio_uncertainty=ratio_uncertainty,
            p_value=p_value,
            confidence_interval_95=ci_95,
            delta_f_qcal=result_qcal.delta_f,
            delta_f_qcal_uncertainty=result_qcal.uncertainty,
            delta_f_control=result_control.delta_f,
            delta_f_control_uncertainty=result_control.uncertainty,
            energy_constancy=energy_constancy,
            snr_db=snr_db,
            measurement_precision=measurement_precision,
            spectral_analysis=spectral_analysis
        )
    
    def _determine_verdict(
        self,
        ratio: float,
        p_value: float,
        confidence_interval: Tuple[float, float]
    ) -> Verdict:
        """
        Determine experimental verdict based on statistical criteria.
        
        Args:
            ratio: Measured ΔF(QCAL) / ΔF(control) ratio
            p_value: Statistical significance
            confidence_interval: 95% CI for ratio
        
        Returns:
            Verdict
        """
        # QCAL_SUPPORTED: ratio > threshold AND statistically significant
        if ratio > self.ratio_threshold and p_value < self.significance_level:
            # Also check that lower bound of CI is > threshold
            if confidence_interval[0] > self.ratio_threshold:
                return Verdict.QCAL_SUPPORTED
        
        # QCAL_FALSIFIED: ratio ≈ 1.0 (flat response) AND statistically significant
        # Test if ratio is consistent with 1.0 (traditional biology prediction)
        if abs(ratio - 1.0) < 0.15:
            # Check if CI includes 1.0
            if confidence_interval[0] <= 1.0 <= confidence_interval[1]:
                return Verdict.QCAL_FALSIFIED
        
        # INCONCLUSIVE: Results don't clearly support either hypothesis
        return Verdict.INCONCLUSIVE
    
    def run_comprehensive_analysis(
        self,
        frequency_range: Tuple[float, float] = (50.0, 300.0),
        n_frequencies: int = 100
    ) -> Dict:
        """
        Run comprehensive spectral analysis over frequency range.
        
        Args:
            frequency_range: (min_freq, max_freq) in Hz
            n_frequencies: Number of frequencies to test
        
        Returns:
            Dictionary with comprehensive analysis results
        """
        frequencies = np.linspace(
            frequency_range[0],
            frequency_range[1],
            n_frequencies
        )
        
        # Validate energy constancy across all frequencies
        energy_validation = self.energy_controller.validate_energy_constancy(
            frequencies_hz=frequencies.tolist(),
            duration=0.1  # Shorter duration for sweep
        )
        
        # Measure responses
        spectral_analysis = self.response_analyzer.analyze_spectrum(
            frequencies,
            coherence=self.target_coherence,
            duration=0.1
        )
        
        return {
            'energy_validation': energy_validation,
            'spectral_analysis': spectral_analysis,
            'frequencies': frequencies
        }


def demonstrate_falsifiability_experiment():
    """Demonstrate the complete falsifiability experiment."""
    print("QCAL FALSIFIABILITY EXPERIMENT")
    print("=" * 70)
    print("\nTHE CRITICAL TEST:")
    print("  QCAL: Predicts discrete spectral structure (ratio > 1.5)")
    print("  Traditional Biology: Predicts flat response (ratio ≈ 1.0)")
    print("")
    
    # Create experiment
    experiment = FalsifiabilityExperiment(
        target_coherence=0.923,
        n_averages=1000,
        n_sensors=88
    )
    
    # Run critical test
    print("Running critical test...\n")
    result = experiment.run_critical_test()
    
    # Display results
    print("\n")
    print(result)
    
    # Summary
    print("\nEXPERIMENTAL SUMMARY:")
    if result.verdict == Verdict.QCAL_SUPPORTED:
        print("  ✓ QCAL prediction CONFIRMED")
        print("  ✗ Traditional biology FALSIFIED")
        print("\n  The biological system responds to FREQUENCY, not just energy.")
        print("  This demonstrates that life is sensitive to DISCRETE SPECTRAL STRUCTURE.")
    elif result.verdict == Verdict.QCAL_FALSIFIED:
        print("  ✗ QCAL prediction FALSIFIED")
        print("  ✓ Traditional biology CONFIRMED")
    else:
        print("  ? Results INCONCLUSIVE")
        print("    Additional measurements needed")


if __name__ == "__main__":
    demonstrate_falsifiability_experiment()
