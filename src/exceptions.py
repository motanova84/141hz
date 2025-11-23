#!/usr/bin/env python3
"""
Custom Exceptions for GW 141.7001 Hz Analysis
==============================================

This module provides custom exception classes for better error handling
throughout the analysis pipeline.

Author: José Manuel Mota Burruezo (JMMB)
"""


class GW141HzException(Exception):
    """Base exception for all GW 141.7001 Hz analysis errors."""
    
    def __init__(self, message: str, details: dict = None):
        """
        Initialize the exception.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        """String representation of the exception."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class DataDownloadError(GW141HzException):
    """Exception raised when data download from GWOSC fails."""
    
    def __init__(self, event_name: str = None, detector: str = None, message: str = None):
        """
        Initialize data download error.
        
        Args:
            event_name: Name of the gravitational wave event
            detector: Detector name (H1, L1, V1, etc.)
            message: Custom error message
        """
        if message is None:
            message = f"Failed to download data for event '{event_name}' from detector '{detector}'"
        
        details = {}
        if event_name:
            details["event"] = event_name
        if detector:
            details["detector"] = detector
            
        super().__init__(message, details)
        self.event_name = event_name
        self.detector = detector


class DataNotFoundError(GW141HzException):
    """Exception raised when requested data is not available."""
    
    def __init__(self, resource: str, message: str = None):
        """
        Initialize data not found error.
        
        Args:
            resource: Description of the missing resource
            message: Custom error message
        """
        if message is None:
            message = f"Data not found: {resource}"
        
        super().__init__(message, {"resource": resource})
        self.resource = resource


class ValidationError(GW141HzException):
    """Exception raised when validation checks fail."""
    
    def __init__(self, validation_name: str, expected: float = None, actual: float = None, message: str = None):
        """
        Initialize validation error.
        
        Args:
            validation_name: Name of the validation that failed
            expected: Expected value (optional)
            actual: Actual value (optional)
            message: Custom error message
        """
        if message is None:
            if expected is not None and actual is not None:
                message = f"Validation failed: {validation_name} (expected={expected}, actual={actual})"
            else:
                message = f"Validation failed: {validation_name}"
        
        details = {"validation": validation_name}
        if expected is not None:
            details["expected"] = expected
        if actual is not None:
            details["actual"] = actual
            
        super().__init__(message, details)
        self.validation_name = validation_name
        self.expected = expected
        self.actual = actual


class AnalysisError(GW141HzException):
    """Exception raised when analysis computation fails."""
    
    def __init__(self, analysis_step: str, message: str = None, cause: Exception = None):
        """
        Initialize analysis error.
        
        Args:
            analysis_step: Name of the analysis step that failed
            message: Custom error message
            cause: Original exception that caused this error
        """
        if message is None:
            message = f"Analysis failed at step: {analysis_step}"
            if cause:
                message += f" - {str(cause)}"
        
        details = {"step": analysis_step}
        if cause:
            details["cause"] = str(cause)
            details["cause_type"] = type(cause).__name__
            
        super().__init__(message, details)
        self.analysis_step = analysis_step
        self.cause = cause


class ConfigurationError(GW141HzException):
    """Exception raised when configuration is invalid or missing."""
    
    def __init__(self, config_key: str, message: str = None):
        """
        Initialize configuration error.
        
        Args:
            config_key: Configuration key that is invalid or missing
            message: Custom error message
        """
        if message is None:
            message = f"Invalid or missing configuration: {config_key}"
        
        super().__init__(message, {"config_key": config_key})
        self.config_key = config_key


class PrecisionError(GW141HzException):
    """Exception raised when precision requirements cannot be met."""
    
    def __init__(self, required_precision: int, message: str = None):
        """
        Initialize precision error.
        
        Args:
            required_precision: Required precision in decimal places
            message: Custom error message
        """
        if message is None:
            message = f"Cannot achieve required precision: {required_precision} decimal places"
        
        super().__init__(message, {"required_precision": required_precision})
        self.required_precision = required_precision


class NetworkError(GW141HzException):
    """Exception raised when network operations fail."""
    
    def __init__(self, url: str = None, message: str = None, status_code: int = None):
        """
        Initialize network error.
        
        Args:
            url: URL that failed to load
            message: Custom error message
            status_code: HTTP status code if applicable
        """
        if message is None:
            message = f"Network operation failed"
            if url:
                message += f" for URL: {url}"
            if status_code:
                message += f" (status code: {status_code})"
        
        details = {}
        if url:
            details["url"] = url
        if status_code:
            details["status_code"] = status_code
            
        super().__init__(message, details)
        self.url = url
        self.status_code = status_code
