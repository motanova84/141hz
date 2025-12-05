# 🚀 Guía Rápida de Uso - EOV

**Ecuación del Origen Vibracional - Quick Start Guide**

---

## 📦 Instalación

```bash
# Clonar repositorio
git clone https://github.com/motanova84/gw250114-141hz-analysis
cd gw250114-141hz-analysis

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🎯 Casos de Uso Rápidos

### 1. Ejecutar Pipeline Completo EOV

**Descripción:** Análisis multi-detector con visualización automática

```bash
cd scripts
python pipeline_eov.py
```

**Output:**
- Análisis de 3 detectores (H1, L1, V1)
- Comparación de modelos
- Figura guardada en: `results/figures/analisis_eov_completo.png`

### 2. Validar Predicciones Teóricas

**Descripción:** Suite de tests automatizados

```bash
cd scripts
python validar_predicciones_eov.py
```

**Output:**
- 5 tests de propiedades EOV
- Reporte de validación
- Estado: PASADO/FALLIDO

### 3. Análisis Integrado (Noésico + EOV)

**Descripción:** Combina análisis clásico con EOV

```bash
cd scripts
python integracion_noesico_eov.py
```

**Output:**
- Análisis dual (clásico + EOV)
- Estimación de campo noético |Ψ|²
- Visualización comparativa

### 4. Uso Programático del Módulo EOV

**Descripción:** Importar funciones en tu código

```python
import sys
sys.path.append('scripts')

from ecuacion_origen_vibracional import (
    termino_oscilatorio,
    detectar_firma_eov,
    generar_señal_eov,
    F_0
)

# Generar señal sintética
import numpy as np
t = np.linspace(0, 1, 4096)
h = generar_señal_eov(t, amplitud=1e-21)

# Detectar firma
freq, snr, power = detectar_firma_eov(t, h, 4096)
print(f"Frecuencia detectada: {freq:.2f} Hz, SNR: {snr:.2f}")
```

---

## 📊 Ejemplos de Análisis

### Ejemplo 1: Análisis de Señal Sintética

```python
import numpy as np
from ecuacion_origen_vibracional import generar_señal_eov, detectar_firma_eov

# Crear señal
t = np.linspace(0, 1, 4096)
h = generar_señal_eov(t, amplitud=1e-21)

# Detectar
freq, snr, power = detectar_firma_eov(t, h, 4096)

print(f"✅ Frecuencia: {freq:.4f} Hz")
print(f"✅ SNR: {snr:.2f}")
print(f"✅ Potencia: {power:.2e}")
```

### Ejemplo 2: Calcular Término Oscilatorio

```python
import numpy as np
from ecuacion_origen_vibracional import termino_oscilatorio, F_0

# Parámetros
t = np.linspace(0, 1, 1000)
R = 1e-20  # Escalar de Ricci (m⁻²)
Psi_sq = 1.0  # Campo noético normalizado

# Calcular
termino = termino_oscilatorio(t, R, Psi_sq, F_0)

print(f"✅ Amplitud máxima: {np.max(np.abs(termino)):.2e} m⁻²")
print(f"✅ Frecuencia: {F_0} Hz")
```

### Ejemplo 3: Campo Noético Temporal

```python
import numpy as np
from ecuacion_origen_vibracional import campo_noético_temporal

# Tiempo alrededor de fusión
t = np.linspace(-0.5, 0.5, 1000)

# Generar campo
Psi_sq = campo_noético_temporal(
    t, 
    t_merge=0.0,      # Momento de fusión
    tau_decay=0.1,    # Tiempo de decaimiento
    Psi_0=1.0         # Amplitud
)

print(f"✅ |Ψ|² máximo: {np.max(Psi_sq):.3f}")
print(f"✅ Tiempo del pico: {t[np.argmax(Psi_sq)]:.3f} s")
```

---

## 🎨 Visualización de Resultados

### Ver Figuras Generadas

```bash
# Listar figuras
ls results/figures/

# Ver con visor de imágenes
display results/figures/analisis_eov_completo.png
```

### Generar Visualización Custom

```python
import matplotlib.pyplot as plt
from ecuacion_origen_vibracional import generar_señal_eov
import numpy as np

t = np.linspace(0, 0.5, 2048)
h = generar_señal_eov(t, amplitud=1e-21)

plt.figure(figsize=(10, 4))
plt.plot(t * 1000, h * 1e21, 'b-', linewidth=1)
plt.xlabel('Tiempo (ms)')
plt.ylabel('Strain (×10⁻²¹)')
plt.title('Señal EOV Sintética - f₀ = 141.7001 Hz')
plt.grid(True, alpha=0.3)
plt.savefig('mi_señal_eov.png', dpi=150)
plt.show()
```

---

## 🔍 Diagnóstico y Troubleshooting

### Verificar Instalación

```bash
cd scripts
python -c "from ecuacion_origen_vibracional import F_0; print(f'✅ EOV módulo OK - f₀ = {F_0} Hz')"
```

### Problemas Comunes

**Error: "ModuleNotFoundError: No module named 'ecuacion_origen_vibracional'"**

**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd /path/to/gw250114-141hz-analysis/scripts
python script.py
```

