# Refactorización: Modularidad, Gestión de Dependencias y Manejo de Excepciones

## Resumen

Esta refactorización mejora significativamente la estructura del código del proyecto GW 141.7001 Hz, implementando:

1. **Gestión moderna de dependencias** con Poetry
2. **Arquitectura modular** con separación clara de responsabilidades
3. **Manejo avanzado de excepciones** con clases personalizadas
4. **Utilidades reutilizables** con retry logic y logging estructurado
5. **Tests completos** para todos los nuevos módulos

## Cambios Principales

### 1. Gestión de Dependencias con Poetry

#### Archivo: `pyproject.toml`

Se ha creado una configuración completa de Poetry que incluye:

- **Dependencias de producción**: gwpy, numpy, scipy, matplotlib, etc.
- **Dependencias de desarrollo**: pytest, flake8, black, mypy
- **Configuración de herramientas**: pytest, black, isort, mypy, coverage
- **Metadata del proyecto**: nombre, versión, autor, licencia

**Ventajas**:
- Gestión determinística de dependencias
- Entorno virtual automático
- Separación clara entre dependencias de desarrollo y producción
- Configuración centralizada de herramientas

**Uso**:
```bash
# Instalar Poetry (si no está instalado)
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell

# Agregar nueva dependencia
poetry add <paquete>

# Agregar dependencia de desarrollo
poetry add --group dev <paquete>
```

### 2. Módulo de Excepciones Personalizadas

#### Archivo: `src/exceptions.py`

Se han creado 8 clases de excepciones especializadas:

1. **GW141HzException** (base): Excepción base con soporte para detalles contextuales
2. **DataDownloadError**: Errores de descarga de datos GWOSC
3. **DataNotFoundError**: Datos no encontrados
4. **ValidationError**: Fallos en validaciones científicas
5. **AnalysisError**: Errores durante análisis computacional
6. **ConfigurationError**: Configuración inválida o faltante
7. **PrecisionError**: Requisitos de precisión no cumplidos
8. **NetworkError**: Fallos de operaciones de red

**Características**:
- Mensajes de error contextuales y descriptivos
- Diccionario `details` con información adicional
- Soporte para causas originales de errores
- Representación string mejorada

**Ejemplo**:
```python
from src.exceptions import DataDownloadError, ValidationError

# Lanzar excepción con contexto
raise DataDownloadError(
    event_name="GW150914",
    detector="H1",
    message="GWOSC API timeout"
)

# Capturar y usar detalles
try:
    validate_data()
except ValidationError as e:
    print(f"Validation failed: {e}")
    print(f"Details: {e.details}")
```

### 3. Módulo de Utilidades

#### Archivo: `src/utils.py`

Utilidades reutilizables con manejo robusto de errores:

#### 3.1. Logging Estructurado

```python
from src.utils import setup_logging

logger = setup_logging(
    level=logging.INFO,
    log_file=Path("logs/analysis.log")
)

logger.info("Analysis started")
logger.error("Error occurred")
```

#### 3.2. Retry Logic con Exponential Backoff

```python
from src.utils import retry_with_backoff

@retry_with_backoff(
    max_attempts=3,
    initial_delay=2.0,
    backoff_factor=2.0
)
def download_gwosc_data(event_name):
    # Función que puede fallar
    return gwosc.get_event_data(event_name)

# Automáticamente reintenta con delays: 2s, 4s, 8s
data = download_gwosc_data("GW150914")
```

#### 3.3. Manejo Seguro de JSON

```python
from src.utils import safe_json_dump, safe_json_load

# Guardar con manejo de errores
results = {"f0": 141.7001, "status": "PASS"}
safe_json_dump(results, Path("results.json"), logger)

# Cargar con manejo de errores
data = safe_json_load(Path("results.json"), logger)
# Retorna None si falla, no lanza excepción
```

#### 3.4. Funciones de Formateo

```python
from src.utils import format_frequency, format_snr

freq_str = format_frequency(141.7001, precision=4)  # "141.7001 Hz"
snr_str = format_snr(21.38, precision=2)             # "21.38"
```

### 4. Validadores Modulares

#### Archivo: `src/validators.py`

Clases orientadas a objetos para validaciones científicas:

#### 4.1. QuantumFrequencyValidator

Valida la frecuencia cuántica fundamental f₀ = 141.7001 Hz:

```python
from src.validators import QuantumFrequencyValidator

validator = QuantumFrequencyValidator(precision=30)
result = validator.validate()

print(f"f₀ = {result['f0_hz']} Hz")
print(f"Status: {result['status']}")
```

#### 4.2. CompactificationRadiusValidator

Valida el radio de compactificación R_Ψ:

```python
from src.validators import CompactificationRadiusValidator

validator = CompactificationRadiusValidator(precision=30)
result = validator.validate()

print(f"R_Ψ = {result['R_psi_calculated']:.2f} m")
print(f"In range: {result['in_expected_range']}")
```

