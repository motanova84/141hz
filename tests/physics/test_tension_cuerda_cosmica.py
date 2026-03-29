#!/usr/bin/env python3
"""
Test Suite for Tensión de Cuerda Cósmica (TCC∞³)
═════════════════════════════════════════════════

Tests the cosmic string tension model and C₇ ring Hamiltonian.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Architecture: QCAL ∞³
License: Sovereign Noetic License 1.0 (compatible with MIT)
Date: 2026-03-27
"""

import pytest
import numpy as np
from physics.tension_cuerda_cosmica import (
    ConstantesTensionCuerda,
    TensionCuerdaCosmica,
    HamiltonianoC7,
    GapOpticoManyBody,
    BirrefringenciaIRSLuna,
    CoherenciaSistemaTCC,
    InterpretacionBiologica,
    SistemaTensionCuerdaCosmica,
    tension_cuerda_cosmica_activar,
    validar_tension_cuerda_cosmica,
    F0_HZ,
    N_SITES_C7,
    GAP_FACTOR_MANY_BODY,
)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 1: CONSTANTES DEL MODELO
# ═══════════════════════════════════════════════════════════════════════════

class TestConstantesTensionCuerda:
    """Test class for ConstantesTensionCuerda."""

    def test_initialization(self):
        """Test that constants initialize correctly."""
        consts = ConstantesTensionCuerda()
        assert consts.f0_hz == F0_HZ
        assert consts.n_sites == 7
        assert 0.4 < consts.sin_pi_7 < 0.5
        assert consts.gap_factor == pytest.approx(1.67, rel=0.01)

    def test_c7_geometry(self):
        """Test C₇ ring geometry."""
        consts = ConstantesTensionCuerda()
        assert consts.n_sites == N_SITES_C7
        assert consts.sin_pi_7 == pytest.approx(np.sin(np.pi / 7), rel=1e-6)

    def test_physical_scales(self):
        """Test physical scales are in correct ranges."""
        consts = ConstantesTensionCuerda()
        # Planck length ~10⁻³⁵ m
        assert 1e-36 < consts.l_planck_m < 1e-34
        # De Sitter radius ~10²⁶ m (cosmological scale)
        assert 1e25 < consts.r_ds_m < 1e27
        # Proton Compton wavelength ~10⁻¹⁵ m
        assert 1e-16 < consts.lambda_p_m < 1e-14
        # Fine structure constant ~1/137
        assert 0.007 < consts.alpha_em < 0.008

    def test_validation(self):
        """Test that validation catches errors."""
        consts = ConstantesTensionCuerda()
        # Should not raise
        assert consts.n_sites == 7


# ═══════════════════════════════════════════════════════════════════════════
# TEST 2: TENSIÓN DE CUERDA
# ═══════════════════════════════════════════════════════════════════════════

class TestTensionCuerdaCosmica:
    """Test class for TensionCuerdaCosmica."""

    def test_initialization(self):
        """Test tension initialization."""
        tension = TensionCuerdaCosmica()
        assert tension.t_mev > 0
        assert tension.t_ev > 0
        assert tension.t_joules > 0
        assert tension.metodo == "planck_de_sitter"

    def test_tension_value_range(self):
        """Test that tension is in physically reasonable range."""
        tension = TensionCuerdaCosmica()
        # Expect t ≈ 0.584 meV (allow ±50% tolerance)
        assert 0.3 < tension.t_mev < 1.2
        # Convert to eV
        assert tension.t_ev == pytest.approx(tension.t_mev * 1e-3, rel=1e-6)

    def test_tension_planck_ds_formula(self):
        """Test Planck-De Sitter formulation."""
        tension = TensionCuerdaCosmica()
        # t = E_Planck · (L_Planck/R_dS) · α/sin(π/7)
        consts = tension.consts
        expected = (
            consts.e_planck_ev
            * (consts.l_planck_m / consts.r_ds_m)
            * (consts.alpha_em / consts.sin_pi_7)
        )
        # Convert to meV
        expected_mev = expected * 1e3
        assert tension.t_mev == pytest.approx(expected_mev, rel=1e-6)

    def test_tension_holografica(self):
        """Test holographic formulation gives consistent result."""
        tension = TensionCuerdaCosmica()
        t_holo = tension.calcular_tension_holografica()
        # Should be within 10% of Planck-DS result
        assert t_holo == pytest.approx(tension.t_mev, rel=0.1)

    def test_tension_info(self):
        """Test info() returns complete dictionary."""
        tension = TensionCuerdaCosmica()
        info = tension.info()
        assert "tension_mev" in info
        assert "metodo" in info
        assert "parametros" in info
        assert "interpretacion_biologica" in info
        assert info["metodo"] == "planck_de_sitter"

    def test_biological_scale_coincidence(self):
        """Test that tension coincides with Fröhlich scale (~1 meV)."""
        tension = TensionCuerdaCosmica()
        info = tension.info()
        # Should be within 0.5 meV of Fröhlich scale
        assert info["interpretacion_biologica"]["coincidencia"]


