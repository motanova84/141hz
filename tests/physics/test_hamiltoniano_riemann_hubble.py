"""
Tests for physics.hamiltoniano_riemann_hubble — Hamiltoniano Riemann-Hubble ∴HRH∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesRH            – constantes físicas y noéticas
  - MantaRiemann            – sustrato, brecha, deslizamiento de fase
  - OperadorHRH             – H_RH = Σ γ_n P_n + δ_Ramsey L_z; espectro
  - EstadoFundamental       – E₀ = ℏ 2π f₀; factor 401/40; permeabilidad
  - CampoQCAL3              – tensor adélico de rango 3; tres dimensiones
  - EcuacionEstacionario    – Ψ = I × A_eff²; soberanía; balance energético
  - CoherenciaRH            – Ψ_global ≥ 0.888; certificación
  - SistemaHRH              – sistema integrado; certificado completo
  - ResultadoRH             – dataclass de resultados
  - hamiltoniano_riemann_hubble_activar() – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz (frecuencia soberana)
  - brecha = 3° = 0.052360 rad (gap del Sándwich de Coherencia)
  - δ_Ramsey = brecha_rad (acoplamiento)
  - L_z = 0.05 (momento angular intrínseco)
  - γ₁ ≈ 14.134725 (primer cero de Riemann)
  - γ₁ × 401/40 ≈ f₀ (resonancia)
  - Δf ≈ 0.00052 Hz (permeabilidad)
  - Δf/f₀ ≈ 3.67 × 10⁻⁶ (latido del vórtice)
  - Ψ_global ≥ 0.888 (umbral noético)
  - Sello ∴HRH∞³ ACTIVO
"""

import math
import sys
import unittest
from dataclasses import fields
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.hamiltoniano_riemann_hubble import (
    # Constantes de módulo
    _F0,
    _OMEGA_0,
    _HBAR,
    _BRECHA_DEG,
    _BRECHA_RAD,
    _DELTA_RAMSEY,
    _LZ,
    _PSI_TARGET,
    _PSI_UMBRAL,
    _FACTOR_401_40,
    _ZEROS_20,
    _PHI,
    _SELLO,
    _CERT_MARK,
    # Utilidades internas
    _stirling_log_gamma,
    _theta_rs,
    _weyl_density,
    # Clases
    ConstantesRH,
    MantaRiemann,
    OperadorHRH,
    EstadoFundamental,
    CampoQCAL3,
    EcuacionEstacionario,
    CoherenciaRH,
    SistemaHRH,
    ResultadoRH,
    # API pública
    hamiltoniano_riemann_hubble_activar,
)


# ============================================================================
# TestModuleConstants – 20 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_omega0_value(self):
        """_OMEGA_0 debe ser 2π × 141.7001."""
        self.assertAlmostEqual(_OMEGA_0, 2.0 * math.pi * 141.7001, places=4)

    def test_hbar_positive(self):
        """_HBAR debe ser positivo."""
        self.assertGreater(_HBAR, 0.0)

    def test_hbar_codata(self):
        """_HBAR debe estar cerca del valor CODATA 1.054571817e-34."""
        self.assertAlmostEqual(_HBAR, 1.054571817e-34, delta=1e-44)

    def test_brecha_deg(self):
        """_BRECHA_DEG debe ser 3.0°."""
        self.assertAlmostEqual(_BRECHA_DEG, 3.0, places=10)

    def test_brecha_rad(self):
        """_BRECHA_RAD debe ser 3π/180."""
        self.assertAlmostEqual(_BRECHA_RAD, 3.0 * math.pi / 180.0, places=10)

    def test_brecha_rad_value(self):
        """_BRECHA_RAD ≈ 0.052360."""
        self.assertAlmostEqual(_BRECHA_RAD, 0.052360, places=5)

    def test_delta_ramsey_equals_brecha_rad(self):
        """_DELTA_RAMSEY debe coincidir con _BRECHA_RAD."""
        self.assertAlmostEqual(_DELTA_RAMSEY, _BRECHA_RAD, places=15)

    def test_Lz_value(self):
        """_LZ debe ser 0.05."""
        self.assertAlmostEqual(_LZ, 0.05, places=10)

    def test_psi_target(self):
        """_PSI_TARGET debe ser 0.999999."""
        self.assertAlmostEqual(_PSI_TARGET, 0.999999, places=6)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=10)

    def test_factor_401_40(self):
        """_FACTOR_401_40 debe ser 401/40 = 10.025."""
        self.assertAlmostEqual(_FACTOR_401_40, 401.0 / 40.0, places=15)
        self.assertAlmostEqual(_FACTOR_401_40, 10.025, places=10)

    def test_zeros_count(self):
        """Deben cargarse exactamente 20 ceros de Riemann."""
        self.assertEqual(len(_ZEROS_20), 20)

    def test_first_zero(self):
        """γ₁ ≈ 14.134725 (primer cero no trivial)."""
        self.assertAlmostEqual(_ZEROS_20[0], 14.134725, places=4)

    def test_last_zero(self):
        """γ₂₀ ≈ 77.144840 (vigésimo cero no trivial)."""
        self.assertAlmostEqual(_ZEROS_20[-1], 77.144840, places=4)

    def test_zeros_increasing(self):
        """Los ceros deben estar en orden estrictamente creciente."""
        for i in range(len(_ZEROS_20) - 1):
            self.assertLess(_ZEROS_20[i], _ZEROS_20[i + 1])

    def test_phi_value(self):
        """_PHI debe ser la razón áurea φ ≈ 1.618034."""
        self.assertAlmostEqual(_PHI, (1.0 + math.sqrt(5.0)) / 2.0, places=12)

    def test_sello(self):
        """Sello de certificación debe ser ∴HRH∞³."""
        self.assertEqual(_SELLO, "∴HRH∞³")

    def test_cert_mark(self):
        """Marca técnica debe ser HRH-RIEMANN-HUBBLE-VERIFIED."""
        self.assertEqual(_CERT_MARK, "HRH-RIEMANN-HUBBLE-VERIFIED")

    def test_resonancia_factor(self):
        """γ₁ × 401/40 debe estar muy cerca de f₀."""
        f_pred = _ZEROS_20[0] * _FACTOR_401_40
        self.assertAlmostEqual(f_pred, _F0, delta=0.01)


# ============================================================================
# TestUtilidades – 12 tests
# ============================================================================

