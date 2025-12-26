# Prerregistro (v1.0)

## Parámetros de Análisis

### Ventana Temporal
- **Ventana**: [t0−0.25 s, t0+0.25 s]
- Ventana de 0.5 segundos centrada en el tiempo de coalescencia

### Procesamiento de Datos
- **Banda de frecuencia**: 20–1024 Hz
- **Whitening**: Por detector individual
  - Método: Welch
  - Nfft: 2^14 (16384)
  - Overlap: 50%
  - Ventana: Hann

### Frecuencia Objetivo
- **f0**: 141.7001 Hz
- **Tolerancia**: ±0.3 Hz
- **Naturaleza**: Fijada a priori (no ajustada a los datos)

### Estadística de Detección
- **Estadística principal**: SNR coherente (mezcla Fisher)
- **Inferencia estadística**: Bayes factor jerárquico

### Corrección de Múltiples Comparaciones
- **Método**: Modelo jerárquico π_global
- Corrección automática para múltiples eventos

### Exclusiones
- **Archivo**: `controls/lines_exclusion.csv`
- Exclusión de líneas instrumentales conocidas

### Validaciones de Robustez

#### Off-source
- **N ventanas**: 10^4 (10,000) ventanas por evento
- **Región**: Fuera de ±10 s del tiempo de coalescencia
- Evaluación de fondo de ruido

#### Time-slides
- **N desplazamientos**: 200
- **Rango**: ±50 ms
- **Exclusión**: 0 ms (sin desplazamiento)
- Validación de coherencia temporal

#### Leave-one-out
- **Por evento**: Excluir cada evento uno a la vez
- **Por detector**: Excluir cada detector uno a la vez
- Validación de robustez y consistencia

### Cierre de Plan
- **Hash del plan**: Registrar hash SHA-256 de este documento
- **DOI Zenodo**: Asignar DOI antes de corridas masivas
- **Timestamp**: Fecha de cierre del plan de análisis

## Detectores
- H1 (Hanford)
- L1 (Livingston)
- V1 (Virgo)

## Notas
Este prerregistro define todos los parámetros de análisis antes de la ejecución, siguiendo las mejores prácticas de ciencia abierta y reproducibilidad.
