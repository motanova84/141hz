# Environmental Data APIs for QCAL Biological Model

This module provides integration with real-world environmental data sources to validate the QCAL biological hypothesis using actual climate observations instead of synthetic data.

## Overview

The QCAL biological model tests the hypothesis that biological cycles synchronize with environmental spectral fields. To validate this with real data, we've integrated two major environmental data APIs:

1. **NOAA Climate Data Online (CDO) API** - Weather station data
2. **NASA POWER API** - Global solar and meteorological data

## Quick Start

### Using NASA POWER (No API Key Required)

NASA POWER provides global coverage and requires no authentication:

```python
from modules.quantum_biology.environmental_integration import (
    create_environmental_cycles_from_nasa_power
)

# Get 1 year of temperature data for Phoenix, AZ
time, signal = create_environmental_cycles_from_nasa_power(
    latitude=33.4484,
    longitude=-112.0740,
    start_date="2020-01-01",
    end_date="2020-12-31",
    parameter="T2M"  # Temperature at 2 meters
)

# Use with QCAL biological model
from modules.quantum_biology.core.qcal_biological_model import SpectralField

field = SpectralField.from_environmental_data(time, signal, n_components=10)
```

### Using NOAA CDO (Requires Free API Token)

NOAA provides high-quality weather station data:

```python
from modules.quantum_biology.environmental_integration import (
    create_environmental_cycles_from_noaa
)

# Get 1 year of temperature data from JFK Airport
time, signal = create_environmental_cycles_from_noaa(
    station_id="GHCND:USW00094728",
    start_date="2020-01-01",
    end_date="2020-12-31",
    parameter="TAVG"  # Average temperature
)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install requests pandas numpy
```

### 2. Get NOAA API Token (Optional)

If you want to use NOAA data:

1. Visit: https://www.ncdc.noaa.gov/cdo-web/token
2. Request a free API token (sent via email)
3. Set environment variable:

```bash
export NOAA_API_TOKEN="your_token_here"
```

Or pass it directly:

```python
from modules.quantum_biology.apis import NOAAClient

client = NOAAClient(token="your_token_here")
```

### 3. NASA POWER (No Setup Required)

NASA POWER API is completely open - no authentication needed!

## API Clients Documentation

### NASA POWER Client

```python
from modules.quantum_biology.apis import NASAPowerClient

client = NASAPowerClient()

# Get daily data for any location
data = client.get_daily_data(
    latitude=33.4484,
    longitude=-112.0740,
    start_date="2020-01-01",
    end_date="2020-12-31",
    parameters=[
        "T2M",                  # Temperature at 2m (°C)
        "ALLSKY_SFC_SW_DWN",    # Solar irradiance (kW-hr/m²/day)
        "RH2M",                 # Relative humidity (%)
        "PRECTOTCORR",          # Precipitation (mm/day)
        "WS2M"                  # Wind speed at 2m (m/s)
    ]
)
```

**Available Parameters:**
- `T2M`, `T2M_MAX`, `T2M_MIN` - Temperature at 2 meters
- `ALLSKY_SFC_SW_DWN` - All-sky surface shortwave downward irradiance
- `RH2M` - Relative humidity at 2 meters
- `PRECTOTCORR` - Precipitation corrected
- `WS2M` - Wind speed at 2 meters
- `PS` - Surface pressure
- And many more! See: https://power.larc.nasa.gov/parameters/

### NOAA CDO Client

```python
from modules.quantum_biology.apis import NOAAClient

client = NOAAClient(token="your_token")

# Find stations near a location
stations = client.find_stations(
    location_id="ZIP:85001",  # Phoenix, AZ zip code
    limit=10
)

# Get daily data from a specific station
data = client.get_daily_data(
    station_id="GHCND:USW00094728",  # JFK Airport
    start_date="2020-01-01",
    end_date="2020-12-31",
    datatypes=["TMAX", "TMIN", "PRCP", "SNOW"]
)
```

**Popular Station IDs:**
- `GHCND:USW00094728` - JFK Airport, NY
- `GHCND:USW00023174` - Los Angeles, CA
- `GHCND:USW00013874` - Chicago O'Hare, IL
- `GHCND:USW00012960` - Seattle-Tacoma, WA
- `GHCND:USW00023183` - Phoenix, AZ

**Available Data Types:**
- `TAVG`, `TMAX`, `TMIN` - Average, maximum, minimum temperature
- `PRCP` - Precipitation
- `SNOW` - Snowfall
- `AWND` - Average wind speed
- `WSF2` - Fastest 2-minute wind speed
- Many more! See: https://www.ncdc.noaa.gov/cdo-web/datasets

## Integration with QCAL Biological Model

### Replace Synthetic Data with Real Data

**Before (synthetic data):**
```python
from modules.quantum_biology.core.qcal_biological_model import (
    create_environmental_cycles
)

time, signal = create_environmental_cycles(duration_years=20)
```