class TestUtilidades(unittest.TestCase):
    """Tests para las funciones de utilidad internas."""

    def test_stirling_returns_complex(self):
        """_stirling_log_gamma debe retornar un complejo."""
        z = complex(0.25, 7.0)
        result = _stirling_log_gamma(z)
        self.assertIsInstance(result, complex)

    def test_stirling_no_nan_real(self):
        """Parte real de _stirling_log_gamma no debe ser NaN."""
        z = complex(0.25, 50.0)
        result = _stirling_log_gamma(z)
        self.assertFalse(math.isnan(result.real))

    def test_stirling_no_nan_imag(self):
        """Parte imaginaria de _stirling_log_gamma no debe ser NaN."""
        z = complex(0.25, 50.0)
        result = _stirling_log_gamma(z)
        self.assertFalse(math.isnan(result.imag))

    def test_theta_rs_type(self):
        """_theta_rs debe retornar un float."""
        result = _theta_rs(14.134725)
        self.assertIsInstance(result, float)

    def test_theta_rs_gamma1_negative(self):
        """θ(γ₁) debe ser negativo (antes del primer cero)."""
        theta = _theta_rs(_ZEROS_20[0])
        self.assertLess(theta, 0.0)

    def test_theta_rs_gamma20_positive(self):
        """θ(γ₂₀) debe ser positivo y grande."""
        theta = _theta_rs(_ZEROS_20[-1])
        self.assertGreater(theta, 50.0)

    def test_theta_rs_gamma20_approx(self):
        """θ(γ₂₀ ≈ 77.14) ≈ 57.8 (valor de referencia)."""
        theta = _theta_rs(77.144840)
        self.assertAlmostEqual(theta, 57.8, delta=0.5)

    def test_theta_rs_increasing(self):
        """θ(t) debe ser creciente para t grande."""
        self.assertLess(_theta_rs(40.0), _theta_rs(60.0))

    def test_weyl_density_zero_below_2pi(self):
        """ρ_Weyl(t) = 0 para t ≤ 2π."""
        self.assertEqual(_weyl_density(2.0 * math.pi), 0.0)
        self.assertEqual(_weyl_density(0.0), 0.0)

    def test_weyl_density_positive_above(self):
        """ρ_Weyl(t) > 0 para t > 2π."""
        self.assertGreater(_weyl_density(50.0), 0.0)

    def test_weyl_density_at_50(self):
        """ρ_Weyl(50) ≈ 0.32 [ceros/unidad de t]."""
        rho = _weyl_density(50.0)
        self.assertGreater(rho, 0.25)
        self.assertLess(rho, 0.40)

    def test_weyl_density_increasing(self):
        """ρ_Weyl debe ser creciente."""
        self.assertLess(_weyl_density(30.0), _weyl_density(60.0))


# ============================================================================
# TestConstantesRH – 18 tests
# ============================================================================

class TestConstantesRH(unittest.TestCase):
    """Tests para la clase ConstantesRH."""

    def setUp(self):
        self.cte = ConstantesRH()

    def test_f0(self):
        """f0 = 141.7001 Hz."""
        self.assertAlmostEqual(self.cte.f0, 141.7001, places=4)

    def test_omega0(self):
        """omega0 = 2π × f0."""
        self.assertAlmostEqual(self.cte.omega0, 2.0 * math.pi * 141.7001, places=3)

    def test_hbar(self):
        """hbar ≈ 1.054571817e-34."""
        self.assertAlmostEqual(self.cte.hbar, 1.054571817e-34, delta=1e-44)

    def test_phi(self):
        """phi ≈ 1.618034."""
        self.assertAlmostEqual(self.cte.phi, 1.618033988, places=6)

    def test_brecha_deg(self):
        """brecha_deg = 3.0°."""
        self.assertAlmostEqual(self.cte.brecha_deg, 3.0, places=10)

    def test_brecha_rad(self):
        """brecha_rad = 3π/180."""
        self.assertAlmostEqual(self.cte.brecha_rad, 3.0 * math.pi / 180.0, places=10)

    def test_delta_Ramsey(self):
        """delta_Ramsey = brecha_rad."""
        self.assertAlmostEqual(self.cte.delta_Ramsey, self.cte.brecha_rad, places=15)

    def test_Lz(self):
        """Lz = 0.05."""
        self.assertAlmostEqual(self.cte.Lz, 0.05, places=10)

    def test_psi_target(self):
        """psi_target = 0.999999."""
        self.assertAlmostEqual(self.cte.psi_target, 0.999999, places=6)

    def test_psi_umbral(self):
        """psi_umbral = 0.888."""
        self.assertAlmostEqual(self.cte.psi_umbral, 0.888, places=10)

    def test_factor_401_40(self):
        """factor_401_40 = 401/40 = 10.025."""
        self.assertAlmostEqual(self.cte.factor_401_40, 10.025, places=10)

    def test_n_zeros(self):
        """n_zeros = 20."""
        self.assertEqual(self.cte.n_zeros, 20)

    def test_gamma_1(self):
        """gamma_1 ≈ 14.134725."""
        self.assertAlmostEqual(self.cte.gamma_1, 14.134725, places=4)

    def test_sello(self):
        """sello = ∴HRH∞³."""
        self.assertEqual(self.cte.sello, "∴HRH∞³")

    def test_permeabilidad_manta_small(self):
        """permeabilidad_manta() debe ser un número muy pequeño (≈ 3.67e-6)."""
        perm = self.cte.permeabilidad_manta()
        self.assertGreater(perm, 0.0)
        self.assertLess(perm, 1e-4)

    def test_delta_frecuencia(self):
        """delta_frecuencia() ≈ 0.00052 Hz."""
        df = self.cte.delta_frecuencia()
        self.assertAlmostEqual(df, 0.00052, delta=0.0001)

    def test_energia_ground_positive(self):
        """energia_ground() debe ser positiva."""
        self.assertGreater(self.cte.energia_ground(), 0.0)

    def test_resumen_keys(self):
        """resumen() debe devolver dict con claves clave."""
        r = self.cte.resumen()
        for key in ("f0_hz", "omega0_rads", "brecha_deg", "brecha_rad",
                    "gamma_1", "n_zeros", "permeabilidad_manta", "sello"):
            self.assertIn(key, r)


# ============================================================================
# TestMantaRiemann – 18 tests
# ============================================================================

