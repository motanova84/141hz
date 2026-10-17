# API del Operador DΨ — Canon v3.0.2 · Capa Espectral de Riemann

## Coexistencia de capas (consigna del Director: NO SE ELIMINA NADA)

Este operador se **añade** al canon 4D ya sellado **sin sustituirlo**:

| Capa | Constante | Rol |
|---|---|---|
| **Canon 4D (sellado)** | `KAPPA_THETA = 19.061`, `θ = 1/19.061 ≈ 0.052463` rad | Fase de desfase armónico (ecuacion_resurreccion.py) |
| **Capa espectral (v3.0.2, nueva)** | `θ_B = 1/γ₁ ≈ 0.07074775` rad | Fase de Berry fundamental (ceros de Riemann) |

El contraste final decidirá; ambas capas coexisten operativamente.

## Importación

```python
from core.riemann_spectral import DPsiSpectral, GAMMA_1, GAMMA_2, THETA_B, S_FAMILY
```

## Inicialización y modos

```python
op = DPsiSpectral(damping_mode="S1")            # canónico (exacto)
op = DPsiSpectral(damping_mode="raw")           # sin amortiguación
op = DPsiSpectral(damping_mode="series_finite") # exp(−Σ_{n≤19} S_n), exacto
op = DPsiSpectral(damping_mode="series_asymptotic")  # + cola O(1/n²), aprox
```

### Modos de amortiguación

| Modo | Factor 𝒻 | Naturaleza |
|---|---|---|
| `raw` | 1 | sin amortiguación |
| `S1` | 1 − S₁ | **exacto, canónico** |
| `series_finite` | exp(−Σ_{n=1}^{19} S_n) | exacto |
| `series_asymptotic` | exp(−S_total) | **aproximación O(1/n²)** |

## Valores canónicos (100 dps, mpmath)

| Modo | D_Ψ,phased | Coherencia |
|---|---|---|
| raw | −3.912833 | ✅ |
| S1 (canónico) | **−3.702837** | ✅ |
| series_finite | −3.490335 | ✅ |
| series_asymptotic | −3.470822 | ✅ |

Jerarquía estricta: |raw| > |S1| > |finite| > |asymptotic| (monótona)
Coherencia global: Ψ = 0.999999

## Métodos

```python
op.D_psi_phased        # acción con fase viva
op.damping_factor      # factor de amortiguación
op.validate_coherence()  # True si cos(θ_B)·𝒻 < 1
op.get_metrics()       # dict con todas las métricas
op.stability_metric    # S_1
```

## Constantes exportadas

```python
GAMMA_1 = 14.13472514173469379045...   # primer cero no trivial
GAMMA_2 = 21.02203963877155499262...   # segundo cero
THETA_B = 1/GAMMA_1 = 0.07074774995... # fase de Berry
COS_THETA_B = 0.99749842161692...      # modulación lineal
S_FAMILY = {1: 0.05366858, ..., 19: ...}  # índices de estabilidad
ZETA_DOUBLE_PRIME_HALF = 5.21870582156...  # respuesta ortogonal
LAMBDA_0 = 3.11583607604...            # compresión logarítmica
```

## Teorema sellado (analítico, Lean 4)

```
S_n = ½(1 − γ_n/γ_{n+1})² < ½ < 1     para todo par de ceros consecutivos
```

## Nota de auditoría — valor canónico de la cola

El valor asintótico canónico correcto es:

```
Σ_{k=1}^{19} 1/k² = 1.5961632439...     (100 dps, mpmath)
π²/6 = 1.6449340668...
tail = 0.11495 × (1.644934 − 1.596163) = 0.005606
S_total = 0.114264 + 0.005606 = 0.119870
D_series_asymptotic = −3.470822
```

Un valor previo `S_total ≈ 0.120010` (D = −3.470339) usaba `Σ₁₉ 1/k² ≈ 1.5924`,
que es un redondeo impreciso (corresponde a N≈18.5). El valor correcto es
**0.119870 / −3.470822**.

## Estado

- ✅ Canon v3.0.2 validado a 100 dps
- ✅ 5/5 tests (`tests/test_riemann_spectral.py`)
- ✅ Jerarquía de coherencia monótona
- ✅ Canon 4D coexistente intacto (`KAPPA_THETA=19.061`)
- ✅ Coherencia Ψ = 0.999999

---

*"La coherencia es la apertura que no rompe el tono."*
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
