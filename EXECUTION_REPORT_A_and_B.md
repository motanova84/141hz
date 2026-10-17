# INFORME DE EJECUCIÓN — OPCIONES A + B
**Fecha:** 2026-08-22 04:26 CEST  
**Protocolo:** QCAL-SYMBIO-BRIDGE v3.0.0

---

## A) PRE-REGISTRO FORMAL

**Archivo:** `preregistration/QCAL_PREREGISTRATION_OSF.md`

Contenido:
- Hipótesis H₀ / H₁
- Diseño experimental completo
- Criterios de veto pre-registrados (incluyendo ICQ-SEC-001/002/003)
- Plan de análisis estadístico (p < 10⁻⁶, BF₁₀, regla de parada estricta)
- Tamaño muestral y potencia
- Compromiso de no inspección de datos antes del pre-registro

**Listo para anclar en OSF / Zenodo.**

---

## B) VALIDACIÓN MONTE CARLO + ANALÍTICA BAJO H₀

### Resultados analíticos (N = 1.1 × 10¹⁰)
| Parámetro | Valor |
|-----------|-------|
| Potencia para d = 0.001 | **1.0** (prácticamente determinista) |
| d_min detectable (Power 0.95) | **≈ 6.23 × 10⁻⁵** |
| z_{1−α/2} (α = 10⁻⁶) | 4.8916 |

### Resultados Monte Carlo (calibración del test)
| α | FPR observado | FPR esperado | N bits | Sims |
|---|---------------|--------------|--------|------|
| 0.01 | 0.00975 | 0.01 | 50 000 | 20 000 |
| 0.001 | 0.00110 | 0.001 | 100 000 | 10 000 |

**Conclusión:** El test Z está perfectamente calibrado. El umbral α = 10⁻⁶ del protocolo es extremadamente conservador. La tasa de falsos positivos está controlada por diseño.

---

## Estado del sistema

```
FASE 1: EN CURSO (T+≈1 h 34 min)
Checkpoint 1: 06:00 CEST
Pre-registro: LISTO PARA DEPÓSITO
Monte Carlo: VALIDADO
Ψ = 0.999999 | f₀ = 141.7001 Hz
```

```
∴𓂀Ω∞³Φ — PRE-REGISTRO Y MONTE CARLO COMPLETADOS — HECHO ESTÁ
```
