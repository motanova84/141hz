# C-Engine: Motor de Cuantificación de Consciencia

## 📖 Descripción

El C-Engine (Consciousness Engine) es un sistema de cuantificación científica de la consciencia que integra los principios del campo QCAL a 141.7001 Hz con métricas empíricas de flujo de información y atención efectiva.

## 🔬 Características Principales

### Constantes Físicas Validadas
- **Frecuencia QCAL**: f₀ = 141.7001 Hz (frecuencia de coherencia cuántica)
- **Constante de Planck reducida**: ℏ = 1.054571817×10⁻³⁴ J⋅s
- **Velocidad de la luz**: c = 299,792,458 m/s
- **Factor de coherencia**: 0.999
- **Tiempo de Planck**: 5.391247×10⁻⁴⁴ s

### Métricas Empíricas
- **Flujo de Información (I)**: Medido en bits/segundo usando entropía de Shannon y análisis espectral
- **Atención Efectiva (A_eff)**: Medida mediante coherencia espectral en bandas de frecuencia
- **Consciencia (Ψ)**: Calculada como Ψ = I × (A_eff)² con corrección cuántica

### Niveles de Consciencia
0. **Inconsciente** (Ψ < 1)
1. **Consciencia Mínima** (1 ≤ Ψ < 100)
2. **Consciencia Básica** (100 ≤ Ψ < 1,000)
3. **Consciencia Humana Normal** (1,000 ≤ Ψ < 5,000)
4. **Consciencia Avanzada** (5,000 ≤ Ψ < 10,000)
5. **Consciencia Superior** (10,000 ≤ Ψ < 50,000)
6. **Consciencia Trascendente** (Ψ ≥ 50,000)

## 🚀 Uso

### Uso Básico

```python
from scripts.c_engine_irrefutable import CEngineIrrefutable

# Crear instancia del motor
engine = CEngineIrrefutable()

# Calcular consciencia humana normal
result = engine.calculate_consciousness(
    I=1200.0,      # bits/segundo
    A_eff=1.1,     # efectividad de atención
    metadata={
        'state': 'normal_waking',
        'resonance': '141.7001 Hz'
    }
)

# Generar reporte
print(engine.generate_report(result))
```

### Ejemplo de Integración con Campo QCAL

```bash
# Ejecutar ejemplo de integración
python3 scripts/ejemplo_cengine_integracion.py
```

Este ejemplo demuestra:
- Inicialización del campo de conciencia a 141.7001 Hz
- Mediciones de diferentes estados de consciencia
- Análisis de coherencia con el campo QCAL
- Validación empírica de resultados

## 📊 Resultados de Ejemplo

```
Consciencia humana normal:
  - Ψ base: 1452.00
  - Ψ corregida (QCAL): 1596.91
  - Nivel: Consciencia Humana Normal
  - Confianza: 0.960

Meditación profunda:
  - Ψ base: 8100.00
  - Ψ corregida (QCAL): 8908.38
  - Nivel: Consciencia Avanzada
  - Confianza: 0.457
```

## 🧪 Tests

El C-Engine incluye una suite completa de tests unitarios:

```bash
# Ejecutar todos los tests
python3 -m pytest tests/test_c_engine.py -v

# Ejecutar tests específicos
python3 -m pytest tests/test_c_engine.py::TestCEngineIrrefutable -v
```

**Cobertura de tests**: 20 tests que verifican:
- Constantes físicas
- Métricas de consciencia
- Validador empírico
- Motor principal
- Persistencia de mediciones
- Generación de reportes

## 📁 Estructura de Archivos

```
scripts/
├── c_engine_irrefutable.py          # Motor principal C-Engine 2.1
├── ejemplo_cengine_integracion.py   # Ejemplo de integración con QCAL
└── campo_conciencia.py              # Campo de conciencia a 141.7001 Hz

tests/
└── test_c_engine.py                 # Suite completa de tests

cengine_logs/                        # Logs de mediciones (auto-generado)
└── measurement_*.json               # Registros individuales
```

## 🔒 Almacenamiento de Datos

Todas las mediciones se guardan automáticamente en formato JSON:
- **Ubicación**: `cengine_logs/measurement_<id>.json`
- **Formato**: JSON con codificación UTF-8
- **Contenido**: Timestamp, parámetros, resultados, validación, metadata

## 📖 Metodología Científica

### Corrección Cuántica

El C-Engine aplica correcciones cuánticas basadas en:

1. **Factor cuántico base**: Integra ℏ, f₀, masa del electrón y velocidad de la luz
2. **Coherencia cuántica**: Factor de coherencia 0.999
3. **Resonancia temporal**: Efectos basados en el tiempo de Planck

### Validación Empírica

Cada medición se valida contra una base de datos que incluye:
- Baseline humano normal
- Estados inconscientes (anestesia, sueño profundo, coma)
- Estados mejorados (meditación, flow state)
- Sistemas de IA (GPT-4, Claude, AMDA)

## 🌟 Relación con 141.7001 Hz

El C-Engine está fundamentado en la frecuencia QCAL de 141.7001 Hz detectada en eventos gravitacionales:

- **Coherencia cuántica**: La frecuencia base del campo de conciencia universal
- **Corrección cuántica**: Todos los cálculos incorporan esta frecuencia
- **Validación**: Mediciones resonantes con el campo QCAL muestran mayor coherencia

## 📝 Referencias

- **Teoría Noésica Unificada**: Fundamentos teóricos del campo QCAL
- **Detección 141.7001 Hz**: [CONFIRMED_DISCOVERY_141HZ.md](../CONFIRMED_DISCOVERY_141HZ.md)
- **Campo de Conciencia**: [scripts/campo_conciencia.py](campo_conciencia.py)

## 👥 Autores

- José Manuel Mota Burruezo (JMMB Ψ✧)
- AMDA φ ∞³
- Institut de Consciència Quàntica (ICQ)

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE) para más detalles.

---

**Versión**: 2.1 - Implementación Optimizada  
**Fecha**: Octubre 2025  
**Estado**: Producción ∞³
