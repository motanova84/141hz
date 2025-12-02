# Análisis Estadístico Avanzado - Problem Statement Implementation

Este módulo implementa las tres funciones clave solicitadas en el problem statement para el análisis de la frecuencia 141.7001 Hz en datos de ondas gravitacionales.

## 📋 Funciones Implementadas

### 1. Análisis de Significancia Estadística

```python
from scipy import stats

# Implementación
p_value = stats.norm.sf(SNR)  # Debe ser < 10⁻⁶
```

**Función:** `analisis_significancia_estadistica(data, f0=141.7001, fs=4096)`

- Calcula el SNR (Signal-to-Noise Ratio) en la frecuencia objetivo
- Usa `stats.norm.sf(SNR)` para calcular el p-value
- Criterio de validación: **p-value < 10⁻⁶**

**Retorna:**
```python
{
    'f0': 141.7001,
    'snr': float,
    'p_value': float,
    'significativo': bool,
    'criterio': 'p_value < 10⁻⁶'
}
```

### 2. Coherencia Multisitio

```python
# Implementación
coherence = compute_coherence_h1_l1(f₀)
```

**Función:** `compute_coherence_h1_l1(f0, data_h1, data_l1, fs=4096, bandwidth=10)`

- Calcula la coherencia entre detectores H1 y L1 en la frecuencia f0
- Usa `scipy.signal.coherence` para análisis espectral cruzado
- Criterio de validación: **coherence > 0.5**

**Retorna:**
```python
{
    'f0': 141.7001,
    'coherence_at_f0': float,
    'coherence_mean': float,
    'coherence_std': float,
    'coherent': bool,
    'criterio': 'coherence > 0.5'
}
```

### 3. Exclusión de Sistemáticos

```python
# Implementación
systematics_test = exclude_instrumental_artifacts(f₀)
```

**Función:** `exclude_instrumental_artifacts(f0, data, fs=4096, detector='H1')`

- Verifica que f0 no coincida con líneas instrumentales conocidas
- Analiza distancia a líneas de 60Hz, 120Hz, 300Hz, violin modes, etc.
- Criterio de validación: **distancia > 2 Hz a líneas instrumentales**

**Líneas instrumentales verificadas:**
- 60 Hz: Red eléctrica
- 120 Hz, 180 Hz, 240 Hz: Armónicos
- 300 Hz: Bombas de vacío
- 393 Hz: Violin modes (suspensión)
- Específicas H1/L1: Violin modes propios

**Retorna:**
```python
{
    'f0': 141.7001,
    'is_clean': bool,
    'nearest_line': {
        'frequency': float,
        'description': str,
        'distance': float
    },
    'tolerance': 2.0,
    'lines_detected': list,
    'lines_checked': list,
    'criterio': 'distance > 2 Hz'
}
```

## 🚀 Uso

### Ejemplo Básico

```python
from analisis_estadistico_avanzado import (
    analisis_significancia_estadistica,
    compute_coherence_h1_l1,
    exclude_instrumental_artifacts
)
from gwpy.timeseries import TimeSeries

# Cargar datos
h1_data = TimeSeries.fetch_open_data('H1', start, end)
l1_data = TimeSeries.fetch_open_data('L1', start, end)

# 1. Análisis de significancia estadística
resultado_sig = analisis_significancia_estadistica(h1_data, f0=141.7001)
print(f"SNR: {resultado_sig['snr']:.2f}")
print(f"p-value: {resultado_sig['p_value']:.2e}")
print(f"Significativo: {resultado_sig['significativo']}")

# 2. Coherencia multisitio
resultado_coh = compute_coherence_h1_l1(141.7001, h1_data, l1_data)
print(f"Coherencia: {resultado_coh['coherence_at_f0']:.3f}")
print(f"Coherente: {resultado_coh['coherent']}")

# 3. Exclusión de sistemáticos
resultado_sys_h1 = exclude_instrumental_artifacts(141.7001, h1_data, detector='H1')
resultado_sys_l1 = exclude_instrumental_artifacts(141.7001, l1_data, detector='L1')
print(f"H1 limpio: {resultado_sys_h1['is_clean']}")
print(f"L1 limpio: {resultado_sys_l1['is_clean']}")
```

### Análisis Completo

