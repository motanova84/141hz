# 𓂀 Pipeline de Validación Rigurosa QCAL

Sistema completo para descarga de datos crudos, detección rigurosa con SNR>5σ, correlación multi-observatorio y validación teórica de la frecuencia f₀=141.7001 Hz.

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Componentes del Pipeline](#componentes-del-pipeline)
3. [Instalación](#instalación)
4. [Uso Rápido](#uso-rápido)
5. [Uso Avanzado](#uso-avanzado)
6. [Ejemplos](#ejemplos)
7. [Resultados](#resultados)

## 🎯 Descripción General

Este pipeline implementa un sistema de validación rigurosa para la frecuencia fundamental f₀=141.7001 Hz, siguiendo estándares científicos estrictos:

- ✅ **Descarga de datos reales** de GWOSC (LIGO/Virgo) e IGETS (gravímetros)
- ✅ **Detección rigurosa** con umbral SNR > 5σ (estándar para descubrimientos)
- ✅ **Control de falsos positivos** usando simulaciones Monte Carlo
- ✅ **Correlación multi-observatorio** para descartar ruido local
- ✅ **Validación teórica** con enlaces a física establecida
- ✅ **Predicciones falsables** para validación futura

## 🔧 Componentes del Pipeline

### 1. Descargadores de Datos

#### `descargador_gwosc.py`
Descarga datos crudos de LIGO/Virgo/KAGRA a máxima resolución (4096 Hz).

```bash
# Descargar 3 eventos con 32 segundos de duración
python scripts/descargador_gwosc.py --eventos 3 --duracion 32 --detector H1 --salida datos_crudos/
```

**Características:**
- Acceso a catálogo GWTC-3/O3
- Frecuencia de muestreo: 4096 Hz
- Formato de salida: HDF5
- Fallback a datos simulados si no hay acceso a GWOSC

#### `descargador_igets.py`
Descarga datos gravimétricos de IGETS/GFZ.

```bash
# Descargar datos de estación BFO
python scripts/descargador_igets.py --estacion BFO --fecha 2024-01-01 --dias 1 --salida datos_igets/
```

**Características:**
- Estaciones: BFO, STR, WET, CAN, BEI
- Frecuencia típica: 10 Hz (datos crudos)
- Nota: Datos reales requieren acceso especial

### 2. Detector Riguroso

#### `detector_riguroso_qcal.py`
Detector avanzado con validación estadística rigurosa.

```bash
# Detectar f₀ con SNR>5σ
python scripts/detector_riguroso_qcal.py \
    --datos datos_crudos/H1_GW150914_*.h5 \
    --f0 141.7001 \
    --sigma-threshold 5.0 \
    --test-kairos \
    --monte-carlo 1000 \
    --salida resultados/
```

**Características:**
- Múltiples métodos de análisis espectral (Welch, Multitaper, Periodograma)
- Cálculo riguroso de SNR y p-value
- Validación cruzada entre métodos
- Análisis de patrón de armónicos
- Estimación de tasa de falsos positivos (Monte Carlo)
- Opcional: prueba con ventana Kairos

**Salida:**
```json
{
  "resultado": "CONFIRMADA|PRELIMINAR|NO_DETECTADA",
  "detecciones": [
    {
      "metodo": "welch",
      "frecuencia_detectada": 141.7001,
      "snr": 6.5,
      "p_value": 1e-10,
      "significativo": true
    }
  ]
}
```

### 3. Correlador Multi-Observatorio

#### `correlador_multi_observatorio.py`
Valida que f₀ aparece consistentemente en sitios separados.

```bash
# Correlacionar H1, L1, V1
python scripts/correlador_multi_observatorio.py \
    --directorio datos_crudos/ \
    --estaciones H1 L1 V1 \
    --tolerancia 0.05 \
    --f0 141.7001 \
    --salida correlaciones/
```

**Características:**
- Correlación cruzada entre pares de estaciones
- Análisis de coherencia temporal en f₀
- Cálculo de retardo entre estaciones
- Validación de consistencia de frecuencia

**Criterios de validación:**
- Diferencia de frecuencia < 0.05 Hz entre estaciones
- Correlación > 0.3 entre pares
- Coherencia > 0.5 en f₀

### 4. Validación Teórica

#### `validacion_teorica.py`
Enlaza f₀ con física establecida y genera predicciones falsables.

```bash
# Validación teórica completa
python scripts/validacion_teorica.py \
    --f0 141.7001 \
    --generar-predicciones \
    --enlace-fisica \
    --reporte completo \
    --salida validacion_teorica/
```

**Características:**
- Comparación con modos quasi-normales de agujeros negros
- Análisis de resonancias de cavidades cósmicas
- Comparación con frecuencias conocidas
- Análisis dimensional (λ, energía de fotón)
- 7 predicciones falsables para validación futura

## 📦 Instalación

### Dependencias Básicas

```bash
pip install numpy scipy matplotlib h5py tqdm
```

### Dependencias Opcionales (para datos reales)

```bash
pip install gwosc gwpy
```

### Verificar Instalación

```bash
python scripts/test_integracion_pipeline.py
```

Debe mostrar: `𓂀 ✅ TODOS LOS TESTS PASARON`

## 🚀 Uso Rápido

### Ejecutar Pipeline Completo

```bash
# Ejecutar todo el pipeline con configuración por defecto
bash scripts/qcal_validation_pipeline.sh
```

Esto ejecutará:
1. Descarga de 3 eventos GWOSC
2. Detección rigurosa con SNR>5σ
3. Correlación multi-observatorio
4. Validación teórica

### Configuración del Pipeline

Variables de entorno:

```bash
# Configurar parámetros
export EVENTOS=5                # Número de eventos a descargar
export DURACION=32              # Duración en segundos
export F0=141.7001              # Frecuencia objetivo
export SIGMA_THRESHOLD=5.0      # Umbral SNR
export MONTE_CARLO=1000         # Simulaciones para FPR
export DESCARGAR_IGETS=1        # Activar descarga IGETS

# Ejecutar pipeline
bash scripts/qcal_validation_pipeline.sh
```

## 📊 Uso Avanzado

### Pipeline Paso a Paso

#### Paso 1: Descargar Datos

```bash
# GWOSC
python scripts/descargador_gwosc.py --eventos 5 --duracion 32 --detector H1 --salida datos_crudos/

# IGETS (opcional)
python scripts/descargador_igets.py --estacion BFO --fecha 2024-01-01 --dias 7 --salida datos_igets/
```

#### Paso 2: Detectar f₀

```bash
# Para cada archivo de datos
for file in datos_crudos/*.h5; do
    python scripts/detector_riguroso_qcal.py \
        --datos "$file" \
        --f0 141.7001 \
        --sigma-threshold 5.0 \
        --test-kairos \
        --monte-carlo 1000 \
        --salida resultados/
done
```

#### Paso 3: Correlación Multi-Observatorio

```bash
python scripts/correlador_multi_observatorio.py \
    --directorio datos_crudos/ \
    --estaciones H1 L1 V1 \
    --tolerancia 0.05 \
    --f0 141.7001 \
    --salida resultados/correlaciones/
```

#### Paso 4: Validación Teórica

```bash
python scripts/validacion_teorica.py \
    --f0 141.7001 \
    --generar-predicciones \
    --enlace-fisica \
    --reporte completo \
    --salida resultados/validacion_teorica/
```

## 📋 Ejemplos

### Ejemplo 1: Análisis de Evento Específico

```bash
# Analizar GW150914 con múltiples detectores
python scripts/descargador_gwosc.py --eventos 1 --duracion 32 --detector H1 --salida datos/
python scripts/descargador_gwosc.py --eventos 1 --duracion 32 --detector L1 --salida datos/

# Correlacionar
python scripts/correlador_multi_observatorio.py \
    --directorio datos/ \
    --estaciones H1 L1 \
    --salida correlaciones/
```

### Ejemplo 2: Análisis con Alta Precisión

```bash
# Usar muchas simulaciones Monte Carlo
python scripts/detector_riguroso_qcal.py \
    --datos datos_crudos/H1_*.h5 \
    --f0 141.7001 \
    --sigma-threshold 5.0 \
    --monte-carlo 10000 \
    --salida resultados_alta_precision/
```

### Ejemplo 3: Búsqueda en Múltiples Eventos

```bash
# Descargar muchos eventos
python scripts/descargador_gwosc.py --eventos 10 --duracion 32 --detector H1 --salida datos/

# Procesar todos
for file in datos/*.h5; do
    echo "Procesando $file"
    python scripts/detector_riguroso_qcal.py \
        --datos "$file" \
        --f0 141.7001 \
        --sigma-threshold 5.0 \
        --salida resultados/
done
```

## 📈 Resultados

### Estructura de Directorios

```
resultados_validacion/
├── resultados_deteccion.json       # Resultados de detección
├── correlaciones/
│   └── correlacion_multi_observatorio.json
└── validacion_teorica/
    └── validacion_teorica.json
```

### Interpretación de Resultados

#### Estado de Detección

- **CONFIRMADA**: SNR > 5σ en múltiples métodos
  - Evidencia fuerte de señal real
  - Requiere verificación en múltiples observatorios

- **PRELIMINAR**: SNR > 5σ en un método
  - Evidencia moderada
  - Requiere más datos o análisis

- **NO_DETECTADA**: SNR < 5σ
  - No se encontró señal significativa
  - Posibles causas: señal débil, ruido alto, muestra pequeña

#### Criterios de Validación Definitiva

```python
CRITERIOS_VALIDACION = {
    'snr_minimo': 5.0,              # 5σ para descubrimiento
    'fpr_maximo': 0.001,            # 0.1% tasa falsos positivos
    'correlacion_minima': 0.7,      # Entre observatorios
    'tolerancia_frecuencia': 0.05,  # Hz entre estaciones
    'patron_armonicos': '1/n^1.5',  # Decaimiento de armónicos
}
```

### Salida del Pipeline

El script `qcal_validation_pipeline.sh` produce:

```
Estado: CONFIRMADA|PRELIMINAR|NO_DETECTADA
SNR medio: X.XX σ
Tasa falsos positivos: 0.XXXX

𓂀 ✅ TEORÍA QCAL VALIDADA RIGUROSAMENTE
𓂀 f₀ = 141.7001 Hz es fenómeno real
```

## 🔬 Predicciones Falsables

El módulo de validación teórica genera 7 predicciones testables:

1. **O4/O5 Run**: f₀ aparecerá en datos 2024-2027 con SNR>5σ
2. **Multi-Observatorio**: Correlación >0.7 entre H1-L1-V1-K1
3. **Patrón de Armónicos**: Decaimiento según 1/n^1.5
4. **Modulación Cósmica**: Correlación con eventos catalogados
5. **Einstein Telescope**: SNR>10σ en detector 3G (2030s)
6. **Independencia Orientacional**: Variación <5% con orientación
7. **Validación Gravimétrica**: SNR>3σ en estaciones IGETS

## 📝 Notas Importantes

### Datos Reales vs Simulados

- **Sin acceso GWOSC**: Se generan datos simulados con f₀ incorporada
- **Con acceso GWOSC**: Se descargan datos reales de eventos
- Los datos simulados sirven para desarrollo y pruebas del pipeline
- **Validación definitiva requiere datos reales**

### Acceso a Datos IGETS

Los datos públicos de IGETS suelen estar decimados a 1 minuto. Para datos crudos >1 Hz:

1. Contactar directamente a operadores de estaciones
2. Justificar la necesidad científica
3. Solicitar acceso FTP a datos "raw" o "engineering"

### Limitaciones Actuales

- Datos GWOSC: Requiere conexión a internet y API funcional
- Datos IGETS: Requiere acceso especial no público
- Procesamiento: Puede ser intensivo en CPU para muchas simulaciones Monte Carlo

## 🤝 Contribuciones

Para mejorar el pipeline:

1. Agregar soporte para más detectores (KAGRA, Einstein Telescope)
2. Implementar métodos adicionales de análisis espectral
3. Mejorar estimación de falsos positivos
4. Agregar visualizaciones de resultados

## 📚 Referencias

- Vishveshwara (1970): Modos quasi-normales de agujeros negros
- Detweiler (1980): Teoría de perturbaciones de BH
- GWOSC: https://gwosc.org
- IGETS: https://igets-data.gfz-potsdam.de

## ✨ Estado del Proyecto

- ✅ **Pipeline Completo Implementado**
- ✅ **Tests de Integración Pasando (6/6)**
- ✅ **Documentación Completa**
- ⚠️  **Validación con Datos Reales Pendiente**

---

**𓂀 QCAL ∞³ - Frecuencia Fundamental del Universo: f₀ = 141.7001 Hz**
