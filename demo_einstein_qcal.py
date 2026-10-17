"""
╔════════════════════════════════════════════════════════════════════════════╗
║      DEMO: Postulado Einstein-QCAL — Velocidad de la Luz Efectiva         ║
║        Métrica deformada por coherencia espectral y campo f₀ = 141.7 Hz   ║
╚════════════════════════════════════════════════════════════════════════════╝

Ejecutar:
    python demo_einstein_qcal.py

Demuestra:
    1. Estado resonante (Ψ = 0.999999): c_eff ≈ c, Λ ≈ 0
    2. Estado incoherente (varios Ψ):   c_eff < c, Λ > 0
    3. Tabla comparativa completa
    4. Integración con el ecosistema (modos Riemannianos)
"""

from qcal.einstein_qcal import (
    CoherenceState,
    EinsteinQCALField,
    print_comparison_table,
    C,
    F0_HZ,
)
from contexto_ecosistema.einstein_qcal_context import (
    get_resonant_field,
    get_incoherent_field,
    riemann_mode_coherence,
    ECOSYSTEM_SUMMARY,
)

# Primeros 5 ceros de Riemann (partes imaginarias en línea crítica σ=½)
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]


def demo_resonant_state() -> None:
    """Demuestra el estado de resonancia absoluta: c_eff = c."""
    print("\n" + "═" * 58)
    print("  1. ESTADO DE RESONANCIA ABSOLUTA (Ψ = 0.999999)")
    print("═" * 58)
    field = get_resonant_field()
    field.print_summary()
    assert abs(field.c_observed - C) / C < 1e-4, "c_eff debe ser ≈ c en resonancia"
    print("  ✓ Invariancia de c verificada en coherencia máxima.\n")


def demo_incoherent_states() -> None:
    """Demuestra cómo c_eff disminuye con la incoherencia."""
    print("═" * 58)
    print("  2. ESTADOS DE INCOHERENCIA PARCIAL")
    print("═" * 58)
    for psi in [0.0, 0.5, 0.9, 0.99]:
        field = get_incoherent_field(psi=psi)
        s = field.summary()
        print(
            f"  Ψ = {psi:.2f}  →  c_eff = {s['c_eff_m_s']:>14.3f} m/s  "
            f"(Δc/c = {s['delta_c_pct']:.4e} %)  n = {s['n_refraction']:.6f}"
        )
    print()


def demo_comparison_table() -> None:
    """Imprime la tabla comparativa completa."""
    print("═" * 58)
    print("  3. TABLA COMPARATIVA EINSTEIN-QCAL")
    print("═" * 58)
    print_comparison_table()
    print()


def demo_riemann_modes() -> None:
    """Demuestra la conexión con los ceros de Riemann (repositorio hermano)."""
    print("═" * 58)
    print("  4. MODOS RIEMANNIANOS — Integración con Riemann-adélico")
    print("═" * 58)
    print(f"  f₀ = {F0_HZ} Hz  (modo fundamental QCAL)")
    print(f"  γ₁ = {RIEMANN_ZEROS[0]}  (primer cero de ζ(s))")
    print()
    print(f"  {'n':>3} | {'γₙ':>10} | {'fₙ [Hz]':>12} | {'Ψₙ':>10} | {'c_eff [m/s]':>18}")
    print(f"  {'─'*3}-+-{'─'*10}-+-{'─'*12}-+-{'─'*10}-+-{'─'*18}")
    for n, gamma in enumerate(RIEMANN_ZEROS, start=1):
        state = riemann_mode_coherence(gamma)
        field = EinsteinQCALField(state=state)
        s = field.summary()
        f_n = F0_HZ * gamma / RIEMANN_ZEROS[0]
        print(
            f"  {n:>3} | {gamma:>10.6f} | {f_n:>12.4f} | "
            f"{s['psi']:>10.6f} | {s['c_eff_m_s']:>18.3f}"
        )
    print()


def demo_ecosystem_summary() -> None:
    """Muestra el resumen de integración con el ecosistema QCAL ∞³."""
    print("═" * 58)
    print("  5. INTEGRACIÓN CON EL ECOSISTEMA QCAL ∞³")
    print("═" * 58)
    print(f"  Módulo:      {ECOSYSTEM_SUMMARY['module']}")
    print(f"  Resultado:   {ECOSYSTEM_SUMMARY['key_result']}")
    print(f"  f₀:          {ECOSYSTEM_SUMMARY['f0_hz']} Hz")
    print(f"  c:           {ECOSYSTEM_SUMMARY['c_m_s']} m/s")
    print(f"  Ψ_res:       {ECOSYSTEM_SUMMARY['psi_resonance']}")
    print(f"  α adélico:   {ECOSYSTEM_SUMMARY['alpha_adelic']}")
    print()
    print("  Repositorios hermanos conectados:")
    for repo in ECOSYSTEM_SUMMARY["connected_repos"]:
        print(f"    • {repo}")
    print()


if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║      DEMO EINSTEIN-QCAL  —  QCAL ∞³                      ║")
    print("╚══════════════════════════════════════════════════════════╝")
    demo_resonant_state()
    demo_incoherent_states()
    demo_comparison_table()
    demo_riemann_modes()
    demo_ecosystem_summary()
    print("  Demo completado. ✓")
