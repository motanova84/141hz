# 🌐 Sistema de Verificación en Tiempo Real GW250114

## 📋 Descripción

Sistema automatizado para monitorear y detectar la disponibilidad de GW250114 en el catálogo GWOSC (Gravitational Wave Open Science Center), con análisis automático de la componente 141.7001 Hz cuando el evento esté disponible.

## 🎯 Características Principales

### 1. Verificación Automática
- ✅ Búsqueda en catálogo GWOSC en tiempo real
- ✅ Detección de eventos similares (GW25*, S250114*, MS250114*)
- ✅ Integración con API GWOSC para eventos públicos

### 2. Descarga Automática de Datos
- ✅ Descarga de datos de múltiples detectores (H1, L1, V1)
- ✅ Ventana temporal optimizada (±16 segundos alrededor del merger)
- ✅ Almacenamiento en formato HDF5 estándar

### 3. Análisis Espectral Automatizado
- ✅ Análisis en banda 140-143 Hz
- ✅ Detección de pico espectral
- ✅ Cálculo de SNR (Signal-to-Noise Ratio)
- ✅ Verificación de coincidencia con 141.7001 Hz (tolerancia < 0.1 Hz)
- ✅ Criterio de significancia: SNR > 5

### 4. Monitoreo Continuo
- ✅ Sistema de verificación periódica configurable
- ✅ Notificación automática cuando evento esté disponible
- ✅ Análisis automático al detectar evento

### 5. Generación de Informes
- ✅ Resultados en formato JSON estructurado
- ✅ Resumen ejecutivo con estadísticas
- ✅ Timestamp de análisis
- ✅ Métricas por detector

## 📁 Estructura de Archivos

```
scripts/
├── verificador_gw250114.py           # Sistema principal
├── test_verificador_gw250114.py      # Suite de tests
└── ejemplo_verificador_gw250114.py   # Ejemplos de uso

data/
└── raw/                               # Datos descargados de GWOSC
    └── .gitkeep

resultados/                            # Resultados de análisis
└── .gitkeep
```

## 🚀 Uso Básico

### Instalación de Dependencias

```bash
pip install gwpy gwosc numpy scipy pandas requests
```

### Verificación Simple

```python
from verificador_gw250114 import VerificadorGW250114

# Crear instancia
verificador = VerificadorGW250114()

# Verificar disponibilidad
disponible = verificador.verificar_disponibilidad_evento()

if disponible:
    # Descargar y analizar
    verificador.descargar_y_analizar_evento("GW250114")
```

### Ejecución Directa

```bash
# Verificación única
python scripts/verificador_gw250114.py

# Ejecutar tests
python scripts/test_verificador_gw250114.py

# Ver ejemplos de uso
python scripts/ejemplo_verificador_gw250114.py
```

### Monitoreo Continuo

```python
from verificador_gw250114 import VerificadorGW250114

verificador = VerificadorGW250114()

# Verificar cada 30 minutos
verificador.monitoreo_continuo(intervalo=1800)
```

## 📊 Formato de Resultados

Los resultados se guardan en `resultados/analisis_{evento}.json`:

```json
{
  "evento": "GW250114",
  "timestamp_analisis": "2025-01-14T12:00:00.000000",
  "resultados": {
    "H1": {
      "frecuencia_detectada": 141.7001,
      "snr": 7.5,
      "diferencia": 0.0001,
      "significativo": true,
      "potencia_pico": 1.2e-42
    },
    "L1": {
      "frecuencia_detectada": 141.75,
      "snr": 3.2,
      "diferencia": 0.0499,
      "significativo": false,
      "potencia_pico": 5.6e-43
    }
  },
  "resumen": {
    "detectores_significativos": ["H1"],
    "total_detectores": 2,
    "exitosos": 1,
    "tasa_exito": 0.5
  }
}
```

## 🔬 Metodología de Análisis

### 1. Preprocesamiento
- Descarga de datos con sample rate 4096 Hz
- Ventana temporal: merger_time ± 16 segundos

