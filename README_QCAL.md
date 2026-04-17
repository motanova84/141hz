# QCAL (141.7 Hz) — Análisis Reproducible

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18557905.svg)](https://doi.org/10.5281/zenodo.18557905)

## Prior Art / Registro de Autoría

Este repositorio se integra en el ecosistema **MCP Noésico QCAL-EPR (QCAL ∞³)**, con trabajo público previo desde 2024.

- **Zenodo (141hz)**: [10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)
- **SafeCreative (autor JMMB84)**: [safecreative.org/creators/JMMB84](https://www.safecreative.org/creators/JMMB84)
- **Ecosistema relacionado**: QCAL-BUS, Riemann-adelic, biologia-cuantica-noesica y demás repositorios QCAL ∞³.

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
