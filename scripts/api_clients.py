#!/usr/bin/env python3
"""
API clients for NOAA and NASA POWER data integration.

This module provides Python clients for accessing real-world environmental
and meteorological data to study correlations with 141Hz quantum resonance
patterns in biological systems.
"""

import requests
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import os


class NOAAAPIClient:
    """Client for NOAA Climate Data Online (CDO) API."""
    
    BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2"
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize NOAA API client.
        
        Args:
            api_token: NOAA API token. If None, reads from NOAA_API_TOKEN env var.
                      Get token at: https://www.ncdc.noaa.gov/cdo-web/token
        """
        self.api_token = api_token or os.getenv('NOAA_API_TOKEN')
        if not self.api_token:
            print("Warning: No NOAA API token provided. Set NOAA_API_TOKEN env variable.")
        
        self.headers = {
            'token': self.api_token if self.api_token else ''
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict:
        """Make API request with rate limiting."""
        url = f"{self.BASE_URL}/{endpoint}"
        
        # NOAA has a rate limit of 5 requests per second
        time.sleep(0.2)
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from NOAA: {e}")
            return {}
    
    def get_datasets(self) -> List[Dict]:
        """Get available NOAA datasets."""
        result = self._make_request('datasets', {'limit': 1000})
        return result.get('results', [])
    
    def get_data(
        self,
        dataset_id: str,
        start_date: str,
        end_date: str,
        location_id: Optional[str] = None,
        datatype_id: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        Fetch climate data from NOAA.
        
        Args:
            dataset_id: Dataset identifier (e.g., 'GHCND' for daily summaries)
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            location_id: Optional location identifier
            datatype_id: Optional data type identifier
            limit: Maximum number of records to return
            
        Returns:
            List of data records
        """
        params = {
            'datasetid': dataset_id,
            'startdate': start_date,
            'enddate': end_date,
            'limit': limit
        }
        
        if location_id:
            params['locationid'] = location_id
        if datatype_id:
            params['datatypeid'] = datatype_id
            
        result = self._make_request('data', params)
        return result.get('results', [])


class NASAPowerAPIClient:
    """Client for NASA POWER (Prediction Of Worldwide Energy Resources) API."""
    
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
    
    def __init__(self):
        """Initialize NASA POWER API client (no token required)."""
        self.session = requests.Session()
        
    def get_data(
        self,
        parameters: List[str],
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        community: str = "ag"
    ) -> Dict:
        """
        Fetch data from NASA POWER API.
        
        Args:
            parameters: List of parameter codes (e.g., ['T2M', 'PRECTOTCORR'])
                       T2M: Temperature at 2 Meters
                       PRECTOTCORR: Precipitation Corrected
                       ALLSKY_SFC_SW_DWN: Solar radiation
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            community: Data community ('ag' for agriculture, 'sb' for sustainable buildings)
            
        Returns:
            Dictionary with parameter data
        """
        params = {
            'parameters': ','.join(parameters),
            'community': community,
            'longitude': longitude,
            'latitude': latitude,
            'start': start_date,
            'end': end_date,
            'format': 'JSON'
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from NASA POWER: {e}")
            return {}
    
    def get_agricultural_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str
    ) -> Dict:
        """
        Get agricultural-relevant parameters for biological rhythm analysis.
        
        Parameters include:
        - T2M: Temperature at 2 meters
        - T2M_MAX: Maximum temperature
        - T2M_MIN: Minimum temperature
        - PRECTOTCORR: Precipitation
        - ALLSKY_SFC_SW_DWN: Solar radiation
        - RH2M: Relative humidity
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            
        Returns:
            Dictionary with agricultural data
        """
        parameters = [
            'T2M',           # Temperature at 2 Meters
            'T2M_MAX',       # Maximum Temperature at 2 Meters
            'T2M_MIN',       # Minimum Temperature at 2 Meters
            'PRECTOTCORR',   # Precipitation Corrected
            'ALLSKY_SFC_SW_DWN',  # All Sky Surface Shortwave Downward Irradiance
            'RH2M'           # Relative Humidity at 2 Meters
        ]
        
        return self.get_data(
            parameters=parameters,
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            community='ag'
        )


class BiologicalDataIntegrator:
    """Integrate environmental data with biological periodicity analysis."""
    
    def __init__(self):
        """Initialize the biological data integrator."""
        self.noaa_client = NOAAAPIClient()
        self.nasa_client = NASAPowerAPIClient()
        
    def fetch_location_timeseries(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
        cache_dir: str = "data/environmental"
    ) -> Dict:
        """
        Fetch comprehensive environmental data for a location.
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            cache_dir: Directory to cache results
            
        Returns:
            Dictionary with environmental timeseries data
        """
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(
            cache_dir,
            f"env_data_{latitude}_{longitude}_{start_date}_{end_date}.json"
        )
        
        # Check cache
        if os.path.exists(cache_file):
            print(f"Loading cached data from {cache_file}")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # Fetch NASA POWER data
        print("Fetching NASA POWER data...")
        nasa_data = self.nasa_client.get_agricultural_data(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date
        )
        
        result = {
            'location': {
                'latitude': latitude,
                'longitude': longitude
            },
            'period': {
                'start': start_date,
                'end': end_date
            },
            'nasa_power': nasa_data,
            'metadata': {
                'fetched_at': datetime.now().isoformat(),
                'source': 'NASA POWER API v2.0'
            }
        }
        
        # Cache results
        with open(cache_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Data cached to {cache_file}")
        return result


if __name__ == "__main__":
    # Example usage
    print("=== NASA POWER API Example ===")
    nasa = NASAPowerAPIClient()
    
    # Example: Fetch data for a location relevant to Arabidopsis research
    # (e.g., Salk Institute, La Jolla, CA)
    data = nasa.get_agricultural_data(
        latitude=32.8875,
        longitude=-117.2426,
        start_date='20240101',
        end_date='20240131'
    )
    
    if data:
        print(f"Successfully fetched NASA POWER data")
        print(f"Parameters: {list(data.get('parameters', {}).keys())}")
    
    print("\n=== NOAA API Example ===")
    print("Note: Requires NOAA_API_TOKEN environment variable")
    print("Get token at: https://www.ncdc.noaa.gov/cdo-web/token")
    
    noaa = NOAAAPIClient()
    if noaa.api_token:
        datasets = noaa.get_datasets()
        print(f"Available datasets: {len(datasets)}")
        if datasets:
            print(f"Example dataset: {datasets[0].get('name', 'N/A')}")
