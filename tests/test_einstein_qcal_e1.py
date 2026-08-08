import unittest

from qcal.constants import F0_HZ
from qcal.einstein_qcal import CoherenceState
from qcal.einstein_qcal_e1 import (
    QCALE1Measurement,
    QCALE1Verdict,
    build_qcal_e1_contract,
    compute_scaling_metrics,
    evaluate_qcal_e1,
    predicted_phase_shift_rad,
)


class TestEinsteinQCALE1(unittest.TestCase):
    def test_contract_uses_exact_anchor(self):
        contract = build_qcal_e1_contract()
        self.assertEqual(contract.central_frequency_hz, 141.7001)
        self.assertEqual(contract.tolerance_hz, 1e-4)
        self.assertTrue(contract.forbid_post_hoc_free_parameters)

    def test_predicted_phase_shift_is_zero_at_resonance_limit(self):
        contract = build_qcal_e1_contract()
        state = CoherenceState(psi=1.0, f_observer=F0_HZ)
        phase_shift = predicted_phase_shift_rad(state, cavity_length_m=4000.0, contract=contract)
        self.assertAlmostEqual(phase_shift, 0.0, places=12)

    def test_supported_verdict_for_exact_peak(self):
        contract = build_qcal_e1_contract()
        scaling = compute_scaling_metrics(cavity_length_m=4000.0, contract=contract)
        measurement = QCALE1Measurement(
            psi_obs=0.999998,
            cavity_length_m=4000.0,
            detected_peak_frequency_hz=F0_HZ,
            detected_peak_power=1.0,
            phase_velocity_sensitive=True,
            scale_linearity_r2=scaling["linear_fit_r2"],
            scale_slope=scaling["linear_fit_slope"],
        )
        evaluation = evaluate_qcal_e1(measurement, contract)
        self.assertEqual(evaluation.verdict, QCALE1Verdict.SUPPORTED.value)
        self.assertTrue(evaluation.criteria["frequency_match"])

    def test_falsified_without_peak_under_incoherence(self):
        contract = build_qcal_e1_contract()
        measurement = QCALE1Measurement(
            psi_obs=0.999998,
            cavity_length_m=4000.0,
            detector_sensitivity_hz_sqrt=1e-24,
            detected_peak_frequency_hz=None,
            detected_peak_power=None,
        )
        evaluation = evaluate_qcal_e1(measurement, contract)
        self.assertEqual(evaluation.verdict, QCALE1Verdict.FALSIFIED.value)

    def test_falsified_if_peak_is_off_frequency(self):
        contract = build_qcal_e1_contract()
        measurement = QCALE1Measurement(
            psi_obs=0.999998,
            cavity_length_m=4000.0,
            detected_peak_frequency_hz=141.9,
            detected_peak_power=1.0,
        )
        evaluation = evaluate_qcal_e1(measurement, contract)
        self.assertEqual(evaluation.verdict, QCALE1Verdict.FALSIFIED.value)


if __name__ == "__main__":
    unittest.main()
