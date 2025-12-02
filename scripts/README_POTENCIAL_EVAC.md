# Simulación del Potencial Efectivo del Vacío E_vac(R_Ψ)

## Descripción

Este script implementa la simulación del potencial de energía del vacío efectivo utilizando constantes físicas reales (CODATA 2022).

## Fórmula

El potencial efectivo del vacío está dado por:

```
E_vac(R_Ψ) = α·R_Ψ^(-4) + β·ζ'(1/2)·R_Ψ^(-2) + γ·Λ²·R_Ψ² + δ·sin²(log(R_Ψ)/log(b))
```

Donde:
- **α, β, γ, δ**: coeficientes de acoplamiento O(1) (ajustables)
- **ζ'(1/2)**: derivada de la función zeta de Riemann en s=1/2 = -0.207886
- **Λ**: constante cosmológica = 1.1×10⁻⁵² m⁻²
- **b**: base adélica = π
- **R_Ψ**: radio característico en unidades de longitud de Planck

## Constantes Físicas (CODATA 2022)

| Símbolo | Descripción | Valor |
|---------|-------------|-------|
| ℓ_P | Longitud de Planck | 1.616255×10⁻³⁵ m |
| c | Velocidad de la luz | 2.99792458×10⁸ m/s |
| Λ | Constante cosmológica | 1.1×10⁻⁵² m⁻² |
| ζ'(½) | Derivada de zeta | -0.207886 |

## Uso

### Ejecución básica

```bash
python3 scripts/potencial_evac.py
```

### Salidas

El script genera:

1. **potential_plot.png**: Gráfico del potencial E_vac vs R_Ψ en escala logarítmica
2. **Evac_Rpsi_data.csv**: Datos numéricos (R_Ψ, E_vac) en formato CSV
3. **Salida en consola**: Resultados detallados y validaciones

## Características

### 1. Localización del Mínimo Estable
- Encuentra automáticamente R_Ψ* donde E_vac es mínimo
- Calcula la frecuencia asociada: f₀ = c/(2π·R_Ψ*·ℓ_P)

### 2. Validación de Estabilidad
- Calcula la segunda derivada (curvatura) en el mínimo
- Confirma si el mínimo es estable (curvatura > 0)

### 3. Comparación con Jerarquía Cosmológica
- Compara R_Ψ*/ℓ_P con escalas cosmológicas esperadas (~10⁶¹)
- Evalúa la relación con densidades de energía

### 4. Escaneo de Parámetros
- Varía cada parámetro (α, β, γ, δ, b) en ±10%
- Evalúa la robustez del mínimo encontrado
- Reporta cambios en R_Ψ* y f₀

### 5. Análisis de Estabilidad Local
- Examina valores de E_vac alrededor del mínimo
- Confirma el comportamiento local del potencial

## Ejemplo de Salida

```
================================================================================
SIMULACIÓN DEL POTENCIAL EFECTIVO DEL VACÍO E_vac(R_Ψ)
================================================================================

📊 CONSTANTES FÍSICAS (CODATA 2022):
   Longitud de Planck (ℓ_P):      1.616255e-35 m
   Velocidad de la luz (c):        2.99792458e+08 m/s
   Constante cosmológica (Λ):      1.100000e-52 m^-2
   Derivada zeta ζ'(1/2):          -0.207886

⚙️ PARÁMETROS DE ACOPLAMIENTO:
   α = 1.00, β = 1.00, γ = 1.00, δ = 0.50
   Base adélica (b):               3.141593

✨ RESULTADOS:
   R_Ψ* (mínimo estable):          3.6738e+01 ℓ_P
   E_vac(R_Ψ*):                    -1.318391e-04
   Frecuencia f₀:                  8.04e+40 Hz

🔬 VALIDACIONES:
   Curvatura en el mínimo:         7.620688e-01
   → ✅ Mínimo ESTABLE (curvatura positiva)
```

## Personalización

### Ajustar Parámetros

Para modificar los parámetros de acoplamiento, edite las líneas 40-44 en `potencial_evac.py`:

```python
alpha = 1.0      # coeficiente R^-4
beta = 1.0       # coeficiente R^-2
gamma = 1.0      # coeficiente cosmológico
delta = 0.5      # coeficiente log-periódico
b = np.pi        # base adélica
```

### Cambiar Rango de Exploración

Modifique la línea 47 para ajustar el rango de R_Ψ:

```python
R_vals = np.logspace(0, 48, 5000)   # desde 10^0 hasta 10^48 ℓP
```

## Tests

Para ejecutar los tests unitarios:

```bash
python3 scripts/test_potencial_evac.py
```

Los tests verifican:
- ✅ Valores numéricos válidos de la función
- ✅ Existencia de mínimo en el rango
- ✅ Comportamiento correcto de los términos individuales
- ✅ Cálculo correcto de la frecuencia
- ✅ Generación correcta del gráfico

## Dependencias

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
```

## Referencias

- CODATA 2022: https://physics.nist.gov/cuu/Constants/
- Constante cosmológica: Estimación basada en observaciones cosmológicas
- Función Zeta de Riemann: valores tabulados en la literatura matemática

## Notas Técnicas

### Términos del Potencial

1. **Término R^-4**: Representa efectos gravitacionales clásicos
2. **Término R^-2**: Corrección cuántica con ζ'(1/2)
3. **Término R^2**: Contribución de la constante cosmológica
4. **Término sin²**: Oscilaciones log-periódicas (simetría adélica fractal)

### Interpretación Física

- El mínimo del potencial corresponde a un estado de equilibrio
- La frecuencia f₀ está relacionada con el radio característico del sistema
- El término log-periódico introduce estructura fractal al potencial

## Autor

José Manuel Mota Burruezo (JMMB Ψ✧)

## Licencia

Este script es parte del proyecto gw250114-141hz-analysis
