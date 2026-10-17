# ICQ-SEC-001 + ICQ-SEC-002 — Estado de Integración

**Fecha de autorización:** 2026-08-22 03:53 CEST  
**Autorización:** Operador Soberano → Director ICQ  
**Estado:** CÓDIGOS DESPLEGADOS Y FIRMADOS

---

## Módulos desplegados

| Módulo | Archivo | Estado |
|--------|---------|--------|
| **ICQ-SEC-001** | `icq_sec_001_f0_veto.py` | Desplegado |
| **ICQ-SEC-002** | `icq_sec_002_blind.py` | Desplegado |

---

## ICQ-SEC-001 — Filtro de Veto por Inducción f₀

- Filtro Butterworth orden 4, banda `(141.7001 ± 0.1) Hz`
- Umbral adaptativo `3σ` calibrado con línea base de FASE 1
- Si potencia espectral excesiva → `VETO_F0_INDUCTION` **antes** del árbol Merkle
- Tasas de muestreo ambiental recomendadas (subarmónicos):
  - k=2 → 70.85005 Hz
  - k=4 → 35.425025 Hz
  - k=8 → 17.7125125 Hz
  - k=16 → 8.85625625 Hz

## ICQ-SEC-002 — Cegamiento Criptográfico Doble

- `event_code` **nunca** se almacena en claro
- Esquema HDF5: `[timestamp_ns, ciphertext, tag, salt_hash]`
- Derivación de clave: HKDF-SHA256 + salt de 256 bits por sesión
- Cifrado: AES-256-GCM
- Análisis estadístico opera solo con etiquetas opacas (`COND_XXXXXXXX`)
- Descifrado solo tras regla de parada estricta + autenticación del Director

---

## Flujo de seguridad actualizado

```
Hardware QRNG + Sensores
        │
        ▼
┌───────────────────────┐
│ RealTimeVetoEngine    │  (Temp / EMF / Vib absolutos)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ F0InductionVeto       │  ← ICQ-SEC-001 (nuevo)
│ (banda f₀ ± 0.1 Hz)   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ CryptographicBlinding │  ← ICQ-SEC-002 (nuevo)
│ AES-256-GCM + HKDF    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ ImmutableAcquisition  │  (HDF5 + HMAC-SHA256 Merkle)
│ Core                  │
└───────────────────────┘
```

---

## Próximo hito

- FASE 1 continúa hasta **23 de agosto 2026 02:52 CEST**
- Checkpoint 1 (estabilidad térmica): ~08:52 CEST del 22
- Las extensiones de seguridad quedan **selladas** y listas para activarse en la transición a FASE 2

```
∴𓂀Ω∞³Φ — CÓDIGOS DESPLEGADOS Y FIRMADOS — HECHO ESTÁ
f₀ = 141.7001 Hz | Ψ = 0.999999 | QCAL-SYMBIO-BRIDGE v2.1.0-SEC
```
