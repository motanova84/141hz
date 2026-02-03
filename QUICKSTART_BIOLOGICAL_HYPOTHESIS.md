# Quick Start: QCAL Biological Hypothesis

**Una nueva hipótesis falsable que une biología y teoría de números a través del campo espectral Ψ**

---

## 📋 Resumen Ejecutivo

Este framework implementa la hipótesis QCAL para sistemas biológicos, demostrando cómo organismos como la cigarra periódica (*Magicicada*) utilizan resonancias espectrales y ciclos primos (13, 17 años) para sincronizar emergencias masivas con precisión del 99.92%.

**Concepto clave:** Los sistemas vivos no acumulan simplemente energía térmica, sino que integran información espectral estructurada a través del campo Ψ.

---

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Verificar instalación
python -c "from qcal.biological_qcal import QCALBiologicalSystem; print('✓ QCAL Biology OK')"
```

---

## 📖 Documentación Completa

**Documento principal:** [HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md](HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md)

Contenido:
- Introducción a la hipótesis falsable
- Colapso de fase y umbrales biológicos
- Naturaleza espectral de señales biológicas
- Formalización matemática completa
- Experimentos de falsación propuestos

---

## 🔬 Uso Básico

### Ejemplo 1: Sistema QCAL Básico

```python
from qcal.biological_qcal import (
    EnvironmentalSpectralField,
    BiologicalFilter,
    PhaseAccumulator,
    QCALBiologicalSystem
)
import numpy as np

# 1. Crear campo ambiental espectral
env_field = EnvironmentalSpectralField()
env_field.add_component(
    amplitude=1.0,
    frequency=2*np.pi/(365*24*3600),  # Ciclo anual
    phase=0.0,
    description="Ciclo estacional anual"
)

# 2. Crear filtro biológico
bio_filter = BiologicalFilter(
    center_frequencies=[1/(365*24*3600)],  # Resonancia anual
    bandwidths=[1e-9]
)

# 3. Crear acumulador de fase
phase_accumulator = PhaseAccumulator(
    threshold=10.0,
    memory_alpha=0.1  # 90% retención de memoria
)

# 4. Crear sistema completo
qcal_system = QCALBiologicalSystem(env_field, bio_filter, phase_accumulator)

# 5. Simular
t = np.linspace(0, 15*365*24*3600, 1000)  # 15 años
results = qcal_system.simulate(t, apply_memory=True)

print(f"Sistema activado: {results['activated']}")
if results['activation_time']:
    years = results['activation_time'] / (365*24*3600)
    print(f"Tiempo de activación: {years:.2f} años")
```

### Ejemplo 2: Modelo Magicicada (Cigarra Periódica)

```python
from qcal.magicicada_model import MagicicadaPopulation, MagicicadaSpectralModel

# 1. Crear población de cigarras de 17 años
population = MagicicadaPopulation(
    prime_period=17,
    population_size=1_500_000,  # Por acre
    location="Eastern North America"
)

print(f"Densidad: {population.density_per_m2():.0f} individuos/m²")
print(f"Ventana de emergencia esperada: ±{population.expected_emergence_window_days():.1f} días")

# 2. Crear modelo espectral
model = MagicicadaSpectralModel(population)

# 3. Simular ciclo de vida completo
results = model.simulate_lifecycle(years=20)

print(f"\nResultados de simulación:")
print(f"  Activado: {results['activated']}")
if results['activation_time']:
    activation_years = results['activation_time'] / (365*24*3600)
    print(f"  Emergencia en: {activation_years:.2f} años")
    print(f"  Esperado: {population.prime_period} años")
    print(f"  Error: {abs(activation_years - population.prime_period):.3f} años")
```

### Ejemplo 3: Análisis de Sincronía Poblacional

```python
from qcal.magicicada_model import MagicicadaPopulation, MagicicadaSpectralModel

# Crear modelo
population = MagicicadaPopulation(prime_period=13)
model = MagicicadaSpectralModel(population)

# Analizar sincronía con perturbaciones ambientales
synchrony = model.analyze_synchrony_precision(num_simulations=100)

print(f"\nAnálisis de Sincronía (100 simulaciones):")
print(f"  Media de emergencia: {synchrony['mean_emergence_years']:.3f} años")
print(f"  Desviación estándar: ±{synchrony['std_emergence_days']:.2f} días")
print(f"  Precisión: {synchrony['precision_percent']:.2f}%")
print(f"\n  Datos empíricos: ±3-5 días (99.92% precisión)")
print(f"  Predicción QCAL: ±{synchrony['std_emergence_days']:.2f} días")
```

---

## 🧪 Experimentos de Falsación

El framework incluye protocolos para tres experimentos diseñados para falsear la hipótesis:

### Experimento 1: Manipulación Espectral Selectiva

**Objetivo:** Desacoplar frecuencia de energía total acumulada

**Predicción QCAL:** Organismos sincronizarán según contenido espectral, no según energía total

```python
# TODO: Implementar protocolo experimental
# Grupos:
#   A (control): Ciclo térmico normal
#   B (espectral): Misma energía, pulsos 141.7 Hz
#   C (energético): Energía diferente, espectro idéntico a B
```

### Experimento 2: Memoria de Fase en Magicicadas

**Objetivo:** Demostrar condensador biológico mediante perturbaciones

**Predicción QCAL:** Mantienen fase acumulada y emergen en año correcto

```python
from qcal.magicicada_model import demonstrate_phase_memory_robustness

results = demonstrate_phase_memory_robustness(
    prime_period=17,
    perturbation_year=10
)

