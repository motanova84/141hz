# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto 141Hz / QC-LLM! Este documento describe cómo contribuir efectivamente al proyecto.

## Requisitos Básicos

- **Python**: 3.10+ (recomendado 3.11 o 3.12)
- **Instalación de desarrollo**: `pip install -e ".[dev]"`
- **Tests**: `pytest -q`
- **Estilo**: PEP8, type hints opcional
- **DCO**: Developer Certificate of Origin en commits

## 🌊 Contribuciones QC-LLM (Quantum Coherence for LLMs)

El proyecto incluye un componente de **estándar de coherencia cuántica para modelos de lenguaje** (QC-LLM). Si trabajas en esta área:

### Áreas de Contribución QC-LLM

1. **Algoritmo de Coherencia**
   - Mejoras al algoritmo BERT+FFT en `API/Python/qc_llm/metrics.py`
   - Optimizaciones de performance
   - Nuevos métodos de análisis espectral
   - **Requisito**: Tests deben pasar con `pytest Tests/test_frequency_validator.py`

2. **Integraciones LLM**
   - Conectores para GPT-4, Claude, Gemini, Llama
   - APIs de validación en tiempo real
   - Benchmarks comparativos
   - **Ubicación**: `Examples/LLM_Integration/`

3. **Documentación Matemática**
   - Expansión de derivaciones en `Documentation/Theory/`
   - Conexiones con física y neurociencia
   - Tutoriales interactivos en Jupyter
   - **Estándar**: Rigor matemático con referencias

4. **Tests y Validación**
   - Tests unitarios adicionales
   - Casos de prueba con LLMs reales
   - Benchmarks de performance
   - **Cobertura**: Objetivo >90% en código QC-LLM

### Estructura QC-LLM

```
API/Python/qc_llm/         # Biblioteca principal
├── __init__.py            # API pública
├── metrics.py             # Compute coherence (BERT+FFT)
└── validator.py           # Clase CoherenceValidator

Tests/                     # Tests unitarios
└── test_frequency_validator.py  # 20+ tests

Documentation/Theory/      # Teoría matemática
└── mathematical_foundation.md   # Derivación f₀ = 141.7001 Hz

Examples/Research/         # Tutoriales
└── qc_llm_tutorial.ipynb  # Tutorial interactivo
```

### Ejecutar Tests QC-LLM

```bash
# Tests básicos (sin BERT)
pytest Tests/test_frequency_validator.py -k "not bert" -v

# Tests completos (requiere transformers)
pip install transformers>=4.48.0 torch>=2.6.0
pytest Tests/test_frequency_validator.py -v

# Test específico
pytest Tests/test_frequency_validator.py::TestComputeCoherence::test_coherence_bounds -v
```

### Pre-commit Hooks

Este proyecto usa pre-commit para calidad de código:

```bash
# Instalar pre-commit
pip install pre-commit
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files

# Actualizar hooks
pre-commit autoupdate
```

Los hooks incluyen:
- **Black**: Formateo de código Python
- **Flake8**: Linting (errores críticos)
- **isort**: Ordenar imports
- **Security checks**: Bandit para vulnerabilidades
- **Scientific checks**: Validar constante F0 no modificada

### Estándares de Código QC-LLM

```python
def compute_coherence(text: str, use_bert: bool = True) -> dict:
    """
    Compute quantum coherence using BERT+FFT.
    
    Args:
        text: Input text to analyze
        use_bert: Use BERT embeddings (requires transformers)
    
    Returns:
        Dictionary with:
        - coherence: float [0, 1]
        - frequency_alignment: float [0, 1]
        - quantum_metric: float [0, 1]
        - recommendation: str
        
    Raises:
        ValueError: If text is empty
        
    Example:
        >>> result = compute_coherence("Quantum coherence is fascinating")
        >>> print(f"Coherence: {result['coherence']:.2%}")
        Coherence: 87.3%
    """
    # Implementación...
```

**Requisitos**:
- Type hints obligatorios
- Docstrings con Args, Returns, Raises, Example
- Valores de retorno en [0, 1] para métricas
- Manejo de errores graceful

## 🤖 Colaboradores Automatizados

Este proyecto cuenta con **8 bots inteligentes** que te ayudarán durante el proceso de contribución:

