# 🔄 Inventario de Workflows Automatizado

*Este documento es generado automáticamente cada semana.*

## Workflows Activos

### QCAL Analysis

**Archivo:** `analysis.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### Auto Label PRs and Issues

**Archivo:** `auto-label.yml`

- Trigger: pull_request

### Auto-Update Documentation

**Archivo:** `auto-update-docs.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: schedule (`0 2 * * 0`)
- Trigger: manual (workflow_dispatch)

### QC-LLM CI/CD

**Archivo:** `ci.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### Coherence Tensor Validation

**Archivo:** `coherence-tensor.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: schedule (`0 0 * * 0`)
- Trigger: manual (workflow_dispatch)

### Create Required Labels

**Archivo:** `create-labels.yml`

- Trigger: push
- Trigger: manual (workflow_dispatch)

### Deploy GitHub Pages

**Archivo:** `deploy-pages.yml`

- Trigger: push
- Trigger: manual (workflow_dispatch)

### GW Validation - 141.7 Hz

**Archivo:** `gw-validation.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### QCAL Hilo A — Lean 4 Verification

**Archivo:** `lean_verify.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### QCAL Production Cycle

**Archivo:** `production-qcal.yml`

- Trigger: schedule (`0 */4 * * *       # Run every 4 hours`)
- Trigger: manual (workflow_dispatch)

### QCAL Biological Validation

**Archivo:** `qcal-biological-validation.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### QCAL Ω Audit

**Archivo:** `qcal-omega-audit.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### "QCAL-Sync: Update Global Context"

**Archivo:** `qcal-sync.yml`

- Trigger: push
- Trigger: manual (workflow_dispatch)

### Sovereignty Check

**Archivo:** `sovereignty-check.yml`

- Trigger: push
- Trigger: pull_request
- Trigger: manual (workflow_dispatch)

### Stationary Phase Monitor — QCAL ∞³

**Archivo:** `stationary-phase-monitor.yml`

- Trigger: pull_request
- Trigger: schedule (`0 6 * * *`)
- Trigger: manual (workflow_dispatch)

---
*Generado automáticamente por el bot de documentación - 2026-09-01 02:04:37 UTC*
