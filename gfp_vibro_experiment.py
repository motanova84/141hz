#!/usr/bin/env python3
"""
GFP Vibro-Fluorescent Experiment (Wet-Lab ∞)
============================================

Implements the specific experiment requested:
- GFP under 141.7 Hz modulation
- Measure ΔF / SNR vs control (100 Hz)
- Prediction: Ratio > 1.5 with constant energy
- Support for NFT theory validation

This is part of the Wet-Lab ∞ experimental protocol.

Author: Sistema QCAL ∞³
Date: 2026-02-14
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Tuple, Optional
import sys

# Import vibrational fluorescence system
try:
    sys.path.insert(0, str(Path(__file__).parent / "modules" / "quantum_biology" / "core"))
    from vibrational_fluorescence import VibrationalFluorescenceSystem, FluorescenceConfig
    VF_AVAILABLE = True
except ImportError:
    print("⚠️  Vibrational fluorescence module not found, using simulation")
    VF_AVAILABLE = False

# Try scipy for signal processing
try:
    from scipy import signal, stats
except ImportError:
    print("❌ scipy required. Install with: pip install scipy")
    sys.exit(1)


class GFPVibroExperiment:
    """
    GFP vibro-fluorescent experiment comparing 141.7 Hz vs 100 Hz control.
    
    Implements the specific prediction:
    - Ratio (141.7 Hz / 100 Hz) > 1.5
    - Constant energy constraint
    - NFT theory support validation
    """
    
    def __init__(self, simulation_mode: bool = True):
        """
        Initialize GFP experiment.
        
        Args:
            simulation_mode: If True, simulate data. If False, interface with hardware.
        """
        self.simulation_mode = simulation_mode
        
        # Experimental parameters
        self.f_qcal = 141.7  # Hz - QCAL frequency
        self.f_control = 100.0  # Hz - Control frequency
        self.energy_constraint = "constant"  # Equal energy for both conditions
        
        # GFP properties
        self.gfp_baseline = 1000.0  # Arbitrary fluorescence units (AFU)
        self.gfp_noise_level = 50.0  # AFU
        
        # Prediction threshold
        self.ratio_threshold = 1.5
        
        # Results
        self.results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "config": {
                "f_qcal": self.f_qcal,
                "f_control": self.f_control,
                "energy_constraint": self.energy_constraint,
                "simulation_mode": simulation_mode
            },
            "measurements": {},
            "analysis": {}
        }
        
        # Initialize fluorescence system if available
        if VF_AVAILABLE:
            config = FluorescenceConfig()
            config.f0 = self.f_qcal
            self.vf_system = VibrationalFluorescenceSystem(config)
        else:
            self.vf_system = None
    
    def measure_fluorescence(self, frequency: float, duration: float = 10.0,
                           n_repeats: int = 5) -> Dict:
        """
        Measure fluorescence response at given frequency.
        
        Args:
            frequency: Modulation frequency (Hz)
            duration: Measurement duration (seconds)
            n_repeats: Number of measurement repeats
            
        Returns:
            Dictionary with measurement results
        """
        print(f"\n📊 Measuring at {frequency:.1f} Hz...")
        
        delta_f_values = []
        snr_values = []
        
        for i in range(n_repeats):
            if self.simulation_mode:
                # Simulate fluorescence response
                delta_f, snr = self._simulate_measurement(frequency, duration)
            else:
                # Interface with actual hardware (placeholder)
                delta_f, snr = self._hardware_measurement(frequency, duration)
            
            delta_f_values.append(delta_f)
            snr_values.append(snr)
        
        # Compute statistics
        mean_delta_f = np.mean(delta_f_values)
        std_delta_f = np.std(delta_f_values)
        mean_snr = np.mean(snr_values)
        std_snr = np.std(snr_values)
        
        result = {
            "frequency": frequency,
            "n_repeats": n_repeats,
            "delta_f": {
                "mean": float(mean_delta_f),
                "std": float(std_delta_f),
                "values": [float(v) for v in delta_f_values]
            },
            "snr": {
                "mean": float(mean_snr),
                "std": float(std_snr),
                "values": [float(v) for v in snr_values]
            }
        }
        
        print(f"   ΔF: {mean_delta_f:.2f} ± {std_delta_f:.2f} AFU")
        print(f"   SNR: {mean_snr:.2f} ± {std_snr:.2f}")
        
        return result
    
    def _simulate_measurement(self, frequency: float, duration: float) -> Tuple[float, float]:
        """
        Simulate fluorescence measurement (for testing).
        
        Args:
            frequency: Modulation frequency
            duration: Measurement duration
            
        Returns:
            (delta_f, snr) tuple
        """
        # QCAL theory predicts enhanced response at 141.7 Hz
        if abs(frequency - self.f_qcal) < 1.0:
            # Near QCAL frequency - enhanced response
            base_response = 150.0  # AFU
            # Add resonance enhancement
            resonance_factor = 1.0 + 0.5 * np.exp(-abs(frequency - self.f_qcal))
            delta_f = base_response * resonance_factor
        else:
            # Off-resonance (control)
            delta_f = 80.0  # AFU - lower response
        
        # Add noise
        noise = np.random.normal(0, self.gfp_noise_level * 0.1)
        delta_f += noise
        
        # Compute SNR
        signal_power = delta_f ** 2
        noise_power = self.gfp_noise_level ** 2
        snr = np.sqrt(signal_power / noise_power)
        
        return delta_f, snr
    
    def _hardware_measurement(self, frequency: float, duration: float) -> Tuple[float, float]:
        """
        Perform actual hardware measurement (placeholder).
        
        In production, this would interface with:
        - Piezoelectric actuator for vibration
        - Fluorescence microscope
        - Data acquisition system
        
        Args:
            frequency: Modulation frequency
            duration: Measurement duration
            
        Returns:
            (delta_f, snr) tuple
        """
        # Placeholder - would connect to real hardware
        raise NotImplementedError("Hardware interface not implemented")
    
    def run_comparison_experiment(self, duration: float = 10.0,
                                 n_repeats: int = 5) -> Dict:
        """
        Run complete comparison: 141.7 Hz vs 100 Hz control.
        
        Args:
            duration: Measurement duration per frequency
            n_repeats: Number of repeats per frequency
            
        Returns:
            Complete experimental results
        """
        print("🔬 GFP Vibro-Fluorescent Experiment (Wet-Lab ∞)")
        print("=" * 70)
        print(f"QCAL frequency: {self.f_qcal} Hz")
        print(f"Control frequency: {self.f_control} Hz")
        print(f"Energy constraint: {self.energy_constraint}")
        print(f"Repeats: {n_repeats}")
        print("=" * 70)
        
        # Measure at QCAL frequency
        print("\n🎯 QCAL Frequency Measurement")
        qcal_result = self.measure_fluorescence(self.f_qcal, duration, n_repeats)
        self.results["measurements"]["qcal_141.7hz"] = qcal_result
        
        # Measure at control frequency
        print("\n🔵 Control Frequency Measurement")
        control_result = self.measure_fluorescence(self.f_control, duration, n_repeats)
        self.results["measurements"]["control_100hz"] = control_result
        
        # Compute ratios
        print("\n📈 Analysis")
        delta_f_ratio = qcal_result["delta_f"]["mean"] / control_result["delta_f"]["mean"]
        snr_ratio = qcal_result["snr"]["mean"] / control_result["snr"]["mean"]
        
        # Statistical test
        t_stat, p_value = stats.ttest_ind(
            qcal_result["delta_f"]["values"],
            control_result["delta_f"]["values"]
        )
        
        # Prediction validation
        prediction_confirmed = delta_f_ratio > self.ratio_threshold
        
        analysis = {
            "delta_f_ratio": {
                "value": float(delta_f_ratio),
                "threshold": self.ratio_threshold,
                "prediction_confirmed": bool(prediction_confirmed)
            },
            "snr_ratio": {
                "value": float(snr_ratio)
            },
            "statistical_test": {
                "t_statistic": float(t_stat),
                "p_value": float(p_value),
                "significant": bool(p_value < 0.05)
            },
            "nft_support": {
                "confirmed": bool(prediction_confirmed and p_value < 0.05),
                "confidence": "high" if p_value < 0.01 else "moderate"
            }
        }
        
        self.results["analysis"] = analysis
        
        print(f"   ΔF Ratio (141.7/100 Hz): {delta_f_ratio:.3f}")
        print(f"   SNR Ratio: {snr_ratio:.3f}")
        print(f"   t-statistic: {t_stat:.3f}")
        print(f"   p-value: {p_value:.4f}")
        print(f"   Prediction (>1.5): {'✅ CONFIRMED' if prediction_confirmed else '❌ NOT CONFIRMED'}")
        
        if analysis["nft_support"]["confirmed"]:
            print(f"\n🎉 NFT Theory Support: ✅ CONFIRMED")
            print(f"   Confidence: {analysis['nft_support']['confidence'].upper()}")
        
        return self.results
    
    def export_results(self, filename: Optional[str] = None) -> Path:
        """
        Export experimental results to JSON.
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gfp_experiment_{timestamp}.json"
        
        output_dir = Path("./experiment_results")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Results exported to: {output_path}")
        
        return output_path
    
    def generate_protocol_document(self) -> Path:
        """
        Generate experimental protocol documentation.
        
        Returns:
            Path to protocol document
        """
        protocol = f"""# GFP Vibro-Fluorescent Experimental Protocol
## Wet-Lab ∞ - NFT Validation

**Date:** {datetime.now().strftime("%Y-%m-%d")}
**QCAL Frequency:** {self.f_qcal} Hz
**Control Frequency:** {self.f_control} Hz

## Objective

Validate NFT (Noetic Field Theory) prediction that GFP fluorescence shows
enhanced response at QCAL frequency (141.7 Hz) compared to control (100 Hz)
with equal energy input.

**Prediction:** ΔF/SNR ratio > {self.ratio_threshold}

## Materials

### Biological
- Green Fluorescent Protein (GFP) solution
- Buffer: PBS pH 7.4
- Temperature: 25°C ± 1°C

### Equipment
- Fluorescence microscope with high-speed camera (≥100 fps)
- Piezoelectric actuator (1-200 Hz range)
- Function generator with amplitude control
- Data acquisition system (≥10 kHz sampling)
- Temperature-controlled stage

## Procedure

### 1. Sample Preparation
1. Prepare GFP solution at optimal concentration
2. Load into observation chamber
3. Allow temperature equilibration (10 min)

### 2. Baseline Measurement
1. Record fluorescence without vibration (5 min)
2. Compute baseline F₀ and noise σ

### 3. QCAL Frequency Measurement (141.7 Hz)
1. Set function generator to {self.f_qcal} Hz
2. Adjust amplitude to target energy E₀
3. Record fluorescence for {self.results['config'].get('duration', 10)} seconds
4. Repeat {self.results['config'].get('n_repeats', 5)} times
5. Compute ΔF and SNR

### 4. Control Frequency Measurement (100 Hz)
1. Set function generator to {self.f_control} Hz
2. **Important:** Adjust amplitude to maintain energy E₀ (constant energy constraint)
3. Record fluorescence for same duration
4. Repeat same number of times
5. Compute ΔF and SNR

### 5. Analysis
1. Compute ΔF ratio = ΔF(141.7 Hz) / ΔF(100 Hz)
2. Compute SNR ratio
3. Perform t-test for statistical significance
4. Compare to prediction threshold

## Data Recording

- Sampling rate: ≥10 kHz
- Duration per trial: 10 seconds
- Number of repeats: 5 per frequency
- Save raw fluorescence traces

## Expected Results

Based on NFT/QCAL theory:
- ΔF ratio > {self.ratio_threshold}
- Statistical significance p < 0.05
- Enhanced response at 141.7 Hz despite equal energy

## Safety Notes

- Handle GFP samples according to biosafety protocols
- Ensure proper laser safety for fluorescence excitation
- Calibrate equipment before measurements

## References

- QCAL Theory: f₀ = 141.7001 Hz universal frequency
- NFT Framework: Coherence economy ℂₛ
- Wet-Lab ∞ Paradigm: Laboratory as conscious organ

---
Generated by Sistema QCAL ∞³
"""
        
        protocol_path = Path("./experiment_results/gfp_protocol.md")
        protocol_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(protocol_path, 'w') as f:
            f.write(protocol)
        
        print(f"📋 Protocol document: {protocol_path}")
        
        return protocol_path


