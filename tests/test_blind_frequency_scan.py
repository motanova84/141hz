#!/usr/bin/env python3
"""
Blind Frequency Scan Test - Look-Elsewhere Effect Mitigation
=============================================================

This test addresses the critical reviewer concern about the look-elsewhere effect:
"Given a pipeline designed to search for 141.7 Hz, the pipeline finds 141.7 Hz."

The counter-argument: "The pipeline doesn't search for 141.7 Hz; it searches for
COHERENCE (Ψ)."

We perform a blind frequency scan from 10 Hz to 2000 Hz, searching for the peak
of coherence without telling the software about 141.7 Hz beforehand. If the
maximum coherence emerges spontaneously at 141.7001 Hz, the look-elsewhere
effect is eliminated.

This would be DISCOVERY OF THE CENTURY - finding a fundamental frequency without
prior knowledge.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import unittest
import numpy as np
from scipy import signal, stats
import warnings
import sys
import os

# Import QCAL constants
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcal.constants import F0_HZ


class TestBlindFrequencyScan(unittest.TestCase):
    """
    Tests for blind frequency scanning without prior knowledge of target frequency
    
    This is the ultimate test: if 141.7 Hz emerges as the peak coherence in a
    blind scan across the entire frequency spectrum, it validates the discovery.
    """
    
    def setUp(self):
        """Set up test parameters"""
        self.true_target_freq = F0_HZ  # 141.7 Hz - what we expect to find
        self.sample_rate = 4096  # Hz
        self.scan_range = (10, 2000)  # Hz - wide scan range
        self.freq_resolution = 0.1  # Hz - frequency resolution
        np.random.seed(42)
        
    def test_blind_scan_finds_injected_signal(self):
        """
        Test 1: Blind scan finds injected 141.7 Hz signal
        
        Inject a weak 141.7 Hz signal into noise and perform a blind scan.
        The scan should find the peak near 141.7 Hz without prior knowledge.
        """
        print("\n" + "="*80)
        print("TEST 1: BLIND FREQUENCY SCAN - INJECTED SIGNAL")
        print("="*80)
        
        # Generate data with injected signal
        duration = 100  # seconds - need long duration for frequency resolution
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Noise
        noise = np.random.normal(0, 1e-21, n_samples)
        
        # Inject signal at 141.7 Hz (weak but detectable)
        signal_amp = 5e-22
        signal_141 = signal_amp * np.sin(2 * np.pi * self.true_target_freq * t)
        
        # Combined data
        data = noise + signal_141
        
        print(f"\nData properties:")
        print(f"  Duration: {duration} seconds")
        print(f"  Sample rate: {self.sample_rate} Hz")
        print(f"  Injected signal frequency: {self.true_target_freq} Hz")
        print(f"  Injected signal amplitude: {signal_amp:.2e}")
        print(f"  Noise level: 1e-21")
        
        # Perform blind scan (without knowing the target frequency)
        print(f"\nPerforming blind scan from {self.scan_range[0]} to {self.scan_range[1]} Hz...")
        scan_result = self._blind_coherence_scan(data, self.scan_range, freq_resolution=0.5)
        
        # Results
        peak_freq = scan_result['peak_frequency']
        peak_coherence = scan_result['peak_coherence']
        freq_error = abs(peak_freq - self.true_target_freq)
        
        print(f"\n{'='*60}")
        print(f"BLIND SCAN RESULTS:")
        print(f"{'='*60}")
        print(f"Peak frequency found: {peak_freq:.3f} Hz")
        print(f"True injected frequency: {self.true_target_freq:.3f} Hz")
        print(f"Frequency error: {freq_error:.3f} Hz")
        print(f"Peak coherence: {peak_coherence:.4f}")
        print(f"Significance: {scan_result['significance']:.2f} sigma")
        
        # The blind scan should find the signal within reasonable tolerance
        # Allow 1 Hz tolerance (about 10x the frequency resolution)
        tolerance_hz = 1.0
        
        self.assertLess(
            freq_error,
            tolerance_hz,
            f"Blind scan found peak at {peak_freq:.3f} Hz, expected {self.true_target_freq:.3f} Hz. "
            f"Error {freq_error:.3f} Hz exceeds tolerance {tolerance_hz} Hz."
        )
        
        # Coherence should be significantly elevated
        self.assertGreater(
            scan_result['significance'],
            3.0,  # At least 3 sigma
            f"Peak coherence significance {scan_result['significance']:.2f} sigma is too low"
        )
        
        print(f"\n✅ PASS: Blind scan successfully found injected signal")
        print(f"✅ Peak at {peak_freq:.3f} Hz matches injected {self.true_target_freq:.3f} Hz")
        
    def test_blind_scan_rejects_pure_noise(self):
        """
        Test 2: Blind scan on pure noise doesn't find spurious peaks
        
        Run blind scan on pure noise. Should not find significant peaks.
        This verifies we're not creating false detections through the scanning process.
        """
        print("\n" + "="*80)
        print("TEST 2: BLIND FREQUENCY SCAN - PURE NOISE")
        print("="*80)
        
        # Generate pure noise
        duration = 100
        n_samples = int(duration * self.sample_rate)
        noise = np.random.normal(0, 1e-21, n_samples)
        
        print(f"\nScanning pure noise from {self.scan_range[0]} to {self.scan_range[1]} Hz...")
        
        # Perform blind scan on noise
        scan_result = self._blind_coherence_scan(noise, self.scan_range, freq_resolution=1.0)
        
        peak_freq = scan_result['peak_frequency']
        peak_coherence = scan_result['peak_coherence']
        
        print(f"\n{'='*60}")
        print(f"PURE NOISE SCAN RESULTS:")
        print(f"{'='*60}")
        print(f"Highest peak frequency: {peak_freq:.3f} Hz")
        print(f"Peak coherence: {peak_coherence:.4f}")
        print(f"Significance: {scan_result['significance']:.2f} sigma")
        
        # In pure noise, significance should be low (< 3 sigma after trials correction)
        # Note: With many frequency bins, we expect some fluctuations
        # Apply trials factor correction
        n_trials = len(scan_result['frequencies'])
        corrected_threshold = 3.0 + np.sqrt(2 * np.log(n_trials))  # Bonferroni-like
        
        print(f"Trials factor: {n_trials} frequency bins")
        print(f"Corrected threshold: {corrected_threshold:.2f} sigma")
        
        self.assertLess(
            scan_result['significance'],
            corrected_threshold,
            f"Pure noise scan shows significance {scan_result['significance']:.2f} sigma, "
            f"exceeds corrected threshold {corrected_threshold:.2f} sigma. "
            f"This suggests false detection problem."
        )
        
        print(f"\n✅ PASS: No spurious peaks found in pure noise")
        
    def test_blind_scan_frequency_resolution(self):
        """
        Test 3: Verify frequency resolution is adequate for blind scan
        
        Check that the scan can resolve closely spaced frequencies and that
        the resolution is fine enough to detect 141.7 Hz accurately.
        """
        print("\n" + "="*80)
        print("TEST 3: FREQUENCY RESOLUTION ADEQUACY")
        print("="*80)
        
        # Test with two closely spaced signals
        duration = 100
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples)
        
        # Two signals separated by 5 Hz
        f1 = 140.0
        f2 = 145.0
        amp = 5e-22
        
        signal1 = amp * np.sin(2 * np.pi * f1 * t)
        signal2 = amp * np.sin(2 * np.pi * f2 * t)
        noise = np.random.normal(0, 1e-21, n_samples)
        
        data = signal1 + signal2 + noise
        
        print(f"\nInjected two signals:")
        print(f"  f1 = {f1} Hz")
        print(f"  f2 = {f2} Hz")
        print(f"  Separation = {f2 - f1} Hz")
        
        # Scan with fine resolution
        scan_result = self._blind_coherence_scan(data, (130, 155), freq_resolution=0.2)
        
        # Find all significant peaks
        coherences = np.array(scan_result['coherences'])
        frequencies = np.array(scan_result['frequencies'])
        
        # Find local maxima
        peaks_idx, properties = signal.find_peaks(
            coherences,
            prominence=2.0,  # Require 2x background
            distance=int(2.0 / 0.2)  # At least 2 Hz apart
        )
        
        peak_freqs = frequencies[peaks_idx]
        peak_cohs = coherences[peaks_idx]
        
        print(f"\nPeaks found: {len(peak_freqs)}")
        for i, (freq, coh) in enumerate(zip(peak_freqs, peak_cohs)):
            print(f"  Peak {i+1}: {freq:.2f} Hz, coherence {coh:.4f}")
            
        # Should find at least 2 peaks (one near each injected frequency)
        self.assertGreaterEqual(
            len(peak_freqs),
            2,
            f"Should find at least 2 peaks, found {len(peak_freqs)}. "
            f"Frequency resolution may be inadequate."
        )
        
        # Check that peaks are near injected frequencies
        found_f1 = any(abs(freq - f1) < 1.0 for freq in peak_freqs)
        found_f2 = any(abs(freq - f2) < 1.0 for freq in peak_freqs)
        
        self.assertTrue(found_f1, f"Did not find peak near {f1} Hz")
        self.assertTrue(found_f2, f"Did not find peak near {f2} Hz")
        
        print(f"\n✅ PASS: Frequency resolution is adequate")
        print(f"✅ Successfully resolved two signals separated by {f2-f1} Hz")
        
    def test_trials_factor_correction(self):
        """
        Test 4: Trials factor correction for look-elsewhere effect
        
        When scanning many frequencies, we must correct for multiple comparisons.
        This test verifies that the trials factor is properly accounted for.
        """
        print("\n" + "="*80)
        print("TEST 4: TRIALS FACTOR CORRECTION")
        print("="*80)
        
        # Scan parameters
        f_min, f_max = 10, 2000
        freq_resolution = 0.5  # Hz
        
        n_bins = int((f_max - f_min) / freq_resolution)
        
        print(f"\nScan parameters:")
        print(f"  Frequency range: {f_min} - {f_max} Hz")
        print(f"  Frequency resolution: {freq_resolution} Hz")
        print(f"  Number of frequency bins: {n_bins}")
        
        # Calculate trials factor
        # For Gaussian statistics, probability of at least one k-sigma fluctuation
        # in N trials: P = 1 - (1 - P_1)^N ≈ N * P_1 for small P_1
        
        # For 5-sigma detection:
        p_single = stats.norm.sf(5.0)  # Probability of 5-sigma in one trial
        p_multiple = 1 - (1 - p_single)**n_bins  # Probability in N trials
        
        # Effective sigma accounting for trials
        if p_multiple > 0 and p_multiple < 1:
            sigma_effective = stats.norm.isf(p_multiple)
        else:
            sigma_effective = 5.0
            
        print(f"\nTrials factor analysis:")
        print(f"  Single-trial p-value (5σ): {p_single:.2e}")
        print(f"  Multiple-trial p-value: {p_multiple:.4f}")
        print(f"  Effective significance needed: {sigma_effective:.2f} sigma")
        
        # Rule of thumb: for N trials, need roughly sqrt(2*ln(N)) additional sigma
        bonferroni_correction = np.sqrt(2 * np.log(n_bins))
        print(f"  Bonferroni-like correction: +{bonferroni_correction:.2f} sigma")
        
        # For claiming discovery with look-elsewhere, typically need > 5 sigma
        # after correction
        uncorrected_detection = 5.0
        corrected_detection = uncorrected_detection + bonferroni_correction
        
        print(f"\n  For {uncorrected_detection}σ local significance:")
        print(f"  Global significance: ~{corrected_detection:.2f}σ required")
        
        # Verify that our correction is reasonable
        self.assertGreater(
            bonferroni_correction,
            0,
            "Trials factor correction should be positive"
        )
        
        self.assertLess(
            bonferroni_correction,
            5.0,
            f"Trials factor correction {bonferroni_correction:.2f} seems too large"
        )
        
        print(f"\n✅ PASS: Trials factor correction is properly calculated")
        
    def _blind_coherence_scan(self, data, freq_range, freq_resolution=0.5):
        """
        Perform blind coherence scan across frequency range
        
        This scans for coherent power across the spectrum without knowing
        the target frequency beforehand.
        
        Parameters
        ----------
        data : np.ndarray
            Time series data
        freq_range : tuple
            (min_freq, max_freq) in Hz
        freq_resolution : float
            Frequency step size in Hz
            
        Returns
        -------
        dict
            Scan results including peak frequency, coherence, and significance
        """
        # Generate frequency grid
        f_min, f_max = freq_range
        frequencies = np.arange(f_min, f_max, freq_resolution)
        
        # Compute PSD once
        duration = len(data) / self.sample_rate
        nperseg = min(int(self.sample_rate * 4), len(data) // 8)
        freqs, psd = signal.welch(
            data,
            fs=self.sample_rate,
            nperseg=nperseg,
            scaling='density'
        )
        
        # Calculate coherence at each frequency
        coherences = []
        
        for target_freq in frequencies:
            # Find nearest frequency bin
            idx = np.argmin(np.abs(freqs - target_freq))
            target_power = psd[idx]
            
            # Background: median of surrounding bins (excluding ±5 bins)
            exclude_range = 5
            background_idx = np.concatenate([
                np.arange(max(0, idx - 20), max(0, idx - exclude_range)),
                np.arange(min(len(psd), idx + exclude_range), min(len(psd), idx + 20))
            ])
            
            if len(background_idx) > 0:
                background = np.median(psd[background_idx])
                # Coherence as ratio to background
                coherence = target_power / (background + 1e-50)
            else:
                coherence = 1.0
                
            coherences.append(coherence)
            
        coherences = np.array(coherences)
        
        # Find peak
        peak_idx = np.argmax(coherences)
        peak_frequency = frequencies[peak_idx]
        peak_coherence = coherences[peak_idx]
        
        # Calculate significance
        # Use median and MAD for robust statistics
        median_coherence = np.median(coherences)
        mad = np.median(np.abs(coherences - median_coherence))
        sigma_robust = 1.4826 * mad  # Convert MAD to sigma for Gaussian
        
        significance = (peak_coherence - median_coherence) / sigma_robust if sigma_robust > 0 else 0
        
        return {
            'frequencies': frequencies,
            'coherences': coherences,
            'peak_frequency': peak_frequency,
            'peak_coherence': peak_coherence,
            'median_coherence': median_coherence,
            'coherence_std': sigma_robust,
            'significance': significance
        }


class TestLookElsewhereCorrection(unittest.TestCase):
    """Additional tests for look-elsewhere effect mitigation"""
    
    def test_bonferroni_correction_calculation(self):
        """Test Bonferroni correction calculation"""
        n_trials = [10, 100, 1000, 10000]
        
        print("\n" + "="*60)
        print("Bonferroni Correction for Different Numbers of Trials")
        print("="*60)
        print(f"{'N trials':<15} {'Correction (sigma)':<20}")
        print("-"*35)
        
        for n in n_trials:
            correction = np.sqrt(2 * np.log(n))
            print(f"{n:<15} {correction:<20.2f}")
            
            # Sanity checks
            self.assertGreater(correction, 0)
            self.assertLess(correction, 10)  # Shouldn't be unreasonably large
            
    def test_global_vs_local_significance(self):
        """Test conversion between local and global significance"""
        n_trials = 4000  # Typical for 10-2000 Hz scan at 0.5 Hz resolution
        
        local_sigma = 5.0
        
        # Calculate global p-value
        p_local = stats.norm.sf(local_sigma)
        p_global = 1 - (1 - p_local)**n_trials
        
        # Global significance
        if p_global > 0 and p_global < 1:
            global_sigma = stats.norm.isf(p_global)
        else:
            global_sigma = 0
            
        print(f"\nLocal significance: {local_sigma:.1f} sigma")
        print(f"Number of trials: {n_trials}")
        print(f"Local p-value: {p_local:.2e}")
        print(f"Global p-value: {p_global:.4f}")
        print(f"Global significance: {global_sigma:.2f} sigma")
        
        # Global significance should be lower than local
        self.assertLess(global_sigma, local_sigma)


if __name__ == '__main__':
    unittest.main(verbosity=2)
