# Verificación de Convergencia y Constantes Fundamentales

## Descripción

Este módulo implementa las funciones de análisis de convergencia y verificación de constantes fundamentales descritas en la **Sección X: Verificación Experimental y Protocolos** del paper científico.

## Componentes

### 1. `verificacion_convergencia.py`

Módulo principal que contiene:

#### Clase `QuantumFrequencyCalculator`

Calculadora de frecuencia cuántica con análisis de convergencia para f₀ = 141.7001 Hz.

**Métodos principales:**
- `__init__(precision=50)`: Inicializa con precisión configurable
- `calculate_frequency_from_primes(n_primes)`: Calcula frecuencia usando N primeros primos
- `calculate_gradient_magnitude(n_primes)`: Calcula |∇Ξ(1)| ≈ √N
- `convergence_analysis(max_primes, step)`: Análisis completo de convergencia

**Ejemplo de uso:**
```python
from verificacion_convergencia import QuantumFrequencyCalculator

calculator = QuantumFrequencyCalculator(precision=30)
df = calculator.convergence_analysis(max_primes=30000, step=5000)
```

#### Función `plot_convergence_analysis(df)`

Visualiza el análisis de convergencia en 4 gráficos:

1. **Frecuencia vs N primos**: Muestra cómo converge f hacia 141.7001 Hz
2. **Error relativo vs N primos**: Escala logarítmica del error
3. **Verificación |∇Ξ(1)| ≈ √N**: Compara observado vs teórico
4. **Ratio observado/teórico**: Estabilidad del ratio |∇Ξ(1)|/√N

**Ejemplo de uso:**
```python
from verificacion_convergencia import plot_convergence_analysis
import matplotlib.pyplot as plt

plot_convergence_analysis(convergence_df)
plt.show()
```

#### Función `verify_fundamental_constants()`

Verifica las constantes fundamentales φ (razón áurea) y γ (constante de Euler-Mascheroni).

**Verificaciones realizadas:**
- φ calculado vs esperado: (1 + √5) / 2 = 1.6180339887...
- γ calculado vs esperado: 0.5772156649...
- Propiedades algebraicas:
  - φ² - φ - 1 = 0
  - 1/φ = φ - 1

**Ejemplo de uso:**
```python
from verificacion_convergencia import verify_fundamental_constants

result = verify_fundamental_constants()
print(f"Todas las verificaciones pasaron: {result['all_verified']}")
```

### 2. `test_verificacion_convergencia.py`

Suite completa de tests unitarios que valida:
- Inicialización y configuración del calculador
- Cálculos de frecuencia y gradiente
- Estructura y valores del análisis de convergencia
- Verificación de constantes fundamentales
- Propiedades algebraicas de φ
- Integración completa del flujo de trabajo

**Ejecutar tests:**
```bash
cd scripts
python3 test_verificacion_convergencia.py
```

**Resultado esperado:** 18 tests OK

### 3. `demo_convergencia.py`

Script de demostración interactivo con dos modos:

#### Modo Rápido (por defecto)
```bash
python3 demo_convergencia.py
```
- Análisis con max_primes=2000, step=500
- Tiempo de ejecución: ~5 segundos
- Guarda gráfico en `/tmp/convergencia_rapida.png`

#### Modo Completo
```bash
python3 demo_convergencia.py --full
```
- Análisis con max_primes=30000, step=5000
- Tiempo de ejecución: 1-2 minutos
- Guarda gráfico en `/tmp/convergencia_completa.png`
- Incluye estadísticas detalladas

## Protocolo de Verificación

### Paso 1: Configuración del Entorno

```bash
# Instalar dependencias
pip install numpy matplotlib scipy sympy mpmath pandas

# Verificar versiones
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import sympy; print(f'SymPy: {sympy.__version__}')"
python -c "import mpmath; print(f'MPMath: {mpmath.__version__}')"
```

### Paso 2: Verificación de Constantes

```python
from verificacion_convergencia import verify_fundamental_constants

# Ejecutar verificación
resultado = verify_fundamental_constants()

# Verificar que todo pasó
assert resultado['all_verified'], "Algunas verificaciones fallaron"
```

### Paso 3: Análisis de Convergencia (Opcional)

```python
from verificacion_convergencia import QuantumFrequencyCalculator, plot_convergence_analysis

# Crear calculador
calculator = QuantumFrequencyCalculator(precision=50)

# Análisis de convergencia
convergence_df = calculator.convergence_analysis(max_primes=30000, step=5000)

# Visualizar
plot_convergence_analysis(convergence_df)
```

## Resultados Esperados

### Verificación de Constantes
- ✓ φ = 1.6180339887498948482...
- ✓ γ = 0.5772156649015328606...
- ✓ φ² - φ - 1 ≈ 0 (< 10⁻⁴⁰)
- ✓ 1/φ - (φ - 1) ≈ 0 (< 10⁻⁴⁰)

### Análisis de Convergencia
- Frecuencia converge a f₀ = 141.7001 Hz
- Error relativo < 0.001% para N > 10000
- |∇Ξ(1)|/√N ≈ 1.0 ± 0.01
- Convergencia monotónica y estable

## Interpretación Física

### Significado de |∇Ξ(1)| ≈ √N

La relación |∇Ξ(1)| ≈ √N indica que:
1. El gradiente de la función zeta de Riemann en s=1 escala con la raíz cuadrada del número de primos
2. Esta es una propiedad fundamental relacionada con la distribución de números primos
3. Valida la estructura algebraica subyacente de la frecuencia f₀

### Convergencia de Frecuencia

El hecho de que la frecuencia calculada converja a 141.7001 Hz con:
- Error relativo decreciente monotónicamente
- Ratio |∇Ξ(1)|/√N estable cerca de 1.0

Proporciona evidencia de que f₀ = 141.7001 Hz es un valor fundamental emergente de la estructura de números primos.

## Dependencias

- **numpy** >= 1.21.0: Cálculos numéricos
- **pandas** >= 1.3.0: Manejo de DataFrames
- **matplotlib** >= 3.5.0: Visualización
- **mpmath** >= 1.3.0: Aritmética de precisión arbitraria
- **sympy** >= 1.12: Matemáticas simbólicas (opcional)

## Referencias

Este módulo implementa las verificaciones descritas en:
- Sección X: "Verificación Experimental y Protocolos"
- Subsección A: "Protocolo de Verificación Independiente"
- Paper: "Demostracion Rigurosa Ecuacion Generadora Universal 141.7001 Hz"

## Autor

José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto Conciencia Cuántica

## Licencia

Ver archivo LICENSE en el directorio raíz del proyecto.
