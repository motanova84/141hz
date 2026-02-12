# QCAL (141.7 Hz) — Análisis Reproducible

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18557905.svg)](https://doi.org/10.5281/zenodo.18557905)

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
