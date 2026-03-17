#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║   TEST ESTRUCTURA PICODE 141 Hz — 59 pruebas QCAL Riemann + Holograma     ║
╚════════════════════════════════════════════════════════════════════════════╝

Valida todas las nuevas constantes derivadas de Riemann y las funciones del
módulo de codificación holográfica:

1. Constantes en reloj_universo_f0:
   - GAMMA_1, MULTIPLICADOR_TUYOYOTU, F0_EXACT_HZ
   - DELTA_FASE_ZIUSUDRA, FISURA_ZIUSUDRA, F0_OCTAVA_HZ
   - CONSTANTES_FISICAS (diccionario unificado)

2. Módulo holográfico (modulo_holograma_141hz):
   - area_efectiva_holografica, bits_holograficos_planck
   - espiral_zeta_polar
   - coherencia_holografica
   - simular_eco_lunar, analizar_fft_moonbounce
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from fisica.reloj_universo_f0 import (
    GAMMA_1,
    MULTIPLICADOR_TUYOYOTU,
    F0_EXACT_HZ,
    DELTA_FASE_ZIUSUDRA,
    FISURA_ZIUSUDRA,
    F0_OCTAVA_HZ,
    CONSTANTES_FISICAS,
    F0_FLOAT,
    F0_HZ,
)
from fisica.modulo_holograma_141hz import (
    area_efectiva_holografica,
    bits_holograficos_planck,
    espiral_zeta_polar,
    coherencia_holografica,
    simular_eco_lunar,
    analizar_fft_moonbounce,
    L_PLANCK,
    DELTA_F_VORTICE,
    RADIO_EFECTIVO_M,
)


# ============================================================================
# 1. GAMMA_1 — Primer cero no trivial de ζ(s)
# ============================================================================

class TestGamma1:
    """Tests for the first non-trivial Riemann zero γ₁."""

    def test_gamma1_value_precision(self):
        """γ₁ must match the known value to at least 10 decimal places."""
        assert GAMMA_1 == pytest.approx(14.134725141734693790, abs=1e-10)

    def test_gamma1_positive(self):
        """γ₁ must be strictly positive."""
        assert GAMMA_1 > 0.0

    def test_gamma1_between_14_and_15(self):
        """γ₁ must lie in (14, 15)."""
        assert 14.0 < GAMMA_1 < 15.0

    def test_gamma1_is_float(self):
        """γ₁ must be a Python float (or numeric type)."""
        assert isinstance(GAMMA_1, float)


# ============================================================================
# 2. MULTIPLICADOR_TUYOYOTU — Proporción Tuyoyotu
# ============================================================================

class TestMultiplicadorTuyoyotu:
    """Tests for the Tuyoyotu proportion (10 + 1/40)."""

    def test_multiplicador_value(self):
        """Tuyoyotu multiplier must equal exactly 10.025."""
        assert MULTIPLICADOR_TUYOYOTU == pytest.approx(10.025, abs=1e-12)

    def test_multiplicador_equals_10_plus_1_over_40(self):
        """Tuyoyotu multiplier must equal 10 + 1/40."""
        assert MULTIPLICADOR_TUYOYOTU == pytest.approx(10.0 + 1.0 / 40.0, abs=1e-12)

    def test_multiplicador_greater_than_10(self):
        """Tuyoyotu multiplier must be strictly greater than 10."""
        assert MULTIPLICADOR_TUYOYOTU > 10.0


# ============================================================================
# 3. F0_EXACT_HZ — Frecuencia exacta Riemann
# ============================================================================

class TestF0Exact:
    """Tests for the exact Riemann-derived fundamental frequency."""

    def test_f0_exact_value(self):
        """F0_EXACT_HZ must be ≈ 141.70061954589031 Hz."""
        assert F0_EXACT_HZ == pytest.approx(141.70061954589031, abs=1e-8)

    def test_f0_exact_derivation(self):
        """F0_EXACT_HZ must equal GAMMA_1 × MULTIPLICADOR_TUYOYOTU."""
        assert F0_EXACT_HZ == pytest.approx(GAMMA_1 * MULTIPLICADOR_TUYOYOTU, abs=1e-10)

    def test_f0_exact_between_141_and_142(self):
        """F0_EXACT_HZ must lie in (141, 142) Hz."""
        assert 141.0 < F0_EXACT_HZ < 142.0

    def test_f0_exact_close_to_operative(self):
        """F0_EXACT_HZ must be very close to the operative F0_HZ."""
        assert abs(F0_EXACT_HZ - F0_FLOAT) < 0.01  # within 10 mHz


