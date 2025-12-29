# Checklist de Publicación (QCAL)

## 1) Preparación

- [ ] Actualiza versión en `pyproject.toml` y `src/qcal/__init__.py`
- [ ] Actualiza `CITATION.cff` (version, date-released, DOI si aplica)
- [ ] Completa `docs/changelog.md` (vX.Y.Z, fecha, cambios)

## 2) Verificación local

```bash
pytest -q --cov=src/qcal --cov-report=xml
cd repro/GWTC-1 && pip-compile --generate-hashes requirements.in -o env.lock && ./run.sh
mkdocs build
```

## 3) CI debe pasar

- [ ] Build & tests ok
- [ ] SBOM (`sbom.json`) generado
- [ ] OSV scan revisado (sin CVEs críticos)
- [ ] Artifacts subidos (figuras, tablas, coverage)

## 4) Tag & GitHub Release

```bash
git tag vX.Y.Z
git push --tags
```

- [ ] Crea GitHub Release y adjunta:
  - `sbom.json`
  - `artifacts/figures/*.png`, `artifacts/tables/*.csv`
  - `coverage.xml` (opcional)
  - enlace a Docs (https://motanova84.github.io/141hz)

## 5) Publicación PyPI (opcional)

Requiere `release.yml` configurado.

- [ ] Enviar tag vX.Y.Z → GitHub Actions publica en PyPI.
- [ ] Verifica en PyPI y añade badge en README.md.

## 6) Zenodo DOI (opcional)

- [ ] Crea o actualiza release en Zenodo (auto-archivado GitHub si está vinculado).
- [ ] Copia el DOI en README.md y CITATION.cff.

## 7) GitHub Pages (Docs)

- [ ] `mkdocs build` local OK
- [ ] Workflow `docs.yml` despliega a gh-pages
- [ ] Verifica https://motanova84.github.io/141hz

## 8) Comunicación

- [ ] Actualiza `docs/dataroom/valuation_onepager.md` con métricas nuevas
- [ ] Comparte enlace de Release + Docs con pilotos/partners
