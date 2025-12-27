# Protocolo Sage ∴ - Documentación

## 🌟 Introducción

El **Protocolo Sage ∴** es un sistema de activación de sabios vibracionales que permite ejecutar scripts `.sage` (SageMath) para verificar principios del **Campo QCAL ∞³** con precisión arbitraria.

### Elementos del Campo QCAL ∞³

- **RΨ** (Radio Cuántico del Campo): `RΨ = c·ℓ_p / (2πf₀)`
- **f₀ = 141.7001 Hz** (Frecuencia del Origen)
- **ζ(s)** (Zeta como vibración aritmética)
- **αΨ** (Derivada consciente de la creación)

## 📦 Instalación

### Requisitos Previos

1. **Python 3.9+**: El módulo está implementado en Python
2. **SageMath** (opcional pero recomendado): Para ejecutar scripts `.sage`

```bash
# Instalar SageMath (Ubuntu/Debian)
sudo apt-get install sagemath

# Instalar SageMath (macOS con Homebrew)
brew install --cask sage

# Instalar SageMath (desde fuente)
# Visita: https://www.sagemath.org/
```

### Verificar Instalación

```bash
# Verificar que Sage está instalado
python scripts/sage_activation.py --verificar

# Debería mostrar:
# ✅ Sage instalado: SageMath version X.Y...
```

## 🚀 Uso

### 1. Desde Línea de Comandos

#### Listar Sabios Disponibles

```bash
python scripts/sage_activation.py --listar scripts/
```

**Salida esperada:**
```
📚 Sabios encontrados en scripts/:
   • scripts/validacion_radio_cuantico.sage
```

#### Activar un Sabio

```bash
python scripts/sage_activation.py scripts/validacion_radio_cuantico.sage
```

**Salida esperada:**
```
⚛️ Invocando al Sabio: scripts/validacion_radio_cuantico.sage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
================================================================================
VALIDACIÓN NUMÉRICA DEL RADIO CUÁNTICO RΨ (SageMath)
================================================================================

Constantes fundamentales (precisión de 100 dígitos):
--------------------------------------------------------------------------------
  c  = 299792458 m/s
  ℓ_p = 1.616255e-35 m
  f₀ = 141.7001 Hz
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sabio activado con éxito ∴
   Campo QCAL ∞³ verificado en: scripts/validacion_radio_cuantico.sage
```

#### Ayuda

```bash
python scripts/sage_activation.py --help
```

### 2. Desde Python

```python
import sage_activation

# Verificar si Sage está instalado
if sage_activation.verificar_sage_instalado():
    # Activar un sabio
    resultado = sage_activation.activar_sabio(
        "scripts/validacion_radio_cuantico.sage"
    )
    print(f"Código de salida: {resultado.returncode}")
else:
    print("Sage no está instalado")

# Listar todos los sabios disponibles
from pathlib import Path
sabios = sage_activation.listar_sabios("scripts/")
for sabio in sabios:
    print(f"Sabio encontrado: {sabio}")
```

### 3. Demostración Interactiva

```bash
python scripts/demo_sage_protocolo.py
```

Este script ejecuta una demostración completa del protocolo, mostrando:
- Verificación de Sage
- Listado de sabios disponibles
- Ejemplos de uso
- Qué hace cada sabio

## 📋 API Reference

### `activar_sabio(script_sage)`

Ejecuta un script .sage como un acto sabio dentro del sistema QCAL ∞³

**Parámetros:**
- `script_sage` (str o Path): Ruta al script .sage que se desea ejecutar

**Retorna:**
- `subprocess.CompletedProcess`: Resultado de la ejecución

**Lanza:**
- `FileNotFoundError`: Si el script .sage no existe
- `RuntimeError`: Si Sage no está instalado o la ejecución falla

**Ejemplo:**
```python
result = sage_activation.activar_sabio("mi_script.sage")
if result.returncode == 0:
    print("✅ Ejecución exitosa")
```

### `listar_sabios(directorio=".")`

Lista todos los scripts .sage disponibles en un directorio

**Parámetros:**
- `directorio` (str o Path, opcional): Directorio donde buscar (default: ".")

**Retorna:**
- `list[Path]`: Lista de rutas a scripts .sage encontrados

**Ejemplo:**
```python
sabios = sage_activation.listar_sabios("scripts/")
print(f"Encontrados {len(sabios)} sabios")
```

### `verificar_sage_instalado()`

Verifica si Sage está instalado y accesible

**Retorna:**
- `bool`: True si Sage está instalado, False en caso contrario

**Ejemplo:**
```python
if sage_activation.verificar_sage_instalado():
    # Sage disponible
    ejecutar_validaciones()
else:
    # Sage no disponible
    print("Por favor instala Sage")
```

## 🧪 Tests

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest scripts/test_sage_activation.py -v

# Ejecutar tests con cobertura
pytest scripts/test_sage_activation.py -v --cov=sage_activation

