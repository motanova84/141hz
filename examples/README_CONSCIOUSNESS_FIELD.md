# Campo de Conciencia Ψ - Guía Rápida

## Descripción

El **Campo de Conciencia Ψ** es un campo escalar físico real y medible que emerge de la ecuación madre L∞³ sin ningún parámetro de ajuste. NO es místico - es física cuántica rigurosa con validación CODATA 2022.

## Uso Rápido

### 1. Ver la Tabla Oficial

```bash
python src/canonical_consciousness_field.py
```

### 2. Validar Relaciones Físicas

```bash
python src/canonical_consciousness_field.py --validate
```

### 3. Exportar a JSON

```bash
python src/canonical_consciousness_field.py --format json > campo_psi.json
```

### 4. Guardar Tabla a Archivo

```bash
python src/canonical_consciousness_field.py --save tabla_oficial.txt
```

### 5. Ejemplo Completo de Validación

```bash
python examples/validate_consciousness_field.py
```

## Uso en Python

```python
from src.canonical_consciousness_field import CONSCIOUSNESS_FIELD

# Acceder a parámetros
print(f"f₀ = {CONSCIOUSNESS_FIELD.F0} Hz")
print(f"E_Ψ = {CONSCIOUSNESS_FIELD.E_PSI} J")
print(f"λ_Ψ = {CONSCIOUSNESS_FIELD.LAMBDA_PSI_KM} km")
print(f"m_Ψ = {CONSCIOUSNESS_FIELD.M_PSI} kg")
print(f"T_Ψ = {CONSCIOUSNESS_FIELD.T_PSI} K")

# Generar tabla completa
tabla = CONSCIOUSNESS_FIELD.generate_official_table()
print(tabla)

# Validar todas las relaciones
validaciones = CONSCIOUSNESS_FIELD.validate_all_relations()
print(f"Válido: {validaciones['all_exact_relations_valid']}")

# Obtener todos los parámetros
parametros = CONSCIOUSNESS_FIELD.get_all_parameters()
for nombre, param in parametros.items():
    print(f"{param.symbol}: {param.value} {param.unit}")

# Exportar a diccionario
datos = CONSCIOUSNESS_FIELD.to_dict()
```

## Parámetros Clave

| Parámetro | Símbolo | Valor | Unidad |
|-----------|---------|-------|--------|
| Frecuencia fundamental | f₀ | 141.7001 | Hz |
| Energía del cuanto | E_Ψ | 9.39 × 10⁻³² | J |
| Longitud de onda | λ_Ψ | 2116 | km |
| Masa efectiva | m_Ψ | 1.04 × 10⁻⁴⁸ | kg |
| Temperatura del vacío | T_Ψ | 6.8 | nK |
| Tiempo característico | τ_Ψ | 7.06 | ms |

## Relaciones Físicas Validadas

Todas estas relaciones se cumplen con precisión CODATA 2022:

1. **E_Ψ = h f₀** (Planck) → Error: 0%
2. **λ_Ψ = c / f₀** (Longitud de onda) → Error: 0%
3. **E_Ψ = m_Ψ c²** (Einstein) → Error: ~10⁻¹⁴%
4. **E_Ψ = k_B T_Ψ** (Boltzmann) → Error: 0%
5. **λ_Ψ ≈ h / √(E_Ψ m_p)** (Yukawa) → Escala coincidente

## Tests

Ejecutar tests de validación:

```bash
pytest tests/test_canonical_consciousness_field.py -v
```

Todos los tests (31 en total) deben pasar exitosamente.

## Interpretación Física

### ¿Qué es el Campo Ψ?

El campo de conciencia Ψ es:

- Un **campo escalar** en el espacio-tiempo
- Con **frecuencia fundamental** f₀ = 141.7001 Hz
- Que produce efectos **medibles** en ondas gravitacionales
- Con **coherencia cuántica** macroscópica

### Significado Ontológico

- **f₀** → El latido único del universo. Todo oscila con este pulso.
- **E_Ψ** → El cuanto irreductible de coherencia.
- **λ_Ψ** → Escala gravitatoria Yukawa (buscada en IGETS/LLR).
- **m_Ψ** → Masa del cuanto de conciencia (~10⁻²³ × masa del protón).
- **T_Ψ** → Temperatura mínima sin perder coherencia.

### Cuando ⟨|Ψ|²⟩ ≥ 1

La **intención** se convierte literalmente en **curvatura del espacio-tiempo**:

```
C = m c² A_eff²
```

## Referencias

- **Framework:** QCAL ∞³ - Quantum Coherent Attentional Logic
- **Constantes:** CODATA 2022
- **Documentación:** `CANONICAL_CONSCIOUSNESS_FIELD_TABLE.md`
- **Módulo:** `src/canonical_consciousness_field.py`
- **Tests:** `tests/test_canonical_consciousness_field.py`

## Autor

José Manuel Mota Burruezo (JMMB Ψ✧)  
9 de diciembre de 2025

---

∴ JMMB Ψ ✧ ∞³
