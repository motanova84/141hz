#!/usr/bin/env python3
"""
Tests for Utility Functions Module
"""

import pytest
import sys
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils import (
    setup_logging,
    retry_with_backoff,
    safe_json_dump,
    safe_json_load,
    ensure_directory,
    format_frequency,
    format_snr
)


class TestSetupLogging:
    """Test logging setup."""
    
    def test_basic_setup(self):
        """Test basic logging setup."""
        logger = setup_logging()
        assert logger is not None
        assert logger.name == 'gw_141hz'
        assert len(logger.handlers) > 0
    
    def test_with_log_file(self, tmp_path):
        """Test setup with log file."""
        log_file = tmp_path / "test.log"
        logger = setup_logging(log_file=log_file)
        
        logger.info("Test message")
        assert log_file.exists()
        assert "Test message" in log_file.read_text()


class TestRetryWithBackoff:
    """Test retry decorator."""
    
    def test_success_first_try(self):
        """Test function succeeds on first try."""
        mock_func = Mock(return_value="success")
        
        @retry_with_backoff(max_attempts=3)
        def test_func():
            return mock_func()
        
        result = test_func()
        assert result == "success"
        assert mock_func.call_count == 1
    
    def test_success_after_retries(self):
        """Test function succeeds after retries."""
        call_count = 0
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = test_func()
        assert result == "success"
        assert call_count == 3
    
    def test_all_attempts_fail(self):
        """Test all retry attempts fail."""
        @retry_with_backoff(max_attempts=3, initial_delay=0.01)
        def test_func():
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError, match="Always fails"):
            test_func()
    
    def test_exponential_backoff(self):
        """Test exponential backoff timing."""
        call_times = []
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.1, backoff_factor=2.0)
        def test_func():
            call_times.append(time.time())
            raise ValueError("Fail")
        
        try:
            test_func()
        except ValueError:
            pass
        
        assert len(call_times) == 3
        # Check that delays are increasing (with some tolerance)
        if len(call_times) >= 2:
            delay1 = call_times[1] - call_times[0]
            assert delay1 >= 0.08  # Should be ~0.1s


class TestJsonFunctions:
    """Test JSON utility functions."""
    
    def test_safe_json_dump(self, tmp_path):
        """Test safe JSON dump."""
        output_file = tmp_path / "test.json"
        data = {"key": "value", "number": 42}
        
        result = safe_json_dump(data, output_file)
        assert result is True
        assert output_file.exists()
        
        with open(output_file) as f:
            loaded = json.load(f)
        assert loaded == data
    
    def test_safe_json_load(self, tmp_path):
        """Test safe JSON load."""
        input_file = tmp_path / "test.json"
        data = {"key": "value", "number": 42}
        
        with open(input_file, 'w') as f:
            json.dump(data, f)
        
        loaded = safe_json_load(input_file)
        assert loaded == data
    
    def test_safe_json_load_nonexistent(self, tmp_path):
        """Test loading nonexistent file."""
        input_file = tmp_path / "nonexistent.json"
        loaded = safe_json_load(input_file)
        assert loaded is None
    
    def test_safe_json_load_invalid(self, tmp_path):
        """Test loading invalid JSON."""
        input_file = tmp_path / "invalid.json"
        input_file.write_text("not valid json {")
        
        loaded = safe_json_load(input_file)
        assert loaded is None


class TestDirectoryFunctions:
    """Test directory utility functions."""
    
    def test_ensure_directory(self, tmp_path):
        """Test directory creation."""
        new_dir = tmp_path / "sub" / "nested" / "dir"
        
        result = ensure_directory(new_dir)
        assert result == new_dir
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_ensure_directory_existing(self, tmp_path):
        """Test with existing directory."""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()
        
        result = ensure_directory(existing_dir)
        assert result == existing_dir
        assert existing_dir.exists()


class TestFormatFunctions:
    """Test formatting functions."""
    
    def test_format_frequency(self):
        """Test frequency formatting."""
        assert format_frequency(141.7001) == "141.7001 Hz"
        assert format_frequency(141.7001, precision=2) == "141.70 Hz"
        assert format_frequency(100.0, precision=1) == "100.0 Hz"
    
    def test_format_snr(self):
        """Test SNR formatting."""
        assert format_snr(21.38) == "21.38"
        assert format_snr(21.38456, precision=3) == "21.385"
        assert format_snr(10.0, precision=1) == "10.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
