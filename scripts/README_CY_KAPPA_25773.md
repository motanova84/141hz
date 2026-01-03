# Generador de Variedades Calabi-Yau (h11 + h21 = 13)

Este directorio contiene un script para generar variedades Calabi-Yau con la restricción `h^{1,1} + h^{2,1} = 13`.

## Archivos

- **generar_cy_kappa_25773.py**: Script principal que genera las variedades CY
- **test_generar_cy_kappa_25773.py**: Suite de tests completa (13 tests)

## Uso

```bash
# Generar el archivo JSON
python scripts/generar_cy_kappa_25773.py

# Ejecutar tests
python scripts/test_generar_cy_kappa_25773.py -v
```

## Salida

El script genera el archivo `data/cy_kappa_25773_log13.json` con 12 variedades Calabi-Yau donde:

- `h^{1,1} + h^{2,1} = 13`
- `χ = 2(h^{1,1} - h^{2,1})` (Característica de Euler)
- `κ_Π = log(13) ≈ 2.564949` (Invariante espectral)

## Ejemplo de Salida

```json
{
  "ID": "CY_6_7",
  "h11": 6,
  "h21": 7,
  "chi_Euler": -2,
  "kappa_pi": 2.564949
}
```

## Variedades Generadas

| ID | h^{1,1} | h^{2,1} | χ | κ_Π |
|----|---------|---------|---|-----|
| CY_1_12 | 1 | 12 | -22 | 2.564949 |
| CY_2_11 | 2 | 11 | -18 | 2.564949 |
| CY_3_10 | 3 | 10 | -14 | 2.564949 |
| CY_4_9 | 4 | 9 | -10 | 2.564949 |
| CY_5_8 | 5 | 8 | -6 | 2.564949 |
| CY_6_7 | 6 | 7 | -2 | 2.564949 |
| CY_7_6 | 7 | 6 | 2 | 2.564949 |
| CY_8_5 | 8 | 5 | 6 | 2.564949 |
| CY_9_4 | 9 | 4 | 10 | 2.564949 |
| CY_10_3 | 10 | 3 | 14 | 2.564949 |
| CY_11_2 | 11 | 2 | 18 | 2.564949 |
| CY_12_1 | 12 | 1 | 22 | 2.564949 |

## Notas

- Todas las variedades tienen el mismo `κ_Π` ya que todas satisfacen `h^{1,1} + h^{2,1} = 13`
- El valor `κ_Π = log(13)` conecta estas variedades con propiedades espectrales universales
- Los números de Hodge van de 1 a 12 para cada variedad
