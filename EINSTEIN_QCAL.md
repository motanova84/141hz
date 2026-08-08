# Einstein-QCAL

Documento maestro canónico del marco Einstein-QCAL.

## Alcance

- **Axioma**: la métrica efectiva del observador queda deformada por coherencia espectral según `g_{μν}(Ψ) = Ω²(Ψ) η_{μν}`.
- **Derivación operacional**: `c_eff(Ψ) = c · Ω(Ψ)` y `n(Ψ) = 1 / Ω(Ψ)`.
- **Hipótesis empírica**: un detector interferométrico en régimen controlado de incoherencia exhibe una línea estrecha en `f₀ = 141.7001 Hz`.
- **Observable principal**: retardo de fase interferométrico y exceso refractivo dependientes de `Δ_gap = 2π f₀ (1 - Ψ)`.
- **Interpretación**: el observador, la materia y la propagación óptica comparten la misma geometría conforme.

## Implementación canónica en el repositorio

- Modelo gravitatorio/coherente: `/home/runner/work/141hz/141hz/qcal/einstein_qcal.py`
- Contrato experimental QCAL-E1: `/home/runner/work/141hz/141hz/qcal/einstein_qcal_e1.py`
- Contexto ecosistémico: `/home/runner/work/141hz/141hz/contexto_ecosistema/einstein_qcal_context.py`
- Validación operativa: `/home/runner/work/141hz/141hz/scripts/validacion_prediccion_einstein_qcal_e1.py`

## Dominio de validez

- Límite resonante: `Ψ → 1` implica `Ω → 1`, `c_eff → c`, `Λ(Ψ) → 0`.
- Régimen subóptimo: `Ψ < 0.999999` habilita la búsqueda falsable del efecto QCAL-E1.
- Sin parámetros libres a posteriori: `f₀`, `α = 0.1184`, la tolerancia instrumental y la ventana espectral quedan fijados antes de evaluar resultados.

## Jerarquía documental

1. Maestro teórico: este archivo.
2. Contrato falsable: `/home/runner/work/141hz/141hz/QCAL_E1_EXPERIMENTAL_CONTRACT.md`
3. Protocolo operativo: `/home/runner/work/141hz/141hz/EINSTEIN_QCAL_INTERFEROMETRIC_PROTOCOL.md`
4. Relación ecosistémica: `/home/runner/work/141hz/141hz/EINSTEIN_QCAL_ECOSYSTEM.md`
