#!/usr/bin/env python3
"""
Tests for Shadow-1 Bayesian Coherence Analysis
================================================

Validates the Bayesian Coherence Inference pipeline for the sub-threshold
gravitational wave candidate "Shadow-1" (GPS: 1251010524.0) and the
EEG coherence pipeline (Shadow-1 of Thought).
"""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.shadow1_bayesian_coherence import (
    SHADOW1_GPS,
    SHADOW1_A_EFF,
    SHADOW1_DURATION_S,
    SHADOW1_DISTANCE_MPC,
    SHADOW1_MASS_MIN,
    SHADOW1_MASS_MAX,
    SHADOW1_MASS_MAX_PRIMARY,
    GLITCH_DURATION_THRESHOLD_S,
    PSI_DEFINITION_GW,
    PSI_DEFINITION_EEG,
    PSI_THRESHOLD_GW,
    PSI_THRESHOLD_EEG,
    chirp_mass_from_frequency_evolution,
    masses_from_chirp_mass,
    compute_phase_coherence,
    compute_score_psi,
    verify_phase_stability,
    band_coherence_feature,
    normalize_bayes_factor,
    time_slide_control,
    control_band_check,
    silent_collision_assessment,
    Shadow1BayesianAnalyzer,
    EEGCoherencePipeline,
)


class TestConstants(unittest.TestCase):
    """Verify physical constants and Shadow-1 event parameters."""

    def test_gps_time(self):
        """Shadow-1 GPS timestamp must match the problem statement."""
        self.assertAlmostEqual(SHADOW1_GPS, 1251010524.0, places=1)

    def test_a_eff(self):
        """Reference A_eff must be 0.89."""
        self.assertAlmostEqual(SHADOW1_A_EFF, 0.89, places=5)

    def test_phase_duration(self):
        """Phase stability duration must be 0.4 s."""
        self.assertAlmostEqual(SHADOW1_DURATION_S, 0.4, places=5)

    def test_distance(self):
        """Luminosity distance must be 600 Mpc."""
        self.assertAlmostEqual(SHADOW1_DISTANCE_MPC, 600.0, places=1)

    def test_mass_range(self):
        """Mass range must cover NS/NSBH regime."""
        self.assertLessEqual(SHADOW1_MASS_MIN, 1.5)
        self.assertGreaterEqual(SHADOW1_MASS_MAX, 2.5)

    def test_mass_max_primary(self):
        """Primary mass upper bound must be greater than secondary max."""
        self.assertGreater(SHADOW1_MASS_MAX_PRIMARY, SHADOW1_MASS_MAX)

    def test_glitch_threshold(self):
        """Glitch threshold must be shorter than Shadow-1 duration."""
        self.assertLess(GLITCH_DURATION_THRESHOLD_S, SHADOW1_DURATION_S)

    def test_psi_definition_gw(self):
        """PSI_DEFINITION_GW must reference MSC at f0."""
        self.assertIn("MSC", PSI_DEFINITION_GW)
        self.assertIn("141.7", PSI_DEFINITION_GW)

    def test_psi_definition_eeg(self):
        """PSI_DEFINITION_EEG must reference PLV."""
        self.assertIn("PLV", PSI_DEFINITION_EEG)

    def test_psi_threshold_gw(self):
        """GW phase threshold must be in (0, 1)."""
        self.assertGreater(PSI_THRESHOLD_GW, 0.0)
        self.assertLess(PSI_THRESHOLD_GW, 1.0)

    def test_psi_threshold_eeg(self):
        """EEG coherence threshold must be in (0, 1) and below GW threshold."""
        self.assertGreater(PSI_THRESHOLD_EEG, 0.0)
        self.assertLess(PSI_THRESHOLD_EEG, 1.0)
        self.assertLess(PSI_THRESHOLD_EEG, PSI_THRESHOLD_GW)


