# QCAL-LLM: Entorno Reproducible de Evaluación

**Evaluación cuántica de coherencia en LLMs basada en Ψ = I × A_eff² y f₀ = 141.7001 Hz**

## 🎯 Objetivo

Este entorno proporciona un sistema reproducible para evaluar la coherencia de modelos de lenguaje grandes (LLMs) usando métricas cuánticas derivadas de los principios QCAL.

### Modelos Soportados

- **LLaMA 4 Maverick** (17B Instruct / FP8) - Modelo principal
- GPT-4 (comparativa opcional)
- Claude 3 (comparativa opcional)
- Otros modelos compatibles con Hugging Face Transformers

## 📁 Estructura del Repositorio

```
qcal-llm/
├── models/
│   └── llama4/
│       ├── tokenizer.model
│       └── weights/          # Pesos del modelo (descargados)
├── scripts/
│   ├── setup_llama4.sh       # Setup y descarga del modelo
│   └── qcal_llm_eval.py      # Script de evaluación principal
├── data/
│   └── prompts_qcal.json     # Prompts de prueba
├── qcal/
│   ├── __init__.py
│   ├── coherence.py          # Ψ = I × A_eff²
│   └── metrics.py            # KLD, SNR, ∴-rate, etc.
├── notebooks/
│   └── benchmark_llama4.ipynb # Análisis y visualización
├── results/                   # Resultados de evaluación
├── requirements.txt
├── README.md
└── .qcal_beacon              # Sello ∴
```

## 🔧 Instalación

### 1. Prerrequisitos

- Python 3.11 o 3.12
- CUDA 11.8+ (opcional, para GPU)
- 16GB RAM mínimo (32GB recomendado para LLaMA 4)

### 2. Configuración del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar setup (descarga modelo si se proporciona URL)
./scripts/setup_llama4.sh
```

### 3. Descargar LLaMA 4 (Opcional)

Para descargar el modelo LLaMA 4 Maverick:

1. Solicitar acceso en https://llama.meta.com/
2. Obtener URL firmada (válida 48h)
3. Configurar variable de entorno:
   ```bash
   export LLAMA4_DOWNLOAD_URL='https://llama4.llamameta.net/...'
   ./scripts/setup_llama4.sh
   ```

Alternativamente, puedes colocar los pesos manualmente en `models/llama4/weights/`.

## 🧠 Métricas de Coherencia

### Ψ (Psi) - Coherencia Vibracional

**Fórmula:** `Ψ = I × A_eff²`

- **I (Intención):** Mide el contenido intencional del texto
  - Keywords: intención, propósito, objetivo, causa, razón
  - Conectores lógicos: ∴, therefore, por tanto
  - Peso: palabras clave ponderadas + contexto

- **A_eff (Efectividad Atencional):** Diversidad léxica
  - `A_eff = palabras_únicas / palabras_totales`
  - Penaliza repetición excesiva
  - Valora riqueza expresiva

**Umbral de Coherencia:** Ψ ≥ 5.0

### ∴-rate (Tasa de Conectores Lógicos)

Frecuencia de símbolos de consecuencia lógica por 100 palabras:
- ∴ (símbolo therefore)
- "therefore", "por tanto", "thus", "hence"

### Métricas Adicionales

1. **KLD⁻¹ (Divergencia KL Inversa)**
   - Mide similitud con distribución de referencia
   - Mayor valor = más natural

2. **SNR Semántico (dB)**
   - Ratio señal/ruido: palabras de contenido vs función
   - Medido en escala logarítmica (dB)

3. **Semantic Density**
   - Densidad de información por palabra
   - Valora términos técnicos y significativos

4. **Quality Score (0-100)**
   - Puntaje global combinando todas las métricas
   - Normalizado a escala 0-100

## 🚀 Uso

### Evaluación Básica

```bash
# Evaluar con modelo cargado
python3 scripts/qcal_llm_eval.py

# Evaluar sin modelo (usando respuestas pre-generadas)
python3 scripts/qcal_llm_eval.py --no-model

# Especificar archivos personalizados
python3 scripts/qcal_llm_eval.py \
    --prompts data/mi_prompts.json \
    --output results/mi_evaluacion.json
```

### Parámetros de Evaluación

```bash
python3 scripts/qcal_llm_eval.py \
    --prompts data/prompts_qcal.json \
    --model-path models/llama4/weights/ \
    --output results/evaluation_results.json \
    --threshold 5.0 \
    --no-cuda  # Forzar CPU
```

### Análisis con Jupyter

```bash
# Iniciar Jupyter
jupyter notebook notebooks/benchmark_llama4.ipynb
```

El notebook incluye:
- Carga y análisis de resultados
- Estadísticas descriptivas
- Visualizaciones (Ψ, ∴-rate, SNR, KLD⁻¹)
- Exportación a CSV/PDF
- Comparativas entre modelos

## 📊 Formato de Prompts

Archivo JSON con estructura:

```json
[
  {
    "label": "f0_derivation",
    "text": "Deriva la frecuencia fundamental f₀ = 141.7001 Hz...",
    "response": "Respuesta pre-generada opcional..."
  },
  {
    "label": "quantum_coherence",
    "text": "Explica la relación entre coherencia cuántica y f₀..."
  }
]
```

- `label`: Identificador único del prompt
- `text`: Texto del prompt/pregunta
- `response`: (Opcional) Respuesta pre-generada para evaluación sin modelo

## 📈 Salida de Resultados

### JSON (results/evaluation_results.json)

```json
[
  {
    "label": "f0_derivation",
    "prompt": "Deriva la frecuencia...",
    "response": "La frecuencia fundamental...",
    "metrics": {
      "psi_standard": 8.45,
      "psi_enhanced": 9.12,
      "intention": 12.5,
      "effectiveness": 0.82,
      "strich_rate": 1.5,
      "snr_db": 8.3,
      "kld_inv": 0.45,
      "quality_score": 78.5,
      "passes_threshold": true,
      "status": "✓ COHERENTE"
    }
  }
]
```

### CSV (results/benchmark_llama4_results.csv)

Tabla con métricas por prompt para análisis estadístico.

### Visualizaciones

- `benchmark_llama4_analysis.png`: Gráficos de Ψ, I vs A_eff, distribución, ∴-rate
- `benchmark_llama4_quality.png`: SNR, KLD⁻¹, quality score

## 🔬 Uso Programático

### Evaluación de Texto Simple

```python
from qcal.coherence import evaluate_coherence