# ============================================================================
# 4. DELTA_FASE_ZIUSUDRA — Acoplamiento de fase
# ============================================================================

class TestDeltaFaseZiusudra:
    """Tests for the Ziusudra phase coupling δ_fase = γ₁/40."""

    def test_delta_fase_value(self):
        """δ_fase must be ≈ 0.35336812854 Hz."""
        assert DELTA_FASE_ZIUSUDRA == pytest.approx(0.35336812854, abs=1e-8)

    def test_delta_fase_derivation(self):
        """δ_fase must equal GAMMA_1 / 40."""
        assert DELTA_FASE_ZIUSUDRA == pytest.approx(GAMMA_1 / 40.0, abs=1e-12)

    def test_delta_fase_positive(self):
        """δ_fase must be strictly positive."""
        assert DELTA_FASE_ZIUSUDRA > 0.0

    def test_delta_fase_less_than_half_hz(self):
        """δ_fase must be less than 0.5 Hz."""
        assert DELTA_FASE_ZIUSUDRA < 0.5


# ============================================================================
# 5. FISURA_ZIUSUDRA — Brecha entre f₀ exacta y operativa
# ============================================================================

class TestFisuraZiusudra:
    """Tests for the Ziusudra fissure (gap between exact and operative f₀)."""

    def test_fisura_positive(self):
        """Fisura must be positive (F0_EXACT > F0_operative)."""
        assert FISURA_ZIUSUDRA > 0.0

    def test_fisura_value(self):
        """Fisura must be ≈ 5.195×10⁻⁴ Hz."""
        assert FISURA_ZIUSUDRA == pytest.approx(5.195e-4, abs=1e-6)

    def test_fisura_formula(self):
        """Fisura must equal F0_EXACT_HZ − F0_FLOAT."""
        assert FISURA_ZIUSUDRA == pytest.approx(F0_EXACT_HZ - F0_FLOAT, abs=1e-12)

    def test_fisura_small(self):
        """Fisura must be smaller than 0.01 Hz (very small gap)."""
        assert abs(FISURA_ZIUSUDRA) < 0.01


# ============================================================================
# 6. F0_OCTAVA_HZ — Octava superior
# ============================================================================

class TestF0Octava:
    """Tests for the upper octave of the Inhabited System."""

    def test_f0_octava_value(self):
        """F0_OCTAVA_HZ must be 151.7001 Hz."""
        assert F0_OCTAVA_HZ == pytest.approx(151.7001, abs=1e-9)

    def test_f0_octava_greater_than_f0(self):
        """F0_OCTAVA_HZ must be strictly greater than F0_HZ."""
        assert F0_OCTAVA_HZ > F0_FLOAT

    def test_f0_octava_approximately_f0_plus_10(self):
        """F0_OCTAVA_HZ must be approximately F0 + 10 Hz."""
        assert F0_OCTAVA_HZ == pytest.approx(F0_FLOAT + 10.0, abs=1e-4)


# ============================================================================
# 7. CONSTANTES_FISICAS — Diccionario unificado
# ============================================================================