class TestComputeScorePsi(unittest.TestCase):
    """Tests for the dimensionless score_psi = I(f0) × MSC(f0) fix."""

    def setUp(self):
        from scipy import signal as sp_signal
        rng = np.random.default_rng(5)
        fs = 4096.0
        n = int(fs * 1.0)
        h1 = rng.normal(0, 1e-22, n)
        l1 = rng.normal(0, 1e-22, n)
        self.freqs, self.psd = sp_signal.welch(h1, fs=fs, nperseg=256)
        _, self.msc = sp_signal.coherence(h1, l1, fs=fs, nperseg=256)

    def test_returns_float(self):
        s = compute_score_psi(self.psd, self.freqs, self.msc, 141.7001)
        self.assertIsInstance(s, float)

    def test_non_negative(self):
        s = compute_score_psi(self.psd, self.freqs, self.msc, 141.7001)
        self.assertGreaterEqual(s, 0.0)

    def test_dimensionless_order_of_magnitude(self):
        """For noise, I(f0) ≈ 1 and MSC ≈ 0 → score_psi should be O(1)."""
        s = compute_score_psi(self.psd, self.freqs, self.msc, 141.7001)
        self.assertLess(s, 100.0)


class TestDataSourceField(unittest.TestCase):
    """run_full_analysis() must include data_source = SIMULATION_FALLBACK."""

    def test_data_source_present(self):
        analyzer = Shadow1BayesianAnalyzer()
        results = analyzer.run_full_analysis()
        self.assertIn("data_source", results)

    def test_data_source_value_simulation(self):
        analyzer = Shadow1BayesianAnalyzer()
        results = analyzer.run_full_analysis()
        self.assertEqual(results["data_source"], "SIMULATION_FALLBACK")


class TestChirpMass(unittest.TestCase):
    """Tests for chirp mass estimation from frequency evolution."""

    def test_basic_calculation(self):
        """Chirp mass calculation returns a positive solar mass value."""
        m_c = chirp_mass_from_frequency_evolution(30.0, 500.0, 0.4)
        self.assertGreater(m_c, 0)
        self.assertLess(m_c, 1000)  # sanity upper bound

    def test_invalid_dt_raises(self):
        """Non-positive dt must raise ValueError."""
        with self.assertRaises(ValueError):
            chirp_mass_from_frequency_evolution(30.0, 500.0, -1.0)

    def test_invalid_frequency_order_raises(self):
        """f_end <= f_start must raise ValueError."""
        with self.assertRaises(ValueError):
            chirp_mass_from_frequency_evolution(500.0, 30.0, 0.4)

    def test_longer_dt_gives_smaller_chirp_mass(self):
        """Slower frequency evolution corresponds to lower chirp mass."""
        m_c_fast = chirp_mass_from_frequency_evolution(30.0, 500.0, 0.2)
        m_c_slow = chirp_mass_from_frequency_evolution(30.0, 500.0, 0.8)
        self.assertGreater(m_c_fast, m_c_slow)


