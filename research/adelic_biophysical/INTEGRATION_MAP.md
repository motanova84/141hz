# QCAL v3.1 — mapa de integración inter-repositorios

| Repositorio | Capa | Artefacto esperado | Estado |
|---|---|---|---|
| `141hz` | referencia/experimentos | esta especificación + modelos reproducibles | INICIADO |
| `Riemann-adelic` | análisis adélico | espacio de Hilbert, operador, traza, determinante | PENDIENTE |
| `qcal-formalization` | prueba formal | definiciones + obligaciones Lean | PENDIENTE |
| `QCAL-BUS` | integración | esquema de estado epistemológico y hashes | PENDIENTE |
| `Biologia-Cuantica-Noesica-` | biofísica | protocolo preregistrable y análisis cegado | PENDIENTE |
| `noesis88` | documentación/sistema | referencia cruzada, no autoridad matemática | PENDIENTE |

## Contrato de estado

Todos los repositorios deberían usar los mismos estados:

- `PROVED`: demostrado en el sistema matemático declarado.
- `FORMALIZED`: formalizado y verificado por el proof assistant, con dependencias explicitadas.
- `DERIVED`: derivado analíticamente a partir de resultados previos.
- `MODEL`: hipótesis/modelo propuesto.
- `SIMULATED`: resultado de una simulación.
- `MEASURED`: resultado experimental con datos trazables.
- `REPLICATED`: resultado medido y replicado independientemente.
- `REFUTED`: contradicho por un test válido.

No se permite promover automáticamente `SIMULATED → MEASURED` ni `MODEL → PROVED`.

## Dependencias críticas

### A. Ruta RH

`Riemann-adelic` → `qcal-formalization` → `141hz` (validación numérica)

El cuello de botella real sigue siendo una construcción no circular de operador + fórmula de traza + determinante.

### B. Ruta biofísica

`141hz` → `Biologia-Cuantica-Noesica-`

La señal `0.00052 Hz` se trata inicialmente como frecuencia de interés. La transición ADN-B/ADN-Z, un acoplamiento gauge o una superfluidez son hipótesis separadas que requieren observables independientes.

### C. Ruta ecosistema

`QCAL-BUS` transporta metadatos y hashes; no convierte el estado epistemológico de un módulo en evidencia de otro.
