# ÍNDICE DE DOCUMENTACIÓN COMPLETA — PROTOCOLO QCAL
## Instituto de Conciencia Cuántica (ICQ)
### Documento Maestro de Inventario | Versión 1.0.0 | 2026-08-22

**Identificador de Sistema:** QCAL-SYMBIO-BRIDGE v2.0.0  
**Frecuencia Base:** f₀ = 141.7001 Hz  
**Coherencia Objetivo:** Ψ = 0.999999  

---

## 1. DOCUMENTOS CIENTÍFICOS PRINCIPALES

| # | Archivo | Descripción | Formato |
|---|---------|-------------|---------|
| 1 | `DOCUMENTO_MAESTRO_QCAL_Protocolo_Experimental_Completo_v1.docx` | **Documento central.** Propuesta experimental completa + Apéndice de implementación. Incluye hipótesis, protocolos A/B, arquitectura, pre-registro OSF, potencia estadística, ética, cronograma y código de referencia. | DOCX (~1 MB) |
| 2 | `Propuesta_Experimental_Consciencia_Cuantica_v1.docx` | Propuesta experimental original (versión anterior). | DOCX |
| 3 | `Apendice_Implementacion_Completo_v1.docx` | Apéndice técnico de implementación (código, NIST, veto, Bayes, GUI). | DOCX |
| 4 | `Propuesta_Experimental_Consciencia_Cuantica_v1.pdf` | Versión PDF de la propuesta. | PDF |

---

## 2. CÓDIGO FUENTE OPERATIVO

| # | Archivo | Descripción | Líneas / Estado |
|---|---------|-------------|-----------------|
| 5 | `qcal_v2/unified_qcal_pipeline.py` | **Pipeline unificado v2.0.0.** Integración completa: Adquisición HDF5 + HMAC-SHA256 Merkle, Veto ambiental en tiempo real, Análisis estadístico (Z, KS, χ², entropía), Inferencia Bayesiana BF₁₀, Correlación EEG-Gamma, Orquestador thread-safe. | 609 líneas — SINTAXIS OK |
| 6 | `test_pipeline.py` | Script de prueba del pipeline de adquisición básico. | Verificado |

---

## 3. PROTOCOLOS DE CALIBRACIÓN Y OPERACIÓN

| # | Archivo | Descripción |
|---|---------|-------------|
| 7 | `qcal_v2/protocolo_calibracion_qrng.md` | **ICQ-CAL-001.** Protocolo completo de calibración QRNG en 5 fases: estabilización térmica/EM (24 h), caracterización de sesgo (10¹⁰ bits), perfilado de deriva, replicabilidad inter-sesión, validación del veto. |
| 8 | `qcal_v2/registro_inicio_fase1.md` | **ICQ-CAL-001-FASE1-INIT.** Acta formal de inicio de FASE 1 (Estabilización Térmica/EM). Timestamp 2026-08-22 02:52:00 +02:00. Sala vacía. Modo CALIBRATION. |

---

## 4. DATOS DE SESIÓN (HDF5)

| # | Archivo | Descripción |
|---|---------|-------------|
| 9 | `qcal_v2/qcal_unified_session.h5` | Archivo de sesión generada durante la verificación del pipeline unificado. |
| 10 | `quantum_consciousness_experiment.h5` | Archivo de prueba anterior del pipeline de adquisición. |

---

## 5. ESTRUCTURA DEL PROTOCOLO EXPERIMENTAL

### Hipótesis
- **H₀:** No hay desviación estadística detectable atribuible a la atención consciente enfocada.
- **H₁:** Existe desviación significativa (Δμ, ΔH(X) o Δ𝒱) asociada a la atención enfocada.

### Protocolos
- **Protocolo A:** QRNG de fotones individuales (divisor 50/50).
- **Protocolo B:** Interferometría de fotón único (visibilidad de franjas).

### Controles
- Condición A: Atención enfocada
- Condición B: Atención dispersa / pasiva
- Condición C: Control máquina (sala vacía)

### Requisitos mínimos de rigor
- Pre-registro en OSF antes de datos
- Automatización máxima + cegamiento criptográfico
- Tamaño muestral para d ≈ 0.001, α = 10⁻⁶, potencia ≥ 0.95
- Replicación independiente como condición sine qua non
- Exclusión automática de artefactos ambientales

---

## 6. ESTADO OPERATIVO ACTUAL (2026-08-22 02:55 CEST)

| Fase | Estado |
|------|--------|
| Diseño experimental | **COMPLETADO** |
| Código unificado v2.0.0 | **DESPLEGADO Y VERIFICADO** |
| Protocolo de calibración ICQ-CAL-001 | **ACTIVO** |
| FASE 1 — Estabilización térmica/EM (24 h) | **EN CURSO** (iniciada 02:52) |
| FASE 2 — Caracterización de sesgo | Pendiente de cumplimiento FASE 1 |
| Ensayo formal con operador humano | Bloqueado hasta dictamen APTO de calibración |

---

## 7. SELLO DE SISTEMA

```
QCAL-SYMBIO-BRIDGE v2.0.0
f₀ = 141.7001 Hz
Ψ = 0.999999
∴𓂀Ω∞³Φ — EL INSTRUMENTO ES EL TEMPLO — HECHO ESTÁ
```

**Documentación completa anclada.**  
**Inventario cerrado y coherente.**

