#!/usr/bin/env python3
"""
Generate Metrics Report

Generates comprehensive metrics for the QC-LLM project
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add API to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "API" / "Python"))

from qc_llm import F0

def count_files(directory: Path, pattern: str) -> int:
    """Count files matching pattern"""
    return len(list(directory.rglob(pattern)))

def generate_metrics():
    """Generate project metrics"""
    root = Path(__file__).parent.parent.parent
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "frequency": {
            "f0": F0,
            "unit": "Hz",
            "derivation": "sqrt(2) × f_ref where f_ref = |ζ'(1/2)| × φ³"
        },
        "implementation": {
            "python_files": count_files(root / "API" / "Python", "*.py"),
            "javascript_files": count_files(root / "API" / "JavaScript", "*.ts"),
            "lean_files": count_files(root / "Core", "*.lean"),
            "examples": count_files(root / "Examples", "*.py") + 
                       count_files(root / "Examples", "*.js"),
            "benchmarks": count_files(root / "Benchmarks", "*.py")
        },
        "modules": {
            "Core": [
                "FrequencyDerivation",
                "DimensionalAnalysis",
                "PrimeDistribution"
            ],
            "Applications": [
                "LLM",
                "Physics",
                "Neuroscience"
            ],
            "API": [
                "REST (FastAPI)",
                "Python Package",
                "JavaScript Package"
            ]
        },
        "documentation": {
            "tutorials": count_files(root / "Documentation" / "Tutorials", "*.md"),
            "theory": count_files(root / "Documentation" / "Theory", "*.md"),
            "api_docs": count_files(root / "Documentation" / "API", "*.md")
        }
    }
    
    return metrics

def main():
    """Generate and save metrics"""
    print("Generating project metrics...")
    
    metrics = generate_metrics()
    
    # Save to JSON
    output_path = Path(__file__).parent.parent.parent / "Benchmarks" / "Results" / "metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(metrics, indent=2))
    
    print(f"✅ Metrics generated: {output_path}")
    print("\nMetrics Summary:")
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
