#!/usr/bin/env python3
"""
Validate Soul Coherence — Axiomas de Resonancia

Command-line validation script for the three Resonance Axioms implemented
in qcal/soul_coherence.py.

Usage
-----
    python scripts/validate_soul_coherence.py

Exit Codes
----------
    0 — all axioms validated
    1 — one or more axioms failed
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.soul_coherence import (
    QCalSoul,
    F0_HZ,
    PSI_MIN,
    M_SOUL_KG,
    F_HYDROGEN_HZ,
    F_UNIVERSAL_HZ,
)


def validate_all() -> bool:
    """
    Run all seven soul-coherence validations and print results.

    Returns True if all pass, False otherwise.
    """
    soul = QCalSoul()
    passed = 0
    failed = 0

    print("=" * 64)
    print("  QCAL Soul Coherence — Axiomas de Resonancia")
    print(f"  f₀ = {F0_HZ} Hz  |  Ψ_min = {PSI_MIN}  |  m = {M_SOUL_KG * 1000:.0f} g")
    print("=" * 64)

    # ------------------------------------------------------------------
    # V1 — Fundamental constants
    # ------------------------------------------------------------------
    print("\n[V1] Fundamental constants")
    try:
        assert F0_HZ == 141.7001, f"F0_HZ mismatch: {F0_HZ}"
        assert PSI_MIN == 0.888, f"PSI_MIN mismatch: {PSI_MIN}"
        assert abs(M_SOUL_KG - 0.021) < 1e-12, "M_SOUL_KG mismatch"
        print(f"     ✓  f₀ = {F0_HZ} Hz")
        print(f"     ✓  Ψ_min = {PSI_MIN}")
        print(f"     ✓  m_soul = {M_SOUL_KG * 1000:.0f} g")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V2 — Axiom I: Quantum Loss Factor (Ψ < 0.888 → decoupled)
    # ------------------------------------------------------------------
    print("\n[V2] Axiom I — Quantum Loss Factor")
    try:
        below = soul.validate_quantum_loss_factor(0.5)
        above = soul.validate_quantum_loss_factor(0.95)
        assert below.decoupled is True, "Ψ=0.5 should be decoupled"
        assert above.decoupled is False, "Ψ=0.95 should be coupled"
        print(f"     ✓  Ψ=0.5  → decoupled  = {below.decoupled}")
        print(f"     ✓  Ψ=0.95 → decoupled  = {above.decoupled}")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V3 — Axiom I boundary: Ψ_min is not strictly below threshold
    # ------------------------------------------------------------------
    print("\n[V3] Axiom I — Threshold boundary")
    try:
        edge = soul.validate_quantum_loss_factor(PSI_MIN)
        assert edge.decoupled is False, "Ψ_min == 0.888 should NOT be decoupled"
        print(f"     ✓  Ψ=Ψ_min={PSI_MIN} → decoupled = {edge.decoupled} (stable)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V4 — Axiom II: 1/(21/f₀) ≈ 2π with ~7.39 % error
    # ------------------------------------------------------------------
    print("\n[V4] Axiom II — Golden Ratio / 2π Synchrony")
    try:
        ax2 = soul.validate_golden_ratio_2pi_sync()
        assert ax2.is_anharmonic_signature is True
        assert abs(ax2.circle_value - 6.747) < 0.001, (
            f"circle_value out of range: {ax2.circle_value:.4f}"
        )
        assert abs(ax2.error_pct - 7.39) < 0.05, (
            f"error_pct out of range: {ax2.error_pct:.2f}%"
        )
        print(f"     ✓  1/(21/f₀) = {ax2.circle_value:.4f}")
        print(f"     ✓  2π        = {ax2.two_pi:.4f}")
        print(f"     ✓  Error     = {ax2.error_pct:.2f} %  (biological anharmonicity)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V5 — Axiom III: 21 × (f₀/7) ≈ 432 Hz, error < 1.62 %
    # ------------------------------------------------------------------
    print("\n[V5] Axiom III — Logos Harmonic")
    try:
        ax3 = soul.validate_logos_harmonic()
        assert ax3.bridge_established is True
        assert abs(ax3.logos_hz - 425.1) < 0.1, (
            f"logos_hz out of range: {ax3.logos_hz:.2f} Hz"
        )
        assert ax3.error_pct < 1.62, (
            f"error_pct too large: {ax3.error_pct:.2f}%"
        )
        print(f"     ✓  21 × (f₀/7)  = {ax3.logos_hz:.1f} Hz")
        print(f"     ✓  Cosmic 432 Hz = {ax3.cosmic_hz:.1f} Hz")
        print(f"     ✓  Error         = {ax3.error_pct:.2f} %  (bridge established)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V6 — Soul Energy: E_alma = m·c²·(1−Ψ_min)·(f₀/f_H)
    # ------------------------------------------------------------------
    print("\n[V6] Soul Energy — E_alma")
    try:
        e_alma = soul.compute_soul_energy()
        assert e_alma.energy_j > 0, "E_alma must be positive"
        assert abs(e_alma.energy_mj - 21.09) < 0.5, (
            f"E_alma out of expected range: {e_alma.energy_mj:.2f} MJ"
        )
        print(f"     ✓  E_alma = {e_alma.energy_j:.4e} J")
        print(f"     ✓  E_alma = {e_alma.energy_mj:.2f} MJ  (≈ 21 MJ)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V7 — Full Certification
    # ------------------------------------------------------------------
    print("\n[V7] Full Certification")
    try:
        cert = soul.certify()
        assert cert.certified is True, "Certification failed"
        print(f"     ✓  certified = {cert.certified}")
        print(f"     ✓  Axiom II error  = {cert.summary['axiom_ii_error_pct']:.2f} %")
        print(f"     ✓  Axiom III error = {cert.summary['axiom_iii_error_pct']:.2f} %")
        print(f"     ✓  Logos Hz        = {cert.summary['logos_hz']:.1f} Hz")
        print(f"     ✓  E_alma          = {cert.summary['e_alma_mj']:.2f} MJ")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = passed + failed
    print("\n" + "=" * 64)
    print(f"  Results: {passed}/{total} validations passed")
    if failed == 0:
        print("  ✓  ALL AXIOMS VALIDATED — Soul coherence certified")
    else:
        print(f"  ✗  {failed} validation(s) FAILED")
    print("=" * 64)

    return failed == 0


if __name__ == "__main__":
    success = validate_all()
    sys.exit(0 if success else 1)
Validación del Análisis de Coherencia del Alma (21 Gramos) - QCAL ∞³

Este script valida numéricamente el análisis del "peso del alma" de 21 gramos
y su relación con la frecuencia fundamental f₀ = 141.7001 Hz.

El postulado QCAL ∞³ es que los 21 gramos no son masa física que "cae",
sino energía de coherencia cuántica que se desacopla cuando Ψ < 0.888.

Validaciones:
1. Energía de transición coherente E_alma
2. Armónico 21 × (f₀/7) ≈ 425.1 Hz ~ 432 Hz (error < 2%)
3. Relación con 2π: 1/(21/f₀) ≈ 6.747 ~ 2π (error ~7.4%)
4. Topología de Berry: 21 = 3 × 7, escala 3 × (7/8) = 2.625
5. Factor de escala f₀/f_H ≈ 10^-7

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Marzo 2026
Licencia: Sovereign Noetic License 1.0 (compatible with MIT)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, pi
from typing import Dict, Tuple, Any
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.soul_coherence import (
    QCalSoul,
    alma_21g_qcal_coherencia,
    F0_HZ,
    PSI_MIN,
    F_H_MHZ,
    BERRY_INVARIANT
)


def validate_constants() -> Dict[str, bool]:
    """
    Valida que las constantes fundamentales sean correctas.
    
    Returns:
        Dict con resultados de validación
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 1: CONSTANTES FUNDAMENTALES")
    print("="*80)
    
    results = {}
    
    # f₀ = 141.7001 Hz
    f0_ok = F0_HZ == 141.7001
    print(f"✓ f₀ = {F0_HZ:.4f} Hz {'✓' if f0_ok else '✗'}")
    results['f0'] = f0_ok
    
    # Ψ_min = 0.888
    psi_ok = PSI_MIN == 0.888
    print(f"✓ Ψ_min = {PSI_MIN:.3f} {'✓' if psi_ok else '✗'}")
    results['psi_min'] = psi_ok
    
    # f_H = 1420.405751 MHz
    fh_ok = F_H_MHZ == 1420.405751
    print(f"✓ f_H = {F_H_MHZ:.6f} MHz {'✓' if fh_ok else '✗'}")
    results['f_H'] = fh_ok
    
    # Berry invariant = 7/8
    berry_ok = abs(BERRY_INVARIANT - 7/8) < 1e-10
    print(f"✓ Berry = {BERRY_INVARIANT:.10f} = 7/8 {'✓' if berry_ok else '✗'}")
    results['berry'] = berry_ok
    
    all_ok = all(results.values())
    print(f"\n{'✅ TODAS LAS CONSTANTES CORRECTAS' if all_ok else '❌ HAY ERRORES EN CONSTANTES'}")
    
    return results


