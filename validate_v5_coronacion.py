#!/usr/bin/env python3
"""
VALIDATE V5 CORONACION - Core Validation Script for Production

This is the main validation script for the production pipeline that validates
the core scientific calculations with configurable precision.

REFACTORED: Now uses modular validation classes with improved error handling.

Usage:
    python3 validate_v5_coronacion.py --precision 30
    python3 validate_v5_coronacion.py --precision 50 --output results/validation.json
"""

import sys
import argparse
from pathlib import Path

# Add src to path for compatibility with direct script execution
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Import from src modules - works both as script and as package
try:
    from src.validators import ValidationOrchestrator
    from src.exceptions import ValidationError, PrecisionError, GW141HzException
    from src.utils import safe_json_dump, setup_logging
except ImportError:
    # Fallback for direct execution
    from validators import ValidationOrchestrator
    from exceptions import ValidationError, PrecisionError, GW141HzException
    from utils import safe_json_dump, setup_logging


def run_complete_validation(precision=30):
    """
    Run complete validation suite using modular validators.
    
    Args:
        precision: Number of decimal places for calculation precision
        
    Returns:
        dict: Complete validation results
        
    Raises:
        PrecisionError: If precision is invalid
        ValidationError: If validation fails critically
    """
    try:
        orchestrator = ValidationOrchestrator(precision=precision)
        return orchestrator.run_all()
    except (PrecisionError, ValidationError) as e:
        logger = setup_logging()
        logger.error(f"Validation failed: {e}")
        raise
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Unexpected error during validation: {e}")
        raise GW141HzException(f"Validation failed with unexpected error: {str(e)}")


def main():
    """
    Main entry point with robust error handling.
    """
    parser = argparse.ArgumentParser(
        description="Validate V5 Coronacion - Core validation for production (Refactored)"
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=30,
        help="Calculation precision in decimal places (default: 30)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (default: results/validation_v5.json)"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Optional log file path"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(
        log_file=Path(args.log_file) if args.log_file else None
    )
    
    try:
        # Validate precision
        if args.precision < 10:
            raise PrecisionError(
                required_precision=args.precision,
                message="Precision must be at least 10 decimal places"
            )
        
        # Run validation
        logger.info(f"Starting validation with precision={args.precision}")
        results = run_complete_validation(args.precision)
        
        # Save results
        output_path = args.output if args.output else "results/validation_v5.json"
        output_file = Path(output_path)
        
        if safe_json_dump(results, output_file, logger):
            logger.info(f"📊 Results saved to: {output_file}")
        else:
            logger.error("Failed to save results")
            sys.exit(2)
        
        # Exit with appropriate code
        exit_code = 0 if results['overall_status'] == 'PASS' else 1
        logger.info(f"Validation complete with status: {results['overall_status']}")
        sys.exit(exit_code)
        
    except PrecisionError as e:
        logger.error(f"Precision error: {e}")
        sys.exit(3)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)
    except GW141HzException as e:
        logger.error(f"Application error: {e}")
        sys.exit(2)
    except KeyboardInterrupt:
        logger.warning("Validation interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(2)


if __name__ == '__main__':
    main()
