#!/usr/bin/env python3
"""
Tests for Custom Exceptions Module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from exceptions import (
    GW141HzException,
    DataDownloadError,
    DataNotFoundError,
    ValidationError,
    AnalysisError,
    ConfigurationError,
    PrecisionError,
    NetworkError
)


class TestGW141HzException:
    """Test base exception class."""
    
    def test_basic_exception(self):
        """Test basic exception creation."""
        exc = GW141HzException("Test error")
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.details == {}
    
    def test_exception_with_details(self):
        """Test exception with details."""
        exc = GW141HzException("Test error", {"key": "value", "num": 42})
        assert "Test error" in str(exc)
        assert "key=value" in str(exc)
        assert "num=42" in str(exc)


class TestDataDownloadError:
    """Test data download error."""
    
    def test_with_event_and_detector(self):
        """Test with event name and detector."""
        exc = DataDownloadError(event_name="GW150914", detector="H1")
        assert "GW150914" in str(exc)
        assert "H1" in str(exc)
        assert exc.event_name == "GW150914"
        assert exc.detector == "H1"
    
    def test_with_custom_message(self):
        """Test with custom message."""
        exc = DataDownloadError(message="Custom download error")
        assert str(exc) == "Custom download error"


class TestDataNotFoundError:
    """Test data not found error."""
    
    def test_basic(self):
        """Test basic data not found error."""
        exc = DataNotFoundError("test_file.json")
        assert "test_file.json" in str(exc)
        assert exc.resource == "test_file.json"


class TestValidationError:
    """Test validation error."""
    
    def test_basic(self):
        """Test basic validation error."""
        exc = ValidationError("test_validation")
        assert "test_validation" in str(exc)
        assert exc.validation_name == "test_validation"
    
    def test_with_expected_actual(self):
        """Test with expected and actual values."""
        exc = ValidationError("test_check", expected=1.0, actual=0.9)
        assert "expected=1.0" in str(exc)
        assert "actual=0.9" in str(exc)
        assert exc.expected == 1.0
        assert exc.actual == 0.9


class TestAnalysisError:
    """Test analysis error."""
    
    def test_basic(self):
        """Test basic analysis error."""
        exc = AnalysisError("computation_step")
        assert "computation_step" in str(exc)
        assert exc.analysis_step == "computation_step"
    
    def test_with_cause(self):
        """Test with underlying cause."""
        cause = ValueError("Invalid value")
        exc = AnalysisError("step1", cause=cause)
        assert "step1" in str(exc)
        assert "Invalid value" in str(exc)
        assert exc.cause == cause


class TestConfigurationError:
    """Test configuration error."""
    
    def test_basic(self):
        """Test basic configuration error."""
        exc = ConfigurationError("missing_key")
        assert "missing_key" in str(exc)
        assert exc.config_key == "missing_key"


class TestPrecisionError:
    """Test precision error."""
    
    def test_basic(self):
        """Test basic precision error."""
        exc = PrecisionError(50)
        assert "50" in str(exc)
        assert exc.required_precision == 50


class TestNetworkError:
    """Test network error."""
    
    def test_basic(self):
        """Test basic network error."""
        exc = NetworkError()
        assert "Network operation failed" in str(exc)
    
    def test_with_url_and_status(self):
        """Test with URL and status code."""
        test_url = "https://example.com"
        exc = NetworkError(url=test_url, status_code=404)
        # Test that error message includes the URL information
        assert test_url in str(exc)
        assert "404" in str(exc)
        # Test that attributes are set correctly
        assert exc.url == test_url
        assert exc.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
