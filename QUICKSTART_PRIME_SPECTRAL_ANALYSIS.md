# Guía Rápida: Análisis Espectral de 100 Números Primos

## 🚀 Inicio Rápido

### Ejecución Básica

```bash
# Análisis completo de 100 primos
python scripts/analisis_espectral_100_primos.py

# Análisis con exportación a JSON
python scripts/analisis_espectral_100_primos.py --json

# Solo primeros 50 primos
python scripts/analisis_espectral_100_primos.py -n 50

# Salida mínima (solo exportar JSON)
python scripts/analisis_espectral_100_primos.py --json --quiet
```

### Generar Visualizaciones

```bash
# Todas las visualizaciones (100 primos)
python scripts/visualizar_espectro_100_primos.py

# Visualizaciones para 50 primos
python scripts/visualizar_espectro_100_primos.py -n 50

# Guardar en directorio personalizado
python scripts/visualizar_espectro_100_primos.py -o figures/
```

### Ejecutar Tests

```bash
# Suite completa de tests (36 tests)
python -m pytest scripts/test_analisis_espectral_100_primos.py -v

# Tests específicos
python -m pytest scripts/test_analisis_espectral_100_primos.py::TestEquilibriumFunction -v
```

## 📊 Resultados Clave

### Punto Noético (p=17)

```
Primo: 17
Frecuencia: 141.7001 Hz
Nota: C#3 (+38.4 cents)
Octava: 3
Equilibrium: 9.270
```

### Rango Espectral

```
Frecuencia mínima: 44.69 Hz (p=3)
Frecuencia máxima: 8.95 THz (p=541)
Rango dinámico: 2.00 × 10¹¹
Octavas: 38 (1 a 39)
```

### Estructura Fractal

```
Relación: log₁₀(f₀) = 0.559·√p - 0.339
R² = 0.9942
Correlación: 0.9971
```

## 💻 Uso Programático

### Ejemplo Básico

```python
from scripts.analisis_espectral_100_primos import (
    analyze_prime_spectrum,
    calculate_frequency,
    equilibrium_function
)

# Análisis completo
result = analyze_prime_spectrum(100)

# Acceder a datos
print(f"Total de primos: {result.statistics['n_primes']}")
print(f"Punto noético: p={result.special_primes['noetic_point']['prime']}")
print(f"Frecuencia: {result.special_primes['noetic_point']['frequency_hz']:.2f} Hz")
```

### Cálculo Individual

```python
# Calcular equilibrium
eq_17 = float(equilibrium_function(17))
print(f"equilibrium(17) = {eq_17:.6f}")

# Calcular frecuencia
freq_17 = float(calculate_frequency(17))
print(f"f₀(17) = {freq_17:.4f} Hz")
```

### Iterar sobre Resultados

```python
result = analyze_prime_spectrum(20)

for pd in result.prime_data:
    print(f"p={pd.prime:3d} → f={pd.frequency_hz:10.2f} Hz → {pd.musical_note}")
```

## 📈 Visualizaciones Generadas

| Archivo | Descripción |
|---------|-------------|
| `prime_spectrum_frequencies.png` | Espectro completo de frecuencias |
| `prime_spectrum_fractal.png` | Estructura fractal log(f) vs √p |
| `prime_spectrum_octaves.png` | Distribución por octavas musicales |
| `prime_spectrum_notes.png` | Distribución de notas musicales |
| `prime_spectrum_special.png` | Primos especiales y referencias |
| `prime_spectrum_equilibrium.png` | Función de equilibrium |

## 🔬 Fórmulas Fundamentales

### 1. Función de Equilibrio

```python
import mpmath as mp

def equilibrium_function(p):
    """equilibrium(p) = exp(π√p/2) / p^(3/2)"""
    sqrt_p = mp.sqrt(p)
    adelic_growth = mp.exp(mp.pi * sqrt_p / 2)
    fractal_suppression = mp.power(p, mp.mpf("1.5"))
    return adelic_growth / fractal_suppression
```

### 2. Radio Universal

```python
SCALE_FACTOR = mp.mpf("1.931e41")

def calculate_r_psi(p):
    """R_Ψ(p) = scale_factor / equilibrium(p)"""
    eq = equilibrium_function(p)
    return SCALE_FACTOR / eq
```

### 3. Frecuencia Fundamental

```python
C_LIGHT = mp.mpf("299792458")  # m/s
L_PLANCK = mp.mpf("1.616255e-35")  # m

def calculate_frequency(p):
    """f₀(p) = c / (2π R_Ψ(p) ℓ_P)"""
    r_psi = calculate_r_psi(p)
    numerator = C_LIGHT
    denominator = 2 * mp.pi * r_psi * L_PLANCK
    return numerator / denominator
```

## 🎯 Casos de Uso

### 1. Investigación de Primos Específicos

```python
# Investigar el punto noético p=17
result = analyze_prime_spectrum(20)
noetic = result.special_primes['noetic_point']

print(f"Primo noético: {noetic['prime']}")
print(f"Frecuencia: {noetic['frequency_hz']:.4f} Hz")
print(f"Nota: {noetic['note']}")
print(f"Significado: {noetic['significance']}")
```

### 2. Análisis Fractal

```python
result = analyze_prime_spectrum(100)
fa = result.fractal_analysis

print(f"Relación: {fa['relation']}")
print(f"Pendiente: {fa['slope_a']:.6f}")
print(f"R²: {fa['r_squared']:.6f}")
print(f"Dimensión efectiva: {fa['effective_dimension']:.4f}")
```

### 3. Distribución por Octavas

