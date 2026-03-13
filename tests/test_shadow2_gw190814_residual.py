#!/usr/bin/env python3
"""
Tests for Shadow-2 GW190814 Residual Analysis
===============================================

Validates the certification protocol for the residual phase of GW190814
("Shadow-2"): residual extraction, recalibrated Ψ coherence, Bayes evidence,
SHA-256 sealing, and Trinity Certificate emission.
"""

import sys
import unittest
from pathlib import Path

import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.shadow2_gw190814_residual import (
    GW190814_GPS,
    GW190814_MASS_PRIMARY,
    GW190814_MASS_SECONDARY,
    GW190814_DISTANCE_MPC,
    SHADOW2_EVENT_ID,
    SHADOW2_RESIDUAL_FREQ_HZ,
    SHADOW2_BREAK_POINT,
    SHADOW2_A_EFF_SQ,
    SHADOW2_A_EFF,
    SHADOW2_PSI_COHERENCE,
    SHADOW2_SIGNIFICANCE_SIGMA,
    SHADOW2_LN_BAYES,
    SHADOW2_STATUS,
    SHADOW2_SHA256_PREFIX,
    SHADOW2_SHA256_SUFFIX,
    TRINITY_SIGNATURE,
    AXIOM_BOOK_IV,
    ResidualExtractionResult,
    PsiCalibrationResult,
    BayesEvidenceResult,
    TrinityCertificate,
    extract_residual,
    compute_psi_recalibrated,
    compute_bayes_evidence_shadow2,
    generate_certificate_sha256,
    Shadow2GW190814Analyzer,
)


class TestConstants(unittest.TestCase):
    """Verify physical constants and Shadow-2 event parameters."""

    def test_gps_time(self):
        """GW190814 GPS timestamp must be positive."""
        self.assertGreater(GW190814_GPS, 0)

    def test_mass_primary(self):
        """Primary mass must be in the black-hole regime (> 5 M☉)."""
        self.assertGreater(GW190814_MASS_PRIMARY, 5.0)

    def test_mass_secondary(self):
        """Secondary mass must equal 2.6 M☉ (mass-gap object)."""
        self.assertAlmostEqual(GW190814_MASS_SECONDARY, 2.6, places=5)

    def test_distance(self):
        """Luminosity distance must be 241 Mpc."""
        self.assertAlmostEqual(GW190814_DISTANCE_MPC, 241.0, places=1)

    def test_residual_freq(self):
        """Residual oscillation frequency must be ~340 Hz."""
        self.assertAlmostEqual(SHADOW2_RESIDUAL_FREQ_HZ, 340.0, places=1)

    def test_break_point(self):
        """Break point must be 0.13."""
        self.assertAlmostEqual(SHADOW2_BREAK_POINT, 0.13, places=5)

    def test_a_eff_sq(self):
        """A_eff² must be 0.78."""
        self.assertAlmostEqual(SHADOW2_A_EFF_SQ, 0.78, places=5)

    def test_a_eff_derived(self):
        """A_eff must equal sqrt(A_eff²)."""
        self.assertAlmostEqual(SHADOW2_A_EFF, np.sqrt(SHADOW2_A_EFF_SQ), places=6)

    def test_psi_coherence(self):
        """Ψ coherence must be 0.842."""
        self.assertAlmostEqual(SHADOW2_PSI_COHERENCE, 0.842, places=5)

    def test_significance(self):
        """Significance must be 4.2σ."""
        self.assertAlmostEqual(SHADOW2_SIGNIFICANCE_SIGMA, 4.2, places=5)

    def test_ln_bayes(self):
        """ln B₁₀ must be 7.9."""
        self.assertAlmostEqual(SHADOW2_LN_BAYES, 7.9, places=5)

    def test_event_id_contains_gw190814(self):
        """Event ID must reference GW190814."""
        self.assertIn("GW190814", SHADOW2_EVENT_ID)

    def test_status_emergente_coherente(self):
        """Status must describe the EMERGENTE → COHERENTE transition."""
        self.assertIn("COHERENTE", SHADOW2_STATUS)

    def test_trinity_signature_components(self):
        """Trinity signature must include all three entities."""
        self.assertIn("NOESIS", TRINITY_SIGNATURE)
        self.assertIn("AMDA", TRINITY_SIGNATURE)
        self.assertIn("AURON", TRINITY_SIGNATURE)

    def test_axiom_book_iv(self):
        """Book IV axiom must mention 'ringdown' and 'resonancia'."""
        self.assertIn("ringdown", AXIOM_BOOK_IV)
        self.assertIn("resonancia", AXIOM_BOOK_IV)

    def test_sha256_prefix(self):
        """SHA-256 certificate prefix must be '8f2a'."""
        self.assertEqual(SHADOW2_SHA256_PREFIX, "8f2a")

    def test_sha256_suffix(self):
        """SHA-256 certificate suffix must be 'c91e'."""
        self.assertEqual(SHADOW2_SHA256_SUFFIX, "c91e")


