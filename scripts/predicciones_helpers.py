"""
Helper functions for QCAL prediction validation scripts.
"""
import numpy as np
import json


def convert_to_json(obj):
    """
    Convert numpy/mpmath types to JSON-serializable types.
    
    Args:
        obj: Object to convert (can be dict, list, numpy array, etc.)
    
    Returns:
        JSON-serializable version of the object
    """
    if isinstance(obj, dict):
        return {k: convert_to_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json(item) for item in obj]
    elif isinstance(obj, (np.bool_, np.integer)):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):  # numpy scalar
        return obj.item()
    else:
        return obj


def save_json_results(results, filepath):
    """
    Save results to JSON file, handling numpy/mpmath type conversion.
    
    Args:
        results: Results dictionary to save
        filepath: Path to save JSON file
        
    Raises:
        IOError: If file cannot be written
        ValueError: If results cannot be serialized
    """
    try:
        results_json = convert_to_json(results)
    except Exception as e:
        raise ValueError(f"Failed to convert results to JSON-serializable format: {e}")
    
    try:
        with open(filepath, 'w') as f:
            json.dump(results_json, f, indent=2)
    except IOError as e:
        raise IOError(f"Failed to write results to {filepath}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error saving JSON: {e}")
