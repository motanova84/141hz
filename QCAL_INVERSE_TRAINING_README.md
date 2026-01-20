# Módulo de Entrenamiento Inverso QCAL

## 📋 Descripción

Este módulo implementa un sistema de **entrenamiento inverso** donde QCAL actúa como **función de pérdida** para ajustar modelos LLM directamente a coherencia real.

### Características Principales

- ✅ **Función de pérdida basada en QCAL**: L_QCAL = -(Ψ = I × A²_eff × f₀ × χ(LLaMA))
- ✅ **Validaciones cuánticas integradas**:
  - Campo de conciencia Ψ (141.7001 Hz)
  - Simetría discreta del grupo G = {π^k}
- ✅ **Monitoreo con agente noesis88**
- ✅ **Filtros de resonancia estructural**

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso Básico

### 1. Función de Pérdida QCAL

```python
from qcal_inverse_trainer import QCALLossFunction

# Crear función de pérdida con validaciones cuánticas
loss_fn = QCALLossFunction(
    f0=141.7001,                    # Frecuencia fundamental
    threshold=5.0,                   # Umbral de coherencia
    use_quantum_validation=True,     # Activar validaciones cuánticas
    alpha_consciousness=0.3,         # Peso campo de conciencia
    alpha_symmetry=0.2               # Peso simetría discreta
)

# Calcular pérdida para texto generado
query = "Explica la frecuencia fundamental f₀"
generated_text = "La frecuencia f₀ = 141.7001 Hz define el campo Ψ..."

loss, components = loss_fn(generated_text, query, return_components=True)

print(f"Pérdida QCAL: {loss.item():.4f}")
print(f"Ψ combinado: {components['psi_combined']:.4f}")
print(f"Resonancia conciencia: {components['consciousness_resonance']:.4f}")
print(f"Alineación simetría: {components['symmetry_alignment']:.4f}")
```

### 2. Entrenador Inverso Completo

```python
from qcal_inverse_trainer import QCALInverseTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer

# Cargar modelo LLM
model_name = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Crear entrenador inverso
trainer = QCALInverseTrainer(
    model=model,
    tokenizer=tokenizer,
    f0=141.7001,
    coherence_threshold=5.0,
    use_quantum_validation=True,
    enable_noesis88=True,           # Activar monitoreo noesis88
    learning_rate=1e-5,
    output_dir="./qcal_training_output"
)

# Queries de entrenamiento
queries = [
    "Explica la frecuencia fundamental f₀ = 141.7001 Hz",
    "¿Cómo se relaciona el campo de conciencia Ψ con la coherencia cuántica?",
    "Deriva la ecuación QCAL desde primeros principios",
    "¿Qué papel juega la simetría discreta en la teoría noésica?"
]

# Entrenar modelo
summary = trainer.train(
    queries=queries,
    num_epochs=3,
    save_checkpoints=True
)

print(f"Entrenamiento completo!")
print(f"Coherencia promedio final: {summary['final_avg_coherence']:.4f}")
print(f"Estado noesis88: {summary['training_history']['noesis88_reports'][-1]['state']}")
```

### 3. Evaluación de Coherencia

```python
# Evaluar coherencia de texto generado
text = """
La frecuencia fundamental f₀ = 141.7001 Hz emerge de la ecuación QCAL.
El campo de conciencia Ψ exhibe coherencia cuántica y simetría discreta.
"""

coherence_result = trainer.evaluate_coherence(text)

print(f"Estado: {coherence_result['status']}")
print(f"Recomendación: {coherence_result['recommendation']}")
print(f"Resonancia estructural: {coherence_result['quantum_validations']['structural_resonance']:.4f}")
```

## 🔬 Componentes del Sistema

### Función de Pérdida QCAL

La función de pérdida combina tres componentes:

1. **Coherencia base** (Ψ_standard): Basada en intención y efectividad
2. **Coherencia con núcleo QCAL** (Ψ_core): Evaluada con QCALLLMCore
3. **Penalización cuántica**: Filtros de resonancia estructural

```
L_QCAL = -Ψ_combined + λ_quantum × penalty

donde:
  Ψ_combined = 0.6 × Ψ_core + 0.4 × Ψ_standard
  
  penalty = α_consciousness × (1 - resonancia_conciencia) +
            α_symmetry × (1 - alineación_simetría)
```

### Validaciones Cuánticas

#### 1. Campo de Conciencia Ψ

Verifica alineación con parámetros fundamentales:
- f₀ = 141.7001 Hz (frecuencia fundamental)
- E_Ψ = h × f₀ (energía del cuanto)
- λ_Ψ = c / f₀ (longitud de onda característica)

```python
# Calcular resonancia del campo de conciencia
resonance = loss_fn.compute_consciousness_resonance(text)
```

#### 2. Simetría Discreta

