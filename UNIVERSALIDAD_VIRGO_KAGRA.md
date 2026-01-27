# Test de Universalidad de 141.7 Hz en Virgo y KAGRA

## 📋 Resumen

Este módulo implementa un test de universalidad para validar la detección de la frecuencia 141.7 Hz en los detectores Virgo (V1) y KAGRA (K1), complementando el análisis multi-evento existente que usa los detectores LIGO H1 y L1.

## 🎯 Objetivo

Verificar si la señal de 141.7 Hz identificada en los detectores LIGO (H1 y L1) también es detectable en el detector europeo Virgo (V1), validando así la universalidad del fenómeno a través de múltiples observatorios independientes.

## 📊 Eventos Analizados

El análisis se centra en cuatro eventos de ondas gravitacionales de 2017:

| Evento | Tiempo GPS Inicio | Tiempo GPS Fin | Duración |
|--------|-------------------|----------------|----------|
| GW170814 | 1186741850 | 1186741882 | 32s |
| GW170817 | 1187008882 | 1187008914 | 32s |
| GW170818 | 1187058327 | 1187058359 | 32s |
| GW170823 | 1187529256 | 1187529288 | 32s |

**Nota sobre KAGRA**: Estos eventos son de 2017, cuando KAGRA aún no estaba operacional. KAGRA comenzó sus observaciones en 2020. El módulo está preparado para incluir análisis de KAGRA cuando se trabajen con eventos posteriores a 2020.

## 🔧 Configuración Técnica

- **Banda de frecuencia**: 141.4 - 142.0 Hz
- **Frecuencia objetivo**: 141.7 Hz
- **Umbral de SNR**: 5.0
- **Detector principal**: Virgo (V1)
- **Método**: Filtro de banda pasante + cálculo de SNR

## 📁 Archivos Implementados

### Script Principal
- **`scripts/test_universalidad_virgo_kagra.py`**
  - Descarga datos de GWOSC para el detector Virgo
  - Aplica filtro de banda pasante alrededor de 141.7 Hz
  - Calcula SNR para cada evento
  - Genera visualización y resultados en JSON

### Suite de Tests
- **`scripts/test_test_universalidad_virgo_kagra.py`**
  - 6 tests comprehensivos
  - Validación de configuración de eventos
  - Validación de banda de frecuencia
  - Tests de funciones de cálculo SNR
  - Verificación de nombres de detectores
  - Validación de umbral de SNR

## 🚀 Uso

### Mediante Make (recomendado)

```bash
# Ejecutar análisis con datos reales de GWOSC
make universalidad-virgo-kagra

# Ejecutar suite de tests (sin conectividad)
make test-universalidad-virgo-kagra
```

### Ejecución Directa

```bash
# Análisis completo con datos GWOSC
python3 scripts/test_universalidad_virgo_kagra.py

# Tests del módulo
python3 scripts/test_test_universalidad_virgo_kagra.py
```

## 📈 Resultados Generados

### Archivos de Salida

1. **`universalidad_virgo_kagra_results.json`**
   - Resultados detallados de SNR para cada evento
   - Información de errores si los hay
   - Formato estructurado para análisis posterior

2. **`universalidad_virgo_kagra.png`**
   - Gráfico de barras con SNR por evento
   - Línea de umbral (SNR=5) marcada
   - Visualización clara de resultados

### Estadísticas Calculadas

- **SNR promedio** de Virgo (V1)
- **Desviación estándar** de SNR
- **Porcentaje de eventos** sobre umbral de detección
- **Resumen comparativo** entre eventos

## ✅ Validación

### Tests Implementados

1. **test_snr_calculation**: Validación del cálculo de SNR con datos sintéticos
2. **test_event_configuration**: Verificación de configuración de eventos
3. **test_target_band**: Validación de banda de frecuencia objetivo
4. **test_calculate_snr_function**: Test de función calculate_snr
5. **test_detector_names**: Verificación de nombres de detectores V1 y K1
6. **test_snr_threshold**: Validación de umbral de SNR (5.0)

### Estado de Tests

```
✅ Pasados: 6/6
✅ Linting: Aprobado (flake8)
✅ Seguridad: Sin alertas (CodeQL)
```

## 🔬 Metodología Científica

### Cálculo de SNR

```python
SNR = max(|señal_filtrada|) / std(señal_filtrada)
```

### Proceso de Análisis

1. **Descarga de datos**: Obtención de datos de Virgo desde GWOSC
2. **Filtrado**: Aplicación de filtro de banda pasante [141.4, 142.0] Hz
3. **Cálculo SNR**: Ratio señal-ruido en banda objetivo
4. **Visualización**: Generación de gráficos comparativos
5. **Estadísticas**: Análisis estadístico de resultados

## 📚 Comparación con Análisis Multi-evento Existente

| Aspecto | Multi-evento SNR | Universalidad Virgo/KAGRA |
|---------|------------------|---------------------------|
| Detectores | H1, L1 (LIGO) | V1 (Virgo), K1 (KAGRA) |
| Eventos | 11 eventos | 4 eventos (2017) |
| Banda | 140.7-142.7 Hz | 141.4-142.0 Hz |
| Objetivo | Validación H1/L1 | Universalidad multi-detector |

## 🔗 Integración con Sistema Existente

Este módulo se integra perfectamente con:

- **`multi_event_snr_analysis.py`**: Análisis paralelo con H1/L1
- **Makefile**: Comandos de ejecución estandarizados
- **Sistema de tests**: Suite de tests consistente
- **CI/CD**: Compatible con workflows de GitHub Actions

## 🌍 Relevancia Científica

La validación de la señal de 141.7 Hz en múltiples detectores independientes (LIGO H1, LIGO L1, Virgo V1) proporciona:

1. **Confirmación independiente**: Diferentes observatorios validan el mismo fenómeno
2. **Reducción de false positives**: Detección multi-detector reduce ruido local
3. **Universalidad**: La señal no es un artefacto de un detector específico
4. **Robustez científica**: Múltiples líneas de evidencia convergen

## 📖 Referencias

- **GWOSC**: Gravitational Wave Open Science Center - Fuente de datos
- **GWpy**: Python package para análisis de ondas gravitacionales
- **Virgo**: Detector europeo de ondas gravitacionales
- **KAGRA**: Detector japonés de ondas gravitacionales

## 🔮 Trabajo Futuro

### Análisis KAGRA

Cuando se analicen eventos posteriores a 2020, incluir:
- Datos de KAGRA (K1)
- Comparación V1 vs K1
- Análisis de consistencia temporal

### Extensiones Posibles

- Análisis de armónicos en Virgo/KAGRA
- Coherencia multi-detector V1-H1-L1
- Estudio de fase entre detectores
- Análisis bayesiano de universalidad

## 👥 Autor

José Manuel Mota Burruezo (JMMB Ψ✧)

## 📄 Licencia

MIT License - Ver LICENSE para detalles
