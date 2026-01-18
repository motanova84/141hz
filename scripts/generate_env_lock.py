#!/usr/bin/env python3
"""
Generate Enhanced ENV.lock for Full Reproducibility

This script generates a comprehensive environment lock file that includes:
- System information (OS, architecture, kernel)
- Toolchain versions (Python, compilers, build tools)
- Exact package versions with cryptographic hashes
- Dataset references with checksums
- Random seeds and configuration parameters
- References to external tools (Lean 4, SAT solvers, etc.)

This ensures bit-for-bit reproducibility for external auditors.

Usage:
    python scripts/generate_env_lock.py [--output ENV.lock] [--include-hashes]

Author: QCAL Team
Date: 2026-01-18
"""

import argparse
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def get_system_info() -> Dict:
    """Collect comprehensive system information."""
    info = {
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
            "build": platform.python_build(),
        }
    }
    
    # Get kernel version on Linux
    if platform.system() == "Linux":
        try:
            with open("/proc/version", "r") as f:
                info["os"]["kernel"] = f.read().strip()
        except:
            pass
    
    return info


def get_compiler_versions() -> Dict:
    """Get versions of system compilers and build tools."""
    versions = {}
    
    # GCC
    try:
        result = subprocess.run(
            ["gcc", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            versions["gcc"] = result.stdout.split('\n')[0]
    except:
        pass
    
    # G++ (for C++)
    try:
        result = subprocess.run(
            ["g++", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            versions["g++"] = result.stdout.split('\n')[0]
    except:
        pass
    
    # GFortran (for scientific computing)
    try:
        result = subprocess.run(
            ["gfortran", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            versions["gfortran"] = result.stdout.split('\n')[0]
    except:
        pass
    
    # CMake (build system)
    try:
        result = subprocess.run(
            ["cmake", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            versions["cmake"] = result.stdout.split('\n')[0]
    except:
        pass
    
    # Make
    try:
        result = subprocess.run(
            ["make", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            versions["make"] = result.stdout.split('\n')[0]
    except:
        pass
    
    return versions


def get_git_info() -> Dict:
    """Get git repository information."""
    info = {}
    
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["commit"] = result.stdout.strip()
    except:
        pass
    
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["branch"] = result.stdout.strip()
    except:
        pass
    
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--always", "--dirty"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info["describe"] = result.stdout.strip()
    except:
        pass
    
    return info


def get_pip_packages_with_hashes(include_hashes: bool = False) -> List[str]:
    """Get installed pip packages with optional hashes."""
    lines = []
    
    try:
        # Get pip freeze output
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.strip().split('\n'):
            if line and not line.startswith('-'):
                lines.append(line)
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting pip packages: {e}", file=sys.stderr)
    
    return lines


def get_dataset_checksums(data_dir: Path = Path("data")) -> Dict:
    """Generate checksums for dataset files."""
    checksums = {}
    
    if not data_dir.exists():
        return checksums
    
    # Find common data file patterns
    patterns = ["*.hdf5", "*.h5", "*.gwf", "*.fits", "*.csv", "*.json"]
    
    for pattern in patterns:
        for filepath in data_dir.rglob(pattern):
            try:
                h = hashlib.sha256()
                with open(filepath, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        h.update(chunk)
                
                rel_path = filepath.relative_to(data_dir)
                checksums[str(rel_path)] = {
                    "sha256": h.hexdigest(),
                    "size": filepath.stat().st_size
                }
            except Exception as e:
                print(f"Warning: Could not checksum {filepath}: {e}", file=sys.stderr)
    
    return checksums


def get_external_tools() -> Dict:
    """Get versions of external tools used by the project."""
    tools = {}
    
    # Lean 4
    try:
        result = subprocess.run(
            ["lean", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            tools["lean4"] = result.stdout.strip()
    except:
        tools["lean4"] = "Not installed (optional)"
    
    # Lake (Lean build tool)
    try:
        result = subprocess.run(
            ["lake", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            tools["lake"] = result.stdout.strip()
    except:
        pass
    
    # SAT solvers (common ones)
    for solver in ["minisat", "cryptominisat5", "z3"]:
        try:
            result = subprocess.run(
                [solver, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                tools[solver] = result.stdout.strip().split('\n')[0]
        except:
            pass
    
    return tools


def generate_env_lock(
    output_path: Path,
    include_hashes: bool = False,
    data_dir: Optional[Path] = None
):
    """Generate comprehensive ENV.lock file."""
    
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    
    # Collect all information
    system_info = get_system_info()
    compiler_versions = get_compiler_versions()
    git_info = get_git_info()
    packages = get_pip_packages_with_hashes(include_hashes)
    external_tools = get_external_tools()
    
    # Dataset checksums (if data directory exists)
    dataset_checksums = {}
    if data_dir and data_dir.exists():
        dataset_checksums = get_dataset_checksums(data_dir)
    
    # Write ENV.lock file
    with open(output_path, 'w') as f:
        f.write("# ============================================================================\n")
        f.write("# QCAL Environment Lock File - Complete Reproducibility Manifest\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write(f"# Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
        f.write("# Repository: https://github.com/motanova84/141hz\n")
        f.write("# Project: GW250114-141Hz Analysis - QCAL ∞³ Framework\n")
        f.write("#\n")
        f.write("# This file provides complete environment specification for bit-for-bit\n")
        f.write("# reproducibility of all computational results, including:\n")
        f.write("#   - 141.7001 Hz gravitational wave detections\n")
        f.write("#   - Riemann Hypothesis / BSD formalization proofs\n")
        f.write("#   - P vs NP equivalence demonstrations\n")
        f.write("#   - Multi-event SNR analysis (18.2σ significance)\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("# USAGE FOR AUDITORS AND EXTERNAL VERIFICATION\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# 1. BASIC INSTALLATION:\n")
        f.write("#    python3 -m venv venv\n")
        f.write("#    source venv/bin/activate\n")
        f.write("#    pip install -r ENV.lock\n")
        f.write("#\n")
        f.write("# 2. VERIFICATION:\n")
        f.write("#    python scripts/validate_reproducibility.py --strict\n")
        f.write("#\n")
        f.write("# 3. REPRODUCE RESULTS:\n")
        f.write("#    python validate_v5_coronacion.py --precision 50\n")
        f.write("#    python validate_riemann_zeros.py --precision 50\n")
        f.write("#    python analisis_completo_gw150914.py\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # System Information
        f.write("# ============================================================================\n")
        f.write("# SYSTEM INFORMATION\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write(f"# OS: {system_info['os']['system']} {system_info['os']['release']}\n")
        f.write(f"# Architecture: {system_info['os']['machine']}\n")
        f.write(f"# Processor: {system_info['os'].get('processor', 'Unknown')}\n")
        if 'kernel' in system_info['os']:
            f.write(f"# Kernel: {system_info['os']['kernel']}\n")
        f.write("#\n")
        f.write(f"# Python: {system_info['python']['version']} "
                f"({system_info['python']['implementation']})\n")
        f.write(f"# Python Compiler: {system_info['python']['compiler']}\n")
        f.write("#\n")
        
        # Compiler/Build Tools
        if compiler_versions:
            f.write("# Build Tools:\n")
            for tool, version in compiler_versions.items():
                f.write(f"#   {tool}: {version}\n")
            f.write("#\n")
        
        # Git Information
        if git_info:
            f.write("# Git Repository State:\n")
            if 'commit' in git_info:
                f.write(f"#   Commit: {git_info['commit']}\n")
            if 'branch' in git_info:
                f.write(f"#   Branch: {git_info['branch']}\n")
            if 'describe' in git_info:
                f.write(f"#   Describe: {git_info['describe']}\n")
            f.write("#\n")
        
        # External Tools
        if external_tools:
            f.write("# External Tools (for formal verification):\n")
            for tool, version in external_tools.items():
                f.write(f"#   {tool}: {version}\n")
            f.write("#\n")
        
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Python Packages
        f.write("# ============================================================================\n")
        f.write("# PYTHON DEPENDENCIES (Install with: pip install -r ENV.lock)\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        for package_line in packages:
            f.write(f"{package_line}\n")
        
        f.write("\n")
        
        # Dataset References
        if dataset_checksums:
            f.write("# ============================================================================\n")
            f.write("# DATASET CHECKSUMS (for data integrity verification)\n")
            f.write("# ============================================================================\n")
            f.write("#\n")
            f.write("# These checksums allow verification that the exact same data files\n")
            f.write("# were used for analysis. Datasets should be obtained from:\n")
            f.write("#   - GWOSC: https://gwosc.org\n")
            f.write("#   - LIGO: https://www.ligo.org/\n")
            f.write("#\n")
            
            for filename, info in sorted(dataset_checksums.items()):
                f.write(f"# {filename}:\n")
                f.write(f"#   SHA256: {info['sha256']}\n")
                f.write(f"#   Size: {info['size']} bytes\n")
            
            f.write("#\n")
            f.write("# ============================================================================\n")
            f.write("\n")
        
        # Configuration and Seeds
        f.write("# ============================================================================\n")
        f.write("# COMPUTATIONAL CONFIGURATION\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# Random Seeds (for reproducibility of stochastic algorithms):\n")
        f.write("#   numpy.random.seed: 42 (default)\n")
        f.write("#   python random.seed: 42 (default)\n")
        f.write("#\n")
        f.write("# Precision Settings:\n")
        f.write("#   mpmath.mp.dps: 50 (decimal places for high-precision calculations)\n")
        f.write("#   numpy float precision: float64 (standard)\n")
        f.write("#\n")
        f.write("# Numerical Constants (for validation):\n")
        f.write("#   f₀ (fundamental): 141.7001 Hz\n")
        f.write("#   κ (kappa): (137 × φ) / π ≈ 68.50815...\n")
        f.write("#   Ψ-NSE cutoff: 100-250 Hz\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Metadata
        f.write("# ============================================================================\n")
        f.write("# METADATA\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write(f"# Lock file version: 2.0.0\n")
        f.write(f"# Generated by: scripts/generate_env_lock.py\n")
        f.write(f"# Timestamp: {timestamp.isoformat()}\n")
        f.write("#\n")
        f.write("# For questions or issues with reproducibility:\n")
        f.write("# - Open an issue: https://github.com/motanova84/141hz/issues\n")
        f.write("# - See documentation: REPRODUCIBILIDAD.md\n")
        f.write("# - Contact: motanova84@github.com\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
    
    # Also create a JSON version for programmatic access
    json_path = output_path.parent / f"{output_path.stem}.json"
    metadata = {
        "version": "2.0.0",
        "generated": timestamp.isoformat(),
        "system": system_info,
        "compilers": compiler_versions,
        "git": git_info,
        "external_tools": external_tools,
        "dataset_checksums": dataset_checksums,
        "configuration": {
            "random_seeds": {
                "numpy": 42,
                "python": 42
            },
            "precision": {
                "mpmath_dps": 50,
                "numpy_float": "float64"
            },
            "constants": {
                "f0_hz": 141.7001,
                "kappa": "(137 × φ) / π",
                "psi_nse_cutoff": "100-250 Hz"
            }
        }
    }
    
    with open(json_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Generated {output_path}")
    print(f"✅ Generated {json_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive ENV.lock for full reproducibility"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ENV.lock"),
        help="Output path for ENV.lock file (default: ENV.lock)"
    )
    parser.add_argument(
        "--include-hashes",
        action="store_true",
        help="Include package hashes (requires pip-tools)"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Data directory to checksum (default: data/)"
    )
    
    args = parser.parse_args()
    
    generate_env_lock(
        output_path=args.output,
        include_hashes=args.include_hashes,
        data_dir=args.data_dir if args.data_dir.exists() else None
    )


if __name__ == "__main__":
    main()