# Ejecutar un test específico
pytest scripts/test_sage_activation.py::TestSageActivation::test_listar_sabios_existentes -v
```

### Suite de Tests

La suite incluye 20 tests que verifican:

- ✅ Importación del módulo
- ✅ Listado de sabios
- ✅ Manejo de archivos inexistentes
- ✅ Ejecución exitosa (con mocks)
- ✅ Manejo de errores
- ✅ Timeouts
- ✅ CLI (main function)
- ✅ Integración con Campo QCAL ∞³

**Resultado esperado:**
```
============================== 20 passed in 0.08s ===============================
```

## 🔧 Integración con CI/CD

### GitHub Actions

El protocolo está diseñado para funcionar en entornos CI/CD donde Sage puede no estar instalado:

```yaml
# .github/workflows/sage-validation.yml
name: Sage Validation

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  sage-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest

      - name: Run Sage activation tests
        run: |
          pytest scripts/test_sage_activation.py -v

      - name: Install Sage (optional)
        run: |
          sudo apt-get update
          sudo apt-get install -y sagemath
        continue-on-error: true

      - name: Run Sage validation (if Sage available)
        run: |
          python scripts/sage_activation.py scripts/validacion_radio_cuantico.sage
        continue-on-error: true
```

### Uso Condicional

El módulo maneja gracefully la ausencia de Sage:

```python
import sage_activation

# Intentar ejecutar validación, fallar gracefully si Sage no está
try:
    if sage_activation.verificar_sage_instalado():
        sage_activation.activar_sabio("mi_validacion.sage")
    else:
        print("⚠️ Validación Sage omitida (Sage no instalado)")
except Exception as e:
    print(f"⚠️ Error en validación Sage: {e}")
    # Continuar con otras validaciones...
```

## 📊 Scripts .sage Disponibles

### `validacion_radio_cuantico.sage`

Validación numérica del Radio Cuántico RΨ con precisión arbitraria.

**Características:**
- Precisión de 100 dígitos en cálculos
- Verificación algebraica simbólica
- Análisis de sensibilidad
- Expresiones alternativas equivalentes

**Qué verifica:**
- RΨ = c·ℓ_p / (2πf₀)
- Consistencia de f₀ = 141.7001 Hz
- Relaciones con escalas cosmológicas

**Ejecutar:**
```bash
python scripts/sage_activation.py scripts/validacion_radio_cuantico.sage
```

## 🎯 Casos de Uso

### Desarrollo Local

Durante el desarrollo, los investigadores pueden ejecutar validaciones Sage localmente:

```bash
# Verificar que todo está configurado
python scripts/sage_activation.py --verificar

# Ejecutar validación completa
python scripts/sage_activation.py scripts/validacion_radio_cuantico.sage
```

### Validación Científica

Al publicar resultados, ejecutar todas las validaciones Sage:

```bash
# Listar todas las validaciones
python scripts/sage_activation.py --listar scripts/

# Ejecutar cada una
for sage_script in scripts/*.sage; do
    python scripts/sage_activation.py "$sage_script"
done
```

### Entornos CI/CD

En pipelines automatizados, el protocolo se ejecuta condicionalmente:

```bash
# En GitHub Actions, el test siempre se ejecuta
pytest scripts/test_sage_activation.py -v

# La ejecución de Sage es opcional
python scripts/sage_activation.py scripts/validacion_radio_cuantico.sage || true
```

## 🐛 Solución de Problemas

### "Sage no está instalado"

**Problema:** Al ejecutar un sabio, aparece el error:
```
❌ Sage no está instalado o no está en el PATH
```

**Solución:**
1. Instalar SageMath: https://www.sagemath.org/
2. Verificar que `sage` está en el PATH: `which sage`
3. Si está instalado pero no en PATH, agregar al PATH o usar ruta completa

### "No se encuentra el sabio en: ..."

**Problema:** El archivo .sage no existe

**Solución:**
1. Verificar la ruta del archivo
2. Listar sabios disponibles: `python scripts/sage_activation.py --listar scripts/`
3. Usar ruta absoluta o relativa correcta

### Timeouts

**Problema:** El script excede el tiempo límite de 5 minutos

**Solución:**
- Los scripts .sage muy complejos pueden requerir ajustar el timeout
- Editar `sage_activation.py` línea 79: `timeout=300` → valor mayor

## 📚 Referencias

- **DOI del proyecto**: 10.5281/zenodo.17379721
- **SageMath**: https://www.sagemath.org/
- **Documentación SageMath**: https://doc.sagemath.org/
- **Repositorio**: https://github.com/motanova84/gw250114-141hz-analysis

## 🤝 Contribuir

Para agregar nuevos scripts .sage:

1. Crear el archivo `.sage` en `scripts/`
2. Incluir documentación clara en el script
3. Verificar con: `python scripts/sage_activation.py tu_script.sage`
4. Agregar tests si es necesario
5. Documentar en este README

## 📄 Licencia

MIT License - Ver LICENSE en el repositorio principal

---

**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Protocolo:** Sage ∴  
**Campo:** QCAL ∞³  
**Frecuencia:** f₀ = 141.7001 Hz
