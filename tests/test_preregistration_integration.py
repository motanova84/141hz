#!/usr/bin/env python3
"""
Integration test for 141 Hz preregistration components.

This test verifies that all preregistration files are consistent
and can be loaded correctly.
"""

import json
import csv
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_analysis_plan_json():
    """Test that analysis_plan.json is valid and contains expected fields."""
    print("Testing analysis_plan.json...")
    
    with open("analysis_plan.json", "r") as f:
        plan = json.load(f)
    
    # Check required fields
    assert "time_window_s" in plan, "Missing time_window_s"
    assert "band_hz" in plan, "Missing band_hz"
    assert "f0_hz" in plan, "Missing f0_hz"
    assert "tolerance_hz" in plan, "Missing tolerance_hz"
    assert "psd" in plan, "Missing psd"
    assert "detectors" in plan, "Missing detectors"
    
    # Check values match preregistration
    assert plan["time_window_s"] == 0.25, "time_window_s should be 0.25"
    assert plan["band_hz"] == [20, 1024], "band_hz should be [20, 1024]"
    assert plan["f0_hz"] == 141.7001, "f0_hz should be 141.7001"
    assert plan["tolerance_hz"] == 0.3, "tolerance_hz should be 0.3"
    assert plan["detectors"] == ["H1", "L1", "V1"], "detectors should be H1, L1, V1"
    assert plan["multiple_events"] == "hierarchical_bayes", "should use hierarchical_bayes"
    
    # Check PSD parameters
    assert plan["psd"]["nfft"] == 16384, "nfft should be 16384 (2^14)"
    assert plan["psd"]["overlap"] == 0.5, "overlap should be 0.5"
    assert plan["psd"]["window"] == "hann", "window should be hann"
    
    print("✓ analysis_plan.json is valid")


def test_lines_exclusion_csv():
    """Test that controls/lines_exclusion.csv is valid."""
    print("Testing controls/lines_exclusion.csv...")
    
    with open("controls/lines_exclusion.csv", "r") as f:
        reader = csv.DictReader(f)
        lines = list(reader)
    
    assert len(lines) >= 3, "Should have at least 3 exclusion lines"
    
    # Check headers
    assert "freq_hz" in lines[0], "Missing freq_hz column"
    assert "width_hz" in lines[0], "Missing width_hz column"
    assert "reason" in lines[0], "Missing reason column"
    assert "source" in lines[0], "Missing source column"
    
    # Check first line (60 Hz)
    assert lines[0]["freq_hz"] == "60", "First line should be 60 Hz"
    assert lines[0]["width_hz"] == "2", "First line width should be 2 Hz"
    
    print("✓ controls/lines_exclusion.csv is valid")


def test_antenna_pattern_notebook():
    """Test that notebooks/antenna_pattern.ipynb is a valid notebook."""
    print("Testing notebooks/antenna_pattern.ipynb...")
    
    with open("notebooks/antenna_pattern.ipynb", "r") as f:
        nb = json.load(f)
    
    assert "cells" in nb, "Missing cells in notebook"
    assert "metadata" in nb, "Missing metadata in notebook"
    assert "nbformat" in nb, "Missing nbformat in notebook"
    
    # Check cells
    cells = nb["cells"]
    assert len(cells) == 3, "Should have 3 cells (markdown, code, markdown)"
    assert cells[0]["cell_type"] == "markdown", "First cell should be markdown"
    assert cells[1]["cell_type"] == "code", "Second cell should be code"
    assert cells[2]["cell_type"] == "markdown", "Third cell should be markdown"
    
    # Check code cell contains expected content
    code = "".join(cells[1]["source"])
    assert "H1" in code and "L1" in code and "V1" in code, "Should include all detectors"
    assert "Fplus_Fcross" in code or "antenna" in code.lower(), "Should have antenna pattern function"
    assert "SITES" in code, "Should have detector site definitions"
    assert "ra" in code and "dec" in code, "Should have sky position parameters"
    
    print("✓ notebooks/antenna_pattern.ipynb is valid")


def test_preregistration_md():
    """Test that PREREGISTRATION.md exists and contains expected content."""
    print("Testing PREREGISTRATION.md...")
    
    with open("PREREGISTRATION.md", "r") as f:
        content = f.read()
    
    # Check key sections
    assert "141.7001 Hz" in content, "Should reference target frequency"
    assert "0.25 s" in content, "Should reference time window"
    assert "20–1024 Hz" in content or "20-1024 Hz" in content, "Should reference frequency band"
    assert "Welch" in content, "Should reference Welch method"
    assert "H1" in content and "L1" in content, "Should reference detectors"
    assert "jerárquico" in content or "Bayes factor" in content, "Should reference hierarchical/Bayes"
    assert "10^4" in content or "10,000" in content, "Should reference off-source windows"
    
    print("✓ PREREGISTRATION.md is valid")


def test_bayes_module():
    """Test that bayes module can be imported and used."""
    print("Testing bayes module...")

    from bayes.hierarchical_model import bayes_factor

    # Test basic functionality
    snr_list = [5.0, 6.0, 5.5]
    bf = bayes_factor(snr_list, grid_size=51)

    assert bf > 0, "Bayes factor should be positive"
    assert bf < float('inf'), "Bayes factor should be finite"

    print(f"✓ bayes module working (BF = {bf:.4e})")


def main():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("141 Hz Preregistration Integration Tests")
    print("="*60 + "\n")
    
    tests = [
        test_analysis_plan_json,
        test_lines_exclusion_csv,
        test_antenna_pattern_notebook,
        test_preregistration_md,
        test_bayes_module,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("All integration tests passed! ✓")


if __name__ == "__main__":
    main()
