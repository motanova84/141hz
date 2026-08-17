import numpy as np

from qcal.noesis_adelic_bio import (
    F0_HZ,
    F_B_HZ,
    PSI_TARGET,
    AdelicDiracModel,
    QCALConstants,
    alpha_flow,
    noesis_stress_energy,
    phoenix_reference,
)


def test_frequency_constants_and_period():
    c = QCALConstants()
    assert F0_HZ == 141.7001
    assert F_B_HZ == 0.00052
    assert PSI_TARGET == 0.999999
    assert np.isclose(1.0 / F_B_HZ, 1923.076923076923)
    assert np.isclose(c.dimensionless_bridge, F_B_HZ / F0_HZ)


def test_adelic_operator_is_real_on_real_mode():
    h = AdelicDiracModel()
    value = h.eigenvalue(14.134725141734693)
    assert np.isfinite(value)
    assert np.isreal(value)


def test_alpha_flow_is_deterministic():
    a = alpha_flow(iterations=50)
    b = alpha_flow(iterations=50)
    assert a == b
    assert np.isfinite(a["alpha_inv"])
    assert a["psi"] > 0.95


def test_phoenix_reference_frequency():
    t = np.arange(0.0, 2.0 / F_B_HZ, 1.0)
    s = phoenix_reference(t)
    assert s.shape == t.shape
    assert np.max(np.abs(s)) <= 1.0


def test_noesis_energy_sector():
    out = noesis_stress_energy(
        psi=0.999999,
        rho=1.0,
        gamma=0.0,
        grad_psi_sq=0.0,
        potential=0.0,
        current_norm=0.5,
    )
    assert out["gamma"] == 0.0
    assert out["rho_total"] > out["rho_classical"]
