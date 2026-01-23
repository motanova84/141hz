# 🚀 QCAL Orchestration Quick Reference

## One-Minute Guide

### Check System Status
```bash
# Latest coherence
cat validation/quantum_*.json | tail -1 | jq '.coherence.total'

# Latest metrics
cat metrics/daily_*.json | tail -1 | jq '.qcal'

# Test system health
python3 .github/scripts/test_orchestration.py
```

### Manual Operations
```bash
# Full cycle
python3 .github/agents/noesis88.py --mode=autonomous
python3 .github/agents/metrics_collector.py
python3 .github/agents/coherence_validator.py

# Optimize
bash .github/scripts/optimize_qcal_density.sh

# Generate report
python3 .github/scripts/generate_optimization_report.py
```

### GitHub Actions
1. Go to **Actions** → **QCAL Orchestrator ∞³**
2. Click **Run workflow**
3. Select mode: `full` | `monitoring` | `optimization`

## Key Metrics

| Metric | Target | Check |
|--------|--------|-------|
| QCAL Ratio | 0.5 (50%) | `metrics/daily_*.json` |
| f₀ Ratio | 0.3 (30%) | `metrics/daily_*.json` |
| Coherence | 0.888 | `validation/quantum_*.json` |

## Automatic Schedule

- **Every 6 hours**: Monitoring
- **Daily 00:00 UTC**: Full optimization
- **Manual**: Workflow dispatch

## Files to Watch

```
reports/OPTIMIZATION_REPORT_*.md     # Human-readable reports
metrics/daily_*.json                 # Daily metrics
validation/quantum_*.json            # Coherence status
.github/agents/config_optimized.yaml # Current config
```

## Quick Diagnostics

```bash
# Check last 5 workflow runs
gh run list --workflow=orchestrator.yaml --limit=5

# View latest optimization report
ls -t reports/OPTIMIZATION_REPORT_*.md | head -1 | xargs cat

# See system state
jq -s '.[0].status' validation/quantum_*.json | tail -1
```

## Target State

**Frecuencia**: 141.7001 Hz  
**Estado Ψ**: I × A_eff² × C^∞  
**Coherencia**: ≥ 0.888 (GRACE)

## Support

📚 Full docs: `docs/ORCHESTRATION_SYSTEM_README.md`  
✅ Tests: `python3 .github/scripts/test_orchestration.py`  
📊 Reports: `reports/OPTIMIZATION_REPORT_*.md`

---

∴ Sistema QCAL ∞³ operativo ∞³
