# Guía de Reproducibilidad - QCAL GW250114-141Hz

## Introducción

Este documento proporciona instrucciones completas para asegurar la reproducibilidad de todos los análisis y resultados del proyecto QCAL. La reproducibilidad es un pilar fundamental de la investigación científica y este proyecto implementa múltiples capas de garantías.

## Principios de Reproducibilidad

### 1. Versiones Exactas de Dependencias

Todos los análisis de producción utilizan `ENV.lock` que contiene versiones exactas de todas las dependencias Python.

**Garantía**: Dos instalaciones desde `ENV.lock` producirán el mismo entorno.

### 2. Checksums de Resultados

Todos los resultados incluyen checksums SHA256 que permiten verificar que los resultados no han sido alterados y que los cálculos se ejecutaron correctamente.

**Garantía**: Dos ejecuciones con el mismo entorno producirán resultados con checksums idénticos.

### 3. Snapshots de Entorno

Cada ejecución de producción genera un snapshot completo del entorno computacional.

**Garantía**: Es posible reconstruir el entorno exacto usado para cualquier análisis.

### 4. Control de Versiones de Código

Todo el código está bajo control de versiones Git con commits referenciados en los resultados.

**Garantía**: Es posible recuperar la versión exacta del código usada para cualquier análisis.

## Uso Básico

### Instalación Reproducible

```bash
# Clonar el repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar desde ENV.lock (reproducibilidad garantizada)
pip install -r ENV.lock

# Verificar la instalación
python scripts/validate_reproducibility.py
```

### Ejecución Reproducible

```bash
# Ejecutar análisis con snapshot de entorno
python scripts/validate_reproducibility.py --generate-snapshot --output environment.json

# Ejecutar validación principal
python validate_v5_coronacion.py --precision 50

# Generar checksums de resultados
find results/ -type f -name "*.json" -exec sha256sum {} \; > results/checksums.txt

# Archivar todo para reproducibilidad futura
tar -czf analysis-$(date +%Y%m%d).tar.gz results/ environment.json ENV.lock
```

## Validación de Reproducibilidad

### Script de Validación Automatizada

El proyecto incluye `scripts/validate_reproducibility.py` que verifica:

1. ✅ Versión de Python (3.11 o 3.12)
2. ✅ Dependencias coinciden con ENV.lock
3. ✅ Checksums de resultados coinciden

```bash
# Validación básica
python scripts/validate_reproducibility.py

# Validación estricta (falla si hay discrepancias)
python scripts/validate_reproducibility.py --strict

# Generar snapshot de entorno
python scripts/validate_reproducibility.py --generate-snapshot --output snapshot.json
```

### Verificación Manual

```bash
# 1. Verificar versión de Python
python3 --version
# Debe ser 3.11.x o 3.12.x

# 2. Verificar dependencias
pip freeze > installed.txt
diff ENV.lock installed.txt

# 3. Verificar checksums de resultados
cd results/
sha256sum -c checksums.txt
```

## Pipelines Reproducibles

### GWTC-1 Pipeline

El directorio `repro/GWTC-1/` contiene un pipeline completamente reproducible:

```bash
cd repro/GWTC-1/

# Ejecutar pipeline completo
./run.sh

# Verificar reproducibilidad ejecutando dos veces
./run.sh
mv ../../artifacts/GWTC-1 ../../artifacts/GWTC-1_run1
./run.sh
mv ../../artifacts/GWTC-1 ../../artifacts/GWTC-1_run2

# Comparar checksums
diff ../../artifacts/GWTC-1_run1/checksums.txt \
     ../../artifacts/GWTC-1_run2/checksums.txt

# Si no hay diferencias, el pipeline es reproducible ✅
```

### Estructura del Pipeline

```
repro/GWTC-1/
├── env.lock           # Dependencias con hashes SHA256
├── run.sh            # Script principal del pipeline
├── Makefile          # Comandos automatizados
└── README.md         # Documentación

artifacts/GWTC-1/     # Resultados del pipeline
├── environment.txt   # Snapshot del entorno
├── analysis_plan.json # Manifiesto de análisis
├── summary.json      # Resultados agregados
├── checksums.txt     # SHA256 de todos los archivos
├── H1/              # Resultados detector LIGO Hanford
├── L1/              # Resultados detector LIGO Livingston
└── V1/              # Resultados detector Virgo
```

## Workflows CI/CD

### Production QCAL Workflow

El workflow `.github/workflows/production-qcal.yml` implementa reproducibilidad:

1. **Instala desde ENV.lock**: Asegura versiones exactas
2. **Genera snapshot de entorno**: Documenta el entorno usado
3. **Ejecuta validaciones con precisión fija**: `--precision 50`
4. **Genera checksums**: SHA256 de todos los resultados
5. **Retiene artefactos**: 30 días de retención

### Dependency Health Workflow

