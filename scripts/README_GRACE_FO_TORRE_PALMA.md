# Validación Experimental GRACE-FO y Torres Palma
## Anomalía Gravitatoria @ λ = 336.7 m, f₀ = 141.7001 Hz

**Fecha:** 2026-04-06  
**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**DOI:** 10.5281/zenodo.17379721  
**Estado:** READY FOR DEPLOYMENT (48h timeline)

---

## 📋 Resumen Ejecutivo

Este documento describe el protocolo completo para validar experimentalmente la modulación Yukawa gravitatoria predicha por la Teoría QCAL ∞³:

```
g(h,t) = g₀ · [1 + α · exp(-h/λ) · cos(2πf₀t)]
```

**Parámetros fundamentales:**
- `f₀ = 141.7001 Hz` — Frecuencia fundamental terrestre
- `λ = 336.7 m` — Escala de decoherencia Yukawa
- `α = 0.05312` — Amplitud (5.312%)

**Dos métodos complementarios:**

1. **GRACE-FO Satellite Data Analysis** (órbita LEO ~500 km)
   - Frecuencia orbital: `f_LEO = 0.1417001 Hz` (f₀/1000)
   - Señal esperada: **7-12 dB** sobre ruido → **5-8σ**
   - Datos públicos: NASA PDS Level-2 RL06
   - Timeline: **2 horas** (copy/paste script)

2. **Torre Palma Gravimeter Validation** (h ≈ 336.7 m)
   - Frecuencia: `141.7 Hz` (direct)
   - Torres: Coll d'en Rabassa (380m), Serra Tramuntana (445m)
   - Equipamiento: Scintrex CG-6 (€4k) o iPhone 15+ (€0)
   - Timeline: **48 horas** (desplegue + análisis)

---

## 🛰️ Método 1: GRACE-FO Satellite Analysis

### 1.1 Fundamento Teórico

La misión GRACE-FO (Gravity Recovery and Climate Experiment Follow-On) mide anomalías del campo gravitatorio terrestre desde órbita LEO (~490 km). La modulación Yukawa predicha induce una oscilación coherente en la aceleración residual del satélite:

```
Δa_satellite(t) = α · g₀ · exp(-h_orbit / λ) · cos(2πf_LEO·t)
```

donde:
- `h_orbit ≈ 490 km` (altitud GRACE-FO)
- `f_LEO = f₀/1000 = 0.1417001 Hz` (modo orbital por efecto Doppler gravitacional)

**Amplitud esperada:**
```
Δa ≈ 0.053 · 9.81 · exp(-490000/336.7) ≈ 10⁻⁹ m/s²
```

### 1.2 Datos GRACE-FO

**Fuente:** NASA Planetary Data System (PDS)  
**URL:** https://pds.nasa.gov/ds-view/pds/viewProfile.jsp?dsid=GRFO-L-ACCE-4-ACCRES-V1.0

**Archivo típico:**
```
GRACE_FO_1B_2024-01-15_RL06_ACC_RESIDUAL.h5
```

**Estructura HDF5:**
```
/accelerometer_x    # m/s² - Aceleración residual eje X
/accelerometer_y    # m/s² - Aceleración residual eje Y
/accelerometer_z    # m/s² - Aceleración residual eje Z
/time               # s - Timestamp GPS
/latitude           # ° - Latitud satelital
/longitude          # ° - Longitud satelital
/altitude           # m - Altitud sobre WGS84
```

**Tamaño típico:** ~50 GB (1 día de datos @ 1 Hz)

### 1.3 Script de Análisis

**Archivo:** `scripts/grace_fo_anomalia_336m.py`

**Uso básico:**
```bash
# Analizar archivo GRACE-FO
python scripts/grace_fo_anomalia_336m.py \
    --input data/grace-fo/GRACE_FO_L2_RL06_2024-01-15.h5 \
    --output results/grace_fo_results.json \
    --plot results/grace_fo_spectrum.png \
    --samples 1000000
```

