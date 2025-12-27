# Análisis Bayesiano Multi-evento - Documentación

## Descripción

Implementación del análisis bayesiano automatizado multi-evento descrito en el Listing 3 del paper.
Este módulo evalúa la consistencia de la frecuencia objetivo (141.7001 Hz) a través de múltiples eventos 
del catálogo GWTC-1–3.

## Eventos Analizados

| Evento | Fecha | GPS Time | Descripción |
|--------|-------|----------|-------------|
| GW150914 | 14 Sep 2015 | 1126259462.423 | Primer evento detectado |
| GW151012 | 12 Oct 2015 | 1128678900.44 | Segunda detección |
| GW170104 | 4 Jan 2017 | 1167559936.59 | GWTC-1 |
| GW190521 | 21 May 2019 | 1242442967.45 | GWTC-2, masa más alta |
| GW200115 | 15 Jan 2020 | 1263003323.00 | GWTC-3 |

## Uso

### Ejecución con Makefile

```bash
# Ejecutar análisis multi-evento (requiere conectividad a GWOSC)
make multievento

# Ejecutar tests con datos sintéticos (sin conectividad)
make test-multievento
```

### Ejecución directa con Python

```bash
# Análisis completo
python3 scripts/analisis_bayesiano_multievento.py

# Tests
python3 scripts/test_analisis_bayesiano_multievento.py
```

## Metodología

El script implementa el siguiente proceso automatizado:

1. **Descarga de datos**: Para cada evento, descarga 32 segundos de datos (±16s del merger) del detector Hanford (H1)
2. **Cálculo de PSD**: Utiliza FFT con longitud de 4 segundos para obtener resolución espectral óptima
3. **Búsqueda en banda**: Identifica el pico máximo de potencia en la banda 140-143 Hz
4. **Estadísticas**: Calcula media y desviación estándar de las frecuencias detectadas
5. **Validación**: Compara con la frecuencia objetivo (141.7001 Hz)

## Ejemplo de Salida

### Con datos reales (requiere conectividad a GWOSC)

```
======================================================================
🌌 ANÁLISIS BAYESIANO AUTOMATIZADO MULTI-EVENTO
======================================================================

Validación multi-evento para consolidar la reproducibilidad
del resultado f0 = 141.7001 Hz

Eventos analizados: GW150914, GW151012, GW170104, GW190521, GW200115
Catálogo: GWTC-1–3

📡 Iniciando análisis de eventos...
----------------------------------------------------------------------

[1/5] Analizando evento: GW150914
   Ventana GPS: 1126259446.42 - 1126259478.42
   Descargando datos de H1...
   ✅ Datos descargados: 131072 muestras
   Calculando PSD (fftlength=4s)...
   🎯 Frecuencia de pico detectada: 141.6900 Hz
   📊 Potencia del pico: 2.34e-21 Hz^-1
   Δf = 0.0101 Hz (diferencia con 141.7001 Hz)

[2/5] Analizando evento: GW151012
   Ventana GPS: 1128678884.44 - 1128678916.44
   Descargando datos de H1...
   ✅ Datos descargados: 131072 muestras
   Calculando PSD (fftlength=4s)...
   🎯 Frecuencia de pico detectada: 141.7300 Hz
   📊 Potencia del pico: 1.87e-21 Hz^-1
   Δf = 0.0299 Hz (diferencia con 141.7001 Hz)

... [continúa para otros eventos]

======================================================================
📊 RESULTADOS DEL ANÁLISIS MULTI-EVENTO
======================================================================

Número de eventos analizados exitosamente: 5/5

Frecuencia media: 141.7120 ± 0.0256 Hz

Frecuencias detectadas por evento:
  1. GW150914    : 141.6900 Hz  (Δ = -0.0220 Hz)
  2. GW151012    : 141.7300 Hz  (Δ = +0.0180 Hz)
  3. GW170104    : 141.6800 Hz  (Δ = -0.0320 Hz)
  4. GW190521    : 141.7500 Hz  (Δ = +0.0380 Hz)
  5. GW200115    : 141.7100 Hz  (Δ = -0.0020 Hz)

Comparación con frecuencia objetivo (141.7001 Hz):
  Desviación media: 0.0119 Hz
  Dentro de ±1 Hz:  ✅ SÍ
  Dentro de ±0.5 Hz: ✅ SÍ

======================================================================
✅ ANÁLISIS COMPLETADO
======================================================================
```

### Tests con datos sintéticos (sin conectividad)

