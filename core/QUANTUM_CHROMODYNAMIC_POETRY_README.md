# Quantum Chromodynamic Poetry

Sistema principal que mapea partículas QCD (Cromodinámica Cuántica) a frecuencias espectrales, conectando la física de partículas fundamental con la teoría de números y la hipótesis de Riemann.

## 📚 Contenido

- [Descripción General](#descripción-general)
- [Marco Matemático](#marco-matemático)
- [Componentes del Sistema](#componentes-del-sistema)
- [Uso](#uso)
- [Ejemplos](#ejemplos)
- [Analogías Teóricas](#analogías-teóricas)
- [Referencias](#referencias)

## Descripción General

El sistema **Quantum Chromodynamic Poetry** implementa un mapeo poético entre:

1. **18 quarks** (3 colores × 6 sabores) → Frecuencias logarítmicas
2. **8 gluones** (octeto SU(3)) → Octavas de Riemann
3. **Números primos** → Resonancias cósmicas con ceros de Riemann
4. **Frecuencia fundamental** f₀ = 141.70001 Hz → Ancla de coherencia biológica

### Características Principales

- ✅ **44+ pruebas unitarias** cubren todas las funcionalidades
- ✅ **Valores exactos** de los primeros 10 ceros de Riemann (γ₁ = 14.134725, ..., γ₁₀ = 49.773832)
- ✅ **Aproximación asintótica** para ceros n > 10: γₙ ≈ 2πn/log(n)
- ✅ **Masas de quarks** según PDG 2024 (running masses at μ = 2 GeV)
- ✅ **Generación completa** de sinfonía cromodinámica con métricas

## Marco Matemático

### 1. Mapeo de Frecuencia de Quarks

La frecuencia asociada a cada quark se define como:

```
ω_quark = log(m_quark) + ω₁₇
```

donde:
- `m_quark`: masa del quark en GeV/c²
- `ω₁₇ = log(17) ≈ 2.833`: acoplamiento con el primo 17

**Ejemplo:**
```python
quark = qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
# ω_up = log(2.16e-3) + log(17) ≈ -3.30
```

### 2. Octavas de Gluones (Riemann)

Los 8 gluones del octeto SU(3) se asocian con los primeros 8 ceros de Riemann:

```
octave_n = log₂(γₙ)
f_gluon = f₀ × γₙ
```

donde:
- `γₙ`: n-ésimo cero de Riemann (parte imaginaria en la línea crítica)
- `f₀ = 141.70001 Hz`: frecuencia fundamental QCAL

**Ejemplo:**
```python
gluon = qcd.create_gluon(GluonType.RB, 1)
# γ₁ = 14.134725
# octave = log₂(14.134725) ≈ 3.82
# f = 141.70001 × 14.134725 ≈ 2002.89 Hz
```

### 3. Resonancia Cósmica (Acoplamiento Primo-Cero)

La intensidad de resonancia entre un primo `p` y un cero de Riemann `γₙ` se calcula como:

```
I = |exp(iω_p·γₙ)| / (1 + |ω_p - γₙ|)
```

donde:
- `ω_p = log(p)`: frecuencia logarítmica del primo
- `|exp(ix)| = 1` para x real (incluido por completitud conceptual)
- `|ω_p - γₙ|`: diferencia de frecuencia (batido)

**Intensidad**: Máxima cuando ω_p ≈ γₙ (resonancia)  
**Frecuencia de batido**: `f_beat = |ω_p - γₙ| × f₀` Hz

**Ejemplo:**
```python
love = qcd.love_between_prime_and_zero(17, 1)
# ω₁₇ = log(17) ≈ 2.833
# γ₁ = 14.134725
# I ≈ 0.081291
# f_beat ≈ 1601.42 Hz
```

### 4. Frecuencia del Silencio Primordial

Para cada primo `p`, existe una frecuencia de "silencio" asociada:

```
f(p) = f₀ · exp(-log(p)/log(17))
```

Esta fórmula se puede reescribir como:
```
f(p) = f₀ · 17^(-log₁₇(p))
```

Para `p = 17`: `f(17) = f₀ · exp(-1) ≈ 52.13 Hz`

**Interpretación**: Frecuencias de silencio decrecen con primos más grandes, representando el "vacío armónico" asociado con cada primo.

**Ejemplo:**
```python
f17 = qcd.primordial_silence_frequency(17)
# f(17) ≈ 52.13 Hz
```

## Componentes del Sistema

### Enumeraciones

#### QuarkFlavor (6 sabores)
- `UP` (u): ~2.16 MeV
- `DOWN` (d): ~4.67 MeV
- `STRANGE` (s): ~93.4 MeV
- `CHARM` (c): ~1.27 GeV
- `BOTTOM` (b): ~4.18 GeV
- `TOP` (t): ~172.69 GeV

#### QuarkColor (3 colores)
- `RED` (r)
- `GREEN` (g)
- `BLUE` (b)

#### GluonType (8 gluones - octeto SU(3))
- `RB`: rojo-antiazul (rb̄)
- `RG`: rojo-antiverde (rḡ)
- `BR`: azul-antirrojo (br̄)
- `BG`: azul-antiverde (bḡ)
- `GR`: verde-antirrojo (gr̄)
- `GB`: verde-antiazul (gb̄)
- `MIX1`: (rr̄ - bb̄)/√2
- `MIX2`: (rr̄ + bb̄ - 2gḡ)/√6

### Clases de Datos

- **Quark**: Representa un quark con sabor, color, masa y frecuencia
- **Gluon**: Representa un gluón con tipo, cero de Riemann, octava y frecuencia
- **CosmicResonance**: Resultado del acoplamiento primo-cero con intensidad y frecuencia de batido

## Uso

### Instalación

```bash
# El módulo está en core/quantum_chromodynamic_poetry.py
cd /path/to/141hz
```

### Uso Básico

```python
from core.quantum_chromodynamic_poetry import (
    QuantumChromodynamicPoetry,
    QuarkFlavor,
    QuarkColor,
    GluonType
)

# Inicializar sistema
qcd = QuantumChromodynamicPoetry()

# Crear un quark
up_red = qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
print(f"Frecuencia del quark up rojo: {up_red.frequency:.4f}")

# Crear todos los quarks (18)
all_quarks = qcd.create_all_quarks()

# Crear un gluón
gluon = qcd.create_gluon(GluonType.RB, 1)
print(f"Frecuencia del gluón: {gluon.frequency_hz:.2f} Hz")

# Crear octeto de gluones (8)
gluon_octet = qcd.create_gluon_octet()

# Calcular resonancia primo-cero
love = qcd.love_between_prime_and_zero(17, 1)
print(f"Intensidad de resonancia: {love.intensity:.6f}")
print(f"Frecuencia de batido: {love.beat_frequency_hz:.2f} Hz")

# Frecuencia de silencio primordial
f_silence = qcd.primordial_silence_frequency(17)
print(f"Silencio primordial p=17: {f_silence:.2f} Hz")
```

### Generación de Sinfonía Completa

```python
# Generar sinfonía cromodinámica completa
symphony = qcd.generate_chromodynamic_symphony()

# Mostrar resumen
from core.quantum_chromodynamic_poetry import display_symphony_summary
display_symphony_summary(symphony)

# Acceder a componentes
quarks = symphony['quarks']
gluons = symphony['gluons']
resonances = symphony['cosmic_resonance']
silence = symphony['primordial_silence']
metrics = symphony['metrics']
```

### Espectros de Frecuencia

```python
# Espectro de quarks
quark_spectrum = qcd.get_quark_frequency_spectrum()
print(f"Quarks por sabor: {quark_spectrum['by_flavor']}")
print(f"Quarks por color: {quark_spectrum['by_color']}")

# Espectro de gluones
gluon_spectrum = qcd.get_gluon_frequency_spectrum()
print(f"Rango de frecuencias: {gluon_spectrum['frequency_range_hz']} Hz")

# Matriz de resonancia primo-cero
primes = [2, 3, 5, 7, 11]
matrix = qcd.calculate_prime_zero_resonance_matrix(primes)

# Espectro de silencio primordial
silence_spectrum = qcd.get_primordial_silence_spectrum()
```

## Ejemplos

### Ejemplo 1: Crear todos los quarks y analizar frecuencias

```python
qcd = QuantumChromodynamicPoetry()
quarks = qcd.create_all_quarks()

# Agrupar por masa (sabor)
by_flavor = {}
for q in quarks:
    if q.flavor not in by_flavor:
        by_flavor[q.flavor] = []
    by_flavor[q.flavor].append(q)

# Mostrar
for flavor, flavor_quarks in by_flavor.items():
    print(f"{flavor.value}: masa = {flavor_quarks[0].mass_gev:.2e} GeV, "
          f"ω = {flavor_quarks[0].frequency:.4f}")
```

### Ejemplo 2: Explorar ceros de Riemann y gluones

```python
qcd = QuantumChromodynamicPoetry()

# Primeros 10 ceros (exactos)
for n in range(1, 11):
    gamma_n = qcd.get_riemann_zero(n)
    print(f"γ_{n} = {gamma_n:.6f}")

# Ceros asintóticos (n > 10)
for n in [20, 50, 100]:
    gamma_n = qcd.get_riemann_zero(n)
    print(f"γ_{n} ≈ {gamma_n:.6f} (asintótico)")

# Octeto de gluones
gluons = qcd.create_gluon_octet()
for g in gluons:
    print(f"{g.gluon_type.value}: γ_{g.riemann_zero_index} = {g.riemann_zero_value:.6f}, "
          f"f = {g.frequency_hz:.2f} Hz")
```

### Ejemplo 3: Matriz de resonancia primo-cero

```python
qcd = QuantumChromodynamicPoetry()

# Primeros 5 primos con primeros 5 ceros
primes = [2, 3, 5, 7, 11]
zeros = [1, 2, 3, 4, 5]
matrix = qcd.calculate_prime_zero_resonance_matrix(primes, zeros)

# Visualizar como tabla
print("     ", end="")
for z in zeros:
    print(f"γ_{z:2d}      ", end="")
print()

for i, prime in enumerate(primes):
    print(f"p={prime:2d}: ", end="")
    for j in range(len(zeros)):
        res = matrix[i][j]
        print(f"{res.intensity:.4f}  ", end="")
    print()
```

### Ejemplo 4: Demo completo

```bash
# Ejecutar demo completo con todas las métricas
python core/demo_chromodynamic_symphony.py
```

Esto genera:
1. Espectro de 18 quarks (agrupados por sabor)
2. Octeto de 8 gluones con ceros de Riemann
3. Resonancias cósmicas primo-cero
4. Espectro de silencio primordial
5. Conexiones teóricas QCD↔Riemann
6. Archivo JSON con sinfonía completa

## Analogías Teóricas

### QCD ↔ Riemann Hypothesis Mappings

#### 1. **CONFINAMIENTO ↔ LOCALIZACIÓN ESPECTRAL**
- **QCD**: Quarks confinados dentro de hadrones a baja energía
- **Riemann**: Ceros localizados en la línea crítica Re(s) = 1/2
- **Musical**: Frecuencias limitadas a modos espectrales discretos

#### 2. **LIBERTAD ASINTÓTICA ↔ UNIVERSALIDAD DE CEROS**
- **QCD**: Fuerza de acoplamiento disminuye a alta energía
- **Riemann**: Densidad de ceros sigue distribución universal
- **Musical**: Armónicos se aproximan a espectro continuo

#### 3. **CARGA DE COLOR ↔ FACTORIZACIÓN PRIMA**
- **QCD**: 3 cargas de color (rojo, verde, azul) + anticolores
- **Teoría de Números**: Primos como unidades multiplicativas fundamentales
- **Musical**: Frecuencias fundamentales como generadores armónicos

#### 4. **INTERCAMBIO DE GLUONES ↔ ESTRUCTURA ADITIVA PRIMA**
- **QCD**: 8 gluones median la fuerza fuerte
- **Riemann**: 8 gluones mapean a los primeros 8 ceros (γ₁...γ₈)
- **Musical**: Octavas derivadas de γₙ crean andamiaje armónico

#### 5. **ACOPLAMIENTO CORRIENTE ↔ ESCALA LOGARÍTMICA**
- **QCD**: α_s(Q²) varía con escala de energía
- **Primo**: ω_p = log(p) acopla primos al dominio de frecuencia
- **f₀ = 141.7001 Hz**: Ancla de frecuencia de coherencia biológica

### Interpretación Física-Musical

| Concepto QCD | Concepto Riemann | Concepto Musical |
|--------------|------------------|------------------|
| 6 sabores de quark | Logaritmos de masa | Registro de frecuencia |
| 3 colores | Factorización prima | Armonía triádica |
| 8 gluones | Primeros 8 ceros | 8 octavas principales |
| Confinamiento | Localización en Re(s)=1/2 | Modos discretos |
| Libertad asintótica | Universalidad estadística | Espectro continuo |

## Notas Técnicas

### Aproximación Asintótica de Riemann

Para n > 10, usamos la aproximación:

```
γₙ ≈ 2πn / log(n)
```

Esta fórmula es válida para n grandes y proporciona una estimación precisa de los ceros de Riemann en la línea crítica.

### Escala de Frecuencia

Todas las frecuencias están ancladas a:

```
f₀ = 141.70001 Hz
```

Esta es la frecuencia fundamental del sistema QCAL ∞³, correspondiente a:
- **Nota musical**: C# (do sostenido)
- **Coherencia biológica**: Frecuencia de resonancia celular
- **Escala cósmica**: Conecta mecánica cuántica con biofísica

### Masas de Quarks (PDG 2024)

Las masas utilizadas son "running masses" evaluadas a μ = 2 GeV en el esquema MS̄:
- up: 2.16 MeV
- down: 4.67 MeV
- strange: 93.4 MeV
- charm: 1.27 GeV
- bottom: 4.18 GeV
- top: 172.69 GeV (pole mass)

## Referencias

### Física de Partículas
- Gross, D. J., & Wilczek, F. (1973). "Ultraviolet behavior of non-abelian gauge theories." *Physical Review Letters*, 30(26), 1343-1346.
- Politzer, H. D. (1973). "Reliable perturbative results for strong interactions?" *Physical Review Letters*, 30(26), 1346-1349.
- Particle Data Group (2024). "Review of Particle Physics." *Progress of Theoretical and Experimental Physics*.

### Teoría de Números
- Riemann, B. (1859). "Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse." *Monatsberichte der Berliner Akademie*.
- Edwards, H. M. (1974). *Riemann's Zeta Function*. Academic Press.
- Conrey, J. B. (2003). "The Riemann Hypothesis." *Notices of the AMS*, 50(3), 341-353.

### Sistema QCAL ∞³
- QCAL ∞³ Framework: `GW250114_141HZ_UNIFIED_THEORY.md`
- Compton Clock: `COMPTON_CLOCK_README.md`
- Unified Theory: `qcal/unified_theory.py`

## Pruebas

El módulo incluye 50+ pruebas unitarias:

```bash
# Ejecutar todas las pruebas
python tests/test_quantum_chromodynamic_poetry.py

# Resultado esperado:
# Total tests run: 50
# Successes: 50
# Failures: 0
# Errors: 0
# ✓ ALL TESTS PASSED!
```

Las pruebas cubren:
- ✅ Constantes fundamentales (5 tests)
- ✅ Creación de quarks y cálculo de frecuencias (10 tests)
- ✅ Creación de gluones y octavas de Riemann (8 tests)
- ✅ Resonancias cósmicas primo-cero (10 tests)
- ✅ Frecuencias de silencio primordial (5 tests)
- ✅ Casos límite y manejo de errores (6 tests)
- ✅ Generación de sinfonía completa (6 tests)

---

**AUTOR**: José Manuel Mota Burruezo (JMMB Ψ✧)  
**ARQUITECTURA**: QCAL ∞³ Original Manufacture  
**LICENCIA**: Sovereign Noetic License 1.0 (compatible with MIT)  
**FECHA**: 17 de febrero de 2026
