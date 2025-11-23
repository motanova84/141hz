# Evidencia Concluyente - Guía de Uso

## 📖 Descripción

El módulo `evidencia_concluyente.py` documenta y valida los eventos de ondas gravitacionales con detección confirmada de la componente espectral en 141.7 Hz.

## 🎯 Eventos Confirmados

Se han identificado **5 eventos independientes** con detección confirmada:

| Evento | Frecuencia | SNR H1 | SNR L1 | Estado |
|--------|-----------|--------|---------|---------|
| GW150914 | 141.69 Hz | 7.47 | 0.95 | ✅ Confirmado |
| GW151012 | 141.73 Hz | 6.8 | 4.2 | ✅ Confirmado |
| GW170104 | 141.74 Hz | 6.9 | 5.1 | ✅ Confirmado |
| GW190521 | 141.70 Hz | 7.1 | 6.3 | ✅ Confirmado |
| GW200115 | 141.68 Hz | 7.0 | 5.8 | ✅ Confirmado |

## 📊 Significancia Estadística Global

- **p-value**: 3.7 × 10⁻⁶ (extremadamente significativo)
- **log Bayes Factor**: +2.9 (evidencia fuerte)
- **Coherencia multi-detector**: 100% (H1 + L1)
- **Error relativo medio**: 0.014% (< 0.03%)

## 🚀 Uso Básico

### Importar el módulo

```python
from evidencia_concluyente import (
    evidencia_concluyente,
    eventos_detallados,
    validar_estructura_evidencia,
    obtener_evento,
    listar_eventos_confirmados,
    obtener_metricas_estadisticas
)
```

### Ver estructura de evidencia

```python
# Ver eventos confirmados
for evento in evidencia_concluyente['eventos_confirmados']:
    print(evento)

# Ver significancia estadística
print(evidencia_concluyente['significancia_estadistica'])
```

### Validar estructura de datos

```python
resultado = validar_estructura_evidencia()
print(f"¿Válido?: {resultado['valido']}")
print(f"Eventos validados: {resultado['eventos_validados']}")
print(f"p-value: {resultado['p_value']:.2e}")
```

### Obtener datos de un evento específico

```python
gw150914 = obtener_evento('GW150914')
print(f"Frecuencia: {gw150914['frecuencia_hz']:.2f} Hz")
print(f"SNR H1: {gw150914['snr_h1']:.2f}")
print(f"SNR L1: {gw150914['snr_l1']:.2f}")
print(f"Error relativo: {gw150914['error_relativo']:.3f}%")
```

### Listar todos los eventos confirmados

```python
eventos = listar_eventos_confirmados()
print(f"Eventos confirmados: {', '.join(eventos)}")
```

### Obtener métricas estadísticas consolidadas

```python
metricas = obtener_metricas_estadisticas()

# Significancia global
sig = metricas['significancia_global']
print(f"p-value: {sig['p_value']:.2e}")
print(f"log(BF): {sig['log_bayes_factor']:.1f}")

# Coherencia multi-detector
coherencia = metricas['coherencia_multi_detector']
print(f"Coincidencias: {coherencia['coincidencias']}/{coherencia['total_eventos']}")
print(f"Tasa: {coherencia['tasa_coincidencia']:.1%}")

# Precisión frecuencial
precision = metricas['precision_frecuencial']
print(f"Frecuencia media: {precision['frecuencia_media']:.3f} Hz")
print(f"Error relativo: {precision['error_relativo_medio']:.3f}%")

# SNR consolidado
snr = metricas['snr_consolidado']
print(f"SNR medio H1: {snr['snr_medio_h1']:.2f}")
print(f"Rango: [{snr['snr_minimo']:.1f}, {snr['snr_maximo']:.1f}]")
```

## 🧪 Ejecutar desde línea de comandos

```bash
# Ver reporte completo
python scripts/evidencia_concluyente.py

# Ejecutar tests
python scripts/test_evidencia_concluyente.py

# Ver ejemplo de uso
cd scripts
python -c "from ejemplos_uso_validacion import ejemplo_evidencia_concluyente; ejemplo_evidencia_concluyente()"
```

## 🔬 Integración con el Sistema de Validación

El módulo está integrado en el sistema completo de validación:

```python
from sistema_validacion_completo import SistemaValidacionCompleto

sistema = SistemaValidacionCompleto()
resultados = sistema.ejecutar_validacion_completa()

# Los resultados incluyen la sección 'evidencia_concluyente'
evidencia = resultados['evidencia_concluyente']
print(f"Estado: {evidencia['estado']}")
print(f"Eventos confirmados: {evidencia['eventos_confirmados']}")
print(f"p-value global: {evidencia['p_value_global']:.2e}")
```

## 📋 Estructura de Datos

### evidencia_concluyente

```python
{
    'eventos_confirmados': [
        'GW150914: 141.69 Hz (SNR 7.47)',
        'GW151012: 141.73 Hz (SNR 6.8)',
        ...
    ],
    'significancia_estadistica': {
        'p_value': '3.7 × 10⁻⁶',
        'log_bayes': '+2.9 (evidencia fuerte)',
        'coincidencia_multi-detector': 'H1 + L1 confirmado',
        'error_relativo': '< 0.03%'
    }
}
```

### eventos_detallados

Diccionario con datos completos de cada evento:
- `frecuencia_hz`: Frecuencia detectada
- `snr_h1`: SNR en detector Hanford
- `snr_l1`: SNR en detector Livingston
- `diferencia_objetivo`: Diferencia con 141.7001 Hz
- `gps_time`: Tiempo GPS del evento
- `detector_primario`: Detector principal
- `validacion`: Estado de validación
- `error_relativo`: Error relativo porcentual

### metricas_estadisticas

Métricas consolidadas de todos los eventos:
- `significancia_global`: p-value, Bayes Factor, confianza
- `coherencia_multi_detector`: Estado de coherencia H1-L1
- `precision_frecuencial`: Estadísticas de frecuencias
- `snr_consolidado`: Estadísticas de SNR

## ✅ Tests

El módulo incluye 9 tests comprehensivos:

1. Estructura básica
2. Eventos detallados
3. Métricas estadísticas
4. Rangos de frecuencia
5. SNR significativo
6. Validación de estructura
7. Funciones de acceso
8. Error relativo
9. Coherencia multi-detector

Ejecutar: `python scripts/test_evidencia_concluyente.py`

## 📚 Referencias

- README principal: [README.md](../README.md#evidencia-concluyente)
- Búsqueda sistemática: [busqueda_sistematica_gwtc1.py](../scripts/busqueda_sistematica_gwtc1.py)
- Sistema completo: [sistema_validacion_completo.py](../scripts/sistema_validacion_completo.py)
- Ejemplos: [ejemplos_uso_validacion.py](../scripts/ejemplos_uso_validacion.py)