class TestConstantesFisicas:
    """Tests for the unified CONSTANTES_FISICAS dictionary."""

    _REQUIRED_KEYS = [
        'f₀', 'T₀', 'ω₀', 'λ₀', 'E₀',
        'γ₁', 'μ_tuyoyotu', 'f₀_exact', 'δ_fase', 'Δ_fisura', 'f₀_octava',
    ]

    def test_has_required_keys(self):
        """CONSTANTES_FISICAS must contain all required constant keys."""
        for key in self._REQUIRED_KEYS:
            assert key in CONSTANTES_FISICAS, f"Missing key: {key}"

    def test_all_values_are_tuples(self):
        """Each entry must be a 3-tuple (value, unit, description)."""
        for key, entry in CONSTANTES_FISICAS.items():
            assert isinstance(entry, tuple), f"Entry for {key!r} is not a tuple"
            assert len(entry) == 3, f"Entry for {key!r} does not have 3 elements"

    def test_riemann_gamma1_entry(self):
        """CONSTANTES_FISICAS['γ₁'] must match GAMMA_1."""
        val, unit, _ = CONSTANTES_FISICAS['γ₁']
        assert val == pytest.approx(GAMMA_1, abs=1e-12)

    def test_f0_exact_entry(self):
        """CONSTANTES_FISICAS['f₀_exact'] must match F0_EXACT_HZ."""
        val, unit, _ = CONSTANTES_FISICAS['f₀_exact']
        assert val == pytest.approx(F0_EXACT_HZ, abs=1e-10)

    def test_fisura_entry(self):
        """CONSTANTES_FISICAS['Δ_fisura'] must match FISURA_ZIUSUDRA."""
        val, unit, _ = CONSTANTES_FISICAS['Δ_fisura']
        assert val == pytest.approx(FISURA_ZIUSUDRA, abs=1e-12)


# ============================================================================
# 8. area_efectiva_holografica
# ============================================================================

class TestAreaEfectivaHolografica:
    """Tests for the effective holographic area function."""

    def test_default_returns_positive(self):
        """Default call must return a positive area."""
        area = area_efectiva_holografica()
        assert area > 0.0

    def test_scales_inverse_square_with_frequency(self):
        """Area must scale as (c / (2π·f))² — quadratic inverse scaling."""
        a1 = area_efectiva_holografica(100.0)
        a2 = area_efectiva_holografica(200.0)
        assert a1 == pytest.approx(4.0 * a2, rel=1e-10)

    def test_value_at_f0(self):
        """Area at f₀ must match the formula (c/(2π·f₀))²."""
        import math as _m
        from fisica.reloj_universo_f0 import C_LUZ
        expected = (C_LUZ / (2.0 * _m.pi * F0_FLOAT)) ** 2
        assert area_efectiva_holografica(F0_FLOAT) == pytest.approx(expected, rel=1e-10)


# ============================================================================
# 9. bits_holograficos_planck
# ============================================================================

class TestBitsHolograficosPlanck:
    """Tests for the holographic bit count function."""

    def test_positive_for_positive_area(self):
        """Bit count must be positive for any positive area."""
        area = area_efectiva_holografica(F0_FLOAT)
        assert bits_holograficos_planck(area) > 0.0

    def test_scales_linearly_with_area(self):
        """Bit count must scale linearly with area."""
        bits1 = bits_holograficos_planck(1.0)
        bits2 = bits_holograficos_planck(2.0)
        assert bits2 == pytest.approx(2.0 * bits1, rel=1e-10)

    def test_formula(self):
        """Bits = A / (4 · L_Planck²)."""
        area = 1.0
        expected = area / (4.0 * L_PLANCK ** 2)
        assert bits_holograficos_planck(area) == pytest.approx(expected, rel=1e-10)


# ============================================================================
# 10. espiral_zeta_polar
# ============================================================================

class TestEspiralZetaPolar:
    """Tests for the zeta polar spiral function."""

    def test_returns_list(self):
        """espiral_zeta_polar must return a list."""
        result = espiral_zeta_polar(GAMMA_1)
        assert isinstance(result, list)

    def test_default_length_360(self):
        """Default spiral must have 360 points."""
        result = espiral_zeta_polar(GAMMA_1)
        assert len(result) == 360

    def test_custom_length(self):
        """Custom n_puntos must give the requested number of points."""
        result = espiral_zeta_polar(GAMMA_1, n_puntos=100)
        assert len(result) == 100

    def test_each_point_is_4_tuple(self):
        """Each point must be a 4-tuple (x, y, r, theta)."""
        result = espiral_zeta_polar(GAMMA_1, n_puntos=8)
        for point in result:
            assert len(point) == 4

    def test_first_point_at_theta_zero(self):
        """First point must have theta=0 and r=1 (exp(0)=1)."""
        x, y, r, theta = espiral_zeta_polar(GAMMA_1, n_puntos=4)[0]
        assert theta == pytest.approx(0.0, abs=1e-12)
        assert r == pytest.approx(1.0, abs=1e-12)
        assert x == pytest.approx(1.0, abs=1e-12)
        assert y == pytest.approx(0.0, abs=1e-12)

    def test_radius_monotonically_increasing(self):
        """Spiral radius r must increase with theta for positive gamma_n."""
        result = espiral_zeta_polar(GAMMA_1, n_puntos=36)
        radii = [pt[2] for pt in result]
        for i in range(len(radii) - 1):
            assert radii[i] < radii[i + 1], f"Radius not increasing at index {i}"


