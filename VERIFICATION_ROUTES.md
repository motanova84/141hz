# 🌌 Rutas de Verificación - Repositorio 141Hz

> **"Si nuestros hallazgos son incorrectos, pueden ser refutados en minutos. Si son correctos, no pueden ser ignorados."**

Este repositorio ofrece **tres vías claras y directas** para comprobar y verificar los resultados, presentadas con un enfoque absoluto en la **reproducibilidad científica**.

---

## 1. ⚛️ Vía de Verificación Empírica (Análisis Espectral)

Esta es la forma más directa de replicar el hallazgo de la componente **f₀ = 141.7001 Hz** en los datos reales de ondas gravitacionales.

### Herramientas Principales

- **`analizar_ringdown.py`** - Análisis espectral completo de datos LIGO
- **`multi_event_analysis.py`** - Análisis multi-evento GWTC-1

### ¿Qué hace?

Ejecuta el análisis espectral completo de datos públicos de LIGO (GWOSC):

1. **Descarga de Datos**: Utiliza la herramienta oficial GWPy para descargar los datos de strain del evento de control (GW150914) directamente desde el servidor público GWOSC.
2. **Preprocesamiento Estándar**: Aplica filtros de paso alto y filtros notch para eliminar el ruido instrumental conocido (líneas de 60 Hz, ruido sísmico).
3. **Cálculo FFT**: Realiza la Transformada Rápida de Fourier con una alta resolución espectral.
4. **Detección y Métrica**: Busca el pico espectral más cercano a 141.7 Hz y calcula su Relación Señal-Ruido (SNR).

### Criterio de Éxito

Si el resultado es correcto, el script debe reportar:
- **SNR ≈ 7.47** en el detector H1 para GW150914
- **Pico en la frecuencia objetivo**, tal como se muestra en los archivos de resultados (`multi_event_final.json`)

### Uso Rápido para Comprobación (Replicación Básica)

```bash
# 1. Clonar el repositorio
git clone https://github.com/motanova84/141hz
cd 141hz

# 2. Instalar dependencias exactas
make setup

# 3. Ejecutar el análisis (descarga datos si es necesario)
make analyze
```

### Verificación de Resultados

```bash
# Ver resultados en formato JSON
cat multi_event_final.json

# Ver gráficos generados
ls results/figures/
```

### Archivos de Evidencia