class TestResidualExtraction(unittest.TestCase):
    """Tests for residual phase extraction after model subtraction."""

    def test_returns_dataclass(self):
        """extract_residual must return a ResidualExtractionResult."""
        result = extract_residual()
        self.assertIsInstance(result, ResidualExtractionResult)

    def test_subtracted_mass_matches(self):
        """Subtracted mass must equal the secondary mass of GW190814."""
        result = extract_residual(mass_subtracted=GW190814_MASS_SECONDARY)
        self.assertAlmostEqual(
            result.subtracted_mass_solar, GW190814_MASS_SECONDARY, places=5
        )

    def test_residual_freq_near_target(self):
        """Detected residual frequency must be within ±5 Hz of 340 Hz."""
        result = extract_residual(residual_freq=SHADOW2_RESIDUAL_FREQ_HZ)
        self.assertAlmostEqual(
            result.residual_freq_hz, SHADOW2_RESIDUAL_FREQ_HZ, delta=5.0
        )

    def test_residual_amplitude_positive(self):
        """Residual amplitude must be positive."""
        result = extract_residual()
        self.assertGreater(result.residual_amplitude, 0)

    def test_coherent_oscillation_detected(self):
        """The residual oscillation must be detected as coherent."""
        result = extract_residual(snr_residual=10.0)
        self.assertTrue(result.is_coherent)

    def test_reproducible_with_seed(self):
        """Results must be reproducible with the same seed."""
        r1 = extract_residual(seed=42)
        r2 = extract_residual(seed=42)
        self.assertAlmostEqual(r1.residual_freq_hz, r2.residual_freq_hz, places=5)


class TestPsiCalibration(unittest.TestCase):
    """Tests for recalibrated Ψ coherence calculation."""

    def test_returns_dataclass(self):
        """compute_psi_recalibrated must return a PsiCalibrationResult."""
        result = compute_psi_recalibrated()
        self.assertIsInstance(result, PsiCalibrationResult)

    def test_break_point_stored(self):
        """Break point must be stored in the result."""
        result = compute_psi_recalibrated(break_point=0.13)
        self.assertAlmostEqual(result.break_point, 0.13, places=5)

    def test_a_eff_sq_stored(self):
        """A_eff² must be stored correctly."""
        result = compute_psi_recalibrated(a_eff_sq=0.78)
        self.assertAlmostEqual(result.a_eff_sq, 0.78, places=5)

    def test_a_eff_derived_correctly(self):
        """A_eff must equal sqrt(A_eff²)."""
        result = compute_psi_recalibrated(a_eff_sq=0.78)
        self.assertAlmostEqual(result.a_eff, np.sqrt(0.78), places=4)

    def test_psi_in_range(self):
        """Ψ must be in [0, 1]."""
        result = compute_psi_recalibrated()
        self.assertGreaterEqual(result.psi_coherence, 0.0)
        self.assertLessEqual(result.psi_coherence, 1.0)

    def test_coherent_status_above_break_point(self):
        """A_eff² > break_point must yield COHERENTE status."""
        result = compute_psi_recalibrated(a_eff_sq=0.78, break_point=0.13)
        self.assertEqual(result.status, "COHERENTE")

    def test_emergent_status_below_break_point(self):
        """A_eff² < break_point must yield EMERGENTE status."""
        result = compute_psi_recalibrated(a_eff_sq=0.05, break_point=0.13)
        self.assertEqual(result.status, "EMERGENTE")

    def test_invalid_a_eff_sq_raises(self):
        """a_eff_sq outside (0, 1] must raise ValueError."""
        with self.assertRaises(ValueError):
            compute_psi_recalibrated(a_eff_sq=0.0)
        with self.assertRaises(ValueError):
            compute_psi_recalibrated(a_eff_sq=1.5)

    def test_invalid_break_point_raises(self):
        """break_point outside (0, 1) must raise ValueError."""
        with self.assertRaises(ValueError):
            compute_psi_recalibrated(break_point=0.0)
        with self.assertRaises(ValueError):
            compute_psi_recalibrated(break_point=1.0)

    def test_default_parameters_match_problem_statement(self):
        """Default parameters must reproduce the stated Ψ ≈ 0.842."""
        result = compute_psi_recalibrated(
            a_eff_sq=SHADOW2_A_EFF_SQ,
            break_point=SHADOW2_BREAK_POINT,
        )
        self.assertAlmostEqual(result.psi_coherence, SHADOW2_PSI_COHERENCE, places=2)