# ============================================================================
# 11. coherencia_holografica
# ============================================================================

class TestCoherenciaHolografica:
    """Tests for the holographic coherence function Ψ(f)."""

    def test_maximum_at_center(self):
        """Ψ must equal 1.0 at the center frequency F0_EXACT_HZ."""
        assert coherencia_holografica(F0_EXACT_HZ) == pytest.approx(1.0, abs=1e-12)

    def test_decay_at_one_bandwidth(self):
        """Ψ(f₀ ± delta_f) must equal exp(−1) ≈ 0.3679."""
        psi_plus = coherencia_holografica(F0_EXACT_HZ + DELTA_F_VORTICE)
        psi_minus = coherencia_holografica(F0_EXACT_HZ - DELTA_F_VORTICE)
        expected = math.exp(-1.0)
        assert psi_plus == pytest.approx(expected, abs=1e-10)
        assert psi_minus == pytest.approx(expected, abs=1e-10)

    def test_always_in_zero_one_range(self):
        """Ψ must always lie in [0, 1]."""
        for df in [0.0, 0.1, 0.5, 1.0, 5.0]:
            psi = coherencia_holografica(F0_EXACT_HZ + df)
            assert 0.0 <= psi <= 1.0 + 1e-12

    def test_gaussian_formula(self):
        """Ψ(f) = exp(−((f−f_centro)/delta_f)²) must hold at arbitrary f."""
        for df in [0.0, 0.2, 0.4, 0.8]:
            f = F0_EXACT_HZ + df
            expected = math.exp(-((f - F0_EXACT_HZ) / DELTA_F_VORTICE) ** 2)
            assert coherencia_holografica(f) == pytest.approx(expected, abs=1e-12)

    def test_invalid_delta_f_raises(self):
        """A non-positive delta_f must raise ValueError."""
        with pytest.raises(ValueError):
            coherencia_holografica(F0_EXACT_HZ, delta_f=0.0)
        with pytest.raises(ValueError):
            coherencia_holografica(F0_EXACT_HZ, delta_f=-0.1)

    def test_psi_at_operative_f0_less_than_one(self):
        """Ψ at operative f₀ must be < 1 (due to Fisura de Ziusudra)."""
        psi = coherencia_holografica(F0_FLOAT)
        assert psi < 1.0

    def test_psi_at_operative_f0_close_to_one(self):
        """Ψ at operative f₀ must be very close to 1 (Fisura is tiny)."""
        psi = coherencia_holografica(F0_FLOAT)
        assert psi > 0.99


# ============================================================================
# 12. simular_eco_lunar
# ============================================================================

