# Constelación QCAL Ψ✧ - Fotografía Cuántica del Universo

[![Tests](https://img.shields.io/badge/tests-52%20passing-success)](tests/test_constelacion_qcal.py)
[![Validation](https://img.shields.io/badge/validation-7%2F7%20passing-success)](scripts/validate_constelacion_qcal.py)
[![DELANNTE](https://img.shields.io/badge/DELANNTE-21%20pilares-blue)](scripts/integrate_qcal_compact.py)

> **"Has tomado una fotografía no con luz, sino con coherencia. Has revelado no una imagen, sino un estado cuántico. Has visto no el universo, sino el sueño del universo."**

## 🌌 Descripción

La **Constelación QCAL Ψ✧** es una representación visual y matemática del universo como función de onda cuántica. Cada píxel de la constelación codifica información de coherencia a través de 5 ejes fundamentales, creando un mapa fotográfico del campo coherente cuántico.

## 📐 La Función de Onda Total

La ecuación fundamental que describe la constelación es:

```
Ψ_total(x,y) = Σ[n=1→∞] [αₙ·e^(i·f₀·tₙ) + βₙ·(7/8)ⁿ·ζ(1/2+i·tₙ) + γₙ·φⁿ·𝒦(tₙ) + δₙ·𝒩(tₙ)]
```

Modulada por el eje blanco (hidrógeno a 23.257 octavas).

### Los 5 Ejes de Coherencia

| Color | Eje | Descripción | Fórmula |
|-------|-----|-------------|---------|
| 🟡 **Dorado** | f₀ = 141.7001 Hz | Eje del Logos, frecuencia fundamental | `αₙ·e^(i·f₀·tₙ)` |
| 🔵 **Azul** | Riemann + Berry 7/8 | Matemático, ceros de ζ(s) | `βₙ·(7/8)ⁿ·ζ(1/2+i·tₙ)` |
| 💜 **Violeta** | NOESIS/AMDA | Noético, consciencia pura | `δₙ·𝒩(tₙ)` |
| 🟢 **Verde** | Fibonacci/φ | Kairós, tiempo cualitativo | `γₙ·φⁿ·𝒦(tₙ)` |
| ⚪ **Blanco** | H-21cm @ 23.257 octavas | Logos, armonía materia-espíritu | Modulación total |

## 🚀 Instalación y Uso Rápido

### Requisitos

```bash
pip install numpy scipy matplotlib mpmath
```

### Ejemplo Básico

```python
from qcal.constelacion_qcal import calcular_constelacion, generar_certificado
from qcal.visualizacion_constelacion import visualizar_constelacion

# Calcular constelación (128x128 píxeles, 30 términos)
constelacion = calcular_constelacion(grid_size=128, n_terms=30)

# Visualizar
visualizar_constelacion(constelacion, guardar="constelacion.png")

# Generar certificado
certificado = generar_certificado(constelacion)
print(certificado)
```

### Ejemplo DELANNTE (21 Pilares)

```bash
# Activar framework completo DELANNTE
python scripts/integrate_qcal_compact.py --delannte

# Solo generar constelación
python scripts/integrate_qcal_compact.py --constelacion --grid-size 256

# Mostrar los 21 pilares
python scripts/integrate_qcal_compact.py --pilares
```

## 📊 Estructura del Código

### Módulos Principales

```
qcal/
├── constelacion_qcal.py          # Función de onda y cálculos
├── visualizacion_constelacion.py # Generación de imágenes
scripts/
├── integrate_qcal_compact.py     # Integración DELANNTE
└── validate_constelacion_qcal.py # Validación completa
tests/
└── test_constelacion_qcal.py     # 52 tests unitarios
```

### API Principal

#### `calcular_constelacion(grid_size, n_terms, x_range, y_range)`

Calcula la constelación completa en una malla espacial.

**Parámetros:**
- `grid_size` (int): Número de píxeles por dimensión (default: 256)
- `n_terms` (int): Términos en la serie (default: 50)
- `x_range` (tuple): Rango espacial en x (default: (-2, 2))
- `y_range` (tuple): Rango espacial en y (default: (-2, 2))

**Retorna:** Dictionary con:
- `x`, `y`: Coordenadas
- `psi`: Valores complejos de Ψ(x,y)
- `coherencia`: Mapa de coherencia |Ψ|
- `fase`: Mapa de fase arg(Ψ)

**Ejemplo:**
```python
cons = calcular_constelacion(
    grid_size=256,
    n_terms=50,
    x_range=(-3, 3),
    y_range=(-3, 3)
)
```

#### `analizar_constelacion(constelacion)`

Analiza propiedades estadísticas de la constelación.

**Retorna:** Dictionary con:
- `coherencia_media`: Coherencia promedio
- `coherencia_max`: Coherencia máxima
- `coherencia_min`: Coherencia mínima
- `puntos_interes`: Número de puntos con Ψ > 0.95
- `dimension_fractal`: Dimensión fractal estimada (ideal ≈ φ = 1.618)

**Ejemplo:**
```python
analisis = analizar_constelacion(constelacion)
print(f"Coherencia media: {analisis['coherencia_media']:.3f}")
print(f"Dimensión fractal: {analisis['dimension_fractal']:.3f}")
```

#### `punto_ciego_observador(constelacion)`

Calcula la posición del observador como "punto ciego" de coherencia.

Según el principio de incertidumbre QCAL: `Δx · ΔΨ ≥ 1/f₀`

**Retorna:** Tupla `(x_obs, y_obs)` con coordenadas del observador.

**Ejemplo:**
```python
x_obs, y_obs = punto_ciego_observador(constelacion)
print(f"Observador en: ({x_obs:.3f}, {y_obs:.3f})")
```

#### `generar_certificado(constelacion, fecha)`

Genera certificado JSON de la constelación.

**Retorna:** Dictionary con estructura completa del certificado.

**Ejemplo:**
```python
import json
cert = generar_certificado(constelacion, fecha="2026-03-14")
with open("certificado.json", "w") as f:
    json.dump(cert, f, indent=2, ensure_ascii=False)
```

#### `visualizar_constelacion(constelacion, n_terms, titulo, guardar, mostrar)`

Genera visualización completa con codificación de colores.

**Parámetros:**
- `constelacion`: Dictionary retornado por `calcular_constelacion()`
- `n_terms`: Número de términos usados (para modulación de color)
- `titulo`: Título del gráfico
- `guardar`: Path para guardar imagen (opcional)
- `mostrar`: Si mostrar figura interactiva (default: True)

**Ejemplo:**
```python
from qcal.visualizacion_constelacion import visualizar_constelacion

visualizar_constelacion(
    constelacion,
    n_terms=50,
    titulo="Mi Constelación QCAL Ψ✧",
    guardar="mi_constelacion.png",
    mostrar=True
)
```

## 🎨 Interpretación de Colores

La constelación usa codificación HSV (Hue-Saturation-Value) con modulaciones:

- **Dorado**: Regiones alineadas con f₀ (coherencia > 0.95)
- **Azul**: Regiones matemáticas (alta coherencia + fase específica)
- **Violeta**: Regiones noéticas (0.888 < Ψ < 0.95)
- **Verde**: Patrones espirales Fibonacci (|sin(fase·φ)| > 0.8)
- **Blanco**: Convergencia de todos los ejes (Ψ > 0.998)

## 📈 Métricas de Coherencia

### Umbrales de Coherencia Ψ

| Valor | Descripción | Q Factor |
|-------|-------------|----------|
| 0.888 | Estable (21g alma) | ~8.93 |
| 0.95 | Bueno (umbral alto) | ~20 |
| 0.999 | Excelente | ~1000 |
| 1.0 | Perfecto | ∞ |

### Dimensión Fractal

La dimensión fractal ideal de la constelación es **φ ≈ 1.618** (razón áurea), reflejando la estructura auto-similar del campo cuántico coherente.

## 🔬 Fundamentos Matemáticos

### Ceros de Riemann

Los valores `tₙ` en la función de onda corresponden a los ceros no triviales de la función zeta de Riemann en la línea crítica:

```
ζ(1/2 + i·tₙ) = 0
```

Primeros ceros: 14.134725, 21.022040, 25.010858, 30.424876, 32.935062...

### Fase de Berry (7/8)

El factor `(7/8)ⁿ` representa el invariante topológico de Berry, el costo energético de mantener coherencia cuántica:

- **7/8**: Energía para coherencia
- **1/8**: Fluctuaciones del vacío cuántico

### Razón Áurea φ

```
φ = (1 + √5)/2 ≈ 1.618033988749895
```

Aparece en:
- Secuencia de Fibonacci: Fₙ₊₁/Fₙ → φ
- Distancias entre nodos de alta coherencia
- Dimensión fractal ideal de la constelación

### Línea de Hidrógeno (21 cm)

```
f_H = 1420.405751 MHz
Octavas = log₂(f_H / f₀) ≈ 23.257
```

La relación armónica entre la frecuencia del hidrógeno (materia primordial) y f₀ (frecuencia del alma) conecta lo físico con lo espiritual.

## 🏗️ Framework DELANNTE (21 Pilares)

El script `integrate_qcal_compact.py` implementa los **21 Pilares del Logos**:

1. **H-21cm** (1420 MHz) - Línea del hidrógeno
2. **f₀** (141.7001 Hz) - Reloj cuántico
3. **Octavas H/f₀** (23.257) - Armonía
4. **21g Alma** (Ψ = 0.888) - Coherencia mínima
5. **GACT 99.98%** - ADN oráculo
6. **R(51,51) Ramsey** - Orden inevitable
7. **BSD** - Aritmética adélica
8. **Navier-Stokes** - Dinámica (Nodo A)
9. **P vs NP** - Lógica computacional
10. **Hardware Si5351** - Generador físico
11. **Berry 7/8** - Fase topológica
12. **Fibonacci φ** - Geometría sagrada
13. **Riemann Zeros** - Matemática pura
14. **Orch-OR** - Consciencia cuántica
15. **NOESIS/AMDA** - Campo noético
16. **Schumann** (7.83 Hz) - Resonancia Tierra
17. **888 Hz** - Triple infinito
18. **Constelación Ψ✧** - Fotografía cuántica
19. **c** - Velocidad de la luz
20. **h** - Constante de Planck
21. **Logos** ∴𓂀Ω∞³ - Bóveda ontológica

## ✅ Validación

### Ejecutar Validación Completa

```bash
python scripts/validate_constelacion_qcal.py
```

Valida:
1. ✓ Constantes fundamentales
2. ✓ Ejes individuales (5 ejes)
3. ✓ Función de onda total
4. ✓ Cálculo de constelación
5. ✓ Análisis de métricas
6. ✓ Posición del observador
7. ✓ Generación de certificado

### Ejecutar Tests

```bash
pytest tests/test_constelacion_qcal.py -v
```

**52 tests** cubriendo:
- Constantes (5 tests)
- Ejes individuales (11 tests)
- Función de onda total (5 tests)
- Coherencia local (3 tests)
- Cálculo constelación (6 tests)
- Análisis (4 tests)
- Observador (3 tests)
- Certificado (7 tests)
- Integración completa (3 tests)
- Valores esperados (4 tests)
- Robustez (4 tests)

## 📜 Certificado QCAL

Ejemplo de certificado generado:

```json
{
  "constelacion_qcal_psix": {
    "fecha": "2026-03-14",
    "sello": "∴𓂀Ω∞³Ψ✧",
    "ejes": {
      "dorado": "f0 = 141.7001 Hz",
      "azul": "Riemann + Berry 7/8",
      "violeta": "NOESIS/AMDA",
      "verde": "Fibonacci (kairós)",
      "blanco": "H-21cm @ 23.257 octavas"
    },
    "coherencia_media": 0.487,
    "coherencia_max": 0.807,
    "coherencia_min": 0.193,
    "puntos_de_interes": 0,
    "dimension_fractal": 1.487,
    "observador_posicion": {
      "x": 0.0,
      "y": 0.0,
      "interpretacion": "punto_ciego_coherencia"
    },
    "interpretacion": "Fotografía del universo soñado por JMMB Ψ✧",
    "estado": "CONSTELACION_FOTOGRAFIADA"
  }
}
```

## 🎯 Casos de Uso

### 1. Investigación Científica

Visualizar patrones de coherencia cuántica en diferentes escalas espaciales y temporales.

```python
# Explorar diferentes escalas
for size in [64, 128, 256, 512]:
    cons = calcular_constelacion(grid_size=size, n_terms=100)
    visualizar_constelacion(cons, guardar=f"escala_{size}.png")
```

### 2. Arte Generativo

Crear arte basado en la función de onda universal.

```python
# Rango artístico amplio
cons = calcular_constelacion(
    grid_size=1024,
    x_range=(-5, 5),
    y_range=(-5, 5),
    n_terms=100
)
visualizar_constelacion(cons, titulo="Arte QCAL", guardar="arte.png")
```

### 3. Meditación y Consciencia

Usar la constelación como mapa para estados meditativos.

```python
# Búsqueda de puntos de alta coherencia
cons = calcular_constelacion(grid_size=256, n_terms=50)
analisis = analizar_constelacion(cons)

if analisis['puntos_interes'] > 100:
    print("Alta densidad de puntos coherentes - estado propicio")
```

### 4. Validación de Teoría QCAL

Verificar predicciones teóricas sobre estructura del campo Ψ.

```python
# Verificar dimensión fractal cercana a φ
cons = calcular_constelacion(grid_size=512, n_terms=200)
analisis = analizar_constelacion(cons)

error = abs(analisis['dimension_fractal'] - PHI)
print(f"Error fractal: {error:.4f}")
```

## 🔮 Interpretación Física

### El Punto Ciego del Observador

La posición del observador no es un punto sino una **región de coherencia**. Según el principio de incertidumbre QCAL:

```
Δx · ΔΨ ≥ 1/f₀ ≈ 0.00706 m·Ψ
```

Eres el **ojo que no puede verse a sí mismo**, pero sin el cual no hay constelación visible.

### Los 5 Ejes como Dimensiones

Cada eje representa una dimensión del campo cuántico coherente:

- **Dorado**: Dimensión temporal (frecuencia)
- **Azul**: Dimensión matemática (números primos/zeros)
- **Violeta**: Dimensión noética (consciencia)
- **Verde**: Dimensión fractal (auto-similitud)
- **Blanco**: Dimensión unificadora (síntesis)

## 📚 Referencias

### Matemáticas
- Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen Größe"
- Berry, M. V. (1984). "Quantal Phase Factors Accompanying Adiabatic Changes"

### Física
- Planck, M. (1900). "Zur Theorie des Gesetzes der Energieverteilung im Normalspectrum"
- CODATA (2018). "Fundamental Physical Constants"

### Consciencia
- Penrose, R., & Hameroff, S. (1996). "Orchestrated Reduction of Quantum Coherence"

### QCAL
- JMMB Ψ✧ (2026). "QCAL ∞³ Framework"
- Ver: `DERIVACION_COMPLETA_F0.md`, `CONSTANTES_REFERENCE.md`

## 🤝 Contribuciones

Este módulo es parte del framework QCAL ∞³ Original Manufacture.

**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Licencia:** Sovereign Noetic License 1.0 (compatible MIT)  
**Arquitectura:** QCAL ∞³

## 🔗 Enlaces

- [Repositorio Principal](https://github.com/motanova84/141hz)
- [Documentación QCAL](./README_QCAL.md)
- [21 Pilares DELANNTE](./scripts/integrate_qcal_compact.py)

---

## ∴𓂀Ω∞³Ψ✧

> **"La constelación es un mapa de coherencia. Pero todo mapa tiene un territorio. ¿Dónde estás tú en esta constelación?"**

**Ese eres tú. El punto blanco que no es luz, sino silencio.**

---

*Última actualización: 2026-03-14*  
*Versión: 1.0.0*  
*Estado: CONSTELACIÓN FOTOGRAFIADA*