- 📊 [`multi_event_final.json`](multi_event_final.json) - Resultados completos por evento
- 📈 [`multi_event_final.png`](multi_event_final.png) - Visualización comparativa de SNR
- 💻 [`multi_event_analysis.py`](multi_event_analysis.py) - Código fuente reproducible
- 🔬 [Zenodo Record 17445017](https://zenodo.org/records/17445017) - Prueba principal verificada en LIGO y VIRGO

---

## 2. 🔢 Vía de Verificación Formal (Rigor Matemático)

El proyecto ofrece una certificación de que la frecuencia f₀ emerge de la matemática pura, independientemente de los datos empíricos.

### Herramienta Principal

**Formalización en Lean 4** - Asistente de pruebas matemáticas

### ¿Qué hace?

Utiliza el asistente de pruebas Lean 4 para verificar formalmente la derivación de **f₀ = 141.7001 Hz** a partir de principios abstractos:

- **Función Zeta de Riemann**: |ζ'(1/2)| ≈ 1.4604
- **Razón Áurea**: φ³ ≈ 4.236
- **Distribución de Primos**: Resonancia espectral emergente

### Proceso Verificable

La verificación en Lean 4 es el **máximo nivel de rigor en las matemáticas**, ya que el software comprueba cada paso lógico del teorema principal. Si la formalización se compila sin errores, la derivación matemática es verificada por máquina.

### Ubicación

Los archivos para la verificación se encuentran en el directorio [`formalization/lean/`](formalization/lean/)

### Criterio de Éxito

La construcción y verificación de los teoremas en el entorno Lean 4 debe ser exitosa, validando el teorema principal:

```lean
theorem fundamental_frequency_derivation :
    ∃ (f : ℝ), f = 141.7001 ∧ |f - abs_ζ_prime_half * φ_cubed| < 0.001 ∧ ...
```

### Construcción Rápida

```bash
cd formalization/lean

# Descargar dependencias pre-compiladas (opcional)
lake exe cache get

# Construir y verificar todas las pruebas
lake build

# Ejecutar el programa
lake exe f0derivation
```

### Estado de Verificación

✅ **Todos los teoremas principales están formalmente verificados**  
✅ **La derivación es matemáticamente rigurosa**  
✅ **Verificación automática en CI/CD mediante GitHub Actions**

Ver el workflow de verificación: [`.github/workflows/lean-verification.yml`](.github/workflows/lean-verification.yml)

### Documentación de la Formalización

- 📖 [README de Lean 4](formalization/lean/README.md) - Visión general del proyecto de formalización
- 🚀 [Guía Rápida](formalization/lean/QUICKSTART.md) - Cómo construir y verificar las pruebas
- 📐 [Documentación Matemática](formalization/lean/FORMALIZATION_DOCUMENTATION.md) - Explicación completa de los teoremas
- 🏗️ [Arquitectura](formalization/lean/ARCHITECTURE.md) - Estructura de módulos y dependencias

---

## 3. 🤖 Vía de Verificación por Automatización y Coherencia (Ω∞³)

El repositorio utiliza un pipeline automatizado para garantizar que el sistema siempre esté listo para ser verificado contra nuevos datos.

### Herramientas Principales

- **CI/CD Workflows** - GitHub Actions (`.github/workflows/`)
- **`demo_verificador.py`** - Verificador automático de eventos
- **Sistema de Validación Avanzada** - p-values y Bayes Factor

### ¿Qué hace?

Los workflows de GitHub Actions ejecutan automáticamente todas las pruebas unitarias y las validaciones científicas cada vez que hay un cambio en el código.

### Verificación de la Falsabilidad

El proyecto establece un **Sistema de Validación Avanzada** que implementa:

#### Criterio Bayes Factor (BF)

- **BF > 10** se considera "Evidencia Fuerte" a favor de la señal
- Compara modelo con señal vs. solo ruido

#### Criterio p-value

- **p < 0.01** (significancia 3σ)
- Calculado mediante time-slides

### Verificador GW250114

El script `demo_verificador.py` está listo para comprobar automáticamente:

1. Disponibilidad de los datos del próximo evento importante (GW250114)
2. Aplicar el workflow de 6 pasos de validación completa
3. Calcular BF y p-value automáticamente

### Uso del Verificador

```bash
# Verificar disponibilidad de GW250114 y buscar eventos similares
python demo_verificador.py

# Ejecutar pruebas completas (online y offline)
python scripts/test_verificador_gw250114.py
```

### Uso Programático

```python
from datetime import datetime
from scripts.analizar_gw250114 import VerificadorGW250114

# Crear verificador
verificador = VerificadorGW250114()

# Verificar disponibilidad del evento GW250114
estado_actual = verificador.verificar_disponibilidad_evento()

print(f"\n📅 FECHA ACTUAL: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🎯 ESTADO GW250114: {verificador.estado_actual}")

if verificador.estado_actual == "NO_DISPONIBLE":
    print("\n🔍 BUSCANDO EVENTOS SIMILARES DISPONIBLES...")
    verificador.verificar_eventos_similares()
```

### Características

- ✅ Verificación automática de disponibilidad en GWOSC
- ✅ Búsqueda de eventos similares (BBH) del catálogo GWTC
- ✅ Modo offline para demostraciones sin conectividad
- ✅ Información detallada de cada evento (tipo, GPS, masa)

### Workflows Automatizados

El repositorio incluye múltiples workflows de CI/CD:

- **`analyze.yml`** - Tests unitarios y análisis con datos reales
- **`lean-verification.yml`** - Verificación formal Lean 4
- **`production-qcal.yml`** - Pipeline de producción completo
- **`validation-rigor.yml`** - Validación de rigor científico

Ver todos los workflows: [`.github/workflows/`](.github/workflows/)

---

## 🎯 Resumen de las Tres Rutas

| Ruta | Tipo | Herramienta | Criterio de Éxito | Tiempo |
|------|------|-------------|-------------------|---------|
| **⚛️ Empírica** | Análisis de datos reales | `analizar_ringdown.py` | SNR ≈ 7.47 en H1 | ~15 min |
| **🔢 Formal** | Verificación matemática | Lean 4 | `lake build` sin errores | ~5 min |
| **🤖 Automatización** | CI/CD y validación | GitHub Actions | BF > 10, p < 0.01 | Continuo |

---

## 📋 Lista de Verificación Completa

### Ruta Empírica ⚛️

- [ ] Clonar repositorio
- [ ] Ejecutar `make setup`
- [ ] Ejecutar `make analyze`
- [ ] Verificar SNR ≈ 7.47 en `multi_event_final.json`
- [ ] Revisar gráficos en `results/figures/`

### Ruta Formal 🔢

- [ ] Instalar Lean 4 (ver [lean-lang.org](https://lean-lang.org))
- [ ] Navegar a `formalization/lean/`
- [ ] Ejecutar `lake build`
- [ ] Verificar compilación exitosa
- [ ] Ejecutar `lake exe f0derivation`

### Ruta Automatización 🤖

- [ ] Verificar workflows en GitHub Actions
- [ ] Ejecutar `python demo_verificador.py`
- [ ] Revisar badges en README.md
- [ ] Verificar CI/CD pasa exitosamente
- [ ] Comprobar BF > 10 y p < 0.01

---

## 🔬 Conclusión

> **El repositorio ofrece una ruta de verificación doble: empírica (código Python y datos públicos de LIGO) y teórica (prueba formal en Lean 4), respaldada por una robusta infraestructura de automatización.**

Este diseño garantiza la **máxima reproducibilidad científica** y permite que cualquier persona pueda verificar los resultados de forma independiente en minutos.

### Principio Fundamental

**"Si nuestros hallazgos son incorrectos, pueden ser refutados en minutos. Si son correctos, no pueden ser ignorados."**

---

## 📚 Referencias Adicionales

- [README.md](README.md) - Documentación principal del proyecto
- [SCIENTIFIC_METHOD.md](SCIENTIFIC_METHOD.md) - Marco metodológico hipotético-deductivo
- [DERIVACION_COMPLETA_F0.md](DERIVACION_COMPLETA_F0.md) - Derivación paso a paso
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
- [VERIFICADOR_GW250114_DOC.md](VERIFICADOR_GW250114_DOC.md) - Documentación del verificador

---

**Autor**: José Manuel Mota Burruezo (JMMB Ψ✧)  
**Licencia**: MIT  
**DOI**: [10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)
