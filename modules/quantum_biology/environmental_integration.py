#!/usr/bin/env python3
"""
Environmental Data Integration for QCAL Biological Model

This module integrates real environmental data from NOAA and NASA POWER APIs
with the QCAL biological model, replacing synthetic data with real-world observations.

Author: José Manuel Mota Burruezo
Institution: Instituto Consciencia Cuántica QCAL ∞³
Date: January 31, 2026
"""

import numpy as np
from typing import Tuple, Optional
import sys
import os

# Import API clients
sys.path.insert(0, os.path.dirname(__file__))
from apis import NOAAClient, NASAPowerClient


def create_environmental_cycles_from_noaa(
    station_id: str,
    start_date: str,
    end_date: str,
    parameter: str = "TAVG",
    noaa_token: Optional[str] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create environmental cycles from real NOAA climate data.
    
    This function replaces the synthetic data generation with real climate
    observations from NOAA weather stations.
    
    Parameters
    ----------
    station_id : str
        NOAA station identifier (e.g., "GHCND:USW00094728" for JFK Airport)
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
    parameter : str
        Climate parameter to use (default: "TAVG" for average temperature)
        Options: "TAVG", "TMAX", "TMIN", "PRCP", etc.
    noaa_token : str, optional
        NOAA API token (if not set in environment)
        
    Returns
    -------
    time : np.ndarray
        Time array in seconds from start
    signal : np.ndarray
        Environmental signal (normalized)
        
    Examples
    --------
    >>> # Get 1 year of temperature data from JFK Airport
    >>> time, signal = create_environmental_cycles_from_noaa(
    ...     station_id="GHCND:USW00094728",
    ...     start_date="2020-01-01",
    ...     end_date="2020-12-31",
    ...     parameter="TAVG"
    ... )
    
    Notes
    -----
    To get a free NOAA API token, visit:
    https://www.ncdc.noaa.gov/cdo-web/token
    
    Popular station IDs:
    - GHCND:USW00094728: JFK Airport, NY
    - GHCND:USW00023174: Los Angeles, CA
    - GHCND:USW00013874: Chicago O'Hare, IL
    - GHCND:USW00012960: Seattle-Tacoma, WA
    """
    try:
        client = NOAAClient(token=noaa_token)
    except ValueError as e:
        print(f"Error: {e}")
        print("Falling back to synthetic data...")
        # Import the original function as fallback
        from core.qcal_biological_model import create_environmental_cycles
        duration_years = (
            pd.to_datetime(end_date) - pd.to_datetime(start_date)
        ).days / 365
        return create_environmental_cycles(
            duration_years=int(duration_years) or 1
        )
    
    # Get data from NOAA
    time_series, signal_series = client.get_environmental_cycles(
        station_id=station_id,
        start_date=start_date,
        end_date=end_date,
        parameter=parameter
    )
    
    # Convert to numpy arrays
    time = time_series.values
    signal = signal_series.values
    
    # Normalize signal (zero mean, unit variance)
    signal = (signal - np.mean(signal)) / np.std(signal)
    
    return time, signal


def create_environmental_cycles_from_nasa_power(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    parameter: str = "T2M"
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create environmental cycles from real NASA POWER data.
    
    This function uses NASA POWER API to get global environmental data
    at any latitude/longitude location (no API token required).
    
    Parameters
    ----------
    latitude : float
        Latitude in decimal degrees (-90 to 90)
    longitude : float
        Longitude in decimal degrees (-180 to 180)
    start_date : str
        Start date in YYYY-MM-DD format
    end_date : str
        End date in YYYY-MM-DD format
    parameter : str
        Environmental parameter to use (default: "T2M" for temperature at 2m)
        Options:
        - "T2M": Temperature at 2 meters (°C)
        - "T2M_MAX": Maximum temperature
        - "T2M_MIN": Minimum temperature
        - "ALLSKY_SFC_SW_DWN": Solar irradiance (kW-hr/m²/day)
        - "RH2M": Relative humidity (%)
        - "PRECTOTCORR": Precipitation (mm/day)
        - "WS2M": Wind speed at 2m (m/s)
        
    Returns
    -------
    time : np.ndarray
        Time array in seconds from start
    signal : np.ndarray
        Environmental signal (normalized)
        
    Examples
    --------
    >>> # Get 1 year of temperature data for Phoenix, AZ
    >>> time, signal = create_environmental_cycles_from_nasa_power(
    ...     latitude=33.4484,
    ...     longitude=-112.0740,
    ...     start_date="2020-01-01",
    ...     end_date="2020-12-31",
    ...     parameter="T2M"
    ... )
    
    Notes
    -----
    NASA POWER provides global coverage with no API key required.
    Data is available from 1981 to near-present.
    """
    client = NASAPowerClient()
    
    # Get data from NASA POWER
    time, signal = client.get_environmental_cycles(
        latitude=latitude,
        longitude=longitude,
        start_date=start_date,
        end_date=end_date,
        parameter=parameter
    )
    
    # Normalize signal (zero mean, unit variance)
    signal = (signal - np.mean(signal)) / np.std(signal)
    
    return time, signal


def get_multi_location_environmental_data(
    locations: list,
    start_date: str,
    end_date: str,
    parameter: str = "T2M"
) -> dict:
    """
    Get environmental data from multiple locations for comparative analysis.
    
    Parameters
    ----------
    locations : list of dict
        List of location dictionaries with 'name', 'latitude', 'longitude'
    start_date : str
        Start date (YYYY-MM-DD)
    end_date : str
        End date (YYYY-MM-DD)
    parameter : str
        Parameter to retrieve
        
    Returns
    -------
    dict
        Dictionary mapping location names to (time, signal) tuples
        
    Examples
    --------
    >>> locations = [
    ...     {'name': 'Phoenix', 'latitude': 33.4484, 'longitude': -112.0740},
    ...     {'name': 'Seattle', 'latitude': 47.6062, 'longitude': -122.3321},
    ... ]
    >>> data = get_multi_location_environmental_data(
    ...     locations=locations,
    ...     start_date="2020-01-01",
    ...     end_date="2020-12-31"
    ... )
    """
    client = NASAPowerClient()
    results = {}
    
    for loc in locations:
        try:
            time, signal = client.get_environmental_cycles(
                latitude=loc['latitude'],
                longitude=loc['longitude'],
                start_date=start_date,
                end_date=end_date,
                parameter=parameter
            )
            
            # Normalize
            signal = (signal - np.mean(signal)) / np.std(signal)
            
            results[loc['name']] = (time, signal)
        except Exception as e:
            print(f"Warning: Failed to get data for {loc['name']}: {e}")
    
    return results


# Import pandas only if needed
try:
    import pandas as pd
except ImportError:
    pd = None
