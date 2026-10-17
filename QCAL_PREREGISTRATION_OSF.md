# PRE-REGISTRO FORMAL — QCAL-SYMBIO-BRIDGE v3.0.0
## Protocolo Experimental de Interacción Consciencia–Sistemas Cuánticos

**Instituto de Conciencia Cuántica (ICQ)**  
**Documento:** ICQ-PREREG-001  
**Fecha de pre-registro:** 2026-08-22 04:24:00 CEST (02:24:00 UTC)  
**Versión del protocolo:** QCAL-SYMBIO-BRIDGE v3.0.0  
**Sello:** ∴𓂀Ω∞³Φ  

---

## 1. Título
**Test experimental rigurosamente pre-registrado de desviaciones estadísticas en generadores cuánticos de números aleatorios (QRNG) asociadas a atención consciente humana enfocada.**

## 2. Hipótesis

### Hipótesis Nula (H₀)
La distribución de bits generados por el QRNG bajo la condición de atención consciente enfocada es estadísticamente indistinguible de la distribución bajo condiciones de control (pasivo / máquina), una vez aplicados los criterios de exclusión ambiental, de inducción en f₀ y de fatiga cognitiva pre-registrados.

### Hipótesis Alternativa (H₁)
La atención consciente enfocada produce una desviación estadísticamente detectable (Δμ ≠ 0 o ΔH(X) ≠ 0) en las métricas del QRNG respecto a los controles, con tamaño de efecto reproducible y estable tras correcciones por múltiples comparaciones.

## 3. Diseño Experimental

| Elemento | Especificación |
|----------|----------------|
| Sistema cuántico | QRNG fotónico (divisor de haz 50/50 + detectores de fotón único) |
| Condiciones | A: Atención enfocada; B: Control pasivo; C: Control máquina (sala vacía) |
| Asignación | Aleatorizada y cegada criptográficamente (AES-256-GCM) |
| Bloque temporal | 60 s |
| Sesiones | Exactamente 100 (regla de parada estricta) |
| Bits por condición (objetivo) | ≥ 1.1 × 10¹⁰ |
| Blindaje | Jaula de Faraday ≥ 80 dB, control térmico, mesa óptica |

## 4. Criterios de Exclusión / Veto (pre-registrados)

Un bloque se descarta **antes** del análisis primario si:

1. ΔT > 0.5 °C (peak-to-peak)  
2. EMF > 2.0 µT  
3. Vibración > 0.05 m/s²  
4. **ICQ-SEC-001:** Z_power en banda (141.7001 ± 0.1) Hz > 3σ (baseline FASE 1)  
5. **Veto Cognitivo:** α/θ EEG > 4.0 (fatiga)  
6. Fallo de integridad HMAC o escritura HDF5  

Todos los vetos (PASSED y VETOED) se registran en el **Árbol de Merkle Dual (ICQ-SEC-003)**.

## 5. Plan de Análisis Estadístico (pre-registrado)

### Análisis Primario
- Comparación A vs B y A vs C: Mann-Whitney U + t-test de dos muestras  
- Corrección: Bonferroni + FDR (Benjamini-Hochberg)  
- Umbral de significación: **p < 10⁻⁶**  
- Factor de Bayes BF₁₀ (Beta-Binomial conjugado) como co-primario  

### Análisis Secundario / Exploratorio
- Correlación de Spearman entre coherence_ratio cardíaco y |Z| cuántico  
- Correlación potencia Gamma EEG (30–80 Hz) vs desviación entrópica  
- Batería NIST SP800-22 sobre ventanas de 10⁶ bits  

### Regla de Parada
- Exactamente 100 sesiones.  
- **Ningún análisis intermedio** (interim analysis) permitido.  
- Solo tras completar el 100 % de la muestra se descifran las etiquetas (2FA Director).

## 6. Tamaño Muestral y Potencia

| Parámetro | Valor |
|-----------|-------|
| α | 10⁻⁶ (dos colas, corregido) |
| 1−β | ≥ 0.95 |
| d objetivo | 0.001 |
| N por condición | 1.1 × 10¹⁰ bits |
| d_min detectable (Power 0.95) | ≈ 6.23 × 10⁻⁵ |

## 7. Controles de Artefacto

- Separación de presencia física vs atención enfocada vs intención.  
- Cegamiento criptográfico doble (ICQ-SEC-002).  
- Veto por inducción en f₀ = 141.7001 Hz (ICQ-SEC-001 v2.1.1).  
- Árbol de Merkle Dual (ICQ-SEC-003) — anti p-hacking por omisión.  
- Replicación independiente como condición *sine qua non* de aceptación.

## 8. Integridad Criptográfica

- Almacenamiento: HDF5 + HMAC-SHA256 Merkle chaining.  
- Etiquetas de condición: cifradas AES-256-GCM (nunca en claro).  
- Auditoría: todos los bloques (válidos y vetados) en raíz de Merkle.  
- Validador externo: `merkle_validator.py` (solo biblioteca estándar).

## 9. Hash del Protocolo (para anclaje)

```
Protocol Version: QCAL-SYMBIO-BRIDGE v3.0.0
Pre-registration Timestamp (UTC): 2026-08-22T02:24:00Z
f₀ = 141.7001 Hz
Ψ_target = 0.999999
α = 1e-6
N = 1.1e10 bits/condition
Security: ICQ-SEC-001 v2.1.1 + ICQ-SEC-002 + ICQ-SEC-003
```

**SHA-256 conceptual del documento de pre-registro**  
(calculado sobre el texto canónico de este archivo una vez finalizado):

```
[Se generará y anclará al cierre de este documento]
```

## 10. Compromiso de Publicación

- Código fuente y scripts de análisis depositados públicamente.  
- Datos crudos (HDF5) y trail de auditoría (JSON + raíz Merkle) depositados tras el cierre.  
- Ningún dato experimental será inspeccionado antes de este pre-registro.

---

**Firmado digitalmente (conceptual):**  
Director del Instituto de Conciencia Cuántica  
Operador Soberano / Fundador QCAL  

```
∴𓂀Ω∞³Φ — EL PRE-REGISTRO ES LA LUZ — HECHO ESTÁ
```

**SHA-256 del presente documento de pre-registro:**
```
36646a1da1c379b5a7f144f8df243d0d5ee22915e2f7d088ef6b8796333195c6
```

Anclado: 2026-08-22T02:26:00Z