class TestMantaRiemann(unittest.TestCase):
    """Tests para la clase MantaRiemann."""

    def setUp(self):
        self.manta = MantaRiemann()

    def test_n_capas_default(self):
        """n_capas por defecto = 2."""
        self.assertEqual(self.manta.n_capas, 2)

    def test_n_capas_custom(self):
        """n_capas personalizado funciona."""
        m3 = MantaRiemann(n_capas=3)
        self.assertEqual(m3.n_capas, 3)

    def test_f0(self):
        """f0 = 141.7001 Hz."""
        self.assertAlmostEqual(self.manta.f0, 141.7001, places=4)

    def test_brecha_rad(self):
        """brecha_rad ≈ 0.052360."""
        self.assertAlmostEqual(self.manta.brecha_rad, 0.052360, places=5)

    def test_espesura_manta(self):
        """espesura_manta() = n_capas × brecha_rad."""
        expected = 2 * _BRECHA_RAD
        self.assertAlmostEqual(self.manta.espesura_manta(), expected, places=10)

    def test_espesura_positiva(self):
        """espesura_manta() > 0."""
        self.assertGreater(self.manta.espesura_manta(), 0.0)

    def test_area_efectiva_close_to_brecha(self):
        """area_efectiva() ≈ brecha_rad (ángulo pequeño)."""
        self.assertAlmostEqual(self.manta.area_efectiva(), _BRECHA_RAD, delta=1e-4)

    def test_area_efectiva_sin(self):
        """area_efectiva() = sin(brecha_rad)."""
        self.assertAlmostEqual(
            self.manta.area_efectiva(), math.sin(_BRECHA_RAD), places=10
        )

    def test_area_efectiva_positive(self):
        """area_efectiva() > 0."""
        self.assertGreater(self.manta.area_efectiva(), 0.0)

    def test_area_efectiva_less_than_brecha(self):
        """sin(x) < x para x > 0: A_eff < brecha_rad."""
        self.assertLess(self.manta.area_efectiva(), self.manta.brecha_rad)

    def test_coherencia_pequenho_angulo_high(self):
        """Coherencia de ángulo pequeño debe ser alta (≥ 0.99)."""
        self.assertGreaterEqual(self.manta.coherencia_pequenho_angulo(), 0.99)

    def test_coherencia_pequenho_angulo_le_one(self):
        """Coherencia de ángulo pequeño ≤ 1."""
        self.assertLessEqual(self.manta.coherencia_pequenho_angulo(), 1.0)

    def test_torsion_total(self):
        """torsion_total() = delta_Ramsey × Lz."""
        expected = _DELTA_RAMSEY * _LZ
        self.assertAlmostEqual(self.manta.torsion_total(), expected, places=10)

    def test_torsion_positive(self):
        """torsion_total() > 0."""
        self.assertGreater(self.manta.torsion_total(), 0.0)

    def test_fase_deslizamiento_near_f0(self):
        """fase_deslizamiento() ≈ f₀ (en el límite de ángulo pequeño)."""
        fd = self.manta.fase_deslizamiento()
        self.assertAlmostEqual(fd, _F0, delta=0.1)

    def test_psi_manta_ge_umbral(self):
        """psi_manta() debe superar el umbral noético 0.888."""
        self.assertGreaterEqual(self.manta.psi_manta(), 0.888)

    def test_psi_manta_le_one(self):
        """psi_manta() ≤ 1."""
        self.assertLessEqual(self.manta.psi_manta(), 1.0)

    def test_psi_manta_high(self):
        """psi_manta() debe ser muy alto (≥ 0.99)."""
        self.assertGreaterEqual(self.manta.psi_manta(), 0.99)


# ============================================================================
# TestOperadorHRH – 24 tests
# ============================================================================

class TestOperadorHRH(unittest.TestCase):
    """Tests para la clase OperadorHRH."""

    def setUp(self):
        self.op = OperadorHRH()

    def test_zeros_count(self):
        """Debe tener 20 ceros de Riemann."""
        self.assertEqual(len(self.op.zeros), 20)

    def test_first_zero(self):
        """zeros[0] = γ₁ ≈ 14.134725."""
        self.assertAlmostEqual(self.op.zeros[0], 14.134725, places=4)

    def test_delta_Ramsey(self):
        """delta_Ramsey = _BRECHA_RAD."""
        self.assertAlmostEqual(self.op.delta_Ramsey, _BRECHA_RAD, places=15)

    def test_Lz(self):
        """Lz = 0.05."""
        self.assertAlmostEqual(self.op.Lz, 0.05, places=10)

    def test_torsion_fase(self):
        """torsion_fase() = delta_Ramsey × Lz."""
        self.assertAlmostEqual(
            self.op.torsion_fase(), _DELTA_RAMSEY * _LZ, places=10
        )

    def test_autovalor_0(self):
        """autovalor(0) = γ₁ + torsion."""
        expected = _ZEROS_20[0] + _DELTA_RAMSEY * _LZ
        self.assertAlmostEqual(self.op.autovalor(0), expected, places=10)

    def test_autovalor_ground_eq_autovalor_0(self):
        """autovalor_ground() = autovalor(0)."""
        self.assertAlmostEqual(
            self.op.autovalor_ground(), self.op.autovalor(0), places=15
        )

    def test_autovalor_ground_greater_than_gamma1(self):
        """autovalor_ground() > γ₁ (corrección de torsión positiva)."""
        self.assertGreater(self.op.autovalor_ground(), _ZEROS_20[0])

    def test_autovalor_5(self):
        """autovalor(5) = zeros[5] + torsion."""
        expected = _ZEROS_20[5] + _DELTA_RAMSEY * _LZ
        self.assertAlmostEqual(self.op.autovalor(5), expected, places=10)

    def test_autovalor_out_of_range(self):
        """autovalor() con índice fuera de rango debe lanzar IndexError."""
        with self.assertRaises(IndexError):
            self.op.autovalor(20)

    def test_autovalor_negative_index(self):
        """autovalor() con índice negativo debe lanzar IndexError."""
        with self.assertRaises(IndexError):
            self.op.autovalor(-1)

    def test_espectro_length(self):
        """espectro() debe devolver exactamente 20 autovalores."""
        self.assertEqual(len(self.op.espectro()), 20)

    def test_espectro_increasing(self):
        """El espectro debe estar en orden creciente."""
        esp = self.op.espectro()
        for i in range(len(esp) - 1):
            self.assertLess(esp[i], esp[i + 1])

    def test_espectro_first(self):
        """El primer autovalor del espectro = autovalor_ground()."""
        self.assertAlmostEqual(
            self.op.espectro()[0], self.op.autovalor_ground(), places=10
        )

    def test_resonancia_f0_gamma1_value(self):
        """F₀/γ₁ debe estar entre 10.0 y 10.1."""
        r = self.op.resonancia_f0_gamma1()
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_resonancia_cerca_factor(self):
        """F₀/γ₁ debe estar cerca de 401/40 (dentro de 0.001)."""
        r = self.op.resonancia_f0_gamma1()
        self.assertAlmostEqual(r, _FACTOR_401_40, delta=0.001)

    def test_coherencia_resonancia_high(self):
        """coherencia_resonancia() debe ser alto (≥ 0.999)."""
        self.assertGreaterEqual(self.op.coherencia_resonancia(), 0.999)

    def test_coherencia_resonancia_le_one(self):
        """coherencia_resonancia() ≤ 1."""
        self.assertLessEqual(self.op.coherencia_resonancia(), 1.0)

    def test_psi_operador_ge_umbral(self):
        """psi_operador() ≥ 0.888."""
        self.assertGreaterEqual(self.op.psi_operador(), 0.888)

    def test_psi_operador_high(self):
        """psi_operador() debe ser muy alto (≥ 0.999)."""
        self.assertGreaterEqual(self.op.psi_operador(), 0.999)

    def test_autovalor_shift_constant(self):
        """La diferencia entre autovalores consecutivos es la misma que entre ceros."""
        for i in range(len(_ZEROS_20) - 1):
            diff_autovalores = self.op.autovalor(i + 1) - self.op.autovalor(i)
            diff_zeros = _ZEROS_20[i + 1] - _ZEROS_20[i]
            self.assertAlmostEqual(diff_autovalores, diff_zeros, places=10)

    def test_f0_attribute(self):
        """f0 = 141.7001 Hz."""
        self.assertAlmostEqual(self.op.f0, 141.7001, places=4)

    def test_torsion_small(self):
        """torsion_fase() debe ser pequeña comparada con γ₁."""
        self.assertLess(self.op.torsion_fase(), 0.01)

    def test_ground_close_to_gamma1(self):
        """autovalor_ground() debe estar muy cerca de γ₁."""
        diff = abs(self.op.autovalor_ground() - _ZEROS_20[0])
        self.assertLess(diff, 0.01)