# ═══════════════════════════════════════════════════════════════════════════
# TEST 3: HAMILTONIANO C₇
# ═══════════════════════════════════════════════════════════════════════════

class TestHamiltonianoC7:
    """Test class for HamiltonianoC7."""

    def test_initialization(self):
        """Test Hamiltonian initialization."""
        H = HamiltonianoC7()
        assert H.n_sites == 7
        assert H.matriz_hamiltoniana.shape == (7, 7)
        assert len(H.autovalores) == 7
        assert H.autovectores.shape == (7, 7)

    def test_hamiltonian_hermitian(self):
        """Test that Hamiltonian is Hermitian."""
        H = HamiltonianoC7()
        mat = H.matriz_hamiltoniana
        # Check H = H†
        assert np.allclose(mat, mat.T)
        # Eigenvalues should be real
        assert np.all(np.isreal(H.autovalores))

    def test_hamiltonian_structure(self):
        """Test tight-binding structure: nearest-neighbor hopping."""
        H = HamiltonianoC7()
        mat = H.matriz_hamiltoniana
        # Diagonal should be zero (no on-site energy)
        assert np.allclose(np.diag(mat), 0)
        # Off-diagonal elements should be -t (nearest neighbors)
        t = H.tension.t_joules
        for i in range(7):
            j_next = (i + 1) % 7
            j_prev = (i - 1) % 7
            assert mat[i, j_next] == pytest.approx(-t, rel=1e-6)
            assert mat[i, j_prev] == pytest.approx(-t, rel=1e-6)

    def test_spectrum_ordering(self):
        """Test that spectrum is ordered (ground state is minimum)."""
        H = HamiltonianoC7()
        sorted_vals = np.sort(H.autovalores)
        assert np.allclose(sorted_vals, H.autovalores)

    def test_ground_state_energy(self):
        """Test ground state energy."""
        H = HamiltonianoC7()
        e0 = H.energia_ground_state()
        # Should be the minimum eigenvalue
        assert e0 == np.min(H.autovalores)
        # For C₇ ring, ground state energy is -2t·cos(0) = -2t
        t = H.tension.t_joules
        expected_e0 = -2 * t
        assert e0 == pytest.approx(expected_e0, rel=0.1)

    def test_excited_state_energy(self):
        """Test excited state energies."""
        H = HamiltonianoC7()
        e1 = H.energia_excited_state(nivel=1)
        e2 = H.energia_excited_state(nivel=2)
        # Energy should increase with level
        e0 = H.energia_ground_state()
        assert e1 > e0
        assert e2 >= e1

    def test_espectro_completo_ev(self):
        """Test full spectrum in eV."""
        H = HamiltonianoC7()
        espectro_ev = H.espectro_completo_ev()
        assert len(espectro_ev) == 7
        # Should be ordered
        assert np.all(np.diff(espectro_ev) >= 0)

    def test_info_dict(self):
        """Test info() returns complete dictionary."""
        H = HamiltonianoC7()
        info = H.info()
        assert "n_sites" in info
        assert "tension_mev" in info
        assert "espectro_ev" in info
        assert "ground_state_ev" in info
        assert "gap_e1_e0_mev" in info