#### 4.3. DiscreteSymmetryValidator

Valida la simetría discreta R_Ψ ↔ 1/R_Ψ:

```python
from src.validators import DiscreteSymmetryValidator

validator = DiscreteSymmetryValidator(precision=30)
result = validator.validate()

print(f"Deviation: {result['deviation_from_unity']:.2e}")
```

#### 4.4. ValidationOrchestrator

Orquesta todas las validaciones:

```python
from src.validators import ValidationOrchestrator

orchestrator = ValidationOrchestrator(precision=30)
results = orchestrator.run_all()

print(f"Overall status: {results['overall_status']}")
print(f"Tests passed: {results['summary']['tests_passed']}/3")
```

### 5. Script Refactorizado

#### Archivo: `validate_v5_coronacion.py`

El script principal ha sido completamente refactorizado:

**Antes**:
- Funciones monolíticas
- Sin manejo de excepciones
- Sin logging estructurado
- Sin separación de responsabilidades

**Después**:
- Usa clases modulares de `src/validators.py`
- Manejo completo de excepciones con códigos de salida apropiados
- Logging estructurado con timestamps
- Separación clara entre lógica de validación y presentación
- Opción de archivo de log

**Nuevas opciones**:
```bash
# Uso básico
python3 validate_v5_coronacion.py --precision 30

# Con archivo de salida personalizado
python3 validate_v5_coronacion.py --precision 50 --output results/custom.json

# Con archivo de log
python3 validate_v5_coronacion.py --precision 30 --log-file logs/validation.log
```

**Códigos de salida**:
- `0`: Validación exitosa (PASS)
- `1`: Validación fallida (FAIL) o ValidationError
- `2`: Error de aplicación general
- `3`: Error de precisión inválida
- `130`: Interrupción por usuario (Ctrl+C)

### 6. Tests Completos

Se han creado tres archivos de tests con cobertura completa:

#### 6.1. `tests/test_exceptions.py`
- 13 tests para todas las clases de excepciones
- Verifica mensajes, contexto y atributos

#### 6.2. `tests/test_utils.py`
- 14 tests para funciones de utilidad
- Incluye tests de retry logic, JSON, logging y formateo

#### 6.3. `tests/test_validators.py`
- 16 tests para validadores
- Tests unitarios e integración end-to-end
- Verifica consistencia entre diferentes precisiones

**Ejecutar tests**:
```bash
# Todos los tests
pytest tests/

# Tests específicos
pytest tests/test_exceptions.py -v
pytest tests/test_utils.py -v
pytest tests/test_validators.py -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html
```

**Resultado**:
- ✅ 43 tests totales
- ✅ 100% passing
- ✅ Alta cobertura de código

## Beneficios de la Refactorización

### 1. Mantenibilidad
- Código más organizado y fácil de entender
- Separación clara de responsabilidades
- Funciones y clases con propósitos únicos

### 2. Extensibilidad
- Fácil agregar nuevos validadores
- Sistema de excepciones extensible
- Utilidades reutilizables en otros scripts

### 3. Robustez
- Manejo completo de errores
- Retry logic automático para operaciones de red
- Logging estructurado para debugging

### 4. Testabilidad
- 43 tests automatizados
- Cobertura completa de nuevos módulos
- Fácil agregar más tests

### 5. Profesionalismo
- Gestión moderna de dependencias
- Estándares de código (Black, isort, mypy)
- Documentación completa

## Próximos Pasos Recomendados

### Scripts para Refactorizar
1. `escuchar.py` - Aplicar mismo patrón modular
2. `experimental_detection_protocol.py` - Extraer clases reutilizables
3. `multi_event_analysis.py` - Agregar manejo de excepciones

### Mejoras Adicionales
1. Agregar type hints completos (mypy)
2. Configurar pre-commit hooks
3. Agregar CI/CD con tests automáticos
4. Documentación API con Sphinx

## Migración para Usuarios

### Código Antiguo
```python
# Antes
results = validate_quantum_frequency(precision=30)
if results['status'] != 'PASS':
    print("Error")
```

### Código Nuevo
```python
# Después
from src.validators import QuantumFrequencyValidator
from src.exceptions import ValidationError

try:
    validator = QuantumFrequencyValidator(precision=30)
    results = validator.validate()
    print(f"✓ Validation passed: {results['status']}")
except ValidationError as e:
    print(f"✗ Validation failed: {e}")
    print(f"Details: {e.details}")
```

## Referencias

- [Poetry Documentation](https://python-poetry.org/docs/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Exception Handling Best Practices](https://docs.python.org/3/tutorial/errors.html)
- [Exponential Backoff Pattern](https://en.wikipedia.org/wiki/Exponential_backoff)

## Conclusión

Esta refactorización establece una base sólida para el desarrollo futuro del proyecto, mejorando significativamente la calidad del código, la mantenibilidad y la robustez del sistema de análisis de ondas gravitacionales.
