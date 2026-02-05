#!/usr/bin/env python3
"""
NASA POWER API Client

Provides access to NASA POWER (Prediction Of Worldwide Energy Resources) API
for solar radiation and meteorological data.

API Documentation: https://power.larc.nasa.gov/docs/services/api/

Author: José Manuel Mota Burruezo
Institution: Instituto Consciencia Cuántica QCAL ∞³
Date: January 31, 2026
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time


class NASAPowerClient:
    """
    Client for NASA POWER API.
    
    Provides access to solar radiation and meteorological parameters including:
    - Solar irradiance (ALLSKY_SFC_SW_DWN)
    - Temperature (T2M, T2M_MAX, T2M_MIN)
    - Relative humidity (RH2M)
    - Precipitation (PRECTOTCORR)
    - Wind speed (WS2M)
    - Pressure (PS)
    
    No API key required!
    
    Usage:
        client = NASAPowerClient()
        data = client.get_daily_data(
            latitude=33.4484,
            longitude=-112.0740,
            start_date="2020-01-01",
            end_date="2020-12-31",
            parameters=["ALLSKY_SFC_SW_DWN", "T2M"]
        )
    """
    
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    def __init__(self):
        """Initialize NASA POWER API client (no authentication required)."""
        self.session = requests.Session()
    
    def _make_request(self, params: Dict) -> Dict:
        """
        Make API request with rate limiting and error handling.
        
        Parameters
        ----------
        params : dict
            Query parameters
            
        Returns
        -------
        dict
            JSON response
        """
        # Be respectful with rate limiting
        time.sleep(0.5)
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=60  # NASA POWER can be slow
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"NASA POWER API request failed: {e}")
    
    def get_daily_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        parameters: List[str] = None,
        community: str = "RE"
    ) -> pd.DataFrame:
        """
        Get daily meteorological data for a specific location.
        
        Parameters
        ----------
        latitude : float
            Latitude in decimal degrees (-90 to 90)
        longitude : float
            Longitude in decimal degrees (-180 to 180)
        start_date : str
            Start date in YYYYMMDD format
        end_date : str
            End date in YYYYMMDD format
        parameters : list of str, optional
            List of parameters to retrieve (e.g., ["ALLSKY_SFC_SW_DWN", "T2M"])
            If None, retrieves common environmental parameters
        community : str
            Data community: "RE" (Renewable Energy), "AG" (Agroclimatology),
            or "SB" (Sustainable Buildings)
            
        Returns
        -------
        pd.DataFrame
            DataFrame with date index and requested parameters as columns
            
        Examples
        --------
        >>> client = NASAPowerClient()
        >>> data = client.get_daily_data(
        ...     latitude=33.4484,
        ...     longitude=-112.0740,
        ...     start_date="20200101",
        ...     end_date="20201231",
        ...     parameters=["ALLSKY_SFC_SW_DWN", "T2M"]
        ... )
        """
        if parameters is None:
            # Default: solar radiation and temperature
            parameters = ["ALLSKY_SFC_SW_DWN", "T2M", "T2M_MAX", "T2M_MIN"]
        
        params = {
            "parameters": ",".join(parameters),
            "community": community,
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date.replace("-", ""),
            "end": end_date.replace("-", ""),
            "format": "JSON"
        }
        
        response = self._make_request(params)
        
        # Extract data from response
        if "properties" not in response or "parameter" not in response["properties"]:
            raise ValueError("Invalid response from NASA POWER API")
        
        parameter_data = response["properties"]["parameter"]
        
        # Convert to DataFrame
        data_dict = {}
        for param in parameters:
            if param in parameter_data:
                data_dict[param] = parameter_data[param]
        
        df = pd.DataFrame(data_dict)
        
        # Convert index to datetime
        df.index = pd.to_datetime(df.index, format="%Y%m%d")
        
        # Replace fill values (-999) with NaN
        df = df.replace(-999, np.nan)
        
        return df
    
    def get_hourly_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        parameters: List[str] = None,
        community: str = "RE"
    ) -> pd.DataFrame:
        """
        Get hourly meteorological data for a specific location.
        
        Parameters
        ----------
        latitude : float
            Latitude in decimal degrees (-90 to 90)
        longitude : float
            Longitude in decimal degrees (-180 to 180)
        start_date : str
            Start date in YYYYMMDD format
        end_date : str
            End date in YYYYMMDD format
        parameters : list of str, optional
            List of parameters to retrieve
        community : str
            Data community (default: "RE")
            
        Returns
        -------
        pd.DataFrame
            DataFrame with datetime index and requested parameters as columns
        """
        if parameters is None:
            parameters = ["ALLSKY_SFC_SW_DWN", "T2M"]
        
        # Use hourly endpoint
        url = "https://power.larc.nasa.gov/api/temporal/hourly/point"
        
        params = {
            "parameters": ",".join(parameters),
            "community": community,
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date.replace("-", ""),
            "end": end_date.replace("-", ""),
            "format": "JSON"
        }
        
        time.sleep(0.5)  # Rate limiting
        
        try:
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"NASA POWER API request failed: {e}")
        
        if "properties" not in data or "parameter" not in data["properties"]:
            raise ValueError("Invalid response from NASA POWER API")
        
        parameter_data = data["properties"]["parameter"]
        
        # Convert to DataFrame
        data_dict = {}
        for param in parameters:
            if param in parameter_data:
                data_dict[param] = parameter_data[param]
        
        df = pd.DataFrame(data_dict)
        
        # Convert index to datetime (hourly format: YYYYMMDDHH)
        df.index = pd.to_datetime(df.index, format="%Y%m%d%H")
        
        # Replace fill values with NaN
        df = df.replace(-999, np.nan)
        
        return df
    
    def get_environmental_cycles(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        parameter: str = "T2M"
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get environmental time series for QCAL biological model.
        
        Parameters
        ----------
        latitude : float
            Latitude in decimal degrees
        longitude : float
            Longitude in decimal degrees
        start_date : str
            Start date (YYYY-MM-DD or YYYYMMDD)
        end_date : str
            End date (YYYY-MM-DD or YYYYMMDD)
        parameter : str
            Parameter to retrieve (default: "T2M" for temperature at 2m)
            
        Returns
        -------
        time : np.ndarray
            Time array in seconds from start
        signal : np.ndarray
            Environmental signal (temperature or other parameter)
        """
        # Get data
        data = self.get_daily_data(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            parameters=[parameter]
        )
        
        if data.empty:
            raise ValueError(
                f"No data retrieved for location ({latitude}, {longitude})"
            )
        
        # Convert to numpy arrays
        if parameter not in data.columns:
            raise ValueError(f"Parameter {parameter} not found in data")
        
        signal = data[parameter].values
        
        # Convert dates to seconds from start
        time_delta = (data.index - data.index[0]).total_seconds()
        time = time_delta.values
        
        return time, signal