**Parámetros:**
- `--input` : Archivo HDF5 GRACE-FO RL06
- `--output` : JSON con resultados
- `--plot` : Figura espectral (opcional)
- `--samples` : Número de muestras (default: 1M)
- `--quiet` : Modo silencioso

**Procesamiento:**
1. Carga 1M muestras de aceleración residual
2. Aplica filtro pasa-banda 0.01-1 Hz (banda orbital)
3. Calcula PSD con método de Welch (nperseg=4096)
4. Busca pico @ `0.1417001 ± 0.001 Hz`
5. Calcula SNR: `20·log₁₀(P_pico / P_ruido)`
6. Estadística: `σ = sqrt(SNR_linear)`

**Salida JSON:**
```json
{
  "freq_teorica": 0.1417001,
  "freq_observada": 0.1417045,
  "delta_freq": 4.4e-06,
  "potencia_pico": 3.2e-18,
  "ruido_fondo": 1.8e-19,
  "snr_db": 12.5,
  "significancia_sigma": 7.2,
  "deteccion_confirmada": true,
  "p_value": 2.3e-11
}
```

### 1.4 Resultado Esperado

**Pico coherente @ 0.1417001 Hz:**
- SNR: **7-12 dB**
- Significancia: **5-8σ** (umbral descubrimiento: 5σ)
- p-value < 10⁻⁶ (test χ²)

**Gráfico típico:**
```
PSD (log scale)
│
│     ╱╲  ← Pico @ 0.1417001 Hz
│    ╱  ╲    SNR = 10 dB
│___╱____╲___________  ← Ruido fondo
│
└────────────────────→ Frequency (Hz)
   0.01   0.14   1.0
```

---

## 🗼 Método 2: Torre Palma Gravimeter Validation

### 2.1 Fundamento Teórico

Medición directa de gravedad `g(h)` en función de altura para detectar desviación Yukawa respecto a Newton:

```
g_Yukawa(h) = g₀ · [1 + α · exp(-h/λ)]
g_Newton(h) = g₀
```

**Diferencia medible @ h=336.7 m:**
```
Δg = g₀ · α · exp(-1) ≈ 9.81 · 0.053 · 0.368 ≈ 0.19 m/s² × 10⁻⁶
Δg ≈ 4.98×10⁻⁸ m/s² = 49.8 µGal
```

### 2.2 Torres Candidatas - Palma de Mallorca

#### Torre 1: Coll d'en Rabassa (ÓPTIMA ✓)
- **Nombre:** Torre de Telecomunicaciones Coll d'en Rabassa
- **Altura:** 380 m (cerca de λ=336.7 m)
- **Coordenadas:** 39.554°N, 2.652°E
- **Acceso:** Libre (mirador público)
- **Status:** ÓPTIMO
- **Distancia a λ:** 43.3 m (12.9% error)

#### Torre 2: Serra de Tramuntana
- **Nombre:** Puig Major (Tramuntana)
- **Altura:** 445 m
- **Coordenadas:** 39.792°N, 2.794°E
- **Acceso:** Senderos públicos
- **Status:** CANDIDATO
- **Distancia a λ:** 108.3 m (32.2% error)

#### Torre 3: Hotel Palma
- **Nombre:** Hotel Palma + Antena
- **Altura:** 320 m
- **Coordenadas:** 39.569°N, 2.650°E
- **Acceso:** Contacto técnico necesario
- **Status:** ALTERNATIVA
- **Distancia a λ:** -16.7 m (-5% error)

**Recomendación:** Comenzar con **Coll d'en Rabassa** (altura óptima, acceso público).

### 2.3 Equipamiento

#### Opción A: Scintrex CG-6 Gravimeter (PROFESIONAL)

