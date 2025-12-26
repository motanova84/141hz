# Solución al Error TypeError en Formateo de SNR

## 📋 Problema

Al calcular el Signal-to-Noise Ratio (SNR) en análisis de ondas gravitacionales, es común encontrar el siguiente error:

```python
TypeError: unsupported format string passed to numpy.ndarray.__format__
```

Este error ocurre cuando se intenta formatear un array de numpy directamente con una especificación de formato como `.2f`:

```python
# ❌ CÓDIGO PROBLEMÁTICO
F_eff = np.array([0.5])
h_rss = np.array([1e-21])
Sn_f0 = np.array([1e-46])

# Cálculo SNR
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)

# Intento de impresión - CAUSA ERROR
print(f"SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}")
# TypeError: unsupported format string passed to numpy.ndarray.__format__
```

## ✅ Solución

Se ha creado el módulo `snr_utils.py` que proporciona funciones seguras para manejar el cálculo y formateo de SNR.

### Opción 1: Usar `safe_format_snr()`

```python
from snr_utils import safe_format_snr

# Cálculo SNR
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)

# Convertir a escalar de forma segura
snr_safe = safe_format_snr(snr)

# Ahora sí se puede formatear
print(f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}")
```

### Opción 2: Usar `print_snr_result()`

```python
from snr_utils import print_snr_result

# Cálculo SNR
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)

# Imprime directamente sin preocupaciones
print_snr_result(snr, ifo, 141.7)
# Output: SNR esperada a 141.70 Hz en H1: 50.00
```

### Opción 3: Usar `calculate_snr_safe()`

```python
from snr_utils import calculate_snr_safe, safe_format_snr

# Cálculo SNR usando función segura
snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)

# Formatear
snr_safe = safe_format_snr(snr)
print(f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}")
```

## 📚 Funciones Disponibles

### `safe_format_snr(snr, decimals=2)`

Convierte un valor de SNR (escalar, array de numpy, etc.) a un float que puede ser formateado de forma segura.

**Parámetros:**
- `snr`: Valor de SNR (float, int, np.ndarray, etc.)
- `decimals`: Número de decimales (default: 2)

**Retorna:** `float` - Valor escalar listo para formatear

**Ejemplo:**
```python
snr = np.array([7.5])
snr_safe = safe_format_snr(snr)
print(f"SNR: {snr_safe:.2f}")  # SNR: 7.50
```

### `format_snr_string(snr, detector=None, frequency=None, decimals=2)`

Genera un string formateado completo con información de SNR.

**Parámetros:**
- `snr`: Valor de SNR
- `detector`: Nombre del detector (opcional, e.g., 'H1', 'L1')
- `frequency`: Frecuencia en Hz (opcional)
- `decimals`: Número de decimales (default: 2)

**Retorna:** `str` - String formateado

**Ejemplo:**
```python
snr = 7.5
result = format_snr_string(snr, 'H1', 141.7)
# Output: "SNR = 7.50 (H1 @ 141.70 Hz)"
```

### `calculate_snr_safe(F_eff, h_rss, Sn_f0)`

Calcula SNR usando la fórmula estándar: SNR = (F_eff * h_rss) / sqrt(Sn_f0)

**Parámetros:**
- `F_eff`: Factor de eficiencia del detector
- `h_rss`: Amplitud root-sum-square de la señal
- `Sn_f0`: Densidad espectral de ruido en la frecuencia objetivo

**Retorna:** `float` o `np.ndarray` - Valor de SNR calculado

**Ejemplo:**
```python
F_eff = np.array([0.5])
h_rss = np.array([1e-21])
Sn_f0 = np.array([1e-46])
snr = calculate_snr_safe(F_eff, h_rss, Sn_f0)
```

### `print_snr_result(snr, ifo, frequency=141.7)`

Imprime un resultado de SNR formateado correctamente, manejando automáticamente arrays de numpy.

**Parámetros:**
- `snr`: Valor de SNR
- `ifo`: Nombre del detector/interferómetro (e.g., 'H1', 'L1')
- `frequency`: Frecuencia en Hz (default: 141.7)

**Ejemplo:**
```python
snr = np.array([7.5])
print_snr_result(snr, 'H1', 141.7)
# Output: SNR esperada a 141.70 Hz en H1: 7.50
```

## 🧪 Pruebas y Ejemplos

### Ejecutar Tests

```bash
cd /home/runner/work/141hz/141hz
python3 -m pytest scripts/test_snr_utils.py -v
```

### Ejecutar Ejemplo Completo

```bash
python3 scripts/ejemplo_snr_formatting.py
```

Este ejemplo demuestra:
- El error original
- Las tres soluciones
- Análisis de múltiples detectores
- Mejores prácticas

### Ejecutar Módulo Directamente

```bash
python3 scripts/snr_utils.py
```

Muestra varios ejemplos de uso de las funciones.

## 📖 Archivos Relacionados

- **`scripts/snr_utils.py`**: Módulo principal con las funciones utilitarias
- **`scripts/test_snr_utils.py`**: Suite de tests completa (22 tests)
- **`scripts/ejemplo_snr_formatting.py`**: Ejemplo interactivo que demuestra el problema y las soluciones

## 🎯 Mejores Prácticas

### ✅ Hacer

1. **Siempre usar `safe_format_snr()` antes de formatear:**
   ```python
   snr_safe = safe_format_snr(snr)
   print(f"SNR: {snr_safe:.2f}")
   ```

2. **O usar `print_snr_result()` directamente:**
   ```python
   print_snr_result(snr, 'H1', 141.7)
   ```

3. **Para múltiples valores, iterar:**
   ```python
   for i, s in enumerate(snr_array):
       print(f"SNR[{i}] = {safe_format_snr(s):.2f}")
   ```

### ❌ Evitar

1. **No formatear arrays directamente:**
   ```python
   # ❌ MALO
   print(f"{snr:.2f}")  # TypeError si snr es array
   ```

2. **No asumir que el resultado es escalar:**
   ```python
   # ❌ MALO
   snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
   # snr podría ser array
   ```

## 🔧 Integración en Código Existente

Para actualizar código existente que tiene este problema:

**Antes:**
```python
snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
print(f"SNR esperada a 141.7 Hz en {ifo}: {snr:.2f}")  # ERROR
```

**Después:**
```python
from snr_utils import safe_format_snr

snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
snr_safe = safe_format_snr(snr)
print(f"SNR esperada a 141.7 Hz en {ifo}: {snr_safe:.2f}")  # ✓
```

**O más simple:**
```python
from snr_utils import print_snr_result

snr = (F_eff * h_rss) / np.sqrt(Sn_f0)
print_snr_result(snr, ifo, 141.7)  # ✓
```

## 📝 Notas Técnicas

- El módulo es compatible con numpy >= 1.21.0
- Funciona con Python 3.11+
- Maneja arrays de numpy, escalares de numpy (np.float64, etc.) y tipos nativos de Python
- Para arrays con múltiples elementos, `safe_format_snr()` retorna el primer valor
- Todos los tests pasan exitosamente (22/22)

## 🐛 Reportar Problemas

Si encuentras algún problema con estas utilidades, por favor:
1. Verifica que estás usando numpy >= 1.21.0
2. Ejecuta los tests: `python3 -m pytest scripts/test_snr_utils.py -v`
3. Revisa el ejemplo: `python3 scripts/ejemplo_snr_formatting.py`
4. Reporta el issue con el traceback completo

## 📄 Licencia

Este código sigue la misma licencia que el proyecto principal 141hz.
