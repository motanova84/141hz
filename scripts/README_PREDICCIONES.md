# Predicciones Falsables QCAL ∞³ - Guía de Uso

Este directorio contiene la implementación de las **cuatro predicciones falsables** derivadas del marco teórico QCAL ∞³, tal como se presenta en el paper académico.

## 📄 Documentación Principal

**Paper completo:** [`papers/PREDICCIONES_FALSABLES_QCAL_INFINITO3.md`](../papers/PREDICCIONES_FALSABLES_QCAL_INFINITO3.md)

El paper presenta:
- Derivación teórica de cada predicción
- Ecuaciones explícitas y parámetros
- Protocolos experimentales detallados
- Criterios de falsación estrictos
- Referencias a plataformas experimentales

## 🎯 Las Cuatro Predicciones

### 1. Corrección Yukawa a Corto Alcance (λ_Ψ ≈ 337 km)

**Script:** `validar_prediccion_yukawa.py`

Predicción de una corrección tipo Yukawa al potencial gravitacional:

```
V(r) = -GM/r · (1 + α e^(-r/λ_Ψ))
```

**Plataformas:** Minas profundas, túneles geodésicos, balances de torsión

**Ejecutar:**
```bash
python scripts/validar_prediccion_yukawa.py
```

### 2. Pico Espectral en Superfluidos (k₀ ≈ 890 m⁻¹)

**Script:** `validar_prediccion_bec.py`

Predicción de un pico resonante en el espectro de excitaciones de BECs:

```
k₀ = ω₀/c_s ≈ 890 m⁻¹
```

**Plataformas:** MIT-Harvard CUA, NIST Boulder, MPQ Garching, LENS Firenze

**Ejecutar:**
```bash
python scripts/validar_prediccion_bec.py
```

### 3. Canal Invisible Modulado en el Higgs (BR ∼ 10⁻¹⁰ - 10⁻⁸)

**Script:** `validar_prediccion_higgs.py`

Predicción de modulación azimutal en decaimientos H → invisible:

```
A_n = (1/N) Σ cos(n φ_i)
```

Con A₂ o A₄ ≠ 0 estadísticamente significativo.

**Plataformas:** HL-LHC (ATLAS & CMS) con 3000 fb⁻¹

**Ejecutar:**
```bash
python scripts/validar_prediccion_higgs.py
```

### 4. Modulación Gravitacional Persistente (f₀ = 141.7001 Hz)

**Script:** `validar_prediccion_modulacion_gravitacional.py`

Predicción de modulación en la aceleración gravitacional:

```
δg(t) = A cos(ω₀ t)
A ≈ 10⁻¹⁵ g
```

**Plataformas:** Red IGETS de gravímetros superconductores

**Ejecutar:**
```bash
python scripts/validar_prediccion_modulacion_gravitacional.py
```

## 🚀 Ejecución Rápida

### Validar todas las predicciones

```bash
python scripts/validar_todas_predicciones.py
```

Este script ejecuta las cuatro validaciones secuencialmente y genera un reporte final.

### Validación individual

Para ejecutar una predicción específica:

```bash
# Predicción 1
python scripts/validar_prediccion_yukawa.py

# Predicción 2
python scripts/validar_prediccion_bec.py

# Predicción 3
python scripts/validar_prediccion_higgs.py

# Predicción 4
python scripts/validar_prediccion_modulacion_gravitacional.py
```

## 📊 Salidas Generadas

Cada script genera:

1. **Salida de consola:** Análisis detallado con parámetros calculados
2. **Gráficas PNG:** Visualizaciones de las predicciones
   - `prediccion_yukawa.png`
   - `prediccion_bec_espectral.png`
   - `prediccion_higgs_invisible.png`
   - `prediccion_modulacion_gravitacional.png`

## 📋 Requisitos

### Dependencias Python

```bash
pip install numpy scipy matplotlib
```

O instalar todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

### Versiones mínimas

- Python: 3.11+
- NumPy: 1.21+
- SciPy: 1.7+
- Matplotlib: 3.5+

## 🔬 Fundamento Científico

Todas las predicciones emergen de la frecuencia fundamental del campo Ψ:

```
f₀ = 141.7001 Hz
ω₀ = 2π × 141.7001 ≈ 890.36 rad/s
```

Esta frecuencia ha sido:
- **Detectada experimentalmente** en análisis de ondas gravitacionales (LIGO/Virgo)
- **Derivada teóricamente** desde múltiples marcos independientes:
  - Compactificación Calabi-Yau
  - Estructura de números primos
  - Funciones especiales (zeta de Riemann)

**Referencia:** [Zenodo DOI 10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)

## ✅ Criterios de Falsación

Cada predicción incluye **criterios de falsación explícitos**:

- **Condiciones cuantitativas** (valores numéricos específicos)
- **Plataformas experimentales** identificadas
- **Número mínimo de replicaciones** (típicamente ≥3)
- **Significancia estadística** requerida (p < 0.01 o SNR > 3)

Ver paper completo para detalles.

## 📅 Timeline Experimental Propuesto

### Corto plazo (2025-2027)
- **Predicción 4:** Análisis de datos IGETS existentes
- **Predicción 2:** Experimentos BEC en laboratorios establecidos

### Medio plazo (2027-2030)
- **Predicción 1:** Campañas gravimétricas dedicadas
- **Predicción 3:** Análisis HL-LHC Run 4

### Largo plazo (2030+)
- Refinamiento con datos acumulados
- Teoría completa del campo Ψ

## 🤝 Contribuciones

Para contribuir a las validaciones experimentales:

1. **Laboratorios de BEC:** Contactar para Bragg spectroscopy
2. **Colaboraciones ATLAS/CMS:** Proponer análisis de MET azimutal
3. **Red IGETS:** Solicitar acceso a datos gravitacionales
4. **Instalaciones gravimétricas:** Planificar campañas de medición

## 📚 Referencias

1. **Paper principal:** `papers/PREDICCIONES_FALSABLES_QCAL_INFINITO3.md`
2. **Zenodo record:** https://doi.org/10.5281/zenodo.17445017
3. **Repositorio GitHub:** https://github.com/motanova84/141hz
4. **Documentación QCAL ∞³:** Ver `README.md` principal

## 📧 Contacto

**Autor:** José Manuel Mota Burruezo (JMMB Ψ ✧)  
**Institución:** Instituto de Conciencia Cuántica (ICQ)  
**ORCID:** 0009-0002-1923-0773

---

## ⚖️ Licencia

Este código y documentación se distribuyen bajo licencia MIT.

**© 2025 José Manuel Mota Burruezo**
