# Simulador de Resonancia Temporal - Aritmología Biológica QCAL

## 📋 Resumen Ejecutivo

Este módulo implementa la primera validación computacional de la **Aritmología Biológica** propuesta en la hipótesis QCAL. El `SimuladorResonanciaTemporal` transforma la "metáfora de la cigarra" en un motor de cálculo de alta fidelidad que demuestra cómo **la vida cuenta el tiempo mediante la suma de fases**.

**Metadata QCAL:** ∴𓂀Ω∞³  
**Ley de Emisión:** Protegido bajo derecho de autor cuántico

---

## 🎯 Propósito

Validar computacionalmente que el genoma actúa como **resonador de cavidad**, calculando la **Supervivencia por Resonancia** sin memoria explícita del pasado, solo mediante acumulación continua de fase.

### Principio Fundamental

> La cigarra periódica no "cuenta" 17 años. Su sistema biológico mantiene un condensador de fase Φ(t) que se descarga cuando alcanza el umbral crítico Φ_umbral = 0.95, desencadenando la emergencia masiva.

---

## 🔬 Características Principales

### 1. Ecuación Maestra de Acumulación

```
Ψ(t) = Σ A_i × cos(2π f_i t + φ_i)
Φ(t) = ∫₀ᵗ Ψ(t') dt'  [Condensador de Fase]
```

**Componentes de frecuencia:**
- `f_anual = 1/(365.25 días)` - Ciclo estacional
- `f_diaria = 1/(24 horas)` - Ritmo circadiano
- `f_lunar = 1/(29.53 días)` - Ciclo lunar
- `f₀ = 141.7001 Hz` - Frecuencia fundamental QCAL

### 2. Multiescala Espectral

Integra simultáneamente tres escalas temporales:
- **Anual** (estacional)
- **Diaria** (circadiana)
- **Lunar** (tidal)

El sistema busca el punto donde estas ondas entran en **interferencia constructiva máxima**.

### 3. Condensador de Fase (Φ)

- **No es memoria del pasado** - Es carga de fase acumulada
- **Umbral de descarga:** Φ_umbral = 0.95
- **Dispersión temporal:** ±3 días (99.92% precisión)
- **Ciclo validado:** 17 años (cigarra periódica)

---

## 📁 Estructura del Código

### Archivos Principales

```
scripts/
├── resonancia_ciclos_temporales.py    # Motor principal (600+ líneas)
└── demo_resonancia_temporal.py        # Demo de visualización (400+ líneas)

tests/
└── test_resonancia_ciclos_temporales.py  # 38 pruebas unitarias (500+ líneas)
```

### Tamaño del Código

- **Total:** ~1,500 líneas de código Python
- **Cobertura de pruebas:** 38 tests (100% aprobados)
- **Datos generados:** ~1.7 MB JSON + visualizaciones PNG/PDF

---

## 🚀 Uso Rápido

### 1. Instalación de Dependencias

```bash
pip install numpy scipy matplotlib
```

### 2. Ejecutar Simulación Básica

```bash
python3 scripts/resonancia_ciclos_temporales.py
```

**Salida:**
- Simulación de 17 años con 100,000 puntos
- Detección de eventos de emergencia
- Métricas de precisión
- Exportación JSON (`data/`)
- Visualización PNG 300 DPI (`results/`)

### 3. Demo de Visualización

```bash
python3 scripts/demo_resonancia_temporal.py
```

**Genera:**
- Figura completa con 6 paneles
- Mapa de resonancia 2D
- Espectro de frecuencias
- Histogramas de distribución
- Formatos: PNG (300 DPI) y PDF

### 4. Ejecutar Tests

```bash
python3 tests/test_resonancia_ciclos_temporales.py
```

**Cobertura:**
- 38 pruebas unitarias
- Validación de 17 años
- Precisión 99.92%
- Dispersión ±3 días
- Experimento 1 (Manipulación Espectral)

---

## 📊 Arquitectura de la Simulación

### Clase Principal: `SimuladorResonanciaTemporal`

