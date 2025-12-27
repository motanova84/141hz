# Guía de Validación de Compactificación Calabi-Yau

## Descripción

Este documento describe el uso del script `validacion_compactificacion_quintica.py` que implementa la validación numérica de la Sección 5.7(f) del paper.

## Propósito

Validar computacionalmente que la jerarquía RΨ ≈ 10⁴⁷ y la frecuencia f₀ = 141.7001 Hz surgen de la compactificación sobre la quíntica en ℂP⁴.

## Uso

### Método 1: Ejecutar directamente con Python

```bash
python3 scripts/validacion_compactificacion_quintica.py
```

### Método 2: Usar el Makefile

```bash
make validacion-quintica
```

## Salida Esperada

El script produce:

1. **Código de validación**: Muestra el código tal como aparece en el paper
2. **Interpretación física**: Explica el significado de R = 10⁴⁷
3. **Cálculos correctos**: 
   - Radio físico R_Ψ ≈ 2.08 × 10⁴⁰ m
   - Frecuencia f₀ = 141.7001 Hz ✅
   - Volumen V₆ ≈ 1.01 × 10²⁴⁶ m⁶
4. **Jerarquía de escalas**: RΨ ≈ 10⁷⁵
5. **Invariantes topológicos**: h^(1,1), h^(2,1), χ
6. **Conclusión**: Validación de estructura Calabi-Yau

## Referencias

- **Paper principal**: [PAPER.md](../PAPER.md) - Sección 5.7
- **Script original**: [validacion_numerica_5_7f.py](../scripts/validacion_numerica_5_7f.py)
- **Verificación teórica**: [verificacion_teorica.py](../scripts/verificacion_teorica.py)
