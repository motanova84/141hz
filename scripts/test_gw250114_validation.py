#!/usr/bin/env python3
"""
Test suite for GW250114 141.7 Hz validation scripts

Tests both single-event and multi-event validation to ensure:
- Scripts run without errors
- Output files are generated
- Results meet basic validation criteria
- JSON outputs are valid
"""

import subprocess
import json
import os
import sys
import tempfile
import shutil


def test_single_event_validation():
    """Test validate_gw250114_141hz_peak.py"""
    print("\n" + "="*70)
    print("TEST 1: Single Event Validation")
    print("="*70)
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = os.path.join(tmpdir, "test_single")
        
        # Run the script
        cmd = [
            "python3",
            "scripts/validate_gw250114_141hz_peak.py",
            "--simulated",
            "--output-dir", output_dir
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check exit code
        assert result.returncode == 0, f"Script failed with code {result.returncode}"
        print("✅ Script executed successfully")
        
        # Check output files exist
        json_file = os.path.join(output_dir, "gw250114_141hz_results.json")
        png_file = os.path.join(output_dir, "gw250114_141hz_validation.png")
        
        assert os.path.exists(json_file), f"Missing results JSON: {json_file}"
        assert os.path.exists(png_file), f"Missing validation plot: {png_file}"
        print("✅ Output files created")
        
        # Load and validate JSON
        with open(json_file, 'r') as f:
            results = json.load(f)
        
        # Check structure
        assert 'analysis' in results, "Missing 'analysis' key"
        assert 'detectors' in results, "Missing 'detectors' key"
        assert 'statistics' in results, "Missing 'statistics' key"
        assert 'H1' in results['detectors'], "Missing H1 detector"
        assert 'L1' in results['detectors'], "Missing L1 detector"
        print("✅ JSON structure valid")
        
        # Check values
        target_freq = results['analysis']['target_frequency']
        assert target_freq == 141.7001, f"Wrong target frequency: {target_freq}"
        
        h1_snr = results['detectors']['H1']['snr']
        l1_snr = results['detectors']['L1']['snr']
        coherent_snr = results['statistics']['coherent_snr']
        p_value = results['statistics']['p_value']
        
        assert isinstance(h1_snr, float), "H1 SNR not a float"
        assert isinstance(l1_snr, float), "L1 SNR not a float"
        assert isinstance(coherent_snr, float), "Coherent SNR not a float"
        assert isinstance(p_value, float), "p-value not a float"
        assert 0 <= p_value <= 1, f"Invalid p-value: {p_value}"
        
        print(f"✅ Results validated:")
        print(f"   Target: {target_freq} Hz")
        print(f"   H1 SNR: {h1_snr:.2f}")
        print(f"   L1 SNR: {l1_snr:.2f}")
        print(f"   Coherent SNR: {coherent_snr:.2f}")
        print(f"   p-value: {p_value:.2e}")
        
        return True


def test_multi_event_validation():
    """Test validate_multievent_141hz_peak.py"""
    print("\n" + "="*70)
    print("TEST 2: Multi-Event Validation")
    print("="*70)
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = os.path.join(tmpdir, "test_multi")
        
        # Run the script with 2 events for faster testing
        cmd = [
            "python3",
            "scripts/validate_multievent_141hz_peak.py",
            "--simulated",
            "--events", "GW250114,GW150914",
            "--output-dir", output_dir
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check exit code
        assert result.returncode == 0, f"Script failed with code {result.returncode}"
        print("✅ Script executed successfully")
        
        # Check output files exist
        json_file = os.path.join(output_dir, "multievent_141hz_results.json")
        report_file = os.path.join(output_dir, "SUMMARY_REPORT.md")
        
        assert os.path.exists(json_file), f"Missing results JSON: {json_file}"
        assert os.path.exists(report_file), f"Missing summary report: {report_file}"
        print("✅ Output files created")
        
        # Load and validate JSON
        with open(json_file, 'r') as f:
            results = json.load(f)
        
        # Check structure
        assert 'events' in results, "Missing 'events' key"
        assert 'combined_statistics' in results, "Missing 'combined_statistics' key"
        assert len(results['events']) == 2, f"Expected 2 events, got {len(results['events'])}"
        print("✅ JSON structure valid")
        
        # Check combined statistics
        stats = results['combined_statistics']
        assert 'combined_p_value' in stats, "Missing combined p-value"
        assert 'combined_sigma' in stats, "Missing combined sigma"
        assert 'detection_rate' in stats, "Missing detection rate"
        
        combined_p = stats['combined_p_value']
        combined_sigma = stats['combined_sigma']
        detection_rate = stats['detection_rate']
        
        assert 0 <= combined_p <= 1, f"Invalid combined p-value: {combined_p}"
        assert 0 <= detection_rate <= 1, f"Invalid detection rate: {detection_rate}"
        
        print(f"✅ Combined results validated:")
        print(f"   Events: {stats['n_events']}")
        print(f"   Detection rate: {detection_rate*100:.1f}%")
        print(f"   Combined p-value: {combined_p:.2e}")
        print(f"   Combined significance: {combined_sigma:.2f}σ")
        
        # Check report file
        with open(report_file, 'r') as f:
            report = f.read()
        
        assert "Multi-Event 141.7001 Hz Validation Report" in report
        assert "141.7001 Hz" in report
        assert "CONCLUSION" in report
        print("✅ Summary report valid")
        
        return True


def test_reproducibility():
    """Test that scripts produce consistent results"""
    print("\n" + "="*70)
    print("TEST 3: Reproducibility")
    print("="*70)
    
    # Run the same analysis twice
    results = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(2):
            output_dir = os.path.join(tmpdir, f"run_{i}")
            
            cmd = [
                "python3",
                "scripts/validate_gw250114_141hz_peak.py",
                "--simulated",
                "--output-dir", output_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            assert result.returncode == 0
            
            json_file = os.path.join(output_dir, "gw250114_141hz_results.json")
            with open(json_file, 'r') as f:
                results.append(json.load(f))
        
        # Compare key metrics (should be similar but not identical due to random noise)
        snr1 = results[0]['statistics']['coherent_snr']
        snr2 = results[1]['statistics']['coherent_snr']
        
        # SNRs should be within reasonable range (same order of magnitude)
        snr_ratio = max(snr1, snr2) / min(snr1, snr2)
        assert snr_ratio < 2.0, f"SNRs too different: {snr1:.2f} vs {snr2:.2f}"
        
        print(f"✅ Reproducibility check passed:")
        print(f"   Run 1 SNR: {snr1:.2f}")
        print(f"   Run 2 SNR: {snr2:.2f}")
        print(f"   Ratio: {snr_ratio:.2f} (< 2.0)")
        
        return True


def main():
    """Run all tests"""
    print("="*70)
    print("GW250114 141.7 Hz Validation Test Suite")
    print("="*70)
    
    # Change to repository root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    os.chdir(repo_root)
    print(f"Working directory: {os.getcwd()}")
    
    tests = [
        ("Single Event Validation", test_single_event_validation),
        ("Multi-Event Validation", test_multi_event_validation),
        ("Reproducibility", test_reproducibility),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Final summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
