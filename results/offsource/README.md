# Off-Source Null Distribution Results

This directory contains results from off-source analysis used to establish null distributions for the 141.7001 Hz signal detection.

## Purpose

Off-source analysis provides a null hypothesis distribution by analyzing the same frequency band (140.7-142.7 Hz) at times far from the gravitational wave coalescence event. This allows us to:

1. Estimate background noise characteristics
2. Determine false alarm probability
3. Assess statistical significance of on-source detections
4. Validate that the signal is localized to the coalescence time

## Methodology

Per `PREREGISTRATION.md` and `analysis_plan.json`:

- **Number of windows**: 10,000 per event
- **Window duration**: 0.5 s (same as on-source)
- **Exclusion zone**: ±10 s around coalescence
- **Distribution**: Uniform sampling of available data
- **Detectors**: H1, L1, V1 (when available)

## File Structure

```
offsource_null.json          - Aggregated off-source statistics
{event_name}_offsource.json  - Per-event off-source results
{event_name}_histogram.png   - Visual comparison on/off source
```

## Expected Results Format

```json
{
  "event": "GW150914",
  "detector": "H1",
  "on_source_snr": 8.2,
  "off_source_statistics": {
    "mean": 0.02,
    "std": 1.01,
    "median": 0.01,
    "n_windows": 10000,
    "n_above_threshold": 5,
    "p_value": 0.0005
  },
  "interpretation": "On-source SNR exceeds 99.95% of off-source distribution"
}
```

## Validation Criteria

From pre-registration:
- **p-value < 0.01**: On-source SNR must be in top 1% of off-source distribution
- **Consistency**: All detectors should show elevated SNR on-source vs off-source
- **Robustness**: Results should hold across different choices of off-source windows

## Status

🚧 **Pending**: Off-source analysis to be executed after unblinding

See `bayes/hierarchical_model.py` for Bayesian framework that incorporates off-source null distribution into final inference.

---

**Last Updated**: 2025-10-30  
**Part of**: Pre-registration v1.0  
**Reference**: [PREREGISTRATION.md](../../PREREGISTRATION.md)
