#!/usr/bin/env python3
"""
Visualize benchmark results

Creates comparison plots from benchmark JSON files.

Author: José Manuel Mota Burruezo (JMMB)
"""

import json
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


def plot_gw_analysis_benchmark(results, output_file):
    """
    Plot GW analysis framework comparison
    
    Args:
        results: Benchmark results dictionary
        output_file: Output plot filename
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Extract available benchmarks
    frameworks = []
    times = []
    memory = []
    
    for name, result in results['benchmarks'].items():
        if result.get('available'):
            frameworks.append(result['framework'])
            times.append(result['execution_time'])
            memory.append(result.get('memory_used_mb', 0))
    
    if not frameworks:
        print("⚠️  No available benchmark data to plot")
        return
    
    # Plot 1: Execution time
    colors = plt.cm.Set2(np.linspace(0, 1, len(frameworks)))
    bars1 = ax1.bar(frameworks, times, color=colors)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=12)
    ax1.set_title('Framework Performance Comparison', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}s',
                ha='center', va='bottom', fontsize=10)
    
    # Plot 2: Memory usage
    bars2 = ax2.bar(frameworks, memory, color=colors)
    ax2.set_ylabel('Memory Used (MB)', fontsize=12)
    ax2.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}MB',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_file}")


def plot_numerical_precision(results, output_file):
    """
    Plot numerical precision results
    
    Args:
        results: Precision test results
        output_file: Output plot filename
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Float precision comparison
    fp = results['tests']['float_precision']
    types = ['float32', 'float64']
    digits = [fp['float32']['significant_digits'], fp['float64']['significant_digits']]
    
    bars1 = ax1.bar(types, digits, color=['#ff7f0e', '#2ca02c'])
    ax1.set_ylabel('Significant Digits', fontsize=11)
    ax1.set_title('Floating Point Precision', fontsize=12, fontweight='bold')
    ax1.set_ylim([0, 18])
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars1, digits):
        ax1.text(bar.get_x() + bar.get_width()/2., val + 0.5,
                f'{val} digits',
                ha='center', va='bottom', fontsize=10)
    
    # Plot 2: Frequency resolution
    fr = results['tests']['frequency_resolution']
    
    ax2.text(0.5, 0.8, f"Sample Rate: {fr['sample_rate']} Hz",
            transform=ax2.transAxes, fontsize=11, ha='center')
    ax2.text(0.5, 0.6, f"Duration: {fr['duration']} s",
            transform=ax2.transAxes, fontsize=11, ha='center')
    ax2.text(0.5, 0.4, f"Resolution: {fr['frequency_resolution']:.4f} Hz",
            transform=ax2.transAxes, fontsize=12, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax2.text(0.5, 0.2, f"Total Bins: {fr['total_bins']:,}",
            transform=ax2.transAxes, fontsize=11, ha='center')
    ax2.set_title('Frequency Resolution', fontsize=12, fontweight='bold')
    ax2.axis('off')
    
    # Plot 3: Energy calculation accuracy
    ea = results['tests']['energy_accuracy']
    
    frequencies = [calc['frequency'] for calc in ea['calculations']]
    accuracies = [calc['accurate_to_digits'] for calc in ea['calculations']]
    
    bars3 = ax3.bar(range(len(frequencies)), accuracies, 
                    color=plt.cm.viridis(np.linspace(0.3, 0.9, len(frequencies))))
    ax3.set_xticks(range(len(frequencies)))
    ax3.set_xticklabels([f"{f:.1f}" for f in frequencies], rotation=45)
    ax3.set_xlabel('Frequency (Hz)', fontsize=11)
    ax3.set_ylabel('Accurate to N Digits', fontsize=11)
    ax3.set_title('Energy Calculation Accuracy (E = hf)', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    ax3.set_ylim([0, 18])
    
    # Plot 4: FFT precision
    fft = results['tests']['fft_precision']
    
    metrics = ['Frequency\nError', 'Reconstruction\nError (relative)']
    values = [fft['frequency_error'], fft['reconstruction_relative_error']]
    
    ax4.bar(metrics, values, color=['#d62728', '#9467bd'])
    ax4.set_ylabel('Error (log scale)', fontsize=11)
    ax4.set_yscale('log')
    ax4.set_title('FFT Precision', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    for i, (metric, val) in enumerate(zip(metrics, values)):
        ax4.text(i, val * 2, f'{val:.2e}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_file}")


def plot_quantum_scaling(results, output_file):
    """
    Plot quantum solver scaling results
    
    Args:
        results: Quantum benchmark results
        output_file: Output plot filename
    """
    if 'scaling_analysis' not in results:
        print("⚠️  No scaling analysis data available")
        return
    
    scaling = results['scaling_analysis']
    if 'results' not in scaling:
        return
    
    # Extract data
    N_values = []
    times = []
    
    for result in scaling['results']:
        if result.get('numpy_scipy', {}).get('available'):
            N_values.append(result['N'])
            times.append(result['numpy_scipy']['avg_time_seconds'])
    
    if not N_values:
        print("⚠️  No valid scaling data to plot")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Linear scale
    ax1.plot(N_values, times, 'o-', linewidth=2, markersize=8, label='Measured')
    ax1.set_xlabel('Number of Spins (N)', fontsize=12)
    ax1.set_ylabel('Time (seconds)', fontsize=12)
    ax1.set_title('Scaling Behavior (Linear)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)
    
    # Plot 2: Log-log scale
    ax2.loglog(N_values, times, 'o-', linewidth=2, markersize=8, label='Measured')
    
    # Fit line
    if 'scaling_analysis' in scaling:
        sa = scaling['scaling_analysis']
        if 'scaling_exponent' in sa:
            alpha = sa['scaling_exponent']
            # Plot fitted line
            N_fit = np.linspace(min(N_values), max(N_values), 100)
            # T = c * N^alpha
            c = times[0] / (N_values[0] ** alpha)
            T_fit = c * (N_fit ** alpha)
            ax2.loglog(N_fit, T_fit, '--', linewidth=2, 
                      label=f'Fit: O(N^{alpha:.2f})', alpha=0.7)
    
    ax2.set_xlabel('Number of Spins (N)', fontsize=12)
    ax2.set_ylabel('Time (seconds)', fontsize=12)
    ax2.set_title('Scaling Behavior (Log-Log)', fontsize=14, fontweight='bold')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Visualize benchmark results'
    )
    parser.add_argument('--input', type=str,
                       help='Input JSON benchmark file')
    parser.add_argument('--type', type=str,
                       choices=['gw_analysis', 'numerical_precision', 'quantum_scaling'],
                       help='Type of benchmark')
    parser.add_argument('--output-dir', type=str,
                       default='results/benchmark/plots',
                       help='Output directory for plots')
    parser.add_argument('--all', action='store_true',
                       help='Generate all available plots')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("BENCHMARK VISUALIZATION")
    print("=" * 70)
    
    if args.all:
        # Generate all available plots
        benchmark_files = {
            'gw_analysis': 'results/benchmark/gw_analysis_benchmark.json',
            'numerical_precision': 'results/benchmark/numerical_precision.json',
            'quantum_scaling': 'results/benchmark_results.json'
        }
        
        for bench_type, filepath in benchmark_files.items():
            filepath = Path(filepath)
            if filepath.exists():
                print(f"\nProcessing {bench_type}...")
                with open(filepath, 'r') as f:
                    results = json.load(f)
                
                output_file = output_dir / f'{bench_type}_comparison.png'
                
                if bench_type == 'gw_analysis':
                    plot_gw_analysis_benchmark(results, output_file)
                elif bench_type == 'numerical_precision':
                    plot_numerical_precision(results, output_file)
                elif bench_type == 'quantum_scaling':
                    plot_quantum_scaling(results, output_file)
            else:
                print(f"\n⚠️  {bench_type}: File not found: {filepath}")
    
    elif args.input:
        # Generate specific plot
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ File not found: {input_path}")
            return
        
        with open(input_path, 'r') as f:
            results = json.load(f)
        
        output_file = output_dir / f'{args.type}_comparison.png'
        
        print(f"\nGenerating {args.type} plot...")
        
        if args.type == 'gw_analysis':
            plot_gw_analysis_benchmark(results, output_file)
        elif args.type == 'numerical_precision':
            plot_numerical_precision(results, output_file)
        elif args.type == 'quantum_scaling':
            plot_quantum_scaling(results, output_file)
    
    else:
        parser.error("Must specify --input and --type, or --all")
    
    print(f"\n✅ Visualization complete!")
    print(f"Plots saved to: {output_dir}")


if __name__ == '__main__':
    main()