- 🏷️ **Auto-Labeler**: Etiqueta tu PR automáticamente
- 👀 **PR Review Bot**: Asigna revisores y envía recordatorios
- 📋 **Issue Management**: Te guía para proporcionar información completa
- 📚 **Documentation Bot**: Mantiene documentación actualizada
- 🔒 **Dependabot**: Mantiene dependencias actualizadas
- 🏥 **Dependency Health**: Monitorea seguridad
- 🧠 **Workflow Intelligence**: Optimiza CI/CD
- 🔄 **Coherence Viz**: Actualiza visualizaciones

📖 **Ver detalles completos**: [AUTOMATED_COLLABORATORS.md](AUTOMATED_COLLABORATORS.md)

## 🚀 CI/CD y Calidad de Código

Este proyecto utiliza **CI/CD automatizado real** para garantizar la calidad y reproducibilidad:

### Pipeline Automático

Cada push o pull request ejecuta automáticamente:

1. **Unit Tests** - Suite completa de tests (9 archivos, >50 casos)
2. **Code Quality** - Validación de sintaxis y estilo con flake8
3. **Scientific Analysis** - Validación con datos GWOSC (cuando disponibles)
4. **Auto-Labeling** - Etiquetado inteligente de PRs
5. **Review Assignment** - Asignación automática de revisores