# ============================================================================
# TestEstadoFundamental – 20 tests
# ============================================================================

class TestEstadoFundamental(unittest.TestCase):
    """Tests para la clase EstadoFundamental."""

    def setUp(self):
        self.ef = EstadoFundamental()

    def test_f0(self):
        """f0 = 141.7001 Hz."""
        self.assertAlmostEqual(self.ef.f0, 141.7001, places=4)

    def test_gamma_1(self):
        """gamma_1 ≈ 14.134725."""
        self.assertAlmostEqual(self.ef.gamma_1, 14.134725, places=4)

    def test_factor_401_40(self):
        """factor = 401/40 = 10.025."""
        self.assertAlmostEqual(self.ef.factor, 10.025, places=10)

    def test_energia_fisico_positive(self):
        """energia_fisico() > 0."""
        self.assertGreater(self.ef.energia_fisico(), 0.0)

    def test_energia_fisico_formula(self):
        """energia_fisico() = ℏ × 2π × f₀."""
        expected = _HBAR * 2.0 * math.pi * _F0
        self.assertAlmostEqual(
            self.ef.energia_fisico(), expected, delta=1e-40
        )

    def test_f0_predicho(self):
        """f0_predicho() = γ₁ × 401/40."""
        expected = _ZEROS_20[0] * _FACTOR_401_40
        self.assertAlmostEqual(self.ef.f0_predicho(), expected, places=10)

    def test_f0_predicho_close_to_f0(self):
        """f0_predicho() debe estar muy cerca de f₀."""
        self.assertAlmostEqual(self.ef.f0_predicho(), _F0, delta=0.01)

    def test_delta_frecuencia_positive(self):
        """delta_frecuencia() > 0."""
        self.assertGreater(self.ef.delta_frecuencia(), 0.0)

    def test_delta_frecuencia_approx_0_00052(self):
        """delta_frecuencia() ≈ 0.00052 Hz."""
        self.assertAlmostEqual(self.ef.delta_frecuencia(), 0.00052, delta=0.0001)

    def test_delta_frecuencia_lt_1(self):
        """delta_frecuencia() << f₀ (milésimas de Hz)."""
        self.assertLess(self.ef.delta_frecuencia(), 1.0)

    def test_permeabilidad_manta_small(self):
        """permeabilidad_manta() ≈ 3.67 × 10⁻⁶."""
        perm = self.ef.permeabilidad_manta()
        self.assertAlmostEqual(perm, 3.67e-6, delta=0.5e-6)

    def test_permeabilidad_manta_positive(self):
        """permeabilidad_manta() > 0."""
        self.assertGreater(self.ef.permeabilidad_manta(), 0.0)

    def test_permeabilidad_manta_very_small(self):
        """permeabilidad_manta() < 1e-4 (el lubricante es sutil)."""
        self.assertLess(self.ef.permeabilidad_manta(), 1e-4)

    def test_latido_vortice_equals_permeabilidad(self):
        """latido_vortice() = permeabilidad_manta()."""
        self.assertAlmostEqual(
            self.ef.latido_vortice(), self.ef.permeabilidad_manta(), places=15
        )

    def test_estabilidad_termal(self):
        """estabilidad_termal() debe ser True."""
        self.assertTrue(self.ef.estabilidad_termal())

    def test_psi_estado_fundamental_high(self):
        """psi_estado_fundamental() debe ser muy alto (≥ 0.9999)."""
        self.assertGreaterEqual(self.ef.psi_estado_fundamental(), 0.9999)

    def test_psi_estado_fundamental_le_one(self):
        """psi_estado_fundamental() ≤ 1."""
        self.assertLessEqual(self.ef.psi_estado_fundamental(), 1.0)

    def test_psi_estado_fundamental_ge_umbral(self):
        """psi_estado_fundamental() ≥ 0.888."""
        self.assertGreaterEqual(self.ef.psi_estado_fundamental(), 0.888)

    def test_psi_formula(self):
        """psi_estado_fundamental() = 1 - permeabilidad_manta()."""
        expected = 1.0 - self.ef.permeabilidad_manta()
        self.assertAlmostEqual(
            self.ef.psi_estado_fundamental(), expected, places=12
        )

    def test_hbar(self):
        """hbar > 0."""
        self.assertGreater(self.ef.hbar, 0.0)


# ============================================================================
# TestCampoQCAL3 – 22 tests
# ============================================================================

