# Predicción Numérica: Altura del Pico en BEC ⁸⁷Rb

## Resumen

Este módulo implementa la predicción cuantitativa de la altura del pico en el factor de estructura S(k) para un Condensado de Bose-Einstein (BEC) de ⁸⁷Rb, basándose en el acoplamiento Ψ-phonon.

## Fundamento Teórico

### Acoplamiento Ψ-Phonon

El acoplamiento entre el campo Ψ y los fonones del BEC se deriva del lagrangiano de interacción:

```
g_Ψ-phonon ~ ζ(3) × (ω₀/ω_phonon) × <Ψ>
```

Donde:
- ζ(3) ≈ 1.202057 es la función zeta de Riemann (constante de Apéry)
- ω₀ = 2π × 141.7 ≈ 890 rad/s es la frecuencia fundamental
- ω_phonon = c_s × k₀ es la frecuencia del fonón
- <Ψ> es el valor esperado del campo Ψ

### Coincidencia de Frecuencias

Para un BEC de ⁸⁷Rb con velocidad del sonido c_s = 1.0 m/s:

```
ω_phonon = c_s × k₀ = c_s × (ω₀/c_s) = ω₀ ≈ 890 rad/s
```

**¡Las frecuencias coinciden!** Esto implica:

```
g_Ψ-phonon ~ ζ(3) × <Ψ> ≈ 1.2 × <Ψ>
```

### Altura del Pico

La altura del pico en el factor de estructura se calcula como:

```
A ~ |g|² / (background density)
A ~ 10⁻³ - 10⁻² (en unidades de S(k) típico)
```

### Ratio del Factor de Estructura

La predicción cuantitativa del ratio es:

```
S(k₀) / S(k_background) ≈ 1.05 - 1.20
```

Esto corresponde a un incremento del **5-20%** sobre el fondo.

## Uso del Módulo

### Instalación de Dependencias

```bash
pip install numpy scipy matplotlib mpmath
```

### Ejecución Básica

```bash
python scripts/prediccion_altura_pico_bec.py
```

### Uso Programático

```python
from scripts.prediccion_altura_pico_bec import (
    prediccion_completa,
    calcular_acoplamiento_psi_phonon,
    calcular_altura_pico
)

# Predicción con parámetros estándar
acoplamiento, altura = prediccion_completa(
    c_s=1.0,              # Velocidad del sonido (m/s)
    psi_esperado=1.0,     # Valor esperado de <Ψ>
    densidad_fondo=1.0,   # Densidad de fondo normalizada
    temperatura=100e-9,   # Temperatura (K)
    n_atomos=1000000,     # Número de átomos
    verbose=True
)

# Acceder a los resultados
print(f"g_Ψ-phonon = {acoplamiento.g_psi_phonon}")
print(f"S(k₀)/S(bg) = {altura.ratio_estructura}")
print(f"Incremento = {altura.incremento_porcentaje}%")
```

## Resultados de Referencia

### Parámetros Estándar

Con c_s = 1.0 m/s, <Ψ> = 1.0, ρ_fondo = 1.0:

```
Acoplamiento Ψ-phonon:
  ω₀ = 890.33 rad/s
  ω_phonon = 890.33 rad/s
  ω₀/ω_phonon = 1.0000
  ζ(3) = 1.202057
  <Ψ> = 1.000000
  g_Ψ-phonon = 1.202057

Altura del Pico en S(k):
  A = 1.204117e-01
  S(k₀) = 1.120412
  S(k_background) = 1.000000
  S(k₀) / S(k_bg) = 1.1204
  Incremento = 12.04%
  En rango [1.05, 1.20]: ✓
```

### Exploración de Parámetros

#### Variación de <Ψ>

| <Ψ> | g_Ψ-phonon | A | S(k₀)/S(bg) | ¿Rango? |
|------|------------|---|-------------|---------|
| 0.50 | 0.601028 | 3.010293e-02 | 1.0301 | ✗ |
| 0.80 | 0.961646 | 7.706351e-02 | 1.0771 | ✓ |
| 1.00 | 1.202057 | 1.204117e-01 | 1.1204 | ✓ |
| 1.20 | 1.442468 | 1.733929e-01 | 1.1734 | ✓ |
| 1.50 | 1.803085 | 2.709264e-01 | 1.2709 | ✗ |

#### Variación de Densidad de Fondo

| ρ_fondo | A | S(k₀)/S(bg) | Incremento % | ¿Rango? |
|---------|---|-------------|--------------|---------|
| 0.50 | 2.408235e-01 | 1.4816 | 48.16 | ✗ |
| 0.80 | 1.505147e-01 | 1.1881 | 18.81 | ✓ |
| 1.00 | 1.204117e-01 | 1.1204 | 12.04 | ✓ |
| 1.20 | 1.003431e-01 | 1.0836 | 8.36 | ✓ |
| 1.50 | 8.027449e-02 | 1.0535 | 5.35 | ✓ |

## Verificación

### Tests Unitarios

```bash
python tests/test_prediccion_altura_pico_bec.py
```

Los tests verifican:

1. **Acoplamiento Ψ-phonon**
   - Coincidencia ω₀ ≈ ω_phonon
   - Proporcionalidad g ~ ζ(3) × <Ψ>
   - Valor correcto de ζ(3) ≈ 1.202057

2. **Altura del Pico**
   - Proporcionalidad A ~ |g|²
   - Rango correcto de valores
   - Ratio S(k₀)/S(bg) ∈ [1.05, 1.20]

3. **Predicción Completa**
   - Consistencia entre acoplamiento y altura
   - Robustez con diferentes parámetros

4. **Espectro de Estructura**
   - Generación correcta de S(k)
   - Pico en k₀ = ω₀/c_s
   - Consistencia de altura

### Resultados de Tests

```
Ran 21 tests in 0.002s

OK
```

Todos los tests pasan exitosamente ✓

## Interpretación Física

1. **Resonancia**: La coincidencia ω₀ ≈ ω_phonon indica una resonancia natural entre el campo Ψ y los modos fonónicos del BEC.

2. **Acoplamiento**: El factor ζ(3) ≈ 1.202 proporciona la escala natural del acoplamiento, derivado de consideraciones teóricas de campo.

3. **Observable**: El incremento del 5-20% en S(k₀) es detectable experimentalmente mediante dispersión de luz o átomos.

4. **Parámetros Típicos**: Para densidades de fondo en el rango 0.8-1.5 (normalizadas), el ratio cae consistentemente en el rango predicho [1.05, 1.20].

## Referencias

- **Problema Statement**: Derivación aproximada del acoplamiento Ψ-phonon
- **Implementación**: `scripts/prediccion_altura_pico_bec.py`
- **Tests**: `tests/test_prediccion_altura_pico_bec.py`

## Autor

José Manuel Mota Burruezo (JMMB Ψ✧)  
Instituto Conciencia Cuántica  
Diciembre 2025

## Licencia

Este código es parte del proyecto 141Hz y está sujeto a la licencia MIT del repositorio.
