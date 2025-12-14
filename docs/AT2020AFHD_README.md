# AT2020afhd - Tidal Disruption Event Analysis

## 🌌 Overview

AT2020afhd es un **evento de disrupción de marea (TDE - Tidal Disruption Event)** donde una estrella fue destrozada por un agujero negro supermasivo. El sistema exhibe oscilaciones regulares de **~20 días** en observaciones multi-longitud de onda (X-ray y radio), consistentes con **precesión Lense-Thirring** predicha por relatividad general.

Este análisis implementa:
- ✅ Descarga de datos oficiales (Swift X-ray, VLA radio)
- ✅ Procesamiento de curvas de luz
- ✅ Análisis de periodicidad (Lomb-Scargle)
- ✅ Ajuste de modelo de precesión Lense-Thirring
- ✅ Comparación con marco teórico QCAL ∞³

## 📚 Referencias Científicas

### Artículo Principal
- **"Detection of disk-jet co-precession in a tidal disruption event"**
  - Disponible en arXiv
  - Periodo confirmado: ~19.6-20 días
  - Mecanismo: Precesión Lense-Thirring del disco de acreción y jet

### Fuentes de Datos
- **Swift Observatory**: NASA HEASARC
  - Instrumento: Swift XRT (X-Ray Telescope)
  - Banda: 0.3-10 keV
  - URL: https://heasarc.gsfc.nasa.gov/

- **Very Large Array**: NRAO
  - Frecuencias: 5-10 GHz
  - URL: https://data.nrao.edu/

### Instituciones
- NASA HEASARC
- NRAO (National Radio Astronomy Observatory)
- Chalmers University of Technology
- Phys.org coverage

## 🚀 Quick Start

### 1. Descargar Datos

```bash
# Descarga automática de datos X-ray y radio
python scripts/descargar_at2020afhd.py --yes

# Solo X-ray
python scripts/descargar_at2020afhd.py --xray-only --yes

# Solo radio
python scripts/descargar_at2020afhd.py --radio-only --yes
```

### 2. Ejecutar Análisis

```bash
# Análisis completo con visualizaciones
python scripts/analizar_at2020afhd.py

# Solo análisis, sin gráficos
python scripts/analizar_at2020afhd.py --no-plots
```

### 3. Notebook Interactivo

```bash
jupyter notebook notebooks/at2020afhd_analysis.ipynb
```

O abrir en Google Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/motanova84/141hz/blob/main/notebooks/at2020afhd_analysis.ipynb)

## 📊 Resultados

### Estructura de Directorios

```
data/tde/at2020afhd/
├── xray/
│   └── swift_xray_at2020afhd.csv
├── radio/
│   └── vla_radio_at2020afhd.csv
├── metadata.json
└── README.md

results/at2020afhd/
├── at2020afhd_results.json
├── at2020afhd_lightcurves.png
├── at2020afhd_periodograms.png
└── at2020afhd_combined_analysis.png
```

### Ejemplo de Resultados

```json
{
  "object": "AT2020afhd",
  "analysis_type": "Lense-Thirring Precession",
  "xray": {
    "n_observations": 50,
    "peak_period_days": 19.74,
    "fit_period_days": 19.81,
    "fit_chi2_reduced": 0.78
  },
  "radio": {
    "n_observations": 35,
    "peak_period_days": 20.12,
    "fit_period_days": 20.05,
    "fit_chi2_reduced": 1.15
  },
  "interpretation": {
    "precession_mechanism": "Lense-Thirring (General Relativity)",
    "expected_period_days": 20.0,
    "multi_wavelength_consistent": true
  }
}
```

## 🔬 Física del Sistema

### Precesión Lense-Thirring

La **precesión Lense-Thirring** es un efecto de relatividad general donde el spin de un agujero negro "arrastra" el spacetime circundante (frame-dragging), causando que el disco de acreción y el jet precesen.

**Periodo de precesión**:
```
P ≈ (2π/Ω_LT) ≈ 20 días
```

Donde Ω_LT depende de:
- Masa del agujero negro (M)
- Spin del agujero negro (a)
- Radio del disco interno

### Modelo Matemático

El modelo de precesión se expresa como:

```
F(t) = A sin(ωt + φ) + F₀
```

Donde:
- `A` = Amplitud de oscilación
- `ω = 2π/P` = Frecuencia angular
- `P` = Periodo de precesión (~20 días)
- `φ` = Fase inicial
- `F₀` = Flujo base

### Conexión con QCAL ∞³

El marco QCAL ∞³ identifica resonancias fundamentales en 141.7 Hz. La conexión con AT2020afhd:

```python
# Periodo de precesión
P_prec = 20 días = 1.728 × 10⁶ segundos

# Frecuencia de precesión
f_prec = 1/P_prec ≈ 5.8 × 10⁻⁷ Hz

# Frecuencia QCAL fundamental
f₀_QCAL = 141.7 Hz

# Relación de escalas
f₀_QCAL / f_prec ≈ 2.4 × 10⁸
```