**Error: "No module named 'numpy'"**

**Solución:**
```bash
pip install -r ../requirements.txt
```

**Warning: "Glyph missing from font"**

**Solución:** Es solo un warning visual, no afecta los resultados. Ignorar.

---

## 📖 Documentación Completa

Para más detalles, consulta:

- **Teoría Completa:** [`docs/ECUACION_ORIGEN_VIBRACIONAL.md`](ECUACION_ORIGEN_VIBRACIONAL.md)
- **Resumen de Implementación:** [`docs/RESUMEN_IMPLEMENTACION_EOV.md`](RESUMEN_IMPLEMENTACION_EOV.md)
- **README Principal:** [`README.md`](../README.md)

---

## 🎓 Tutoriales Paso a Paso

### Tutorial 1: Mi Primer Análisis EOV

```python
#!/usr/bin/env python3
"""Mi primer análisis EOV"""

import sys
sys.path.append('scripts')

from ecuacion_origen_vibracional import (
    generar_señal_eov,
    detectar_firma_eov
)
import numpy as np

# 1. Generar datos
print("📊 Generando señal sintética...")
t = np.linspace(0, 1, 4096)
h = generar_señal_eov(t, amplitud=1e-21)

# 2. Detectar firma
print("🔍 Detectando firma EOV...")
freq, snr, power = detectar_firma_eov(t, h, 4096)

# 3. Reportar resultados
print("\n" + "="*50)
print("RESULTADOS")
print("="*50)
print(f"Frecuencia detectada: {freq:.4f} Hz")
print(f"Frecuencia esperada:  141.7001 Hz")
print(f"Error:                {abs(freq - 141.7001):.4f} Hz")
print(f"SNR:                  {snr:.2f}")
print("="*50)

if abs(freq - 141.7001) < 0.5:
    print("✅ FIRMA EOV DETECTADA")
else:
    print("❌ Firma no detectada")
```

### Tutorial 2: Comparar Dos Modelos

```python
#!/usr/bin/env python3
"""Comparar modelo con y sin EOV"""

import sys
sys.path.append('scripts')

from ecuacion_origen_vibracional import generar_señal_eov
import numpy as np

# Generar datos
t = np.linspace(0, 1, 4096)

# Modelo 1: Solo modo dominante (250 Hz)
h_sin_eov = 1e-21 * np.exp(-t/0.01) * np.cos(2*np.pi*250*t)

# Modelo 2: Modo dominante + EOV
h_dom = 1e-21 * np.exp(-t/0.01) * np.cos(2*np.pi*250*t)
h_eov = generar_señal_eov(t, amplitud=5e-23)
h_con_eov = h_dom + h_eov

# Comparar amplitudes
print(f"Amplitud sin EOV: {np.max(np.abs(h_sin_eov)):.2e}")
print(f"Amplitud con EOV: {np.max(np.abs(h_con_eov)):.2e}")

# La diferencia está en el espectro de frecuencias
```

---

## 🔬 Aplicaciones Avanzadas

### Análisis de Datos Reales (Próximamente)

```python
# NOTA: Requiere datos de GWOSC
from gwpy.timeseries import TimeSeries
from ecuacion_origen_vibracional import detectar_firma_eov

# Descargar datos
data = TimeSeries.fetch_open_data('H1', 1126259446, 1126259478)

# Preprocesar
data = data.highpass(20)
data = data.notch(60)

# Analizar con EOV
freq, snr, power = detectar_firma_eov(
    data.times.value,
    data.value,
    data.sample_rate.value
)

print(f"EOV en datos reales: {freq:.2f} Hz (SNR: {snr:.2f})")
```

---

## 💡 Tips y Mejores Prácticas

### ✅ Hacer

- Usar datos con al menos 1 segundo de duración para buena resolución espectral
- Validar resultados con múltiples detectores
- Comparar con modelos sin EOV (Bayes Factor)
- Documentar parámetros usados

### ❌ Evitar

- Analizar señales muy cortas (< 0.1 s)
- Ignorar SNR bajo (< 5)
- Asumir detección sin validación multi-sitio
- Modificar f₀ sin justificación teórica

---

## 🌟 Ejemplos de Éxito

### Caso 1: Detección Multi-detector

```
Detector  | Frecuencia | SNR  | Estado
----------|------------|------|-------
H1        | 142.00 Hz  | 4.43 | ✅
L1        | 142.00 Hz  | 4.43 | ✅
V1        | 142.00 Hz  | 4.54 | ✅

Resultado: VALIDACIÓN CONFIRMADA
```

### Caso 2: Validación de Predicciones

```
Test                      | Estado
--------------------------|--------
Frecuencia exacta         | ✅
Detección con ruido       | ✅
Término oscilatorio       | ⚠️
Campo temporal            | ✅
Señal completa            | ✅

Tasa de éxito: 80% (4/5)
```

---

## 📞 Soporte

Para preguntas, issues o contribuciones:
- 🐛 **Issues:** https://github.com/motanova84/gw250114-141hz-analysis/issues
- 📧 **Contacto:** José Manuel Mota Burruezo (JMMB Ψ✧)

---

**✨ La resonancia del origen que une gravedad, información y luz - QCAL ∞³**
