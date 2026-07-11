#!/usr/bin/env python3
"""
QCAL Hilo A — Test runner estructural del kernel Lean.

Verifica que la estructura del kernel Lean sea sana SIN depender de
`lake build` (que requiere red + toolchain instalado). Comprueba:

  · Existencia de `lean-toolchain` y contenido esperado.
  · Existencia de `lakefile.lean` con paquete `QCAL`.
  · Existencia de los módulos del kernel.
  · Presencia de los teoremas / definiciones nombrados por API pública.
  · Consistencia entre `count_lean_sorries.py` y `lean_sorry_report.py`.

Uso:
    python scripts/test_qcal_lean.py

Exit 0 si todo pasa; 1 en el primer fallo.

Sello: QCAL-HILO-A-TEST-KERNEL ∴ 𓂀 Ω ∞³ Φ
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KERNEL = ROOT / "src" / "qcal_lean"
QCAL_DIR = KERNEL / "QCAL"

EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.7.0"

EXPECTED_SYMBOLS: dict[str, list[str]] = {
    "F_Ψ_Purified.lean": [
        "ΨSpace",
        "FieldParams",
        "F_Ψ_Purified",
        "QCAL_fixed",
        "F0_hz",
        "delta_f_observable",
        "delta_f_at_zero",
        "delta_f_linear",
        "omega_Psi",
        "omega_Psi_nonneg",
        "omega_Psi_sq",
    ],
    "Domain_Invariant.lean": [
        "D",
        "barrier_A_lower",
        "barrier_A_upper",
        "barrier_S_lower",
        "barrier_S_upper",
        "barrier_P_lower",
        "barrier_P_upper",
        "Nagumo_A_lower",
        "Domain_Invariant",
    ],
    "Stability.lean": [
        "V_Lyapunov",
        "V_positive",
        "V_zero_at_QCAL",
        "V_dot",
        "V_derivative_negative",
    ],
    "Completeness.lean": [
        "flows_to_QCAL",
        "QCAL_completeness",
    ],
}


class TestFail(Exception):
    pass


def check(name: str, cond: bool, detail: str = "") -> None:
    marker = "✅" if cond else "❌"
    print(f"  {marker} {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        raise TestFail(name)


def test_toolchain() -> None:
    print("[1] lean-toolchain")
    path = KERNEL / "lean-toolchain"
    check("existe lean-toolchain", path.exists())
    content = path.read_text(encoding="utf-8").strip()
    check(
        f"contenido = {EXPECTED_TOOLCHAIN}",
        content == EXPECTED_TOOLCHAIN,
        f"leído: {content!r}",
    )


def test_lakefile() -> None:
    print("[2] lakefile.lean")
    lf = KERNEL / "lakefile.lean"
    check("existe lakefile.lean", lf.exists())
    text = lf.read_text(encoding="utf-8")
    check("declara package QCAL", "package" in text and "QCAL" in text)


def test_modules_exist() -> None:
    print("[3] módulos del kernel")
    for fname in EXPECTED_SYMBOLS:
        check(f"existe {fname}", (QCAL_DIR / fname).exists())


def test_symbols() -> None:
    print("[4] símbolos por módulo")
    for fname, symbols in EXPECTED_SYMBOLS.items():
        text = (QCAL_DIR / fname).read_text(encoding="utf-8")
        for sym in symbols:
            check(f"{fname} contiene `{sym}`", sym in text)


def test_sorry_consistency() -> None:
    print("[5] consistencia contadores de sorries")
    # Ejecuta reporter JSON
    report_json = subprocess.check_output(
        [sys.executable, str(ROOT / "scripts" / "lean_sorry_report.py"),
         "--root", str(QCAL_DIR), "--print"],
        cwd=ROOT,
    ).decode()
    report = json.loads(report_json)
    total_report = report["total"]

    # Ejecuta contador clásico si existe
    counter = ROOT / "scripts" / "count_lean_sorries.py"
    if counter.exists():
        out = subprocess.check_output(
            [sys.executable, str(counter)],
            cwd=ROOT,
        ).decode()
        # Extrae número tras "TOTAL:"
        total_counter = None
        for line in out.splitlines():
            if "TOTAL" in line:
                for tok in line.replace(":", " ").split():
                    if tok.isdigit():
                        total_counter = int(tok)
                        break
                break
        check(
            f"reporter.total == counter.total ({total_report})",
            total_counter == total_report,
            f"reporter={total_report}, counter={total_counter}",
        )
    else:
        check("reporter.total >= 0", total_report >= 0,
              f"total={total_report} (contador clásico ausente)")


def main() -> int:
    print("QCAL-HILO-A — Test estructural del kernel Lean")
    print("=" * 60)
    try:
        test_toolchain()
        test_lakefile()
        test_modules_exist()
        test_symbols()
        test_sorry_consistency()
    except TestFail as e:
        print(f"\n❌ FALLO: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        return 1
    print("=" * 60)
    print("✅ TODOS LOS TESTS ESTRUCTURALES PASARON")
    return 0


if __name__ == "__main__":
    sys.exit(main())