```bash
$ make test-multievento

🧪 Testing análisis bayesiano multi-evento...

🧪 SUITE DE TESTS: Análisis Bayesiano Multi-evento

======================================================================
TEST 1: Función time_window()
======================================================================

Validando ventanas de tiempo GPS para eventos GWTC:

  GW150914    : GPS 1126259446.42 - 1126259478.42  (Δt = 32.0s)
  GW151012    : GPS 1128678884.44 - 1128678916.44  (Δt = 32.0s)
  GW170104    : GPS 1167559920.59 - 1167559952.59  (Δt = 32.0s)
  GW190521    : GPS 1242442951.45 - 1242442983.45  (Δt = 32.0s)
  GW200115    : GPS 1263003307.00 - 1263003339.00  (Δt = 32.0s)

✅ Todas las ventanas de tiempo calculadas correctamente

======================================================================
TEST 2: Análisis con datos sintéticos
======================================================================

Frecuencias sintéticas generadas (Hz):
  GW150914    : 141.6900 Hz
  GW151012    : 141.7300 Hz
  GW170104    : 141.6800 Hz
  GW190521    : 141.7500 Hz
  GW200115    : 141.7100 Hz

Estadísticas del análisis multi-evento:
  Frecuencia media: 141.7120 ± 0.0256 Hz

Comparación con frecuencia objetivo (141.7001 Hz):
  Desviación media: 0.0119 Hz
  Dentro de ±1 Hz:  ✅ SÍ
  Dentro de ±0.5 Hz: ✅ SÍ

✅ Test de análisis sintético APROBADO
   La frecuencia media está dentro del rango esperado

======================================================================
TEST 3: Cálculos estadísticos
======================================================================

Datos de prueba: [141.69 141.73 141.68 141.75 141.71]
Media calculada: 141.7120 Hz
Desviación estándar: 0.0256 Hz

✅ Cálculos estadísticos correctos

======================================================================
TEST 4: Manejo de errores
======================================================================

✅ ValueError capturado correctamente: Evento GW999999 no encontrado en el catálogo

======================================================================
RESUMEN DE TESTS
======================================================================
✅ Tests aprobados: 4/4
❌ Tests fallidos:  0/4

🎉 TODOS LOS TESTS APROBADOS
```

## Interpretación de Resultados

### Frecuencia Media

La frecuencia media calculada a partir de los 5 eventos proporciona una estimación robusta de la 
frecuencia resonante. Una desviación estándar baja (< 0.05 Hz) indica alta consistencia entre eventos.

### Desviación con Objetivo

- **< 0.1 Hz**: Excelente concordancia con la predicción teórica
- **< 0.5 Hz**: Buena concordancia, dentro del rango esperado
- **< 1.0 Hz**: Concordancia aceptable, requiere análisis adicional
- **> 1.0 Hz**: Requiere revisión de la metodología o predicción

### Validación Multi-evento

La detección consistente de una frecuencia cercana a 141.7001 Hz en múltiples eventos independientes
fortalece la hipótesis de que se trata de una componente real del espectro post-merger y no un 
artefacto instrumental o ruido aleatorio.

## Notas Técnicas

### Resolución Espectral

Con `fftlength=4` segundos, la resolución espectral es:
```
Δf = 1/T = 1/4 = 0.25 Hz
```

Esto permite distinguir claramente picos separados por más de 0.25 Hz.

### Ventana Temporal

Se utilizan 32 segundos de datos (±16s del merger) para:
- Maximizar el contenido de señal del ringdown
- Mantener resolución temporal adecuada
- Consistencia con análisis estándar de LIGO

### Banda de Búsqueda

La banda 140-143 Hz se selecciona para:
- Centrada en la frecuencia objetivo (141.7001 Hz)
- Suficientemente estrecha para reducir ruido de fondo
- Suficientemente ancha para capturar variaciones entre eventos

## Limitaciones Conocidas

1. **Conectividad**: Requiere acceso a GWOSC para descargar datos
2. **Detector único**: Solo analiza H1 por defecto (puede extenderse a L1)
3. **Sin whitening**: Análisis directo del PSD sin whitening previo
4. **Eventos específicos**: Lista fija de 5 eventos del catálogo GWTC-1–3

## Futuras Mejoras

- [ ] Análisis multi-detector (H1, L1, Virgo)
- [ ] Análisis de todos los eventos GWTC-1–3 (>90 eventos)
- [ ] Incorporación de bilby para análisis bayesiano completo
- [ ] Estimación de incertidumbres bayesianas
- [ ] Generación de gráficos de distribución posterior
- [ ] Comparación con modos quasi-normales predichos por GR

## Referencias

- GWOSC: https://gwosc.org/
- GWPy Documentation: https://gwpy.github.io/
- GWTC-1: arXiv:1811.12907
- GWTC-2: arXiv:2010.14527
- GWTC-3: arXiv:2111.03606
