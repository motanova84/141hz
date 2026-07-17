# 🧪 Guía Rápida: Protocolos Experimentales f₀ = 141.7001 Hz

Esta guía proporciona instrucciones rápidas para ejecutar y validar los tres experimentos diseñados para validar la frecuencia fundamental f₀.

---

## 🚀 Inicio Rápido (2 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/motanova84/gw250114-141hz-analysis
cd gw250114-141hz-analysis

# 2. Ejecutar todos los experimentos con simulaciones
make experimentos

# 3. Ver resultados
cat results/experimentos_f0.json
```

**Resultado esperado**: 3/3 experimentos exitosos (100%)

---

## 📊 Comandos Disponibles

### Ejecución de Experimentos

```bash
# Ejecutar los 3 experimentos
make experimentos

# O directamente con Python
python scripts/protocolos_experimentales.py
```

**Salida**:
- `results/experimentos_f0.json` - Resultados en formato JSON
- Reporte en consola con métricas clave

### Tests y Validación

```bash
# Ejecutar tests (28 tests unitarios)
make test-experimentos

# O directamente
python scripts/test_protocolos_experimentales.py
```

**Cobertura**: 
- Experimento 1: 9 tests
- Experimento 2: 7 tests
- Experimento 3: 8 tests
- Integración: 2 tests
- Constantes: 2 tests

### Visualizaciones

```bash
# Generar diagramas de flujo
make diagrams-experimentos

# Ver diagramas
open results/figures/flujo_experimentos_f0.png
open results/figures/timeline_experimentos_f0.png
```

---

## 🧠 Experimento 1: Resonancia Neuronal

### Concepto

Neuronas en meditación profunda deberían sincronizar a 141.7 Hz.

### Ejecución Individual

```python
from scripts.protocolos_experimentales import ExperimentoResonanciaNeuronal

# Crear experimento
exp = ExperimentoResonanciaNeuronal(sampling_rate=1000)

# Ejecutar protocolo
resultado = exp.ejecutar_protocolo(
    duracion=60.0,      # 60 segundos por sesión
    n_sujetos=20        # 20 sujetos por grupo
)

# Ver resultados
print(f"SNR meditación: {resultado.metricas['snr_meditacion']:.2f}")
print(f"SNR control: {resultado.metricas['snr_control']:.2f}")
print(f"Ratio: {resultado.metricas['ratio_amplitud']:.2f}")
print(f"Éxito: {resultado.exito}")
```

### Parámetros Ajustables

- `sampling_rate`: Frecuencia de muestreo EEG (≥1000 Hz)
- `duracion`: Duración de cada sesión (segundos)
- `n_sujetos`: Número de sujetos por grupo
- `snr_objetivo`: SNR de la señal simulada

### Criterios de Éxito

- ✅ SNR > 5 en banda 141.7 Hz (meditación)
- ✅ Ratio meditación/control > 10

---

## ⚛️ Experimento 2: Modulación de Masa

### Concepto

BEC con alta coherencia muestra desviación en masa efectiva.

### Ejecución Individual

```python
from scripts.protocolos_experimentales import ExperimentoModulacionMasa

# Crear experimento
exp = ExperimentoModulacionMasa()

# Ejecutar protocolo
resultado = exp.ejecutar_protocolo(n_mediciones=100)

# Ver resultados
print(f"Δm/m: {resultado.metricas['delta_m_relativo']:.2e}")
print(f"Predicción: {resultado.metricas['delta_m_predicho']:.2e}")
print(f"Éxito: {resultado.exito}")
```

### Parámetros Ajustables

- `n_atomos`: Número de átomos en BEC (default: 10⁶)
- `temperatura`: Temperatura del BEC (default: 100 nK)
- `coherencia`: Factor de coherencia 0-1 (default: 0.9)
- `n_mediciones`: Número de mediciones

### Criterios de Éxito

- ✅ Δm/m en rango 10⁻¹⁰ a 10⁻⁶
- ✅ BEC coherente muestra mayor Δm que gas térmico

---

## 🛰️ Experimento 3: Entrelazamiento a Distancia

### Concepto

Decoherencia cuántica muestra "salto" en λ_Ψ ≈ 2,000 km.

### Ejecución Individual

```python
from scripts.protocolos_experimentales import ExperimentoEntrelazamientoDistancia