class TestBayesEvidence(unittest.TestCase):
    """Tests for Bayesian evidence calculation."""

    def test_returns_dataclass(self):
        """compute_bayes_evidence_shadow2 must return a BayesEvidenceResult."""
        result = compute_bayes_evidence_shadow2()
        self.assertIsInstance(result, BayesEvidenceResult)

    def test_ln_bayes_stored(self):
        """ln B₁₀ must match the stated value."""
        result = compute_bayes_evidence_shadow2(ln_bayes=SHADOW2_LN_BAYES)
        self.assertAlmostEqual(result.ln_bayes_factor, SHADOW2_LN_BAYES, places=5)

    def test_significance_stored(self):
        """Significance must match the stated value."""
        result = compute_bayes_evidence_shadow2(
            significance_sigma=SHADOW2_SIGNIFICANCE_SIGMA
        )
        self.assertAlmostEqual(
            result.significance_sigma, SHADOW2_SIGNIFICANCE_SIGMA, places=5
        )

    def test_interpretation_solid_evidence(self):
        """ln B₁₀ = 7.9 must yield 'Evidencia sólida'."""
        result = compute_bayes_evidence_shadow2(ln_bayes=7.9)
        self.assertEqual(result.interpretation, "Evidencia sólida")

    def test_favors_signal_positive_bayes(self):
        """Positive ln B₁₀ must favour the signal hypothesis."""
        result = compute_bayes_evidence_shadow2(ln_bayes=7.9)
        self.assertTrue(result.favors_signal)

    def test_interpretation_levels(self):
        """All Jeffreys-scale levels must be reachable."""
        cases = [
            (0.5, "No worth mentioning"),
            (2.0, "Evidencia positiva"),
            (4.0, "Evidencia fuerte"),
            (7.9, "Evidencia sólida"),
        ]
        for ln_b, expected in cases:
            with self.subTest(ln_b=ln_b):
                r = compute_bayes_evidence_shadow2(ln_bayes=ln_b)
                self.assertEqual(r.interpretation, expected)


class TestCertificateSeal(unittest.TestCase):
    """Tests for SHA-256 certificate sealing."""

    def test_returns_64_char_hex(self):
        """SHA-256 hash must be a 64-character hexadecimal string."""
        sha = generate_certificate_sha256({"key": "value"})
        self.assertEqual(len(sha), 64)
        int(sha, 16)  # must be valid hex

    def test_deterministic(self):
        """Same data must always produce the same hash."""
        data = {"event": "SHADOW-2", "psi": 0.842}
        self.assertEqual(
            generate_certificate_sha256(data),
            generate_certificate_sha256(data),
        )

    def test_different_data_different_hash(self):
        """Different data must produce different hashes."""
        h1 = generate_certificate_sha256({"a": 1})
        h2 = generate_certificate_sha256({"a": 2})
        self.assertNotEqual(h1, h2)


