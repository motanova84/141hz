# GWOSC Real Data Integration Guide

## Overview

The `gw_analysis.py` script now supports direct integration with GWOSC (Gravitational Wave Open Science Center) to analyze real FITS/HDF5 gravitational wave data from LIGO, Virgo, and KAGRA detectors.

## Features

### Real Data Access
- Direct download of public GWOSC FITS/HDF5 data files
- Support for all events in GWTC-1, GWTC-2, GWTC-3, and O1/O2/O3 catalogs
- Automatic fallback to simulation when network unavailable or event not found

### Command-Line Interface
- New `--gwosc-event` parameter for single event analysis
- Alias `--center` for `--center-freq` parameter (both accepted)
- Automatic detection of real vs. simulated data mode

## Usage Examples

### Analyze Specific GWOSC Event
```bash
# GW200129_215028 with 141.7 Hz filter
python gw_analysis.py --gwosc-event=GW200129_215028 --center=141.7001 --band=0.0032 --export-certificate

# GW150914 (first detection)
python gw_analysis.py --gwosc-event=GW150914 --center=141.7001 --band=0.0032

# GW170817 (neutron star merger)
python gw_analysis.py --gwosc-event=GW170817 --detector=L1 --center=141.7001 --band=0.0032
```

### Multi-Event Run Analysis
```bash
# Analyze full O3 run
python gw_analysis.py --run=O3 --center=141.7001 --band=0.0032

# O4 run with certificate generation
python gw_analysis.py --run=O4 --export-certificate
```

### Force Simulated Mode
```bash
# Use simulation even if GWOSC is available
python gw_analysis.py --gwosc-event=GW150914 --simulated
```

## Parameters

### Required
None - all parameters have sensible defaults

### Optional
- `--gwosc-event EVENT`: Specific GWOSC event name (e.g., GW200129_215028, GW150914)
- `--run RUN`: Observing run to analyze (O3, O4, O5) - default: O4
- `--center FREQ` or `--center-freq FREQ`: Center frequency in Hz - default: 141.7001
- `--band BW`: Filter bandwidth in Hz - default: 0.0032
- `--detector DET`: Detector to use (H1, L1, V1) - default: H1
- `--min-events N`: Minimum events for subdominant search - default: 20
- `--export-certificate`: Generate analysis certificate with cryptographic hash
- `--simulated`: Force simulated data mode
- `--output FILE`: Custom output filename

## Data Flow

### With Network Access
1. Script attempts to connect to GWOSC API
2. Event GPS time is retrieved from catalog
3. FITS/HDF5 strain data is downloaded (32 seconds centered on event)
4. Data is processed with spectral filter
5. Results and certificate are generated

### Without Network Access
1. Script attempts GWOSC connection
2. Connection fails (network error or event not found)
3. Graceful fallback to simulation mode
4. Simulated strain data is generated (reproducible via event name seed)
5. Results and certificate are generated with simulation flag

## Output

### Terminal Output
```
======================================================================
GW Analysis - Spectral Filter for 141.7 Hz QCAL Signature
======================================================================
Mode: Single GWOSC Event Analysis
Event: GW200129_215028
Center frequency: 141.7001 Hz
Bandwidth: 0.0032 Hz
Detector: H1
Data source: Real GWOSC FITS/HDF5
======================================================================

🔬 Multi-Event Subdominant Search
   Target: 1 events (minimum: 20)
   Detector: H1
   Center frequency: 141.7001 ± 0.0016 Hz

🔍 Analyzing GW200129_215028 (H1)...
   📡 Fetching real GWOSC data for GW200129_215028 from H1...
   ✓ Found GPS time: 1264316116.4
   📥 Downloading strain data from GWOSC...
   ✓ Successfully loaded 131072 samples
   ✓ Data format: FITS/HDF5 from GWOSC
   ✓ SNR: 3.45 | Peak: 141.7002 Hz | Δf: 0.0001 Hz

📊 Statistics:
   Detections: 1/1 (100.0%)
   Mean SNR: 3.45 ± 0.00
   Mean peak: 141.7002 ± 0.0000 Hz
   Consistency: 1.000

🎓 Generating Analysis Certificate...
   ✓ Certificate ID: a3f4b5c6d7e8f9a0
   ✓ Hash: a3f4b5c6d7e8f9a0b1c2d3e4f5a6b7c8...

✅ Certificate generated with ID: a3f4b5c6d7e8f9a0

💾 Results exported to: results/gw_analysis_o4/gw_analysis_O4_20260215_141530.json
```

