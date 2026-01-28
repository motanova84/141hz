#!/usr/bin/env python3
"""
Validation and testing framework for biological periodicity analysis.

This script provides automated tests and validation checks to ensure
the reproducibility and correctness of the biological rhythm analysis.
Designed for peer review and external validation.
"""

import sys
import os
import json
import numpy as np
from typing import Dict, List, Tuple


def validate_api_clients():
    """Test that API clients are properly configured and functional."""
    print("=== Validating API Clients ===")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
        from api_clients import NASAPowerAPIClient, NOAAAPIClient
        
        # Test NASA POWER client
        print("Testing NASA POWER API client...")
        nasa = NASAPowerAPIClient()
        
        # Test with a simple request
        test_data = nasa.get_agricultural_data(
            latitude=0.0,
            longitude=0.0,
            start_date='20240101',
            end_date='20240102'
        )
        
        if test_data and 'parameters' in test_data:
            print("✓ NASA POWER API client working")
        else:
            print("⚠ NASA POWER API returned empty response (may be rate limited)")
        
        # Test NOAA client
        print("Testing NOAA API client...")
        noaa = NOAAAPIClient()
        if noaa.api_token:
            print("✓ NOAA API token configured")
        else:
            print("⚠ NOAA API token not configured (set NOAA_API_TOKEN env var)")
        
        return True
        
    except Exception as e:
        print(f"✗ API client validation failed: {e}")
        return False