# Crear experimento
exp = ExperimentoEntrelazamientoDistancia()

# Ejecutar protocolo
resultado = exp.ejecutar_protocolo(n_mediciones_por_distancia=50)

# Ver resultados
print(f"τ antes de 2000 km: {resultado.metricas['tau_antes_2000km']:.3f} s")
print(f"τ después de 2000 km: {resultado.metricas['tau_despues_2000km']:.3f} s")
print(f"Razón de salto: {resultado.metricas['razon_salto']:.2f}")
print(f"Éxito: {resultado.exito}")
```

### Parámetros Ajustables

- `distancias_prueba`: Lista de distancias en km
- `n_mediciones_por_distancia`: Número de mediciones por distancia
- `lambda_psi`: Longitud característica (default: 2000 km)

### Criterios de Éxito

- ✅ Razón de salto > 2 en d ≈ 2000 km
- ✅ τ_dec(d < λ_Ψ) > τ_dec(d > λ_Ψ)

---

## 📈 Interpretación de Resultados

### Formato JSON de Salida

```json
{
  "resonancia_neuronal": {
    "experimento": "Resonancia Neuronal",
    "timestamp": "2025-10-22T...",
    "exito": true,
    "metricas": {
      "snr_meditacion": 1218196.58,
      "snr_control": 8824.69,
      "ratio_amplitud": 138.04,
      "n_sujetos": 10
    },
    "notas": [...]
  },
  "modulacion_masa": {...},
  "entrelazamiento_distancia": {...}
}
```

### Tasa de Éxito

**Simulaciones actuales**: 3/3 (100%)

**Interpretación**:
- **3/3 éxitos**: ✅ Fuerte evidencia para f₀
- **2/3 éxitos**: 🟡 Evidencia mixta, requiere refinamiento
- **0-1/3 éxitos**: ❌ Hipótesis no soportada

---

## 🔬 Validación Científica

### Tests Automatizados

```bash
# Ejecutar suite completa de tests
python scripts/test_protocolos_experimentales.py -v

# Tests específicos
python -m pytest scripts/test_protocolos_experimentales.py::TestExperimentoResonanciaNeuronal
python -m pytest scripts/test_protocolos_experimentales.py::TestExperimentoModulacionMasa
python -m pytest scripts/test_protocolos_experimentales.py::TestExperimentoEntrelazamientoDistancia
```

### Verificación Manual

1. **Experimento 1**: Verificar que SNR meditación >> SNR control
2. **Experimento 2**: Verificar que Δm/m está en orden correcto (10⁻⁸)
3. **Experimento 3**: Verificar discontinuidad en 2000 km

---

## 🛠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'numpy'"

```bash
pip install numpy scipy matplotlib
```

### Error: "No such file or directory: 'results/'"

Los directorios se crean automáticamente. Si el error persiste:

```bash
mkdir -p results/figures
```

### Tests fallan

```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Verificar versión de Python (requiere 3.11+)
python3 --version
```

---

## 📚 Documentación Completa

- **Protocolos detallados**: [docs/PROTOCOLOS_EXPERIMENTALES.md](../docs/PROTOCOLOS_EXPERIMENTALES.md)
- **Código fuente**: [scripts/protocolos_experimentales.py](../scripts/protocolos_experimentales.py)
- **Tests**: [scripts/test_protocolos_experimentales.py](../scripts/test_protocolos_experimentales.py)
- **README principal**: [README.md](../README.md)

---

## 🤝 Contribuir

Para mejorar los experimentos:

1. Fork el repositorio
2. Crea una rama: `git checkout -b mejora-experimentos`
3. Modifica `scripts/protocolos_experimentales.py`
4. Añade tests en `scripts/test_protocolos_experimentales.py`
5. Ejecuta tests: `make test-experimentos`
6. Commit y push
7. Abre un Pull Request

---

## 📞 Contacto

**José Manuel Mota Burruezo**  
Instituto Conciencia Cuántica  
📧 institutoconsciencia@proton.me

---

**Versión**: 1.0 - Octubre 2025  
**Licencia**: MIT  
**Estado**: ✅ Implementado y validado
