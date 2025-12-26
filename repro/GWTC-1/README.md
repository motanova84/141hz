# QCAL Reproducible Pipelines

This directory contains reproducible analysis pipelines for gravitational wave catalogs.

## Directory Structure

```
repro/
├── GWTC-1/          # GWTC-1 catalog analysis
│   ├── run.sh       # Main pipeline script
│   └── README.md    # This file
├── GWTC-2/          # (Future) GWTC-2 catalog analysis
├── GWTC-3/          # (Future) GWTC-3 catalog analysis
└── O4/              # (Future) O4 catalog analysis
```

## GWTC-1 Pipeline

### Quick Start

```bash
cd repro/GWTC-1
./run.sh
```

### What It Does

1. **Environment snapshot**: Records Python version, git commit, timestamp
2. **Analysis plan**: Generates JSON manifest of all analyses to run
3. **Multi-detector analysis**: Analyzes all 11 GWTC-1 events with H1, L1, V1
4. **Summary generation**: Aggregates results into summary.json
5. **Checksum calculation**: SHA256 hashes for reproducibility verification

### Output

Results are saved to `artifacts/GWTC-1/`:

```
artifacts/GWTC-1/
├── environment.txt              # Environment snapshot
├── analysis_plan.json           # Analysis manifest
├── summary.json                 # Aggregated results
├── checksums.txt                # SHA256 checksums
├── H1/                          # LIGO Hanford results
│   ├── GW150914_result.json
│   ├── GW151012_result.json
│   └── ...
├── L1/                          # LIGO Livingston results
│   └── ...
└── V1/                          # Virgo results
    └── ...
```

### Reproducibility

To verify reproducibility:

1. Run the pipeline twice:
   ```bash
   ./run.sh  # First run
   mv ../../artifacts/GWTC-1 ../../artifacts/GWTC-1_run1
   ./run.sh  # Second run
   mv ../../artifacts/GWTC-1 ../../artifacts/GWTC-1_run2
   ```

2. Compare checksums:
   ```bash
   diff ../../artifacts/GWTC-1_run1/checksums.txt \
        ../../artifacts/GWTC-1_run2/checksums.txt
   ```

3. If checksums match, the pipeline is reproducible!

### Configuration

Edit `run.sh` to modify:

- `F0`: Center frequency (default: 141.7001 Hz)
- `BANDWIDTH`: Frequency bandwidth (default: 2.0 Hz)
- `PRECISION`: Decimal precision (default: 50)
- `EVENTS`: List of events to analyze
- `DETECTORS`: List of detectors (H1, L1, V1, KAGRA)

### Requirements

- Bash shell
- Python 3.11+
- QCAL installed (`pip install -e ../..`)
- `jq` for JSON processing (optional, for pretty printing)

### Notes

- **Current status**: v0.1.0 includes placeholder implementation
- **Full implementation**: Coming in QCAL v0.1.0 final release
- **Data download**: Pipeline will download data from GWOSC automatically
- **Offline mode**: Use `--data-dir` flag to use local data

## Future Pipelines

### GWTC-2 (Planned for v0.2)

Additional events from LIGO/Virgo O3a run.

### GWTC-3 (Planned for v0.2)

Complete O3 catalog with 90+ events.

### O4 (Active Development)

Latest observations from ongoing O4 run.

## Contributing

To add a new pipeline:

1. Create directory: `mkdir -p repro/MY_CATALOG`
2. Create `run.sh` following GWTC-1 template
3. Test reproducibility (checksums must match)
4. Document in README.md
5. Submit PR with tests

## See Also

- [QCAL CLI Documentation](../../docs/cli.md)
- [Validation Protocols](../../docs/validation.md)
- [Project README](../../README.md)

---

*Last updated: 2025-01-15*