**After (real NASA POWER data):**
```python
from modules.quantum_biology.environmental_integration import (
    create_environmental_cycles_from_nasa_power
)

time, signal = create_environmental_cycles_from_nasa_power(
    latitude=33.4484,
    longitude=-112.0740,
    start_date="2000-01-01",
    end_date="2020-12-31",  # 20 years of real data
    parameter="T2M"
)
```

### Multi-Location Comparative Analysis

Compare biological synchrony across different climates:

```python
from modules.quantum_biology.environmental_integration import (
    get_multi_location_environmental_data
)

locations = [
    {'name': 'Phoenix (Hot Desert)', 'latitude': 33.4484, 'longitude': -112.0740},
    {'name': 'Seattle (Temperate Oceanic)', 'latitude': 47.6062, 'longitude': -122.3321},
    {'name': 'Miami (Tropical)', 'latitude': 25.7617, 'longitude': -80.1918},
    {'name': 'Anchorage (Subarctic)', 'latitude': 61.2181, 'longitude': -149.9003},
]

data = get_multi_location_environmental_data(
    locations=locations,
    start_date="2020-01-01",
    end_date="2020-12-31",
    parameter="T2M"
)

# Analyze each location
for name, (time, signal) in data.items():
    print(f"\n{name}:")
    print(f"  Data points: {len(signal)}")
    print(f"  Temperature range: {signal.min():.1f} to {signal.max():.1f}°C")
```

## Example: Complete QCAL Validation with Real Data

```python
import numpy as np
from modules.quantum_biology.environmental_integration import (
    create_environmental_cycles_from_nasa_power
)
from modules.quantum_biology.core.qcal_biological_model import (
    SpectralField, BiologicalFilter, PhaseAccumulator
)

# 1. Get real environmental data
time, signal = create_environmental_cycles_from_nasa_power(
    latitude=33.4484,
    longitude=-112.0740,
    start_date="2010-01-01",
    end_date="2020-12-31",  # 10 years
    parameter="T2M"
)

# 2. Create spectral field from real data
field = SpectralField.from_environmental_data(
    time, signal, n_components=20
)

# 3. Apply biological filter (tuned to 141.7 Hz)
bio_filter = BiologicalFilter()
filtered_power = bio_filter.apply(field)

# 4. Accumulate phase over time
accumulator = PhaseAccumulator(alpha=0.1, threshold=100.0)

# Simulate biological response
dt_days = np.diff(time) / (24 * 3600)  # Convert to days
phases = []

for power, dt in zip(filtered_power[:-1], dt_days):
    phase = accumulator.accumulate(power, dt)
    phases.append(phase)
    
    if accumulator.check_activation():
        print(f"Activation detected at day {len(phases)}")
        break

print(f"\nPhase accumulation over {len(phases)} days")
print(f"Final phase: {phases[-1]:.2f}")
```

## Testing

Run the test suite:

```bash
# Run all tests (some require NOAA_API_TOKEN)
pytest tests/test_api_clients.py -v

# Run only NASA POWER tests (no auth required)
pytest tests/test_api_clients.py::TestNASAPowerClient -v

# Run only NOAA tests (requires token)
export NOAA_API_TOKEN="your_token"
pytest tests/test_api_clients.py::TestNOAAClient -v
```

## Rate Limiting and Best Practices

### NASA POWER
- No strict rate limits, but be respectful
- Internal rate limiting: 0.5s between requests
- Global coverage from 1981 to near-present
- Daily and hourly data available

### NOAA CDO
- Rate limit: 5 requests per second
- Maximum 1000 results per request (pagination handled automatically)
- Internal rate limiting: 0.2s between requests
- Historical data availability varies by station

## Error Handling

Both clients have robust error handling:

```python
from modules.quantum_biology.apis import NASAPowerClient

client = NASAPowerClient()

try:
    data = client.get_daily_data(
        latitude=33.4484,
        longitude=-112.0740,
        start_date="2020-01-01",
        end_date="2020-12-31",
        parameters=["T2M"]
    )
except RuntimeError as e:
    print(f"API request failed: {e}")
    # Fallback to synthetic data
    from modules.quantum_biology.core.qcal_biological_model import (
        create_environmental_cycles
    )
    time, signal = create_environmental_cycles(duration_years=1)
```

## References

- **NOAA CDO API Documentation**: https://www.ncdc.noaa.gov/cdo-web/webservices/v2
- **NASA POWER API Documentation**: https://power.larc.nasa.gov/docs/services/api/
- **NASA POWER Parameters**: https://power.larc.nasa.gov/parameters/
- **QCAL Biological Hypothesis**: See `HIPOTESIS_QCAL_BIOLOGIA_NUMEROS.md`

## Support

For issues or questions:
1. Check the API documentation links above
2. Review test cases in `tests/test_api_clients.py`
3. Open an issue in the repository

## License

This code follows the same license as the main repository (MIT/Apache-2.0).
