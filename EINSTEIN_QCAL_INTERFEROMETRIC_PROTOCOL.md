# Einstein-QCAL Interferometric Protocol

Protocolo operativo mínimo para ejecutar la validación QCAL-E1.

## Puentes reutilizados

- Metrología de `Ψ_obs`: `/home/runner/work/141hz/141hz/scripts/protocolo_metrologia_qcal.py`
- Compatibilidad instrumental: `/home/runner/work/141hz/141hz/scripts/validacion_alternativa_interferometrica.py`
- Veredicto operacional: `/home/runner/work/141hz/141hz/qcal/einstein_qcal_e1.py`

## Ejecución

```bash
python /home/runner/work/141hz/141hz/scripts/validacion_prediccion_einstein_qcal_e1.py --output-dir results
```

## Salidas esperadas

- `results/einstein_qcal_e1_metrology_stimulated.csv`
- `results/einstein_qcal_e1_metrology_baseline.csv`
- `results/prediccion_einstein_qcal_e1.json`

## Criterios de lectura

- **SUPPORTED**: línea exacta, sensibilidad a `ΔΨ`, escalado lineal con `Δ_gap`
- **FALSIFIED**: ausencia de línea, frecuencia fuera de tolerancia o insensibilidad a la coherencia
- **INCONCLUSIVE**: datos insuficientes para uno de los dos extremos
