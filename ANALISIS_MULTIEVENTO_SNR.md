# Análisis Multi-evento de SNR en 141.7 Hz - Documentación

## Descripción General

Este módulo implementa un análisis multi-evento de SNR (Signal-to-Noise Ratio) centrado en la frecuencia objetivo de 141.7 Hz, analizando 11 eventos de ondas gravitacionales del catálogo GWTC.

## Características Principales

- **Análisis de 11 eventos**: GW150914, GW151012, GW151226, GW170104, GW170608, GW170729, GW170809, GW170814, GW170817, GW170818, GW170823
- **Detectores duales**: Analiza tanto H1 (Hanford) como L1 (Livingston)
- **Filtrado de banda**: Aplica filtro pasa-banda de 140.7-142.7 Hz (±1 Hz alrededor de 141.7 Hz)
- **Cálculo de SNR**: Utiliza la métrica `max(abs(señal)) / std(señal)`
- **Resultados en JSON**: Exporta datos estructurados para análisis posterior
- **Visualización comparativa**: Genera gráfico de barras comparando H1 vs L1
- **Estadísticas automáticas**: Calcula medias, desviaciones estándar y conteo de eventos sobre umbral

## Archivos del Módulo

### Script Principal: `scripts/multi_event_snr_analysis.py`

Implementa el análisis completo según el código del problema statement.

**Funciones principales:**

```python
def calculate_snr(data, band):
    """Calcula SNR aplicando filtro de banda y estadística max/std"""
    
def analyze_event(name, start, end, band):
    """Analiza un evento individual descargando datos de H1 y L1"""
    
def main():
    """Ejecuta el análisis completo de todos los eventos"""
```

### Suite de Tests: `scripts/test_multi_event_snr_analysis.py`

Valida el módulo sin requerir conectividad a GWOSC.

**Tests implementados:**

1. **Test de cálculo de SNR**: Valida el cálculo con datos sintéticos
2. **Test de configuración de eventos**: Verifica la estructura de eventos
3. **Test de configuración de banda**: Valida parámetros de frecuencia
4. **Test de función calculate_snr**: Verifica firma de función
5. **Test de función analyze_event**: Verifica firma de función

## Eventos Analizados

| Evento | Fecha | GPS Start | GPS End | Duración |
|--------|-------|-----------|---------|----------|
| GW150914 | 14 Sep 2015 | 1126259462 | 1126259494 | 32s |
| GW151012 | 12 Oct 2015 | 1128678900 | 1128678932 | 32s |
| GW151226 | 26 Dec 2015 | 1135136350 | 1135136382 | 32s |
| GW170104 | 4 Jan 2017 | 1167559936 | 1167559968 | 32s |
| GW170608 | 8 Jun 2017 | 1180922440 | 1180922472 | 32s |
| GW170729 | 29 Jul 2017 | 1185389806 | 1185389838 | 32s |
| GW170809 | 9 Aug 2017 | 1186302508 | 1186302540 | 32s |
| GW170814 | 14 Aug 2017 | 1186741850 | 1186741882 | 32s |
| GW170817 | 17 Aug 2017 | 1187008882 | 1187008914 | 32s |
| GW170818 | 18 Aug 2017 | 1187058327 | 1187058359 | 32s |
| GW170823 | 23 Aug 2017 | 1187529256 | 1187529288 | 32s |

## Parámetros de Análisis

- **Banda de frecuencia**: 140.7 - 142.7 Hz (±1 Hz alrededor de 141.7 Hz)
- **Frecuencia objetivo**: 141.7 Hz
- **Umbral de SNR**: 5.0
- **Ventana temporal**: 32 segundos por evento
- **Método de SNR**: `max(abs(señal)) / std(señal)`

## Uso

### Ejecución del Análisis Completo

**Con Makefile (recomendado):**

```bash
# Ejecutar análisis multi-evento (requiere conectividad a GWOSC)
make multi-event-snr

# Ejecutar tests sin conectividad
make test-multi-event-snr
```

**Directamente:**

```bash
# Análisis completo
python3 scripts/multi_event_snr_analysis.py

# Tests
python3 scripts/test_multi_event_snr_analysis.py
```

### Archivos Generados

Al ejecutar el análisis se generan:

1. **`multi_event_results.json`**: Resultados en formato JSON
   ```json
   {
     "GW150914": {
       "H1": 12.45,
       "L1": 10.23
     },
     "GW151012": {
       "H1": 8.67,
       "L1": 9.12
     },
     ...
   }
   ```

2. **`multi_event_analysis.png`**: Visualización comparativa H1 vs L1
   - Gráfico de barras lado a lado
   - Línea horizontal en SNR = 5 (umbral)
   - Etiquetas de eventos en eje X
   - SNR en eje Y

## Salida Esperada