El workflow `.github/workflows/dependency-health.yml`:

1. Escanea vulnerabilidades semanalmente
2. Verifica compatibilidad Python 3.11 y 3.12
3. Genera reportes de salud de dependencias
4. Crea issues automáticamente para vulnerabilidades reales

## Mejores Prácticas

### Para Investigadores

1. **Siempre usar ENV.lock**
   ```bash
   pip install -r ENV.lock  # ✅ Correcto
   pip install -r requirements.txt  # ❌ No reproducible
   ```

2. **Documentar el entorno**
   ```bash
   python scripts/validate_reproducibility.py --generate-snapshot --output env.json
   ```

3. **Guardar checksums con resultados**
   ```bash
   find results/ -type f -exec sha256sum {} \; > results/checksums.txt
   ```

4. **Archivar para el futuro**
   ```bash
   tar -czf analysis-YYYYMMDD.tar.gz results/ env.json ENV.lock
   ```

### Para Desarrolladores

1. **Actualizar ENV.lock después de cambios**
   ```bash
   # Después de modificar requirements.txt
   python3 -m venv venv_temp
   source venv_temp/bin/activate
   pip install -r requirements.txt
   pip freeze > ENV.lock
   deactivate
   rm -rf venv_temp
   ```

2. **Probar reproducibilidad localmente**
   ```bash
   # Ejecutar dos veces y comparar
   python validate_v5_coronacion.py --precision 50 > run1.json
   python validate_v5_coronacion.py --precision 50 > run2.json
   diff run1.json run2.json  # Debe estar vacío
   ```

3. **Validar en CI antes de merge**
   - Los workflows automáticamente validan reproducibilidad
   - Revisar artifacts y checksums en cada PR

## Verificación de Integridad de Datos

### Checksums SHA256

Todos los archivos de datos y resultados deben tener checksums:

```bash
# Generar checksums
sha256sum file1.json file2.json > checksums.txt

# Verificar checksums
sha256sum -c checksums.txt

# Ejemplo de salida exitosa:
# file1.json: OK
# file2.json: OK
```

### Proveniencia de Datos

Documentar el origen de todos los datos:

```json
{
  "data_source": "GWOSC",
  "event": "GW150914",
  "detector": "H1",
  "download_date": "2025-01-06T15:30:00Z",
  "url": "https://gwosc.org/...",
  "checksum": "sha256:abc123..."
}
```

## Resolución de Problemas

### Discrepancias en Dependencias

**Problema**: `validate_reproducibility.py` reporta versiones diferentes

**Solución**:
```bash
# Reinstalar desde ENV.lock
pip uninstall -y -r <(pip freeze)
pip install -r ENV.lock
```

### Checksums No Coinciden

**Problema**: Los checksums de resultados no coinciden entre ejecuciones

**Causas posibles**:
1. Diferentes versiones de dependencias
2. Diferentes seeds aleatorios
3. Comportamiento no determinista (punto flotante, paralelización)

**Solución**:
```bash
# Verificar entorno
python scripts/validate_reproducibility.py --strict

# Si las dependencias coinciden, revisar el código para:
# - Seeds aleatorios fijos
# - Ordenamiento determinista
# - Evitar paralelización no determinista
```

### Python Version Mismatch

**Problema**: Versión de Python no compatible

**Solución**:
```bash
# Instalar Python 3.11 o 3.12
# Ubuntu/Debian
sudo apt-get install python3.11

# macOS
brew install python@3.11

# Luego crear venv con versión correcta
python3.11 -m venv venv
```

## Formato de Archivos

### environment_snapshot.json

```json
{
  "python_version": "3.11.7",
  "platform": {
    "system": "Linux",
    "release": "5.15.0",
    "machine": "x86_64"
  },
  "timestamp": "2025-01-06T20:00:00Z",
  "git": {
    "commit": "a1b2c3d4",
    "branch": "main"
  }
}
```

### checksums.txt

```
a1b2c3d4...  ./results/validation_v5.json
e5f6g7h8...  ./results/riemann_zeros.json
i9j0k1l2...  ./results/at2020afhd_validation.json
```

## Referencias

- **SEGURIDAD.md**: Política de seguridad (español)
- **SECURITY.md**: Security policy (inglés)
- **RESUMEN DE SEGURIDAD.md**: Resumen de seguridad (español)
- **SECURITY_SUMMARY.md**: Security summary (inglés)
- **repro/GWTC-1/README.md**: Pipeline reproducible GWTC-1
- **ENV.lock**: Archivo de bloqueo de dependencias

## Contacto

Para preguntas sobre reproducibilidad:
- **Email**: institutoconsciencia@proton.me
- **Issues**: https://github.com/motanova84/141hz/issues

---

**Última actualización**: 2025-01-06  
**Versión**: 1.0.0  
**Mantenedor**: QCAL Team
