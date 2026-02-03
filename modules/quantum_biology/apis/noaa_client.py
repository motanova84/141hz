#!/usr/bin/env python3
"""
NOAA Climate Data Online (CDO) API Client

Provides access to NOAA climate and weather data for QCAL biological model validation.

API Documentation: https://www.ncdc.noaa.gov/cdo-web/webservices/v2

Author: José Manuel Mota Burruezo
Institution: Instituto Consciencia Cuántica QCAL ∞³
Date: January 31, 2026
"""

import requests
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time
import os


class NOAAClient:
    """
    Client for NOAA Climate Data Online (CDO) API v2.
    
    Provides access to weather and climate time series data including:
    - Temperature (TMAX, TMIN, TAVG)
    - Precipitation
    - Pressure
    - Wind speed
    - And many more parameters
    
    Usage:
        client = NOAAClient(token="your_token")
        data = client.get_daily_data(
            station_id="GHCND:USW00094728",
            start_date="2020-01-01",
            end_date="2020-12-31",
            datatypes=["TMAX", "TMIN"]
        )
    """
    
    BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize NOAA API client.
        
        Parameters
        ----------
        token : str, optional
            NOAA API token. If not provided, will try to read from
            NOAA_API_TOKEN environment variable.
            
        Notes
        -----
        To get a free API token, visit:
        https://www.ncdc.noaa.gov/cdo-web/token
        """
        self.token = token or os.getenv("NOAA_API_TOKEN")
        if not self.token:
            raise ValueError(
                "NOAA API token required. Set NOAA_API_TOKEN environment variable "
                "or pass token parameter. Get token at: "
                "https://www.ncdc.noaa.gov/cdo-web/token"
            )
        
        self.headers = {"token": self.token}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """
        Make API request with rate limiting and error handling.
        
        Parameters
        ----------
        endpoint : str
            API endpoint (e.g., "data", "stations")
        params : dict
            Query parameters
            
        Returns
        -------
        dict
            JSON response
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        # NOAA API has a limit of 5 requests per second
        time.sleep(0.2)  # Conservative rate limiting
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"NOAA API request failed: {e}")
    
    def get_daily_data(
        self,
        station_id: str,
        start_date: str,
        end_date: str,
        datatypes: List[str] = None,
        units: str = "metric"
    ) -> pd.DataFrame:
        """
        Get daily climate data for a specific station.
        
        Parameters
        ----------
        station_id : str
            Station identifier (e.g., "GHCND:USW00094728" for JFK Airport)
        start_date : str
            Start date in YYYY-MM-DD format
        end_date : str
            End date in YYYY-MM-DD format
        datatypes : list of str, optional
            List of data types to retrieve (e.g., ["TMAX", "TMIN", "PRCP"])
            If None, retrieves all available data types
        units : str
            Units system: "metric" or "standard"
            
        Returns
        -------
        pd.DataFrame
            DataFrame with date index and requested parameters as columns
            
        Examples
        --------
        >>> client = NOAAClient(token="your_token")
        >>> data = client.get_daily_data(
        ...     station_id="GHCND:USW00094728",
        ...     start_date="2020-01-01",
        ...     end_date="2020-12-31",
        ...     datatypes=["TMAX", "TMIN"]
        ... )
        """
        if datatypes is None:
            datatypes = ["TMAX", "TMIN", "PRCP"]
        
        params = {
            "datasetid": "GHCND",  # Global Historical Climatology Network Daily
            "stationid": station_id,
            "startdate": start_date,
            "enddate": end_date,
            "datatypeid": datatypes,
            "units": units,
            "limit": 1000  # Maximum per request
        }
        
        all_results = []
        offset = 1
        
        # Handle pagination
        while True:
            params["offset"] = offset
            response = self._make_request("data", params)
            
            if "results" not in response or not response["results"]:
                break
            
            all_results.extend(response["results"])
            
            # Check if there are more results
            metadata = response.get("metadata", {})
            result_set = metadata.get("resultset", {})
            count = result_set.get("count", 0)
            
            if offset + 1000 > count:
                break
            
            offset += 1000
        
        # Convert to DataFrame
        if not all_results:
            return pd.DataFrame()
        
        df = pd.DataFrame(all_results)
        df["date"] = pd.to_datetime(df["date"])
        
        # Pivot to wide format
        df_pivot = df.pivot_table(
            index="date",
            columns="datatype",
            values="value",
            aggfunc="first"
        )
        
        return df_pivot
    
    def find_stations(
        self,
        location_id: Optional[str] = None,
        dataset_id: str = "GHCND",
        limit: int = 10
    ) -> pd.DataFrame:
        """
        Find weather stations by location.
        
        Parameters
        ----------
        location_id : str, optional
            Location identifier (e.g., "FIPS:US", "CITY:US390029", "ZIP:90210")
        dataset_id : str
            Dataset ID (default: "GHCND")
        limit : int
            Maximum number of stations to return
            
        Returns
        -------
        pd.DataFrame
            DataFrame with station information
        """
        params = {
            "datasetid": dataset_id,
            "limit": limit
        }
        
        if location_id:
            params["locationid"] = location_id
        
        response = self._make_request("stations", params)
        
        if "results" not in response:
            return pd.DataFrame()
        
        return pd.DataFrame(response["results"])
    
    def get_environmental_cycles(
        self,
        station_id: str,
        start_date: str,
        end_date: str,
        parameter: str = "TAVG"
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Get environmental time series for QCAL biological model.
        
        Parameters
        ----------
        station_id : str
            Station identifier
        start_date : str
            Start date (YYYY-MM-DD)
        end_date : str
            End date (YYYY-MM-DD)
        parameter : str
            Parameter to retrieve (default: "TAVG" for average temperature)
            
        Returns
        -------
        time : pd.Series
            Time series in seconds from start
        signal : pd.Series
            Environmental signal (temperature or other parameter)
        """
        # Get data
        data = self.get_daily_data(
            station_id=station_id,
            start_date=start_date,
            end_date=end_date,
            datatypes=[parameter]
        )
        
        if data.empty:
            raise ValueError(f"No data retrieved for station {station_id}")
        
        # Convert to time series
        if parameter not in data.columns:
            raise ValueError(f"Parameter {parameter} not found in data")
        
        signal = data[parameter]
        
        # Convert dates to seconds from start
        time_delta = (signal.index - signal.index[0]).total_seconds()
        time = pd.Series(time_delta.values, index=signal.index)
        
        return time, signal
