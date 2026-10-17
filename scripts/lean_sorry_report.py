#!/usr/bin/env python3
"""
QCAL Hilo A — Reporte estructurado de sorries en el kernel Lean.

Extiende `count_lean_sorries.py` con salida JSON diff-friendly:
por cada archivo, lista los números de línea con `sorry`, el teorema
contenedor (por búsqueda hacia atrás del `theorem`/`lemma` más cercano)
y el total global.

Uso:
    python scripts/lean_sorry_report.py [--root src/qcal_lean/QCAL] \
        [--out sorry_report.json] [--print]

Sello: QCAL-HILO-A-SORRY-REPORT ∴ 𓂀 Ω ∞³ Φ
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

SORRY_RE = re.compile(r"(^|[^A-Za-z0-9_])sorry([^A-Za-z0-9_]|$)")
THEOREM_RE = re.compile(r"^\s*(theorem|lemma|example|def)\s+([A-Za-z_][A-Za-z0-9_']*)")
LINE_COMMENT_RE = re.compile(r"^\s*--")


def strip_block_comments(text: str) -> str:
    """Elimina bloques /- ... -/ (no anidados) preservando líneas."""
    out = []
    i = 0
    depth = 0
    while i < len(text):
        if text[i:i + 2] == "/-":
            depth += 1
            i += 2
            continue
        if text[i:i + 2] == "-/" and depth > 0:
            depth -= 1
            i += 2
            continue
        if depth > 0:
            out.append("\n" if text[i] == "\n" else " ")
        else:
            out.append(text[i])
        i += 1
    return "".join(out)


def find_container(lines: list[str], sorry_line_idx: int) -> Optional[str]:
    """Busca hacia atrás el nombre del teorema/lemma más cercano."""
    for j in range(sorry_line_idx, -1, -1):
        m = THEOREM_RE.match(lines[j])
        if m:
            return m.group(2)
    return None


def scan_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    stripped = strip_block_comments(raw)
    lines_stripped = stripped.splitlines()
    lines_raw = raw.splitlines()

    findings: list[dict] = []
    for idx, line in enumerate(lines_stripped):
        if LINE_COMMENT_RE.match(line):
            continue
        if SORRY_RE.search(line):
            container = find_container(lines_raw, idx)
            findings.append({
                "line": idx + 1,
                "theorem": container,
                "source": lines_raw[idx].strip(),
            })
    return {
        "file": str(path),
        "count": len(findings),
        "sorries": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="QCAL Lean sorry reporter (JSON)")
    ap.add_argument("--root", default="src/qcal_lean/QCAL",
                    help="Directorio raíz del kernel Lean")
    ap.add_argument("--out", default=None, help="Ruta de salida JSON")
    ap.add_argument("--print", action="store_true",
                    help="Imprime el JSON a stdout además de escribirlo")
    ap.add_argument("--max", type=int, default=None,
                    help="Si se especifica, exit=2 cuando total > max")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"[ERROR] Raíz no existe: {root}", file=sys.stderr)
        return 1

    files = sorted(root.rglob("*.lean"))
    per_file = [scan_file(p) for p in files]
    total = sum(f["count"] for f in per_file)

    report = {
        "seal": "QCAL-HILO-A-SORRY-REPORT",
        "root": str(root),
        "total": total,
        "files": per_file,
    }

    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(payload + "\n", encoding="utf-8")
    if args.print or not args.out:
        print(payload)

    if args.max is not None and total > args.max:
        print(f"[FAIL] total={total} > max={args.max}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
