#!/usr/bin/env python3
"""
Utility Functions for GW 141.7001 Hz Analysis
==============================================

This module provides common utility functions for data handling,
error recovery, and logging.

Author: José Manuel Mota Burruezo (JMMB)
"""

import time
import logging
from functools import wraps
from typing import Callable, Any, Optional, Type, Tuple
from pathlib import Path

# Try relative import first, fall back to direct import for compatibility
try:
    from . import exceptions as exc
except ImportError:
    import exceptions as exc


# Configure logging
def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Configure logging for the analysis pipeline.
    
    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        log_file: Optional file path to write logs
        format_string: Optional custom format string
        
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logger = logging.getLogger('gw_141hz')
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(format_string)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    logger: Optional[logging.Logger] = None
) -> Callable:
    """
    Decorator that implements retry logic with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        backoff_factor: Multiplier for delay after each attempt
        max_delay: Maximum delay in seconds between retries
        exceptions: Tuple of exception types to catch and retry
        logger: Optional logger for retry messages
        
    Returns:
        Decorated function with retry logic
        
    Example:
        @retry_with_backoff(max_attempts=3, initial_delay=2.0)
        def download_data(event_name):
            # Function that might fail
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        if logger:
                            logger.error(
                                f"Function {func.__name__} failed after {max_attempts} attempts: {str(e)}"
                            )
                        raise
                    
                    if logger:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                    
                    time.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
            
            # Should not reach here, but just in case
            if last_exception:
                raise last_exception
                
        return wrapper
    return decorator


def safe_download(
    download_func: Callable,
    *args,
    max_attempts: int = 3,
    logger: Optional[logging.Logger] = None,
    **kwargs
) -> Any:
    """
    Safely download data with retry logic and error handling.
    
    Args:
        download_func: Function to call for downloading
        *args: Positional arguments to pass to download_func
        max_attempts: Maximum number of retry attempts
        logger: Optional logger for messages
        **kwargs: Keyword arguments to pass to download_func
        
    Returns:
        Result from download_func
        
    Raises:
        DataDownloadError: If download fails after all retry attempts
    """
    @retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=2.0,
        backoff_factor=2.0,
        exceptions=(Exception,),
        logger=logger
    )
    def _download():
        try:
            return download_func(*args, **kwargs)
        except Exception as e:
            # Wrap generic exceptions in DataDownloadError
            if isinstance(e, (exc.DataDownloadError, exc.NetworkError, exc.GW141HzException)):
                raise
            raise exc.DataDownloadError(
                message=f"Download failed: {str(e)}"
            )
    
    return _download()


def validate_file_exists(file_path: Path, raise_error: bool = True) -> bool:
    """
    Validate that a file exists.
    
    Args:
        file_path: Path to the file
        raise_error: Whether to raise an error if file doesn't exist
        
    Returns:
        True if file exists, False otherwise
        
    Raises:
        FileNotFoundError: If file doesn't exist and raise_error is True
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        if raise_error:
            raise FileNotFoundError(f"Required file not found: {file_path}")
        return False
    
    return True


def ensure_directory(directory: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
        
    Returns:
        Path object for the directory
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def safe_json_dump(data: dict, output_path: Path, logger: Optional[logging.Logger] = None) -> bool:
    """
    Safely write JSON data to a file with error handling.
    
    Args:
        data: Dictionary to write as JSON
        output_path: Path to output file
        logger: Optional logger for messages
        
    Returns:
        True if successful, False otherwise
    """
    import json
    
    try:
        output_path = Path(output_path)
        ensure_directory(output_path.parent)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        if logger:
            logger.info(f"Successfully wrote JSON to {output_path}")
        
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"Failed to write JSON to {output_path}: {str(e)}")
        return False


def safe_json_load(input_path: Path, logger: Optional[logging.Logger] = None) -> Optional[dict]:
    """
    Safely load JSON data from a file with error handling.
    
    Args:
        input_path: Path to input file
        logger: Optional logger for messages
        
    Returns:
        Loaded dictionary, or None if loading fails
    """
    import json
    
    try:
        input_path = Path(input_path)
        
        if not input_path.exists():
            if logger:
                logger.warning(f"JSON file not found: {input_path}")
            return None
        
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        if logger:
            logger.info(f"Successfully loaded JSON from {input_path}")
        
        return data
        
    except json.JSONDecodeError as e:
        if logger:
            logger.error(f"Invalid JSON in {input_path}: {str(e)}")
        return None
    except Exception as e:
        if logger:
            logger.error(f"Failed to load JSON from {input_path}: {str(e)}")
        return None


def format_frequency(freq: float, precision: int = 4) -> str:
    """
    Format frequency value with specified precision.
    
    Args:
        freq: Frequency value in Hz
        precision: Number of decimal places
        
    Returns:
        Formatted frequency string
    """
    return f"{freq:.{precision}f} Hz"


def format_snr(snr: float, precision: int = 2) -> str:
    """
    Format SNR value with specified precision.
    
    Args:
        snr: Signal-to-noise ratio value
        precision: Number of decimal places
        
    Returns:
        Formatted SNR string
    """
    return f"{snr:.{precision}f}"