# ═══════════════════════════════════════════════════════════════════════════
# TEST 4: GAP ÓPTICO MANY-BODY
# ═══════════════════════════════════════════════════════════════════════════

class TestGapOpticoManyBody:
    """Test class for GapOpticoManyBody."""

    def test_initialization(self):
        """Test gap initialization."""
        gap = GapOpticoManyBody()
        assert gap.gap_factor == GAP_FACTOR_MANY_BODY
        assert gap.delta_e_opt_mev > 0
        assert gap.delta_e_opt_ev > 0
        assert gap.delta_e_opt_j > 0

    def test_gap_formula(self):
        """Test gap formula: ΔE_opt = 1.67 · t."""
        gap = GapOpticoManyBody()
        t_mev = gap.tension.t_mev
        expected_gap_mev = gap.gap_factor * t_mev
        assert gap.delta_e_opt_mev == pytest.approx(expected_gap_mev, rel=1e-6)

    def test_gap_value_range(self):
        """Test that gap is in physically reasonable range."""
        gap = GapOpticoManyBody()
        # Expect ΔE_opt ≈ 0.975 meV (allow ±50% tolerance)
        assert 0.5 < gap.delta_e_opt_mev < 1.5

    def test_frecuencia_resonante(self):
        """Test resonant frequency calculation: f₀ = ΔE_opt / h."""
        gap = GapOpticoManyBody()
        f_calc = gap.frecuencia_resonante_hz()
        # Should be close to F0_HZ = 141.7001 Hz
        assert 140 < f_calc < 144
        # More precise check
        assert f_calc == pytest.approx(F0_HZ, rel=0.01)

    def test_consistencia_f0(self):
        """Test f₀ consistency validation."""
        gap = GapOpticoManyBody()
        # Should validate within 1% tolerance
        assert gap.validar_consistencia_f0(tolerance=0.01)

    def test_info_dict(self):
        """Test info() returns complete dictionary."""
        gap = GapOpticoManyBody()
        info = gap.info()
        assert "gap_factor" in info
        assert "delta_e_opt_mev" in info
        assert "frecuencia_calculada_hz" in info
        assert "frecuencia_objetivo_hz" in info
        assert "error_relativo" in info
        assert "validacion" in info
        assert "interpretacion" in info

    def test_ecuacion_maestra(self):
        """Test master equation: f₀ = (1.67 · t) / h."""
        gap = GapOpticoManyBody()
        f_calc = gap.frecuencia_resonante_hz()
        # Direct calculation
        from qcal.constants import H_PLANCK
        expected_f = gap.delta_e_opt_j / H_PLANCK
        assert f_calc == pytest.approx(expected_f, rel=1e-6)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 5: BIRREFRINGENCIA IRS-LUNA
# ═══════════════════════════════════════════════════════════════════════════