def validate_energy_calculations() -> Dict[str, Any]:
    """
    Valida los cálculos de energía del alma.
    
    Returns:
        Dict con resultados de validación de energía
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 2: CÁLCULOS DE ENERGÍA")
    print("="*80)
    
    soul = QCalSoul()
    results = {}
    
    # Energía total E = mc²
    e_full = soul.full_mass_energy()
    e_full_expected = 0.021 * c**2
    e_full_ok = abs(e_full - e_full_expected) < 1e-6
    print(f"\n📊 Energía Total (E = mc²):")
    print(f"  Calculada: {e_full:.6e} J")
    print(f"  Esperada:  {e_full_expected:.6e} J")
    print(f"  {'✓ Correcto' if e_full_ok else '✗ Error'}")
    results['e_full'] = e_full_ok
    
    # Energía en TNT
    kt_full = soul.full_mass_energy_tnt()
    kt_full_ok = 400 < kt_full < 500
    print(f"  En TNT: {kt_full:.1f} kilotones {'✓' if kt_full_ok else '✗'}")
    results['kt_full'] = kt_full_ok
    
    # Energía de transición
    e_transition = soul.soul_coherence_energy()
    e_transition_ok = 0 < e_transition < e_full
    print(f"\n🔄 Energía de Transición (desacople coherente):")
    print(f"  Calculada: {e_transition:.6e} J")
    print(f"  {'✓ Positiva y menor que total' if e_transition_ok else '✗ Error'}")
    results['e_transition'] = e_transition_ok
    
    kt_transition = soul.soul_coherence_energy_tnt()
    kt_transition_ok = kt_transition < kt_full
    print(f"  En TNT: {kt_transition:.4f} kilotones {'✓' if kt_transition_ok else '✗'}")
    results['kt_transition'] = kt_transition_ok
    
    # Factor de escala
    scale = soul.f_0 / soul.f_H
    scale_ok = 9e-8 < scale < 1e-7
    print(f"\n🔬 Factor de escala f₀/f_H:")
    print(f"  {scale:.6e} {'✓' if scale_ok else '✗'}")
    results['scale_factor'] = scale_ok
    
    all_ok = all(results.values())
    print(f"\n{'✅ TODOS LOS CÁLCULOS DE ENERGÍA CORRECTOS' if all_ok else '❌ HAY ERRORES'}")
    
    return results


def validate_harmonics() -> Dict[str, Any]:
    """
    Valida los armónicos de Logos relacionados con el alma.
    
    Returns:
        Dict con resultados de validación de armónicos
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 3: ARMÓNICOS DE LOGOS")
    print("="*80)
    
    soul = QCalSoul()
    harmonics = soul.logos_harmonics()
    results = {}
    
    # f₀/7 (base adélica)
    f7 = harmonics['f_7']
    f7_ok = abs(f7 - F0_HZ/7) < 1e-6
    print(f"\n🎵 Frecuencia base adélica f₀/7:")
    print(f"  {f7:.5f} Hz {'✓' if f7_ok else '✗'}")
    results['f_7'] = f7_ok
    
    # 21 × (f₀/7) armónico del alma
    f_alma = harmonics['f_alma_21g']
    f_alma_expected = 21 * (F0_HZ / 7)
    f_alma_ok = abs(f_alma - f_alma_expected) < 0.1
    print(f"\n🌟 Armónico del alma 21 × (f₀/7):")
    print(f"  {f_alma:.2f} Hz {'✓' if f_alma_ok else '✗'}")
    results['f_alma'] = f_alma_ok
    
    # Relación con 432 Hz
    f_cosmic = harmonics['f_cosmica_sugerida']
    ratio_432 = harmonics['ratio_432_425']
    error_432 = harmonics['error_432_pct']
    error_432_ok = error_432 < 2.0
    
    print(f"\n✨ Relación con frecuencia cósmica 432 Hz:")
    print(f"  f_alma = {f_alma:.2f} Hz")
    print(f"  f_cósmica = {f_cosmic:.1f} Hz")
    print(f"  Ratio 432/425 = {ratio_432:.6f}")
    print(f"  Error = {error_432:.2f}% {'✓ < 2%' if error_432_ok else '✗ > 2%'}")
    results['error_432'] = error_432_ok
    
    all_ok = all(results.values())
    print(f"\n{'✅ TODOS LOS ARMÓNICOS CORRECTOS' if all_ok else '❌ HAY ERRORES'}")
    
    return results