### JSON Output
Results are saved to `results/gw_analysis_<run>/` directory with structure:
```json
{
  "config": {
    "center_freq": 141.7001,
    "bandwidth": 0.0032,
    "run": "O4",
    "timestamp": "2026-02-15T14:15:30.123456Z"
  },
  "events": {
    "GW200129_215028": {
      "event": "GW200129_215028",
      "detector": "H1",
      "snr": 3.45,
      "peak_freq": 141.7002,
      "peak_power": 1.23e-42,
      "delta_f": 0.0001,
      "significance": 3450.0,
      "detected": true
    }
  },
  "statistics": {
    "total_events": 1,
    "detections": 1,
    "detection_rate": 1.0,
    "mean_snr": 3.45,
    "std_snr": 0.0,
    "mean_peak_freq": 141.7002,
    "std_peak_freq": 0.0,
    "consistency": 1.0
  },
  "certificate": {
    "certificate_id": "a3f4b5c6d7e8f9a0",
    "hash": "a3f4b5c6d7e8f9a0b1c2d3e4f5a6b7c8...",
    "data": { ... },
    "signature": "..."
  }
}
```

## Dependencies

### Required
```bash
pip install numpy scipy gwpy gwosc
```

### Optional (for enhanced features)
```bash
pip install matplotlib  # For visualization
pip install h5py       # For local HDF5 file reading
```

## GWOSC Event Catalogs

### Available Events
- **O1 (2015-2016)**: GW150914, GW151012, GW151226
- **O2 (2016-2017)**: GW170104, GW170608, GW170729, GW170809, GW170814, GW170817, GW170818, GW170823
- **O3 (2019-2020)**: 50+ events in GWTC-2 and GWTC-3
- **O4 (2023-2025)**: Events being published progressively

### Event Naming
- Format: `GW<YYMMDD>` or `GW<YYMMDD>_<HHMMSS>`
- Example: `GW200129_215028` = 2020-01-29 at 21:50:28 UTC

## Technical Details

### Data Processing
1. **Download**: 32 seconds of strain data (±16s around event)
2. **Sample Rate**: 4096 Hz (can be configured)
3. **Filter**: 8th-order Butterworth bandpass
4. **SNR**: Computed as RMS(filtered) / RMS(residual)
5. **Peak Detection**: Within ±10× bandwidth of center frequency

### Validation
- Wang et al. AT2020afhd validation included in certificates
- Reference: Science Advances (2024), DOI: 10.1126/sciadv.ady9068
- 27.838 octaves below f₀ = 141.7001 Hz

## Troubleshooting

### Network Errors
```
❌ Error loading GW200129_215028: HTTPSConnectionPool(...): Max retries exceeded
```
**Solution**: Network access blocked or GWOSC servers down. Script will automatically use simulation.

### Event Not Found
```
⚠️ Event GW250114 not found in GWOSC catalog
ℹ️ Available catalogs: GWTC-1, GWTC-2, GWTC-3, O1, O2, O3
```
**Solution**: Event not yet published to GWOSC. Use simulation or wait for official release.

### Missing Dependencies
```
❌ Error: gwpy is required. Install with: pip install gwpy gwosc
```
**Solution**: Install required packages: `pip install gwpy gwosc`

## Future Enhancements

- [ ] Local FITS/HDF5 file support
- [ ] Batch processing of multiple GWOSC events
- [ ] Real-time O4/O5 event monitoring
- [ ] Advanced visualization of spectral features
- [ ] Integration with PyCBC for template matching

## References

1. GWOSC: https://gwosc.org
2. GWPy Documentation: https://gwpy.github.io
3. LIGO Open Science Center: https://www.ligo.org/science/outreach.php
4. Wang et al. (2024): Science Advances, DOI: 10.1126/sciadv.ady9068

## Support

For issues or questions:
- GitHub Issues: https://github.com/motanova84/141hz/issues
- GWOSC Help: https://gwosc.org/about/
- GWPy Help: https://gwpy.github.io/docs/stable/