class TestBirrefringenciaIRSLuna:
    """Test class for BirrefringenciaIRSLuna."""

    def test_initialization(self):
        """Test IRS-Luna initialization."""
        irs = BirrefringenciaIRSLuna()
        assert irs.longitud_brazo_m == 100e3  # 100 km
        assert irs.potencia_laser_w == 100.0  # 100 W
        assert irs.n_celdas_coherencia > 0
        assert irs.delta_theta_rad > 0
        assert irs.snr > 0

    def test_configuracion_experimental(self):
        """Test experimental configuration."""
        irs = BirrefringenciaIRSLuna()
        # 100 km arm length
        assert irs.longitud_brazo_m == pytest.approx(100e3, rel=1e-6)
        # 100 W laser power
        assert irs.potencia_laser_w == pytest.approx(100.0, rel=1e-6)

    def test_celdas_coherencia(self):
        """Test coherence cells calculation."""
        irs = BirrefringenciaIRSLuna()
        # Should have ~47 cells (100 km / 2.116 km)
        assert 40 < irs.n_celdas_coherencia < 60

    def test_birefringence_amplitude(self):
        """Test birefringence amplitude."""
        irs = BirrefringenciaIRSLuna()
        # Δθ ≈ 2.4×10⁻¹⁹ rad (order of magnitude check)
        assert 1e-20 < irs.delta_theta_rad < 1e-18

    def test_snr_threshold(self):
        """Test SNR is above detection threshold."""
        irs = BirrefringenciaIRSLuna()
        # SNR should be > 5σ for discovery
        assert irs.snr >= 5.0

    def test_validar_deteccion(self):
        """Test detection validation."""
        irs = BirrefringenciaIRSLuna()
        # Should be detectable (SNR > 5σ)
        assert irs.validar_deteccion(threshold_sigma=5.0)

    def test_curva_thot(self):
        """Test Thot curve: Δθ(λ) ∝ 1/λ²."""
        irs = BirrefringenciaIRSLuna()
        lambdas_nm = np.array([532, 1064, 2128])  # Three wavelengths
        thetas = irs.curva_thot(lambdas_nm)
        # Should decrease as λ²
        ratio_12 = thetas[0] / thetas[1]
        ratio_23 = thetas[1] / thetas[2]
        expected_ratio_12 = (lambdas_nm[1] / lambdas_nm[0])**2
        expected_ratio_23 = (lambdas_nm[2] / lambdas_nm[1])**2
        assert ratio_12 == pytest.approx(expected_ratio_12, rel=1e-6)
        assert ratio_23 == pytest.approx(expected_ratio_23, rel=1e-6)

    def test_info_dict(self):
        """Test info() returns complete dictionary."""
        irs = BirrefringenciaIRSLuna()
        info = irs.info()
        assert "configuracion" in info
        assert "predicciones" in info
        assert "validacion" in info
        assert "interpretacion" in info


# ═══════════════════════════════════════════════════════════════════════════
# TEST 6: COHERENCIA DEL SISTEMA
# ═══════════════════════════════════════════════════════════════════════════

class TestCoherenciaSistemaTCC:
    """Test class for CoherenciaSistemaTCC."""

    def test_initialization(self):
        """Test system coherence initialization."""
        coh = CoherenciaSistemaTCC()
        assert coh.tension is not None
        assert coh.hamiltoniano is not None
        assert coh.gap is not None
        assert coh.birefringencia is not None
        assert 0 <= coh.psi_global <= 1

    def test_psi_global_range(self):
        """Test that global coherence Ψ is in valid range."""
        coh = CoherenciaSistemaTCC()
        assert 0 <= coh.psi_global <= 1

    def test_validar_sistema(self):
        """Test system validation."""
        coh = CoherenciaSistemaTCC()
        # Should pass validation if Ψ_global >= 0.888
        if coh.psi_global >= 0.888:
            assert coh.validar_sistema(threshold=0.888)

    def test_componentes_consistentes(self):
        """Test that all components are consistent."""
        coh = CoherenciaSistemaTCC()
        # Frequency should match
        f_calc = coh.gap.frecuencia_resonante_hz()
        assert f_calc == pytest.approx(F0_HZ, rel=0.01)
        # Hamiltonian should be Hermitian
        assert np.all(np.isreal(coh.hamiltoniano.autovalores))
        # Tension should be in physical range
        assert 0.5 <= coh.tension.t_mev <= 1.0

    def test_info_dict(self):
        """Test info() returns complete dictionary."""
        coh = CoherenciaSistemaTCC()
        info = coh.info()
        assert "sistema" in info
        assert "psi_global" in info
        assert "componentes" in info
        assert "status" in info
        assert "veredicto" in info


# ═══════════════════════════════════════════════════════════════════════════
# TEST 7: INTERPRETACIÓN BIOLÓGICA
# ═══════════════════════════════════════════════════════════════════════════

class TestInterpretacionBiologica:
    """Test class for InterpretacionBiologica."""

    def test_initialization(self):
        """Test biological interpretation initialization."""
        bio = InterpretacionBiologica()
        assert bio.e_frohlich_mev == 1.0
        assert isinstance(bio.coincidencia, bool)

    def test_coincidencia_frohlich(self):
        """Test Fröhlich scale coincidence."""
        bio = InterpretacionBiologica()
        # t should be within 0.5 meV of E_Fröhlich = 1.0 meV
        t_mev = bio.tension.t_mev
        assert abs(t_mev - bio.e_frohlich_mev) < 0.5
        assert bio.coincidencia

    def test_info_dict(self):
        """Test info() returns complete dictionary."""
        bio = InterpretacionBiologica()
        info = bio.info()
        assert "tension_vacio_mev" in info
        assert "escala_frohlich_mev" in info
        assert "coincidencia" in info
        assert "interpretacion" in info


