#!/usr/bin/env python3
"""
QCAL ∞³ — Contador de sorries en el kernel Lean 4.

Uso:
    python scripts/count_lean_sorries.py [--max 0] [--root src/qcal_lean/QCAL]

Devuelve exit code 1 si SORRIES > --max.

Sello: QCAL-HILO-A
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SORRY_RE = re.compile(r"(?<![A-Za-z0-9_])sorry(?![A-Za-z0-9_])")
COMMENT_LINE = re.compile(r"^\s*--")


def count_file(path: Path) -> int:
    n = 0
    in_block = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        # gestión rudimentaria de bloques /- … -/
        if "/-" in stripped and "-/" not in stripped:
            in_block = True
            continue
        if in_block:
            if "-/" in stripped:
                in_block = False
            continue
        if COMMENT_LINE.match(line):
            continue
        # eliminar comentario de línea
        code = line.split("--", 1)[0]
        n += len(SORRY_RE.findall(code))
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="src/qcal_lean/QCAL")
    ap.add_argument("--max", type=int, default=8,
                    help="Máximo tolerado (default 8, objetivo 0)")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"❌ Ruta no encontrada: {root}")
        return 2

    files = sorted(root.rglob("*.lean"))
    total = 0
    per_file = []
    for f in files:
        n = count_file(f)
        per_file.append((f, n))
        total += n

    print("=" * 62)
    print("QCAL ∞³ — SORRY COUNTER (Hilo A)")
    print("=" * 62)
    for f, n in per_file:
        mark = "✅" if n == 0 else "⚠️"
        print(f"  {mark}  {n:>3}  {f}")
    print("-" * 62)
    print(f"  TOTAL: {total} sorries  (máximo tolerado: {args.max})")
    if total > args.max:
        print(f"❌ FAILED: {total} > {args.max}")
        return 1
    print(f"✅ PASSED: {total} ≤ {args.max}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