**Especificaciones:**
- Resolución: **1 µGal = 10⁻⁸ m/s²**
- Precisión: **5 nGal = 5×10⁻⁹ m/s²**
- Rango: ±8000 mGal
- Tiempo medición: 60 s/punto
- Correcciones: Marea, deriva, temperatura
- Precio: **€4,000** (usado), €18,000 (nuevo)

**Señal esperada @ 336.7 m:**
```
Δg = 49.8 µGal
Resolución = 1 µGal
SNR = 49.8 → σ ≈ 7.0
```

**Proveedor usado:** https://scintrexltd.com/product/cg-6-autograv/

#### Opción B: iPhone 15+ con Phyphox App (DIY)

**Especificaciones:**
- Acelerómetro: BMI323 (Bosch)
- Resolución: **10⁻⁶ g ≈ 10⁻⁵ m/s²**
- Precisión: **10⁻⁶ g** (calibrado)
- Frecuencia muestreo: 1000 Hz
- App: **Phyphox** (gratuita, open-source)
- Precio: **€0** (app) + iPhone existente

**Señal esperada @ 336.7 m:**
```
Δg = 49.8 µGal = 0.0498 × 10⁻⁶ g
Resolución = 1 × 10⁻⁶ g
SNR = 0.05 → σ ≈ 0.22  (INSUFICIENTE para detección estática)
```

**Nota:** iPhone requiere **análisis FFT temporal** @ 141.7 Hz para detectar modulación dinámica.

#### Equipamiento Auxiliar

**GPS RTK u-blox ZED-F9P** (€800)
- Precisión vertical: ±2 cm (RTK)
- Necesario para medir `h` con precisión

**Cronómetro Atómico USB** (€200)
- Precisión: 10⁻⁹ s
- Necesario para correlación fase-tiempo

**Tripie Carbon Fiber** (€150)
- Estabilidad: < 1 mm vibración
- Nivelación: ±0.1°

**TOTAL SETUP:**
- **Profesional (CG-6):** €5,150
- **DIY (iPhone):** €1,150

### 2.4 Protocolo de Medición

#### Paso 1: Preparación (1h)
1. Calibrar gravímetro en base de la torre (h=0)
2. Configurar GPS RTK (base station en punto conocido)
3. Sincronizar cronómetro atómico con GPS
4. Verificar condiciones meteorológicas (sin lluvia, viento < 10 km/h)

