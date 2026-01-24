#!/usr/bin/env python3
"""
Demonstration of Refactored Code Improvements
==============================================

This script demonstrates the benefits of the refactoring:
1. Exception handling with context
2. Retry logic with exponential backoff
3. Modular validators
4. Structured logging

Author: José Manuel Mota Burruezo (JMMB)
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from exceptions import DataDownloadError, ValidationError, PrecisionError
from utils import setup_logging, retry_with_backoff, format_frequency, format_snr
from validators import ValidationOrchestrator


def demo_exception_handling():
    """Demonstrate improved exception handling."""
    print("\n" + "=" * 70)
    print("DEMO 1: Exception Handling with Context")
    print("=" * 70)
    
    try:
        # Simulate a download error
        raise DataDownloadError(
            event_name="GW150914",
            detector="H1",
            message="GWOSC API timeout after 30s"
        )
    except DataDownloadError as e:
        print(f"\n✓ Caught exception: {e}")
        print(f"  Event: {e.event_name}")
        print(f"  Detector: {e.detector}")
        print(f"  Details: {e.details}")
    
    try:
        # Simulate a validation error
        raise ValidationError(
            validation_name="symmetry_check",
            expected=1.0,
            actual=0.999,
            message="Symmetry deviation exceeds tolerance"
        )
    except ValidationError as e:
        print(f"\n✓ Caught exception: {e}")
        print(f"  Validation: {e.validation_name}")
        print(f"  Expected: {e.expected}")
        print(f"  Actual: {e.actual}")


def demo_retry_logic():
    """Demonstrate retry logic with exponential backoff."""
    print("\n" + "=" * 70)
    print("DEMO 2: Retry Logic with Exponential Backoff")
    print("=" * 70)
    
    logger = setup_logging()
    
    attempt_count = 0
    
    @retry_with_backoff(
        max_attempts=3,
        initial_delay=0.5,
        backoff_factor=2.0,
        logger=logger
    )
    def unreliable_function():
        nonlocal attempt_count
        attempt_count += 1
        print(f"\n  Attempt {attempt_count}...")
        
        if attempt_count < 3:
            raise ConnectionError(f"Connection failed (attempt {attempt_count})")
        
        return "Success!"
    
    print("\n✓ Function will fail twice, then succeed:")
    result = unreliable_function()
    print(f"\n✓ Final result: {result}")
    print(f"✓ Total attempts: {attempt_count}")


def demo_modular_validators():
    """Demonstrate modular validator architecture."""
    print("\n" + "=" * 70)
    print("DEMO 3: Modular Validators")
    print("=" * 70)
    
    logger = setup_logging()
    
    print("\n✓ Running validation with precision=25...")
    
    try:
        # Create orchestrator
        orchestrator = ValidationOrchestrator(precision=25)
        
        # Run all validations
        results = orchestrator.run_all()
        
        # Display results
        print(f"\n✓ Overall Status: {results['overall_status']}")
        print(f"✓ Tests Passed: {results['summary']['tests_passed']}/{results['summary']['tests_run']}")
        
        # Show individual results
        print("\n  Quantum Frequency:")
        qf = results['quantum_frequency']
        print(f"    f₀ = {format_frequency(qf['f0_hz'])}")
        print(f"    E_Ψ = {qf['E_psi_joules']:.6e} J")
        print(f"    Status: {qf['status']}")
        
        print("\n  Compactification Radius:")
        cr = results['compactification_radius']
        print(f"    R_Ψ = {cr['R_psi_calculated']:.2f} m")
        print(f"    In Range: {cr['in_expected_range']}")
        print(f"    Status: {cr['status']}")
        
        print("\n  Discrete Symmetry:")
        ds = results['discrete_symmetry']
        print(f"    Deviation: {ds['deviation_from_unity']:.2e}")
        print(f"    Status: {ds['status']}")
        
    except PrecisionError as e:
        logger.error(f"Precision error: {e}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")


def demo_utility_functions():
    """Demonstrate utility functions."""
    print("\n" + "=" * 70)
    print("DEMO 4: Utility Functions")
    print("=" * 70)
    
    # Formatting functions
    print("\n✓ Formatting Functions:")
    print(f"  Frequency: {format_frequency(141.7001, precision=4)}")
    print(f"  SNR: {format_snr(21.38, precision=2)}")
    
    # Logging
    print("\n✓ Structured Logging:")
    logger = setup_logging()
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # JSON handling (using temp path)
    from utils import safe_json_dump, safe_json_load
    
    print("\n✓ Safe JSON Handling:")
    temp_file = Path("/tmp/demo_data.json")
    test_data = {
        "f0": 141.7001,
        "status": "PASS",
        "timestamp": "2025-11-05T00:00:00Z"
    }
    
    if safe_json_dump(test_data, temp_file, logger):
        print(f"  ✓ Data saved to {temp_file}")
    
    loaded_data = safe_json_load(temp_file, logger)
    if loaded_data:
        print(f"  ✓ Data loaded: {loaded_data['f0']} Hz")
    
    # Cleanup
    temp_file.unlink(missing_ok=True)


def demo_comparison():
    """Compare old vs new approach."""
    print("\n" + "=" * 70)
    print("DEMO 5: Before vs After Comparison")
    print("=" * 70)
    
    print("\n❌ OLD APPROACH:")
    print("""
    # Monolithic function
    def validate_all(precision):
        mp.dps = precision
        # 200 lines of mixed logic...
        if error:
            print("Error!")
            sys.exit(1)
    
    # No exception handling
    results = validate_all(30)
    
    # Manual JSON writing
    with open('results.json', 'w') as f:
        json.dump(results, f)
    """)
    
    print("\n✅ NEW APPROACH:")
    print("""
    # Modular classes
    from src.validators import ValidationOrchestrator
    from src.exceptions import ValidationError
    from src.utils import safe_json_dump, setup_logging
    
    logger = setup_logging()
    
    try:
        # Clean separation of concerns
        orchestrator = ValidationOrchestrator(precision=30)
        results = orchestrator.run_all()
        
        # Safe JSON writing with logging
        safe_json_dump(results, 'results.json', logger)
        
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        print(f"Details: {e.details}")
    """)
    
    print("\n✓ Benefits:")
    print("  • Modular and reusable code")
    print("  • Proper exception handling")
    print("  • Structured logging")
    print("  • Easy to test and maintain")
    print("  • Clear separation of concerns")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("   REFACTORING DEMONSTRATION")
    print("   Modularidad, Dependencias y Manejo de Excepciones")
    print("=" * 70)
    
    try:
        demo_exception_handling()
        time.sleep(1)
        
        demo_retry_logic()
        time.sleep(1)
        
        demo_modular_validators()
        time.sleep(1)
        
        demo_utility_functions()
        time.sleep(1)
        
        demo_comparison()
        
        print("\n" + "=" * 70)
        print("✅ All demonstrations completed successfully!")
        print("=" * 70)
        print("\nFor more information, see REFACTORING_GUIDE.md")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error during demonstration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
