#!/usr/bin/env python3
"""
Bayes Factor Translation Test
==============================

This test addresses the concern that "ICV is not an accepted statistic."

We translate the ICV (Internal Coherence Value) metric to Bayes Factors, which
are the standard language of peer review in gravitational wave physics.

Bayes Factors compare the evidence for two models:
- H0: Standard GR Model + Noise (null hypothesis)
- H1: Standard GR Model + QCAL 141Hz Signal (alternative hypothesis)

The Bayes Factor B01 = P(data|H0) / P(data|H1)
Or equivalently, Log Evidence Ratio = log(P(data|H0)) - log(P(data|H1))

Interpretation (Kass & Raftery 1995):
- |log B| < 1: Not worth mentioning
- 1 < |log B| < 3: Positive evidence
- 3 < |log B| < 5: Strong evidence  
- |log B| > 5: Very strong evidence

This makes our ICV findings directly comparable to standard GW analysis.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import unittest
import numpy as np
from scipy import signal, stats, special
import warnings
import sys
import os

# Import QCAL constants
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcal.constants import F0_HZ


class TestBayesFactorTranslation(unittest.TestCase):
    """
    Tests for translating ICV to Bayes Factors
    
    This makes the QCAL findings compatible with standard peer review
    in gravitational wave physics.
    """
    
    def setUp(self):
        """Set up test parameters"""
        self.target_freq = F0_HZ  # 141.7 Hz
        self.sample_rate = 4096  # Hz
        np.random.seed(42)
        
    def test_icv_to_bayes_factor_conversion(self):
        """
        Test: ICV can be converted to Bayes Factor
        
        Verify that we can compute a meaningful Bayes Factor from the
        coherence measurements used in ICV.
        """
        print("\n" + "="*80)
        print("TEST: ICV TO BAYES FACTOR CONVERSION")
        print("="*80)
        
        # Simulate a signal with known properties
        duration = 10  # seconds
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Pure noise case
        noise = np.random.normal(0, 1e-21, n_samples)
        
        # Signal + noise case (weak 141.7 Hz signal)
        signal_amplitude = 5e-22  # Weak signal
        signal_component = signal_amplitude * np.sin(2 * np.pi * self.target_freq * t)
        signal_plus_noise = noise + signal_component
        
        # Calculate ICV for both cases
        icv_noise = self._calculate_icv(noise)
        icv_signal = self._calculate_icv(signal_plus_noise)
        
        # Convert to Bayes Factors
        bf_noise = self._icv_to_bayes_factor(icv_noise)
        bf_signal = self._icv_to_bayes_factor(icv_signal)
        
        print(f"\nPure Noise:")
        print(f"  ICV: {icv_noise:.4f}")
        print(f"  log(BF): {bf_noise['log_bayes_factor']:.2f}")
        print(f"  Interpretation: {bf_noise['interpretation']}")
        
        print(f"\nSignal + Noise:")
        print(f"  ICV: {icv_signal:.4f}")
        print(f"  log(BF): {bf_signal['log_bayes_factor']:.2f}")
        print(f"  Interpretation: {bf_signal['interpretation']}")
        
        # Signal should have higher Bayes Factor than noise
        self.assertGreater(
            bf_signal['log_bayes_factor'],
            bf_noise['log_bayes_factor'],
            "Signal+noise should have higher Bayes Factor than pure noise"
        )
        
        # Noise-only should have BF close to 0 (no preference for either model)
        self.assertLess(
            abs(bf_noise['log_bayes_factor']),
            1.0,
            f"Noise-only log(BF) = {bf_noise['log_bayes_factor']:.2f} should be close to 0"
        )
        
        print(f"\n✅ PASS: ICV to Bayes Factor conversion works correctly")
        
    def test_model_comparison_noise_vs_signal(self):
        """
        Test: Model comparison using Bayes Factors
        
        Compare two models:
        - M0: Data = GR waveform + Gaussian noise
        - M1: Data = GR waveform + 141.7 Hz component + Gaussian noise
        
        Calculate the Bayes Factor to determine which model is preferred.
        """
        print("\n" + "="*80)
        print("TEST: MODEL COMPARISON - NOISE VS SIGNAL")
        print("="*80)
        
        duration = 10
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Generate synthetic data with known signal
        noise_level = 1e-21
        signal_amplitude = 3e-22  # SNR ~ 3
        
        noise = np.random.normal(0, noise_level, n_samples)
        signal_141 = signal_amplitude * np.sin(2 * np.pi * self.target_freq * t)
        
        # Simplified GR waveform (chirp)
        t_merger = duration / 2
        chirp_amp = 5e-21 * np.exp(-((t - t_merger) / 0.5)**2)
        chirp_freq = 100 + 50 * (t / duration)  # Sweeping frequency
        gr_waveform = chirp_amp * np.sin(2 * np.pi * chirp_freq * t)
        
        data = gr_waveform + signal_141 + noise
        
        # Calculate log-evidence for each model
        log_evidence_m0 = self._calculate_log_evidence(data, include_141hz=False)
        log_evidence_m1 = self._calculate_log_evidence(data, include_141hz=True)
        
        # Bayes Factor: B10 = P(data|M1) / P(data|M0)
        log_bf_10 = log_evidence_m1 - log_evidence_m0
        
        print(f"\nModel 0 (GR + Noise):")
        print(f"  log(Evidence): {log_evidence_m0:.2f}")
        
        print(f"\nModel 1 (GR + 141.7Hz + Noise):")
        print(f"  log(Evidence): {log_evidence_m1:.2f}")
        
        print(f"\nBayes Factor:")
        print(f"  log(B10): {log_bf_10:.2f}")
        print(f"  Interpretation: {self._interpret_bayes_factor(log_bf_10)}")
        
        # Since we injected a 141.7 Hz signal, M1 should be preferred
        self.assertGreater(
            log_bf_10,
            0,
            f"Model with 141.7 Hz component should be preferred, got log(B10)={log_bf_10:.2f}"
        )
        
        # For SNR~3 signal, we expect positive to strong evidence (log BF > 1)
        self.assertGreater(
            log_bf_10,
            1.0,
            f"With injected signal, should have log(BF) > 1, got {log_bf_10:.2f}"
        )
        
        print(f"\n✅ PASS: Model comparison correctly identifies signal presence")
        
    def test_bayes_factor_interpretation_levels(self):
        """
        Test: Bayes Factor interpretation follows Kass & Raftery scale
        
        Verify that our interpretation function correctly categorizes
        different levels of evidence.
        """
        print("\n" + "="*80)
        print("TEST: BAYES FACTOR INTERPRETATION LEVELS")
        print("="*80)
        
        test_cases = [
            (0.5, "Not worth mentioning"),
            (1.5, "Positive evidence"),
            (3.5, "Strong evidence"),
            (5.5, "Very strong evidence"),
            (-0.5, "Not worth mentioning"),
            (-1.5, "Positive evidence"),
            (-3.5, "Strong evidence"),
            (-5.5, "Very strong evidence"),
        ]
        
        print(f"\n{'log(BF)':<12} {'Interpretation':<30}")
        print(f"{'-'*42}")
        
        for log_bf, expected_level in test_cases:
            interpretation = self._interpret_bayes_factor(log_bf)
            print(f"{log_bf:>8.1f}    {interpretation:<30}")
            
            # Check that interpretation matches expected level
            self.assertIn(
                expected_level.lower(),
                interpretation.lower(),
                f"log(BF)={log_bf} should be interpreted as '{expected_level}'"
            )
            
        print(f"\n✅ PASS: Bayes Factor interpretation is correct")
        
    def test_sensitivity_to_signal_strength(self):
        """
        Test: Bayes Factor scales appropriately with signal strength
        
        As signal amplitude increases, Bayes Factor should increase.
        This verifies the conversion is physically meaningful.
        """
        print("\n" + "="*80)
        print("TEST: SENSITIVITY TO SIGNAL STRENGTH")
        print("="*80)
        
        duration = 10
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples)
        
        noise = np.random.normal(0, 1e-21, n_samples)
        
        # Test different signal amplitudes
        amplitudes = [0, 1e-22, 3e-22, 5e-22, 10e-22]
        log_bfs = []
        
        print(f"\n{'Amplitude (strain)':<20} {'log(BF)':<15} {'Interpretation':<30}")
        print(f"{'-'*65}")
        
        for amp in amplitudes:
            signal = amp * np.sin(2 * np.pi * self.target_freq * t)
            data = noise + signal
            
            log_evidence_no_signal = self._calculate_log_evidence(data, include_141hz=False)
            log_evidence_with_signal = self._calculate_log_evidence(data, include_141hz=True)
            
            log_bf = log_evidence_with_signal - log_evidence_no_signal
            log_bfs.append(log_bf)
            
            interpretation = self._interpret_bayes_factor(log_bf)
            print(f"{amp:.2e}         {log_bf:>8.2f}      {interpretation:<30}")
            
        # Verify monotonic increase (with some tolerance for noise)
        # At least trend should be increasing
        log_bfs = np.array(log_bfs)
        
        # Check that BF generally increases with amplitude
        # (allowing for some fluctuations due to noise)
        trend = np.polyfit(amplitudes, log_bfs, 1)[0]  # Linear fit slope
        
        self.assertGreater(
            trend,
            0,
            f"Bayes Factor should increase with signal amplitude, got trend {trend:.2e}"
        )
        
        print(f"\n✅ PASS: Bayes Factor increases with signal strength (trend = {trend:.2e})")
        
    def _calculate_icv(self, data):
        """
        Calculate Internal Coherence Value (ICV)
        
        Parameters
        ----------
        data : np.ndarray
            Time series data
            
        Returns
        -------
        float
            ICV metric
        """
        # Compute PSD
        nperseg = min(int(self.sample_rate), len(data) // 4)
        freqs, psd = signal.welch(
            data,
            fs=self.sample_rate,
            nperseg=nperseg,
            scaling='density'
        )
        
        # Find power at target frequency
        target_idx = np.argmin(np.abs(freqs - self.target_freq))
        target_power = psd[target_idx]
        
        # Background power (surrounding frequencies)
        low_idx = max(0, target_idx - 10)
        high_idx = min(len(psd), target_idx + 10)
        background_indices = list(range(low_idx, target_idx)) + list(range(target_idx+1, high_idx))
        background_power = np.mean(psd[background_indices])
        
        # ICV as ratio of target to background
        icv = target_power / (background_power + 1e-50)
        
        return icv
        
    def _icv_to_bayes_factor(self, icv):
        """
        Convert ICV to Bayes Factor
        
        This is a simplified conversion. In a full implementation, we would
        use proper Bayesian model comparison with priors.
        
        Parameters
        ----------
        icv : float
            Internal Coherence Value
            
        Returns
        -------
        dict
            Bayes Factor information including log(BF) and interpretation
        """
        # Simple mapping: ICV > 1 suggests signal presence
        # log(BF) ~ log(ICV) for ICV > 1
        # This is a heuristic conversion; rigorous calculation would use
        # full Bayesian evidence calculation
        
        if icv > 1:
            log_bf = np.log(icv)
        else:
            log_bf = -np.log(1/icv) if icv > 0 else -10
            
        interpretation = self._interpret_bayes_factor(log_bf)
        
        return {
            'log_bayes_factor': log_bf,
            'bayes_factor': np.exp(log_bf),
            'interpretation': interpretation
        }
        
    def _calculate_log_evidence(self, data, include_141hz=True):
        """
        Calculate log-evidence for a model
        
        This is a simplified calculation. A full Bayesian analysis would
        include proper priors, marginalization over parameters, etc.
        
        Parameters
        ----------
        data : np.ndarray
            Time series data
        include_141hz : bool
            Whether model includes 141.7 Hz component
            
        Returns
        -------
        float
            Log evidence (log marginal likelihood)
        """
        # Compute residuals under each model
        if include_141hz:
            # Model: data ~ GR + 141.7Hz + noise
            # Fit 141.7 Hz component
            t = np.arange(len(data)) / self.sample_rate
            
            # Simple least squares fit for amplitude and phase
            A_sin = 2 * np.dot(data, np.sin(2 * np.pi * self.target_freq * t)) / len(data)
            A_cos = 2 * np.dot(data, np.cos(2 * np.pi * self.target_freq * t)) / len(data)
            
            # Reconstruct and subtract 141.7 Hz component
            signal_fit = (A_sin * np.sin(2 * np.pi * self.target_freq * t) +
                         A_cos * np.cos(2 * np.pi * self.target_freq * t))
            residuals = data - signal_fit
        else:
            # Model: data ~ GR + noise (no 141.7 Hz)
            residuals = data
            
        # Calculate likelihood under Gaussian noise assumption
        # log p(data|model) = -0.5 * sum((residuals/sigma)^2) - N*log(sigma*sqrt(2*pi))
        
        sigma = np.std(residuals)
        n = len(residuals)
        
        log_likelihood = -0.5 * np.sum((residuals / sigma)**2) - n * np.log(sigma * np.sqrt(2 * np.pi))
        
        # For simplicity, assume flat priors so log evidence ≈ log likelihood
        # In rigorous analysis, would integrate over prior distributions
        log_evidence = log_likelihood
        
        # Occam penalty for model complexity (more complex model is penalized)
        if include_141hz:
            # Additional 2 parameters (amplitude and phase) for 141.7 Hz
            occam_penalty = -np.log(n)  # BIC-like penalty
            log_evidence += occam_penalty
            
        return log_evidence
        
    def _interpret_bayes_factor(self, log_bf):
        """
        Interpret Bayes Factor according to Kass & Raftery (1995) scale
        
        Parameters
        ----------
        log_bf : float
            Natural log of Bayes Factor
            
        Returns
        -------
        str
            Interpretation string
        """
        abs_log_bf = abs(log_bf)
        
        if abs_log_bf < 1:
            strength = "Not worth mentioning"
        elif abs_log_bf < 3:
            strength = "Positive evidence"
        elif abs_log_bf < 5:
            strength = "Strong evidence"
        else:
            strength = "Very strong evidence"
            
        if log_bf > 0:
            direction = "for H1 (signal present)"
        else:
            direction = "for H0 (no signal)"
            
        return f"{strength} {direction}"


class TestBayesianStatistics(unittest.TestCase):
    """Additional tests for Bayesian statistical methods"""
    
    def test_gaussian_likelihood_calculation(self):
        """Test that Gaussian likelihood is calculated correctly"""
        np.random.seed(42)
        
        # Known Gaussian data
        mu = 0
        sigma = 1
        n = 1000
        data = np.random.normal(mu, sigma, n)
        
        # Calculate log likelihood
        log_likelihood = -0.5 * np.sum(((data - mu) / sigma)**2) - n * np.log(sigma * np.sqrt(2 * np.pi))
        
        # Compare with scipy
        scipy_log_likelihood = np.sum(stats.norm.logpdf(data, mu, sigma))
        
        np.testing.assert_almost_equal(
            log_likelihood,
            scipy_log_likelihood,
            decimal=5,
            err_msg="Gaussian likelihood calculation mismatch"
        )
        
    def test_bayes_factor_symmetry(self):
        """Test that B10 = 1/B01"""
        np.random.seed(42)
        
        # Arbitrary log evidences
        log_e0 = -100.5
        log_e1 = -98.3
        
        # B10 = P(D|M1) / P(D|M0)
        log_b10 = log_e1 - log_e0
        
        # B01 = P(D|M0) / P(D|M1)
        log_b01 = log_e0 - log_e1
        
        # Should be negatives
        self.assertAlmostEqual(log_b10, -log_b01, places=10)
        
        # In linear space: B10 * B01 = 1
        b10 = np.exp(log_b10)
        b01 = np.exp(log_b01)
        self.assertAlmostEqual(b10 * b01, 1.0, places=10)


if __name__ == '__main__':
    unittest.main(verbosity=2)
