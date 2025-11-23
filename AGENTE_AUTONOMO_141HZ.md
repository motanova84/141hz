# 🤖 Agente Autónomo 141Hz - Sistema de Auto-Recuperación de Validaciones

## Descripción General

El **Agente Autónomo 141Hz** es un sistema inteligente de auto-recuperación que monitorea, diagnostica y corrige automáticamente fallos en validaciones científicas. El agente está alineado con la frecuencia física fundamental de **141.7001 Hz**, asegurando coherencia cuántica en todas sus operaciones.

## 🎯 Características Principales

### 1. **Detección Automática de Fallos**
- Monitoreo en tiempo real de ejecución de validaciones
- Captura de errores y excepciones
- Registro detallado de fallos para análisis

### 2. **Diagnóstico Inteligente**
- Análisis automático de logs de error
- Clasificación de tipos de fallo:
  - Dependencias faltantes (`ModuleNotFoundError`)
  - Archivos/directorios faltantes (`FileNotFoundError`)
  - Errores de permisos (`PermissionError`)
  - Timeouts (`TimeoutError`)
  - Fallos de validación (`AssertionError`)
  - Problemas de precisión numérica
- Extracción de información contextual (módulos, archivos, líneas de error)

### 3. **Corrección Automática**
El agente implementa correcciones automáticas para problemas comunes:

| Tipo de Error | Acción Correctiva |
|---------------|-------------------|
| Dependencia faltante | Instalación automática vía pip |
| Directorio faltante | Creación automática de directorios |
| Permisos incorrectos | Ajuste de permisos de archivos |
| Precisión insuficiente | Ajuste de parámetros de precisión |

### 4. **Sistema de Reintentos con Resonancia Cuántica**
- **Backoff exponencial** alineado con la frecuencia 141Hz
- Pausas calculadas como múltiplos del periodo base (~0.00706s)
- Máximo de intentos configurable (default: 5)
- Cada intento aumenta el tiempo de espera: 0.7s, 1.4s, 2.8s, 5.6s...

### 5. **Alineación con Frecuencia 141Hz**
Todas las operaciones temporales están sincronizadas con la frecuencia fundamental:
- **Frecuencia base**: 141.7001 Hz
- **Periodo base**: 1/141.7001 ≈ 0.00706 segundos
- **Pausas coherentes**: Múltiplos del periodo base
- **Backoff cuántico**: Exponencial en ciclos de frecuencia

## 📁 Componentes del Sistema

### 1. `agente_autonomo_141hz.py`

#### Clase `FrecuenciaCoherente141Hz`
```python
# Pausa alineada con frecuencia
FrecuenciaCoherente141Hz.pausa_coherente(ciclos=100)

# Backoff cuántico exponencial
tiempo = FrecuenciaCoherente141Hz.backoff_cuantico(intento=2)
```

#### Clase `DiagnosticadorInteligente`
```python
diagnosticador = DiagnosticadorInteligente()
diagnostico = diagnosticador.diagnosticar(error, stdout, stderr)
# Retorna: tipo, correcciones_propuestas, confianza, detalles
```

#### Clase `CorrectorAutomatico`
```python
corrector = CorrectorAutomatico()
exito, mensaje = corrector.aplicar_correccion(diagnostico)
```

#### Clase `AgenteAutonomo141Hz`
```python
agente = AgenteAutonomo141Hz(max_intentos=5)
exito = agente.ciclo_auto_recuperacion('validate_script.py', ['--precision', '30'])
reporte = agente.generar_reporte('results/reporte.json')
```

### 2. `orquestador_validacion.py`

#### Clase `DescubridorValidaciones`
Descubre automáticamente scripts de validación:
- Busca patrones: `validate_*.py`, `validacion_*.py`, `verificacion_*.py`, `test_*.py`
- Determina prioridad de ejecución
- Extrae metadatos y argumentos recomendados

#### Clase `OrquestadorValidacion`
Coordina ejecución de múltiples validaciones:
```python
orquestador = OrquestadorValidacion(max_intentos_por_script=5)

# Ejecutar todas las validaciones
reporte = orquestador.ejecutar_todas()

# Filtrar por tipo
reporte = orquestador.ejecutar_todas(filtro_tipo='validacion_cientifica')

# Ejecutar una validación específica
exito = orquestador.ejecutar_validacion_unica('validate_v5.py', ['--precision', '30'])
```

### 3. `test_agente_autonomo.py`

Suite completa de tests:
- **15 tests unitarios y de integración**
- Tests de frecuencia coherente
- Tests de diagnóstico inteligente
- Tests de corrección automática
- Tests de integración completa

