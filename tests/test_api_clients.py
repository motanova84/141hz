#!/usr/bin/env python3
"""
Tests for NOAA and NASA POWER API clients.

These tests verify the API client functionality. Some tests require
API credentials and network access, so they can be skipped if not available.

Author: José Manuel Mota Burruezo
Date: January 31, 2026
"""

import pytest
import numpy as np
import pandas as pd
import os
import sys

# Add module path
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), '..', '..', 'modules', 'quantum_biology')
)

from modules.quantum_biology.apis.nasa_power_client import NASAPowerClient
from modules.quantum_biology.apis.noaa_client import NOAAClient
from modules.quantum_biology.environmental_integration import (
    create_environmental_cycles_from_nasa_power,
    create_environmental_cycles_from_noaa,
    get_multi_location_environmental_data
)


# NASA POWER tests (no auth required)
class TestNASAPowerClient:
    """Test NASA POWER API client."""
    
    def test_client_initialization(self):
        """Test that client can be initialized without errors."""
        client = NASAPowerClient()
        assert client is not None
        assert client.session is not None
    
    def test_get_daily_data(self):
        """Test fetching daily data from NASA POWER API."""
        client = NASAPowerClient()
        
        # Small date range for testing
        data = client.get_daily_data(
            latitude=33.4484,  # Phoenix, AZ
            longitude=-112.0740,
            start_date="2023-01-01",
            end_date="2023-01-07",  # Just 7 days
            parameters=["T2M"]
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "T2M" in data.columns
        assert len(data) == 7
    
    def test_get_environmental_cycles(self):
        """Test environmental cycles extraction."""
        client = NASAPowerClient()
        
        time, signal = client.get_environmental_cycles(
            latitude=33.4484,
            longitude=-112.0740,
            start_date="2023-01-01",
            end_date="2023-01-31",
            parameter="T2M"
        )
        
        assert isinstance(time, np.ndarray)
        assert isinstance(signal, np.ndarray)
        assert len(time) == len(signal)
        assert len(time) > 0
        # Check that time is in seconds
        assert time[0] == 0  # First timestep should be 0


class TestNASAPowerIntegration:
    """Test NASA POWER integration functions."""
    
    def test_create_environmental_cycles_from_nasa_power(self):
        """Test creating environmental cycles from NASA POWER."""
        time, signal = create_environmental_cycles_from_nasa_power(
            latitude=33.4484,
            longitude=-112.0740,
            start_date="2023-01-01",
            end_date="2023-01-31",
            parameter="T2M"
        )
        
        assert isinstance(time, np.ndarray)
        assert isinstance(signal, np.ndarray)
        assert len(time) == len(signal)
        
        # Check normalization (mean should be close to 0, std close to 1)
        assert abs(np.mean(signal)) < 0.1
        assert abs(np.std(signal) - 1.0) < 0.1
    
    def test_multi_location_data(self):
        """Test fetching data from multiple locations."""
        locations = [
            {'name': 'Phoenix', 'latitude': 33.4484, 'longitude': -112.0740},
            {'name': 'Seattle', 'latitude': 47.6062, 'longitude': -122.3321},
        ]
        
        data = get_multi_location_environmental_data(
            locations=locations,
            start_date="2023-01-01",
            end_date="2023-01-07",
            parameter="T2M"
        )
        
        assert isinstance(data, dict)
        assert len(data) == 2
        assert 'Phoenix' in data
        assert 'Seattle' in data
        
        # Check data structure
        time, signal = data['Phoenix']
        assert len(time) == len(signal)


# NOAA tests (require API token)
class TestNOAAClient:
    """Test NOAA API client."""
    
    def test_client_initialization_without_token(self):
        """Test that client raises error without token."""
        # Clear environment variable if set
        old_token = os.environ.get("NOAA_API_TOKEN")
        if old_token:
            del os.environ["NOAA_API_TOKEN"]
        
        with pytest.raises(ValueError, match="NOAA API token required"):
            NOAAClient()
        
        # Restore token if it existed
        if old_token:
            os.environ["NOAA_API_TOKEN"] = old_token
    
    @pytest.mark.skipif(
        not os.getenv("NOAA_API_TOKEN"),
        reason="NOAA_API_TOKEN not set"
    )
    def test_client_initialization_with_token(self):
        """Test that client can be initialized with token."""
        client = NOAAClient()
        assert client is not None
        assert client.token is not None
        assert client.session is not None
    
    @pytest.mark.skipif(
        not os.getenv("NOAA_API_TOKEN"),
        reason="NOAA_API_TOKEN not set"
    )
    def test_find_stations(self):
        """Test finding weather stations."""
        client = NOAAClient()
        
        # Find stations in a specific location
        stations = client.find_stations(
            location_id="FIPS:36",  # New York state
            limit=5
        )
        
        assert isinstance(stations, pd.DataFrame)
        assert not stations.empty
        assert "id" in stations.columns
    
    @pytest.mark.skipif(
        not os.getenv("NOAA_API_TOKEN"),
        reason="NOAA_API_TOKEN not set"
    )
    def test_get_daily_data(self):
        """Test fetching daily data from NOAA API."""
        client = NOAAClient()
        
        # JFK Airport weather station
        data = client.get_daily_data(
            station_id="GHCND:USW00094728",
            start_date="2023-01-01",
            end_date="2023-01-07",
            datatypes=["TMAX", "TMIN"]
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        # Note: Some data might be missing for certain dates
    
    @pytest.mark.skipif(
        not os.getenv("NOAA_API_TOKEN"),
        reason="NOAA_API_TOKEN not set"
    )
    def test_get_environmental_cycles(self):
        """Test environmental cycles extraction from NOAA."""
        client = NOAAClient()
        
        time, signal = client.get_environmental_cycles(
            station_id="GHCND:USW00094728",
            start_date="2023-01-01",
            end_date="2023-01-31",
            parameter="TMAX"
        )
        
        assert isinstance(time, pd.Series)
        assert isinstance(signal, pd.Series)
        assert len(time) == len(signal)
        assert time.iloc[0] == 0  # First timestep should be 0


class TestNOAAIntegration:
    """Test NOAA integration functions."""
    
    @pytest.mark.skipif(
        not os.getenv("NOAA_API_TOKEN"),
        reason="NOAA_API_TOKEN not set"
    )
    def test_create_environmental_cycles_from_noaa(self):
        """Test creating environmental cycles from NOAA."""
        time, signal = create_environmental_cycles_from_noaa(
            station_id="GHCND:USW00094728",
            start_date="2023-01-01",
            end_date="2023-01-31",
            parameter="TMAX"
        )
        
        assert isinstance(time, np.ndarray)
        assert isinstance(signal, np.ndarray)
        assert len(time) == len(signal)
        
        # Check normalization
        assert abs(np.mean(signal)) < 0.2  # Allow some tolerance
        assert abs(np.std(signal) - 1.0) < 0.2


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