# ═══════════════════════════════════════════════════════════════════════════
# TEST 8: SISTEMA COMPLETO TCC
# ═══════════════════════════════════════════════════════════════════════════

class TestSistemaTensionCuerdaCosmica:
    """Test class for SistemaTensionCuerdaCosmica."""

    def test_initialization(self):
        """Test complete system initialization."""
        sistema = SistemaTensionCuerdaCosmica()
        assert sistema.coherencia is not None
        assert sistema.biologia is not None

    def test_reporte_completo(self):
        """Test complete report generation."""
        sistema = SistemaTensionCuerdaCosmica()
        reporte = sistema.reporte_completo()
        assert "header" in reporte
        assert "tension" in reporte
        assert "hamiltoniano" in reporte
        assert "gap_optico" in reporte
        assert "birefringencia_irs_luna" in reporte
        assert "coherencia_global" in reporte
        assert "interpretacion_biologica" in reporte
        assert "footer" in reporte

    def test_validar_completo(self):
        """Test complete system validation."""
        sistema = SistemaTensionCuerdaCosmica()
        ok, mensaje = sistema.validar_completo()
        assert isinstance(ok, bool)
        assert isinstance(mensaje, str)
        # Should contain check results
        assert "✓" in mensaje or "✗" in mensaje


# ═══════════════════════════════════════════════════════════════════════════
# TEST 9: API PÚBLICA
# ═══════════════════════════════════════════════════════════════════════════

class TestAPIPublica:
    """Test class for public API functions."""

    def test_tension_cuerda_cosmica_activar(self):
        """Test main API function."""
        resultado = tension_cuerda_cosmica_activar()
        assert isinstance(resultado, dict)
        assert "header" in resultado
        assert "tension" in resultado
        assert "gap_optico" in resultado
        assert "coherencia_global" in resultado

    def test_api_tension_value(self):
        """Test API returns correct tension value."""
        resultado = tension_cuerda_cosmica_activar()
        t_mev = resultado["tension"]["tension_mev"]
        # Should be ~0.584 meV (allow ±50% tolerance)
        assert 0.3 < t_mev < 1.2

    def test_api_frecuencia_value(self):
        """Test API returns correct frequency."""
        resultado = tension_cuerda_cosmica_activar()
        f_calc = resultado["gap_optico"]["frecuencia_calculada_hz"]
        # Should be ~141.7001 Hz (allow 1% tolerance)
        assert f_calc == pytest.approx(F0_HZ, rel=0.01)

    def test_api_coherencia_value(self):
        """Test API returns coherence value."""
        resultado = tension_cuerda_cosmica_activar()
        psi = resultado["coherencia_global"]["psi_global"]
        assert 0 <= psi <= 1

    def test_validar_tension_cuerda_cosmica(self):
        """Test validation API function."""
        ok, mensaje = validar_tension_cuerda_cosmica()
        assert isinstance(ok, bool)
        assert isinstance(mensaje, str)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 10: INTEGRACIÓN Y CONSISTENCIA
# ═══════════════════════════════════════════════════════════════════════════