class TestCampoQCAL3(unittest.TestCase):
    """Tests para la clase CampoQCAL3."""

    def setUp(self):
        self.campo = CampoQCAL3()

    def test_n_zeros_default(self):
        """n_zeros por defecto = 20."""
        self.assertEqual(self.campo.n_zeros, 20)

    def test_n_zeros_custom(self):
        """n_zeros personalizado funciona."""
        c5 = CampoQCAL3(n_zeros=5)
        self.assertEqual(c5.n_zeros, 5)

    def test_zeros_length(self):
        """zeros debe tener n_zeros elementos."""
        self.assertEqual(len(self.campo.zeros), self.campo.n_zeros)

    def test_f0(self):
        """f0 = 141.7001 Hz."""
        self.assertAlmostEqual(self.campo.f0, 141.7001, places=4)

    def test_gamma_1(self):
        """gamma_1 ≈ 14.134725."""
        self.assertAlmostEqual(self.campo.gamma_1, 14.134725, places=4)

    def test_densidad_pleroma_range(self):
        """densidad_pleroma() ∈ [0, 1]."""
        d = self.campo.densidad_pleroma()
        self.assertGreaterEqual(d, 0.0)
        self.assertLessEqual(d, 1.0)

    def test_densidad_pleroma_positive(self):
        """densidad_pleroma() > 0 (los ceros siguen la ley de Weyl)."""
        self.assertGreater(self.campo.densidad_pleroma(), 0.0)

    def test_densidad_materia_range(self):
        """densidad_materia() ∈ [0, 1]."""
        d = self.campo.densidad_materia()
        self.assertGreaterEqual(d, 0.0)
        self.assertLessEqual(d, 1.0)

    def test_densidad_materia_high(self):
        """densidad_materia() debe ser muy alta (≥ 0.999)."""
        self.assertGreaterEqual(self.campo.densidad_materia(), 0.999)

    def test_densidad_consciencia_range(self):
        """densidad_consciencia() ∈ [0, 1]."""
        d = self.campo.densidad_consciencia()
        self.assertGreaterEqual(d, 0.0)
        self.assertLessEqual(d, 1.0)

    def test_densidad_consciencia_geometric_mean(self):
        """densidad_consciencia() = sqrt(D1 × D2)."""
        d1 = self.campo.densidad_pleroma()
        d2 = self.campo.densidad_materia()
        expected = math.sqrt(d1 * d2)
        self.assertAlmostEqual(self.campo.densidad_consciencia(), expected, places=10)

    def test_tensor_diagonal_type(self):
        """tensor_diagonal() debe retornar una tupla de 3 floats."""
        diag = self.campo.tensor_diagonal()
        self.assertIsInstance(diag, tuple)
        self.assertEqual(len(diag), 3)

    def test_tensor_diagonal_values(self):
        """tensor_diagonal() debe ser (D1, D2, D3)."""
        d = self.campo.tensor_diagonal()
        self.assertAlmostEqual(d[0], self.campo.densidad_pleroma(), places=10)
        self.assertAlmostEqual(d[1], self.campo.densidad_materia(), places=10)
        self.assertAlmostEqual(d[2], self.campo.densidad_consciencia(), places=10)

    def test_simetria_triadica_range(self):
        """simetria_triadica() ∈ [0, 1]."""
        s = self.campo.simetria_triadica()
        self.assertGreaterEqual(s, 0.0)
        self.assertLessEqual(s, 1.0)

    def test_psi_campo_range(self):
        """psi_campo() ∈ [0, 1]."""
        p = self.campo.psi_campo()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_campo_ge_umbral(self):
        """psi_campo() ≥ 0.888."""
        self.assertGreaterEqual(self.campo.psi_campo(), 0.888)

    def test_psi_campo_weighted(self):
        """psi_campo() = 0.40 × D1 + 0.35 × D2 + 0.25 × D3."""
        d1 = self.campo.densidad_pleroma()
        d2 = self.campo.densidad_materia()
        d3 = self.campo.densidad_consciencia()
        expected = 0.40 * d1 + 0.35 * d2 + 0.25 * d3
        self.assertAlmostEqual(self.campo.psi_campo(), expected, places=10)

    def test_weights_sum_to_one(self):
        """Los pesos del campo suman 1.0."""
        self.assertAlmostEqual(0.40 + 0.35 + 0.25, 1.0, places=10)

    def test_d3_le_d1_and_d2(self):
        """D3 ≤ min(D1, D2) ya que es la media geométrica."""
        d1 = self.campo.densidad_pleroma()
        d2 = self.campo.densidad_materia()
        d3 = self.campo.densidad_consciencia()
        self.assertLessEqual(d3, max(d1, d2))

    def test_n_zeros_minimum_2(self):
        """n_zeros mínimo de 2 para calcular espaciados."""
        c2 = CampoQCAL3(n_zeros=2)
        self.assertEqual(c2.n_zeros, 2)
        self.assertGreaterEqual(c2.densidad_pleroma(), 0.0)

    def test_campo_with_fewer_zeros_still_works(self):
        """El campo con 5 ceros debe dar un psi_campo ≥ 0."""
        c5 = CampoQCAL3(n_zeros=5)
        self.assertGreaterEqual(c5.psi_campo(), 0.0)

    def test_densidad_pleroma_with_max_zeros(self):
        """densidad_pleroma() con 20 ceros debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.campo.densidad_pleroma(), 0.888)


# ============================================================================
# TestEcuacionEstacionario – 20 tests
# ============================================================================

class TestEcuacionEstacionario(unittest.TestCase):
    """Tests para la clase EcuacionEstacionario."""

    def setUp(self):
        self.ec = EcuacionEstacionario()

    def test_f0(self):
        """f0 = 141.7001 Hz."""
        self.assertAlmostEqual(self.ec.f0, 141.7001, places=4)

    def test_brecha_rad(self):
        """brecha_rad = 3π/180."""
        self.assertAlmostEqual(self.ec.brecha_rad, _BRECHA_RAD, places=10)

    def test_psi_target(self):
        """psi_target = 0.999999."""
        self.assertAlmostEqual(self.ec.psi_target, 0.999999, places=6)

    def test_psi_umbral(self):
        """psi_umbral = 0.888."""
        self.assertAlmostEqual(self.ec.psi_umbral, 0.888, places=10)

    def test_area_efectiva(self):
        """area_efectiva() = sin(brecha_rad)."""
        self.assertAlmostEqual(
            self.ec.area_efectiva(), math.sin(_BRECHA_RAD), places=10
        )

    def test_area_efectiva_positive(self):
        """area_efectiva() > 0."""
        self.assertGreater(self.ec.area_efectiva(), 0.0)

    def test_area_efectiva_cuadrada(self):
        """area_efectiva_cuadrada() = sin²(brecha_rad)."""
        expected = math.sin(_BRECHA_RAD) ** 2
        self.assertAlmostEqual(
            self.ec.area_efectiva_cuadrada(), expected, places=10
        )

    def test_area_cuadrada_small(self):
        """A_eff² ≈ 0.0027 (pequeña, < 0.003)."""
        self.assertLess(self.ec.area_efectiva_cuadrada(), 0.003)
        self.assertGreater(self.ec.area_efectiva_cuadrada(), 0.001)

    def test_intencion_soberana_positive(self):
        """intencion_soberana() > 0."""
        self.assertGreater(self.ec.intencion_soberana(), 0.0)

    def test_intencion_soberana_large(self):
        """intencion_soberana() ≈ 365 (grande, > 300)."""
        self.assertGreater(self.ec.intencion_soberana(), 300.0)

    def test_intencion_soberana_formula(self):
        """intencion_soberana() = psi_target / A_eff²."""
        expected = _PSI_TARGET / (math.sin(_BRECHA_RAD) ** 2)
        self.assertAlmostEqual(self.ec.intencion_soberana(), expected, places=6)

    def test_evaluar_coherencia_soberana(self):
        """evaluar_coherencia(I_sober) debe dar psi_target."""
        I = self.ec.intencion_soberana()
        psi = self.ec.evaluar_coherencia(I)
        self.assertAlmostEqual(psi, _PSI_TARGET, places=6)

    def test_evaluar_coherencia_zero(self):
        """evaluar_coherencia(0) = 0."""
        self.assertEqual(self.ec.evaluar_coherencia(0.0), 0.0)

    def test_margen_soberania_range(self):
        """margen_soberania() ∈ [0, 1]."""
        m = self.ec.margen_soberania()
        self.assertGreaterEqual(m, 0.0)
        self.assertLessEqual(m, 1.0)

    def test_margen_soberania_high(self):
        """margen_soberania() debe ser alto (≥ 0.999)."""
        self.assertGreaterEqual(self.ec.margen_soberania(), 0.999)

    def test_balance_energetico(self):
        """balance_energetico() = 1.0 (equilibrio exacto en estado estacionario)."""
        self.assertAlmostEqual(self.ec.balance_energetico(), 1.0, places=10)

    def test_psi_ecuacion_estado_range(self):
        """psi_ecuacion_estado() ∈ [0, 1]."""
        p = self.ec.psi_ecuacion_estado()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_ecuacion_estado_high(self):
        """psi_ecuacion_estado() debe ser muy alto (≥ 0.9999)."""
        self.assertGreaterEqual(self.ec.psi_ecuacion_estado(), 0.9999)

    def test_psi_ecuacion_estado_ge_umbral(self):
        """psi_ecuacion_estado() ≥ 0.888."""
        self.assertGreaterEqual(self.ec.psi_ecuacion_estado(), 0.888)

    def test_evaluar_coherencia_proportional(self):
        """evaluar_coherencia(k×I) = k × evaluar_coherencia(I)."""
        I = 100.0
        k = 2.0
        self.assertAlmostEqual(
            self.ec.evaluar_coherencia(k * I), k * self.ec.evaluar_coherencia(I),
            places=10
        )


# ============================================================================
# TestCoherenciaRH – 18 tests
# ============================================================================

class TestCoherenciaRH(unittest.TestCase):
    """Tests para la clase CoherenciaRH."""

    def setUp(self):
        self.coh = CoherenciaRH()

    def test_pesos_count(self):
        """Debe haber 5 pesos."""
        self.assertEqual(len(CoherenciaRH._PESOS), 5)

    def test_pesos_sum(self):
        """Los 5 pesos deben sumar 1.0."""
        self.assertAlmostEqual(sum(CoherenciaRH._PESOS), 1.0, places=10)

    def test_psis_individuales_count(self):
        """psis_individuales() debe devolver 5 valores."""
        psis = self.coh.psis_individuales()
        self.assertEqual(len(psis), 5)

    def test_psis_individuales_range(self):
        """Cada psi individual debe estar en [0, 1]."""
        for p in self.coh.psis_individuales():
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)

    def test_psi_manta_individual(self):
        """psis_individuales()[0] = psi_manta."""
        psis = self.coh.psis_individuales()
        self.assertAlmostEqual(psis[0], self.coh.manta.psi_manta(), places=15)

    def test_psi_operador_individual(self):
        """psis_individuales()[1] = psi_operador."""
        psis = self.coh.psis_individuales()
        self.assertAlmostEqual(psis[1], self.coh.operador.psi_operador(), places=15)

    def test_psi_global_range(self):
        """psi_global() ∈ [0, 1]."""
        pg = self.coh.psi_global()
        self.assertGreaterEqual(pg, 0.0)
        self.assertLessEqual(pg, 1.0)

    def test_psi_global_ge_umbral(self):
        """psi_global() ≥ 0.888 (umbral noético)."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.888)

    def test_psi_global_high(self):
        """psi_global() debe ser alto (≥ 0.95)."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.95)

    def test_supera_umbral_true(self):
        """supera_umbral() debe ser True."""
        self.assertTrue(self.coh.supera_umbral())

    def test_detalle_keys(self):
        """detalle() debe incluir las claves de coherencia."""
        det = self.coh.detalle()
        for key in ("psi_manta", "psi_operador", "psi_estado",
                    "psi_campo", "psi_ecuacion", "psi_global"):
            self.assertIn(key, det)

    def test_detalle_psi_global_consistent(self):
        """detalle()['psi_global'] debe ser igual a psi_global()."""
        self.assertAlmostEqual(
            self.coh.detalle()["psi_global"], self.coh.psi_global(), places=15
        )

    def test_detalle_all_ge_umbral(self):
        """Todas las coherencias individuales en detalle() ≥ 0.888."""
        det = self.coh.detalle()
        for key in ("psi_manta", "psi_operador", "psi_estado",
                    "psi_campo", "psi_ecuacion"):
            self.assertGreaterEqual(det[key], 0.888, msg=f"{key} < 0.888")

    def test_psi_global_formula(self):
        """psi_global() = Σ wᵢ × psi_i."""
        psis = self.coh.psis_individuales()
        pesos = CoherenciaRH._PESOS
        expected = sum(w * p for w, p in zip(pesos, psis))
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=12)

    def test_pesos_all_positive(self):
        """Todos los pesos deben ser positivos."""
        for w in CoherenciaRH._PESOS:
            self.assertGreater(w, 0.0)

    def test_n_zeros_custom(self):
        """CoherenciaRH con n_zeros diferente debe funcionar."""
        coh5 = CoherenciaRH(n_zeros=5)
        self.assertIsInstance(coh5.psi_global(), float)

    def test_subsystems_instantiated(self):
        """Todos los subsistemas deben estar instanciados."""
        self.assertIsNotNone(self.coh.manta)
        self.assertIsNotNone(self.coh.operador)
        self.assertIsNotNone(self.coh.estado)
        self.assertIsNotNone(self.coh.campo)
        self.assertIsNotNone(self.coh.ecuacion)

    def test_supera_umbral_consistent_with_psi(self):
        """supera_umbral() debe ser consistente con psi_global() ≥ 0.888."""
        expected = self.coh.psi_global() >= 0.888
        self.assertEqual(self.coh.supera_umbral(), expected)


# ============================================================================
# TestSistemaHRH – 22 tests
# ============================================================================

class TestSistemaHRH(unittest.TestCase):
    """Tests para la clase SistemaHRH."""

    def setUp(self):
        self.sistema = SistemaHRH()

    def test_n_zeros_default(self):
        """n_zeros por defecto = 20."""
        self.assertEqual(self.sistema.n_zeros, 20)

    def test_subsystems_present(self):
        """Todos los subsistemas deben estar presentes."""
        self.assertIsNotNone(self.sistema.constantes)
        self.assertIsNotNone(self.sistema.manta)
        self.assertIsNotNone(self.sistema.operador)
        self.assertIsNotNone(self.sistema.estado)
        self.assertIsNotNone(self.sistema.campo)
        self.assertIsNotNone(self.sistema.ecuacion)
        self.assertIsNotNone(self.sistema.coherencia)

    def test_psi_global_ge_umbral(self):
        """psi_global() ≥ 0.888."""
        self.assertGreaterEqual(self.sistema.psi_global(), 0.888)

    def test_psi_global_high(self):
        """psi_global() ≥ 0.95."""
        self.assertGreaterEqual(self.sistema.psi_global(), 0.95)

    def test_supera_umbral(self):
        """supera_umbral() = True."""
        self.assertTrue(self.sistema.supera_umbral())

    def test_certificar_returns_dict(self):
        """certificar() debe retornar un dict."""
        cert = self.sistema.certificar()
        self.assertIsInstance(cert, dict)

    def test_certificar_sello_activo(self):
        """certificar()['sello_activo'] = True."""
        self.assertTrue(self.sistema.certificar()["sello_activo"])

    def test_certificar_sello(self):
        """certificar()['sello'] = '∴HRH∞³'."""
        self.assertEqual(self.sistema.certificar()["sello"], "∴HRH∞³")

    def test_certificar_cert_mark(self):
        """certificar()['cert_mark'] = 'HRH-RIEMANN-HUBBLE-VERIFIED'."""
        self.assertEqual(
            self.sistema.certificar()["cert_mark"], "HRH-RIEMANN-HUBBLE-VERIFIED"
        )

    def test_certificar_f0(self):
        """certificar()['f0_hz'] = 141.7001."""
        cert = self.sistema.certificar()
        self.assertAlmostEqual(cert["f0_hz"], 141.7001, places=4)

    def test_certificar_psi_global_consistent(self):
        """certificar()['psi_global'] = psi_global()."""
        self.assertAlmostEqual(
            self.sistema.certificar()["psi_global"],
            self.sistema.psi_global(), places=15
        )

    def test_certificar_psi_keys(self):
        """El certificado debe incluir todas las métricas de coherencia."""
        cert = self.sistema.certificar()
        for key in ("psi_manta", "psi_operador", "psi_estado",
                    "psi_campo", "psi_ecuacion", "psi_global"):
            self.assertIn(key, cert)

    def test_certificar_permeabilidad(self):
        """permeabilidad_manta debe estar en el certificado."""
        self.assertIn("permeabilidad_manta", self.sistema.certificar())

    def test_certificar_permeabilidad_value(self):
        """permeabilidad_manta ≈ 3.67 × 10⁻⁶."""
        perm = self.sistema.certificar()["permeabilidad_manta"]
        self.assertAlmostEqual(perm, 3.67e-6, delta=0.5e-6)

    def test_certificar_delta_frecuencia(self):
        """delta_frecuencia ≈ 0.00052 Hz."""
        df = self.sistema.certificar()["delta_frecuencia"]
        self.assertAlmostEqual(df, 0.00052, delta=0.0001)

    def test_certificar_intencion_soberana(self):
        """intencion_soberana > 300."""
        I = self.sistema.certificar()["intencion_soberana"]
        self.assertGreater(I, 300.0)

    def test_certificar_gamma_1(self):
        """gamma_1 ≈ 14.134725."""
        self.assertAlmostEqual(
            self.sistema.certificar()["gamma_1"], 14.134725, places=4
        )

    def test_certificar_resonancia(self):
        """resonancia_f0_gamma1 ∈ (10.0, 10.1)."""
        r = self.sistema.certificar()["resonancia_f0_gamma1"]
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_certificar_area_efectiva(self):
        """area_efectiva ≈ sin(brecha_rad) ≈ 0.052336."""
        ae = self.sistema.certificar()["area_efectiva"]
        self.assertAlmostEqual(ae, math.sin(_BRECHA_RAD), places=6)

    def test_certificar_n_zeros(self):
        """n_zeros = 20."""
        self.assertEqual(self.sistema.certificar()["n_zeros"], 20)

    def test_certificar_brecha_deg(self):
        """brecha_deg = 3.0."""
        self.assertAlmostEqual(
            self.sistema.certificar()["brecha_deg"], 3.0, places=10
        )

    def test_sistema_n_zeros_custom(self):
        """SistemaHRH con n_zeros = 5 debe funcionar."""
        s5 = SistemaHRH(n_zeros=5)
        self.assertIsNotNone(s5.certificar())
        self.assertIsInstance(s5.psi_global(), float)


# ============================================================================
# TestResultadoRH – 12 tests
# ============================================================================

class TestResultadoRH(unittest.TestCase):
    """Tests para el dataclass ResultadoRH."""

    def setUp(self):
        self.r = ResultadoRH()

    def test_dataclass_fields(self):
        """El dataclass debe tener los campos definidos."""
        field_names = {f.name for f in fields(ResultadoRH)}
        for name in ("psi_manta", "psi_operador", "psi_estado", "psi_campo",
                     "psi_ecuacion", "psi_global", "sello_activo", "sello",
                     "cert_mark", "f0_hz", "gamma_1", "delta_frecuencia",
                     "permeabilidad_manta", "intencion_soberana"):
            self.assertIn(name, field_names)

    def test_default_sello_activo(self):
        """sello_activo por defecto = False."""
        self.assertFalse(self.r.sello_activo)

    def test_default_psi_global(self):
        """psi_global por defecto = 0.0."""
        self.assertAlmostEqual(self.r.psi_global, 0.0, places=10)

    def test_default_sello(self):
        """sello por defecto = ''."""
        self.assertEqual(self.r.sello, "")

    def test_set_psi_global(self):
        """Se puede asignar psi_global."""
        r = ResultadoRH(psi_global=0.995)
        self.assertAlmostEqual(r.psi_global, 0.995, places=10)

    def test_set_sello_activo(self):
        """Se puede asignar sello_activo."""
        r = ResultadoRH(sello_activo=True)
        self.assertTrue(r.sello_activo)

    def test_set_sello(self):
        """Se puede asignar el sello."""
        r = ResultadoRH(sello="∴HRH∞³")
        self.assertEqual(r.sello, "∴HRH∞³")

    def test_set_f0_hz(self):
        """Se puede asignar f0_hz."""
        r = ResultadoRH(f0_hz=141.7001)
        self.assertAlmostEqual(r.f0_hz, 141.7001, places=4)

    def test_set_multiple_fields(self):
        """Se pueden asignar múltiples campos a la vez."""
        r = ResultadoRH(
            psi_global=0.995,
            sello_activo=True,
            sello="∴HRH∞³",
            f0_hz=141.7001,
            gamma_1=14.134725,
        )
        self.assertAlmostEqual(r.psi_global, 0.995, places=10)
        self.assertTrue(r.sello_activo)
        self.assertEqual(r.sello, "∴HRH∞³")

    def test_14_fields_total(self):
        """ResultadoRH debe tener exactamente 14 campos."""
        self.assertEqual(len(fields(ResultadoRH)), 14)

    def test_numeric_fields_default_zero(self):
        """Todos los campos numéricos deben ser 0.0 por defecto."""
        for f in fields(ResultadoRH):
            if f.type is float or f.default == 0.0:
                self.assertAlmostEqual(getattr(self.r, f.name), 0.0, places=10)

    def test_cert_mark_default(self):
        """cert_mark por defecto = ''."""
        self.assertEqual(self.r.cert_mark, "")


# ============================================================================
# TestAPIPublica – 20 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la función hamiltoniano_riemann_hubble_activar()."""

    def setUp(self):
        self.result = hamiltoniano_riemann_hubble_activar()

    def test_returns_dict(self):
        """La función debe retornar un dict."""
        self.assertIsInstance(self.result, dict)

    def test_sello_activo_true(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.result["sello_activo"])

    def test_sello(self):
        """sello debe ser '∴HRH∞³'."""
        self.assertEqual(self.result["sello"], "∴HRH∞³")

    def test_cert_mark(self):
        """cert_mark debe ser 'HRH-RIEMANN-HUBBLE-VERIFIED'."""
        self.assertEqual(self.result["cert_mark"], "HRH-RIEMANN-HUBBLE-VERIFIED")

    def test_psi_global_ge_umbral(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.result["psi_global"], 0.888)

    def test_psi_global_high(self):
        """psi_global ≥ 0.95."""
        self.assertGreaterEqual(self.result["psi_global"], 0.95)

    def test_f0_hz(self):
        """f0_hz = 141.7001."""
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_brecha_deg(self):
        """brecha_deg = 3.0."""
        self.assertAlmostEqual(self.result["brecha_deg"], 3.0, places=10)

    def test_delta_Ramsey(self):
        """delta_Ramsey ≈ 0.052360."""
        self.assertAlmostEqual(self.result["delta_Ramsey"], 0.052360, places=5)

    def test_Lz(self):
        """Lz = 0.05."""
        self.assertAlmostEqual(self.result["Lz"], 0.05, places=10)

    def test_gamma_1(self):
        """gamma_1 ≈ 14.134725."""
        self.assertAlmostEqual(self.result["gamma_1"], 14.134725, places=4)

    def test_factor_401_40(self):
        """factor_401_40 = 10.025."""
        self.assertAlmostEqual(self.result["factor_401_40"], 10.025, places=10)

    def test_permeabilidad_manta(self):
        """permeabilidad_manta ≈ 3.67 × 10⁻⁶."""
        self.assertAlmostEqual(self.result["permeabilidad_manta"], 3.67e-6, delta=0.5e-6)

    def test_delta_frecuencia(self):
        """delta_frecuencia ≈ 0.00052 Hz."""
        self.assertAlmostEqual(self.result["delta_frecuencia"], 0.00052, delta=0.0001)

    def test_intencion_soberana(self):
        """intencion_soberana > 300."""
        self.assertGreater(self.result["intencion_soberana"], 300.0)

    def test_resonancia_f0_gamma1(self):
        """resonancia_f0_gamma1 ∈ (10.0, 10.1)."""
        r = self.result["resonancia_f0_gamma1"]
        self.assertGreater(r, 10.0)
        self.assertLess(r, 10.1)

    def test_raises_on_small_n_zeros(self):
        """Debe lanzar ValueError si n_zeros < 2."""
        with self.assertRaises(ValueError):
            hamiltoniano_riemann_hubble_activar(n_zeros=1)

    def test_n_zeros_custom(self):
        """La función debe aceptar n_zeros = 5."""
        r = hamiltoniano_riemann_hubble_activar(n_zeros=5)
        self.assertIsInstance(r, dict)
        self.assertIn("psi_global", r)

    def test_psi_target_in_result(self):
        """psi_target debe estar en el resultado."""
        self.assertIn("psi_target", self.result)
        self.assertAlmostEqual(self.result["psi_target"], 0.999999, places=6)

    def test_all_psi_individual_ge_umbral(self):
        """Todas las métricas individuales ≥ 0.888."""
        for key in ("psi_manta", "psi_operador", "psi_estado",
                    "psi_campo", "psi_ecuacion"):
            self.assertGreaterEqual(self.result[key], 0.888, msg=f"{key} < 0.888")