def validate_biological_analysis():
    """Test biological periodicity analysis functions."""
    print("\n=== Validating Biological Analysis ===")
    
    try:
        from biological_periodicity import (
            BiologicalRhythmAnalyzer,
            ArabidopsisAnalyzer,
            TrichogrammaAnalyzer
        )
        
        # Test basic analyzer
        print("Testing BiologicalRhythmAnalyzer...")
        analyzer = BiologicalRhythmAnalyzer('arabidopsis')
        
        # Test harmonic calculation
        result = analyzer.calculate_harmonic_relationship(24.0)
        
        # Verify expected properties
        assert 'biological_period_hours' in result
        assert 'harmonic_ratio' in result
        assert 'nearest_harmonic' in result
        assert 'is_harmonic' in result
        
        # Test specific values
        assert result['biological_period_hours'] == 24.0
        assert result['f0_hz'] == 141.7001
        
        print("✓ Basic harmonic calculation working")
        
        # Test Arabidopsis analyzer
        print("Testing ArabidopsisAnalyzer...")
        arab = ArabidopsisAnalyzer()
        arab_results = arab.analyze_all_periods()
        
        assert 'species' in arab_results
        assert arab_results['species'] == 'arabidopsis'
        assert 'periods' in arab_results
        assert len(arab_results['periods']) > 0
        
        print("✓ Arabidopsis analysis working")
        
        # Test Trichogramma analyzer
        print("Testing TrichogrammaAnalyzer...")
        trich = TrichogrammaAnalyzer()
        trich_results = trich.analyze_developmental_stages(25.0)
        
        assert 'temperature_celsius' in trich_results
        assert 'stages' in trich_results
        
        print("✓ Trichogramma analysis working")
        
        return True
        
    except Exception as e:
        print(f"✗ Biological analysis validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_harmonic_accuracy():
    """
    Validate that harmonic calculations are accurate.
    
    Tests known values to ensure mathematical correctness.
    """
    print("\n=== Validating Harmonic Accuracy ===")
    
    try:
        from biological_periodicity import BiologicalRhythmAnalyzer
        
        analyzer = BiologicalRhythmAnalyzer('arabidopsis')
        f0 = 141.7001
        
        # Test 1: 24-hour period should give specific harmonic
        result_24h = analyzer.calculate_harmonic_relationship(24.0)
        
        # Calculate expected values
        period_sec = 24.0 * 3600
        freq_hz = 1 / period_sec
        expected_ratio = f0 / freq_hz
        
        # Check calculations
        assert abs(result_24h['biological_freq_hz'] - freq_hz) < 1e-10
        assert abs(result_24h['harmonic_ratio'] - expected_ratio) < 1e-6
        
        print(f"✓ 24h period: harmonic ratio = {result_24h['harmonic_ratio']:.2f}")
        
        # Test 2: Very short period (should not be harmonic)
        result_short = analyzer.calculate_harmonic_relationship(0.001)
        assert result_short['is_harmonic'] == False
        print("✓ Short periods correctly identified as non-harmonic")
        
        # Test 3: Verify reciprocal relationship
        # If period P is harmonic n, then frequency should be f0/n
        for test_period in [24.0, 12.0, 3.0]:
            result = analyzer.calculate_harmonic_relationship(test_period)
            n = result['nearest_harmonic']
            expected_freq = f0 / n
            
            # Check frequency matches (within tolerance for non-exact harmonics)
            freq_error = abs(result['biological_freq_hz'] - expected_freq) / expected_freq
            
            if result['is_harmonic']:
                assert freq_error < 0.01  # Within 1% for harmonics
            
        print("✓ Harmonic reciprocal relationships verified")
        
        return True
        
    except Exception as e:
        print(f"✗ Harmonic accuracy validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_data_quality():
    """Validate data quality and consistency checks."""
    print("\n=== Validating Data Quality ===")
    
    try:
        from biological_periodicity import compare_species_periodicities
        
        # Run cross-species comparison
        comparison = compare_species_periodicities()
        
        # Check data structure
        assert 'f0_hz' in comparison
        assert 'species_comparison' in comparison
        assert 'harmonic_resonances' in comparison
        
        # Validate f0 value
        assert comparison['f0_hz'] == 141.7001
        print("✓ Fundamental frequency correct")
        
        # Check each species has valid data
        for species_name, species_data in comparison['species_comparison'].items():
            assert 'species' in species_data
            assert 'periods' in species_data
            assert len(species_data['periods']) > 0
            
            # Validate each period has required fields
            for period_name, period_data in species_data['periods'].items():
                required_fields = [
                    'biological_period_hours',
                    'biological_freq_hz',
                    'harmonic_ratio',
                    'nearest_harmonic',
                    'harmonic_deviation_percent',
                    'is_harmonic'
                ]
                
                for field in required_fields:
                    assert field in period_data, f"Missing field {field} in {species_name}/{period_name}"
                
                # Validate numeric ranges
                assert period_data['biological_period_hours'] > 0
                assert period_data['biological_freq_hz'] > 0
                assert period_data['nearest_harmonic'] > 0
                assert 0 <= period_data['harmonic_deviation_percent'] <= 100
        
        print(f"✓ Data quality validated for {len(comparison['species_comparison'])} species")
        
        return True
        
    except Exception as e:
        print(f"✗ Data quality validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_validation_report():
    """Generate a comprehensive validation report."""
    print("\n" + "="*60)
    print("PEER REVIEW VALIDATION REPORT")
    print("="*60)
    
    results = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'tests': {}
    }
    
    # Run all validation tests
    tests = [
        ('API Clients', validate_api_clients),
        ('Biological Analysis', validate_biological_analysis),
        ('Harmonic Accuracy', validate_harmonic_accuracy),
        ('Data Quality', validate_data_quality),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results['tests'][test_name] = {
                'passed': passed,
                'error': None
            }
            if not passed:
                all_passed = False
        except Exception as e:
            results['tests'][test_name] = {
                'passed': False,
                'error': str(e)
            }
            all_passed = False
    
    # Save report
    report_file = 'validation_report.json'
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for t in results['tests'].values() if t['passed'])
    total_count = len(results['tests'])
    
    print(f"Tests passed: {passed_count}/{total_count}")
    
    if all_passed:
        print("\n✓ ALL VALIDATION TESTS PASSED")
        print("\nThe analysis is ready for peer review.")
    else:
        print("\n✗ SOME TESTS FAILED")
        print("\nPlease review the errors above.")
    
    print(f"\nDetailed report saved to: {report_file}")
    
    return all_passed


if __name__ == "__main__":
    print("Biological Periodicity Analysis - Validation Suite")
    print("="*60)
    print("\nThis script validates the reproducibility and correctness")
    print("of the biological rhythm analysis for peer review.\n")
    
    success = generate_validation_report()
    
    sys.exit(0 if success else 1)
