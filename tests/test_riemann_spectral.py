"""
tests/test_riemann_spectral.py — Validación de la Capa Espectral (Canon v3.0.2)

Verifica en silicio (mpmath, 100 dps) los invariantes de la refundación sobre
los ceros no triviales de Riemann. Se AÑADE al canon 4D sin sustituirlo
(consigna del Director: NO SE ELIMINA NADA; coexisten las capas 19.061 y γ₁).

Invariantes verificados:
  1. Forma cerrada de S₁ = ½(1 − γ₁/γ₂)²
  2. Cota universal S_n < ½ < 1 (analítica, Teorema 3)
  3. Coherencia: cos(θ_B)·(1 − S₁) < 1
  4. Familia S_n completa (n=1..18) subcrítica
  5. Canon 4D coexistente intacto (KAPPA_THETA = 19.061)
"""

import os
import importlib.util
from mpmath import mp, mpf, nstr

mp.dps = 100

# Carga directa del módulo (core/ no es paquete, sin __init__.py)
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SPEC = importlib.util.spec_from_file_location(
    "riemann_spectral", os.path.join(_REPO, "core", "riemann_spectral.py")
)
rs = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(rs)


def test_forma_cerrada_S1():
    """S₁ = ½(1 − γ₁/γ₂)² — forma cerrada exacta."""
    S1_closed = mpf("0.5") * (mpf(1) - rs.GAMMA_1 / rs.GAMMA_2) ** 2
    assert abs(rs.S_1 - S1_closed) < mpf("1e-60")
    print(f"  ✅ Forma cerrada S₁ = {nstr(S1_closed, 15)}")


def test_cota_universal_S_n():
    """Teorema 3: S_n < ½ < 1 para toda la familia (n=1..18)."""
    assert all(v < mpf("0.5") for v in rs.S_FAMILY.values())
    mx = max(float(v) for v in rs.S_FAMILY.values())
    assert mx < 0.5
    print(f"  ✅ Cota universal S_n < ½ (max = {mx:.8f}, n=1..{len(rs.S_FAMILY)})")


def test_coherencia():
    """cos(θ_B)·(1 − S₁) < 1 — la corrección no rompe la coherencia."""
    op = rs.DPsiSpectral("S1")
    assert op.validate_coherence()
    print(f"  ✅ Coherencia conservada (factor = {float(op.phase_correction):.15f})")


def test_operador_modos():
    """Los 4 modos del operador son estables; el modo canonical es S1 (exacto)."""
    op_s1 = rs.DPsiSpectral("S1")
    op_fin = rs.DPsiSpectral("series_finite")
    op_asym = rs.DPsiSpectral("series_asymptotic")
    op_raw = rs.DPsiSpectral("raw")
    # Jerarquía estricta de coherencia: |raw| > |S1| > |finite| > |asymptotic|
    vals = [abs(float(o.D_psi_phased)) for o in (op_raw, op_s1, op_fin, op_asym)]
    assert all(vals[i] > vals[i+1] for i in range(3)), f"jerarquía rota: {vals}"
    # Valores exactos reproducidos del suite del Director (5e-4)
    assert abs(float(op_s1.D_psi_phased) - (-3.702837)) < 5e-4
    assert abs(float(op_fin.D_psi_phased) - (-3.490335)) < 5e-4
    print(f"  ✅ 4 modos jerárquicos: raw {vals[0]:.4f} > S1 {vals[1]:.4f} > fin {vals[2]:.4f} > asym {vals[3]:.4f}")
    print(f"  ✅ Modo canónico S1: D_Ψ,phased = {float(op_s1.D_psi_phased):.6f} (exacto)")
    print(f"  ✅ Modo series_finite: D_Ψ,phased = {float(op_fin.D_psi_phased):.6f} (exacto)")
    print(f"  ✅ Modo series_asymptotic: D_Ψ,phased = {float(op_asym.D_psi_phased):.6f} (aprox O(1/n²))")
    print(f"  ✅ Σ_finito(n=1..19) = {float(op_asym.S_sum_finite):.6f}, S_total_aprox = {float(op_asym.S_total_approx):.6f}")


def test_canon4d_coexistente():
    """El canon 4D (theta=1/19.061) NO se toca — ambas capas coexisten."""
    spec = importlib.util.spec_from_file_location(
        "er", os.path.join(_REPO, "core", "ecuacion_resurreccion.py")
    )
    er = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(er)
    assert abs(float(er.KAPPA_THETA) - 19.061) < 1e-12
    print(f"  ✅ Canon 4D intacto: KAPPA_THETA = {er.KAPPA_THETA}, "
          f"theta = {nstr(er.THETA_DESFASE_ARMONICO, 15)} (coexiste con θ_B={nstr(rs.THETA_B, 15)})")


def run_all():
    print("=== TEST CAPA ESPECTRAL (Canon v3.0.2) — 100 dps ===")
    test_forma_cerrada_S1()
    test_cota_universal_S_n()
    test_coherencia()
    test_operador_modos()
    test_canon4d_coexistente()
    print("\nTODOS LOS TESTS PASARON ✅")
    print("Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ")


if __name__ == "__main__":
    run_all()