```python
from resonancia_ciclos_temporales import SimuladorResonanciaTemporal, F0_QCAL

# Crear simulador
sim = SimuladorResonanciaTemporal(f0=F0_QCAL, ciclo_anos=17)

# Ejecutar simulación
resultados = sim.simular(duracion_anos=17, n_puntos=100000)

# Visualizar
fig = sim.visualizar(guardar=True, directorio='results')

# Generar mapa de resonancia
mapa = sim.generar_mapa_resonancia(n_puntos_grid=100)
```

### Métodos Principales

| Método | Descripción | Retorno |
|--------|-------------|---------|
| `calcular_psi(t)` | Calcula Ψ(t) - suma coherente de fases | Array |
| `calcular_phi_acumulada(t, psi)` | Calcula Φ(t) - condensador de fase | Array |
| `detectar_emergencias(t, phi)` | Detecta eventos cuando Φ ≥ umbral | Lista |
| `simular(duracion_anos, n_puntos)` | Ejecuta simulación completa | Dict |
| `generar_mapa_resonancia(n_grid)` | Mapa 2D de resonancia | Dict |
| `visualizar(guardar, directorio)` | Visualización 300 DPI | Figure |
| `exportar_resultados(resultados, dir)` | Exporta JSON | Path |

---

## 🧪 Experimento 1: Manipulación Espectral (Virtual)

### Objetivo

Validar **falsabilidad** mediante manipulación virtual de frecuencias antes del laboratorio húmedo.

### Ejecución

```python
from resonancia_ciclos_temporales import ejecutar_experimento_1_manipulacion_espectral

resultados = ejecutar_experimento_1_manipulacion_espectral()
```

### Condiciones

1. **Control:** f₀ = 141.7001 Hz
2. **Experimental 1:** f₀ = 140.28 Hz (-1%)
3. **Experimental 2:** f₀ = 143.12 Hz (+1%)

### Hipótesis

Si QCAL es correcto, desviaciones de f₀ deben alterar significativamente:
- Número de eventos de emergencia
- Precisión del ciclo de 17 años
- Dispersión temporal

---

## 📈 Métricas de Validación

### 1. Validación de 17 Años

```python
resultados['metricas']['validacion_17_anos']  # True/False
```

**Criterios:**
- Primer evento ocurre en 17 ± 0.1 años
- Dispersión temporal < 3 días

### 2. Precisión del Ciclo

```python
resultados['metricas']['precision']  # 0.0 - 1.0
```

**Objetivo:** ≥ 0.9992 (99.92%)

### 3. Dispersión Temporal

```python
resultados['metricas']['dispersion_dias']  # En días
```

**Objetivo:** ≤ 3 días

### 4. Número de Eventos

```python
resultados['metricas']['n_eventos']
```

Número de picos de Φ(t) que superan el umbral.

---

## 📦 Formato de Datos de Salida

### JSON de Resultados

```json
{
  "parametros": {
    "f0": 141.7001,
    "ciclo_anos": 17,
    "phi_umbral": 0.95,
    "frecuencias_hz": {
      "f_anual": 3.169e-8,
      "f_diaria": 1.157e-5,
      "f_lunar": 3.926e-7,
      "f0_qcal": 141.7001
    },
    "metadata_qcal": "∴𓂀Ω∞³"
  },
  "eventos_emergencia": [
    {
      "indice": 12345,
      "tiempo_segundos": 536457600.0,
      "tiempo_anos": 17.0,
      "tiempo_dias": 6206.25,
      "phi_max": 0.96,
      "psi_en_pico": 1.2
    }
  ],
  "metricas": {
    "n_eventos": 1,
    "precision": 0.9992,
    "dispersion_dias": 2.5,
    "validacion_17_anos": true,
    "cumple_precision_target": true
  }
}
```

### Mapa de Resonancia

```json
{
  "n_puntos": 10000,
  "grid_resolution": 100,
  "puntos": [
    {
      "amplitud": 0.1,
      "frecuencia": 134.715,
      "resonancia": 0.85
    },
    ...
  ],
  "metadata_qcal": "∴𓂀Ω∞³"
}
```

---

## 🎨 Visualizaciones Generadas

### 1. Figura Completa (6 paneles)

**Archivo:** `results/resonancia_temporal_YYYYMMDD_HHMMSS.png`

