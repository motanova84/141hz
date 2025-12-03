#!/usr/bin/env python3
"""
Plot Balance Function: Visualization of P17 Adelic-Fractal Equilibrium

This script creates a visualization of the balance function:
    balance(p) = base + amplitude × (√p - √17)²

showing the clear minimum at p = 17.

The quadratic form in √p ensures that p = 17 is the unique equilibrium point
where adelic growth and fractal suppression balance perfectly.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Instituto de Consciencia Cuántica (ICQ)
QCAL ∞³ — Frecuencia Universal 141.7001 Hz
"""

import sys
import os
import numpy as np

try:
    import mpmath as mp
except ImportError:
    print("❌ Error: mpmath is required for high-precision calculations")
    print("Install with: pip install mpmath")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("❌ Error: matplotlib is required for plotting")
    print("Install with: pip install matplotlib")
    sys.exit(1)

# Import constants and functions from the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p17_balance_optimality import (
    BALANCE_BASE,
    BALANCE_AMPLITUDE,
    balance as p17_balance,
    get_primes_to_check,
)


def balance(p: float, precision: int = 50) -> float:
    """
    Calculate the balance function balance(p) = base + amplitude × (√p - √17)².

    This is a wrapper around the function from p17_balance_optimality for
    use with continuous (non-integer) values in plotting.

    Args:
        p: Prime number (or any positive real for interpolation)
        precision: Decimal precision for calculations

    Returns:
        The balance value at p
    """
    mp.dps = precision
    sqrt_p = mp.sqrt(p)
    sqrt_17 = mp.sqrt(17)
    return float(BALANCE_BASE + BALANCE_AMPLITUDE * (sqrt_p - sqrt_17) ** 2)


