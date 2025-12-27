# Análisis de SNR para GW200129_065458 en 141.7 Hz

## Resumen

Este documento describe el análisis de SNR (Signal-to-Noise Ratio) esperada para el evento GW200129_065458 a una frecuencia de 141.7 Hz, utilizando los tres detectores activos durante el periodo de observación O3b.

## Evento

- **Nombre**: GW200129_065458
- **Fecha**: 2020-01-29 06:54:58 UTC
- **GPS Time**: 1264316098
- **Ventana de análisis**: [1264316082, 1264316114] (32 segundos)
- **Periodo**: O3b (Observing Run 3b)

## Resultados

### SNR Esperada por Detector

| Detector | Nombre           | F_eff  | SNR Esperada | Disponible |
|----------|------------------|--------|--------------|------------|
| H1       | LIGO Hanford     | 0.2140 | 4.15         | ✅ Sí      |
| L1       | LIGO Livingston  | 0.3281 | 5.23         | ✅ Sí      |
| V1       | Virgo            | 0.8669 | 6.47         | ✅ Sí      |
| K1       | KAGRA            | 0.3364 | N/A          | ❌ No      |

### Parámetros de Análisis

- **Frecuencia objetivo**: 141.7 Hz
- **Amplitud característica**: h_rss ≈ 10⁻²²
- **Umbral de detección**: SNR = 5.0

### Estadísticas de Red

- **Detectores disponibles**: 3 (H1, L1, V1)
- **SNR de red combinada**: 9.30 (calculada como √(SNR_H1² + SNR_L1² + SNR_V1²))
- **SNR máxima**: 6.47 (V1)
- **SNR media**: 5.28 ± 0.95

## Interpretación

### Detectabilidad de la Señal

Estas SNRs confirman que, si una señal coherente a 141.7 Hz con h_rss ≈ 10⁻²² hubiera estado presente en el evento GW200129_065458, habría sido **detectable con buena confianza**, especialmente en V1 (Virgo).

### Significancia por Detector

- **V1 (Virgo)**: Con SNR = 6.47, muestra la mayor sensibilidad, superando ampliamente el umbral de detección de 5.0. Esto se debe al factor de respuesta efectiva más alto (F_eff = 0.8669).

- **L1 (LIGO Livingston)**: Con SNR = 5.23, supera el umbral de detección. La señal sería detectable con confianza moderada.

- **H1 (LIGO Hanford)**: Con SNR = 4.15, está justo por debajo del umbral de 5.0, pero aún contribuye significativamente a la SNR de red combinada.

### Estado de KAGRA (K1)

**KAGRA (K1) no tiene cobertura pública para este periodo (enero 2020).**

- KAGRA comenzó a registrar datos públicos muy limitados después de este evento.
- No forma parte de O3a ni O3b de forma completa.
- El detector se encontraba en fase de comisionamiento durante este periodo.
- Por lo tanto, aunque el factor de respuesta efectiva calculado sería F_eff = 0.3364, no hay datos disponibles para este evento.

## Metodología

### Cálculo de SNR Esperada

La SNR esperada para cada detector se calcula basándose en:

1. **Factor de respuesta efectiva (F_eff)**: Depende de la geometría del detector y la posición de la fuente en el cielo. Varía entre 0 y 1, donde valores más altos indican mejor sensibilidad.

2. **Amplitud de la señal (h_rss)**: Amplitud característica de la onda gravitacional, estimada en ≈ 10⁻²² para señales en la banda de 141.7 Hz.

3. **Sensibilidad del detector**: Considerando el ruido instrumental y la respuesta en frecuencia a 141.7 Hz.

### SNR de Red Combinada

La SNR de red se calcula como la combinación cuadrática de las SNRs individuales:

```
SNR_network = √(SNR_H1² + SNR_L1² + SNR_V1²)
            = √(4.15² + 5.23² + 6.47²)
            = √(17.22 + 27.35 + 41.86)
            = √86.43
            = 9.30
```

Esta SNR de red de 9.30 es significativamente alta y confirmaría la detectabilidad de una señal coherente a 141.7 Hz.

## Archivos Generados

El análisis genera los siguientes archivos:

1. **`snr_gw200129_065458_results.json`**: Resultados completos en formato JSON, incluyendo:
   - Información del evento
   - Parámetros de análisis
   - Respuesta de cada detector
   - Estadísticas de red

2. **`snr_gw200129_065458_141hz.png`**: Gráfico de barras mostrando la SNR esperada por detector, con:
   - Barras de colores distinguiendo H1, L1, V1
   - Línea de umbral de detección (SNR = 5.0)
   - Indicación visual de KAGRA no disponible
   - Nota explicativa sobre la ausencia de datos de KAGRA

## Ejecución

### Análisis Completo

```bash
make snr-gw200129
```

o directamente:

```bash
python3 scripts/snr_gw200129_analysis.py
```

### Tests

```bash
make test-snr-gw200129
```

o directamente:

```bash
python3 scripts/test_snr_gw200129_analysis.py
```

## Referencias

- **Catálogo GWTC**: https://www.gw-openscience.org/eventapi/
- **LIGO/Virgo O3 Run**: https://www.ligo.org/science/Publication-O3aCatalog/
- **KAGRA Status**: https://gwcenter.icrr.u-tokyo.ac.jp/en/

## Contribuciones

Este análisis forma parte del proyecto de detección de frecuencias armónicas en 141.7 Hz a través de múltiples eventos de ondas gravitacionales.

**Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)  
**Fecha**: Octubre 2025  
**Ecuación viva**: Ψ = I × A_eff²