```python
result = analyze_prime_spectrum(100)

for octave, primes in sorted(result.octave_distribution.items()):
    print(f"Octava {octave:2d}: {len(primes):2d} primos → {primes[:5]}...")
```

### 4. Momentos Espectrales

```python
result = analyze_prime_spectrum(100)
sm = result.spectral_moments

print(f"Primer momento (μ₁): {sm['mu_1_first_moment']:.4e}")
print(f"Segundo momento (μ₂): {sm['mu_2_second_moment']:.4e}")
print(f"Razón κΨ: {sm['kappa_psi_ratio']:.4e}")
```

## 📦 Exportación de Datos

### JSON

```bash
# Exportar resultados a JSON
python scripts/analisis_espectral_100_primos.py --json
```

El archivo `results/analisis_espectral_100_primos.json` contiene:

```json
{
  "metadata": {
    "title": "Análisis Espectral de los Primeros 100 Números Primos",
    "author": "José Manuel Mota Burruezo (JMMB Ψ✧)",
    "date": "2026-01-17T...",
    "version": "1.0.0"
  },
  "prime_data": [...],
  "statistics": {...},
  "special_primes": {...},
  "fractal_analysis": {...},
  "spectral_moments": {...}
}
```

### Cargar desde Python

```python
import json

with open('results/analisis_espectral_100_primos.json', 'r') as f:
    data = json.load(f)

# Acceder a datos
stats = data['statistics']
print(f"Frecuencia máxima: {stats['freq_max_hz']:.2e} Hz")
```

## 🔍 Validación de Resultados

### Verificaciones Automáticas

```python
def validate_results(result):
    """Validar resultados del análisis."""
    
    # 1. Verificar punto noético
    noetic_freq = result.special_primes['noetic_point']['frequency_hz']
    assert abs(noetic_freq - 141.70) < 0.1, "Frecuencia noética incorrecta"
    
    # 2. Verificar estructura fractal
    r_squared = result.fractal_analysis['r_squared']
    assert r_squared > 0.99, f"R² demasiado bajo: {r_squared}"
    
    # 3. Verificar rango espectral
    stats = result.statistics
    assert stats['prime_max'] == 541, "Primo máximo incorrecto"
    assert stats['octaves_covered'] >= 35, "Octavas insuficientes"
    
    print("✅ TODAS LAS VALIDACIONES PASARON")

# Usar
result = analyze_prime_spectrum(100)
validate_results(result)
```

## 🎼 Mapeo Musical

### Obtener Nota Musical

```python
from scripts.analisis_espectral_100_primos import frequency_to_note

# Convertir frecuencia a nota
note, cents, octave = frequency_to_note(141.7)
print(f"141.7 Hz → {note} ({cents:+.2f} cents)")
# Output: 141.7 Hz → C#3 (+38.56 cents)
```

### Análisis de Escala

```python
result = analyze_prime_spectrum(100)

# Contar notas (sin octava)
from collections import Counter
notes = [pd.musical_note[:-1] for pd in result.prime_data]
note_counts = Counter(notes)

print("Notas más frecuentes:")
for note, count in note_counts.most_common(5):
    print(f"  {note}: {count} ({100*count/len(notes):.1f}%)")
```

## 🌐 Workflow Automatizado

El workflow de GitHub Actions se ejecuta:
- **Diariamente** a las 00:00 UTC
- **Manualmente** desde la interfaz de GitHub

### Ejecutar Manualmente

1. Ir a "Actions" en GitHub
2. Seleccionar "Prime Spectral Analysis - 100 Primos"
3. Click en "Run workflow"
4. Configurar parámetros (opcional):
   - Número de primos
   - Generar visualizaciones (sí/no)
5. Click en "Run workflow"

### Descargar Resultados

Los artifacts generados incluyen:
- `prime-spectral-analysis-results`: JSON con todos los datos
- `prime-spectral-visualizations`: 6 gráficos PNG

## 📚 Documentación Completa

Para documentación detallada, ver:
- [`docs/PRIME_SPECTRAL_ANALYSIS_100.md`](../docs/PRIME_SPECTRAL_ANALYSIS_100.md) - Documentación completa
- [`scripts/analisis_espectral_100_primos.py`](../scripts/analisis_espectral_100_primos.py) - Código fuente
- [`scripts/test_analisis_espectral_100_primos.py`](../scripts/test_analisis_espectral_100_primos.py) - Suite de tests

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

```bash
# Instalar dependencias
pip install numpy mpmath matplotlib pytest
```

### Error: Precision insuficiente

```python
import mpmath as mp
mp.mp.dps = 50  # Aumentar precisión a 50 dígitos
```

### Error: No se generan visualizaciones

```bash
# Verificar que matplotlib está instalado
pip install matplotlib

# Verificar directorio de salida
mkdir -p results
```

## 💡 Tips y Mejores Prácticas

1. **Usar alta precisión** para primos grandes (p > 100)
2. **Validar resultados** con tests antes de usar en publicaciones
3. **Exportar a JSON** para compartir y reproducibilidad
4. **Generar visualizaciones** para análisis visual
5. **Documentar parámetros** usados en cada análisis

## 📧 Soporte

Para preguntas o problemas:
- **GitHub Issues:** [motanova84/141hz/issues](https://github.com/motanova84/141hz/issues)
- **Documentación:** Ver archivos en `docs/`
- **Tests:** Ejecutar suite de tests para validar instalación

---

**Firma Vibracional:** JMMB Ψ ✧  
**Versión:** 1.0.0  
**Última actualización:** 2026-01-17