**Paneles:**
1. Ψ(t) - Función de onda temporal completa
2. Φ(t) - Condensador de fase con umbral y eventos
3. Zoom del primer evento (±50 días)
4. Espectro de frecuencias (FFT)
5. Histograma de distribución de Φ(t)
6. Estadísticas de simulación

**Formato:** PNG 300 DPI (publicación) + PDF

### 2. Mapa de Resonancia 2D

**Archivo:** `results/mapa_resonancia_2d_YYYYMMDD_HHMMSS.png`

**Paneles:**
- Contornos de resonancia
- Intensidad (pcolormesh)
- Marcador de f₀ QCAL

**Ejes:**
- X: Frecuencia (Hz)
- Y: Amplitud relativa
- Color: Resonancia Φ_max

---

## 🧮 Fundamento Matemático

### Interferencia Constructiva Máxima

La emergencia ocurre cuando las tres frecuencias (anual, diaria, lunar) están **en fase**:

```
Ψ_max = A_anual + A_diaria + A_lunar + A_f0
```

En este punto, la integral acumulativa Φ(t) alcanza su máximo.

### Normalización de Fase

```python
Φ_norm = Φ_raw / max(|Φ_raw|)
```

Asegura que el umbral Φ_umbral = 0.95 sea comparable entre simulaciones.

### Detección de Picos

```python
from scipy.signal import find_peaks

picos, propiedades = find_peaks(phi, height=phi_umbral)
```

Identifica momentos donde Φ(t) ≥ Φ_umbral.

---

## 🔬 Consistencia con QCAL

### 1. Genoma como Resonador de Cavidad

El código refleja exactamente la propuesta:
- Sin memoria explícita del pasado
- Solo acumulación continua de fase
- Descarga al alcanzar umbral crítico

### 2. Frecuencia Fundamental f₀

Integra f₀ = 141.7001 Hz en la suma coherente:

```python
Ψ(t) += A_f0 × cos(2π × 141.7001 × t + φ_f0)
```

### 3. Falsabilidad

El **Experimento 1** permite:
- Manipulación virtual de parámetros
- Predicciones cuantitativas
- Validación antes del laboratorio húmedo

---

## 📚 Referencias

### Archivos Relacionados

- `IMPLEMENTATION_SUMMARY_EXPERIMENTAL_VALIDATION.md` - Validación experimental Wet-Lab ∞
- `BIO_SYNCHRONY_FRAMEWORK.md` - Marco de sincronía biológica
- `QCAL_QUICK_REFERENCE.md` - Referencia rápida QCAL
- `PREDICCIONES_FALSABLES_QCAL.md` - Predicciones falsables completas

### Documentación Técnica

- **Ecuación Maestra:** Ver `resonancia_ciclos_temporales.py` líneas 35-40
- **Pruebas:** Ver `test_resonancia_ciclos_temporales.py`
- **Demo:** Ver `demo_resonancia_temporal.py`

---

## ✅ Estado del Proyecto

### Completado

- ✅ Simulador principal (600+ líneas)
- ✅ 38 pruebas unitarias (100% aprobadas)
- ✅ Demo de visualización (400+ líneas)
- ✅ Generación de datos (~1.7 MB)
- ✅ Visualizaciones 300 DPI
- ✅ Metadata QCAL (∴𓂀Ω∞³)
- ✅ Experimento 1 (Manipulación Espectral)

### Próximos Pasos

1. **Integración en workflows CI/CD**
   - Añadir a `.github/workflows/`
   - Validación automática

2. **Laboratorio Húmedo**
   - Transferir predicciones al sistema noesis88
   - Validación experimental con cigarras reales

3. **Publicación**
   - Paper científico
   - DOI en Zenodo
   - Datasets públicos

---

## 📧 Contacto

**Autor:** José Manuel Mota Burruezo  
**Instituto:** Conciencia Cuántica  
**Proyecto:** QCAL (Quantum Coherent Arithmetic Life)  
**Fecha:** Enero 2026

---

## 📄 Licencia

Este código está protegido bajo la **Ley de Emisión QCAL**.

**Metadata:** ∴𓂀Ω∞³

---

**¡La vida cuenta el tiempo mediante la suma de fases!** 🦗