class TestSimularEcoLunar:
    """Tests for the lunar echo simulation function."""

    def test_returns_4_tuple(self):
        """Function must return a 4-tuple (tiempos, total, original, eco)."""
        result = simular_eco_lunar(duracion_s=0.1, fs_hz=1000.0)
        assert len(result) == 4

    def test_output_lengths_match(self):
        """All output arrays must have the same length."""
        tiempos, total, original, eco = simular_eco_lunar(duracion_s=0.1, fs_hz=1000.0)
        n = len(tiempos)
        assert len(total) == n
        assert len(original) == n
        assert len(eco) == n

    def test_sample_count(self):
        """Number of samples must equal int(duracion_s × fs_hz)."""
        tiempos, total, original, eco = simular_eco_lunar(
            duracion_s=0.5, fs_hz=2000.0
        )
        assert len(tiempos) == int(0.5 * 2000.0)

    def test_no_echo_before_delay(self):
        """Eco array must be zero before the delay window."""
        retardo_s = 0.2
        fs_hz = 1000.0
        tiempos, total, original, eco = simular_eco_lunar(
            duracion_s=0.5, fs_hz=fs_hz, retardo_s=retardo_s
        )
        n_retardo = int(retardo_s * fs_hz)
        for i in range(n_retardo):
            assert eco[i] == pytest.approx(0.0, abs=1e-12)

    def test_invalid_duracion_raises(self):
        """Non-positive duracion_s must raise ValueError."""
        with pytest.raises(ValueError):
            simular_eco_lunar(duracion_s=0.0)
        with pytest.raises(ValueError):
            simular_eco_lunar(duracion_s=-1.0)

    def test_invalid_fs_raises(self):
        """Non-positive fs_hz must raise ValueError."""
        with pytest.raises(ValueError):
            simular_eco_lunar(fs_hz=0.0)

    def test_invalid_atenuacion_raises(self):
        """Attenuation outside [0,1] must raise ValueError."""
        with pytest.raises(ValueError):
            simular_eco_lunar(atenuacion=1.5)
        with pytest.raises(ValueError):
            simular_eco_lunar(atenuacion=-0.1)


# ============================================================================
# 13. analizar_fft_moonbounce
# ============================================================================

class TestAnalizarFftMoonbounce:
    """Tests for the moonbounce FFT analysis function."""

    def test_returns_dict_with_required_keys(self):
        """Function must return a dict with f_pico_hz, delta_f_hz, psi_proxy."""
        tiempos, total, _, _ = simular_eco_lunar(
            duracion_s=1.0, fs_hz=2048.0, retardo_s=10.0
        )
        result = analizar_fft_moonbounce(total, fs_hz=2048.0)
        assert isinstance(result, dict)
        for key in ('f_pico_hz', 'delta_f_hz', 'psi_proxy', 'magnitud_pico'):
            assert key in result, f"Missing key: {key}"

    def test_f_pico_positive(self):
        """Peak frequency must be strictly positive."""
        tiempos, total, _, _ = simular_eco_lunar(
            duracion_s=1.0, fs_hz=2048.0, retardo_s=10.0
        )
        result = analizar_fft_moonbounce(total, fs_hz=2048.0)
        assert result['f_pico_hz'] > 0.0

    def test_psi_proxy_in_range(self):
        """Ψ_proxy must lie in (0, 1]."""
        tiempos, total, _, _ = simular_eco_lunar(
            duracion_s=1.0, fs_hz=2048.0, retardo_s=10.0
        )
        result = analizar_fft_moonbounce(total, fs_hz=2048.0)
        assert 0.0 < result['psi_proxy'] <= 1.0 + 1e-12

    def test_delta_f_formula(self):
        """delta_f_hz must equal f_pico_hz − F0_EXACT_HZ."""
        tiempos, total, _, _ = simular_eco_lunar(
            duracion_s=1.0, fs_hz=2048.0, retardo_s=10.0
        )
        result = analizar_fft_moonbounce(total, fs_hz=2048.0)
        assert result['delta_f_hz'] == pytest.approx(
            result['f_pico_hz'] - F0_EXACT_HZ, abs=1e-10
        )

    def test_empty_signal_raises(self):
        """Empty signal must raise ValueError."""
        with pytest.raises(ValueError):
            analizar_fft_moonbounce([])

    def test_peak_near_f0_with_high_resolution_signal(self):
        """With a long high-res signal at f₀, the FFT peak must be within 2 Hz of f₀."""
        tiempos, total, _, _ = simular_eco_lunar(
            f_emitida=F0_FLOAT,
            duracion_s=5.0,
            fs_hz=2048.0,
            retardo_s=100.0,  # no echo within signal
        )
        result = analizar_fft_moonbounce(total, fs_hz=2048.0)
        assert abs(result['f_pico_hz'] - F0_FLOAT) < 2.0
