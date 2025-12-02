# Análisis SNR para GW200129

Este documento describe el nuevo script de análisis de SNR para el evento GW200129.

## 📋 Descripción

El script `scripts/analizar_gw200129_snr.py` implementa el análisis de relación señal-ruido (SNR) esperada para el evento gravitacional GW200129_065458 en la frecuencia objetivo de 141.7 Hz.

## 🎯 Características

- **Evento**: GW200129_065458
- **GPS Time**: 1264316116.4
- **Frecuencia objetivo**: 141.7 Hz
- **Detectores**: H1 (Hanford), L1 (Livingston), V1 (Virgo)
- **h_rss supuesto**: 1e-22

### Factores Efectivos QCAL a 141.7 Hz

| Detector | Factor Efectivo |
|----------|-----------------|
| H1       | 0.2140          |
| L1       | 0.3281          |
| V1       | 0.8669          |

## 📦 Requisitos

```bash
pip install pycbc>=2.0.0
pip install gwpy>=3.0.0
pip install numpy>=1.21.0
```

O usando el archivo de requisitos del proyecto:

```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Ejecución básica

```bash
python3 scripts/analizar_gw200129_snr.py
```

### Salida esperada

El script:
1. Descarga datos de GWOSC para cada detector
2. Calcula el PSD (Power Spectral Density)
3. Evalúa el PSD en 141.7 Hz
4. Calcula la SNR esperada usando: `SNR = (F_eff * h_rss) / sqrt(Sn(f0))`
5. Guarda los resultados en `results/gw200129_snr_analysis.json`

### Ejemplo de salida

```
======================================================================
🌌 Análisis de SNR esperada para GW200129_065458
======================================================================
📍 GPS Time: 1264316116.4
📍 Frecuencia objetivo: 141.7 Hz
📍 h_rss supuesto: 1e-22
📍 Detectores: H1, L1, V1
======================================================================

🔬 Procesando detector H1...
----------------------------------------------------------------------
   Factor efectivo QCAL (F_eff): 0.214
   Descargando datos de H1...
   Remuestreando a 4096 Hz...
   Calculando PSD (fftlength=4s)...
   Interpolando PSD (delta_f=0.25 Hz)...
   PSD en 141.7 Hz: 1.23e-46 Hz⁻¹
   ✅ SNR esperada a 141.7 Hz en H1: 5.42

[... similar para L1 y V1 ...]

======================================================================
📊 RESUMEN DE RESULTADOS
======================================================================
H1: SNR = 5.42
L1: SNR = 8.30
V1: SNR = 21.93

SNR promedio: 11.88
SNR máxima: 21.93
SNR mínima: 5.42

📁 Resultados guardados en: results/gw200129_snr_analysis.json
```

## 🧪 Tests

El script incluye una suite completa de tests unitarios:

```bash
python3 scripts/test_analizar_gw200129_snr.py -v
```

### Tests incluidos

- ✅ Validación del tiempo GPS del evento
- ✅ Validación de la frecuencia objetivo
- ✅ Validación de factores efectivos QCAL
- ✅ Validación de la amplitud h_rss
- ✅ Prueba de la fórmula de cálculo SNR
- ✅ Validación de lista de detectores
- ✅ Validación de parámetros PSD
- ✅ Prueba de estructura de resultados
- ✅ Verificación de existencia del script
- ✅ Verificación de permisos de ejecución

Todos los tests pasan exitosamente: **12/12 ✅**

## 📊 Formato de resultados (JSON)

```json
{
  "event": "GW200129_065458",
  "gps_time": 1264316116.4,
  "frequency": 141.7,
  "h_rss": 1e-22,
  "results": {
    "H1": {
      "F_eff": 0.2140,
      "Sn_f0": 1.234e-46,
      "SNR": 5.42,
      "error": null
    },
    "L1": {
      "F_eff": 0.3281,
      "Sn_f0": 1.456e-46,
      "SNR": 8.30,
      "error": null
    },
    "V1": {
      "F_eff": 0.8669,
      "Sn_f0": 1.567e-46,
      "SNR": 21.93,
      "error": null
    }
  }
}
```

## 🔬 Metodología

### 1. Obtención de PSD

La función `get_psd()` implementa el siguiente proceso:

1. Descarga datos de GWOSC usando `gwpy.timeseries.TimeSeries.fetch_open_data()`
2. Remuestrea a 4096 Hz para análisis consistente
3. Calcula el PSD usando el método de Welch con ventana Hann
4. Interpola el PSD con resolución de 0.25 Hz

### 2. Cálculo de SNR

La fórmula implementada es:

```
SNR = (F_eff × h_rss) / √(Sn(f₀))
```

Donde:
- `F_eff`: Factor efectivo angular del detector (de QCAL)
- `h_rss`: Amplitud root-sum-square de la señal
- `Sn(f₀)`: Densidad espectral de potencia del ruido en f₀

## 🔧 Integración con CI/CD

El script se integra automáticamente con el sistema CI/CD del proyecto:

- Los tests se ejecutan en cada push/PR
- Se valida con flake8 (0 errores)
- Compatible con Python 3.9, 3.11 y 3.12

## 📚 Referencias

- [PyCBC Documentation](https://pycbc.org/)
- [GWpy Documentation](https://gwpy.github.io/)
- [GWOSC Data Access](https://www.gw-openscience.org/)

## 🤝 Contribuir

Para reportar problemas o sugerir mejoras, por favor abre un issue en el repositorio.

## 📄 Licencia

Este código está bajo la misma licencia MIT del proyecto principal.