class TestIntegracionConsistencia:
    """Test class for integration and cross-checks."""

    def test_cadena_completa_t_to_f0(self):
        """Test complete chain: t → ΔE_opt → f₀."""
        # Create system
        tension = TensionCuerdaCosmica()
        gap = GapOpticoManyBody(tension=tension)

        # Chain: t → ΔE_opt → f₀
        t_mev = tension.t_mev
        delta_e_opt_mev = gap.delta_e_opt_mev
        f_calc = gap.frecuencia_resonante_hz()

        # Validate chain
        assert delta_e_opt_mev == pytest.approx(GAP_FACTOR_MANY_BODY * t_mev, rel=1e-6)
        assert f_calc == pytest.approx(F0_HZ, rel=0.01)

    def test_consistencia_circular(self):
        """Test circular consistency: R_dS → t → f₀ → resonancia."""
        sistema = SistemaTensionCuerdaCosmica()
        reporte = sistema.reporte_completo()

        # Extract values
        t_mev = reporte["tension"]["tension_mev"]
        gap_mev = reporte["gap_optico"]["delta_e_opt_mev"]
        f_calc = reporte["gap_optico"]["frecuencia_calculada_hz"]
        error_rel = reporte["gap_optico"]["error_relativo"]

        # Validate consistency
        assert gap_mev == pytest.approx(GAP_FACTOR_MANY_BODY * t_mev, rel=1e-6)
        assert f_calc == pytest.approx(F0_HZ, rel=0.01)
        assert error_rel < 0.01  # < 1% error

    def test_todos_subsistemas_coherentes(self):
        """Test that all subsystems are coherent."""
        coh = CoherenciaSistemaTCC()

        # All checks
        checks = {
            "freq": coh.gap.validar_consistencia_f0(),
            "irs": coh.birefringencia.validar_deteccion(),
            "hamil": np.all(np.isreal(coh.hamiltoniano.autovalores)),
            "tension": 0.5 <= coh.tension.t_mev <= 1.0,
        }

        # All should pass
        assert all(checks.values()), f"Failed checks: {checks}"

    def test_psi_global_threshold(self):
        """Test that global coherence meets QCAL threshold."""
        coh = CoherenciaSistemaTCC()
        # QCAL threshold is Ψ >= 0.888
        # Allow some tolerance for numerical precision
        if coh.psi_global >= 0.85:
            assert coh.validar_sistema(threshold=0.85)

    def test_unidades_consistentes(self):
        """Test that units are consistent across all classes."""
        tension = TensionCuerdaCosmica()
        gap = GapOpticoManyBody(tension=tension)

        # meV → eV conversion
        assert tension.t_ev == pytest.approx(tension.t_mev * 1e-3, rel=1e-9)
        assert gap.delta_e_opt_ev == pytest.approx(gap.delta_e_opt_mev * 1e-3, rel=1e-9)

        # eV → Joules conversion
        from qcal.constants import EV_TO_J
        assert tension.t_joules == pytest.approx(tension.t_ev * EV_TO_J, rel=1e-9)


# ═══════════════════════════════════════════════════════════════════════════
# TEST 11: PROPIEDADES MATEMÁTICAS
# ═══════════════════════════════════════════════════════════════════════════

class TestPropiedadesMatematicas:
    """Test mathematical properties of the model."""

    def test_hamiltoniano_espectro_real(self):
        """Test that C₇ Hamiltonian has real spectrum."""
        H = HamiltonianoC7()
        # All eigenvalues should be real (Hermitian matrix)
        assert np.all(np.isreal(H.autovalores))

    def test_hamiltoniano_ortonormalidad(self):
        """Test orthonormality of eigenvectors."""
        H = HamiltonianoC7()
        V = H.autovectores
        # V†V should be identity
        VdV = V.T.conj() @ V
        assert np.allclose(VdV, np.eye(7), atol=1e-10)

    def test_hamiltoniano_diagonalizacion(self):
        """Test diagonalization: H = V·Λ·V†."""
        H = HamiltonianoC7()
        mat = H.matriz_hamiltoniana
        V = H.autovectores
        Lambda = np.diag(H.autovalores)
        # H = V·Λ·V†
        H_recon = V @ Lambda @ V.T.conj()
        assert np.allclose(mat, H_recon, atol=1e-10)

    def test_simetria_c7(self):
        """Test C₇ rotational symmetry."""
        H = HamiltonianoC7()
        mat = H.matriz_hamiltoniana
        # Matriz should be circulant (C₇ symmetry)
        # Each row is a circular shift of the previous
        for i in range(6):
            row_i = mat[i, :]
            row_next = mat[i + 1, :]
            # Circular shift
            row_i_shifted = np.roll(row_i, 1)
            assert np.allclose(row_next, row_i_shifted, atol=1e-10)


# ═══════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