Ver estado actual: [![CI/CD](https://github.com/motanova84/gw250114-141hz-analysis/actions/workflows/analyze.yml/badge.svg)](https://github.com/motanova84/gw250114-141hz-analysis/actions/workflows/analyze.yml)

### Requisitos de Calidad

Para que tu contribución sea aceptada, debe:

- ✅ **Pasar todos los tests** - `make test` o `python scripts/run_all_tests.py`
- ✅ **Sin errores críticos de lint** - `flake8 scripts/ --select=E9,F63,F7,F82`
- ✅ **Código documentado** - Docstrings en funciones públicas
- ✅ **Tests para nuevo código** - Añade tests para nuevas funcionalidades

💡 **Nota**: Los bots automatizados verificarán automáticamente muchos de estos requisitos.

## 📋 Proceso de Contribución

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/gw250114-141hz-analysis.git
cd gw250114-141hz-analysis
```

### 2. Configurar Entorno

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Crear Branch

```bash
# Crear branch descriptivo
git checkout -b feature/mi-mejora
# o
git checkout -b fix/mi-correccion
```

### 4. Desarrollo

```bash
# Hacer cambios
# Ejecutar tests frecuentemente
python scripts/run_all_tests.py

# Verificar calidad de código
flake8 scripts/ --select=E9,F63,F7,F82
```

### 5. Commit y Push

```bash
# Commit con mensaje descriptivo
git add .
git commit -m "feat: descripción clara de la mejora"

# Push a tu fork
git push origin feature/mi-mejora
```

### 6. Pull Request

- Abre un PR desde tu fork al repositorio principal
- Describe claramente los cambios
- Espera la revisión automática de CI/CD
- Responde a comentarios de revisión

## 🧪 Ejecutar Tests Localmente

### Suite Completa

```bash
# Ejecutar todos los tests
python scripts/run_all_tests.py

# O usando Make
make setup  # primera vez
python scripts/run_all_tests.py
```

### Tests Individuales

```bash
# Test de energía cuántica
python scripts/test_energia_cuantica.py

# Test de análisis bayesiano
python scripts/test_analisis_bayesiano_multievento.py

# Test de simetría discreta
python scripts/test_simetria_discreta.py
```

### Linting

```bash
# Errores críticos (sintaxis, nombres indefinidos)
flake8 scripts/ --select=E9,F63,F7,F82 --show-source

# Todas las advertencias
flake8 scripts/ --max-line-length=120
```

## 📝 Estándares de Código

### Python

- **Estilo**: PEP 8 (con líneas hasta 120 caracteres)
- **Docstrings**: Todas las funciones públicas
- **Type hints**: Preferidos para funciones principales
- **Tests**: unittest para tests científicos

### Ejemplo de Función

```python
def calcular_energia_cuantica(frecuencia: float) -> float:
    """
    Calcula la energía cuántica E = hf.
    
    Args:
        frecuencia: Frecuencia en Hz
        
    Returns:
        Energía en Joules
        
    Raises:
        ValueError: Si frecuencia es negativa
    """
    if frecuencia < 0:
        raise ValueError("Frecuencia debe ser positiva")
    
    h = 6.62607015e-34  # Constante de Planck (J·s)
    return h * frecuencia
```

### Tests

```python
import unittest

class TestEnergiaCuantica(unittest.TestCase):
    def test_energia_positiva(self):
        """Verificar que energía sea positiva"""
        E = calcular_energia_cuantica(141.7001)
        self.assertGreater(E, 0)
    
    def test_frecuencia_invalida(self):
        """Verificar que frecuencia negativa lance error"""
        with self.assertRaises(ValueError):
            calcular_energia_cuantica(-1)

if __name__ == '__main__':
    unittest.main()
```

## 🔬 Tipos de Contribuciones

### Muy Bienvenidas

- ✅ **Correcciones de bugs** en análisis o cálculos
- ✅ **Nuevos tests** para aumentar cobertura
- ✅ **Mejoras de documentación** técnica
- ✅ **Optimizaciones** de rendimiento con pruebas
- ✅ **Nuevos análisis** basados en framework existente

### Requieren Discusión Previa

- ⚠️ **Cambios en teoría fundamental** (abrir issue primero)
- ⚠️ **Refactorizaciones grandes** (discutir arquitectura)
- ⚠️ **Nuevas dependencias** (justificar necesidad)

### No Aceptadas

- ❌ **Cambios que rompen reproducibilidad** sin justificación
- ❌ **Código sin tests** para funcionalidad crítica
- ❌ **Violaciones de estándares científicos** (GWOSC, LIGO)

## 🔄 Reproducibilidad de Resultados

### Flujo Completo de Reproducción

Para reproducir completamente los resultados del proyecto:

#### 1. Análisis con Datos Reales (GWOSC)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Descargar datos de GWOSC para GW150914
python scripts/descargar_datos.py --event GW150914 --detector H1 --duration 32

# Ejecutar análisis principal
python scripts/analizar_ringdown.py --frequency 141.7

# Verificar resultados
python scripts/validar_v5_coronacion.py
```

#### 2. Análisis con Datos Sintéticos (Testing)

```bash
# Generar datos sintéticos con señal en 141.7 Hz
python scripts/generar_datos_prueba.py

# Ejecutar análisis
python scripts/analizar_ringdown.py

# Los resultados deben mostrar:
# - Pico espectral cerca de 141.7 Hz
# - SNR > 2.0 para la señal inyectada
# - Gráficos en results/figures/
```

#### 3. Validación Científica Completa

```bash
# Ejecutar suite completa de validaciones
python run_all_validations.py

# O validaciones individuales:
python scripts/test_energia_cuantica.py
python scripts/test_simetria_discreta.py
python scripts/analisis_bayesiano_multievento.py
```

### Verificación de Resultados

#### Criterios de Éxito

Un análisis exitoso debe cumplir:

1. **Frecuencia Detectada**: 141.7 ± 0.1 Hz
2. **SNR Mínimo**: > 2.0 (datos sintéticos), > 1.5 (datos reales)
3. **Consistencia Energética**: E = hf con precisión 10^-10
4. **Validación Bayesiana**: Factor de Bayes > 3.0

#### Comparación de Resultados

```bash
# Ver resultados de referencia
cat results/reference/gw150914_141hz_baseline.json

# Comparar con tus resultados
python scripts/compare_results.py \
    --reference results/reference/gw150914_141hz_baseline.json \
    --current results/figures/analysis_results.json
```

### Solución de Problemas Comunes

#### Problema: "No se encontraron datos"

```bash
# Verificar que data/raw/ existe
ls -la data/raw/

# Si está vacío, generar datos de prueba
python scripts/generar_datos_prueba.py
```

#### Problema: "ImportError: No module named 'gwpy'"

```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt

# Verificar instalación
python -c "import gwpy; print(gwpy.__version__)"
```

#### Problema: "RuntimeError: FFT computation failed"

```bash
# Verificar tamaño de datos
python -c "import h5py; f=h5py.File('data/raw/H1-GW150914-32s.hdf5'); print(f['strain/Strain'].shape)"

# Debe ser múltiplo de 2 para FFT eficiente
# Regenerar datos si necesario
```

#### Problema: Resultados no coinciden

```bash
# Verificar versiones de dependencias críticas
pip list | grep -E "(numpy|scipy|gwpy|matplotlib)"

# Versiones recomendadas:
# numpy>=1.21.0
# scipy>=1.7.0
# gwpy>=3.0.0
```

### Variables de Entorno Opcionales

```bash
# Para análisis de alta precisión
export PRECISION_MODE=high  # Usa mpmath con 100 dígitos

# Para debugging detallado
export DEBUG_ANALYSIS=1

# Para deshabilitar plots (CI/CD)
export HEADLESS_MODE=1
```

## 📊 Estructura del Proyecto

```
scripts/
├── test_*.py           # Tests unitarios (ejecutados por CI/CD)
├── analizar_*.py       # Scripts de análisis principal
├── validar_*.py        # Scripts de validación
├── generar_*.py        # Generadores de datos sintéticos
├── benchmark_*.py      # Scripts de benchmarking
└── run_all_tests.py    # Runner de tests (usado por CI/CD)

tests/
├── test_*.py           # Tests científicos con unittest
└── fixtures/           # Datos de referencia para tests

data/
├── raw/                # Datos descargados de GWOSC (no en git)
├── synthetic/          # Datos sintéticos generados (no en git)
└── reference/          # Datos de referencia para validación

results/
├── figures/            # Gráficos generados (no en git)
├── benchmark/          # Resultados de benchmarks
└── reference/          # Resultados de referencia (en git)

notebooks/
├── *.ipynb             # Notebooks reproducibles
└── validation_quick.ipynb  # Validación rápida

.github/
└── workflows/
    ├── analyze.yml     # Pipeline CI/CD (tests, lint, análisis)
    └── production-qcal.yml  # Pipeline de producción
```

## 🧬 Datos Sintéticos y Simulados

### Uso de Datos Sintéticos para Testing

Los datos sintéticos son esenciales para:
- ✅ Testing rápido sin descargar datos de GWOSC
- ✅ Validar algoritmos con señales conocidas
- ✅ Pruebas de regresión en CI/CD
- ✅ Desarrollo sin conexión a internet

### Tipos de Datos Sintéticos Disponibles

#### 1. Señal Simple en 141.7 Hz

```bash
# Generar señal simple con ruido gaussiano
python scripts/generar_datos_prueba.py

# Propiedades:
# - Frecuencia: 141.7 Hz exacta
# - SNR: ~2.0
# - Duración: 32 segundos
# - Sample rate: 4096 Hz
```

#### 2. Señal de Merger Completo

```bash
# Generar señal que simula merger + ringdown
python scripts/synthetic_datasets/generate_merger_signal.py \
    --mass1 36 --mass2 29 --frequency 141.7 --output data/synthetic/

# Propiedades:
# - Incluye inspiral, merger y ringdown
# - Parámetros ajustables (masas, spin, distancia)
# - Compatible con análisis PyCBC
```

#### 3. Señal Multi-Detector

```bash
# Generar señales para H1, L1, V1 con tiempos de llegada realistas
python scripts/synthetic_datasets/generate_multidetector.py \
    --detectors H1,L1,V1 --event-type BBH

# Útil para:
# - Tests de coherencia multi-detector
# - Validación de localización en el cielo
# - Tests de análisis bayesiano
```

#### 4. Dataset con Glitches

```bash
# Generar datos con artefactos instrumentales
python scripts/synthetic_datasets/generate_with_glitches.py

# Incluye:
# - Blip glitches
# - Scattered light
# - Variaciones de línea de potencia
# - Útil para testing de robustez
```

### Validación de Datos Sintéticos

```bash
# Verificar calidad de datos sintéticos
python scripts/validate_synthetic_data.py --input data/synthetic/

# Verifica:
# - Formato HDF5 correcto
# - Frecuencia de muestreo
# - PSD realista
# - Señal inyectada recuperable
```

### Documentación Completa de Datasets

Ver: **[docs/SYNTHETIC_DATASETS.md](docs/SYNTHETIC_DATASETS.md)** para:
- Descripción detallada de cada tipo de dataset
- Parámetros de generación
- Casos de uso recomendados
- Ejemplos de código

## 🏆 Benchmarking y Comparación

### Ejecutar Benchmarks

```bash
# Benchmark completo contra frameworks estándar
python scripts/benchmark_quantum_solvers.py --output results/benchmark/

# Benchmark de análisis GW contra PyCBC
python scripts/benchmark_gw_analysis.py --frameworks pycbc,gwpy

# Benchmark de precisión numérica
python scripts/benchmark_numerical_precision.py
```

### Frameworks Comparados

#### Quantum Computing
- **NumPy/SciPy** (baseline, nuestra implementación)
- **QuTiP** (estándar industria quantum optics)
- **OpenFermion** (framework de Google)

#### Gravitational Waves
- **GWPy** (nuestra base)
- **PyCBC** (estándar LIGO para búsqueda)
- **LALSuite** (librería oficial LIGO)

### Métricas de Benchmark

#### Performance
- ⏱️ Tiempo de ejecución (segundos)
- 💾 Uso de memoria (MB)
- 🔄 Escalabilidad (O(N³) esperado)

#### Precisión
- 🎯 Accuracy numérica (10^-10 objetivo)
- 📊 Error relativo vs. solución analítica
- ✓ Tests de regresión contra resultados publicados

#### Reproducibilidad
- 🔁 Varianza entre ejecuciones
- 🖥️ Consistencia cross-platform
- 📌 Determinismo con seeds fijos

### Interpretar Resultados de Benchmark

```bash
# Ver resultados previos de referencia
cat results/benchmark/reference_results.json

# Comparar con tu ejecución
python scripts/compare_benchmark_results.py \
    --current results/benchmark/benchmark_results.json \
    --reference results/benchmark/reference_results.json

# Output esperado:
# ✅ Performance: Within 10% of reference
# ✅ Accuracy: Matches to 10^-10
# ✅ Scaling: O(N^3.02) ≈ O(N^3)
```

### Añadir Nuevos Benchmarks

Para contribuir con nuevos benchmarks:

1. **Crear script de benchmark**:
   ```python
   # scripts/benchmark_mi_feature.py
   def benchmark_mi_algoritmo(N, num_trials=10):
       # Implementar benchmark
       return resultados
   ```

2. **Añadir tests**:
   ```python
   # tests/test_benchmark_mi_feature.py
   def test_benchmark_regression():
       # Verificar que performance no degrada
       pass
   ```

3. **Documentar en BENCHMARKING.md**:
   - Metodología
   - Frameworks comparados
   - Interpretación de resultados

4. **Actualizar CI/CD** (opcional):
   ```yaml
   # .github/workflows/benchmarks.yml
   - name: Run new benchmark
     run: python scripts/benchmark_mi_feature.py
   ```

### Certificación de Performance

Para que una contribución sea aceptada con cambios de performance:

- ✅ Debe incluir benchmark comparativo
- ✅ Performance no debe degradar > 10% sin justificación
- ✅ Precision numérica debe mantenerse (10^-10)
- ✅ Resultados deben ser reproducibles

## 🐛 Reportar Bugs

### Información a Incluir

1. **Descripción clara** del problema
2. **Pasos para reproducir**
3. **Comportamiento esperado** vs. observado
4. **Entorno**: Python version, OS, dependencias
5. **Logs/errores** completos

### Template de Issue

```markdown
## Descripción
[Descripción clara del problema]

## Pasos para Reproducir
1. Ejecutar `python scripts/...`
2. Observar error en...

## Comportamiento Esperado
[Qué debería suceder]

## Comportamiento Observado
[Qué sucede actualmente]

## Entorno
- Python: 3.9.x
- OS: Ubuntu 22.04
- GWPy: 3.0.13

## Logs
```
[Pegar logs aquí]
```
```

## ✨ Sugerir Mejoras

Abre un issue con:

1. **Motivación**: ¿Por qué es útil?
2. **Propuesta**: ¿Qué cambiarías?
3. **Alternativas**: ¿Consideraste otras opciones?
4. **Impacto**: ¿Afecta reproducibilidad?

## 💰 Apoyo al Proyecto

[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-ff69b4)](https://github.com/sponsors/motanova84)

Tu apoyo ayuda a:
- Mantener análisis actualizado con GWTC-3, GWTC-4
- Desarrollar nuevas herramientas open source
- Mejorar documentación y tutoriales
- Infraestructura de CI/CD y tests

## 📧 Contacto

**José Manuel Mota Burruezo**  
📧 institutoconsciencia@proton.me  
🐙 GitHub: [@motanova84](https://github.com/motanova84)

## 📜 Licencia

Al contribuir, aceptas que tu código se distribuya bajo la misma licencia MIT del proyecto.

---

**¡Gracias por hacer que la ciencia sea más abierta y reproducible! 🌌✨**
