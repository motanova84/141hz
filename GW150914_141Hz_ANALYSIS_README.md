# Análisis de GW150914: Búsqueda de Resonancia a 141.7 Hz

## 📋 Descripción

Este script implementa un análisis científico completo del evento de ondas gravitacionales GW150914 para detectar y caracterizar potenciales resonancias a 141.7 Hz en la fase de post-merger (ringdown).

## 🎯 Objetivos

1. **Cargar datos reales** de GW150914 desde GWOSC
2. **Analizar el espectro post-merger** en la ventana de 10ms a 500ms después del pico
3. **Calcular significancia estadística** mediante Monte Carlo
4. **Evaluar coherencia** entre detectores H1 y L1
5. **Generar visualizaciones** completas del análisis
6. **Producir reporte científico** detallado

## 📊 Componentes Principales

### 1. Carga y Verificación de Datos
- Descarga automática desde GWOSC
- Ventana de 4 segundos alrededor del evento
- Tasa de muestreo: 4096 Hz
- Detectores: H1 (Hanford) y L1 (Livingston)

### 2. Análisis Espectrotemporal
- **PSD (Power Spectral Density)**: Caracterización del ruido
- **Q-transform**: Análisis tiempo-frecuencia
- **FFT**: Análisis espectral en 130-160 Hz
- **SNR**: Relación señal-ruido en banda estrecha (±0.1 Hz)

### 3. Análisis Estadístico
- **Distribución de Rayleigh**: Modelo de ruido gaussiano
- **Monte Carlo**: 10,000 simulaciones para FAP
- **P-value**: Probabilidad de falsa alarma
- **Significancia**: Conversión a unidades sigma (σ)

### 4. Análisis de Coherencia
- **Fase relativa**: Entre H1 y L1
- **SNR combinado**: √(SNR_H1² + SNR_L1²)
- **Comparación instrumental**: Líneas conocidas (60 Hz, 141.65 Hz, etc.)
- **Estimación energética**: Energía radiada si fuera señal real

### 5. Análisis Avanzado

#### FFT Interpolación
- Zero-padding (factor 4x)
- Resolución mejorada: Δf ~ 0.5 Hz → 0.125 Hz
- Precisión espectral aumentada

#### Coherencia Espectral H1-L1
- Producto coherente: FFT_H1 × conj(FFT_L1)
- Coherencia normalizada
- Criterio: >0.5 indica señal astrofísica

#### Filtro de Adaptación por Resonancia (Ψ-NSE v1.0)
- Filtro Butterworth de 4to orden
- Centrado en 141.7 Hz
- Factor Q = 100
- Ancho de banda: ~1.4 Hz

#### Triangulación de Fase Relativista
- Diferencia de fase H1-L1
- Tiempo de retraso implícito
- Comparación con tiempo de luz (~10 ms)
- Validación de origen astrofísico

### 6. Visualización Completa (9 Subplots)

1. **Serie temporal post-merger**: Strain vs tiempo
2. **Espectro de potencia**: √PSD vs frecuencia
3. **Q-transform**: Mapa tiempo-frecuencia
4. **Zoom espectral**: 130-160 Hz
5. **Distribución de ruido**: Histograma + ajuste Rayleigh
6. **Comparación QNM**: Frecuencias teóricas vs observadas
7. **Coherencia de fase**: Diagrama polar H1-L1
8. **Métricas de significancia**: SNR, P-value, FAP, σ
9. **Resumen ejecutivo**: Resultados clave

### 7. Reporte Científico

Genera un reporte completo en formato texto con:
- **Datos y métodos**: Parámetros del análisis
- **Resultados principales**: SNR, coherencia, significancia
- **Comparación teórica**: QNM de Kerr vs 141.7 Hz
- **Conclusiones**: Interpretación física
- **Límites y sistemáticas**: Fuentes de incertidumbre
- **Protocolo de verificación**: Instrucciones para reproducir

## 🚀 Uso

### Requisitos

```bash
pip install gwpy astropy scipy matplotlib h5py numpy
```

### Ejecución

```bash
python analizar_gw150914_1417hz.py
```

### Archivos de Salida

