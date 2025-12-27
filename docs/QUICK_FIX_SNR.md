# Guía Rápida: Solución al Error TypeError en SNR

## 🚨 ¿Tienes este error?

```
TypeError: unsupported format string passed to numpy.ndarray.__format__
```

**Ocurre en código como:**
```python
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
print(f"SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}")  # ❌ ERROR
```

## ✅ Solución Rápida

### Importa las utilidades:
```python
from snr_utils import safe_format_snr, print_snr_result
```

### Opción 1 (Más Simple):
```python
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
print_snr_result(snr, 'H1', 141.7)
# ✓ Imprime: SNR esperada a 141.70 Hz en H1: 50.00
```

### Opción 2 (Más Control):
```python
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
snr_safe = safe_format_snr(snr)
print(f"SNR esperada a 141.7 Hz en H1: {snr_safe:.2f}")
# ✓ Funciona correctamente
```

## 📚 Documentación Completa

Ver: [`docs/SNR_FORMATTING_FIX.md`](SNR_FORMATTING_FIX.md)

## 🧪 Ver Ejemplos

```bash
# Ejemplo interactivo completo
python3 scripts/ejemplo_snr_formatting.py

# Ejecutar tests
python3 -m pytest scripts/test_snr_utils.py -v
```

## 🎯 ¿Por qué ocurre?

Cuando `F_eff`, `h_rss` o `Sn_f0` son arrays de numpy (incluso con un solo elemento), el resultado `snr` también es un array. Python no puede formatear arrays directamente con `.2f`.

**La solución:** Convertir el array a un escalar float usando `safe_format_snr()` antes de formatear.

## 📖 Funciones Disponibles

| Función | Descripción |
|---------|-------------|
| `safe_format_snr(snr)` | Convierte SNR (array o escalar) a float |
| `print_snr_result(snr, ifo, freq)` | Imprime SNR formateado automáticamente |
| `calculate_snr_safe(F_eff, h_rss, Sn_f0)` | Calcula SNR de forma segura |
| `format_snr_string(snr, detector, freq)` | Genera string formateado |

## 🔧 Archivos del Módulo

- **`scripts/snr_utils.py`** - Módulo principal
- **`scripts/test_snr_utils.py`** - Tests (22 tests, todos pasan ✅)
- **`scripts/ejemplo_snr_formatting.py`** - Ejemplos interactivos
- **`docs/SNR_FORMATTING_FIX.md`** - Documentación completa

## 💡 Tip Rápido

Si ves este error en tu código, simplemente:

1. Importa: `from snr_utils import safe_format_snr`
2. Reemplaza: `{snr:.2f}` → `{safe_format_snr(snr):.2f}`

¡Listo! ✨