Ambas escalas reflejan la geometría del spacetime en diferentes regímenes:
- **142 Hz**: Fusiones compactas, dinámica de merger
- **~20 días**: Acreción, precesión de disco-jet

## 📈 Análisis Implementados

### 1. Curvas de Luz
- Visualización multi-longitud de onda
- X-ray (Swift) y Radio (VLA)
- Errores fotométricos incluidos

### 2. Periodogramas Lomb-Scargle
- Análisis de periodicidad robusto para datos irregulares
- Detección de pico dominante ~20 días
- Significancia estadística

### 3. Ajuste de Modelo
- Modelo sinusoidal de precesión
- Minimización χ² con errores
- Extracción de parámetros físicos

### 4. Correlaciones Multi-longitud
- Comparación X-ray vs Radio
- Análisis de fase relativa
- Consistencia temporal

## 🔧 Dependencias

```python
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0
matplotlib>=3.5.0
astropy>=5.0
```

Instalación:
```bash
pip install numpy pandas scipy matplotlib astropy
```

## 🤖 Automatización GitHub Actions

El workflow `.github/workflows/at2020afhd-analysis.yml` ejecuta:

1. **Descarga de datos**: Cada 4 horas o manual
2. **Análisis de precesión**: Lomb-Scargle + ajuste
3. **Comparación QCAL**: Escalas de frecuencia
4. **Generación de reportes**: JSON + visualizaciones

Trigger manual:
```bash
gh workflow run at2020afhd-analysis.yml
```

## 📖 Uso Detallado

### Script de Descarga

```bash
python scripts/descargar_at2020afhd.py --help
```

Opciones:
- `--yes, -y`: Auto-confirmar descargas
- `--xray-only`: Solo datos X-ray
- `--radio-only`: Solo datos radio

### Script de Análisis

```bash
python scripts/analizar_at2020afhd.py --help
```

Opciones:
- `--data-dir`: Directorio de datos (default: `data/tde/at2020afhd`)
- `--output-dir`: Directorio de salida (default: `results/at2020afhd`)
- `--no-plots`: Análisis sin gráficos

### Notebook

El notebook `notebooks/at2020afhd_analysis.ipynb` incluye:

1. Instalación de dependencias
2. Descarga de datos
3. Carga y exploración
4. Visualización de curvas de luz
5. Cálculo de periodogramas
6. Ajuste de modelo Lense-Thirring
7. Comparación con QCAL
8. Resumen de resultados
9. Conclusiones científicas

## 🎓 Educación y Divulgación

### Conceptos Clave

- **Evento de Disrupción de Marea (TDE)**: Estrella destruida por fuerzas de marea de agujero negro
- **Lense-Thirring**: Efecto de arrastre de marcos (frame-dragging) predicho por Einstein
- **Precesión**: Movimiento cónico del eje de rotación
- **Multi-longitud de onda**: Observaciones en X-ray + radio correlacionadas

### Por qué es importante

AT2020afhd proporciona:
1. **Test de Relatividad General**: Precesión en campo fuerte
2. **Propiedades del BH**: Masa y spin del agujero negro
3. **Física de Acreción**: Estructura del disco interno
4. **Jets Relativistas**: Co-precesión disco-jet confirmada

## 🔗 Enlaces Útiles

- [NASA HEASARC](https://heasarc.gsfc.nasa.gov/)
- [NRAO Data Archive](https://data.nrao.edu/)
- [arXiv: TDE Precession Papers](https://arxiv.org/search/?query=AT2020afhd&searchtype=all)
- [Chalmers University - TDE Research](https://www.chalmers.se/)

## 📝 Citación

Si utilizas este código en investigación, por favor cita:

```bibtex
@software{at2020afhd_analysis,
  author = {QCAL Project},
  title = {AT2020afhd Tidal Disruption Event Analysis},
  year = {2024},
  url = {https://github.com/motanova84/141hz},
  note = {Lense-Thirring precession analysis}
}
```

Y el artículo original:
```bibtex
@article{at2020afhd_detection,
  title = {Detection of disk-jet co-precession in a tidal disruption event},
  journal = {arXiv preprint},
  year = {2024},
  note = {AT2020afhd multi-wavelength observations}
}
```

## 🤝 Contribuciones

Para contribuir:
1. Fork el repositorio
2. Crea un branch (`git checkout -b feature/mejora-tde`)
3. Commit cambios (`git commit -am 'Mejora análisis TDE'`)
4. Push al branch (`git push origin feature/mejora-tde`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para detalles.

## 🙏 Agradecimientos

- NASA HEASARC por datos públicos de Swift
- NRAO por datos del VLA
- Autores del paper de AT2020afhd
- Comunidad de astrofísica de altas energías

---

**Nota**: Los datos incluidos son ejemplos simulados basados en publicaciones científicas. Para análisis con datos reales, acceder a los archivos oficiales de HEASARC y NRAO.