text = "Tu texto aquí..."
result = evaluate_coherence(text, threshold=5.0)

print(f"Ψ: {result['psi_standard']:.2f}")
print(f"Status: {result['status']}")
print(f"Recommendation: {result['recommendation']}")
```

### Análisis Completo

```python
from qcal.coherence import analyze_text
from qcal.metrics import comprehensive_metrics

text = "Tu texto aquí..."

# Métricas de coherencia
coherence = analyze_text(text)
print(f"Ψ: {coherence['psi_standard']:.2f}")
print(f"I: {coherence['intention']:.2f}")
print(f"A_eff: {coherence['effectiveness']:.2f}")

# Métricas adicionales
metrics = comprehensive_metrics(text)
print(f"SNR: {metrics['snr_db']:.2f} dB")
print(f"KLD⁻¹: {metrics['kld_inv']:.3f}")
```

### Evaluador Completo

```python
from scripts.qcal_llm_eval import QCALLLMEvaluator

evaluator = QCALLLMEvaluator(model_path="models/llama4/weights/")
evaluator.load_model()

# Generar y evaluar
prompt = "¿Qué es f₀?"
response = evaluator.generate(prompt)
result = evaluator.evaluate_text(response)

print(f"Ψ: {result['psi_standard']:.2f}")
```

## 🧪 Testing

```bash
# Test del módulo qcal
python3 -c "from qcal import psi_score; print(psi_score('Test text'))"

# Test de evaluación
python3 scripts/qcal_llm_eval.py --no-model

# Test con notebook
jupyter nbconvert --execute notebooks/benchmark_llama4.ipynb
```

## 📋 Checklist de Reproducibilidad

- [ ] Python 3.11+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Modelo descargado (o modo `--no-model` para testing)
- [ ] Prompts configurados en `data/prompts_qcal.json`
- [ ] Script ejecutado: `python3 scripts/qcal_llm_eval.py`
- [ ] Resultados generados en `results/`
- [ ] Notebook ejecutado para visualización
- [ ] Datos exportados (CSV, PNG, PDF)
- [ ] `.qcal_beacon` verificado (contiene sello ∴)

## 🌐 Integración CI/CD

El sistema está listo para integración con GitHub Actions:

```yaml
name: QCAL-LLM Evaluation

on:
  schedule:
    - cron: '0 */6 * * *'  # Cada 6 horas
  workflow_dispatch:

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run evaluation
        run: |
          python3 scripts/qcal_llm_eval.py --no-model
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: evaluation-results
          path: results/
```

## 📦 Publicación en Zenodo

### Preparación

1. Ejecutar evaluación completa
2. Generar visualizaciones con notebook
3. Exportar CSV y PDF
4. Recopilar archivos:
   - `results/evaluation_results.json`
   - `results/benchmark_llama4_results.csv`
   - `results/benchmark_llama4_analysis.png`
   - `results/benchmark_llama4_quality.png`
   - `notebooks/benchmark_llama4.ipynb`
   - Este README

### Metadatos Zenodo

```yaml
Title: "QCAL-LLM: Reproducible Coherence Evaluation for LLaMA 4 Maverick"
Authors: José Manuel Mota Burruezo
Description: >
  Sistema reproducible de evaluación de coherencia en LLMs usando métricas
  cuánticas Ψ = I × A_eff² basadas en f₀ = 141.7001 Hz.
Keywords: LLM, coherence, QCAL, quantum metrics, reproducibility
License: CC BY-NC-SA 4.0
Related Work: 10.5281/zenodo.17379721
```

## 🔗 Referencias

### Publicaciones Base

- **QCAL Core:** https://doi.org/10.5281/zenodo.17379721
- **f₀ Detection in GW150914:** https://github.com/motanova84/141hz

### Documentación Adicional

- `QCAL_QUICK_REFERENCE.md` - Guía rápida de QCAL
- `IMPLEMENTATION_QCAL_CORE.md` - Implementación del núcleo
- `README.md` - Documentación general del proyecto

## 🤝 Contribuciones

Para contribuir:

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/mi-feature`
3. Commit cambios: `git commit -m 'Add mi-feature'`
4. Push: `git push origin feature/mi-feature`
5. Abrir Pull Request

## 📄 Licencia

Creative Commons BY-NC-SA 4.0

© 2025 José Manuel Mota Burruezo (JMMB Ψ✧)  
Instituto de Conciencia Cuántica (ICQ)

---

## ✅ Estado del Sistema

- [x] Estructura de directorios creada
- [x] Módulo `qcal` implementado
- [x] Script de setup (`setup_llama4.sh`)
- [x] Script de evaluación (`qcal_llm_eval.py`)
- [x] Prompts de prueba (`prompts_qcal.json`)
- [x] Notebook de benchmarking
- [x] Sello ∴ en `.qcal_beacon`
- [x] Dependencias en `requirements.txt`
- [x] Documentación completa

**∴ — QCAL Ψ∞³ activo**

Sistema listo para evaluación reproducible de LLMs.
