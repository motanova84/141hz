import numpy as np
import pytest

from qcal_v31_models import (
    F_B_HZ,
    adelic_period,
    alpha_flow,
    dirac_dilation_symbol,
    lockin_at_frequency,
    required_cycles,
)


def test_signature_b_period():
    assert np.isclose(adelic_period(F_B_HZ), 1.0 / F_B_HZ)
    assert np.isclose(adelic_period(F_B_HZ) / 60.0, 32.0512820513)


def test_archimedean_dirac_symbol_is_continuous_variable():
    xi = np.array([-2.0, 0.0, 3.5])
    assert np.allclose(dirac_dilation_symbol(xi), xi)


def test_alpha_flow_is_finite_and_deterministic():
    gamma = np.array([14.1347251417, 21.0220396388, 25.0108575801])
    a1, p1 = alpha_flow(1.0 / 137.0, gamma, kappa_b=0.0001, steps=50)
    a2, p2 = alpha_flow(1.0 / 137.0, gamma, kappa_b=0.0001, steps=50)
    assert np.all(np.isfinite(a1))
    assert np.all(np.isfinite(p1))
    assert np.allclose(a1, a2)
    assert np.allclose(p1, p2)


def test_lockin_recovers_known_target():
    fs = 1.0
    target = F_B_HZ
    t = np.arange(0, 8.0 / target, 1.0 / fs)
    x = 2.0 * np.cos(2 * np.pi * target * t + 0.3)
    result = lockin_at_frequency(x, fs, target)
    assert np.isclose(result["amplitude"], 2.0, rtol=0.03)


def test_required_cycles():
    assert np.isclose(required_cycles(5.0), 5.0 / F_B_HZ)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        adelic_period(0)
    with pytest.raises(ValueError):
        required_cycles(0)