def create_balance_plot(output_path: str = "balance_p17.png", show: bool = False):
    """
    Create a visualization of the balance function with minimum at p=17.

    Args:
        output_path: Path to save the output image
        show: Whether to display the plot interactively
    """
    # Calculate balance for discrete primes
    primes = get_primes_to_check()
    balance_values = [balance(p) for p in primes]

    # Find minimum
    min_idx = np.argmin(balance_values)
    min_prime = primes[min_idx]
    min_balance = balance_values[min_idx]

    # Create continuous curve for interpolation
    p_continuous = np.linspace(10, 32, 200)
    balance_continuous = [balance(p) for p in p_continuous]

    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(10, 7))

    # Plot continuous curve (interpolation)
    ax.plot(p_continuous, balance_continuous, 'b-', alpha=0.3, linewidth=2,
            label=r'balance(x) = $b + a(\sqrt{x} - \sqrt{17})^2$')

    # Plot discrete prime points
    ax.scatter(primes, balance_values, s=100, c='blue', zorder=5, edgecolors='white',
               linewidth=2, label='Relevant primes')

    # Highlight the minimum at p=17
    ax.scatter([min_prime], [min_balance], s=200, c='red', marker='*', zorder=10,
               edgecolors='darkred', linewidth=2, label=f'MINIMUM: p={min_prime}')

    # Add vertical line at p=17
    ax.axvline(x=17, color='red', linestyle='--', alpha=0.5, linewidth=1.5)

    # Add horizontal line at minimum
    ax.axhline(y=min_balance, color='red', linestyle=':', alpha=0.3, linewidth=1)

    # Labels for each prime
    for p, b in zip(primes, balance_values):
        offset_y = 5 if p != min_prime else -15
        fontweight = 'bold' if p == min_prime else 'normal'
        ax.annotate(f'p={p}\n({b:.1f})',
                    xy=(p, b), xytext=(0, offset_y),
                    textcoords='offset points', ha='center', fontsize=9,
                    fontweight=fontweight,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    # Set labels and title
    ax.set_xlabel('Prime p', fontsize=12, fontweight='bold')
    ax.set_ylabel('balance(p)', fontsize=12, fontweight='bold')
    ax.set_title('Adelic-Fractal Balance Function\n'
                 'Minimum at p₀ = 17 → f₀ = 141.7001 Hz',
                 fontsize=14, fontweight='bold')

    # Linear scale is fine for the quadratic function
    # ax.set_yscale('log')  # Not needed for quadratic

    # Grid and legend
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=10)

    # Add text box with mathematical formula
    textstr = '\n'.join([
        r'$\mathrm{balance}(p) = b + a(\sqrt{p} - \sqrt{17})^2$',
        '',
        r'$b = 76.143$ (base value)',
        r'$a = 50.91$ (amplitude)',
        '',
        r'$p_0 = 17$ is the global minimum',
        r'$\Rightarrow f_0 = 141.7001$ Hz'
    ])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
    ax.text(0.97, 0.97, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    # Set axis limits
    ax.set_xlim(9, 31)

    plt.tight_layout()

    # Save and optionally show
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✓ Plot saved to: {output_path}")

    if show:
        plt.show()

    plt.close()

    return {
        "output_path": output_path,
        "primes": primes,
        "balance_values": balance_values,
        "minimum_prime": min_prime,
        "minimum_balance": min_balance
    }


def create_loglog_plot(output_path: str = "balance_p17_loglog.png", show: bool = False):
    """
    Create a log-log visualization of the balance function.

    Args:
        output_path: Path to save the output image
        show: Whether to display the plot interactively
    """
    # Calculate balance for discrete primes
    primes = get_primes_to_check()
    balance_values = [balance(p) for p in primes]

    # Find minimum
    min_idx = np.argmin(balance_values)
    min_prime = primes[min_idx]
    min_balance = balance_values[min_idx]

    # Create extended range for context
    extended_primes = [2, 3, 5, 7] + primes + [31, 37, 41, 43, 47]
    extended_balance = [balance(p) for p in extended_primes]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot all primes
    ax.scatter(extended_primes, extended_balance, s=60, c='blue', alpha=0.6,
               label='All primes')

    # Highlight the relevant range
    ax.scatter(primes, balance_values, s=120, c='green', zorder=5,
               edgecolors='darkgreen', linewidth=2,
               label='Relevant primes [11, 29]')

    # Highlight the minimum
    ax.scatter([min_prime], [min_balance], s=300, c='red', marker='*', zorder=10,
               edgecolors='darkred', linewidth=2,
               label=f'GLOBAL MINIMUM: p₀ = {min_prime}')

    # Add vertical line at p=17
    ax.axvline(x=17, color='red', linestyle='--', alpha=0.7, linewidth=2,
               label='p = 17')

    # Set log-log scale
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Labels
    ax.set_xlabel('Prime p (log scale)', fontsize=12, fontweight='bold')
    ax.set_ylabel('balance(p) (log scale)', fontsize=12, fontweight='bold')
    ax.set_title('Log-Log Plot: Adelic-Fractal Balance Function\n'
                 'Clear minimum at p₀ = 17',
                 fontsize=14, fontweight='bold')

    # Grid and legend
    ax.grid(True, alpha=0.3, which='both')
    ax.legend(loc='upper right', fontsize=10)

    # Add annotations for the key primes
    for p, b in zip(primes, balance_values):
        color = 'red' if p == min_prime else 'black'
        fontweight = 'bold' if p == min_prime else 'normal'
        ax.annotate(f'{p}', xy=(p, b), xytext=(0, 10),
                    textcoords='offset points', ha='center',
                    fontsize=10, fontweight=fontweight, color=color)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✓ Log-log plot saved to: {output_path}")

    if show:
        plt.show()

    plt.close()


def main():
    """Main entry point for command-line execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Plot Balance Function for P17 Optimality",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-o", "--output",
        default="balance_p17.png",
        help="Output path for main plot (default: balance_p17.png)"
    )
    parser.add_argument(
        "--loglog",
        action="store_true",
        help="Also create a log-log plot"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display plots interactively"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("BALANCE FUNCTION VISUALIZATION")
    print("Adelic-Fractal Equilibrium at p = 17")
    print("=" * 60)

    # Create main plot
    results = create_balance_plot(args.output, args.show)

    # Create log-log plot if requested
    if args.loglog:
        loglog_path = args.output.replace('.png', '_loglog.png')
        create_loglog_plot(loglog_path, args.show)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Minimum found at: p = {results['minimum_prime']}")
    print(f"Minimum balance value: {results['minimum_balance']:.6f}")
    print("\nBalance values:")
    for p, b in zip(results['primes'], results['balance_values']):
        marker = " ← MINIMUM" if p == results['minimum_prime'] else ""
        print(f"  p = {p:2d}: balance = {b:8.3f}{marker}")
    print("=" * 60)


if __name__ == "__main__":
    main()
