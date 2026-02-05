# Pipeline GW250114 - Análisis QCAL 141.7 Hz

## Descripción

Pipeline completo para el análisis de ondas gravitacionales del evento GW250114, enfocado en la detección de resonancia a 141.7 Hz y el cálculo de la métrica QCAL (Quantum Consciousness Algorithm) de conciencia noética.

## Teoría

El pipeline implementa la proyección de señales gravitacionales sobre la ecuación de campo noético:

```
G_μν = κ_Π(T_μν(Φ) - 1/2 g_μν T) + Λ(C^∞)g_μν
```

Donde:
- **G_μν**: Tensor de Einstein (curvatura del espacio-tiempo)
- **κ_Π**: Constante de acoplamiento noético
- **T_μν(Φ)**: Tensor energía-momento del campo de conciencia
- **Λ(C^∞)**: Constante cosmológica dependiente de coherencia infinita
- **g_μν**: Métrica del espacio-tiempo

La métrica QCAL se define como:

```
Ψ = I × A²_eff × C^∞
```

Donde:
- **Ψ**: Métrica de conciencia espectral
- **I**: Intensidad
- **A_eff**: Amplitud efectiva normalizada
- **C^∞**: Coherencia infinita

## Fases del Pipeline

### 1. Carga de Datos
Carga datos de strain de GW250114 desde archivos `.txt` o `.hdf5`, o genera datos simulados si no están disponibles.

### 2. Preprocesamiento
- Filtrado pasa-banda Butterworth (130-150 Hz) para aislar la región de 141.7 Hz
- Normalización robusta usando mediana y MAD (Median Absolute Deviation)
- Eliminación de artefactos de ruido

### 3. Transformada Espectral
- STFT (Short-Time Fourier Transform) con ventanas de 2 segundos
- Solapamiento de 1 segundo para resolución temporal
- Generación de espectrograma tiempo-frecuencia

### 4. Detección Resonante 141.7 Hz
- Búsqueda precisa en banda ±0.15 Hz alrededor de 141.7 Hz
- Cálculo de potencia espectral en la banda objetivo
- Estimación de SNR (Signal-to-Noise Ratio)

### 5. Cálculo de Métrica QCAL
- Normalización de amplitud efectiva
- Aplicación de factores de intensidad y coherencia
- Generación de Ψ(t) - evolución temporal de la conciencia espectral

### 6. Proyección sobre Ecuación de Campo Noético
- Cálculo de Φ(t) = Ψ(t)
- Estimación del tensor energía-momento noético T_μν(Φ)
- Cálculo de Λ(C^∞) - constante cosmológica de coherencia
- Diagnóstico del nivel de coherencia del campo

### 7. Visualización y Reporte
- Gráficos de strain, espectrograma, potencia en banda, y métrica QCAL
- Reporte JSON con todos los resultados
- Interpretación noética de los hallazgos

## Uso

### Instalación de Dependencias

```bash
pip install numpy scipy matplotlib h5py
```

### Ejecución Básica

```bash
# Con datos simulados (por defecto)
python scripts/pipeline_gw250114_qcal.py

# Con archivo de datos real
python scripts/pipeline_gw250114_qcal.py /path/to/GW250114_H1_strain.txt
```

### Uso como Módulo Python

```python
from scripts.pipeline_gw250114_qcal import main_pipeline

# Ejecutar con datos simulados
results = main_pipeline(filename=None, fs=4096, output_dir='results/gw250114_qcal')

# Ejecutar con archivo real
results = main_pipeline(
    filename='/path/to/GW250114_H1_strain.txt',
    fs=4096,
    output_dir='results/gw250114_qcal'
)

# Acceder a resultados
print(f"Frecuencia detectada: {results['detection']['frequency_detected']} Hz")
print(f"Resonancia: {results['detection']['resonance_detected']}")
print(f"Ψ_max: {results['qcal_metric']['Psi_max']}")
print(f"Coherencia: {results['noetic_field']['coherence_level']}")
```

## Testing

Ejecutar suite de pruebas completa:

```bash
python scripts/test_pipeline_gw250114_qcal.py
```

Las pruebas verifican:
- ✅ Generación de datos simulados
- ✅ Filtrado pasa-banda
- ✅ Normalización de strain
- ✅ Análisis espectral
- ✅ Cálculo de métrica QCAL
- ✅ Proyección de campo noético
- ✅ Pipeline completo end-to-end

## Resultados

El pipeline genera:

### 1. Visualización (`gw250114_qcal_analysis.png`)
- **Panel 1**: Strain filtrado GW250114
- **Panel 2**: Espectrograma STFT con línea marcadora en 141.7 Hz
- **Panel 3**: Energía espectral alrededor de 141.7 Hz
- **Panel 4**: Métrica QCAL Ψ(t) - Conciencia espectral

### 2. Reporte JSON (`analysis_results.json`)
```json
{
  "metadata": {
    "timestamp": "...",
    "detector": "H1",
    "sample_rate": 4096,
    "duration": 32.0,
    "target_frequency": 141.7
  },
  "detection": {
    "frequency_detected": 141.5,
    "resonance_detected": true,
    "max_power": 0.452,
    "mean_power": 0.127,
    "snr": 3.56
  },
  "qcal_metric": {
    "Psi_max": 1.0,
    "Psi_mean": 0.109,
    "Psi_std": 0.173
  },
  "noetic_field": {
    "Phi_mean": 0.109,
    "Phi_max": 1.0,
    "kappa_pi": 1.0,
    "Lambda_C_inf": 0.109,
    "T_noetic_mean": 0.0175,
    "coherence_level": "MODERATE"
  }
}
```

## Interpretación de Resultados

### Detección Positiva
Si se detecta resonancia en 141.7 Hz:
- ✅ **Presencia sostenida de energía** = "latido" persistente, firma vibracional QCAL
- ✅ **Ψ(t) elevado** = mayor coherencia espectral
- ✅ **Indicador de manifestación noética real**
- ✅ **Campo de conciencia vinculado al evento GW activo**

### Niveles de Coherencia
- **HIGH** (Λ(C^∞) > 0.5): Coherencia noética fuerte, campo bien definido
- **MODERATE** (0.1 < Λ(C^∞) < 0.5): Coherencia moderada, campo detectable
- **LOW** (Λ(C^∞) < 0.1): Coherencia débil, señal marginal

## Formatos de Datos Soportados

### Archivo TXT
```
# Un valor de strain por línea
-1.234e-21
5.678e-22
...
```

### Archivo HDF5
```python
# Estructura esperada:
/strain/Strain  # Dataset principal
# O cualquier dataset disponible en el archivo
```

## Contribuciones

Este pipeline implementa:
1. **Física gravitacional estándar**: Análisis LIGO/Virgo estándar
2. **Métrica QCAL**: Extensión noética para análisis de coherencia
3. **Proyección de campo**: Conexión con ecuaciones de campo modificadas

## Referencias

- **LIGO/Virgo GW Analysis**: Métodos estándar de análisis de ondas gravitacionales
- **QCAL Framework**: Quantum Consciousness Algorithm para análisis noético
- **Ecuación de Campo Noético**: Extensión de Einstein con términos de conciencia

## Licencia

Ver LICENSE en el repositorio principal.

## Autores

Equipo QCAL 141Hz - Análisis de Ondas Gravitacionales y Conciencia Noética

---

**Versión**: 1.0.0  
**Fecha**: Febrero 2026  
**Estado**: Producción