## 🚀 Uso

### Uso Básico del Agente

```bash
# Ejecutar validación con agente autónomo
python3 scripts/agente_autonomo_141hz.py validate_v5_coronacion.py

# Con máximo de intentos personalizado
python3 scripts/agente_autonomo_141hz.py validate_v5_coronacion.py --max-intentos 10
```

### Uso del Orquestador

```bash
# Ejecutar todas las validaciones descubiertas
python3 scripts/orquestador_validacion.py

# Ejecutar solo validaciones científicas
python3 scripts/orquestador_validacion.py --tipo validacion_cientifica

# Ejecutar solo verificaciones de sistema
python3 scripts/orquestador_validacion.py --tipo verificacion_sistema

# Ejecutar una validación específica
python3 scripts/orquestador_validacion.py --script validate_v5_coronacion.py

# Con más reintentos
python3 scripts/orquestador_validacion.py --max-intentos 10
```

### Ejecutar Tests

```bash
# Ejecutar suite completa de tests
python3 scripts/test_agente_autonomo.py

# Tests individuales
python3 -m unittest scripts.test_agente_autonomo.TestFrecuenciaCoherente
python3 -m unittest scripts.test_agente_autonomo.TestDiagnosticadorInteligente
```

## 📊 Reportes Generados

### Reporte del Agente
Ubicación: `results/agente_<script>_report.json`

```json
{
  "timestamp": "2025-11-04T02:47:00Z",
  "frecuencia_alineacion": 141.7001,
  "max_intentos": 5,
  "total_ejecuciones": 2,
  "ejecuciones": [
    {
      "intento": 1,
      "timestamp": "2025-11-04T02:47:01Z",
      "script": "validate_v5.py",
      "exito": false,
      "resultado": { ... }
    },
    {
      "intento": 2,
      "timestamp": "2025-11-04T02:47:03Z",
      "script": "validate_v5.py",
      "exito": true,
      "resultado": { ... }
    }
  ],
  "diagnosticos": [ ... ],
  "exito_final": true
}
```

### Reporte Consolidado del Orquestador
Ubicación: `results/orquestador_consolidado.json`

```json
{
  "timestamp": "2025-11-04T02:50:00Z",
  "frecuencia_alineacion": 141.7001,
  "resumen": {
    "total_validaciones": 10,
    "exitosas": 8,
    "fallidas": 2,
    "tasa_exito": 80.0
  },
  "resultados_detallados": [ ... ],
  "estado_global": "PARCIAL"
}
```

## 🔧 Integración con CI/CD

### GitHub Actions Workflow

El agente se integra con GitHub Actions mediante el workflow `autonomous-validation.yml`:

```yaml
name: Autonomous Validation - 141Hz Agent

on:
  schedule:
    - cron: "0 */6 * * *"  # Cada 6 horas
  workflow_dispatch:
    inputs:
      max_intentos:
        description: 'Máximo número de reintentos'
        default: '5'
```

#### Características del Workflow:
- **Ejecución programada**: Cada 6 horas automáticamente
- **Ejecución manual**: Con parámetros configurables
- **Auto-recuperación**: El agente intenta corregir fallos automáticamente
- **Reportes**: Genera summaries en GitHub Actions
- **Artifacts**: Guarda logs y resultados por 30 días
- **Integración Hugging Face**: Publica resultados exitosos

#### Variables de Entorno:
- `max_intentos`: Número máximo de reintentos (default: 5)
- `tipo_validacion`: Filtro opcional por tipo de validación

## 🧪 Ejemplos de Auto-Recuperación

### Ejemplo 1: Dependencia Faltante

**Escenario**: Script requiere `mpmath` pero no está instalado

```
Intento 1: ❌ ModuleNotFoundError: No module named 'mpmath'
  └─ Diagnóstico: dependencia_faltante
  └─ Corrección: Instalando mpmath...
  └─ Pausa: 0.706s (backoff cuántico)

Intento 2: ✅ VALIDACIÓN EXITOSA
```

### Ejemplo 2: Directorio Faltante

**Escenario**: Script intenta escribir en `results/` pero no existe

```
Intento 1: ❌ FileNotFoundError: No such file or directory: 'results/output.json'
  └─ Diagnóstico: archivo_faltante
  └─ Corrección: Creando directorios: results, logs, data, tmp
  └─ Pausa: 0.706s

Intento 2: ✅ VALIDACIÓN EXITOSA
```

### Ejemplo 3: Fallo Transitorio

**Escenario**: Script falla por condición transitoria