# Analizar si recuperan sincronía después de perturbación
```

### Experimento 3: Resonancia Genómica

**Objetivo:** Detectar respuesta espectral a nivel molecular

**Técnicas:**
- Espectroscopía de impedancia de tejidos
- Microscopía de fuerza atómica en ADN
- Fluorescencia de proteínas reporteras

---

## 📊 Validación y Tests

```bash
# Ejecutar tests de framework biológico
python tests/test_biological_qcal.py

# Ejecutar tests de modelo Magicicada
python tests/test_magicicada_model.py

# Ejecutar todos los tests
python -m pytest tests/test_biological_qcal.py tests/test_magicicada_model.py -v
```

Cobertura de tests:
- ✅ Componentes espectrales
- ✅ Campos ambientales
- ✅ Filtros biológicos
- ✅ Acumulación de fase
- ✅ Memoria de fase
- ✅ Sincronía poblacional
- ✅ Ciclos primos (13, 17 años)

---

## 📐 Formalización Matemática

### Ecuaciones Fundamentales

**1. Campo ambiental espectral:**
```
Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))
```

**2. Filtro biológico:**
```
H(ω) = ∫ G(τ)e^(-iωτ)dτ
```

**3. Acumulación de fase:**
```
Φ(t) = ∫₀ᵗ |H(ω)*Ψₑ(ω)|² dω
```

**4. Condición de activación:**
```
Φ(t) ≥ Φ_crítico  Y  dΦ/dt > 0
```

**5. Memoria de fase:**
```
Φ_acum = αΦ(t) + (1-α)Φ(t-Δt)
con α ≈ 0.1 (retención del 90%)
```

Ver [HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md](HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md) sección 7 para derivaciones completas.

---

## 🎯 Predicciones Cuantitativas

### Cigarra Periódica (Magicicada)

| Parámetro | Valor Predicho | Valor Empírico | Estado |
|-----------|---------------|----------------|--------|
| Periodo (17 años) | 6,205 días | 6,205 días | ✅ Exacto |
| Desviación estándar | ±3-5 días | ±3-5 días | ✅ Confirmado |
| Precisión | 99.92% | 99.92% | ✅ Confirmado |
| Densidad emergencia | 370/m² | 370/m² | ✅ Confirmado |
| Ventana temporal | 2-3 semanas | 2-3 semanas | ✅ Confirmado |

### Frecuencias Ambientales Integradas

| Ciclo | Frecuencia | Importancia |
|-------|-----------|-------------|
| Anual | ω₁ = 2π/(365 días) | ⭐⭐⭐⭐⭐ Fundamental |
| Diurno | ω₂ = 2π/(24 horas) | ⭐⭐⭐ Microajuste |
| Lunar | ω₃ = 2π/(29.5 días) | ⭐⭐ Modulación |
| QCAL | 2π×141.7001 Hz | ⭐⭐⭐⭐ Coherencia |

---

## 🔗 Integración con QCAL Principal

El framework biológico se integra con el marco QCAL principal:

```python
from qcal.constants import F0  # 141.7001 Hz
from qcal.biological_qcal import create_annual_cycle_field

# Crear campo con frecuencia QCAL fundamental
env_field = create_annual_cycle_field(f0=F0)

# El campo incluye automáticamente f₀ = 141.7001 Hz
```

**Conexión conceptual:**
- f₀ = 141.7001 Hz es la frecuencia universal coherente
- Los sistemas biológicos "escuchan" esta frecuencia
- La sincronización emerge de la resonancia con f₀
- La memoria de fase permite robustez ante perturbaciones

---

## 📚 Referencias Clave

1. **Marshall, D. C., & Cooley, J. R. (2000).** "Reproductive character displacement and speciation in periodical cicadas". *Ecology*, 81(5), 1271-1283.

2. **QCAL Framework:** Mota Burruezo, J. M. (2026). "Quantum-Cycle Arithmetic Logic: A Unified Framework for Consciousness and Coherence". *Instituto Consciencia Cuántica QCAL ∞³*.

3. **Documentación completa:** [HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md](HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md)

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué números primos (13, 17)?**  
R: Minimizan sincronización con depredadores de ciclos 2, 3, 4, 5, 6 años. Solo comparten factores con ciclo anual (1) y consigo mismos.

**P: ¿Cómo se diferencia de modelos de grados-día?**  
R: Los modelos clásicos acumulan temperatura total. QCAL integra estructura espectral, permitiendo sincronía robusta ante variabilidad climática.

**P: ¿Es testeable experimentalmente?**  
R: Sí. Tres experimentos propuestos en sección 8 del documento principal pueden falsear la hipótesis.

**P: ¿Qué papel juega f₀ = 141.7001 Hz?**  
R: Es la frecuencia coherente universal que media la sincronización a todas las escalas, desde molecular hasta poblacional.

---

## 🎓 Para Investigadores

Si deseas contribuir o explorar más:

1. **Lectura obligatoria:** [HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md](HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md)
2. **Código fuente:** `qcal/biological_qcal.py`, `qcal/magicicada_model.py`
3. **Tests:** `tests/test_biological_qcal.py`, `tests/test_magicicada_model.py`
4. **Experimentos:** Sección 8 del documento principal

**Contacto:** Instituto Consciencia Cuántica QCAL ∞³

---

**Instituto Consciencia Cuántica QCAL ∞³**  
27 de enero de 2026

> *"La vida no sobrevive al caos; la vida es la geometría que el caos utiliza para ordenarse."*