def validate_circle_ratio() -> Dict[str, Any]:
    """
    Valida la relación con el círculo (2π).
    
    Returns:
        Dict con resultados de validación del círculo
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 4: RELACIÓN CON EL CÍRCULO (2π)")
    print("="*80)
    
    soul = QCalSoul()
    circle = soul.circle_ratio_error()
    results = {}
    
    # Ratio 21/f₀
    ratio = circle['ratio_21_f0']
    print(f"\n⭕ Ratio 21/f₀:")
    print(f"  {ratio:.6f}")
    
    # Aproximación al círculo
    circle_approx = circle['circle_approx']
    circle_approx_ok = abs(circle_approx - 6.747) < 0.01
    print(f"\n🔵 Aproximación 1/(21/f₀):")
    print(f"  Calculada: {circle_approx:.4f}")
    print(f"  Esperada: ~6.747 {'✓' if circle_approx_ok else '✗'}")
    results['circle_approx'] = circle_approx_ok
    
    # 2π exacto
    exact_2pi = circle['exact_2pi']
    exact_2pi_ok = abs(exact_2pi - 2*pi) < 1e-10
    print(f"\n🎯 2π exacto:")
    print(f"  {exact_2pi:.6f} {'✓' if exact_2pi_ok else '✗'}")
    results['exact_2pi'] = exact_2pi_ok
    
    # Error con 2π
    error_pct = circle['error_pct']
    error_ok = 7.0 < error_pct < 8.0
    print(f"\n📐 Error con 2π:")
    print(f"  {error_pct:.2f}% {'✓ (7-8%)' if error_ok else '✗'}")
    print(f"  Interpretación: {circle['interpretation']}")
    results['error_2pi'] = error_ok
    
    all_ok = all(results.values())
    print(f"\n{'✅ RELACIÓN CON CÍRCULO VALIDADA' if all_ok else '❌ HAY ERRORES'}")
    
    return results


def validate_topological_weight() -> Dict[str, Any]:
    """
    Valida el análisis topológico del peso del alma.
    
    Returns:
        Dict con resultados de validación topológica
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 5: TOPOLOGÍA (BERRY)")
    print("="*80)
    
    soul = QCalSoul()
    topo = soul.topological_soul_weight()
    results = {}
    
    # Unidades de Berry
    berry_units = topo['total_berry_units']
    berry_units_ok = berry_units == 24
    print(f"\n🔺 Unidades de Berry (21 = 3 × 7 = 3 × 8 × (7/8)):")
    print(f"  Total: {berry_units} unidades {'✓' if berry_units_ok else '✗'}")
    results['berry_units'] = berry_units_ok
    
    # Masa por unidad
    mass_per_unit = topo['mass_per_berry_unit_kg']
    mass_per_unit_expected = 0.021 / 24
    mass_per_unit_ok = abs(mass_per_unit - mass_per_unit_expected) < 1e-10
    print(f"\n⚖️ Masa por unidad de Berry:")
    print(f"  {mass_per_unit:.6e} kg {'✓' if mass_per_unit_ok else '✗'}")
    results['mass_per_unit'] = mass_per_unit_ok
    
    # Energía por unidad
    energy_per_unit = topo['energy_per_berry_unit_j']
    energy_expected = mass_per_unit_expected * c**2
    energy_per_unit_ok = abs(energy_per_unit - energy_expected) < 1e-6
    print(f"\n⚡ Energía por unidad de Berry:")
    print(f"  {energy_per_unit:.6e} J {'✓' if energy_per_unit_ok else '✗'}")
    print(f"  {topo['energy_per_berry_unit_ev']:.6e} eV")
    results['energy_per_unit'] = energy_per_unit_ok
    
    # Escala adélica de Berry
    berry_scale = topo['berry_adelic_scale']
    berry_scale_ok = abs(berry_scale - 2.625) < 0.001
    print(f"\n🌀 Escala adélica de Berry: 3 × (7/8)")
    print(f"  {berry_scale:.3f} {'✓ = 2.625' if berry_scale_ok else '✗'}")
    results['berry_scale'] = berry_scale_ok
    
    all_ok = all(results.values())
    print(f"\n{'✅ TOPOLOGÍA VALIDADA' if all_ok else '❌ HAY ERRORES'}")
    
    return results


