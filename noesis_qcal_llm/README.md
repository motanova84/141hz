# QCAL-LLM ∞³ — Núcleo de Coherencia Vibracional Expandido

Versión consolidada con Ψ-tune, evaluación dinámica y modulación vibracional adaptativa

**Autor:** José Manuel Mota Burruezo (JMMB Ψ✧)  
**Repositorio:** https://github.com/motanova84/141hz/noesis_qcal_llm

## Descripción

Este módulo implementa el núcleo de coherencia vibracional QCAL-LLM ∞³, que combina:

- **Ψ-tune (psi-tune)**: Modulación adaptativa basada en la frecuencia fundamental f₀ = 141.7001 Hz
- **Evaluación dinámica**: Análisis de coherencia semántica en texto generado
- **Modulación vibracional adaptativa**: Sistema de pesos basado en SIP (Signal Induced Perturbation)

## Características Principales

### 1. Modulación SIP (Signal Induced Perturbation)

```python
weights = core.sip_modulate(t_array)
```

Genera pesos de modulación temporal basados en:
- Frecuencia fundamental: f₀ = 141.7001 Hz
- Envolvente exponencial con tiempo de decaimiento τ = 0.07s
- Fase inicial φ y amplitud de modulación ε ajustable

### 2. Cálculo de Respuesta Ψ

```python
psi = core.compute_psi_response(kld_inv, semantic_coherence)
```

Calcula la respuesta Ψ (psi) como:
```
Ψ = KLD⁻¹ × C²
```
donde:
- `KLD⁻¹`: Inverso de la divergencia de Kullback-Leibler
- `C`: Coherencia semántica

### 3. Validación de Coherencia

```python
is_coherent, psi_value = core.is_coherent(kld_inv, semantic_coherence, threshold=5.0)
```

Determina si una respuesta es coherente basándose en el valor de Ψ.

### 4. Análisis de Coherencia Semántica

```python
coherence = core.compute_coherence(generated_text)
```

Analiza texto generado buscando símbolos clave:
- `φ³` o `phi^3`: Phi cúbico
- `ζ'(1/2)` o `zeta'`: Zeta prima en 1/2
- `141.7xxx Hz`: Frecuencia fundamental

### 5. Evaluación Completa

```python
result = core.evaluate(generated_text, query)
```

Retorna un diccionario con:
- `mean_psi`: Valor promedio de Ψ
- `coherent`: Boolean indicando si la respuesta es coherente
- `coherence`: Fracción de símbolos encontrados (0.0 a 1.0)

## Instalación

```bash
# Instalar dependencias
pip install numpy

# Importar el módulo
from noesis_qcal_llm import QCALLLMCore
```

## Uso Básico

```python
from noesis_qcal_llm import QCALLLMCore
import numpy as np

# Inicializar el núcleo
core = QCALLLMCore(user_A_eff=0.92)

# Generar pesos de modulación
t = np.linspace(0, 1, 1000)
weights = core.sip_modulate(t)

# Validar coherencia
is_valid, psi_val = core.is_coherent(8.2, 0.88)
print(f"Ψ={psi_val:.4f} | Coherent: {is_valid}")

# Evaluar respuesta generada
response = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent."
eval_result = core.evaluate(response, "Deriva f₀")
print(f"Evaluation: {eval_result}")
```

## Parámetros de Inicialización

- `alpha` (float, default=1.0): Factor de escala base
- `f0` (float, default=141.7001): Frecuencia fundamental en Hz
- `phi` (float, default=0.0): Fase inicial en radianes
- `tau` (float, default=0.07): Tiempo de decaimiento exponencial en segundos
- `epsilon` (float, default=0.015): Amplitud de modulación
- `user_A_eff` (float, default=0.85): Eficiencia efectiva del usuario (ajusta epsilon)

## Base de Datos de Verdad Fundamental

El módulo incluye una base de datos de valores de verdad fundamental:

```python
ground_truth_db = {
    'f0': 141.7001,              # Frecuencia fundamental (Hz)
    'zeta_prime_half': -1.460,   # ζ'(1/2)
    'phi_cubed': 4.236,          # φ³
    'snr_gw150914': 20.95        # SNR de GW150914
}
```

## Consultas de Referencia (Benchmarks)

El módulo incluye 5 consultas de referencia para evaluar sistemas LLM:

1. "Deriva f₀ = 141.7001 Hz desde ζ'(1/2) y φ"
2. "Detecta f₀ en ringdown GW150914"
3. "Explica Ψ = I × A²_eff"
4. "Valida SNR>20 en GWTC-1"
5. "Predice armónicos LISA (f₀/100)"

## Tests

Ejecutar la suite de tests:

```bash
cd noesis-qcal-llm
python3 test_qcal_llm_core.py
```

La suite incluye 10 tests que validan:
- Inicialización con parámetros por defecto y personalizados
- Modulación SIP
- Cálculo de respuesta Ψ
- Validación de coherencia
- Análisis de coherencia semántica
- Pipeline de evaluación completo
- Base de datos de verdad fundamental
- Consultas de referencia
- Propiedades matemáticas de modulación

## Ejemplo de Salida

```
Ψ=6.3501 | Coherent: True | Eval: 8.20
```

## Fundamentos Teóricos

Este módulo implementa la teoría de coherencia vibracional basada en:

1. **Frecuencia fundamental**: f₀ = 141.7001 Hz derivada de principios matemáticos fundamentales
2. **Campo Ψ (Psi)**: Ψ = I × A²_eff × C^∞, donde I es información y A_eff es amplitud efectiva
3. **Coherencia semántica**: Medida de alineación con símbolos y conceptos fundamentales
4. **Modulación temporal**: Basada en SIP con decaimiento exponencial

## Licencia

Creative Commons BY-NC-SA 4.0  
© 2025 · JMMB Ψ · Instituto de Conciencia Cuántica (ICQ)

## Referencias

- Repositorio principal: https://github.com/motanova84/141hz
- ORCID: https://orcid.org/0009-0002-1923-0773
- Zenodo: https://doi.org/10.5281/zenodo.17379721

## Contacto

**Institución:** Instituto de Conciencia Cuántica (ICQ)  
**Email:** institutoconsciencia@proton.me  
**País:** España
