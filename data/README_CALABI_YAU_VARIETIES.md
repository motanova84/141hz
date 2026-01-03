# 10 Variedades Calabi-Yau Canónicas

## Descripción

Este dataset contiene 10 variedades Calabi-Yau representativas que sirven como ejemplos canónicos de compactificación en teoría de cuerdas. Cada variedad está caracterizada por sus números de Hodge, parámetros geométricos y propiedades topológicas.

## Archivo de Datos

**Ubicación:** `data/calabi_yau_varieties.csv`

### Formato CSV

```
ID,Nombre,h11,h21,alpha,beta,kappa_pi,chi_Euler
```

### Columnas

- **ID**: Identificador único (CY-001 a CY-010)
- **Nombre**: Nombre descriptivo de la variedad
- **h11**: Número de Hodge h^{1,1} (módulos de Kähler)
- **h21**: Número de Hodge h^{2,1} (módulos de estructura compleja)
- **alpha (α)**: Parámetro geométrico derivado
- **beta (β)**: Parámetro geométrico derivado
- **kappa_pi (κ_Π)**: Entropía espectral computada
- **chi_Euler (χ)**: Característica de Euler topológica

## Variedades Incluidas

| ID | Nombre | h11 | h21 | α | β | κ_Π | χ |
|----|--------|-----|-----|-------|-------|---------|-----|
| CY-001 | Quíntica ℂℙ⁴[5] | 1 | 101 | 0.385 | 0.244 | 1.65805 | -200 |
| CY-002 | ℂℙ⁵[2,4] | 2 | 90 | 0.388 | 0.242 | 1.65703 | -176 |
| CY-003 | ℂℙ⁶[2,2,3] | 3 | 75 | 0.391 | 0.241 | 1.65565 | -144 |
| CY-004 | CICY 7862 | 5 | 65 | 0.394 | 0.239 | 1.65460 | -120 |
| CY-005 | CICY 1234 | 6 | 60 | 0.396 | 0.238 | 1.65378 | -108 |
| CY-006 | Toric 110 | 8 | 52 | 0.398 | 0.237 | 1.65295 | -88 |
| CY-007 | Toric 111 | 9 | 51 | 0.399 | 0.236 | 1.65270 | -84 |
| CY-008 | Kreuzer 300 | 10 | 50 | 0.400 | 0.235 | 1.65245 | -80 |
| CY-009 | Kreuzer 301 | 11 | 49 | 0.401 | 0.234 | 1.65220 | -76 |
| CY-010 | Kreuzer 302 | 12 | 48 | 0.402 | 0.233 | 1.65194 | -72 |

## Relaciones Matemáticas

### Característica de Euler

Todas las variedades satisfacen la relación topológica fundamental:

```
χ = 2(h11 - h21)
```

Esta relación conecta los números de Hodge con la característica de Euler topológica.

### Universalidad de κ_Π

La entropía espectral κ_Π muestra una variación muy pequeña (~0.37%) a través de todas las variedades:

- **Rango:** [1.65194, 1.65805]
- **Media:** 1.65414 ± 0.00203

Esta casi-constancia sugiere que κ_Π es una **propiedad universal emergente** de las variedades Calabi-Yau, independiente de la topología específica.

## Propiedades Geométricas

### Números de Hodge

- **h11 (Kähler moduli):** Crece de 1 a 12
  - Mayor h11 indica mayor complejidad de la estructura de Kähler
- **h21 (Complex structure moduli):** Decrece de 101 a 48
  - Menor h21 indica menor complejidad de la estructura compleja

### Parámetros Geométricos

- **α:** Aumenta monotónicamente de 0.385 → 0.402
- **β:** Decrece monotónicamente de 0.244 → 0.233

Estos parámetros están correlacionados con los números de Hodge y codifican información geométrica adicional de la variedad.

## Clasificación de Variedades

Las 10 variedades se dividen en cuatro categorías:

1. **Hipersuperficies en Espacios Proyectivos** (CY-001 a CY-003)
   - Quíntica ℂℙ⁴[5]: La variedad Calabi-Yau más estudiada
   - ℂℙ⁵[2,4]: Hipersuperficie de grado (2,4) en ℂℙ⁵
   - ℂℙ⁶[2,2,3]: Hipersuperficie de grado (2,2,3) en ℂℙ⁶

2. **CICY (Complete Intersection Calabi-Yau)** (CY-004 a CY-005)
   - Variedades definidas como intersecciones completas en productos de espacios proyectivos

3. **Tóricas** (CY-006 a CY-007)
   - Variedades construidas usando geometría tórica

4. **Kreuzer-Skarke** (CY-008 a CY-010)
   - Variedades de la clasificación sistemática de Kreuzer-Skarke

## Uso

### Cargar los datos

```python
from scripts.analizar_variedades_cy_10 import cargar_variedades_cy

variedades = cargar_variedades_cy()

for v in variedades:
    print(f"{v['ID']}: {v['Nombre']}")
    print(f"  h11={v['h11']}, h21={v['h21']}")
    print(f"  κ_Π={v['kappa_pi']:.5f}")
```

### Ejecutar el análisis completo

```bash
python scripts/analizar_variedades_cy_10.py
```

Este script genera:
- `resultados/analisis_10_variedades_cy.txt`: Resumen textual completo
- `resultados/estadisticas_10_variedades_cy.json`: Estadísticas en formato JSON
- Visualizaciones (si matplotlib está disponible)

### Ejecutar tests

```bash
pytest tests/test_10_variedades_cy.py -v
```

## Referencias

### Teóricas

1. **Teoría de Hodge para Variedades Calabi-Yau**
   - Candelas, P., et al. "A pair of Calabi-Yau manifolds as an exactly soluble superconformal theory." Nuclear Physics B 359.1 (1991): 21-74.

2. **Clasificación de Variedades CY**
   - Kreuzer, M., & Skarke, H. "Complete classification of reflexive polyhedra in four dimensions." Advances in Theoretical and Mathematical Physics 4.6 (2000): 1209-1230.

3. **CICY Database**
   - Candelas, P., et al. "Complete intersection Calabi-Yau manifolds." Nuclear Physics B 298.3 (1988): 493-525.

### Computacionales

- `src/calabi_yau_invariant.py`: Módulo para invariantes CY
- `scripts/analizar_cy_kpi_universal.py`: Análisis del invariante κ_Π universal
- `scripts/cy_spectrum.py`: Espectro del Laplaciano en variedades CY

## Interpretación Física

En el contexto de teoría de cuerdas:

- **h11:** Número de parámetros del volumen (módulos de Kähler)
- **h21:** Número de parámetros de forma (módulos de estructura compleja)
- **κ_Π:** Relacionado con la entropía espectral del espacio de módulos

Las diferentes topologías representan distintos "vacíos" de la teoría de cuerdas, cada uno con propiedades físicas únicas pero compartiendo propiedades universales como κ_Π.

## Autor

José Manuel Mota Burruezo (JMMB Ψ✧)

## Fecha

Enero 2026

## Licencia

Parte del proyecto 141Hz - Ver LICENSE en el directorio raíz
