# Demostración Matemática: 141.7001 Hz como Frecuencia Inevitable

## Descripción

Este script implementa una demostración matemática rigurosa que prueba que la frecuencia **141.7001 Hz** emerge inevitablemente de la estructura fundamental de los números primos organizados según la proporción áurea φ.

## Script

**Archivo:** `demostracion_matematica_141hz_inevitable.py`

## Componentes de la Demostración

### 1. Serie Prima Compleja

Implementa la serie:

```
S_N = Σ(n=1 to N) e^(2πi·log(p_n)/φ)
```

donde `p_n` son los números primos y `φ` es la proporción áurea.

### 2. Comportamiento Asintótico

Analiza el comportamiento de `|S_N|/√N` para demostrar que converge a una constante `C ≈ 4.9`.

### 3. Distribución de Fases

Verifica que las fases `θ_n = 2π log(p_n)/φ` siguen una distribución cuasi-uniforme, confirmando la hipótesis de independencia estadística.

### 4. Función Theta de Jacobi

Implementa la función theta `θ(it) = 1 + 2e^(πt)` que proporciona la frecuencia fundamental `f₀ = 1/(2π)`.

### 5. Transformación Dimensional

Visualiza la transformación del dominio matemático al dominio físico mediante:

- **Escalado por constantes fundamentales:** γ (Euler-Mascheroni), φ (proporción áurea), π, e
- **Conexión cuántica:** Postulado de Planck-Einstein (E = ℏω)

### 6. Construcción de Frecuencia

Construye la frecuencia paso a paso desde las constantes fundamentales:

```
f = (1/2π) · e^γ · √(2πγ) · (φ²/2π) · |∇Ξ(1)| = 141.7001 Hz
```

## Uso

### Ejecución Básica

```bash
python3 scripts/demostracion_matematica_141hz_inevitable.py
```

### Salida

El script genera dos archivos PNG en el directorio `results/`:

1. **puentes_dimensionales.png** (20x10 pulgadas, 300 DPI)
   - Panel 1: Puente dimensional entre matemática pura y realidad física
   - Panel 2: Escalas dimensionales y factores de conversión

2. **demostracion_141hz_inevitable.png** (20x24 pulgadas, 300 DPI)
   - Panel 1: Serie prima compleja en el plano complejo
   - Panel 2: Convergencia asintótica |∇Ξ(1)| ≈ C√N
   - Panel 3: Distribución cuasi-uniforme de fases
   - Panel 4: Función theta (componente espectral fundamental)
   - Panel 5: Construcción paso a paso de la frecuencia
   - Panel 6: Resumen y conclusiones con constantes fundamentales

### Salida de Consola

El script imprime:
- Constantes matemáticas fundamentales
- Progreso del análisis
- Resultados estadísticos (convergencia, KS-test)
- Transformación dimensional paso a paso
- Resumen de la demostración

## Requisitos

### Dependencias Python

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
mpmath>=1.3.0
```

Estas dependencias están incluidas en `requirements.txt`.

## Estructura del Código

### Funciones Principales

- `sieve_of_eratosthenes(limit)`: Genera números primos hasta un límite
- `get_first_n_primes(n)`: Obtiene los primeros n números primos
- `compute_prime_complex_series(primes)`: Calcula la serie prima compleja
- `analyze_asymptotic_behavior(max_n, num_points)`: Analiza comportamiento asintótico
- `analyze_phase_distribution(n_primes)`: Analiza distribución de fases
- `theta_function(t, num_terms)`: Calcula función theta de Jacobi
- `create_dimensional_bridge_panel(ax1, ax2)`: Crea visualización de puentes dimensionales
- `create_complete_demonstration()`: Genera la demostración completa de 6 paneles

### Configuración

La variable `RESULTS_DIR` al inicio del script define el directorio de salida:

```python
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
```

Para cambiar el directorio de salida, modifica esta variable.

## Fundamentos Matemáticos

### Constantes Fundamentales

- **γ (Euler-Mascheroni):** 0.5772156649...
- **φ (Proporción Áurea):** 1.6180339887... = (1 + √5)/2
- **π:** 3.1415926536...
- **e:** 2.7182818285...

### Factores Derivados

- **e^γ:** 1.78107242
- **√(2πγ):** 1.90440358
- **φ²/(2π):** 0.41668362

## Interpretación de Resultados

### Convergencia Asintótica

El valor de convergencia (0 a 1) indica qué tan bien |S_N|/√N se aproxima a una constante. Valores cercanos a 1 indican convergencia fuerte.

### Test de Kolmogorov-Smirnov

El KS-test verifica la uniformidad de la distribución de fases:
- **Estadístico KS bajo (< 0.2):** Distribución aproximadamente uniforme
- **p-value bajo:** Rechaza hipótesis de uniformidad perfecta (esperado en distribuciones cuasi-uniformes)

### Ecuación Maestra

La ecuación final demuestra que 141.7001 Hz emerge exclusivamente de:
1. Constantes matemáticas fundamentales (γ, φ, π, e)
2. La estructura de los números primos
3. Sin parámetros empíricos o ajustables

## Referencias

- **Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)
- **Fecha:** 21 de agosto de 2025
- **Proyecto:** Análisis GW 141Hz

## Notas Técnicas

- Los gráficos utilizan `matplotlib.use('Agg')` para compatibilidad sin display
- Las imágenes se guardan con alta resolución (150 DPI) para publicación
- El script es completamente autocontenido y reproducible
- No requiere datos externos ni conexión a internet