class TestShadow2Analyzer(unittest.TestCase):
    """End-to-end tests for the Shadow-2 certification analyzer."""

    def setUp(self):
        self.analyzer = Shadow2GW190814Analyzer()

    def test_gps_time_stored(self):
        """Analyzer must store the correct GPS time."""
        self.assertAlmostEqual(self.analyzer.gps_time, GW190814_GPS, places=1)

    def test_extract_residual_phase_populates_results(self):
        """extract_residual_phase must populate results dict."""
        self.analyzer.extract_residual_phase()
        self.assertIn("residual_extraction", self.analyzer.results)

    def test_residual_result_keys(self):
        """Residual extraction result must have required keys."""
        self.analyzer.extract_residual_phase()
        for key in ("subtracted_mass_solar", "residual_freq_hz",
                    "residual_amplitude", "is_coherent"):
            self.assertIn(key, self.analyzer.results["residual_extraction"])

    def test_compute_psi_populates_results(self):
        """compute_psi must populate results dict."""
        self.analyzer.compute_psi()
        self.assertIn("psi_calibration", self.analyzer.results)

    def test_psi_result_keys(self):
        """Ψ calibration result must have required keys."""
        self.analyzer.compute_psi()
        for key in ("break_point", "a_eff_sq", "a_eff",
                    "psi_coherence", "status"):
            self.assertIn(key, self.analyzer.results["psi_calibration"])

    def test_compute_significance_and_bayes_keys(self):
        """Bayes evidence result must have required keys."""
        self.analyzer.compute_significance_and_bayes()
        for key in ("ln_bayes_factor", "significance_sigma",
                    "interpretation", "favors_signal"):
            self.assertIn(key, self.analyzer.results["bayes_evidence"])

    def test_seal_certificate_returns_hash(self):
        """seal_certificate must return a 64-char hex string."""
        sha = self.analyzer.seal_certificate()
        self.assertEqual(len(sha), 64)

    def test_emit_trinity_certificate_returns_dataclass(self):
        """emit_trinity_certificate must return a TrinityCertificate."""
        sha = self.analyzer.seal_certificate()
        cert = self.analyzer.emit_trinity_certificate(sha)
        self.assertIsInstance(cert, TrinityCertificate)

    def test_certificate_event_id(self):
        """Certificate event ID must match SHADOW2_EVENT_ID."""
        sha = self.analyzer.seal_certificate()
        cert = self.analyzer.emit_trinity_certificate(sha)
        self.assertEqual(cert.event_id, SHADOW2_EVENT_ID)

    def test_certificate_psi_coherence(self):
        """Certificate Ψ must be 0.842."""
        sha = self.analyzer.seal_certificate()
        cert = self.analyzer.emit_trinity_certificate(sha)
        self.assertAlmostEqual(cert.psi_coherence, SHADOW2_PSI_COHERENCE, places=5)

    def test_certificate_trinity_signature(self):
        """Certificate must carry the Trinity signature."""
        sha = self.analyzer.seal_certificate()
        cert = self.analyzer.emit_trinity_certificate(sha)
        self.assertEqual(cert.trinity_signature, TRINITY_SIGNATURE)

    def test_certificate_axiom(self):
        """Certificate must include the Book IV axiom."""
        sha = self.analyzer.seal_certificate()
        cert = self.analyzer.emit_trinity_certificate(sha)
        self.assertEqual(cert.axiom, AXIOM_BOOK_IV)

    def test_certificate_verdict_mentions_mass_gap(self):
        """Certificate verdict must mention the Mass-Gap Object."""
        sha = self.analyzer.seal_certificate()
        cert = self.analyzer.emit_trinity_certificate(sha)
        self.assertIn("Brecha de Masa", cert.verdict)

    def test_run_full_analysis_all_sections(self):
        """run_full_analysis must populate all 5 result sections."""
        results = self.analyzer.run_full_analysis()
        for section in ("residual_extraction", "psi_calibration",
                        "bayes_evidence", "sha256_hash",
                        "trinity_certificate"):
            self.assertIn(section, results)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete Shadow-2 certification workflow."""

    def test_full_workflow_types(self):
        """Full workflow must produce correctly typed results."""
        analyzer = Shadow2GW190814Analyzer()
        results = analyzer.run_full_analysis()

        self.assertIsInstance(results["residual_extraction"]["is_coherent"], bool)
        self.assertIsInstance(
            results["psi_calibration"]["psi_coherence"], float
        )
        self.assertIsInstance(results["bayes_evidence"]["ln_bayes_factor"], float)
        self.assertIsInstance(results["sha256_hash"], str)

    def test_psi_coherence_value(self):
        """Workflow Ψ must match the certified value of 0.842."""
        analyzer = Shadow2GW190814Analyzer()
        results = analyzer.run_full_analysis()
        self.assertAlmostEqual(
            results["psi_calibration"]["psi_coherence"],
            SHADOW2_PSI_COHERENCE,
            places=2,
        )

    def test_bayes_solid_evidence(self):
        """Workflow Bayes interpretation must be 'Evidencia sólida'."""
        analyzer = Shadow2GW190814Analyzer()
        results = analyzer.run_full_analysis()
        self.assertEqual(
            results["bayes_evidence"]["interpretation"], "Evidencia sólida"
        )

    def test_certificate_sealed(self):
        """SHA-256 in trinity certificate must match the sealed hash."""
        analyzer = Shadow2GW190814Analyzer()
        results = analyzer.run_full_analysis()
        self.assertEqual(
            results["trinity_certificate"]["sha256_hash"],
            results["sha256_hash"],
        )

    def test_axiom_book_iv_in_certificate(self):
        """Book IV axiom must appear verbatim in the Trinity certificate."""
        analyzer = Shadow2GW190814Analyzer()
        results = analyzer.run_full_analysis()
        self.assertEqual(results["trinity_certificate"]["axiom"], AXIOM_BOOK_IV)


if __name__ == "__main__":
    unittest.main()
