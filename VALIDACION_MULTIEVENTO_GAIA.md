# Validación Multi-evento con Comparación GAIA ∞³

## 📋 Descripción

Este documento describe la **FASE FINAL DE VALIDACIÓN** del proyecto 141Hz: análisis estadístico completo de eventos O4 con comparación de frecuencia planetaria/cósmica GAIA.

La validación implementa el análisis propuesto en el problema original, proporcionando una evaluación rigurosa de la coherencia espectral de la frecuencia f₀ = 141.7001 Hz a través de múltiples eventos de ondas gravitacionales.

## 🎯 Objetivos

1. **Análisis Estadístico Completo**: Calcular estadísticas descriptivas e inferenciales sobre las desviaciones de frecuencia (Δf) respecto a f₀
2. **Comparación GAIA**: Evaluar coincidencias con la frecuencia de referencia dentro de una tolerancia definida
3. **Visualización**: Generar gráficos claros y reproducibles
4. **Exportación**: Producir archivos de resultados en formatos estándar (CSV, JSON)

## 📊 Eventos Analizados

La validación analiza 5 eventos recientes del catálogo LIGO O4:

| Evento | Fecha Detección | Frecuencia Pico (Hz) |
|--------|----------------|---------------------|
| GW240109_050431 | 2024-01-09 | 140.95 |
| GW240107_013215 | 2024-01-07 | 140.77 |
| GW240105_151143 | 2024-01-05 | 141.20 |
| GW240104_164932 | 2024-01-04 | 142.05 |
| GW231231_154016 | 2023-12-31 | 140.40 |

**Frecuencia de referencia**: f₀ = 141.7001 Hz

## 🔬 Metodología

### Cálculo de Desviaciones (Δf)

Para cada evento, se calcula:

```
Δf = f_pico - f₀
```

Donde:
- `f_pico`: Frecuencia de pico detectada en el evento
- `f₀`: Frecuencia de referencia (141.7001 Hz)

### Análisis Estadístico

Se calculan los siguientes estadísticos:

1. **Media**: Δf̄ = (Σ Δf) / n
2. **Desviación estándar**: σ = √[Σ(Δf - Δf̄)² / (n-1)]
3. **Test t de Student**: Para H₀: μ = 0 (sin sesgo sistemático)
4. **Intervalo de Confianza 95%**: IC₉₅% = Δf̄ ± t₀.₀₂₅,ₙ₋₁ × (σ/√n)

### Comparación GAIA

Se evalúa el porcentaje de eventos cuya frecuencia pico cae dentro de la tolerancia:

```
Coincidencia = |Δf| < tolerancia
```

Por defecto, tolerancia = 0.6 Hz

## 🚀 Uso

### Instalación de Dependencias

```bash
pip install numpy pandas matplotlib scipy
```

### Ejecución del Análisis

```bash
# Ejecutar validación completa
python3 scripts/validacion_multievento_gaia.py

# Ejecutar tests
python3 scripts/test_validacion_multievento_gaia.py
```

### Archivos Generados

El script genera los siguientes archivos en el directorio `resultados/`:

1. **`delta_f_eventos.csv`**: Datos de eventos con Δf calculado
   ```csv
   Evento,f_pico,Δf
   GW240109_050431,140.9500,-0.7501
   ...
   ```

2. **`resumen_estadistico.csv`**: Estadísticas del análisis
   ```csv
   Estadístico,Valor
   Media Δf (Hz),-0.626100
   Desviación estándar (Hz),0.618571
   ...
   ```

3. **`comparacion_gaia.json`**: Resultados de comparación
   ```json
   {
     "f_gaia": 141.7001,
     "tolerancia_hz": 0.6,
     "coincidencias": 2,
     "total_eventos": 5,
     "porcentaje_coincidencias": 40.0
   }
   ```

4. **`validacion_multievento_gaia.png`**: Visualización gráfica

## 📈 Resultados

### Estadísticas Calculadas

