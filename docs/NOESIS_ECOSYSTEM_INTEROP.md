# NOESIS Ecosystem Interoperability Map

`141hz` is the integration spine for the current NOESIS/QCAL bridge.

## Active nodes

| Node | Repository | Interface |
|---|---|---|
| Spectral/adelic | `Riemann-adelic` | adelic operators, spectral data, provenance |
| Formal | `qcal-formalization` | explicit constants and formal invariants |
| Field | `field-qcal` | effective `T_mu_nu^Noesis` / Einstein-QCAL boundary |
| Timing | `RelojCuantico-141Hz-QCAL` | `f0`, `omega0`, `fB`, `omegaB` |
| Biological | `Biologia-Cuantica-Noesica-` | PHOENIX / ultra-slow signal layer |
| Transport | `QCAL-BUS` | ecosystem routing and state propagation |
| Integration | `141hz` | cross-node tests, state vectors and CI |

## Canonical state vector

```text
f0_hz       = 141.7001
fB_hz       = 0.00052
Psi_target  = 0.999999
alpha_inv   = 137.035999084
bridge      = fB_hz / f0_hz
```

Every cross-node result should carry repository + commit + parameter-set provenance. This turns the ecosystem into a reproducible graph rather than a collection of isolated claims.

## Data flow

```text
Riemann-adelic -> qcal-formalization -> 141hz
                         |               |
                         v               v
                   field-qcal       RelojCuantico
                         |               |
                         +-------+-------+
                                 v
                              PHOENIX
                                 |
                                 v
                              QCAL-BUS
```