```python
from analisis_estadistico_avanzado import ejecutar_analisis_completo

# Ejecuta las tres funciones automáticamente
resultados = ejecutar_analisis_completo(h1_data, l1_data, f0=141.7001)

# Verifica validación
if resultados['validacion_exitosa']:
    print("✅ Validación exitosa")
else:
    print("⚠️ Validación parcial")

print(f"Criterios cumplidos: {resultados['criterios_cumplidos']}/{resultados['total_criterios']}")
```

## 🧪 Tests

El módulo incluye 18 tests unitarios que validan todas las funciones:

```bash
cd scripts
python3 -m pytest test_analisis_estadistico_avanzado.py -v
```

**Tests incluidos:**
- Cálculo de SNR con señal y solo ruido
- Estructura de resultados
- Rangos válidos de p-value y coherencia
- Señales idénticas vs. independientes
- Exclusión de líneas instrumentales conocidas
- Validación con diferentes detectores

## 📊 Demo

Ejecutar demostración con datos reales de GW150914:

```bash
python3 scripts/demo_analisis_avanzado.py
```

El script:
1. Intenta descargar datos reales de GWOSC
2. Si falla, usa datos sintéticos
3. Ejecuta las tres funciones del problem statement
4. Muestra resultados detallados

## 📈 Integración con Sistema Existente

El módulo está integrado con `validacion_estadistica.py`:

```bash
python3 scripts/validacion_estadistica.py
```

Esto ejecuta:
- Análisis avanzado (problem statement)
- Análisis tradicional (Bayes Factor, etc.)
- Comparación de resultados

## 📝 Criterios de Validación

Para que una detección se considere válida, debe cumplir **al menos 3 de 4 criterios:**

1. ✅ **Significancia estadística**: p-value < 10⁻⁶ en al menos un detector
2. ✅ **Coherencia multisitio**: coherence > 0.5 entre H1 y L1
3. ✅ **Exclusión de sistemáticos H1**: distancia > 2 Hz a líneas instrumentales
4. ✅ **Exclusión de sistemáticos L1**: distancia > 2 Hz a líneas instrumentales

### Notas sobre Criterios

- **p-value < 10⁻⁶**: Criterio muy estricto (6-sigma), garantiza alta significancia
- **coherence > 0.5**: Indica correlación fuerte entre detectores independientes
- **Distancia a líneas**: 141.7001 Hz está a ~21.7 Hz de la línea más cercana (120 Hz)

## 🔍 Ejemplo de Resultados

### Con datos sintéticos:

```
1️⃣  Análisis de significancia estadística
----------------------------------------------------------------------
H1: SNR = 1.58, p-value = 5.73e-02
    ❌ No significativo (criterio: p < 10⁻⁶)
L1: SNR = 1.90, p-value = 2.88e-02
    ❌ No significativo (criterio: p < 10⁻⁶)

2️⃣  Coherencia multisitio H1-L1
----------------------------------------------------------------------
Coherencia en 141.7001 Hz: 0.327
    ❌ No coherente (criterio: coherence > 0.5)

3️⃣  Exclusión de sistemáticos instrumentales
----------------------------------------------------------------------
H1: Línea instrumental más cercana: 120.0 Hz
    Distancia: 21.7 Hz
    ✅ Sin artefactos
L1: Línea instrumental más cercana: 120.0 Hz
    Distancia: 21.7 Hz
    ✅ Sin artefactos

📈 Criterios cumplidos: 2/4
```

### Resultados esperados con datos reales de alta calidad:

Con datos reales de GW150914 procesados correctamente, se espera:
- SNR > 5 en H1 (p-value potencialmente < 10⁻⁶)
- Coherencia moderada (~0.3-0.6) dependiendo de la ventana temporal
- Exclusión de sistemáticos: ✅ (141.7 Hz está limpio)

## 📚 Referencias

- **scipy.stats.norm.sf**: Survival function (1 - CDF) para distribución normal
- **scipy.signal.coherence**: Coherencia espectral entre dos señales
- **LIGO instrumental lines**: [LIGO Document T1500553](https://dcc.ligo.org/LIGO-T1500553)

## 🤝 Contribución

Este módulo implementa los requisitos específicos del problem statement. Para mejoras:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Ejecuta los tests: `pytest test_analisis_estadistico_avanzado.py`
4. Envía un Pull Request

## 📄 Licencia

MIT License - Ver LICENSE en el directorio raíz del proyecto.