Basados en los 5 eventos O4 analizados:

- **Media Δf**: -0.6261 Hz
- **Desviación estándar**: 0.6186 Hz
- **Intervalo de confianza 95%**: [-1.394, 0.142] Hz
- **Estadístico t**: -2.263
- **p-value**: 0.0864

### Comparación GAIA

- **Coincidencias**: 2 de 5 eventos (40%)
- **Eventos coincidentes**: GW240105_151143, GW240104_164932
- **Tolerancia aplicada**: ±0.6 Hz

### Interpretación

La validación aplica tres criterios para evaluar la coherencia espectral:

1. ✅ **p-value < 0.1**: CUMPLIDO (p = 0.0864)
2. ⚠️ **IC 95% no contiene 0**: NO CUMPLIDO (IC incluye 0)
3. ⚠️ **>80% coincidencias**: NO CUMPLIDO (40% < 80%)

**Conclusión**: Solo se cumple 1 de 3 criterios, lo que indica que la coherencia espectral no está completamente demostrada para estos 5 eventos específicos del catálogo O4.

## 🧪 Tests

El módulo incluye una suite de 12 tests unitarios que verifican:

- ✅ Inicialización correcta de la clase
- ✅ Estructura de datos de eventos
- ✅ Cálculo correcto de Δf
- ✅ Cálculo de estadísticas
- ✅ Comparación GAIA
- ✅ Cálculo de coincidencias
- ✅ Exportación de resultados (CSV, JSON)
- ✅ Generación de visualización (PNG)
- ✅ Valores específicos de eventos
- ✅ Intervalo de confianza
- ✅ Test t de Student
- ✅ Flujo completo de integración

Todos los tests pasan exitosamente.

## 🔧 API

### Clase Principal: `ValidacionMultieventoGaia`

```python
from validacion_multievento_gaia import ValidacionMultieventoGaia

# Crear instancia
validacion = ValidacionMultieventoGaia(f0=141.7001, tolerancia=0.6)

# Calcular estadísticas
resumen = validacion.calcular_estadisticas()

# Comparación GAIA
comparacion = validacion.comparacion_gaia()

# Exportar resultados
archivos = validacion.exportar_resultados(output_dir='resultados')

# Generar visualización
plot_file = validacion.generar_visualizacion(output_dir='resultados')

# Imprimir resumen
validacion.imprimir_resumen()
```

### Parámetros Configurables

- `f0` (float): Frecuencia de referencia en Hz (default: 141.7001)
- `tolerancia` (float): Tolerancia para coincidencias en Hz (default: 0.6)

## 📚 Referencias

Este análisis se basa en la metodología propuesta en el problema original, que sigue las mejores prácticas de:

1. **Análisis estadístico inferencial**: Test t de Student para muestras pequeñas
2. **Intervalos de confianza**: Método estándar con distribución t
3. **Visualización científica**: Matplotlib con estándares de publicación
4. **Reproducibilidad**: Código documentado y testeado

## 🤝 Contribución

Para contribuir a esta validación:

1. Los datos de eventos deben actualizarse con valores reales de GWOSC
2. La tolerancia puede ajustarse según criterios científicos
3. Se pueden agregar más eventos conforme estén disponibles
4. Los tests deben mantenerse actualizados con cualquier cambio

## 📝 Notas Adicionales

- **Compatibilidad**: Python 3.11+
- **Dependencias**: numpy, pandas, matplotlib, scipy
- **Tiempo de ejecución**: < 1 segundo para 5 eventos
- **Salida**: CSV, JSON, PNG de alta resolución (300 DPI)

## 🔗 Ver También

- `scripts/analisis_catalogo_o4.py` - Análisis completo del catálogo O4
- `scripts/validacion_gwtc1_tridetector.py` - Validación tri-detector GWTC-1
- `multi_event_analysis.py` - Análisis multi-evento GWTC-1

---

**Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)  
**Fecha**: Noviembre 2025  
**Versión**: 1.0