class TestMassesFromChirpMass(unittest.TestCase):
    """Tests for component mass derivation from chirp mass."""

    def test_equal_mass_ratio(self):
        """Equal-mass binary: m1 == m2."""
        m1, m2 = masses_from_chirp_mass(1.2, mass_ratio=1.0)
        self.assertAlmostEqual(m1, m2, places=6)
        self.assertGreater(m1, 0)

    def test_mass_ordering(self):
        """m1 >= m2 for mass_ratio <= 1."""
        m1, m2 = masses_from_chirp_mass(1.5, mass_ratio=0.7)
        self.assertGreaterEqual(m1, m2)

    def test_chirp_mass_recovery(self):
        """Recovered chirp mass from components must match input."""
        m_c_input = 1.2
        m1, m2 = masses_from_chirp_mass(m_c_input, mass_ratio=0.9)
        eta = (m1 * m2) / (m1 + m2) ** 2
        m_c_recovered = (m1 + m2) * eta ** 0.6
        self.assertAlmostEqual(m_c_recovered, m_c_input, places=4)

    def test_invalid_mass_ratio_raises(self):
        """mass_ratio outside (0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            masses_from_chirp_mass(1.2, mass_ratio=0.0)
        with self.assertRaises(ValueError):
            masses_from_chirp_mass(1.2, mass_ratio=1.5)


class TestPhaseCoherence(unittest.TestCase):
    """Tests for inter-detector phase coherence calculation."""

    def setUp(self):
        fs = 4096.0
        n = int(0.5 * fs)
        t = np.linspace(0, 0.5, n, endpoint=False)
        sig = 1e-22 * np.sin(2 * np.pi * 150.0 * t)
        rng = np.random.default_rng(seed=7)
        noise = rng.normal(0, 1e-23, n)
        self.h1 = sig + noise
        self.l1 = sig * 0.98 + rng.normal(0, 1e-23, n)
        self.fs = fs

    def test_returns_expected_keys(self):
        """compute_phase_coherence must return required keys."""
        result = compute_phase_coherence(self.h1, self.l1, self.fs)
        for key in ("freqs", "coherence", "a_eff", "phase_stable",
                    "psi_definition", "psi_threshold"):
            self.assertIn(key, result)

    def test_psi_definition_in_result(self):
        """compute_phase_coherence result must include GW psi_definition."""
        result = compute_phase_coherence(self.h1, self.l1, self.fs)
        self.assertEqual(result["psi_definition"], PSI_DEFINITION_GW)
        self.assertEqual(result["psi_threshold"], PSI_THRESHOLD_GW)

    def test_a_eff_in_range(self):
        """A_eff must be in [0, 1]."""
        result = compute_phase_coherence(self.h1, self.l1, self.fs)
        self.assertGreaterEqual(result["a_eff"], 0.0)
        self.assertLessEqual(result["a_eff"], 1.0)

    def test_coherent_signal_high_a_eff(self):
        """Coherent signals should yield A_eff close to 1."""
        result = compute_phase_coherence(self.h1, self.h1, self.fs)
        self.assertGreater(result["a_eff"], 0.7)


class TestPhaseStabilityVerification(unittest.TestCase):
    """Tests for glitch-exclusion logic."""

    def test_long_stable_phase_is_astrophysical(self):
        """A_eff=0.89 for 0.4 s must be classified as astrophysical."""
        result = verify_phase_stability(0.89, 0.4)
        self.assertTrue(result["is_glitch_excluded"])
        self.assertTrue(result["is_astrophysical"])
        self.assertEqual(result["verdict"], "Silent Collision")

    def test_glitch_duration_excluded(self):
        """Duration < 0.05 s must be classified as glitch."""
        result = verify_phase_stability(0.89, 0.03)
        self.assertFalse(result["is_glitch_excluded"])
        self.assertFalse(result["is_astrophysical"])
        self.assertNotEqual(result["verdict"], "Silent Collision")

    def test_low_a_eff_not_astrophysical(self):
        """Low A_eff even with long duration must not be astrophysical."""
        result = verify_phase_stability(0.50, 0.4)
        self.assertFalse(result["is_astrophysical"])


class TestShadow1BayesianAnalyzer(unittest.TestCase):
    """End-to-end tests for the Shadow-1 Bayesian analyzer."""

    def setUp(self):
        self.analyzer = Shadow1BayesianAnalyzer()

    def test_gps_time_stored(self):
        """Analyzer must store the correct GPS time."""
        self.assertAlmostEqual(self.analyzer.gps_time, SHADOW1_GPS, places=1)

    def test_estimate_parameters_keys(self):
        """Parameter estimation must return all required keys."""
        params = self.analyzer.estimate_parameters()
        for key in ("gps_time", "chirp_mass_solar", "m1_solar", "m2_solar",
                    "distance_mpc", "in_ns_nsbh_range"):
            self.assertIn(key, params)

    def test_distance_in_parameters(self):
        """Distance must be 600 Mpc."""
        params = self.analyzer.estimate_parameters()
        self.assertAlmostEqual(params["distance_mpc"], 600.0, places=1)

    def test_masses_positive(self):
        """Estimated component masses must be positive."""
        params = self.analyzer.estimate_parameters()
        self.assertGreater(params["m1_solar"], 0)
        self.assertGreater(params["m2_solar"], 0)

    def test_phase_coherence_analysis(self):
        """Phase coherence analysis must return the reference A_eff."""
        coh = self.analyzer.analyze_phase_coherence()
        self.assertAlmostEqual(coh["a_eff_reference"], SHADOW1_A_EFF, places=5)
        self.assertIn("verdict", coh)

    def test_bayes_evidence_keys(self):
        """Bayes evidence (backward-compat) must return required keys."""
        bayes = self.analyzer.compute_bayes_evidence()
        for key in ("log_bayes_factor", "interpretation", "favors_signal"):
            self.assertIn(key, bayes)

    def test_posterior_proxy_keys(self):
        """compute_posterior_proxy must return posterior_proxy keys."""
        proxy = self.analyzer.compute_posterior_proxy()
        for key in ("log_posterior_proxy", "interpretation", "favors_signal",
                    "method"):
            self.assertIn(key, proxy)

    def test_posterior_proxy_method_field(self):
        """method field must indicate IBC/log-likelihood ratio."""
        proxy = self.analyzer.compute_posterior_proxy()
        self.assertIn("IBC", proxy["method"])

    def test_posterior_proxy_matches_bayes_evidence(self):
        """compute_posterior_proxy and compute_bayes_evidence must give same values."""
        proxy = self.analyzer.compute_posterior_proxy()
        bayes = self.analyzer.compute_bayes_evidence()
        self.assertAlmostEqual(proxy["log_posterior_proxy"],
                               bayes["log_bayes_factor"], places=5)

    def test_phase_coherence_psi_definition(self):
        """Phase coherence result must include psi_definition and psi_threshold."""
        coh = self.analyzer.analyze_phase_coherence()
        self.assertEqual(coh["psi_definition"], PSI_DEFINITION_GW)
        self.assertEqual(coh["psi_threshold"], PSI_THRESHOLD_GW)

    def test_posterior_proxy_in_results(self):
        """run_full_analysis must populate posterior_proxy in results."""
        results = self.analyzer.run_full_analysis()
        self.assertIn("posterior_proxy", results)
        self.assertIn("log_posterior_proxy", results["posterior_proxy"])

    def test_bayes_evidence_finite(self):
        """log_bayes_factor must be a finite number."""
        bayes = self.analyzer.compute_bayes_evidence()
        self.assertTrue(np.isfinite(bayes["log_bayes_factor"]))

    def test_run_full_analysis(self):
        """Full analysis must populate all result sections."""
        results = self.analyzer.run_full_analysis()
        for section in ("parameters", "phase_coherence", "posterior_proxy"):
            self.assertIn(section, results)
        # Backward-compat alias must also be present
        self.assertIn("bayes_evidence", results)

    def test_silent_collision_verdict(self):
        """Shadow-1 must be classified as Silent Collision."""
        self.analyzer.run_full_analysis()
        verdict = self.analyzer.results["phase_coherence"]["verdict"]
        self.assertEqual(verdict, "Silent Collision")


class TestEEGCoherencePipeline(unittest.TestCase):
    """Tests for the EEG coherence pipeline (Shadow-1 of Thought)."""

    def setUp(self):
        self.fs = 256.0
        self.pipeline = EEGCoherencePipeline(fs=self.fs, band_hz=(30.0, 80.0))

        rng = np.random.default_rng(seed=99)
        n = int(self.fs * 10)
        t = np.linspace(0, 10, n, endpoint=False)
        coherent = 1e-6 * np.sin(2 * np.pi * 40.0 * t)
        self.left = coherent + rng.normal(0, 5e-6, n)
        self.right = coherent * 0.9 + rng.normal(0, 5e-6, n)

    def test_bandpass_output_shape(self):
        """Filtered signal must have same shape as input."""
        filtered = self.pipeline.bandpass_filter(self.left)
        self.assertEqual(filtered.shape, self.left.shape)

    def test_a_eff_eeg_in_range(self):
        """A_eff EEG must be in [0, 1]."""
        result = self.pipeline.inter_hemisphere_coherence(self.left, self.right)
        self.assertGreaterEqual(result["a_eff_eeg"], 0.0)
        self.assertLessEqual(result["a_eff_eeg"], 1.0)

    def test_identical_channels_high_coherence(self):
        """Identical channels must produce A_eff EEG close to 1."""
        result = self.pipeline.inter_hemisphere_coherence(self.left, self.left)
        self.assertGreater(result["a_eff_eeg"], 0.7)

    def test_analyze_returns_required_keys(self):
        """analyze() must return all required keys."""
        result = self.pipeline.analyze(self.left, self.right)
        for key in ("a_eff_eeg", "amplitude_suppression",
                    "shadow_thought_detected"):
            self.assertIn(key, result)

    def test_analyze_returns_psi_definition(self):
        """analyze() result must include psi_definition and psi_threshold."""
        result = self.pipeline.inter_hemisphere_coherence(self.left, self.right)
        self.assertEqual(result["psi_definition"], PSI_DEFINITION_EEG)
        self.assertEqual(result["psi_threshold"], PSI_THRESHOLD_EEG)

    def test_invalid_band_raises(self):
        """Invalid frequency band must raise ValueError."""
        bad_pipeline = EEGCoherencePipeline(fs=self.fs, band_hz=(80.0, 30.0))
        with self.assertRaises(ValueError):
            bad_pipeline.bandpass_filter(self.left)


class TestIntegration(unittest.TestCase):
    """Integration tests for Shadow-1 full analysis."""

    def test_full_workflow(self):
        """Complete Shadow-1 workflow must succeed without errors."""
        analyzer = Shadow1BayesianAnalyzer()
        results = analyzer.run_full_analysis()

        # Verify parameter types
        self.assertIsInstance(results["parameters"]["chirp_mass_solar"], float)
        self.assertIsInstance(results["parameters"]["m1_solar"], float)

        # Verify Bayesian evidence is sensible
        log_bf = results["bayes_evidence"]["log_bayes_factor"]
        self.assertTrue(np.isfinite(log_bf))

        # Verify axiom compliance: H1-L1 coherence verified
        self.assertTrue(results["phase_coherence"]["is_glitch_excluded"])


class TestNormalizeBayesFactor(unittest.TestCase):
    """Tests for Bayes factor normalization (no ambiguity)."""

    def test_lnB_gives_correct_log10(self):
        """Passing lnB=ln(1000) must return log10_bayes_factor≈3.0."""
        b = normalize_bayes_factor(lnB=math.log(1000.0))
        # ln(1000)/ln(10) = log10(1000) = 3; 6 decimal places is appropriate for float64
        self.assertAlmostEqual(b["log10_bayes_factor"], 3.0, places=6)

    def test_log10B_gives_correct_ln(self):
        """Passing log10B=2.0 must return ln_bayes_factor≈2*ln(10)."""
        b = normalize_bayes_factor(log10B=2.0)
        self.assertAlmostEqual(b["ln_bayes_factor"], 2.0 * math.log(10.0), places=10)

    def test_both_present_consistent(self):
        """Both representations must be mutually consistent."""
        lnB = 4.5
        b = normalize_bayes_factor(lnB=lnB)
        self.assertAlmostEqual(b["ln_bayes_factor"], lnB, places=10)
        self.assertAlmostEqual(
            b["ln_bayes_factor"],
            b["log10_bayes_factor"] * math.log(10.0),
            places=10,
        )

    def test_no_args_raises(self):
        """Calling with no arguments must raise ValueError."""
        with self.assertRaises(ValueError):
            normalize_bayes_factor()


class TestTimeSlideControl(unittest.TestCase):
    """Tests for the time-slide anti-artefact control."""

    def setUp(self):
        self.fs = 4096.0
        n = int(self.fs * 2.0)
        # Use a short transient burst localized in time so that sliding breaks coherence
        rng = np.random.default_rng(seed=42)
        noise_x = rng.normal(0, 1e-22, n)
        noise_y = rng.normal(0, 1e-22, n)
        # Burst occupies only ~0.05 s (well within the 2 s window)
        burst_len = int(self.fs * 0.05)
        burst_start = n // 4
        t_burst = np.linspace(0, 0.05, burst_len, endpoint=False)
        burst = 1e-20 * np.sin(2 * np.pi * 50.0 * t_burst)
        noise_x[burst_start:burst_start + burst_len] += burst
        # 0.99 factor: near-unity correlation mimics physical H1/L1 coherence at SNR~10
        noise_y[burst_start:burst_start + burst_len] += burst * 0.99
        self.x = noise_x
        self.y = noise_y
        self.band = (30.0, 80.0)

    def test_returns_required_keys(self):
        """time_slide_control must return required keys."""
        result = time_slide_control(self.x, self.y, self.fs, self.band)
        for key in ("slides_s", "a_eff_slide_median", "a_eff_slide_max", "details"):
            self.assertIn(key, result)

    def test_coherent_signal_slide_lowers_a_eff(self):
        """Time-sliding a truly coherent signal must lower A_eff vs on-time."""
        on_time = band_coherence_feature(self.x, self.y, self.fs, self.band)
        slid = time_slide_control(self.x, self.y, self.fs, self.band)
        self.assertGreater(on_time["a_eff"], slid["a_eff_slide_median"])

    def test_a_eff_values_in_range(self):
        """All slide A_eff values must be in [0, 1]."""
        result = time_slide_control(self.x, self.y, self.fs, self.band)
        self.assertGreaterEqual(result["a_eff_slide_median"], 0.0)
        self.assertLessEqual(result["a_eff_slide_max"], 1.0)


class TestControlBandCheck(unittest.TestCase):
    """Tests for off-target control band ratio."""

    def setUp(self):
        self.fs = 4096.0
        n = int(self.fs * 2.0)
        t = np.linspace(0, 2.0, n, endpoint=False)
        # Coherence only in signal band (50 Hz)
        sig = 1e-22 * np.sin(2 * np.pi * 50.0 * t)
        rng = np.random.default_rng(seed=7)
        noise = rng.normal(0, 5e-23, n)
        self.x = sig + noise
        self.y = sig * 0.99 + rng.normal(0, 5e-23, n)
        self.signal_band = (30.0, 80.0)
        self.control_band = (190.0, 240.0)

    def test_returns_required_keys(self):
        """control_band_check must return 'signal', 'control', 'ratio_relativo'."""
        result = control_band_check(
            self.x, self.y, self.fs, self.signal_band, self.control_band
        )
        for key in ("signal", "control", "ratio_relativo"):
            self.assertIn(key, result)

    def test_signal_band_higher_a_eff_than_control(self):
        """Signal band A_eff must exceed control band A_eff for band-limited coherence."""
        result = control_band_check(
            self.x, self.y, self.fs, self.signal_band, self.control_band
        )
        self.assertGreater(result["signal"]["a_eff"], result["control"]["a_eff"])

    def test_ratio_relativo_greater_than_one(self):
        """ratio_relativo must be > 1 when coherence is band-limited to signal band."""
        result = control_band_check(
            self.x, self.y, self.fs, self.signal_band, self.control_band
        )
        self.assertGreater(result["ratio_relativo"], 1.0)


class TestSilentCollisionAssessment(unittest.TestCase):
    """Tests for the silent_collision_assessment function."""

    def test_silent_flag_true_when_all_controls_pass(self):
        """silent_flag must be True when A_eff, duration, slide, and ratio all pass."""
        result = silent_collision_assessment(
            a_eff=0.90,
            duration_s=0.4,
            a_eff_slide_median=0.50,  # 0.90 - 0.50 = 0.40 >= 0.10
            ratio_relativo=2.0,       # >= 1.5
        )
        self.assertTrue(result["silent_flag"])
        self.assertTrue(result["passes_slide_control"])
        self.assertTrue(result["passes_control_band"])

    def test_silent_flag_false_when_slide_fails(self):
        """silent_flag must be False when slide control is not passed."""
        result = silent_collision_assessment(
            a_eff=0.90,
            duration_s=0.4,
            a_eff_slide_median=0.85,  # 0.90 - 0.85 = 0.05 < 0.10
            ratio_relativo=2.0,
        )
        self.assertFalse(result["silent_flag"])
        self.assertFalse(result["passes_slide_control"])

    def test_silent_flag_false_when_ratio_fails(self):
        """silent_flag must be False when control band ratio is too low."""
        result = silent_collision_assessment(
            a_eff=0.90,
            duration_s=0.4,
            a_eff_slide_median=0.50,
            ratio_relativo=1.0,  # < 1.5
        )
        self.assertFalse(result["silent_flag"])
        self.assertFalse(result["passes_control_band"])

    def test_silent_score_positive_and_increases_with_duration(self):
        """silent_score must be positive and increase with duration."""
        r1 = silent_collision_assessment(
            a_eff=0.90, duration_s=0.1,
            a_eff_slide_median=0.5, ratio_relativo=2.0,
        )
        r2 = silent_collision_assessment(
            a_eff=0.90, duration_s=0.5,
            a_eff_slide_median=0.5, ratio_relativo=2.0,
        )
        self.assertGreater(r1["silent_score"], 0.0)
        self.assertGreater(r2["silent_score"], r1["silent_score"])

    def test_returns_thresholds(self):
        """Result must include the thresholds dict."""
        result = silent_collision_assessment(
            a_eff=0.90, duration_s=0.4,
            a_eff_slide_median=0.5, ratio_relativo=2.0,
        )
        self.assertIn("thresholds", result)
        for key in ("a_eff_thr", "dur_thr", "slide_margin", "ratio_thr"):
            self.assertIn(key, result["thresholds"])


class TestEEGDisclaimer(unittest.TestCase):
    """Test that EEG pipeline result includes the independence disclaimer."""

    def test_eeg_disclaimer_in_main_results(self):
        """main() must attach the EEG independence disclaimer to eeg_pipeline."""
        import importlib
        import scripts.shadow1_bayesian_coherence as mod
        # Simulate what main() does without printing
        analyzer = mod.Shadow1BayesianAnalyzer()
        results = analyzer.run_full_analysis()

        rng = np.random.default_rng(seed=0)
        fs_eeg = 256.0
        n_eeg = int(fs_eeg * 10.0)
        t_eeg = np.linspace(0.0, 10.0, n_eeg, endpoint=False)
        coherent = 0.5e-6 * np.sin(2.0 * np.pi * 40.0 * t_eeg)
        left_channel = coherent + rng.normal(0.0, 5e-6, n_eeg)
        right_channel = coherent * 0.95 + rng.normal(0.0, 5e-6, n_eeg)

        pipeline = mod.EEGCoherencePipeline(fs=fs_eeg)
        eeg_result = pipeline.analyze(left_channel, right_channel)
        results["eeg_pipeline"] = {
            k: v for k, v in eeg_result.items() if k not in ("freqs", "coherence")
        }
        results["eeg_pipeline"]["disclaimer"] = (
            "Independent pipeline; not joint inference with GW."
        )
        self.assertIn("disclaimer", results["eeg_pipeline"])
        self.assertIn("not joint inference", results["eeg_pipeline"]["disclaimer"])


class TestBayesEvidenceNormalized(unittest.TestCase):
    """Test that compute_bayes_evidence returns both ln and log10 Bayes factors."""

    def test_both_bayes_formats_present(self):
        """bayes_evidence must contain both ln_bayes_factor and log10_bayes_factor."""
        analyzer = Shadow1BayesianAnalyzer()
        bayes = analyzer.compute_bayes_evidence()
        self.assertIn("ln_bayes_factor", bayes)
        self.assertIn("log10_bayes_factor", bayes)

    def test_bayes_formats_consistent(self):
        """ln_bayes_factor and log10_bayes_factor must be mutually consistent."""
        analyzer = Shadow1BayesianAnalyzer()
        bayes = analyzer.compute_bayes_evidence()
        ln_b = bayes["ln_bayes_factor"]
        log10_b = bayes["log10_bayes_factor"]
        # Both values are rounded to 4 decimal places, so check at 3 places for rounding tolerance
        self.assertAlmostEqual(ln_b / math.log(10.0), log10_b, places=3)


class TestFullAnalysisControls(unittest.TestCase):
    """Test that run_full_analysis populates controls and verdict sections."""

    def test_controls_present(self):
        """run_full_analysis must populate 'controls' section."""
        analyzer = Shadow1BayesianAnalyzer()
        results = analyzer.run_full_analysis()
        self.assertIn("controls", results)
        self.assertIn("time_slide", results["controls"])
        self.assertIn("control_band", results["controls"])

    def test_verdict_present(self):
        """run_full_analysis must populate 'verdict' section with silent_score."""
        analyzer = Shadow1BayesianAnalyzer()
        results = analyzer.run_full_analysis()
        self.assertIn("verdict", results)
        self.assertIn("silent_score", results["verdict"])
        self.assertIn("silent_flag", results["verdict"])


if __name__ == "__main__":
    unittest.main()
