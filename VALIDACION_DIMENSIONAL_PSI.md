# Validación Dimensional de Ψ = I · A_eff²

## Problema Resuelto Matemáticamente

La fórmula de coherencia QCAL:

```
Ψ = I · A_eff²
```

donde:
- **I**: Información (contenido intencional) — dimensional [bits, nats, etc.]
- **A_eff**: Efectividad atencional — **adimensional** (coeficiente 0 ≤ A_eff ≤ 1)
- **Ψ**: Coherencia vibracional — dimensional [bits, nats, etc.] (hereda de I)

## Demostración de Consistencia Dimensional

### 1. A_eff es Adimensional

```
A_eff = palabras_únicas / palabras_totales
[A_eff] = [conteo] / [conteo] = 1 (sin dimensiones)
```

### 2. Ψ Conserva las Dimensiones de I

```
[Ψ] = [I · A_eff²]
    = [I] · [A_eff²]
    = [I] · [1]²
    = [I]
```

**✓ NO HAY RUPTURA DIMENSIONAL**

### 3. Comportamiento Límite Correcto

```
lim(A_eff→1) Ψ = lim(A_eff→1) [I · A_eff²]
                = I · 1²
                = I
```

**Interpretación física**: Efectividad perfecta (A_eff = 1) → Coherencia = Información (Ψ = I)

### 4. Análogo a Física Estándar

| Fórmula física | Constante adimensional | Descripción |
|----------------|------------------------|-------------|
| E_binding = α² · m_e · c² | α ≈ 1/137 | Constante estructura fina (QED) |
| σ ∝ αs² | αs ≈ 0.1 | Acoplamiento fuerte (QCD) |
| Γ_decay ∝ g² | g ≈ 0.65 | Acoplamiento débil |
| V(φ) = λ · φ⁴ | λ ≈ 0.13 | Autoacoplamiento Higgs |
| **Ψ = I · A_eff²** | **A_eff ≈ 0.92** | **Efectividad QCAL** |

**Conclusión**: A_eff actúa como un factor de acoplamiento estándar. **Esto es física textbook**.

## Uso

### Validación Automatizada

```python
from qcal import complete_dimensional_validation, print_validation_report

# Ejecutar validación completa
results = complete_dimensional_validation(I=10.0, A_eff=0.92)

# Imprimir reporte
print_validation_report(results)
```

**Salida**:
```
══════════════════════════════════════════════════════════════════════
PROBLEMA RESUELTO MATEMÁTICAMENTE
══════════════════════════════════════════════════════════════════════

Fórmula: Ψ = I · A_eff²

Dimensionalidad:
  • I tiene dimensión [bits]
  • A_eff es adimensional (coeficiente de efectividad) [1]
  • A_eff² es adimensional [1]
  • Ψ tiene dimensión [bits]

✓ NO HAY RUPTURA DIMENSIONAL
✓ I fija la escala dimensional
✓ A_eff es puramente adimensional
✓ La fórmula es matemáticamente consistente

══════════════════════════════════════════════════════════════════════
```

### Ejemplo Manual

```python
from qcal import psi_score, compute_intention, compute_effectiveness

text = "Este es un texto coherente con propósito claro"

# Calcular componentes
I = compute_intention(text)
A_eff = compute_effectiveness(text)
Psi = I * (A_eff ** 2)

print(f"I = {I:.4f} (información)")
print(f"A_eff = {A_eff:.4f} (efectividad, adimensional)")
print(f"Ψ = {Psi:.4f} (coherencia)")
```

## Tests

**34 tests** validando:
- ✓ A_eff es adimensional
- ✓ Ψ es dimensionalmente consistente
- ✓ Comportamiento límite correcto
- ✓ Comparación con factores de acoplamiento en física
- ✓ Casos extremos y reproducibilidad

```bash
pytest tests/test_dimensional_analysis_psi.py -v
# 34 passed in 0.13s
```

## Archivos Relacionados

- **Módulo principal**: [`qcal/dimensional_analysis_psi.py`](qcal/dimensional_analysis_psi.py)
- **Tests**: [`tests/test_dimensional_analysis_psi.py`](tests/test_dimensional_analysis_psi.py)
- **Validación**: [`core/validate_dimensional_psi.py`](core/validate_dimensional_psi.py)
- **Ejemplo**: [`examples/ejemplo_dimensional_psi.py`](examples/ejemplo_dimensional_psi.py)
- **Documentación**: [`PROBLEMA_MATEMATICO_RESUELTO.md`](PROBLEMA_MATEMATICO_RESUELTO.md)

## Referencias

- **Autor**: José Manuel Mota Burruezo (JMMB Ψ ∞³)
- **Fecha**: 8 de febrero de 2026
- **Licencia**: MIT

---

**Este módulo certifica matemáticamente que Ψ = I · A_eff² es dimensionalmente consistente y no presenta ruptura dimensional.**