- `gw150914_1417Hz_analysis.png`: Visualización completa (9 subplots)
- `GW150914_1417Hz_Analysis_Report.txt`: Reporte científico detallado

## 📈 Interpretación de Resultados

### Criterios de Detección

- **SNR > 8.0**: Umbral mínimo para detección
- **Significancia > 5σ**: Umbral para descubrimiento
- **Coherencia > 0.5**: Consistencia entre detectores
- **Retardo < 10 ms**: Compatibilidad con señal astrofísica

### Comparación con QNM Teóricos

| Modo | Frecuencia Teórica | Observado | Desviación |
|------|-------------------|-----------|------------|
| l=2,m=2,n=0 | 251.0 ± 3.1 Hz | 141.7 Hz | -43.6% |
| l=2,m=2,n=1 | 415.0 ± 5.3 Hz | - | - |
| l=3,m=3,n=0 | 484.0 ± 6.0 Hz | - | - |

### Posibles Resultados

#### ✅ HALLAZGO SIGNIFICATIVO (SNR > 8, σ > 5)
- Evidencia de potencia espectral anómala a 141.7 Hz
- Coherencia entre detectores compatible con origen astrofísico
- Desviación del -43.6% respecto a predicciones de Relatividad General
- Requiere análisis independiente para confirmación

#### ❌ NO DETECCIÓN (SNR < 8 o σ < 5)
- No evidencia convincente de señal a 141.7 Hz
- Potencia observada compatible con fluctuaciones de ruido
- Se establece límite superior en amplitud posible
- Requiere mayor sensibilidad instrumental

## 🔬 Validación y Reproducibilidad

### Tests Incluidos

```bash
python test_analizar_gw150914_1417hz.py
```

Verifica:
- ✅ Dependencias instaladas
- ✅ Sintaxis del script
- ✅ Definición de funciones
- ✅ Parámetros de GW150914
- ✅ Análisis con datos sintéticos

### Reproducibilidad

Para verificación independiente:

1. Descargar datos:
```python
from gwpy.timeseries import TimeSeries
strain = TimeSeries.fetch_open_data('H1', 1126259460.4, 1126259464.4)
```

2. Ejecutar análisis:
```bash
python analizar_gw150914_1417hz.py
```

3. Comparar con reporte generado

## 📚 Referencias

- **Abbott et al. 2016**, *PRL 116, 061102*: Observación de GW150914
- **Berti et al. 2009**, *PRD 93, 124051*: Modos quasi-normales de agujeros negros de Kerr
- **GWOSC**: https://www.gw-openscience.org/
- **GWpy Documentation**: https://gwpy.github.io/

## 🎓 Parámetros Oficiales de GW150914

| Parámetro | Valor |
|-----------|-------|
| GPS Time | 1126259462.4 |
| Masa M1 | 35.6 M☉ |
| Masa M2 | 30.6 M☉ |
| Masa Final | 67.6 M☉ |
| Spin Final | 0.69 |
| Distancia | 410 Mpc |
| Frecuencia Merger | 150 Hz |

## 🔧 Mejoras Futuras

- [ ] Análisis poblacional (GWTC-1, GWTC-2, GWTC-3)
- [ ] Inclusión de Virgo (V1) para GW170814
- [ ] Análisis Bayesiano de parámetros
- [ ] Comparación con plantillas numéricas (NR)
- [ ] Búsqueda en múltiples frecuencias armónicas
- [ ] Análisis de efectos no lineales
- [ ] Modelado de líneas instrumentales

## 👥 Contribuciones

Este script es parte del proyecto QCAL de análisis de ondas gravitacionales.

**Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)  
**Fecha**: Enero 2026  
**Repositorio**: https://github.com/motanova84/141hz

## 📝 Licencia

Ver archivo LICENSE en el repositorio principal.

## 🆘 Soporte

Para problemas o preguntas:
1. Verificar conexión a GWOSC
2. Verificar instalación de dependencias
3. Revisar logs de error
4. Contactar a los mantenedores del proyecto

---

**Nota**: Este análisis es de naturaleza exploratoria. Los resultados deben ser validados por análisis independientes antes de cualquier afirmación científica definitiva.