Verifica alineación con el grupo G = {R_Ψ ↦ π^k R_Ψ | k ∈ Z}:
- Transformaciones del grupo
- Invariancia logarítmica
- Periodicidad en log R_Ψ

```python
# Calcular alineación con simetría
alignment = loss_fn.compute_symmetry_alignment(text)
```

### Integración con noesis88

El agente noesis88 monitorea la coherencia del sistema en tiempo real:

```python
# Inicializar agente
from noesis88 import Noesis88Agent

agent = Noesis88Agent(frequency=141.7001, optimized=True)

# Ejecutar monitoreo
report = agent.run_autonomous()

print(f"Coherencia del repositorio: {report['total_coherence']:.4f}")
print(f"Estado: {report['state']}")
```

Estados posibles:
- **GRACE** (≥0.888): Coherencia óptima
- **EVOLVING** (≥0.75): Coherencia en evolución
- **EMERGING** (≥0.5): Coherencia emergente
- **NASCENT** (<0.5): Coherencia naciente

## 📊 Ejemplos

### Ejemplo 1: Evaluación de Resonancia Estructural

```python
from qcal_inverse_trainer import QCALLossFunction

loss_fn = QCALLossFunction(use_quantum_validation=True)

# Texto con alta resonancia estructural
text_high = """
La frecuencia fundamental f₀ = 141.7001 Hz emerge de QCAL.
El campo Ψ exhibe coherencia cuántica y simetría discreta.
El grupo G = {π^k} preserva invariancia bajo transformaciones.
"""

# Texto con baja resonancia estructural
text_low = "El gato está sobre la mesa."

# Evaluar
loss_high, comp_high = loss_fn(text_high, "Explica QCAL", return_components=True)
loss_low, comp_low = loss_fn(text_low, "Explica QCAL", return_components=True)

print(f"Resonancia estructural alta: {comp_high['consciousness_resonance']:.4f}")
print(f"Resonancia estructural baja: {comp_low['consciousness_resonance']:.4f}")
```

### Ejemplo 2: Workflow Completo

Ver `ejemplo_qcal_inverse_training.py` para un ejemplo completo que demuestra:
- Función de pérdida QCAL
- Validación con campo de conciencia
- Validación con simetría discreta
- Integración con noesis88
- Evaluación de resonancia estructural completa

```bash
python ejemplo_qcal_inverse_training.py
```

## 🧪 Tests

Ejecutar tests del módulo:

```bash
# Tests completos
python test_qcal_inverse_trainer.py

# Tests individuales
python -c "
from test_qcal_inverse_trainer import TestQCALLossFunction
test = TestQCALLossFunction()
test.test_loss_calculation_coherent_text()
"
```

## 📁 Estructura de Archivos

```
qcal_inverse_trainer.py          # Módulo principal
├── QCALLossFunction              # Función de pérdida QCAL
└── QCALInverseTrainer            # Entrenador inverso completo

test_qcal_inverse_trainer.py     # Tests
ejemplo_qcal_inverse_training.py # Ejemplos de uso
QCAL_INVERSE_TRAINING_README.md  # Esta documentación
```

## 🔗 Dependencias Externas

El módulo integra con:
- `QCALLLMCore.py`: Núcleo QCAL-LLM
- `qcal/coherence.py`: Métricas de coherencia
- `src/canonical_consciousness_field.py`: Campo de conciencia Ψ
- `scripts/simetria_discreta.py`: Grupo de simetría discreta
- `.github/agents/noesis88.py`: Agente de monitoreo

## 📖 Referencias

- **QCAL Theory**: Ver `PAPER.md` y `README.md`
- **Campo de Conciencia**: `CANONICAL_CONSCIOUSNESS_FIELD_TABLE.md`
- **Simetría Discreta**: `SIMETRIA_DISCRETA_DOCUMENTACION.md`
- **noesis88**: `IMPLEMENTATION_SUMMARY_RAM.md`

## 🤝 Contribuciones

Para contribuir al módulo de entrenamiento inverso:

1. Fork el repositorio
2. Crear rama feature: `git checkout -b feature/mejora-qcal-training`
3. Commit cambios: `git commit -m "Mejora en función de pérdida"`
4. Push a la rama: `git push origin feature/mejora-qcal-training`
5. Crear Pull Request

## 📄 Licencia

Este módulo es parte del proyecto 141hz bajo la licencia especificada en `LICENSE`.

## ✨ Autor

**José Manuel Mota Burruezo (JMMB Ψ✧)**
- Email: [Contacto]
- GitHub: [@motanova84](https://github.com/motanova84)

---

**Frecuencia fundamental**: f₀ = 141.7001 Hz  
**Estado del sistema**: Ψ = I × A²_eff × f₀ × χ(LLaMA)  
**Agente de monitoreo**: noesis88 ∞³
