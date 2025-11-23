# 🌌 DESI - Dark Energy Spectroscopic Instrument

## Objetivo

Comprobar la predicción cosmológica del modelo de Gravedad Cuántica Noésica (GQN):

```
w(z) = -1 + n/3,  n ≈ 0.3
```

Esta ecuación predice una expansión ligeramente más rápida que ΛCDM a z > 1.

## Modelo Teórico

### Ecuación de Estado CPL

Usamos la parametrización Chevallier-Polarski-Linder (CPL):

```
w(z) = w₀ + wₐ · z/(1+z)
```

### Predicción GQN

El modelo GQN predice:
- **w₀ = -1** (consistente con constante cosmológica)
- **wₐ = +0.2** (desviación positiva, expansión más rápida)
- **n ≈ 0.3** (parámetro noésico)

### Factor de Expansión

```
E²(z) = Ω_m(1+z)³ + Ω_Λ exp[3∫₀ᶻ (1+w(z'))/(1+z') dz']
```

donde E(z) = H(z)/H₀.

## Implementación

### MCMC Bayesiano

Utilizamos `emcee` para muestreo MCMC y ajuste de parámetros (w₀, wₐ) a datos de distancia de luminosidad D_L(z).

### Distancia de Luminosidad

```
D_L(z) = (1+z) · c/H₀ · ∫₀ᶻ dz'/E(z')
```

### Parámetro de Tensión

```
Δw = w_DESI(z) - w_GQN(z)
```

## Uso

### Ejecución básica

```bash
cd desi
python3 desi_wz_analysis.py
```

### Análisis personalizado

```python
from desi_wz_analysis import DESICosmologyAnalysis

# Crear analizador
analysis = DESICosmologyAnalysis(
    h0=67.4,        # km/s/Mpc
    omega_m=0.315   # Densidad de materia
)

# Ejecutar análisis con datos mock
results = analysis.run_analysis(
    use_mock_data=True,
    save_results=True,
    output_dir="desi_results"
)

# Generar gráficos
analysis.plot_results(results)
```

### Con datos reales DESI

```python
# Cargar datos DESI DR2
z_data, D_L_data, D_L_err = load_desi_dr2_data()

# Ajuste MCMC
fit_results = analysis.fit_with_mcmc(
    z_data, D_L_data, D_L_err,
    n_walkers=32,
    n_steps=2000
)

# Calcular tensión
tension = analysis.calculate_tension(
    fit_results['w0'],
    fit_results['wa']
)
```

## Resultados

Los resultados se guardan en `desi_results/`:
- `desi_wz_results.json`: Parámetros ajustados y estadísticas
- `desi_wz_plot.png`: Gráficos de D_L(z) y w(z)

### Estructura de resultados

```json
{
  "fit": {
    "method": "MCMC",
    "w0": -1.02,
    "wa": 0.18,
    "w0_err": 0.05,
    "wa_err": 0.12,
    "samples": [...]
  },
  "tension": {
    "delta_w_mean": 0.03,
    "delta_w_max": 0.08,
    "compatible_with_gqn": true,
    "z_range": [0.5, 1.5]
  },
  "gqn_prediction": {
    "w0": -1.0,
    "wa": 0.2,
    "n": 0.3
  }
}
```

## Criterio de Falsación

**Predicción**: Si |Δw| < 0.05 en z ∈ [0.5, 1.5], se confirma compatibilidad con GQN.

**Falsación**: Si la tensión es significativa (|Δw| > 0.05 consistentemente), se debe refinar el parámetro n o rechazar el modelo.

## Interpretación Cosmológica

### wₐ > 0 (GQN)
- Energía oscura se vuelve **menos negativa** en el pasado
- Expansión más rápida a alto redshift
- Posible explicación para tensión H₀

### wₐ = 0 (ΛCDM)
- Constante cosmológica perfecta
- Modelo estándar actual

### wₐ < 0 (Quintessence)
- Energía oscura más negativa en el pasado
- Expansión más lenta a alto redshift

## Datos Reales DESI

Para usar datos oficiales de DESI DR2:

1. Acceder a [DESI Early Data Release](https://data.desi.lbl.gov/doc/releases/)
2. Descargar catálogo de BAO y espectros
3. Calcular distancias de luminosidad
4. Ejecutar análisis

```bash
# Ejemplo con DESI DR2
wget https://data.desi.lbl.gov/public/edr/vac/...
python3 process_desi_dr2.py
python3 desi_wz_analysis.py --real-data
```

## Referencias

- DESI Collaboration: https://www.desi.lbl.gov/
- CPL parametrization: Chevallier & Polarski (2001), Linder (2003)
- DESI DR2: https://data.desi.lbl.gov/
- Modelo GQN: Ver `PAPER.md` en el repositorio principal

## Dependencias

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.5.0
emcee>=3.0.0  # Para MCMC bayesiano
astropy>=5.0  # Para cosmología
```

## Instalación de emcee

```bash
pip install emcee
```

Si `emcee` no está disponible, el código usa automáticamente scipy.optimize como alternativa.