```
======================================================================
🌌 ANÁLISIS MULTI-EVENTO DE SNR EN 141.7 Hz
======================================================================

Banda de frecuencia: 140.7-142.7 Hz
Frecuencia objetivo: 141.7 Hz
Umbral de SNR: 5.0
Eventos a analizar: 11

[1/11] ⏳ Analizando GW150914...
         ✅ H1 SNR = 12.34, L1 SNR = 10.56

[2/11] ⏳ Analizando GW151012...
         ✅ H1 SNR = 8.23, L1 SNR = 7.89

...

💾 Resultados guardados en: multi_event_results.json
📊 Visualización guardada en: multi_event_analysis.png

======================================================================
📊 RESUMEN ESTADÍSTICO
======================================================================
Eventos analizados exitosamente: 11/11

H1 SNR - Media: 9.45, Desv. Est: 2.31
L1 SNR - Media: 8.92, Desv. Est: 2.18

Eventos con SNR ≥ 5.0:
  H1: 9/11 (81.8%)
  L1: 8/11 (72.7%)

======================================================================
✅ Análisis completado. Archivos generados:
  - multi_event_results.json
  - multi_event_analysis.png
======================================================================
```

## Integración con el Proyecto

### Targets de Makefile

El módulo se integra mediante dos nuevos targets:

- **`multi-event-snr`**: Ejecuta el análisis completo (requiere internet)
- **`test-multi-event-snr`**: Ejecuta la suite de tests (sin internet)

### Archivos Ignorados

Los archivos de salida se agregan automáticamente a `.gitignore`:
- `multi_event_results.json`
- `multi_event_analysis.png`

## Metodología

### Cálculo de SNR

El SNR se calcula mediante:

```python
def calculate_snr(data, band):
    data_band = data.bandpass(*band)  # Filtrar banda 140.7-142.7 Hz
    snr = np.max(np.abs(data_band.value)) / np.std(data_band.value)
    return snr
```

Esta métrica identifica la amplitud máxima de la señal filtrada en relación con el ruido de fondo (desviación estándar).

### Análisis por Evento

Para cada evento:

1. **Descarga de datos**: Se obtienen datos de H1 y L1 desde GWOSC
2. **Filtrado**: Se aplica bandpass filter en 140.7-142.7 Hz
3. **Cálculo de SNR**: Se calcula SNR para cada detector
4. **Almacenamiento**: Los resultados se guardan en estructura de datos

### Manejo de Errores

El script incluye manejo robusto de errores:
- Si falla la descarga de datos, se registra el error y continúa con siguiente evento
- Los errores se guardan en el JSON con estructura `{"error": "mensaje"}`
- Se genera visualización solo si hay datos exitosos

## Compatibilidad

- **Python**: 3.11+
- **GWPy**: >= 3.0.0
- **NumPy**: >= 1.21.0
- **Matplotlib**: >= 3.5.0
- **Conectividad**: Requerida para análisis real, opcional para tests

## Notas Técnicas

### Ventana Temporal

Cada evento se analiza en una ventana de 32 segundos:
- Suficiente para capturar la señal completa
- Minimiza contaminación de ruido externo
- Estándar en análisis de ondas gravitacionales

### Banda de Frecuencia

La banda de 140.7-142.7 Hz (±1 Hz) se elige porque:
- Centra el análisis en la frecuencia objetivo 141.7 Hz
- Permite capturar variaciones y armónicos cercanos
- Reduce contribuciones de ruido fuera de banda

### Umbral de SNR

El umbral de SNR = 5.0:
- Es un valor conservador para detección de señales
- Coincide con estándares de análisis LIGO
- Permite identificar eventos con señal significativa

## Futuras Mejoras

Posibles extensiones del módulo:

1. **Análisis de Virgo**: Agregar detector V1 cuando disponible
2. **Análisis temporal**: Estudiar evolución de SNR en el tiempo
3. **Análisis espectral completo**: Extender análisis a múltiples frecuencias
4. **Estadística bayesiana**: Implementar inferencia bayesiana de SNR
5. **Comparación con modelos**: Comparar SNR observado vs predicho
6. **Análisis de coherencia**: Medir coherencia entre H1 y L1
7. **Exportación a HDF5**: Guardar datos procesados en formato HDF5
8. **Visualizaciones avanzadas**: Spectrogramas, mapas de tiempo-frecuencia

## Referencias

- **GWOSC**: Gravitational Wave Open Science Center - https://gwosc.org
- **GWPy**: Python package for gravitational wave astronomy - https://gwpy.github.io
- **GWTC**: Gravitational Wave Transient Catalog - https://www.ligo.org/science/GWTC.php
- **Paper**: Análisis de f₀ = 141.7001 Hz en ondas gravitacionales

## Autores y Contribuciones

Este módulo fue implementado como parte del proyecto de análisis de la frecuencia fundamental f₀ = 141.7001 Hz en ondas gravitacionales.

**Contacto**: Ver CONTRIBUTING.md para más información.

## Licencia

Ver LICENSE para detalles de licencia del proyecto.
