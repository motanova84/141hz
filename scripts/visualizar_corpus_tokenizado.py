#!/usr/bin/env python3
"""
Visualización de Comparativa QCAL vs Sistemas Tradicionales
============================================================

Genera gráficos comparativos de coherencia y densidad ontológica.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import json
import sys
from pathlib import Path


def print_bar_chart(title: str, data: dict, max_width: int = 50):
    """Print a simple ASCII bar chart"""
    print(f"\n{title}")
    print("=" * (max_width + 30))
    
    # Find max value for scaling
    max_val = max(data.values())
    
    for name, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
        # Calculate bar width
        bar_width = int((value / max_val) * max_width)
        bar = "█" * bar_width
        
        # Format value
        if value >= 1000:
            value_str = f"{value:,.0f}"
        else:
            value_str = f"{value:.4f}"
        
        print(f"{name:20s} {bar:50s} {value_str}")


def main():
    """Generate visualizations from comparison data"""
    
    # Load comparison data
    comparison_file = Path("results/corpus_tokenizado_comparison.json")
    
    if not comparison_file.exists():
        print("Error: No se encontró results/corpus_tokenizado_comparison.json")
        print("Ejecuta primero: python scripts/analizar_corpus_tokenizado.py")
        return 1
    
    with open(comparison_file, 'r') as f:
        data = json.load(f)
    
    print("\n" + "=" * 70)
    print("QCAL ∞³ - Visualización de Comparativa")
    print("=" * 70)
    
    # Coherence comparison
    coherence_data = {
        'QCAL ∞³': data['qcal_corpus']['coherence'],
        'Lean4': data['lean4_library']['coherence'],
        'arXiv Math': data['arxiv_math']['coherence'],
        'GPT-4': data['gpt4_pretrain']['coherence']
    }
    
    print_bar_chart("📊 COHERENCIA (Ψ)", coherence_data)
    
    # Density comparison
    density_data = {
        'QCAL ∞³': data['qcal_corpus']['density'],
        'Lean4': data['lean4_library']['density'],
        'arXiv Math': data['arxiv_math']['density'],
        'GPT-4': data['gpt4_pretrain']['density']
    }
    
    print_bar_chart("🏗️  DENSIDAD ONTOLÓGICA (tokens/archivo)", density_data)
    
    # Advantage metrics
    print("\n" + "=" * 70)
    print("✨ VENTAJAS DE QCAL ∞³")
    print("=" * 70)
    
    print(f"\n🎯 Coherencia:  {data['coherence_advantage']:,.1f}x mejor que GPT-4")
    print(f"🎯 Densidad:    {data['density_advantage']:.2f}x mejor que GPT-4")
    
    # Compression methods
    print("\n" + "=" * 70)
    print("⚡ COMPRESIÓN DE TOKENS")
    print("=" * 70)
    
    compression = data['compression_vs_standard']
    for method, ratio in compression.items():
        marker = "✅" if "QCAL" in method else "  "
        print(f"{marker} {method:20s}: {ratio}")
    
    # Impact comparison
    print("\n" + "=" * 70)
    print("💡 IMPACTO COGNITIVO")
    print("=" * 70)
    
    impacts = {
        'QCAL ∞³': data['qcal_corpus']['impact'],
        'GPT-4': data['gpt4_pretrain']['impact'],
        'arXiv Math': data['arxiv_math']['impact'],
        'Lean4': data['lean4_library']['impact']
    }
    
    for system, impact in impacts.items():
        print(f"  {system:20s}: {impact}")
    
    print("\n" + "=" * 70)
    print("CONCLUSIÓN: QCAL ∞³ transforma Big Data en Deep Coherence")
    print("=" * 70)
    
    # Summary table
    print("\n📋 TABLA RESUMEN")
    print("-" * 70)
    print(f"{'Sistema':<20} {'Tokens':>12} {'Coherencia':>12} {'Densidad':>12}")
    print("-" * 70)
    
    systems = ['qcal_corpus', 'gpt4_pretrain', 'arxiv_math', 'lean4_library']
    for sys in systems:
        sys_data = data[sys]
        tokens = sys_data['tokens']
        
        # Format tokens
        if tokens >= 1_000_000_000_000:  # Trillions
            tokens_str = f"{tokens/1_000_000_000_000:.0f}T"
        elif tokens >= 1_000_000_000:  # Billions
            tokens_str = f"{tokens/1_000_000_000:.0f}B"
        elif tokens >= 1_000_000:  # Millions
            tokens_str = f"{tokens/1_000_000:.1f}M"
        else:
            tokens_str = f"{tokens:,}"
        
        print(f"{sys_data['name']:<20} {tokens_str:>12} "
              f"{sys_data['coherence']:>12.6f} {sys_data['density']:>12.1f}")
    
    print("-" * 70)
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
