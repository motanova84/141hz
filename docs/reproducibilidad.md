# Reproducibilidad

QCAL garantiza reproducibilidad completa de los análisis mediante gestión rigurosa de dependencias y versionado.

## Gestión de dependencias

### pip-compile

Utilizamos `pip-compile` (de `pip-tools`) para gestionar dependencias de forma determinística:

```bash
# Instalar pip-tools
pip install pip-tools

# Compilar requirements.txt desde requirements.in
pip-compile requirements.in

# Sincronizar entorno con requirements.txt
pip-sync requirements.txt
```

### Estructura de archivos

```
requirements.in        # Dependencias directas (editables)
requirements.txt       # Dependencias pinned (generado automáticamente)
```

### Actualizar dependencias

```bash
# Actualizar todas las dependencias
pip-compile --upgrade requirements.in

# Actualizar solo una dependencia específica
pip-compile --upgrade-package numpy requirements.in
```

## Entornos virtuales

### Crear entorno reproducible

```bash
# Python 3.11 (recomendado)
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Conda (alternativa)

```bash
# Crear entorno con conda
conda create -n qcal python=3.11
conda activate qcal
pip install -r requirements.txt
```

## Docker

Para reproducibilidad total, usamos Docker:

```bash
# Construir imagen
docker build -t qcal:latest .

# Ejecutar análisis
docker run -v $(pwd)/results:/app/results qcal:latest \
  qcal analyze --event GW150914 --detector H1
```

### Docker Compose

```bash
# Ejecutar con docker-compose
docker-compose up analysis
```

## CI/CD

### GitHub Actions

Los workflows de CI garantizan reproducibilidad:

- **`.github/workflows/ci.yml`**: Tests básicos en cada commit
- **`.github/workflows/analyze.yml`**: Análisis completo en schedule
- **`.github/workflows/production-qcal.yml`**: Pipeline de producción

### Matriz de pruebas

Testeamos en múltiples configuraciones:

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    python-version: ['3.11', '3.12']
```

## SBOM (Software Bill of Materials)

Generamos SBOM automáticamente en cada release:

```bash
# Generar SBOM local
pip install cyclonedx-bom
cyclonedx-py -r -i requirements.txt -o sbom.xml
```

## Escaneo de vulnerabilidades

### OSV Scanner

```bash
# Instalar osv-scanner
go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Escanear dependencias
osv-scanner --lockfile requirements.txt
```

### GitHub Dependabot

Dependabot analiza automáticamente `requirements.txt` y crea PRs para actualizaciones de seguridad.

## Versionado

### Semantic Versioning

Seguimos SemVer: `MAJOR.MINOR.PATCH`

- **MAJOR**: Cambios incompatibles en API
- **MINOR**: Nueva funcionalidad compatible
- **PATCH**: Correcciones de bugs

### Tags y releases

```bash
# Crear tag
git tag -a v0.1.1 -m "Release v0.1.1"
git push --tags

# Ver tags
git tag -l
```

## Checksums y firmas

### Verificar integridad de datos

```bash
# Generar checksums
sha256sum results/*.json > checksums.txt

# Verificar
sha256sum -c checksums.txt
```

## Parámetros de análisis

Todos los parámetros se documentan en `analysis_plan.json`:

```json
{
  "frequency_target": 141.7001,
  "time_windows": {...},
  "spectral_method": "welch",
  "validation_controls": [...]
}
```

Ver [analysis_plan.json](../analysis_plan.json) completo.

## Logs y trazabilidad

Los análisis generan logs detallados:

```bash
# Ejecutar con logs verbosos
qcal analyze --event GW150914 --detector H1 --verbose

# Logs se guardan en
results/logs/analysis_YYYYMMDD_HHMMSS.log
```

## Archivado a largo plazo

### Zenodo

Releases importantes se archivan en Zenodo con DOI:

- [https://zenodo.org/](https://zenodo.org/)
- Ver [ZENODO_PUBLICATION_GUIDE.md](../ZENODO_PUBLICATION_GUIDE.md)

## Buenas prácticas

1. ✅ **Siempre** usar `requirements.txt` (no instalar paquetes ad-hoc)
2. ✅ **Versionar** todos los scripts de análisis
3. ✅ **Documentar** parámetros de análisis
4. ✅ **Archivar** resultados con checksums
5. ✅ **Testear** en múltiples entornos antes de publicar

## Ver también

- [CLI](cli.md): Referencia de comandos
- [Validación](validation.md): Tests y verificación
- [CI/CD Implementation](../CI_CD_IMPLEMENTATION.md): Detalles de workflows
```bash
cd repro/GWTC-1
pip-compile --generate-hashes requirements.in -o env.lock
./run.sh
```

Esto crea un entorno con hashes inmutables y reproduce tablas/figuras de GWTC-1.
