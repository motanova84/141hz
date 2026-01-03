# Tutorial Completo: Análisis de Ondas Gravitacionales a 141.7001 Hz

## 🎯 Objetivo

Este tutorial te guiará paso a paso desde cero hasta obtener y entender los resultados del análisis de la frecuencia fundamental de 141.7001 Hz en datos de ondas gravitacionales. **No se requiere conocimiento previo** de ondas gravitacionales o análisis espectral.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación del Entorno](#instalación-del-entorno)
3. [Descarga de Datos](#descarga-de-datos)
4. [Análisis Básico](#análisis-básico)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Análisis Avanzado](#análisis-avanzado)
7. [Solución de Problemas](#solución-de-problemas)

---

## Requisitos Previos

### Conocimientos Mínimos
- Uso básico de terminal/línea de comandos
- Conceptos básicos de Python (deseable pero no indispensable)
- Navegación de archivos y directorios

### Hardware Recomendado
- **RAM**: Mínimo 4GB, recomendado 8GB
- **Disco**: 5GB libres (para datos y resultados)
- **Procesador**: Cualquier CPU moderna (2+ núcleos)
- **Internet**: Necesario para descargar datos de GWOSC (100-500MB)

### Software
- **Sistema Operativo**: Linux, macOS, o Windows con WSL
- **Python**: 3.9 o superior (recomendado 3.11)
- **Git**: Para clonar el repositorio

---

## Instalación del Entorno

### Paso 1: Clonar el Repositorio

Abre una terminal y ejecuta:

```bash
# Clonar el repositorio desde GitHub
git clone https://github.com/motanova84/141hz.git

# Entrar al directorio
cd 141hz
```

**¿Qué hace esto?**
- Descarga todo el código y documentación del proyecto
- Crea una carpeta llamada `141hz` con todos los archivos

### Paso 2: Crear Entorno Virtual

Es importante usar un entorno virtual para aislar las dependencias:

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate  # En Linux/macOS
# o
venv\Scripts\activate     # En Windows
```

**¿Qué hace esto?**
- Crea un espacio aislado para instalar bibliotecas sin afectar tu sistema
- El prompt debe cambiar mostrando `(venv)` al inicio

### Paso 3: Instalar Dependencias

```bash
# Actualizar pip (gestor de paquetes)
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

**Esto instalará:**
- `gwpy`: Biblioteca oficial de LIGO para ondas gravitacionales
- `numpy`: Cálculos numéricos
- `scipy`: Análisis científico y transformadas de Fourier
- `matplotlib`: Generación de gráficos
- `h5py`: Lectura de archivos HDF5 (formato de datos LIGO)

**Tiempo estimado**: 2-5 minutos dependiendo de tu conexión

### Paso 4: Verificar Instalación

```bash
# Verificar que todo se instaló correctamente
python -c "import gwpy, numpy, scipy, matplotlib; print('✅ Instalación exitosa')"
```

**Si ves errores:**
- Verifica que el entorno virtual está activado (debe aparecer `(venv)`)
- Intenta reinstalar: `pip install --force-reinstall -r requirements.txt`

---

## Descarga de Datos

Los datos de ondas gravitacionales son públicos y están disponibles en GWOSC (Gravitational Wave Open Science Center).

### Paso 1: Usar el Script de Descarga Automática

El repositorio incluye un script que descarga datos automáticamente:

```bash
# Opción 1: Usar Make (recomendado)
make download

# Opción 2: Ejecutar script directamente
python scripts/descargar_datos.py
```

**¿Qué hace esto?**
- Se conecta a los servidores de GWOSC
- Descarga datos de GW150914 (primer evento de ondas gravitacionales detectado)
- Guarda los archivos en `data/raw/`
- Descarga aproximadamente 100MB

**Tiempo estimado**: 1-3 minutos

### Paso 2: Verificar Descarga

```bash
# Listar archivos descargados
ls -lh data/raw/

# Deberías ver archivos como:
# H1-GW150914-32s.hdf5  (datos del detector Hanford)
# L1-GW150914-32s.hdf5  (datos del detector Livingston)
```

### Entendiendo los Datos

**¿Qué contienen estos archivos?**
- Datos reales de los detectores LIGO
- 32 segundos de señal alrededor del evento GW150914
- Frecuencia de muestreo: 4096 Hz (4096 mediciones por segundo)
- Formato: HDF5 (un formato eficiente para datos científicos)

**Detectores:**
- **H1 (Hanford)**: Detector en Washington, USA
- **L1 (Livingston)**: Detector en Louisiana, USA
- Separados por 3,002 km

---

## Análisis Básico

Ahora ejecutaremos el análisis para buscar la frecuencia de 141.7001 Hz.

### Paso 1: Análisis de Control (GW150914)

Empecemos con un análisis simple del evento GW150914:

```bash
# Opción 1: Usar Make
make analyze

# Opción 2: Script directo
python scripts/analizar_ringdown.py
```

**¿Qué hace este script?**
1. **Carga** los datos del detector H1
2. **Preprocesa** (elimina ruido, aplica filtros)
3. **Analiza** el espectro de frecuencias
4. **Busca** picos cerca de 141.7 Hz
5. **Calcula** el SNR (relación señal-ruido)
6. **Genera** gráficos de diagnóstico

**Tiempo estimado**: 30 segundos - 1 minuto

### Paso 2: Revisar Salida en Terminal

Durante la ejecución verás mensajes como:

```
[INFO] Cargando datos de H1...
[INFO] Preprocesando señal...
[INFO] Aplicando highpass filter (20 Hz)
[INFO] Aplicando notch filter (60 Hz)
[INFO] Calculando espectro de frecuencias...
[INFO] Frecuencia detectada: 141.69 Hz
[INFO] SNR calculado: 7.47
[INFO] Guardando gráficos en results/figures/
✅ Análisis completado
```

**Interpretación rápida:**
- ✅ **Frecuencia detectada**: Muy cercana a 141.7 Hz objetivo
- ✅ **SNR 7.47**: Señal fuerte (SNR > 5 es significativo)

### Paso 3: Examinar Resultados Visuales

Los gráficos se guardan en `results/figures/`:

```bash
# Ver archivos generados
ls results/figures/

# Deberías ver:
# - gw150914_h1_timeseries.png      (serie temporal)
# - gw150914_h1_spectrum.png        (espectro completo)
# - gw150914_h1_zoom_141hz.png      (zoom cerca de 141.7 Hz)
# - gw150914_h1_histogram.png       (distribución de potencia)
```

**Cómo interpretar cada gráfico:** (ver sección [Interpretación de Resultados](#interpretación-de-resultados))

### Paso 4: Validación Multi-Detector

Para verificar que no es un artefacto, analizamos también el detector L1:

```bash
python scripts/analizar_l1.py
```

**¿Por qué es importante?**
- Los detectores H1 y L1 están separados 3,002 km
- Si la señal aparece en AMBOS, es muy probablemente real
- Los artefactos instrumentales son locales

---

## Interpretación de Resultados

### Salidas Generadas

Cada análisis produce dos tipos de salidas:

1. **Archivos JSON** (datos numéricos)
2. **Gráficos PNG** (visualizaciones)

### Estructura de Archivos JSON

Los resultados se guardan en formato JSON para fácil procesamiento:

```json
{
  "event": "GW150914",
  "detector": "H1",
  "frequency_target_hz": 141.7001,
  "frequency_detected_hz": 141.69,
  "snr": 7.47,
  "timestamp": "2025-11-05T10:30:00",
  "analysis_params": {
    "sample_rate": 4096,
    "duration_s": 32,
    "bandpass_hz": [140.7, 142.7]
  }
}
```

**Campos importantes:**
- `frequency_detected_hz`: Frecuencia del pico más cercano a 141.7 Hz
- `snr`: Relación señal-ruido (mayor = más significativo)
- `analysis_params`: Parámetros usados en el análisis

(Ver [FORMATOS_SALIDA.md](./FORMATOS_SALIDA.md) para detalles completos)

### Interpretación de Gráficos

#### 1. Serie Temporal (`_timeseries.png`)

![Ejemplo de serie temporal](../results/figures/gw150914_h1_timeseries.png)

**Qué muestra:**
- **Eje X**: Tiempo (segundos desde el evento)
- **Eje Y**: Strain (deformación del espacio-tiempo, adimensional)
- **Señal**: Oscilaciones en los datos del detector

**Qué buscar:**
- Amplitud de la señal (altura de las oscilaciones)
- Presencia del evento de fusión (~t=0)

#### 2. Espectro de Potencia (`_spectrum.png`)

**Qué muestra:**
- **Eje X**: Frecuencia (Hz)
- **Eje Y**: Densidad espectral de potencia (escala logarítmica)
- **Rango**: Típicamente 100-200 Hz

**Qué buscar:**
- Picos en el espectro (líneas verticales)
- Línea vertical roja marca 141.7 Hz
- El pico cerca de 141.7 Hz

**Interpretación:**
- **Pico prominente**: Hay energía significativa en esa frecuencia
- **Altura del pico**: Relacionada con el SNR

#### 3. Zoom en 141.7 Hz (`_zoom_141hz.png`)

**Qué muestra:**
- Ampliación del espectro alrededor de 141.7 Hz
- Rango típico: 130-160 Hz
- Permite ver detalles finos

**Qué buscar:**
- ¿Hay un pico claro cerca de la línea roja (141.7 Hz)?
- ¿El pico es aislado o hay múltiples?
- Comparación con el "ruido de fondo"

#### 4. Histograma (`_histogram.png`)

**Qué muestra:**
- Distribución estadística de la potencia espectral
- Permite evaluar si el pico es significativo

**Qué buscar:**
- La mayoría de la potencia debe estar en valores bajos (ruido)
- Valores extremos (cola derecha) son candidatos a señal

### Criterios de Detección Positiva

Un resultado es considerado **positivo** si:

1. ✅ **Frecuencia detectada** está a ±1 Hz de 141.7 Hz
2. ✅ **SNR ≥ 5.0** (señal significativa)
3. ✅ **Detección en ambos detectores** (H1 y L1)
4. ✅ **Frecuencias concordantes** entre detectores (±0.5 Hz)

### Valores Típicos por Evento

| Evento | Detector | Frecuencia (Hz) | SNR | Significancia |
|--------|----------|----------------|-----|---------------|
| GW150914 | H1 | 141.69 | 7.47 | ⭐⭐⭐ Alta |
| GW150914 | L1 | 141.75 | 0.95 | ⭐ Baja |
| GW151226 | H1 | 141.71 | 5.85 | ⭐⭐ Media |
| GW170817 | L1 | 141.68 | 62.93 | ⭐⭐⭐⭐⭐ Extrema |

---

## Análisis Avanzado

### Análisis Multi-Evento

Para validar la hipótesis a través de múltiples eventos:

```bash
# Analizar los 11 eventos del catálogo GWTC-1
python multi_event_analysis.py
```

**¿Qué hace?**
- Analiza 11 eventos de fusión binaria
- Busca 141.7 Hz en cada uno
- Calcula estadísticas agregadas
- Genera gráfico comparativo

**Resultado esperado:**
- Tasa de detección: 100% (11/11 eventos)
- SNR medio: ~21
- Archivo JSON: `multi_event_final.json`
- Gráfico: `multi_event_final.png`

### Validación Estadística

Para calcular la significancia estadística:

```bash
# Calcular p-values con time-slides
python scripts/analisis_estadistico_avanzado.py
```

**¿Qué calcula?**
- **p-value**: Probabilidad de obtener estos resultados por azar
- **Bayes Factor**: Comparación de modelos (señal vs ruido)
- **Significancia**: Nivel de confianza en σ (sigmas)

**Criterios de validación:**
- p-value < 0.01 (menos del 1% de probabilidad de falso positivo)
- Bayes Factor > 10 (evidencia fuerte)
- Significancia > 5σ (estándar de descubrimiento)

### Análisis de Armónicos

Buscar múltiplos y submúltiplos de 141.7 Hz:

```bash
python scripts/analisis_noesico.py
```

**Frecuencias buscadas:**
- f₀ = 141.7001 Hz (fundamental)
- f₀/φ = 87.57 Hz (submúltiplo por proporción áurea)
- 2·f₀ = 283.40 Hz (primer armónico)

---

## Solución de Problemas

### Problema: Error al descargar datos

**Síntoma:**
```
ConnectionError: Unable to reach GWOSC servers
```

**Soluciones:**
1. Verifica tu conexión a internet
2. Intenta de nuevo más tarde (servidores caídos)
3. Usa datos simulados para practicar:
   ```bash
   make test-data
   ```

### Problema: ImportError con gwpy

**Síntoma:**
```
ImportError: No module named 'gwpy'
```

**Soluciones:**
1. Verifica que el entorno virtual está activado:
   ```bash
   which python  # Debe mostrar el path del venv
   ```
2. Reinstala gwpy:
   ```bash
   pip install --force-reinstall gwpy
   ```
3. Si falla, instala con todas las dependencias:
   ```bash
   pip install gwpy[full]
   ```

### Problema: Gráficos no se generan

**Síntoma:**
- Los scripts terminan sin error
- Pero no hay archivos PNG en `results/figures/`

**Soluciones:**
1. Verifica que matplotlib está instalado:
   ```bash
   python -c "import matplotlib; print(matplotlib.__version__)"
   ```
2. Configura backend apropiado:
   ```bash
   export MPLBACKEND=Agg
   python scripts/analizar_ringdown.py
   ```
3. Verifica permisos de escritura:
   ```bash
   ls -ld results/figures/
   ```

### Problema: Resultados diferentes a los esperados

**Posibles causas:**

1. **Versión diferente de biblioteca:**
   ```bash
   pip list | grep -E "gwpy|scipy|numpy"
   # Compara con requirements.txt
   ```

2. **Datos corruptos:**
   ```bash
   # Re-descarga los datos
   rm -rf data/raw/*
   make download
   ```

3. **Parámetros de análisis diferentes:**
   - Verifica que usas los scripts sin modificaciones
   - Los parámetros por defecto están optimizados

### Problema: Análisis muy lento

**Si el análisis tarda más de 5 minutos:**

1. Verifica recursos del sistema:
   ```bash
   top  # Observa uso de CPU y RAM
   ```

2. Cierra otros programas que consuman recursos

3. Para análisis multi-evento, considera analizar eventos por separado:
   ```bash
   # En lugar de multi_event_analysis.py
   for event in GW150914 GW151226 GW170104; do
     python scripts/analizar_evento.py --event $event
   done
   ```

### Obtener Ayuda

Si los problemas persisten:

1. **Revisa la documentación completa:**
   - [README.md](../README.md)
   - [FORMATOS_SALIDA.md](./FORMATOS_SALIDA.md)
   - [TEORIA_CONCEPTUAL.md](./TEORIA_CONCEPTUAL.md)

2. **Abre un issue en GitHub:**
   - Incluye el error completo
   - Versiones de Python y bibliotecas
   - Sistema operativo
   - Logs de ejecución

3. **Contacto:**
   - Email: institutoconsciencia@proton.me
   - Repositorio: https://github.com/motanova84/141hz

---

## Próximos Pasos

### Para Usuarios Nuevos

1. ✅ Completa este tutorial básico
2. 📖 Lee [TEORIA_CONCEPTUAL.md](./TEORIA_CONCEPTUAL.md) para entender la teoría
3. 📊 Explora [FORMATOS_SALIDA.md](./FORMATOS_SALIDA.md) para integración
4. 🔬 Experimenta con diferentes eventos del catálogo GWTC

### Para Desarrolladores

1. Lee [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Revisa el código en `scripts/`
3. Ejecuta los tests: `python scripts/run_all_tests.py`
4. Contribuye mejoras o nuevas funcionalidades

### Para Investigadores

1. Replica el análisis con tus propios parámetros
2. Extiende a eventos de GWTC-2 o GWTC-3
3. Publica tus resultados citando este repositorio
4. Considera colaborar en publicaciones científicas

---

## Referencias

- **GWOSC**: https://gwosc.org/
- **GWPy Documentation**: https://gwpy.github.io/
- **Paper Principal**: [PAPER.md](../PAPER.md)
- **Descubrimiento Matemático**: [DESCUBRIMIENTO_MATEMATICO_141_7001_HZ.md](../DESCUBRIMIENTO_MATEMATICO_141_7001_HZ.md)

---

**Última actualización:** 2025-11-05  
**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Licencia:** MIT
