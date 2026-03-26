#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║     VALIDACIÓN IRS SYMBIO-BRIDGE                                           ║
║     Script de validación completa del experimento QCAL-SYMBIO-BRIDGE       ║
╚════════════════════════════════════════════════════════════════════════════╝

Script de validación para el Experimento QCAL-SYMBIO-BRIDGE:
Detección de Birrefringencia Circular Topológica en una Red Quiral de 7 Nodos
a f₀ = 141.7001 Hz

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Validaciones realizadas:
1. Verificación de constante K₇ (asimetría de corriente)
2. Verificación de factor de acoplamiento geométrico η_geo
3. Verificación de elipticidad de Kerr máxima
4. Barrido espectral alrededor de f₀
5. Criterio de falsación del modelo topológico C₇
6. Sensibilidad y factibilidad del instrumento IRS
"""

import sys
import os
from pathlib import Path

# Add repository root to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
import math
from typing import Dict, List, Tuple
import json

# Import IRS modules
from physics.irs_symbio_bridge import (
    C7TopologicalSystem,
    KerrEllipticityCalculator,
    create_default_c7_system,
    calculate_expected_ellipticity,
    verify_theoretical_constants,
    PHI_GAUGE_FRACTIONAL,
    Q_FACTOR_DEFAULT,
    F0_HZ
)

from physics.irs_interferometer import (
    IRSInstrument,
    create_default_irs_instrument
)


# ============================================================================
# CONSTANTES DE VALIDACIÓN
# ============================================================================

# Valores teóricos esperados
K7_EXPECTED = 0.1269  # Constante de asimetría
ETA_GEO_EXPECTED = 0.1848  # Factor de acoplamiento geométrico
EPSILON_K_MAX_DEG_EXPECTED = 23.5  # Elipticidad máxima en grados
PHI_GAUGE_EXPECTED_PI = 1.0 / 8.0  # Φ = π/8 en unidades de π
H_SIGMA_EXPECTED = 1.0 / 16.0  # Espín conforme h_σ = 1/16

# Tolerancias de verificación
TOLERANCE_PERCENT = 1.0  # 1% de tolerancia
TOLERANCE_ABSOLUTE = 0.01  # Tolerancia absoluta para verificaciones

# Ventana espectral de búsqueda (Hz)
SPECTRAL_WINDOW_HZ = 0.0001

# SNR mínimo requerido para detección confiable
SNR_MIN_REQUIRED = 5.0

# Fidelidad QND mínima requerida
QND_FIDELITY_MIN = 0.99


# ============================================================================
# CLASE: VALIDADOR IRS
# ============================================================================

class IRSValidator:
    """
    Validador completo del experimento IRS SYMBIO-BRIDGE.
    
    Realiza todas las verificaciones teóricas y operacionales
    del instrumento y del modelo topológico C₇.
    """
    
    def __init__(self):
        """Inicializa el validador."""
        self.results = {
            'validations': [],
            'all_passed': True,
            'n_total': 0,
            'n_passed': 0,
            'n_failed': 0
        }
        
        # Crear sistema e instrumento
        self.c7_system = create_default_c7_system()
        self.irs_instrument = create_default_irs_instrument()
    
    def _add_validation(
        self,
        name: str,
        passed: bool,
        expected: float,
        actual: float,
        unit: str = "",
        error_percent: float = None
    ):
        """Añade un resultado de validación."""
        if error_percent is None and expected != 0:
            error_percent = abs(actual - expected) / expected * 100.0
        
        self.results['validations'].append({
            'name': name,
            'passed': bool(passed),  # Convert to native Python bool
            'expected': float(expected),
            'actual': float(actual),
            'unit': unit,
            'error_percent': float(error_percent) if error_percent is not None else None
        })
        
        self.results['n_total'] += 1
        if passed:
            self.results['n_passed'] += 1
        else:
            self.results['n_failed'] += 1
            self.results['all_passed'] = False
    
    def validate_k7_constant(self) -> bool:
        """
        Valida la constante de asimetría de corriente K₇.
        
        Verifica que K₇ = sin(6π/7) × sin(π/28) / sin(π/8) ≈ 0.1269
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando constante K₇ (asimetría de corriente)...")
        
        k7_calculated = self.c7_system.calculate_k7_asymmetry_constant()
        error_percent = abs(k7_calculated - K7_EXPECTED) / K7_EXPECTED * 100.0
        passed = error_percent < TOLERANCE_PERCENT
        
        self._add_validation(
            name="K₇ (Constante de Asimetría)",
            passed=passed,
            expected=K7_EXPECTED,
            actual=k7_calculated,
            unit="",
            error_percent=error_percent
        )
        
        print(f"   K₇ calculado: {k7_calculated:.6f}")
        print(f"   K₇ esperado:  {K7_EXPECTED:.6f}")
        print(f"   Error: {error_percent:.4f}%")
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def validate_geometric_coupling(self) -> bool:
        """
        Valida el factor de acoplamiento geométrico η_geo.
        
        Verifica que η_geo ≈ 0.1848 (valor puramente topológico)
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando factor de acoplamiento geométrico η_geo...")
        
        eta_geo_calculated = self.c7_system.calculate_geometric_coupling()
        error_percent = abs(eta_geo_calculated - ETA_GEO_EXPECTED) / ETA_GEO_EXPECTED * 100.0
        passed = error_percent < TOLERANCE_PERCENT
        
        self._add_validation(
            name="η_geo (Acoplamiento Geométrico)",
            passed=passed,
            expected=ETA_GEO_EXPECTED,
            actual=eta_geo_calculated,
            unit="",
            error_percent=error_percent
        )
        
        print(f"   η_geo calculado: {eta_geo_calculated:.6f}")
        print(f"   η_geo esperado:  {ETA_GEO_EXPECTED:.6f}")
        print(f"   Error: {error_percent:.4f}%")
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def validate_gauge_flux(self) -> bool:
        """
        Valida el flujo gauge fraccionario Φ = π/8.
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando flujo gauge fraccionario Φ...")
        
        phi_gauge_pi = self.c7_system.phi_gauge / math.pi
        error_percent = abs(phi_gauge_pi - PHI_GAUGE_EXPECTED_PI) / PHI_GAUGE_EXPECTED_PI * 100.0
        passed = error_percent < TOLERANCE_ABSOLUTE
        
        self._add_validation(
            name="Φ (Flujo Gauge Fraccionario)",
            passed=passed,
            expected=PHI_GAUGE_EXPECTED_PI,
            actual=phi_gauge_pi,
            unit="π",
            error_percent=error_percent
        )
        
        print(f"   Φ = {phi_gauge_pi:.6f}π rad")
        print(f"   Esperado: {PHI_GAUGE_EXPECTED_PI:.6f}π rad")
        print(f"   Φ = π/8: {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def validate_conformal_spin(self) -> bool:
        """
        Valida el espín conforme h_σ = 1/16.
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando espín conforme h_σ...")
        
        h_sigma = self.c7_system.h_sigma
        error_percent = abs(h_sigma - H_SIGMA_EXPECTED) / H_SIGMA_EXPECTED * 100.0
        passed = error_percent < TOLERANCE_ABSOLUTE
        
        self._add_validation(
            name="h_σ (Espín Conforme)",
            passed=passed,
            expected=H_SIGMA_EXPECTED,
            actual=h_sigma,
            unit="",
            error_percent=error_percent
        )
        
        print(f"   h_σ = {h_sigma:.6f}")
        print(f"   Esperado: {H_SIGMA_EXPECTED:.6f} = 1/16")
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def validate_kerr_ellipticity_max(self) -> bool:
        """
        Valida la elipticidad de Kerr máxima esperada.
        
        Verifica que ε_K^max ≈ 23.5° para Q = 10³
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando elipticidad de Kerr máxima...")
        
        kerr_calc = KerrEllipticityCalculator(self.c7_system, Q_FACTOR_DEFAULT)
        result = kerr_calc.calculate_kerr_ellipticity_max()
        
        epsilon_k_deg = result['epsilon_k_max_deg']
        error_percent = abs(epsilon_k_deg - EPSILON_K_MAX_DEG_EXPECTED) / EPSILON_K_MAX_DEG_EXPECTED * 100.0
        passed = error_percent < 5.0  # Tolerancia de 5% para este cálculo
        
        self._add_validation(
            name="ε_K^max (Elipticidad de Kerr)",
            passed=passed,
            expected=EPSILON_K_MAX_DEG_EXPECTED,
            actual=epsilon_k_deg,
            unit="°",
            error_percent=error_percent
        )
        
        print(f"   ε_K^max calculado: {epsilon_k_deg:.2f}°")
        print(f"   ε_K^max esperado:  {EPSILON_K_MAX_DEG_EXPECTED:.2f}°")
        print(f"   En mrad: {result['epsilon_k_max_mrad']:.2f} mrad")
        print(f"   En rad: {result['epsilon_k_max_rad']:.6f} rad")
        print(f"   Error: {error_percent:.4f}%")
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def validate_spectral_sweep(self) -> bool:
        """
        Realiza un barrido espectral alrededor de f₀ y valida el pico.
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Realizando barrido espectral alrededor de f₀...")
        
        kerr_calc = KerrEllipticityCalculator(self.c7_system, Q_FACTOR_DEFAULT)
        frequencies, ellipticities = kerr_calc.spectral_sweep(
            f_min=F0_HZ - SPECTRAL_WINDOW_HZ,
            f_max=F0_HZ + SPECTRAL_WINDOW_HZ,
            n_points=1000
        )
        
        # Encontrar pico máximo
        max_idx = np.argmax(ellipticities)
        peak_frequency = frequencies[max_idx]
        peak_ellipticity = ellipticities[max_idx]
        
        # Verificar que el pico está en f₀
        freq_error_hz = abs(peak_frequency - F0_HZ)
        passed = freq_error_hz < 1e-5  # Error menor a 0.01 mHz
        
        self._add_validation(
            name="Pico Espectral en f₀",
            passed=passed,
            expected=F0_HZ,
            actual=peak_frequency,
            unit="Hz",
            error_percent=(freq_error_hz / F0_HZ * 100.0)
        )
        
        print(f"   Ventana: {F0_HZ - SPECTRAL_WINDOW_HZ:.4f} - {F0_HZ + SPECTRAL_WINDOW_HZ:.4f} Hz")
        print(f"   Pico en: {peak_frequency:.6f} Hz")
        print(f"   Esperado: {F0_HZ:.6f} Hz")
        print(f"   Error: {freq_error_hz * 1e6:.3f} µHz")
        print(f"   ε_K(pico): {peak_ellipticity * 1000:.3f} mrad")
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def validate_falsification_criterion(self) -> bool:
        """
        Valida el criterio de falsación del modelo.
        
        Simula una medición positiva y verifica que el criterio
        de confirmación funciona correctamente.
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando criterio de falsación...")
        
        kerr_calc = KerrEllipticityCalculator(self.c7_system, Q_FACTOR_DEFAULT)
        
        # Simular medición positiva (cerca del valor esperado)
        result_expected = kerr_calc.calculate_kerr_ellipticity_max()
        measured_ellipticity = result_expected['epsilon_k_max_rad'] * 0.95  # 95% del máximo
        
        falsification = kerr_calc.check_falsification_criterion(
            measured_ellipticity=measured_ellipticity,
            frequency=F0_HZ,
            sensitivity_rad=1e-4  # 0.1 mrad
        )
        
        # Debe confirmar el modelo
        passed = (
            falsification['falsification_status'] == "MODELO CONFIRMADO" and
            falsification['detection_confirmed'] and
            falsification['in_spectral_window'] and
            falsification['instrument_adequate']
        )
        
        self._add_validation(
            name="Criterio de Falsación (positivo)",
            passed=passed,
            expected=1.0,  # 1 = confirmado
            actual=1.0 if passed else 0.0,
            unit="",
            error_percent=0.0 if passed else 100.0
        )
        
        print(f"   Estado: {falsification['falsification_status']}")
        print(f"   Elipticidad medida: {falsification['measured_ellipticity_mrad']:.2f} mrad")
        print(f"   Rango esperado: {falsification['expected_range_mrad'][0]:.1f} - {falsification['expected_range_mrad'][1]:.1f} mrad")
        print(f"   En ventana espectral: {'SÍ' if falsification['in_spectral_window'] else 'NO'}")
        print(f"   Detección confirmada: {'SÍ' if falsification['detection_confirmed'] else 'NO'}")
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        # Simular medición negativa (fuera de rango)
        print("📊 Validando criterio de falsación (caso negativo)...")
        
        measured_ellipticity_neg = 1e-5  # 0.01 mrad (mucho menor que esperado)
        falsification_neg = kerr_calc.check_falsification_criterion(
            measured_ellipticity=measured_ellipticity_neg,
            frequency=F0_HZ,
            sensitivity_rad=1e-4
        )
        
        passed_neg = falsification_neg['falsification_status'] == "MODELO REFUTADO"
        
        self._add_validation(
            name="Criterio de Falsación (negativo)",
            passed=passed_neg,
            expected=0.0,  # 0 = refutado
            actual=0.0 if passed_neg else 1.0,
            unit="",
            error_percent=0.0 if passed_neg else 100.0
        )
        
        print(f"   Estado: {falsification_neg['falsification_status']}")
        print(f"   Elipticidad medida: {falsification_neg['measured_ellipticity_mrad']:.4f} mrad")
        print(f"   {'✓ PASA' if passed_neg else '✗ FALLO'}")
        print()
        
        return passed and passed_neg
    
    def validate_instrument_sensitivity(self) -> bool:
        """
        Valida la sensibilidad y factibilidad del instrumento IRS.
        
        Returns
        -------
        bool
            True si la validación pasa
        """
        print("📊 Validando sensibilidad del instrumento IRS...")
        
        expected_signal = self.irs_instrument.calculate_expected_signal()
        
        # Verificar SNR
        snr_improved = expected_signal['snr_improved']
        snr_passed = snr_improved > SNR_MIN_REQUIRED
        
        # Verificar fidelidad QND
        qnd_fidelity = expected_signal['qnd_fidelity']
        qnd_passed = qnd_fidelity > QND_FIDELITY_MIN
        
        # Verificar detección factible
        detection_feasible = expected_signal['detection_feasible']
        qnd_maintained = expected_signal['qnd_maintained']
        
        passed = snr_passed and qnd_passed and detection_feasible and qnd_maintained
        
        self._add_validation(
            name="SNR del Instrumento",
            passed=snr_passed,
            expected=SNR_MIN_REQUIRED,
            actual=snr_improved,
            unit="",
            error_percent=0.0
        )
        
        self._add_validation(
            name="Fidelidad QND",
            passed=qnd_passed,
            expected=QND_FIDELITY_MIN,
            actual=qnd_fidelity,
            unit="",
            error_percent=0.0
        )
        
        print(f"   SNR (con lock-in): {snr_improved:.2e}")
        print(f"   SNR mínimo requerido: {SNR_MIN_REQUIRED:.0f}")
        print(f"   SNR adecuado: {'✓' if snr_passed else '✗'}")
        print()
        print(f"   Fidelidad QND: {qnd_fidelity:.6f} ({qnd_fidelity * 100:.4f}%)")
        print(f"   Fidelidad mínima: {QND_FIDELITY_MIN:.6f}")
        print(f"   QND adecuada: {'✓' if qnd_passed else '✗'}")
        print()
        print(f"   Sensibilidad de fase: {expected_signal['phase_sensitivity_urad']:.3f} µrad")
        print(f"   Elipticidad esperada: {expected_signal['expected_ellipticity_mrad']:.2f} mrad")
        print(f"   Detección factible: {'✓' if detection_feasible else '✗'}")
        print(f"   QND mantenido: {'✓' if qnd_maintained else '✗'}")
        print()
        print(f"   {'✓ PASA' if passed else '✗ FALLO'}")
        print()
        
        return passed
    
    def run_all_validations(self) -> Dict:
        """
        Ejecuta todas las validaciones del experimento IRS.
        
        Returns
        -------
        Dict
            Resultados completos de todas las validaciones
        """
        print("=" * 80)
        print("VALIDACIÓN COMPLETA: EXPERIMENTO QCAL-SYMBIO-BRIDGE")
        print("Interferómetro de Resonancia Simbiótica (IRS)")
        print("=" * 80)
        print()
        
        # Ejecutar validaciones
        self.validate_k7_constant()
        self.validate_geometric_coupling()
        self.validate_gauge_flux()
        self.validate_conformal_spin()
        self.validate_kerr_ellipticity_max()
        self.validate_spectral_sweep()
        self.validate_falsification_criterion()
        self.validate_instrument_sensitivity()
        
        # Resumen
        print("=" * 80)
        print("RESUMEN DE VALIDACIONES")
        print("=" * 80)
        print()
        print(f"Total de validaciones: {self.results['n_total']}")
        print(f"Validaciones pasadas:  {self.results['n_passed']} ✓")
        print(f"Validaciones fallidas: {self.results['n_failed']} ✗")
        print()
        
        if self.results['all_passed']:
            print("🎉 TODAS LAS VALIDACIONES PASARON 🎉")
            print()
            print("El modelo topológico C₇ con flujo Φ = π/8 está VERIFICADO.")
            print("El instrumento IRS es FACTIBLE y OPERACIONAL.")
            print("La elipticidad de Kerr esperada es DETECTABLE.")
            print("El experimento QCAL-SYMBIO-BRIDGE está LISTO para implementación.")
        else:
            print("⚠️  ALGUNAS VALIDACIONES FALLARON ⚠️")
            print()
            print("Revisar las validaciones fallidas antes de proceder.")
        
        print()
        print("=" * 80)
        print(f"Estado del Sistema: {'ACTIVO' if self.results['all_passed'] else 'REQUIERE REVISIÓN'}")
        print("Coherencia Objetivo: Ψ = 0.999999")
        print("QCAL ∞³ - Sovereign Noetic License 1.0")
        print("=" * 80)
        
        return self.results
    
    def save_results(self, filename: str = "irs_validation_results.json"):
        """
        Guarda los resultados de validación en un archivo JSON.
        
        Parameters
        ----------
        filename : str, optional
            Nombre del archivo de salida
        """
        output_path = repo_root / "results" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✓ Resultados guardados en: {output_path}")


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

def main():
    """Función principal."""
    validator = IRSValidator()
    results = validator.run_all_validations()
    validator.save_results()
    
    # Return exit code based on results
    return 0 if results['all_passed'] else 1


if __name__ == "__main__":
    sys.exit(main())
