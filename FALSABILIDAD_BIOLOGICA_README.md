# Test de Falsabilidad Biológica QCAL

## 🎯 Resumen Ejecutivo

Este documento describe el **experimento decisivo** para la falsabilidad de QCAL (Quantum Chromatic Action Logic) mediante mediciones biológicas de respuesta espectral.

## 📋 Criterio de Falsación

La falsabilidad reside en una predicción precisa:

### QCAL Predice
- La respuesta biológica mostrará **estructura espectral discreta** (picos en frecuencias específicas)
- Esta estructura es **independiente de la energía total**
- Específicamente: **ΔF(141.7 Hz) / ΔF(100 Hz) > 1.5** con misma energía

### Biología Tradicional Predice
- Respuesta **plana** en función de frecuencia cuando la energía se mantiene constante
- **ΔF(ω) = constante ± error experimental**

## 🔬 Experimento Decisivo

### Metodología

**Objetivo:** Medir ΔF(ω) con precisión del 0.1% mientras se varía ω manteniendo ∫Ψ²dt constante.

**Parámetros:**
- **Precisión objetivo:** 0.1% (0.001 relativo)
- **Frecuencias medidas:** 50, 70, 100, 120, 141.7, 150, 170, 200 Hz
- **Energía constante:** ∫Ψ²dt = 1.0 (normalizado)
- **Mediciones por frecuencia:** 1000+

### Criterios de Falsación

#### Si ΔF(141.7 Hz) / ΔF(100 Hz) > 1.5 con misma energía
→ **QCAL recibe apoyo experimental fuerte**

#### Si ΔF(ω) = constante ± error experimental
→ **QCAL se falsa**

## 💻 Implementación

### Scripts Principales

#### 1. Experimento de Falsabilidad
**Archivo:** `scripts/test_falsabilidad_biologica.py`

```bash
# Ejecutar experimento completo
python scripts/test_falsabilidad_biologica.py
```

**Salidas:**
- `results/falsabilidad_biologica_qcal.json` - Resultados modelo QCAL
- `results/falsabilidad_biologica_qcal.png` - Visualización modelo QCAL
- `results/falsabilidad_biologica_traditional.json` - Resultados modelo tradicional
- `results/falsabilidad_biologica_traditional.png` - Visualización modelo tradicional

#### 2. Tests Unitarios
**Archivo:** `tests/test_falsabilidad_biologica.py`

```bash
# Ejecutar tests
python -m pytest tests/test_falsabilidad_biologica.py -v
```

**Tests incluidos (18 total):**
- Configuración experimental
- Respuesta QCAL en resonancia
- Respuesta tradicional plana
- Energía constante
- Precisión del 0.1%
- Criterio de ratio QCAL
- Test de planicidad
- Falsabilidad QCAL
- Workflows completos

## 📊 Resultados

### Modelo QCAL

```
Test de Ratio (141.7 Hz / 100 Hz):
  ΔF(141.7 Hz) = 3.500
  ΔF(100 Hz) = 1.035
  Ratio = 3.380 ± 0.005
  Umbral QCAL = 1.5
  QCAL soportado: ✅ True
  Significancia: 392.9σ
  Precisión relativa: 0.14%

Test de Planicidad:
  Coeficiente de variación: 0.5658
  Respuesta plana: ❌ False
  Biología tradicional soportada: ❌ False

Veredicto: QCAL recibe apoyo experimental fuerte
```

### Modelo Tradicional

```
Test de Ratio (141.7 Hz / 100 Hz):
  ΔF(141.7 Hz) = 1.000
  ΔF(100 Hz) = 1.000
  Ratio = 1.000 ± 0.001
  Umbral QCAL = 1.5
  QCAL soportado: ❌ False
  Significancia: -358.0σ
  Precisión relativa: 0.14%

Test de Planicidad:
  Coeficiente de variación: 0.0000
  Respuesta plana: ✅ True
  Biología tradicional soportada: ✅ True

Veredicto: Biología tradicional confirmada
```

## 🔄 CI/CD Integration

### Workflow Automatizado

**Archivo:** `.github/workflows/biological-falsifiability.yml`

**Triggers:**
- Semanal (domingos a medianoche)
- Manual (`workflow_dispatch`)
- Push/PR modificando archivos relacionados

**Jobs:**
1. `test-falsifiability` - Ejecuta experimento en Python 3.11 y 3.12
2. `validate-precision` - Valida requisito de precisión 0.1%

**Artefactos:**
- Resultados JSON
- Gráficos PNG
- Retención: 30 días

### Ejecución Manual

```bash
# Vía GitHub Actions UI
# 1. Ir a Actions → Biological Falsifiability Test
# 2. Click "Run workflow"
# 3. Seleccionar modelo (qcal, traditional, both)
```

## 📈 Visualizaciones

El experimento genera 4 gráficos por modelo:

### 1. Respuesta vs Frecuencia
- Respuesta biológica medida en cada frecuencia
- Marca vertical en f₀ = 141.7 Hz
- Barras de error (precisión)

### 2. Respuesta Normalizada
- Normalizado por respuesta media
- Línea horizontal en 1.0 (respuesta plana esperada)
- Comparación con predicción tradicional

### 3. Precisión Alcanzada
- Error relativo por frecuencia
- Línea horizontal en 0.001 (objetivo 0.1%)
- Escala logarítmica

### 4. Comparación Clave (141.7 Hz vs 100 Hz)
- Gráfico de barras
- Ratio calculado
- Umbral QCAL (1.5)
- Veredicto

## 🧪 Uso Programático

### Ejemplo Básico

```python
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, 'scripts')

from test_falsabilidad_biologica import (
    ExperimentalConfig,
    QCALBiologicalExperiment
)

# Crear configuración
config = ExperimentalConfig(
    precision_target=0.001,  # 0.1%
    frequencies=[100.0, 141.7],
    energy_constant=1.0,
    num_measurements=1000
)

# Crear experimento
experiment = QCALBiologicalExperiment(config)

# Ejecutar con modelo QCAL
experiment.run_experiment(model='qcal')

# Calcular test de ratio
ratio_test = experiment.calculate_ratio_test()
print(f"Ratio: {ratio_test['ratio']:.3f}")
print(f"QCAL supported: {ratio_test['qcal_supported']}")

# Test de planicidad
flat_test = experiment.test_flat_response()
print(f"Is flat: {flat_test['is_flat']}")

# Generar reporte completo
report = experiment.generate_report('qcal')
print(f"Verdict: {report['verdict']}")

# Generar gráficos
experiment.plot_results(Path('output.png'))
```

### Configuración Personalizada

```python
# Alta precisión
config = ExperimentalConfig(
    precision_target=0.0001,  # 0.01%
    num_measurements=10000,
    frequencies=[50, 100, 141.7, 200]
)

# Múltiples frecuencias
config = ExperimentalConfig(
    frequencies=[i * 10.0 for i in range(5, 21)],  # 50-200 Hz cada 10 Hz
    energy_constant=2.0
)
```

## 📚 Fundamento Teórico

### Campo Ψ y Resonancia

El campo Ψ en QCAL obedece:

```
□Ψ + m²_Ψ Ψ + ζ(3) R Ψ + R cos(2πf₀t) Ψ = 0
```

Donde:
- **f₀ = 141.7001 Hz** - Frecuencia fundamental
- **ζ(3) ≈ 1.202** - Constante de acoplamiento
- **R** - Escalar de Ricci

### Respuesta Biológica QCAL

La respuesta biológica sigue:

```
ΔF_QCAL(ω) = E × (1 + A_res / (1 + ((ω - f₀) / Γ)²))
```

Donde:
- **E** - Energía total (constante)
- **A_res ≈ 2.5** - Factor de resonancia
- **Γ ≈ 5 Hz** - Ancho de resonancia

### Respuesta Tradicional

```
ΔF_trad(ω) = E
```

La respuesta depende **solo de la energía**, no de la frecuencia.

## 🎓 Significancia Científica

### Implicaciones si QCAL es Apoyado
1. Existencia de estructura espectral discreta en biología
2. Frecuencia fundamental universal (141.7 Hz)
3. Acoplamiento campo Ψ - sistemas biológicos
4. Nueva física más allá del modelo estándar

### Implicaciones si QCAL es Falsado
1. Respuesta biológica es puramente energética
2. No existe frecuencia fundamental especial
3. Biología tradicional confirmada
4. Estructura espectral es artefacto

## 🔗 Referencias

### Documentos Relacionados
- [PREDICCIONES_FALSABLES_QCAL.md](../PREDICCIONES_FALSABLES_QCAL.md) - Predicciones completas
- [PREDICCIONES_FALSABLES_RESUMEN.md](../PREDICCIONES_FALSABLES_RESUMEN.md) - Resumen ejecutivo
- [README.md](../README.md) - Documentación principal

### Scripts Relacionados
- `scripts/falsabilidad_explicita.py` - Criterios de falsación generales
- `scripts/orquestador_predicciones_qcal.py` - Orquestador de predicciones

### Workflows Relacionados
- `.github/workflows/predicciones-qcal.yml` - Validación de predicciones

## 📝 Licencia

Este código está bajo licencia dual MIT/Apache-2.0.

Copyright © 2024 José Manuel Mota Burruezo

## ✉️ Contacto

- **Autor:** José Manuel Mota Burruezo
- **ORCID:** [0009-0002-1923-0773](https://orcid.org/0009-0002-1923-0773)
- **DOI:** [10.5281/zenodo.17887499](https://doi.org/10.5281/zenodo.17887499)

---

**Última actualización:** 2024-01-27