### 2. Análisis Espectral
- Método: Periodograma de Welch
- Banda de interés: 140-143 Hz
- Frecuencia objetivo: 141.7001 Hz

### 3. Criterios de Significancia
```python
significativo = (
    abs(f_pico - 141.7001) < 0.1  # Hz
    AND
    snr > 5
)
```

### 4. Evaluación Multi-Detector
- Análisis independiente H1, L1, V1
- Coherencia entre detectores
- Tasa de éxito = detectores_significativos / total_detectores

## 🧪 Tests Implementados

### test_verificador_gw250114.py

1. **test_basic_initialization**: Verifica inicialización correcta
   - Estado inicial
   - Creación de directorios

2. **test_generar_resumen**: Verifica generación de resumen
   - Conteo de detectores
   - Tasa de éxito
   - Identificación de detectores significativos

3. **test_guardar_resultados**: Verifica guardado de resultados
   - Formato JSON
   - Estructura de datos
   - Integridad de información

## 🔄 Integración con Pipeline Existente

El verificador se integra con el pipeline de validación actual:

```
Pipeline Validación GW150914 (control)
         ↓
    [BF > 10, p < 0.01] ✅
         ↓
  Verificador GW250114
         ↓
    ┌─────────┴─────────┐
    │                   │
Disponible         No disponible
    │                   │
    ↓                   ↓
Descarga          Buscar eventos
Análisis          similares
Resultados        Monitoreo
```

## 📝 Ejemplos de Uso

Ver `scripts/ejemplo_verificador_gw250114.py` para ejemplos completos:

- Verificación básica de disponibilidad
- Búsqueda de eventos similares
- Análisis de evento específico
- Integración con pipeline
- Interpretación de resultados

## ⚙️ Configuración

### Parámetros Ajustables

```python
class VerificadorGW250114:
    def __init__(self):
        self.evento_objetivo = "GW250114"      # Evento a buscar
        self.gwosc_base_url = "https://gwosc.org"
        
    def analizar_frecuencia_141hz(self, evento):
        # Banda de búsqueda
        banda = (140, 143)  # Hz
        
        # Umbral de significancia
        umbral_snr = 5
        
        # Tolerancia de frecuencia
        tolerancia = 0.1  # Hz
```

### Intervalo de Monitoreo

```python
# Verificar cada hora
verificador.monitoreo_continuo(intervalo=3600)

# Verificar cada 30 minutos
verificador.monitoreo_continuo(intervalo=1800)

# Verificar cada 10 minutos
verificador.monitoreo_continuo(intervalo=600)
```

## 🛡️ Manejo de Errores

El sistema maneja gracefully:
- ❌ Módulos no disponibles (gwosc, gwpy, scipy)
- ❌ Problemas de conectividad con GWOSC
- ❌ Eventos no encontrados
- ❌ Detectores sin datos
- ❌ Errores de análisis por detector

## 🎓 Validación Científica

El verificador aplica la metodología validada en GW150914:

- ✅ Control con evento conocido (GW150914)
- ✅ Criterios de significancia: BF > 10, p < 0.01
- ✅ Análisis multi-detector
- ✅ Verificación de coherencia

## 📚 Referencias

- [GWOSC - Gravitational Wave Open Science Center](https://gwosc.org)
- [GWpy Documentation](https://gwpy.github.io)
- Metodología basada en validación GW150914 (scripts/validar_gw150914.py)

## 🤝 Contribuciones

Para contribuir o reportar issues:
1. Ejecutar tests: `python scripts/test_verificador_gw250114.py`
2. Verificar integración: `python scripts/ejemplo_verificador_gw250114.py`
3. Validar compatibilidad con pipeline existente

## 📄 Licencia

Mismo que el proyecto principal GW250114-141hz-analysis.

---

**Nota**: Este sistema está diseñado para ejecutarse automáticamente cuando GW250114 esté disponible en GWOSC. Actualmente, GW250114 es un evento objetivo hipotético y el sistema está validado con eventos conocidos como GW150914.
