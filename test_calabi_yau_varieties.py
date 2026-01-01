#!/usr/bin/env python3
"""
Test script for Calabi-Yau varieties database.

This script validates the 150 Calabi-Yau varieties data and ensures
all the functionality works correctly.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∞³)
Date: January 2026
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from calabi_yau_varieties import CalabiYauDatabase, CalabiYauVariety


def test_database_loading():
    """Test that the database loads correctly."""
    print("Testing database loading...")
    
    db = CalabiYauDatabase()
    
    assert len(db.varieties) == 150, f"Expected 150 varieties, got {len(db.varieties)}"
    assert db.metadata['total_varieties'] == 150, "Metadata total_varieties mismatch"
    
    print("✅ Database loaded successfully with 150 varieties")


def test_variety_properties():
    """Test that variety properties are calculated correctly."""
    print("\nTesting variety properties...")
    
    # Test Fermat quintic: (h¹¹=1, h²¹=101) → χ = 2(1-101) = -200
    variety = CalabiYauVariety(id=1, h11=1, h21=101)
    
    assert variety.euler_characteristic == -200, f"Euler characteristic mismatch: {variety.euler_characteristic}"
    assert variety.hodge_numbers == (1, 101), f"Hodge numbers mismatch: {variety.hodge_numbers}"
    
    # Test symmetric case: (h¹¹=30, h²¹=30) → χ = 0
    variety2 = CalabiYauVariety(id=30, h11=30, h21=30)
    assert variety2.euler_characteristic == 0, f"Euler characteristic should be 0: {variety2.euler_characteristic}"
    
    print("✅ Variety properties calculated correctly")


def test_database_queries():
    """Test database query methods."""
    print("\nTesting database queries...")
    
    db = CalabiYauDatabase()
    
    # Test get_variety
    variety1 = db.get_variety(1)
    assert variety1 is not None, "Variety 1 not found"
    assert variety1.h11 == 1 and variety1.h21 == 101, "Variety 1 has wrong Hodge numbers"
    
    # Test get_quintic_fermat
    quintic = db.get_quintic_fermat()
    assert quintic is not None, "Fermat quintic not found"
    assert quintic.h11 == 1 and quintic.h21 == 101, "Fermat quintic has wrong Hodge numbers"
    
    # Test filter_by_h11
    h11_1_varieties = db.filter_by_h11(1)
    assert len(h11_1_varieties) > 0, "No varieties with h¹¹=1 found"
    
    # Test filter_by_h21
    h21_101_varieties = db.filter_by_h21(101)
    assert len(h21_101_varieties) > 0, "No varieties with h²¹=101 found"
    
    # Test filter_by_euler
    chi_0_varieties = db.filter_by_euler(0)
    assert len(chi_0_varieties) > 0, "No varieties with χ=0 found"
    
    print("✅ Database queries work correctly")


def test_data_consistency():
    """Test that all 150 varieties have the correct Hodge numbers."""
    print("\nTesting data consistency...")
    
    db = CalabiYauDatabase()
    
    # Expected Hodge numbers from the problem statement
    expected = [
        (1, 101), (2, 90), (3, 75), (4, 64), (5, 65),
        (6, 60), (7, 54), (8, 52), (9, 51), (10, 50),
        (11, 49), (12, 48), (13, 47), (14, 46), (15, 45),
        (16, 44), (17, 43), (18, 42), (19, 41), (20, 40),
        (21, 39), (22, 38), (23, 37), (24, 36), (25, 35),
        (26, 34), (27, 33), (28, 32), (29, 31), (30, 30),
        (31, 29), (32, 28), (33, 27), (34, 26), (35, 25),
        (36, 24), (37, 23), (38, 22), (39, 21), (40, 20),
        (41, 19), (42, 18), (43, 17), (44, 16), (45, 15),
        (46, 14), (47, 13), (48, 12), (49, 11), (50, 10),
        (51, 9), (52, 8), (53, 7), (54, 6), (55, 5),
        (56, 4), (57, 3), (58, 2), (59, 1), (60, 60),
        (61, 59), (62, 58), (63, 57), (64, 56), (65, 55),
        (66, 54), (67, 53), (68, 52), (69, 51), (70, 50),
        (71, 49), (72, 48), (73, 47), (74, 46), (75, 45),
        (76, 44), (77, 43), (78, 42), (79, 41), (80, 40),
        (81, 39), (82, 38), (83, 37), (84, 36), (85, 35),
        (86, 34), (87, 33), (88, 32), (89, 31), (90, 30),
        (91, 29), (92, 28), (93, 27), (94, 26), (95, 25),
        (96, 24), (97, 23), (98, 22), (99, 21), (100, 20),
        (101, 19), (102, 18), (103, 17), (104, 16), (105, 15),
        (106, 14), (107, 13), (108, 12), (109, 11), (110, 10),
        (111, 9), (112, 8), (113, 7), (114, 6), (115, 5),
        (116, 4), (117, 3), (118, 2), (119, 1), (120, 120),
        (121, 119), (122, 118), (123, 117), (124, 116), (125, 115),
        (126, 114), (127, 113), (128, 112), (129, 111), (130, 110),
        (131, 109), (132, 108), (133, 107), (134, 106), (135, 105),
        (136, 104), (137, 103), (138, 102), (139, 101), (140, 100),
        (141, 99), (142, 98), (143, 97), (144, 96), (145, 95),
        (146, 94), (147, 93), (148, 92), (149, 91), (150, 90)
    ]
    
    for i, (h11_exp, h21_exp) in enumerate(expected, start=1):
        variety = db.get_variety(i)
        assert variety is not None, f"Variety {i} not found"
        assert variety.h11 == h11_exp, f"Variety {i}: expected h¹¹={h11_exp}, got {variety.h11}"
        assert variety.h21 == h21_exp, f"Variety {i}: expected h²¹={h21_exp}, got {variety.h21}"
    
    print("✅ All 150 varieties have correct Hodge numbers")


def test_export_functionality():
    """Test CSV and JSON export."""
    print("\nTesting export functionality...")
    
    db = CalabiYauDatabase()
    
    # Create temporary output directory using tempfile for cross-platform compatibility
    import tempfile
    with tempfile.TemporaryDirectory() as output_dir:
        output_path = Path(output_dir)
        
        # Test CSV export
        csv_file = output_path / "test_export.csv"
        db.export_to_csv(csv_file)
        assert csv_file.exists(), "CSV export failed"
        
        # Verify CSV has correct number of lines (header + 150 varieties)
        with open(csv_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 151, f"CSV should have 151 lines (header + 150), got {len(lines)}"
        
        # Test JSON export
        json_file = output_path / "test_export.json"
        db.export_to_json(json_file)
        assert json_file.exists(), "JSON export failed"
    
    print("✅ Export functionality works correctly")


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("CALABI-YAU VARIETIES DATABASE - TEST SUITE")
    print("=" * 80)
    print()
    
    try:
        test_database_loading()
        test_variety_properties()
        test_database_queries()
        test_data_consistency()
        test_export_functionality()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80)
        return 0
    
    except AssertionError as e:
        print("\n" + "=" * 80)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 80)
        return 1
    
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ UNEXPECTED ERROR: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