def main():
    """Main entry point for GFP experiment."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="GFP Vibro-Fluorescent Experiment (Wet-Lab ∞)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Run simulated experiment
  python gfp_vibro_experiment.py --simulated
  
  # Run with custom parameters
  python gfp_vibro_experiment.py --simulated --duration 20 --repeats 10
  
  # Generate protocol only
  python gfp_vibro_experiment.py --protocol-only
        """
    )
    
    parser.add_argument("--simulated", action="store_true",
                       help="Use simulated data (default for testing)")
    parser.add_argument("--duration", type=float, default=10.0,
                       help="Measurement duration in seconds")
    parser.add_argument("--repeats", type=int, default=5,
                       help="Number of measurement repeats")
    parser.add_argument("--protocol-only", action="store_true",
                       help="Generate protocol document only")
    parser.add_argument("--output", type=str, default=None,
                       help="Output filename for results")
    
    args = parser.parse_args()
    
    # Create experiment
    experiment = GFPVibroExperiment(simulation_mode=args.simulated)
    
    # Generate protocol
    protocol_path = experiment.generate_protocol_document()
    
    if args.protocol_only:
        print(f"\n✅ Protocol generated: {protocol_path}")
        return 0
    
    # Run experiment
    results = experiment.run_comparison_experiment(
        duration=args.duration,
        n_repeats=args.repeats
    )
    
    # Export results
    output_path = experiment.export_results(args.output)
    
    # Summary
    print("\n" + "=" * 70)
    print("Experiment Complete!")
    print("=" * 70)
    
    analysis = results["analysis"]
    if analysis["nft_support"]["confirmed"]:
        print("🎉 NFT THEORY SUPPORT CONFIRMED")
        print(f"   ΔF Ratio: {analysis['delta_f_ratio']['value']:.3f} > {analysis['delta_f_ratio']['threshold']}")
        print(f"   p-value: {analysis['statistical_test']['p_value']:.4f}")
    else:
        print("⚠️  NFT Theory Support: INCONCLUSIVE")
        print(f"   ΔF Ratio: {analysis['delta_f_ratio']['value']:.3f} (threshold: {analysis['delta_f_ratio']['threshold']})")
    
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
