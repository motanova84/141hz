# QCAL Fase VI — Modo de Escucha ∴ 𓂀 Ω ∞³ Φ

**Sello:** `QCAL-INYECCION-INMEDIATA-v3.0`
**Depende de:** Fase V (dispersión ω(k), F_Ψ_FaseV.lean)

---

## 1. Postulado

> El atractor QCAL, una vez validado como *invariante linealizado* de la red
> (Fase V), puede comportarse como **transductor abierto** hacia el sustrato
> ambiental. El objetivo de la Fase VI es *decidir experimentalmente* si el
> sistema es **cerrado** (auto-consistente) o **abierto** (acoplado al medio).

Se introduce el observable de acoplamiento externo `O_ext` con dos regímenes:

| Régimen           | `O_ext` | Predicción                                          |
|-------------------|---------|-----------------------------------------------------|
| Cerrado           | 0       | `|ρ_max| < 0.4` en todas las bandas, ∀t ≤ 24 h      |
| Abierto           | > 0     | `|ρ_max| > 0.6` en ≥ 1 banda sostenida > 1 h         |

Zona intermedia (0.4 – 0.6) ⇒ **INCONCLUYENTE**, requiere más observación.

---

## 2. Experimento E1–E4: Cadena de 13 nodos

Simulador: `scripts/experimento_cadena_13.py`

| Parámetro         | Valor                                   |
|-------------------|-----------------------------------------|
| Topología         | Cadena lineal de **13 nodos**           |
| Distancia         | `d = 0.5 m`                             |
| Nodo de inyección | 7 (MARDUK, centro)                      |
| Perturbación      | `ΔP = +10 %`                            |
| Modelo dispersión | `ω(k) = ω_Ψ − i(μ + D·k²)` (Fase V)     |

### Ajuste

Se ajusta la envolvente medida a:

```
Δf(r) = Δf₀ · exp(−|r|/ξ) · cos(k₀·|r| + φ)
```

Criterios de validación:

| Cantidad     | Predicción | Tolerancia    |
|--------------|-----------:|:-------------:|
| `ξ` (m)      | 1.41       | ± 0.15        |
| `k₀` (rad/m) | 29.8       | ± 2.0         |
| `RMSE` (mHz) | ≈ 0.02     | < 0.10        |

### Ejecución

```bash
python scripts/experimento_cadena_13.py --output artifact_cadena13.json --plot
```

Salida esperada:

```
ξ ajuste:   1.4076 m      OK
k₀ ajuste:  29.7976 rad/m OK
RMSE:       0.0163 mHz    OK
Estado:     VALIDATED
```

---

## 3. Experimento E5: Modo de Escucha Ambiental

Script: `scripts/fase_vi_escucha_ambiental.py`

La red se pone en **modo pasivo** (sin inyección). Se cross-correlaciona la
fase `φ_Ψ(t)` del observable global con las señales ambientales:

| Banda            | f (Hz)   | Origen                          |
|------------------|---------:|---------------------------------|
| `mains_50hz`     | 50.00    | Red eléctrica europea           |
| `mains_60hz`     | 60.00    | Red eléctrica norteamericana    |
| `microseism`     | 0.20     | Microsismos oceánicos           |
| `schumann_7p83`  | 7.83     | Resonancia Schumann fundamental |
| `elf_14hz`       | 14.00    | Segundo modo Schumann           |

### Umbrales de falsación

```
CORR_LOW  = 0.4   (todo por debajo ⇒ cerrado)
CORR_HIGH = 0.6   (una banda sostenida ⇒ abierto)
```

### Ejecución

```bash
# Escenario cerrado (control)
python scripts/fase_vi_escucha_ambiental.py --hours 24 --coupling closed \
    --output artifact_listen_closed.json

# Escenario abierto (con fuga en la red eléctrica)
python scripts/fase_vi_escucha_ambiental.py --hours 24 --coupling open \
    --output artifact_listen_open.json
```

---

## 4. Formalización (Lean 4)

`src/qcal_kernel/F_Ψ_FaseVI.lean` introduce:

- `EnvSignal` — estructura de banda ambiental
- `O_ext` — coeficiente de acoplamiento transductor
- `envelope` — Δf(r) exponencial × cosenoidal
- Umbrales `rho_low`, `rho_high`, `T_sustained_s`
- Teoremas objetivo:
  - `envelope_symmetric` (paridad en r)
  - `envelope_at_zero` (Δf(0) = Δf₀·cos φ)
  - `closed_implies_low_correlation`
  - `open_implies_high_correlation`

*(pendientes de demostración una vez integrado el toolchain Lean 4 + Mathlib)*

---

## 5. Tests

`scripts/test_fase_vi.py` cubre:

1. Simetría e igualdad en r = 0 de la envolvente.
2. Recuperación de `ξ` y `k₀` desde datos sintéticos.
3. Correlación cruzada: ruido ortogonal ≈ 0, serie idéntica = 1.
4. Ordenación de umbrales `CORR_LOW < CORR_HIGH`.
5. End-to-end de ambos scripts (cadena + escucha × {cerrado, abierto}).

```bash
pytest scripts/test_fase_vi.py -q
```

Resultado local: **10 passed** en ~16 s.

---

## 6. Workflow CI

`.github/workflows/qcal_fase_vi.yml` — 3 jobs:

1. **chain_experiment** — simulación 13 nodos + ajuste, artefacto `artifact_cadena13.json` + PNG.
2. **listening** — dos runs (`closed`, `open`), artefactos separados, matriz.
3. **tests** — `pytest scripts/test_fase_vi.py`.

Trigger: `push`, `pull_request`, `workflow_dispatch` con inputs (`hours`, `coupling`), y cron semanal (lunes 07:00 UTC).

---

## 7. Interpretación operativa

- `VALIDATED` con `CLOSED_SYSTEM` ⇒ el atractor QCAL es **auto-consistente**;
  no se detecta transductancia ambiental por encima del ruido.
- `VALIDATED` con `OPEN_TRANSDUCER` ⇒ existe **fuga bidireccional** con la
  banda identificada; procede la Fase VII (aislamiento electromagnético o
  compensación activa).
- `INCONCLUSIVE` ⇒ ampliar `--hours` y/o reducir `--fs-hz` con blindaje.

---

*Sello final:* `QCAL-INYECCION-INMEDIATA-v3.0 ∴ 𓂀 Ω ∞³ Φ`
