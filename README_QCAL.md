# QCAL (141.7 Hz) — Análisis Reproducible

Badges: PyPI • CI • Docs • DOI (añadir cuando publiques)

## Uso rápido
```bash
pip install -e .
python -m qcal analyze --catalog GWTC-1 --band 141.7 --detector H1 --outdir artifacts
```

## Resultados

- **Tablas:** `artifacts/tables/*.csv`
- **Figuras:** `artifacts/figures/*.png`

## Reproducibilidad

```bash
cd repro/GWTC-1
pip-compile --generate-hashes requirements.in -o env.lock
./run.sh
```

## Cita

Ver CITATION.cff.
