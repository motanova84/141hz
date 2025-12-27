#!/usr/bin/env python3
"""
Generate Badges for README

Generates status badges for the project
"""

import json
from pathlib import Path
from datetime import datetime

def generate_badge_url(label: str, message: str, color: str) -> str:
    """
    Generate shields.io badge URL
    
    Args:
        label: Badge label
        message: Badge message
        color: Badge color
    
    Returns:
        Badge markdown
    """
    base_url = "https://img.shields.io/badge"
    url = f"{base_url}/{label}-{message}-{color}"
    return f"![{label}]({url})"

def main():
    """Generate badges"""
    print("Generating project badges...")
    
    badges = {
        "frequency": generate_badge_url("frequency", "141.7001_Hz", "blue"),
        "coherence": generate_badge_url("coherence", "validated", "success"),
        "lean4": generate_badge_url("Lean_4", "formalized", "purple"),
        "python": generate_badge_url("python", "3.8+", "blue"),
        "javascript": generate_badge_url("javascript", "ES2020", "yellow"),
        "license": generate_badge_url("license", "MIT", "green"),
        "doi": "[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17379721.svg)](https://doi.org/10.5281/zenodo.17379721)"
    }
    
    # Generate badges markdown
    badges_md = "## Project Badges\n\n"
    for name, badge in badges.items():
        badges_md += f"{badge} "
    
    # Save to file
    output_path = Path(__file__).parent.parent.parent / "Benchmarks" / "Results" / "badges.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(badges_md)
    
    print(f"✅ Badges generated: {output_path}")
    print("\nBadges:")
    print(badges_md)

if __name__ == "__main__":
    main()
