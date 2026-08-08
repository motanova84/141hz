# QCAL-E1 Experimental Contract

Predicción falsable operacional del postulado Einstein-QCAL.

## Identificador

- **Predicción**: `QCAL-E1`
- **Frecuencia central exacta**: `141.7001 Hz`
- **Tolerancia instrumental**: `±0.0001 Hz`
- **Ventana espectral mínima**: `100-200 Hz`
- **Sensibilidad mínima**: `S_h(f) ≤ 10^-24 Hz^-1/2`
- **Constante fija**: `α = 0.1184`

## Condiciones de falsación

La predicción queda **falsada** si ocurre cualquiera de estas condiciones:

1. No aparece un pico en `141.7001 Hz` cuando `Ψ < 0.999999` y la sensibilidad instrumental cumple el umbral.
2. El pico aparece, pero fuera de `±0.0001 Hz`.
3. La propagación de fase resulta insensible a `ΔΨ > 0`.

## Condición de soporte

La predicción queda **soportada** si aparece una línea en `141.7001 Hz`, la fase depende de la coherencia y la respuesta operacional escala linealmente con `Δ_gap = 2π f₀ (1 - Ψ)`.

## Artefacto auditable

Cada corrida de `/home/runner/work/141hz/141hz/scripts/validacion_prediccion_einstein_qcal_e1.py` produce:

- CSV metrológico estimulado
- CSV metrológico basal
- JSON con contrato, entradas, observables, compatibilidad interferométrica, anclajes del ecosistema y veredicto
