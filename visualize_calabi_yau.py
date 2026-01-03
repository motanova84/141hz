#!/usr/bin/env python3
"""
Visualize the distribution of Calabi-Yau varieties Hodge numbers.

This script creates plots showing the distribution of (h¹¹, h²¹) pairs
and the Euler characteristic χ across the 150 varieties.

Author: José Manuel Mota Burruezo (JMMB Ψ✧∞³)
Date: January 2026
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from calabi_yau_varieties import CalabiYauDatabase


def print_ascii_histogram(values, title, bins=20, width=60):
    """
    Print an ASCII histogram of values.
    
    Args:
        values: List of numeric values
        title: Title for the histogram
        bins: Number of bins
        width: Width of the histogram in characters
    """
    if not values:
        return
    
    min_val = min(values)
    max_val = max(values)
    
    # Handle case where all values are the same
    if min_val == max_val:
        print(f"\n{title}")
        print("=" * 80)
        print(f"All values are {min_val:.1f}")
        print()
        return
    
    # Create bins
    bin_width = (max_val - min_val) / bins
    bin_counts = [0] * bins
    
    for v in values:
        bin_idx = int((v - min_val) / bin_width)
        bin_idx = min(bin_idx, bins - 1)  # Handle max value
        bin_counts[bin_idx] += 1
    
    max_count = max(bin_counts) if bin_counts else 1
    
    print(f"\n{title}")
    print("=" * 80)
    
    for i, count in enumerate(bin_counts):
        bin_start = min_val + i * bin_width
        bin_end = bin_start + bin_width
        bar_length = int((count / max_count) * width) if max_count > 0 else 0
        bar = "█" * bar_length
        print(f"[{bin_start:6.1f}-{bin_end:6.1f}] {count:3d} {bar}")
    
    print()


def print_scatter_plot(h11_values, h21_values, width=70, height=25):
    """
    Print an ASCII scatter plot of (h¹¹, h²¹) pairs.
    
    Args:
        h11_values: List of h¹¹ values
        h21_values: List of h²¹ values
        width: Width of plot in characters
        height: Height of plot in characters
    """
    if not h11_values or not h21_values:
        return
    
    min_h11 = min(h11_values)
    max_h11 = max(h11_values)
    min_h21 = min(h21_values)
    max_h21 = max(h21_values)
    
    # Create grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Plot points
    for h11, h21 in zip(h11_values, h21_values):
        x = int((h11 - min_h11) / (max_h11 - min_h11) * (width - 1)) if max_h11 > min_h11 else 0
        y = int((h21 - min_h21) / (max_h21 - min_h21) * (height - 1)) if max_h21 > min_h21 else 0
        y = height - 1 - y  # Flip Y axis
        
        if grid[y][x] == ' ':
            grid[y][x] = '●'
        elif grid[y][x] == '●':
            grid[y][x] = '◆'  # Multiple points
    
    print("\nScatter Plot: Hodge Numbers (h¹¹, h²¹)")
    print("=" * 80)
    print(f"h²¹ ({max_h21:3.0f})")
    print("│")
    
    for row in grid:
        print("│" + ''.join(row))
    
    print("└" + "─" * width)
    print(f"{' ' * (width - 10)}h¹¹ ({max_h11:3.0f})")
    print()


def analyze_patterns(db):
    """
    Analyze and print patterns in the Calabi-Yau varieties.
    
    Args:
        db: CalabiYauDatabase instance
    """
    varieties = db.get_all()
    
    print("\nPattern Analysis")
    print("=" * 80)
    
    # Count symmetric varieties (h¹¹ = h²¹)
    symmetric = [v for v in varieties if v.h11 == v.h21]
    print(f"Symmetric varieties (h¹¹ = h²¹): {len(symmetric)}")
    if symmetric:
        print(f"  Examples: {', '.join(f'({v.h11},{v.h21})' for v in symmetric[:5])}")
    
    # Count varieties with χ = 0
    chi_zero = [v for v in varieties if v.euler_characteristic == 0]
    print(f"\nVarieties with χ = 0: {len(chi_zero)}")
    if chi_zero:
        print(f"  Examples: {', '.join(f'({v.h11},{v.h21})' for v in chi_zero[:5])}")
    
    # Find extreme values
    max_chi = max(varieties, key=lambda v: v.euler_characteristic)
    min_chi = min(varieties, key=lambda v: v.euler_characteristic)
    
    print(f"\nExtreme Euler characteristics:")
    print(f"  Maximum: χ = {max_chi.euler_characteristic} at (h¹¹={max_chi.h11}, h²¹={max_chi.h21})")
    print(f"  Minimum: χ = {min_chi.euler_characteristic} at (h¹¹={min_chi.h11}, h²¹={min_chi.h21})")
    
    # Mirror symmetry candidates
    print(f"\nMirror symmetry notes:")
    print(f"  The Fermat quintic (1,101) has mirror partner (101,1) with χ = 200")
    print(f"  This demonstrates the h¹¹ ↔ h²¹ mirror symmetry in string theory")
    
    print()


def main():
    """Main visualization function."""
    print("=" * 80)
    print("CALABI-YAU VARIETIES - VISUALIZATION")
    print("=" * 80)
    
    # Load database
    db = CalabiYauDatabase()
    varieties = db.get_all()
    
    # Extract data
    h11_values = [v.h11 for v in varieties]
    h21_values = [v.h21 for v in varieties]
    chi_values = [v.euler_characteristic for v in varieties]
    
    # Print scatter plot
    print_scatter_plot(h11_values, h21_values)
    
    # Print histograms
    print_ascii_histogram(h11_values, "Distribution of h¹¹ values", bins=15)
    print_ascii_histogram(h21_values, "Distribution of h²¹ values", bins=15)
    print_ascii_histogram(chi_values, "Distribution of Euler characteristic χ", bins=15)
    
    # Analyze patterns
    analyze_patterns(db)
    
    # Print summary statistics
    print("Summary Statistics")
    print("=" * 80)
    print(f"Total varieties: {len(varieties)}")
    print(f"h¹¹: mean = {sum(h11_values)/len(h11_values):.1f}, "
          f"range = [{min(h11_values)}, {max(h11_values)}]")
    print(f"h²¹: mean = {sum(h21_values)/len(h21_values):.1f}, "
          f"range = [{min(h21_values)}, {max(h21_values)}]")
    print(f"χ:   mean = {sum(chi_values)/len(chi_values):.1f}, "
          f"range = [{min(chi_values)}, {max(chi_values)}]")
    print()
    
    print("=" * 80)
    print("VISUALIZATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
