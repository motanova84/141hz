#!/usr/bin/env bash
# QCAL ∞³ — Instalador de toolchain Lean 4 + Mathlib
# Uso: bash scripts/install_lean_toolchain.sh
set -euo pipefail

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  QCAL ∞³ — INSTALACIÓN TOOLCHAIN LEAN 4 + MATHLIB            ║"
echo "╚══════════════════════════════════════════════════════════════╝"

TOOLCHAIN="${QCAL_LEAN_TOOLCHAIN:-leanprover/lean4:v4.7.0}"

# 1. Elan (Lean version manager)
if ! command -v elan >/dev/null 2>&1; then
  echo "[1/4] Instalando elan…"
  curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf \
    | sh -s -- -y --default-toolchain none
  # shellcheck disable=SC1091
  source "${HOME}/.elan/env"
else
  echo "[1/4] elan ya instalado."
fi

# 2. Lean 4 stable
echo "[2/4] Instalando toolchain ${TOOLCHAIN}…"
elan toolchain install "${TOOLCHAIN}"
elan default "${TOOLCHAIN}"

# 3. Lake (build system) sanity check
echo "[3/4] Verificando lake…"
lake --version

# 4. Descarga de dependencias del proyecto
PROJECT="${QCAL_LEAN_DIR:-src/qcal_lean}"
if [[ -f "${PROJECT}/lakefile.lean" ]]; then
  echo "[4/4] Resolviendo dependencias en ${PROJECT}…"
  (cd "${PROJECT}" && lake update && lake exe cache get || true)
else
  echo "[4/4] No se encontró ${PROJECT}/lakefile.lean — omitiendo."
fi

echo "✅ Toolchain listo."
lean --version
lake --version
