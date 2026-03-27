"""
Tests for physics/tejido_cosmologico.py

Validates the mass-energy translation from f₀ = 141.7001 Hz to cosmological
fabric parameters: fabric mass m_ψ, Swampland coupling λ, DM self-interaction
σ/m, and black-hole superradiance conditions.

Author: José Manuel Mota Burruezo
License: MIT
"""

import math
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.tejido_cosmologico import (
    masa_tejido_kg,
    masa_tejido_eV,
    energia_tejido_J,
    energia_tejido_eV,
    regimen_materia_oscura,
    acoplamiento_swampland,
    seccion_eficaz_autointeraccion,
    sigma_sobre_masa_cm2_g,
    margen_bullet_cluster,
    masa_bh_optima_kg,
    masa_bh_optima_masas_solares,
    parametro_alfa_gravitacional,
    frecuencia_compton_tejido,
    condicion_superradiancia,
    calcular_tejido,
    resumen_tejido,
    TejidoCosmologico,
    BULLET_CLUSTER_LIMIT_CM2_G,
    DM_ULTRALIGHT_MAX_EV,
    DM_LIGHT_MAX_EV,
)
from qcal.constants import F0_HZ, H_PLANCK, HBAR, C, EV_TO_J, M_PLANCK_KG


class TestMasaTejido(unittest.TestCase):
    """Section I — Fabric mass: from frequency to rest energy."""

    # Expected values
    _M_PSI_EV = 5.86e-13   # eV/c²  (m_ψ = hf₀/c²)
    _M_PSI_KG = 1.04e-48   # kg
    _E_PSI_EV = 5.86e-13   # eV (same number, different interpretation)
    _E_PSI_J  = 9.39e-32   # J

    def test_masa_tejido_kg_value(self):
        """m_ψ in kg matches hf₀/c²."""
        expected = H_PLANCK * F0_HZ / C**2
        self.assertAlmostEqual(masa_tejido_kg(), expected, delta=expected * 1e-6,
                               msg="Fabric mass in kg should equal h·f₀/c²")

    def test_masa_tejido_kg_order_of_magnitude(self):
        """m_ψ is of order 10⁻⁴⁸ kg."""
        m = masa_tejido_kg()
        self.assertGreater(m, 1e-49, "m_ψ should be > 10⁻⁴⁹ kg")
        self.assertLess(m, 1e-47, "m_ψ should be < 10⁻⁴⁷ kg")

    def test_masa_tejido_eV_value(self):
        """m_ψ in eV/c² ≈ 5.86 × 10⁻¹³ eV/c² (correct unit conversion)."""
        m_eV = masa_tejido_eV()
        self.assertAlmostEqual(m_eV, self._M_PSI_EV, delta=0.02e-13,
                               msg="Fabric mass should be ≈5.86×10⁻¹³ eV/c²")

    def test_masa_tejido_eV_consistency(self):
        """m_ψ[kg] × c² / eV_to_J == m_ψ[eV/c²]."""
        from_kg = masa_tejido_kg() * C**2 / EV_TO_J
        self.assertAlmostEqual(masa_tejido_eV(), from_kg, delta=from_kg * 1e-6,
                               msg="eV conversion must include c² factor")

    def test_energia_tejido_J(self):
        """E_ψ = h·f₀ in joules."""
        expected = H_PLANCK * F0_HZ
        self.assertAlmostEqual(energia_tejido_J(), expected, delta=expected * 1e-6)

    def test_energia_tejido_eV(self):
        """E_ψ ≈ 5.86 × 10⁻¹³ eV."""
        e_eV = energia_tejido_eV()
        self.assertAlmostEqual(e_eV, self._E_PSI_EV, delta=0.02e-13,
                               msg="Energy should be ≈5.86×10⁻¹³ eV")

    def test_energia_equals_masa_numerically(self):
        """E_ψ[eV] == m_ψ[eV/c²] numerically (rest energy in natural units)."""
        self.assertAlmostEqual(energia_tejido_eV(), masa_tejido_eV(),
                               delta=masa_tejido_eV() * 1e-6,
                               msg="Rest energy in eV equals mass in eV/c² numerically")

    def test_f0_is_141_7001(self):
        """Module uses the canonical f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)


class TestRegimensDarkMatter(unittest.TestCase):
    """Dark matter mass regime classification."""

    def test_regimen_es_ligero(self):
        """m_ψ ≈ 5.86×10⁻¹³ eV falls in the 'ligero' (light boson DM) window."""
        self.assertEqual(regimen_materia_oscura(), "ligero")

    def test_regimen_above_ultralight(self):
        """m_ψ is NOT in the ultra-light regime (which has small-scale issues)."""
        self.assertNotEqual(regimen_materia_oscura(), "ultra-ligero")

    def test_m_psi_within_boson_dm_range(self):
        """m_ψ is between 10⁻²² and 10⁻¹⁰ eV (optimal boson DM window)."""
        m = masa_tejido_eV()
        self.assertGreater(m, DM_ULTRALIGHT_MAX_EV,
                           "m_ψ should be above the ultra-light limit 10⁻²² eV")
        self.assertLess(m, DM_LIGHT_MAX_EV,
                        "m_ψ should be below the light/intermediate boundary 10⁻¹⁰ eV")


class TestAcoplamientoSwampland(unittest.TestCase):
    """Section II — Swampland coupling constant λ."""

    _LAMBDA_EXPECTED = 4.8e-41

    def test_lambda_value(self):
        """λ = m_ψ/M_P ≈ 4.8 × 10⁻⁴¹."""
        lam = acoplamiento_swampland()
        self.assertAlmostEqual(lam, self._LAMBDA_EXPECTED, delta=0.1e-41,
                               msg="Swampland coupling should be ≈4.8×10⁻⁴¹")

    def test_lambda_order_of_magnitude(self):
        """λ is of order 10⁻⁴¹ (i.e. log₁₀ λ between −42 and −40)."""
        lam = acoplamiento_swampland()
        log_lam = math.log10(lam)
        self.assertGreater(log_lam, -42.0, msg="log₁₀(λ) should be > −42")
        self.assertLess(log_lam, -40.0, msg="log₁₀(λ) should be < −40")

    def test_lambda_positive(self):
        """λ > 0 (repulsive self-interaction → prevents singularities)."""
        self.assertGreater(acoplamiento_swampland(), 0)

    def test_lambda_much_less_than_one(self):
        """λ ≪ 1 ensures the effective field theory is under control."""
        self.assertLess(acoplamiento_swampland(), 1e-10)

    def test_lambda_formula(self):
        """λ = M_QCAL_KG / M_PLANCK_KG."""
        expected = masa_tejido_kg() / M_PLANCK_KG
        self.assertAlmostEqual(acoplamiento_swampland(), expected, delta=expected * 1e-6)


class TestAutoInteraccion(unittest.TestCase):
    """Section III-A — Dark matter self-interaction (Bullet Cluster)."""

    def test_sigma_positive(self):
        """Self-interaction cross section is positive."""
        self.assertGreater(seccion_eficaz_autointeraccion(), 0)

    def test_sigma_sobre_masa_positive(self):
        """σ/m is positive."""
        self.assertGreater(sigma_sobre_masa_cm2_g(), 0)

    def test_sigma_sobre_masa_well_below_bullet_cluster(self):
        """σ/m ≪ 1 cm²/g (Bullet Cluster limit must not be violated)."""
        sm = sigma_sobre_masa_cm2_g()
        self.assertLess(sm, BULLET_CLUSTER_LIMIT_CM2_G,
                        "σ/m must be below the 1 cm²/g Bullet Cluster limit")

    def test_margen_bullet_cluster_enormous(self):
        """Safety margin is >> 1 (fabric is transparent to itself)."""
        margin = margen_bullet_cluster()
        self.assertGreater(margin, 1e6,
                           "Margin relative to Bullet Cluster limit should be >> 10⁶")

    def test_sigma_formula_components(self):
        """σ = λ²ℏ² / (16π m_ψ² c) — check each factor individually."""
        lam = acoplamiento_swampland()
        m = masa_tejido_kg()
        expected = (lam**2 * HBAR**2) / (16.0 * math.pi * m**2 * C)
        self.assertAlmostEqual(seccion_eficaz_autointeraccion(), expected,
                               delta=expected * 1e-6)


class TestSuperradianciaAgujerosNegros(unittest.TestCase):
    """Section III-B — Black hole superradiance."""

    def test_masa_bh_optima_kg_positive(self):
        """Optimal BH mass is positive."""
        self.assertGreater(masa_bh_optima_kg(), 0)

    def test_masa_bh_optima_masas_solares_range(self):
        """Optimal BH mass is in the intermediate-mass BH range (~10–10⁴ M_sun)."""
        m_sol = masa_bh_optima_masas_solares()
        self.assertGreater(m_sol, 10,
                           "Optimal BH should be heavier than 10 M_sun")
        self.assertLess(m_sol, 1e4,
                        "Optimal BH should be lighter than 10⁴ M_sun")

    def test_masa_bh_optima_approx_228_msun(self):
        """Optimal BH mass ≈ 228 M_sun."""
        m_sol = masa_bh_optima_masas_solares()
        self.assertAlmostEqual(m_sol, 228.0, delta=10.0,
                               msg="Optimal BH mass should be ≈228 M_sun")

    def test_alpha_gravitacional_at_optimal_is_unity(self):
        """α = G M_opt m_ψ / (ℏ c) ≈ 1 at the optimal BH mass."""
        m_opt_kg = masa_bh_optima_kg()
        alpha = parametro_alfa_gravitacional(m_opt_kg)
        self.assertAlmostEqual(alpha, 1.0, delta=0.01,
                               msg="α should equal 1 at the optimal BH mass")

    def test_alpha_increases_with_bh_mass(self):
        """Larger BH mass → larger α (tighter gravitational coupling)."""
        m_opt = masa_bh_optima_kg()
        alpha_small = parametro_alfa_gravitacional(m_opt * 0.1)
        alpha_large = parametro_alfa_gravitacional(m_opt * 10.0)
        self.assertLess(alpha_small, alpha_large)

    def test_alpha_invalid_mass_raises(self):
        """Non-positive BH mass raises ValueError."""
        with self.assertRaises(ValueError):
            parametro_alfa_gravitacional(0.0)
        with self.assertRaises(ValueError):
            parametro_alfa_gravitacional(-1e30)

    def test_frecuencia_compton_equals_f0_angular(self):
        """ω_C = m_ψ c²/ℏ equals 2π f₀ (Compton frequency ≡ f₀ angular frequency)."""
        omega_c = frecuencia_compton_tejido()
        omega_f0 = 2.0 * math.pi * F0_HZ
        self.assertAlmostEqual(omega_c, omega_f0, delta=omega_f0 * 1e-4,
                               msg="ω_Compton should equal 2π·f₀ = 2π×141.7001 rad/s")

    def test_superradiancia_condition_true(self):
        """Mode below threshold satisfies superradiance condition."""
        omega_mode = 100.0    # rad/s
        omega_horizon = 200.0  # rad/s
        self.assertTrue(condicion_superradiancia(omega_mode, omega_horizon))

    def test_superradiancia_condition_false(self):
        """Mode above threshold does NOT satisfy superradiance condition."""
        omega_mode = 300.0
        omega_horizon = 200.0
        self.assertFalse(condicion_superradiancia(omega_mode, omega_horizon))

    def test_superradiancia_azimuthal_mode(self):
        """Azimuthal mode m=2 doubles the threshold frequency."""
        omega_mode = 350.0
        omega_horizon = 200.0
        # m=1: 350 > 200 → False
        self.assertFalse(condicion_superradiancia(omega_mode, omega_horizon, 1))
        # m=2: 350 < 400 → True
        self.assertTrue(condicion_superradiancia(omega_mode, omega_horizon, 2))

    def test_superradiancia_invalid_mode_raises(self):
        """Azimuthal mode m < 1 raises ValueError."""
        with self.assertRaises(ValueError):
            condicion_superradiancia(100.0, 200.0, modo_azimutal=0)


class TestCalcularTejido(unittest.TestCase):
    """Integration test: calcular_tejido() summary object."""

    def setUp(self):
        self.tejido = calcular_tejido()

    def test_returns_tejido_cosmologico(self):
        """calcular_tejido() returns a TejidoCosmologico instance."""
        self.assertIsInstance(self.tejido, TejidoCosmologico)

    def test_f0_correct(self):
        """f₀ in the summary equals F0_HZ."""
        self.assertAlmostEqual(self.tejido.f0_hz, F0_HZ, places=4)

    def test_masa_eV_correct(self):
        """m_ψ in eV/c² ≈ 5.86×10⁻¹³."""
        self.assertAlmostEqual(self.tejido.masa_eV, 5.86e-13, delta=0.02e-13)

    def test_lambda_correct(self):
        """λ ≈ 4.8×10⁻⁴¹."""
        self.assertAlmostEqual(self.tejido.lambda_swampland, 4.8e-41, delta=0.1e-41)

    def test_sigma_below_bullet_cluster(self):
        """σ/m is below the Bullet Cluster limit in summary."""
        self.assertLess(self.tejido.sigma_sobre_masa_cm2_g, BULLET_CLUSTER_LIMIT_CM2_G)

    def test_regimen_dm_ligero(self):
        """Regime classification in summary is 'ligero'."""
        self.assertEqual(self.tejido.regimen_dm, "ligero")

    def test_bh_optima_approx_228(self):
        """Optimal BH mass in summary ≈ 228 M_sun."""
        self.assertAlmostEqual(self.tejido.masa_bh_optima_msun, 228.0, delta=10.0)

    def test_alpha_bh_optimo_near_unity(self):
        """Gravitational α at optimal BH mass ≈ 1."""
        self.assertAlmostEqual(self.tejido.alpha_bh_optimo, 1.0, delta=0.01)

    def test_omega_compton_positive(self):
        """Compton frequency is positive."""
        self.assertGreater(self.tejido.omega_compton_rad_s, 0)


class TestResumenTejido(unittest.TestCase):
    """resumen_tejido() human-readable output."""

    def setUp(self):
        self.resumen = resumen_tejido()

    def test_returns_dict(self):
        """resumen_tejido() returns a dictionary."""
        self.assertIsInstance(self.resumen, dict)

    def test_has_required_keys(self):
        """Summary contains all required parameter keys."""
        required = ["f₀", "m_ψ (kg)", "m_ψ (eV/c²)", "E_ψ (eV)",
                    "Régimen DM", "λ (Swampland)", "σ/m",
                    "Margen Bullet", "M_BH óptima", "α_grav óptimo", "ω_Compton"]
        for key in required:
            self.assertIn(key, self.resumen, f"Key '{key}' missing from summary")

    def test_all_values_are_strings(self):
        """All summary values are formatted strings."""
        for key, value in self.resumen.items():
            self.assertIsInstance(value, str, f"Value for '{key}' should be a string")

    def test_f0_in_summary(self):
        """f₀ value appears correctly in the summary."""
        self.assertIn("141.7001", self.resumen["f₀"])

    def test_regimen_in_summary(self):
        """Dark matter regime appears in summary."""
        self.assertIn("ligero", self.resumen["Régimen DM"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
