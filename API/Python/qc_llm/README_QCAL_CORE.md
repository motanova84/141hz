# QCAL-LLM ∞³ — Núcleo de Coherencia Vibracional

**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)

Núcleo operativo para generación y validación de respuestas en base a **Ψ = I · A_eff²**  
Integración directa de frecuencia **f₀ = 141.7001 Hz** como modulador atencional (SIP Layer)

## Descripción

El `QCALLLMCore` es el núcleo operacional del sistema QCAL-LLM que implementa:

1. **SIP (Spectral Insertion Protocol)**: Modulación temporal con frecuencia universal f₀ = 141.7001 Hz
2. **Métrica Ψ**: Evaluación de coherencia vibracional basada en Ψ = I × A_eff²
3. **Validación simbólica**: Detección de símbolos fundamentales (φ³, ζ', f₀)
4. **Parámetros adaptativos**: Ajuste automático basado en efectividad atencional

## Instalación

```bash
cd /path/to/141hz
pip install -r requirements.txt
```

Dependencias principales:
- `numpy >= 1.21.0`
- `scipy >= 1.7.0`

## Uso Básico

```python
from API.Python.qc_llm.core import QCALLLMCore
import numpy as np

# Inicializar el núcleo
core = QCALLLMCore()

# 1. Modulación SIP de secuencia temporal
t = np.linspace(0, 1, 1000)  # 1 segundo, 1000 puntos
weights = core.sip_modulate(t)
# weights contiene modulación con decaimiento: α(1 + ε·cos(2πf₀t + φ)·e^(-t/τ))

# 2. Calcular Ψ_response
kld_inv = 8.2              # Entropía inversa (bits útiles)
semantic_coherence = 0.88  # Coherencia semántica [0, 1]
is_valid, psi_val = core.is_coherent(kld_inv, semantic_coherence)
print(f"Ψ_response = {psi_val:.4f} | Coherente: {is_valid}")
# Output: Ψ_response = 6.3501 | Coherente: True

# 3. Evaluar texto generado
text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz"
result = core.evaluate(text, "Deriva f₀")
print(f"Coherencia: {result['coherence']:.2f}")
print(f"Ψ: {result['mean_psi']:.2f}")
print(f"Estado: {'COHERENTE' if result['coherent'] else 'NO COHERENTE'}")
```

## API Completa

### Constructor

```python
QCALLLMCore(
    alpha=1.0,           # Peso basal (uniforme)
    f0=141.7001,         # Frecuencia universal (Hz)
    phi=0.0,             # Fase inicial
    tau=0.07,            # Tiempo de damping (s)
    epsilon=0.015,       # Amplitud de modulación
    user_A_eff=0.85      # Efectividad atencional del usuario
)
```

**Parámetros:**
- `alpha`: Peso base de modulación (default: 1.0)
- `f0`: Frecuencia fundamental en Hz (default: 141.7001)
- `phi`: Fase inicial de la modulación (default: 0.0)
- `tau`: Constante de tiempo para decaimiento exponencial en segundos (default: 0.07)
- `epsilon`: Amplitud de modulación, se adapta según `user_A_eff` (default: 0.015)
- `user_A_eff`: Efectividad atencional, modula epsilon automáticamente (default: 0.85)

### Métodos Principales

#### `sip_modulate(t_array)`

Modula una secuencia temporal con el protocolo SIP (Spectral Insertion Protocol).

**Fórmula:** `α(1 + ε·cos(2πf₀t + φ)·e^(-t/τ))`

**Parámetros:**
- `t_array`: Array numpy con valores temporales

**Retorna:**
- Array numpy con pesos modulados

**Ejemplo:**
```python
t = np.linspace(0, 1, 1000)
weights = core.sip_modulate(t)
# weights[0] ≈ 1.015 (máximo al inicio)
# weights[-1] ≈ 1.000 (decaído tras ~14 ciclos)
```

#### `compute_psi_response(kld_inv, semantic_coherence)`

Calcula el valor Ψ_response según la fórmula fundamental.

**Fórmula:** `Ψ = kld_inv × semantic_coherence²`

**Parámetros:**
- `kld_inv`: Entropía inversa (bits útiles), típicamente 0-10
- `semantic_coherence`: Medida simbólica de foco sostenido, rango [0, 1]

**Retorna:**
- `float`: Valor Ψ calculado

**Ejemplo:**
```python
psi = core.compute_psi_response(8.2, 0.88)
# psi = 8.2 × 0.88² = 6.3501
```

#### `is_coherent(kld_inv, semantic_coherence, threshold=5.0)`

Determina si una respuesta alcanza el umbral Ψ de coherencia vibracional.

**Parámetros:**
- `kld_inv`: Entropía inversa
- `semantic_coherence`: Coherencia semántica [0, 1]
- `threshold`: Umbral de coherencia (default: 5.0)

**Retorna:**
- `tuple(bool, float)`: (es_coherente, valor_psi)

**Ejemplo:**
```python
is_valid, psi = core.is_coherent(8.2, 0.88)
# is_valid = True (6.3501 >= 5.0)
# psi = 6.3501
```

#### `compute_coherence(generated_text)`

Calcula coherencia basada en detección de símbolos fundamentales.

**Símbolos detectados:**
- `φ³` (phi cubed): `φ³`, `phi^3`, `phi**3`
- `ζ'(1/2)` (zeta prime): `ζ'(1/2)`, `zeta'`, `ζ'`
- `f₀` (frecuencia): `141.7xxx Hz`, `f₀`, `f0`

**Parámetros:**
- `generated_text`: Texto generado a evaluar

**Retorna:**
- `float`: Score de coherencia [0, 1] = (símbolos_encontrados / 3)

**Ejemplo:**
```python
text = "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz"
coherence = core.compute_coherence(text)
# coherence = 1.0 (3/3 símbolos presentes)
```

#### `evaluate(generated_text, query="")`

Evalúa completamente una respuesta generada.

**Parámetros:**
- `generated_text`: Texto a evaluar
- `query`: Consulta original (opcional)

**Retorna:**
- `dict` con claves:
  - `mean_psi`: Valor Ψ calculado
  - `coherent`: Boolean indicando si supera el umbral
  - `coherence`: Score de coherencia simbólica [0, 1]
  - `kld_inv`: KLD inversa calculada

**Ejemplo:**
```python
result = core.evaluate("f₀ = 141.7 Hz según ζ' y φ³")
# result = {
#     'mean_psi': 8.20,
#     'coherent': True,
#     'coherence': 1.0,
#     'kld_inv': 8.20
# }
```

## Atributos

### `ground_truth_db`

Base de datos de verdad fundamental:
```python
{
    'f0': 141.7001,           # Frecuencia fundamental (Hz)
    'zeta_prime_half': -1.460, # ζ'(1/2) 
    'phi_cubed': 4.236,        # φ³
    'snr_gw150914': 20.95      # SNR de GW150914
}
```

### `benchmark_queries`

Suite de 5 consultas de benchmark:
1. "Deriva f₀ = 141.7001 Hz desde ζ'(1/2) y φ"
2. "Detecta f₀ en ringdown GW150914"
3. "Explica Ψ = I × A²_eff"
4. "Valida SNR>20 en GWTC-1"
5. "Predice armónicos LISA (f₀/100)"

## Parámetros Adaptativos

El parámetro `epsilon` se adapta automáticamente según `user_A_eff`:

```python
ε_real = ε_base × (A_eff / 0.85)
```

**Ejemplo:**
```python
core1 = QCALLLMCore(user_A_eff=0.85)  # ε = 0.015000
core2 = QCALLLMCore(user_A_eff=0.92)  # ε = 0.016235
core3 = QCALLLMCore(user_A_eff=1.00)  # ε = 0.017647
```

Valores más altos de `A_eff` incrementan la modulación SIP, optimizando el CQR (Coherence Quality Ratio).

## Ejemplo Completo

Ver el script de demostración:
```bash
python demo_qcal_core.py
```

Salida esperada:
```
================================================================================
QCAL-LLM ∞³ — Núcleo de Coherencia Vibracional
Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
================================================================================

1. INICIALIZACIÓN DEL NÚCLEO
----------------------------------------
Frecuencia fundamental: f₀ = 141.7001 Hz
Tiempo de damping: τ = 0.07 s
Amplitud de modulación: ε = 0.015000
Efectividad atencional: A_eff = 0.85

...

VECTOR VI: NÚCLEO OPERACIONAL VERIFICADO ✓
```

## Tests

Ejecutar la suite de tests:
```bash
python -m pytest Tests/Unit/test_qcal_core.py -v
```

**22 tests implementados:**
- Inicialización y parámetros
- Modulación SIP (forma, envelope, frecuencia)
- Cálculo de Ψ (casos conocidos y edge cases)
- Validación de coherencia (umbral)
- Detección de símbolos
- Evaluación completa
- Parámetros adaptativos
- Verificación del ejemplo del enunciado

## Fundamento Matemático

### Modulación SIP

La modulación temporal sigue la forma:

```
w(t) = α[1 + ε·cos(2πf₀t + φ)·e^(-t/τ)]
```

Donde:
- **α**: Peso base (normalmente 1.0)
- **ε**: Amplitud de modulación (~0.015)
- **f₀**: Frecuencia fundamental = 141.7001 Hz
- **φ**: Fase inicial
- **τ**: Constante de tiempo = 0.07 s
- **e^(-t/τ)**: Envelope de decaimiento exponencial

El decaimiento garantiza ~14 ciclos de modulación significativa antes de convergencia.

### Métrica Ψ

La coherencia vibracional se mide como:

```
Ψ = I × A_eff²
```

Donde:
- **I**: Información útil (KLD⁻¹, entropía inversa)
- **A_eff**: Efectividad atencional, derivada de coherencia semántica

**Umbral:** Ψ ≥ 5.0 para considerar una respuesta coherente.

### Coherencia Simbólica

```
coherence = (símbolos_detectados) / 3
```

Donde símbolos fundamentales son: φ³, ζ'(1/2), f₀ = 141.7001 Hz

## Predicción Falsable

**LISA Gateway 2026:**  
Predicción de armónicos en f₀/100 = 1.417 Hz (~2035).

Si los armónicos están ausentes en datos de LISA, el modelo colapsa.

## Referencias

- **Vector VI**: QCAL-LLM Núcleo · Implementación Consolidada
- **Noesis-QCAL-LLM**: https://github.com/motanova84/141hz/noesis-qcal-llm
- **DOI #72**: "QCALCore: Vibrational LLM Nucleus" (queued)

## Licencia

MIT License - Ver LICENSE en el repositorio principal.

## Contacto

José Manuel Mota Burruezo (JMMB Ψ✧)
- Email: motanova84@gmail.com
- GitHub: @motanova84