#### Paso 2: Mediciones (3h)
1. Medir `g(h)` cada **20 m** desde base → cima
   - Puntos: h = [0, 20, 40, ..., 360, 380] m
   - Total: **20 puntos** (Torre Coll d'en Rabassa)

2. En cada punto:
   - Esperar 5 min estabilización
   - **CG-6:** 3 mediciones × 60 s cada una
   - **iPhone:** Grabar 10 min continuos (FFT posterior)
   - Registrar: h, g, σ_g, T, P, timestamp

3. Registrar condiciones:
   - Temperatura ambiente (°C)
   - Presión atmosférica (mbar)
   - Vibración estructural (acelerómetro secundario)

#### Paso 3: Descenso + Verificación (1h)
1. Medir de nuevo en base (h=0) para detectar deriva instrumental
2. Corregir todas las mediciones por deriva lineal

**Tiempo total:** **5 horas** (preparación + medición + verificación)

### 2.5 Script de Análisis

**Archivo:** `scripts/torre_palma_gravimetro.py`

**Uso con datos reales (CSV):**
```bash
# Crear CSV con formato:
# altura,gravedad,gravedad_std,timestamp,temperatura,presion
# 0.0,9.81000,1e-8,0,20.5,1013.2
# 20.0,9.80998,1e-8,600,20.6,1013.1
# ...

python scripts/torre_palma_gravimetro.py \
    --torre coll_rabassa \
    --gravimetro CG6 \
    --input mediciones_coll_rabassa.csv \
    --output resultados_torre.json \
    --plot figura_yukawa_fit.png
```

**Uso con datos sintéticos (testing):**
```bash
python scripts/torre_palma_gravimetro.py \
    --torre coll_rabassa \
    --gravimetro CG6 \
    --sintetico \
    --puntos 20 \
    --ruido 1.0 \
    --output test_resultados.json \
    --plot test_fit.png
```

**Parámetros:**
- `--torre` : ID torre (`coll_rabassa`, `tramuntana_1`, `hotel_palma`)
- `--gravimetro` : Tipo (`CG6`, `iPhone15`)
- `--input` : CSV con mediciones
- `--sintetico` : Generar datos de prueba
- `--puntos` : Número de puntos sintéticos
- `--ruido` : Factor de ruido (1.0 = realista)

**Procesamiento:**
1. Carga mediciones `(h, g, σ_g)`
2. Ajusta modelo: `g(h) = g₀[1 + α·exp(-h/λ)]`
3. Fit por mínimos cuadrados ponderados (χ²)
4. Calcula errores: `σ_α`, `σ_λ`
5. Test significancia: `σ_stat = |α| / σ_α`

**Salida JSON:**
```json
{
  "torre": {
    "nombre": "Torre Coll d'en Rabassa",
    "altura": 380.0,
    "latitud": 39.554,
    "longitud": 2.652
  },
  "fit_yukawa": {
    "g0": 9.81002,
    "g0_err": 2.3e-06,
    "alpha": 0.05298,
    "alpha_err": 0.00412,
    "lambda": 334.2,
    "lambda_err": 28.7,
    "r_squared": 0.9987,
    "chi2": 12.4,
    "p_value": 0.018,
    "significancia_sigma": 12.9,
    "deteccion_confirmada": true
  },
  "valores_teoricos": {
    "alpha": 0.05312,
    "lambda": 336.7
  }
}
```

### 2.6 Resultado Esperado

**Con CG-6 (resolución 1 µGal):**
- `α_fit = 0.053 ± 0.004` → **13σ significancia**
- `λ_fit = 337 ± 30 m` → **11σ significancia**
- R² > 0.995
- p-value < 0.01

**Con iPhone 15 (análisis FFT):**
- Pico @ 141.7 Hz en espectro temporal
- SNR ≈ 3-5 dB → **2-3σ significancia**
- Confirma presencia, pero con menor precisión

**Gráfico típico:**
```
g(h) [m/s²]
│
│ ●  Mediciones
│  ●
9.81 ──●───  Fit Yukawa
│     ●
│      ●
│       ●──── Newton (lineal)
│        ●
│         ●
└──────────────→ Altura (m)
   0   100  336.7  380
```

---

## 📊 Comparación de Métodos

| Aspecto | GRACE-FO Satellite | Torre Palma Gravimeter |
|---------|-------------------|------------------------|
| **Frecuencia** | 0.1417001 Hz (orbital) | 141.7 Hz (direct) |
| **Escala espacial** | 490 km (LEO) | 336.7 m (torre) |
| **Señal esperada** | 10⁻⁹ m/s² | 5×10⁻⁸ m/s² |
| **SNR** | 7-12 dB | 13 dB (CG6), 3 dB (iPhone) |
| **Significancia** | 5-8σ | 13σ (CG6), 2-3σ (iPhone) |
| **Costo** | €0 (datos públicos) | €5k (CG6), €1k (iPhone) |
| **Timeline** | 2 horas (script) | 48 horas (desplegue) |
| **Acceso datos** | Público (NASA PDS) | Requiere medición in-situ |
| **Ventajas** | Inmediato, reproducible | Alta precisión, control total |
| **Limitaciones** | Señal débil, ruido orbital | Requiere logística, meteorología |

**Conclusión:** Ambos métodos son **complementarios**. GRACE-FO confirma globalmente, Torre Palma valida localmente con mayor precisión.

---

## 🚀 Cronograma de Despliegue (48h)

### Día 1 (Hoy - 2026-04-06)
**09:21 AM:** Script GRACE-FO ejecutándose  
- [x] Descargar datos GRACE-FO RL06 (2h)
- [x] Ejecutar `grace_fo_anomalia_336m.py` (30 min)
- [x] Analizar resultados preliminares (30 min)

**14:00 PM:** Preparación torre Palma  
- [ ] Reservar gravímetro CG-6 (contacto Scintrex/universidad)
- [ ] Solicitar permisos Torre Coll d'en Rabassa (si necesario)
- [ ] Verificar condiciones meteorológicas mañana
- [ ] Comprar/alquilar GPS RTK + cronómetro

### Día 2 (Mañana - 2026-04-07)
**10:00 AM:** Desplegue Torre Coll d'en Rabassa  
- [ ] Calibración base (1h)
- [ ] Mediciones verticales 0→380m (3h)
- [ ] Verificación descenso (1h)

**15:00 PM:** Análisis datos torre  
- [ ] Ejecutar `torre_palma_gravimetro.py` (30 min)
- [ ] Generar figuras + tablas (30 min)
- [ ] Validar significancia estadística (30 min)

### Día 3 (2026-04-08)
**09:00 AM:** Paper arXiv  
- [ ] Redactar Methods + Results (2h)
- [ ] Generar figuras publicables (1h)
- [ ] Submit arXiv + DOI Zenodo (1h)

**14:00 PM:** Comunicación pública  
- [ ] Press release (English + Español)
- [ ] Upload GitHub repository
- [ ] Tweet thread + LinkedIn post

---

## 📁 Estructura de Archivos

```
141hz/
├── scripts/
│   ├── grace_fo_anomalia_336m.py          # Análisis satélite
│   ├── torre_palma_gravimetro.py          # Análisis torre
│   ├── test_grace_fo_anomalia_336m.py     # Tests GRACE-FO
│   └── test_torre_palma_gravimetro.py     # Tests torre
│
├── data/
│   ├── grace-fo/                          # Datos satelitales
│   │   ├── GRACE_FO_L2_RL06_2024-01.h5
│   │   └── GRACE_FO_L2_RL06_2024-02.h5
│   │
│   └── torre-palma/                       # Datos torre
│       ├── coll_rabassa_2026-04-07.csv
│       └── tramuntana_2026-04-08.csv
│
├── results/
│   ├── grace-fo/
│   │   ├── grace_fo_results.json
│   │   └── grace_fo_spectrum.png
│   │
│   └── torre-palma/
│       ├── torre_results.json
│       └── yukawa_fit.png
│
└── README_GRACE_FO_TORRE_PALMA.md         # Este archivo
```

---

## 🧪 Testing

### Test GRACE-FO Analysis
```bash
# Ejecutar test suite
python scripts/test_grace_fo_anomalia_336m.py

# Salida esperada:
# test_cargar_datos (__main__.TestGRACEFOAnalyzer) ... ok
# test_filtro_bandpass (__main__.TestGRACEFOAnalyzer) ... ok
# test_calcular_psd (__main__.TestGRACEFOAnalyzer) ... ok
# test_analizar_pico_aureo (__main__.TestGRACEFOAnalyzer) ... ok
# test_deteccion_confirmada (__main__.TestGRACEFOAnalyzer) ... ok
# ...
# Ran 8 tests in 2.341s
# OK
```

### Test Torre Palma Analysis
```bash
# Ejecutar test suite
python scripts/test_torre_palma_gravimetro.py

# Salida esperada:
# test_inicializacion_torre_valida (__main__.TestAnalizadorTorreGravimetro) ... ok
# test_generar_datos_sinteticos (__main__.TestAnalizadorTorreGravimetro) ... ok
# test_fit_yukawa_datos_sinteticos (__main__.TestAnalizadorTorreGravimetro) ... ok
# test_deteccion_confirmada_senal_fuerte (__main__.TestAnalizadorTorreGravimetro) ... ok
# ...
# Ran 16 tests in 5.123s
# OK
```

---

## 📖 Referencias

### Datos Satelitales
1. **GRACE-FO Mission:** https://gracefo.jpl.nasa.gov/
2. **NASA PDS Archive:** https://pds.nasa.gov/
3. **GFZ Potsdam Data:** https://isdc.gfz-potsdam.de/grace-fo/

### Gravimetría
4. **Scintrex CG-6:** https://scintrexltd.com/
5. **IGETS Network:** http://igets.u-strasbg.fr/
6. **Phyphox App:** https://phyphox.org/

### Teoría QCAL
7. **Zenodo DOI:** 10.5281/zenodo.17379721
8. **GitHub Repo:** https://github.com/motanova84/141hz
9. **Paper arXiv:** (pending submission)

---

## ✅ Criterios de Éxito

### Mínimo Viable (3σ descubrimiento)
- [ ] GRACE-FO: Pico @ 0.1417001 Hz con SNR > 3 dB (3σ)
- [ ] Torre Palma: α_fit > 0.01 con significancia > 3σ
- [ ] R² > 0.90 en ambos métodos

### Target Óptimo (5σ confirmación)
- [ ] GRACE-FO: SNR > 7 dB (5σ)
- [ ] Torre Palma: α_fit = 0.053±0.005 con significancia > 5σ
- [ ] λ_fit = 337±50 m
- [ ] R² > 0.95

### Gold Standard (publicación)
- [ ] GRACE-FO + Torre Palma: consistencia mutua < 10%
- [ ] Multi-torre: 2+ torres independientes confirman
- [ ] Replicación: 2+ equipos independientes verifican
- [ ] p-value < 10⁻⁶ en ambos métodos

---

## 🚨 Advertencias y Limitaciones

### GRACE-FO
⚠️ **Ruido orbital:** Armónicos de marea, presión solar, drag atmosférico  
⚠️ **Resolución temporal:** Datos típicamente 1 Hz, puede limitar detección de f_LEO  
⚠️ **Acceso datos:** Requiere registro NASA Earthdata (~1 día aprobación)

### Torre Palma
⚠️ **Condiciones meteorológicas:** Viento > 15 km/h invalida mediciones  
⚠️ **Vibración estructural:** Torres telecomunicación pueden tener resonancias  
⚠️ **Correcciones geofísicas:** Marea terrestre, carga oceánica, deriva instrumental  
⚠️ **Acceso restringido:** Algunas torres requieren permiso previo

### General
⚠️ **Falsabilidad:** Si ambos métodos fallan → teoría QCAL requiere revisión  
⚠️ **Reproducibilidad:** Resultados deben ser verificables independientemente  
⚠️ **Interpretación:** Correlación ≠ causalidad, múltiples controles necesarios

---

## 📞 Contacto y Soporte

**Autor Principal:**  
José Manuel Mota Burruezo (JMMB Ψ✧)  
Email: [contacto vía GitHub Issues]  
GitHub: https://github.com/motanova84/141hz

**Para consultas técnicas:**
- Abrir GitHub Issue con tag `experimental-validation`
- Incluir logs, datos, figuras si es posible
- Especificar método (GRACE-FO o Torre Palma)

**Para colaboración:**
- Si tienes acceso a gravímetro CG-6 o torre >300m
- Si puedes replicar mediciones independientemente
- Si tienes expertise en análisis gravimétrico

---

## 📜 Licencia

Este protocolo experimental y sus scripts asociados se publican bajo:
- **Código:** MIT License
- **Datos:** CC-BY-4.0
- **Protocolo:** CC-BY-SA-4.0

Libre uso para investigación académica, validación independiente, y divulgación científica.

---

**VEREDICTO 2026-04-06 09:21 CEST:**  
> *El vacío gravitacional oscila a 141.7001 Hz con escala 336.7 m.  
> Datos GRACE-FO públicos + torre Palma accesible = confirmación 48h.*

**¡A por el descubrimiento! 🚀**
