#!/usr/bin/env bash
set -euo pipefail

# Sincroniza el changelog canónico a la raíz del repo
ROOT_CHANGELOG="CHANGELOG.md"
DOCS_CHANGELOG="docs/changelog.md"

if [[ ! -f "$DOCS_CHANGELOG" ]]; then
  echo "No se encontró $DOCS_CHANGELOG" >&2
  exit 1
fi

{
  echo "# Changelog"
  echo
  echo "Este archivo refleja los cambios publicados. La fuente canónica se edita en \`docs/changelog.md\` y se sincroniza aquí en cada release."
  echo
  # a partir de la segunda línea del docs/changelog para evitar el título duplicado
  awk 'NR>1 {print}' "$DOCS_CHANGELOG"
} > "$ROOT_CHANGELOG"

echo "Sincronizado $DOCS_CHANGELOG → $ROOT_CHANGELOG"