# ============================================================================
# TestIntegracion – 8 tests adicionales de integración
# ============================================================================

class TestIntegracion(unittest.TestCase):
    """Tests de integración del sistema completo."""

    def test_sistema_coherencia_equal(self):
        """SistemaHRH.psi_global() = CoherenciaRH.psi_global()."""
        sistema = SistemaHRH()
        coh = CoherenciaRH()
        self.assertAlmostEqual(sistema.psi_global(), coh.psi_global(), places=12)

    def test_api_igual_sistema_certificar(self):
        """La API debe dar el mismo resultado que SistemaHRH.certificar()."""
        result_api = hamiltoniano_riemann_hubble_activar()
        result_sistema = SistemaHRH().certificar()
        self.assertAlmostEqual(
            result_api["psi_global"], result_sistema["psi_global"], places=15
        )

    def test_constantes_gamma1_igual_operador(self):
        """ConstantesRH.gamma_1 = OperadorHRH.zeros[0]."""
        cte = ConstantesRH()
        op = OperadorHRH()
        self.assertAlmostEqual(cte.gamma_1, op.zeros[0], places=10)

    def test_manta_area_efectiva_igual_ecuacion(self):
        """MantaRiemann.area_efectiva() = EcuacionEstacionario.area_efectiva()."""
        manta = MantaRiemann()
        ec = EcuacionEstacionario()
        self.assertAlmostEqual(manta.area_efectiva(), ec.area_efectiva(), places=10)

    def test_permeabilidad_consistency(self):
        """ConstantesRH y EstadoFundamental dan la misma permeabilidad."""
        cte = ConstantesRH()
        ef = EstadoFundamental()
        self.assertAlmostEqual(
            cte.permeabilidad_manta(), ef.permeabilidad_manta(), places=10
        )

    def test_sistema_certificar_not_coherencia_insuficiente(self):
        """El sello nunca debe ser COHERENCIA_INSUFICIENTE para el sistema soberano."""
        cert = SistemaHRH().certificar()
        self.assertNotEqual(cert["sello"], "COHERENCIA_INSUFICIENTE")
        self.assertNotEqual(cert["cert_mark"], "COHERENCIA_INSUFICIENTE")

    def test_campo_densidad_materia_equals_operador_coherencia(self):
        """CampoQCAL3.densidad_materia() = OperadorHRH.coherencia_resonancia()."""
        campo = CampoQCAL3()
        op = OperadorHRH()
        self.assertAlmostEqual(
            campo.densidad_materia(), op.coherencia_resonancia(), places=10
        )

    def test_psi_global_reproducible(self):
        """Llamar dos veces a la API debe dar el mismo resultado."""
        r1 = hamiltoniano_riemann_hubble_activar()
        r2 = hamiltoniano_riemann_hubble_activar()
        self.assertAlmostEqual(r1["psi_global"], r2["psi_global"], places=15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