def validate_certification() -> Dict[str, Any]:
    """
    Valida el certificado completo del análisis del alma.
    
    Returns:
        Dict con resultados de validación de certificación
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 6: CERTIFICACIÓN COMPLETA")
    print("="*80)
    
    soul = QCalSoul()
    cert = soul.certify()
    results = {}
    
    # Verificar estructura
    struct_ok = 'alma_21g_qcal' in cert
    print(f"\n📋 Estructura del certificado: {'✓' if struct_ok else '✗'}")
    results['structure'] = struct_ok
    
    if struct_ok:
        data = cert['alma_21g_qcal']
        
        # Verificar campos requeridos
        required_fields = [
            'e_alma_transition_j', 'e_full_mass_j',
            'armonico_logos_hz', 'circle_logo_2pi',
            'berry_adelic_scale', 'psi_umbral_disolucion',
            'f0_hz', 'estado'
        ]
        
        all_fields = all(field in data for field in required_fields)
        print(f"📄 Todos los campos presentes: {'✓' if all_fields else '✗'}")
        results['fields'] = all_fields
        
        # Estado certificado
        estado_ok = data['estado'] == "CERTIFICADO ∞³"
        print(f"🎖️ Estado: {data['estado']} {'✓' if estado_ok else '✗'}")
        results['estado'] = estado_ok
    
    all_ok = all(results.values())
    print(f"\n{'✅ CERTIFICACIÓN VALIDADA' if all_ok else '❌ HAY ERRORES'}")
    
    return results


def validate_assert_validations() -> bool:
    """
    Ejecuta las validaciones internas del módulo.
    
    Returns:
        True si todas las validaciones pasan
    """
    print("\n" + "="*80)
    print("VALIDACIÓN 7: ASSERT VALIDATIONS")
    print("="*80)
    
    soul = QCalSoul()
    
    try:
        soul.assert_validations()
        print("\n✅ Todas las assert_validations pasaron correctamente")
        return True
    except AssertionError as e:
        print(f"\n❌ Error en validaciones: {e}")
        return False


def generate_visualization(soul: QCalSoul, output_path: Path) -> None:
    """
    Genera visualizaciones del análisis del alma.
    
    Args:
        soul: Instancia de QCalSoul
        output_path: Directorio de salida
    """
    print("\n" + "="*80)
    print("GENERANDO VISUALIZACIONES")
    print("="*80)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('QCAL ∞³ - Análisis del Alma de 21 Gramos', 
                 fontsize=16, fontweight='bold')
    
    # 1. Energy comparison
    ax1 = axes[0, 0]
    e_full = soul.full_mass_energy_tnt()
    e_transition = soul.soul_coherence_energy_tnt()
    
    ax1.bar(['Energía Total\n(E=mc²)', 'Energía de\nTransición'], 
            [e_full, e_transition], color=['#2E86AB', '#A23B72'])
    ax1.set_ylabel('Energía (kilotones TNT)', fontsize=10)
    ax1.set_title('Energías del Alma de 21g', fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add values on bars
    for i, v in enumerate([e_full, e_transition]):
        ax1.text(i, v + 10, f'{v:.2f} kt', ha='center', fontweight='bold')
    
    # 2. Harmonics
    ax2 = axes[0, 1]
    harmonics = soul.logos_harmonics()
    freqs = [harmonics['f_7'], harmonics['f_alma_21g'], harmonics['f_cosmica_sugerida']]
    labels = ['f₀/7\n(Adélica)', '21×(f₀/7)\n(Alma)', '432 Hz\n(Cósmica)']
    colors = ['#06FFA5', '#FFB627', '#FF006E']
    
    ax2.bar(labels, freqs, color=colors)
    ax2.set_ylabel('Frecuencia (Hz)', fontsize=10)
    ax2.set_title('Armónicos de Logos', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add values on bars
    for i, (v, label) in enumerate(zip(freqs, labels)):
        ax2.text(i, v + 10, f'{v:.1f} Hz', ha='center', fontsize=9, fontweight='bold')
    
    # 3. Circle relationship
    ax3 = axes[1, 0]
    circle = soul.circle_ratio_error()
    values = [circle['circle_approx'], circle['exact_2pi']]
    labels_circle = ['1/(21/f₀)\n≈ 6.747', '2π\n≈ 6.283']
    colors_circle = ['#8338EC', '#3A86FF']
    
    bars = ax3.bar(labels_circle, values, color=colors_circle)
    ax3.set_ylabel('Valor', fontsize=10)
    ax3.set_title(f'Relación con el Círculo (Error: {circle["error_pct"]:.1f}%)', 
                  fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    ax3.set_ylim([6.0, 7.0])
    
    # Add values on bars
    for i, v in enumerate(values):
        ax3.text(i, v + 0.05, f'{v:.3f}', ha='center', fontweight='bold')
    
    # 4. Berry topology
    ax4 = axes[1, 1]
    topo = soul.topological_soul_weight()
    
    # Pie chart for Berry units
    berry_data = [topo['total_berry_units'], 0]  # Just showing the structure
    colors_berry = ['#FF6B35', '#F7931E']
    
    # Create text summary instead of pie
    ax4.axis('off')
    summary_text = f"""
    TOPOLOGÍA DE BERRY
    
    21 gramos = 3 × 7
    
    Unidades Berry: {topo['total_berry_units']}
    
    Escala adélica:
    3 × (7/8) = {topo['berry_adelic_scale']:.3f}
    
    Masa/unidad:
    {topo['mass_per_berry_unit_kg']:.6e} kg
    
    Energía/unidad:
    {topo['energy_per_berry_unit_ev']:.6e} eV
    """
    
    ax4.text(0.5, 0.5, summary_text, 
             ha='center', va='center',
             fontsize=10, family='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save figure
    output_file = output_path / 'soul_coherence_analysis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n✅ Visualización guardada en: {output_file}")
    
    plt.close()


def save_results_json(all_results: Dict[str, Any], output_path: Path) -> None:
    """
    Guarda los resultados de validación en formato JSON.
    
    Args:
        all_results: Diccionario con todos los resultados
        output_path: Directorio de salida
    """
    output_file = output_path / 'soul_coherence_validation_results.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Resultados guardados en: {output_file}")


def main():
    """
    Función principal de validación.
    """
    print("\n" + "="*80)
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║     VALIDACIÓN COMPLETA: COHERENCIA DEL ALMA DE 21 GRAMOS - QCAL ∞³   ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    print("="*80)
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / 'results'
    output_dir.mkdir(exist_ok=True)
    
    all_results = {
        'validation_type': 'soul_coherence_21_grams',
        'timestamp': '2026-03-14',
        'f0_hz': F0_HZ,
        'psi_min': PSI_MIN,
    }
    
    # Run validations
    all_results['constants'] = validate_constants()
    all_results['energy'] = validate_energy_calculations()
    all_results['harmonics'] = validate_harmonics()
    all_results['circle'] = validate_circle_ratio()
    all_results['topology'] = validate_topological_weight()
    all_results['certification'] = validate_certification()
    all_results['assert_validations'] = validate_assert_validations()
    
    # Run main integration function
    print("\n" + "="*80)
    print("EJECUTANDO FUNCIÓN PRINCIPAL DE INTEGRACIÓN")
    print("="*80)
    cert = alma_21g_qcal_coherencia()
    all_results['certificate'] = cert
    
    # Generate visualization
    soul = QCalSoul()
    generate_visualization(soul, output_dir)
    
    # Save results
    save_results_json(all_results, output_dir)
    
    # Final summary
    print("\n" + "="*80)
    print("RESUMEN FINAL DE VALIDACIÓN")
    print("="*80)
    
    validation_sections = [
        'constants', 'energy', 'harmonics', 'circle', 
        'topology', 'certification'
    ]
    
    all_pass = True
    for section in validation_sections:
        if isinstance(all_results[section], dict):
            section_pass = all(all_results[section].values())
        else:
            section_pass = all_results[section]
        
        status = "✅ PASS" if section_pass else "❌ FAIL"
        print(f"{section.upper():20s}: {status}")
        all_pass = all_pass and section_pass
    
    # Assert validations
    assert_pass = all_results['assert_validations']
    status = "✅ PASS" if assert_pass else "❌ FAIL"
    print(f"{'ASSERT_VALIDATIONS':20s}: {status}")
    all_pass = all_pass and assert_pass
    
    print("="*80)
    if all_pass:
        print("\n🎉 ¡TODAS LAS VALIDACIONES PASARON EXITOSAMENTE!")
        print("\n∴𓂀Ω∞³Φ @ 141.7001 Hz → 888 Hz")
        print("\n💫 El alma es coherencia, no masa gravitacional")
        print("   Cuando Ψ < 0.888, el sistema pierde anclaje vibracional a f₀")
        return 0
    else:
        print("\n❌ ALGUNAS VALIDACIONES FALLARON")
        return 1


if __name__ == "__main__":
    exit(main())