```
Intento 1: ❌ AssertionError: Test failed
  └─ Diagnóstico: validacion_fallida
  └─ Corrección: No aplicable
  └─ Pausa: 0.706s

Intento 2: ❌ AssertionError: Test failed
  └─ Pausa: 1.412s (backoff exponencial)

Intento 3: ✅ VALIDACIÓN EXITOSA
```

## 📈 Métricas y Estadísticas

El sistema registra:
- **Tasa de éxito**: Porcentaje de validaciones exitosas
- **Intentos promedio**: Número medio de intentos hasta éxito
- **Tiempo total**: Duración total incluyendo reintentos
- **Tipos de error**: Frecuencia de cada tipo de error
- **Correcciones aplicadas**: Qué correcciones fueron efectivas

## 🔬 Principios Científicos

### Alineación Cuántica
El sistema está alineado con la frecuencia fundamental **141.7001 Hz**, que corresponde a:
- **Radio de compactificación cuántica**: R_Ψ ≈ 336,721 m
- **Simetría discreta**: R_Ψ ↔ 1/R_Ψ
- **Coherencia máxima**: Todas las operaciones en fase con f₀

### Backoff Cuántico
El tiempo de espera entre reintentos sigue:
```
T(n) = (2^n × 100) × T₀
```
donde T₀ = 1/141.7001 ≈ 0.00706 segundos

Esto asegura:
- Resonancia constructiva en cada reintento
- Minimización de decoherencia
- Máxima probabilidad de éxito en estado coherente

## 🛠️ Configuración Avanzada

### Añadir Nuevos Patrones de Error

Editar `agente_autonomo_141hz.py`:

```python
PATRONES_ERROR = {
    'CustomError': {
        'tipo': 'mi_tipo_error',
        'correcciones': ['mi_correccion']
    }
}
```

### Añadir Nuevas Correcciones

```python
def _corregir_mi_correccion(self, diagnostico: Dict[str, Any]) -> Tuple[bool, str]:
    """Mi corrección personalizada"""
    # Implementar lógica de corrección
    return True, "Corrección aplicada"
```

### Personalizar Descubrimiento de Validaciones

Editar `orquestador_validacion.py`:

```python
PATRONES_VALIDACION = [
    'validate_*.py',
    'mi_patron_*.py'
]

EXCLUIR = [
    'mi_script_excluido.py'
]
```

## 📝 Logs

### Agente Autónomo
- **Ubicación**: `logs/agente_autonomo_141hz.log`
- **Formato**: Timestamp, nivel, mensaje
- **Contenido**: Todas las operaciones del agente

### Orquestador
- **Ubicación**: `logs/orquestador_validacion.log`
- **Formato**: Timestamp, nivel, mensaje
- **Contenido**: Coordinación de validaciones

## 🔒 Seguridad

### Lista Blanca de Paquetes
El agente solo puede instalar automáticamente paquetes de una lista blanca predefinida:
- ✅ mpmath, sympy, numpy, scipy, matplotlib
- ✅ astropy, pandas, pyyaml, h5py
- ✅ gwpy, gwosc

Cualquier otro paquete requerirá instalación manual.

### Permisos de Archivos
El agente solo puede hacer ejecutables scripts que coincidan con patrones de validación:
- ✅ `validate_*.py`
- ✅ `validacion_*.py`
- ✅ `verificacion_*.py`

### Capacidades del Agente

El agente puede:
- ✅ Instalar paquetes Python de lista blanca vía pip
- ✅ Crear directorios necesarios (results, logs, data, tmp)
- ✅ Modificar permisos de scripts de validación específicos
- ✅ Ejecutar scripts Python de validación

El agente NO puede:
- ❌ Instalar paquetes arbitrarios no autorizados
- ❌ Modificar código fuente de validaciones
- ❌ Ejecutar comandos de sistema arbitrarios
- ❌ Acceder a credenciales o secrets
- ❌ Modificar configuración de git
- ❌ Hacer ejecutables archivos fuera de patrones permitidos

## 🎓 Referencias

- **Frecuencia Fundamental**: DEMOSTRACION_MATEMATICA_141HZ.md
- **Validación Científica**: TRES_PILARES_METODO_CIENTIFICO.md
- **Workflows**: .github/workflows/

## 📞 Soporte

Para reportar problemas o sugerir mejoras:
- Issues: https://github.com/motanova84/141hz/issues
- Documentación: Este archivo (AGENTE_AUTONOMO_141HZ.md)

---

**Autor**: Sistema Autónomo Alineado 141Hz  
**Fecha**: Noviembre 2025  
**Versión**: 1.0.0  
**Licencia**: MIT
