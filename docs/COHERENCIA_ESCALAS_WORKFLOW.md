# 🌈 Visualización de Coherencia Multi-escala - Flujo Interactivo Autoactualizado

## 📋 Descripción

Este sistema genera automáticamente visualizaciones de la coherencia de la frecuencia fundamental **f₀ = 141.7001 Hz** a través de múltiples escalas del universo:

- **Escala de Planck** (10⁻⁴⁴ a 10⁻³⁵ m) - Física cuántica fundamental
- **Escala LIGO** (10¹ a 10³ Hz) - Ondas gravitacionales
- **Escala CMB** (10⁻³ a 10¹) - Cosmología y radiación de fondo

## 🔄 Flujo Automático

### GitHub Actions Workflow

El sistema implementa un **flujo interactivo autoactualizado** mediante GitHub Actions que:

1. **Se ejecuta automáticamente cada día** a las 00:00 UTC
2. **Se ejecuta en cada push** al script de generación
3. **Se puede ejecutar manualmente** desde la UI de GitHub Actions
4. **Actualiza automáticamente** la imagen en el repositorio si hay cambios

### Archivo de Workflow

Ubicación: `.github/workflows/update_coherence_visualization.yml`

```yaml
# Triggers automáticos:
on:
  push:                    # En cada push
  workflow_dispatch:       # Ejecución manual
  schedule:                # Diariamente a las 00:00 UTC
    - cron: '0 0 * * *'
```

## 🚀 Uso

### Generación Local

```bash
# Usando Make
make coherencia-escalas

# O directamente con Python
python scripts/generar_coherencia_escalas.py
```

### Ejecución Manual en GitHub

1. Ve a la pestaña **Actions** en GitHub
2. Selecciona **Auto-Update Coherence Visualization**
3. Haz clic en **Run workflow**
4. La visualización se regenerará y actualizará automáticamente

## 📊 Archivos Generados

El script genera dos copias de la imagen:

1. **`coherence_f0_scales.png`** - En la raíz del proyecto (para README)
2. **`results/figures/coherence_f0_scales.png`** - En el directorio de resultados

## 🔍 Verificación

### Tests Automatizados

```bash
# Ejecutar tests de verificación
python scripts/test_coherencia_escalas.py
```

Los tests verifican:
- ✅ Existencia del script generador
- ✅ Generación correcta de la imagen
- ✅ Existencia del workflow de GitHub Actions
- ✅ Inclusión de la imagen en README.md

### Integración en CI/CD

El workflow se integra perfectamente con el sistema CI/CD existente:

- **Artifacts**: Las visualizaciones se guardan como artifacts (90 días de retención)
- **Summary**: Cada ejecución genera un resumen en la pestaña Actions
- **Auto-commit**: Si hay cambios, se commitean automáticamente con `[skip ci]`

## 📈 Características Técnicas

### Funciones de Visualización

El script implementa cuatro funciones representativas:

```python
def zeta_curve(s):           # Función zeta de Riemann
def modulation_eeg(s):       # Modulación EEG
def gravitational_waves(s):  # Ondas gravitacionales
def cmb_pattern(s):          # Patrón CMB
```

### Escalas Logarítmicas

Todas las curvas se visualizan en escala logarítmica para capturar la coherencia a través de múltiples órdenes de magnitud.

### Marcadores de Frecuencia

Líneas verticales discontinuas marcan la posición de **f₀ = 141.7001 Hz** en cada dominio.

## 🎨 Personalización

Para modificar la visualización, edita `scripts/generar_coherencia_escalas.py`:

```python
# Cambiar rangos de escala
escalas = {
    'Planck': np.logspace(-44, -35, 100),
    'LIGO': np.logspace(1, 3, 100),
    'CMB': np.logspace(-3, 1, 100)
}

# Modificar funciones de curvas
def zeta_curve(s):
    return np.abs(np.sin(np.log10(s)*5)) * 1e-2
```

## 🔗 Integración con README

La imagen se incluye automáticamente en el README.md:

```markdown
![Coherencia f₀ en Distintas Escalas](coherence_f0_scales.png)
```

## 🛡️ Robustez

El sistema incluye:

- **Cache de dependencias** - Instalaciones rápidas en CI/CD
- **Detección de cambios** - Solo commitea si la imagen cambió
- **Manejo de errores** - Continua incluso si hay advertencias
- **Artifacts permanentes** - Historial de 90 días de visualizaciones

## 📝 Logs y Monitoring

Cada ejecución del workflow genera:

1. **Summary detallado** en la pestaña Actions
2. **Artifacts descargables** con las imágenes generadas
3. **Commits automáticos** con mensaje descriptivo

## 🔮 Futuras Mejoras

Posibles extensiones del sistema:

- [ ] Animaciones temporales de coherencia
- [ ] Visualización 3D de múltiples frecuencias
- [ ] Comparación con datos experimentales reales
- [ ] Dashboard interactivo con Plotly/Dash
- [ ] Exportación a múltiples formatos (SVG, PDF, etc.)

## 📚 Referencias

- Script principal: `scripts/generar_coherencia_escalas.py`
- Tests: `scripts/test_coherencia_escalas.py`
- Workflow: `.github/workflows/update_coherence_visualization.yml`
- Make target: `make coherencia-escalas`

---

**Última actualización:** 2025-10-20  
**Versión:** 1.0.0  
**Autor:** Sistema automatizado basado en especificaciones del problem statement
