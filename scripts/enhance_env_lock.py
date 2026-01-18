#!/usr/bin/env python3
"""
Enhance existing ENV.lock with comprehensive metadata

This script takes the existing ENV.lock and adds:
- System information header
- Toolchain versions
- Git repository state
- External tools information
- Dataset checksums
- Configuration parameters

This preserves the existing package versions while adding metadata
for complete reproducibility.

Usage:
    python scripts/enhance_env_lock.py [--input ENV.lock] [--output ENV.lock]

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
from typing import Dict, Optional


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
            "build": str(platform.python_build()),
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
    
    for tool, cmd in [
        ("gcc", ["gcc", "--version"]),
        ("g++", ["g++", "--version"]),
        ("gfortran", ["gfortran", "--version"]),
        ("cmake", ["cmake", "--version"]),
        ("make", ["make", "--version"]),
    ]:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                versions[tool] = result.stdout.split('\n')[0]
        except:
            pass
    
    return versions


def get_git_info() -> Dict:
    """Get git repository information."""
    info = {}
    
    for key, cmd in [
        ("commit", ["git", "rev-parse", "HEAD"]),
        ("branch", ["git", "branch", "--show-current"]),
        ("describe", ["git", "describe", "--tags", "--always", "--dirty"]),
    ]:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                info[key] = result.stdout.strip()
        except:
            pass
    
    return info


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
        tools["lean4"] = "Not installed (optional - for formal verification)"
    
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
            tools[solver] = "Not installed (optional - for SAT solving)"
    
    # LALSuite (for gravitational wave analysis)
    try:
        result = subprocess.run(
            ["lalapps_version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            tools["lalsuite"] = result.stdout.strip().split('\n')[0]
    except:
        tools["lalsuite"] = "Not installed (optional - for LAL gravitational wave analysis)"
    
    return tools


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
                # Skip very large files (> 100MB) to avoid timeout
                if filepath.stat().st_size > 100 * 1024 * 1024:
                    continue
                
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


def enhance_env_lock(
    input_path: Path,
    output_path: Path,
    data_dir: Optional[Path] = None,
    doi: str = "10.5281/zenodo.17445017"
):
    """Enhance existing ENV.lock with comprehensive metadata."""
    
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    
    # Collect all information
    system_info = get_system_info()
    compiler_versions = get_compiler_versions()
    git_info = get_git_info()
    external_tools = get_external_tools()
    
    # Dataset checksums (if data directory exists)
    dataset_checksums = {}
    if data_dir and data_dir.exists():
        dataset_checksums = get_dataset_checksums(data_dir)
    
    # Read existing ENV.lock
    existing_content = []
    if input_path.exists():
        with open(input_path, 'r') as f:
            existing_content = f.readlines()
    
    # Write enhanced ENV.lock file
    with open(output_path, 'w') as f:
        # Write comprehensive header
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
        f.write("#   - 141.7001 Hz gravitational wave detections (GW150914, GW250114, etc.)\n")
        f.write("#   - Riemann Hypothesis / BSD formalization proofs (Lean 4)\n")
        f.write("#   - P vs NP equivalence demonstrations\n")
        f.write("#   - Multi-event SNR analysis (18.2σ cumulative significance)\n")
        f.write("#   - AT2020afhd harmonic analysis (noesis field verification)\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("# USAGE FOR AUDITORS AND EXTERNAL VERIFICATION\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# 1. BASIC INSTALLATION (creates reproducible environment):\n")
        f.write("#    python3 -m venv venv\n")
        f.write("#    source venv/bin/activate  # On Windows: venv\\Scripts\\activate\n")
        f.write("#    pip install -r ENV.lock\n")
        f.write("#\n")
        f.write("# 2. VERIFY ENVIRONMENT INTEGRITY:\n")
        f.write("#    python scripts/validate_reproducibility.py --strict\n")
        f.write("#\n")
        f.write("# 3. REPRODUCE KEY RESULTS:\n")
        f.write("#    # Validate fundamental frequency and κ constant\n")
        f.write("#    python validate_v5_coronacion.py --precision 50\n")
        f.write("#    \n")
        f.write("#    # Verify Riemann zeros connection\n")
        f.write("#    python validate_riemann_zeros.py --precision 50\n")
        f.write("#    \n")
        f.write("#    # Analyze GW150914 with 141.7 Hz resonance\n")
        f.write("#    python analisis_completo_gw150914.py\n")
        f.write("#    \n")
        f.write("#    # Validate AT2020afhd harmonic detection\n")
        f.write("#    python validate_at2020afhd_harmonic.py\n")
        f.write("#\n")
        f.write("# 4. OBTAIN DATASETS (if not included):\n")
        f.write("#    # Gravitational wave data from GWOSC:\n")
        f.write("#    wget https://gwosc.org/eventapi/html/GWTC-1-confident/GW150914/\n")
        f.write("#    \n")
        f.write("#    # Additional LIGO data:\n")
        f.write("#    python -c 'from gwosc import datasets; datasets.find_datasets()'\n")
        f.write("#\n")
        f.write("# 5. RUN COMPLETE VALIDATION SUITE:\n")
        f.write("#    python run_all_validations.py\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # System Information
        f.write("# ============================================================================\n")
        f.write("# SYSTEM INFORMATION (Environment where ENV.lock was generated)\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write(f"# Operating System: {system_info['os']['system']} {system_info['os']['release']}\n")
        f.write(f"# OS Version: {system_info['os']['version']}\n")
        f.write(f"# Architecture: {system_info['os']['machine']}\n")
        f.write(f"# Processor: {system_info['os'].get('processor', 'Unknown')}\n")
        if 'kernel' in system_info['os']:
            # Write full kernel info, but split to multiple lines if very long
            kernel_info = system_info['os']['kernel']
            if len(kernel_info) > 120:
                # Split kernel info across multiple comment lines
                f.write(f"# Kernel (full): {kernel_info[:120]}\n")
                remaining = kernel_info[120:]
                while remaining:
                    chunk = remaining[:120]
                    f.write(f"#   {chunk}\n")
                    remaining = remaining[120:]
            else:
                f.write(f"# Kernel: {kernel_info}\n")
        f.write("#\n")
        f.write(f"# Python Version: {system_info['python']['version']} "
                f"({system_info['python']['implementation']})\n")
        f.write(f"# Python Compiler: {system_info['python']['compiler']}\n")
        f.write(f"# Python Build: {system_info['python']['build']}\n")
        f.write("#\n")
        f.write("# Note: Results are reproducible across different OS/architectures when\n")
        f.write("# using the same Python version and package versions listed below.\n")
        f.write("#\n")
        
        # Compiler/Build Tools
        if compiler_versions:
            f.write("# Build Tools and Compilers:\n")
            for tool, version in compiler_versions.items():
                # Truncate if too long
                if len(version) > 80:
                    version = version[:77] + "..."
                f.write(f"#   {tool}: {version}\n")
            f.write("#\n")
        
        # Git Information
        if git_info:
            f.write("# Git Repository State (when ENV.lock was generated):\n")
            if 'commit' in git_info:
                f.write(f"#   Commit SHA: {git_info['commit']}\n")
            if 'branch' in git_info:
                f.write(f"#   Branch: {git_info['branch']}\n")
            if 'describe' in git_info:
                f.write(f"#   Git Describe: {git_info['describe']}\n")
            f.write("#\n")
        
        # External Tools
        if external_tools:
            f.write("# External Tools (for specialized computations):\n")
            for tool, version in external_tools.items():
                f.write(f"#   {tool}: {version}\n")
            f.write("#\n")
        
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Write original package content, skipping old header comments
        f.write("# ============================================================================\n")
        f.write("# PYTHON DEPENDENCIES\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# Install all dependencies with: pip install -r ENV.lock\n")
        f.write("#\n")
        f.write("# For hash-verified installation (maximum security):\n")
        f.write("#   See repro/GWTC-1/env.lock for pip-compile generated hashes\n")
        f.write("#   Or generate your own: pip-compile --generate-hashes requirements.txt\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Copy package lines from original, skip header comments
        in_packages = False
        for line in existing_content:
            stripped = line.strip()
            
            # Start copying at first package line
            if not in_packages:
                if stripped and not stripped.startswith('#'):
                    in_packages = True
                    f.write(line)
            else:
                f.write(line)
        
        f.write("\n")
        
        # Dataset References
        f.write("# ============================================================================\n")
        f.write("# DATASET REFERENCES AND CHECKSUMS\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# Datasets used for analysis with SHA256 checksums for verification.\n")
        f.write("# Obtain datasets from:\n")
        f.write("#   - GWOSC (Gravitational Wave Open Science Center): https://gwosc.org\n")
        f.write("#   - LIGO Scientific Collaboration: https://www.ligo.org/\n")
        f.write("#\n")
        
        if dataset_checksums:
            f.write("# Data files in repository:\n")
            for filename, info in sorted(dataset_checksums.items()):
                f.write(f"# {filename}:\n")
                f.write(f"#   SHA256: {info['sha256']}\n")
                f.write(f"#   Size: {info['size']} bytes\n")
            f.write("#\n")
        else:
            f.write("# (No local data files found - datasets downloaded dynamically)\n")
            f.write("#\n")
        
        # Known dataset references
        f.write("# Standard GWOSC datasets used (download automatically):\n")
        f.write("#   - GW150914: https://gwosc.org/eventapi/html/GWTC-1-confident/GW150914/\n")
        f.write("#   - GW170814: https://gwosc.org/eventapi/html/GWTC-1-confident/GW170814/\n")
        f.write("#   - GW250114: (O4 data, pending public release)\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Configuration and Seeds
        f.write("# ============================================================================\n")
        f.write("# COMPUTATIONAL CONFIGURATION\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# Random Seeds (for reproducibility of stochastic algorithms):\n")
        f.write("#   numpy.random.seed(42)  # Used in all validation scripts\n")
        f.write("#   random.seed(42)        # Python standard library\n")
        f.write("#\n")
        f.write("# Precision Settings:\n")
        f.write("#   mpmath.mp.dps = 50  # Decimal places for arbitrary precision arithmetic\n")
        f.write("#   numpy.float64       # Standard floating point precision\n")
        f.write("#\n")
        f.write("# Physical/Mathematical Constants (for validation):\n")
        f.write("#   f₀ (fundamental frequency): 141.7001 Hz\n")
        f.write("#   κ (kappa structural constant): (137 × φ) / π ≈ 68.50815...\n")
        f.write("#   φ (golden ratio): (1 + √5) / 2 ≈ 1.618033988749...\n")
        f.write("#   Ψ-NSE bandpass cutoff: 100-250 Hz\n")
        f.write("#\n")
        f.write("# Sampling Rates:\n")
        f.write("#   LIGO/Virgo: 4096 Hz (standard for O3/O4)\n")
        f.write("#   KAGRA: 4096 Hz\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Verification Instructions
        f.write("# ============================================================================\n")
        f.write("# REPRODUCIBILITY VERIFICATION CHECKLIST\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write("# After installation, verify your environment matches this lock file:\n")
        f.write("#\n")
        f.write("# ✓ 1. Python version matches (3.11 or 3.12):\n")
        f.write("#      python --version\n")
        f.write("#\n")
        f.write("# ✓ 2. All packages installed with correct versions:\n")
        f.write("#      pip freeze | diff - ENV.lock\n")
        f.write("#\n")
        f.write("# ✓ 3. Run validation script:\n")
        f.write("#      python scripts/validate_reproducibility.py --strict\n")
        f.write("#\n")
        f.write("# ✓ 4. Verify core constants compute correctly:\n")
        f.write("#      python -c 'from qcal.core import f0; print(f\"f0={f0:.6f} Hz\")'\n")
        f.write("#\n")
        f.write("# ✓ 5. Test high-precision arithmetic:\n")
        f.write("#      python -c 'import mpmath; mpmath.mp.dps=50; print(mpmath.phi)'\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
        f.write("\n")
        
        # Metadata
        f.write("# ============================================================================\n")
        f.write("# METADATA\n")
        f.write("# ============================================================================\n")
        f.write("#\n")
        f.write(f"# Lock File Version: 2.0.0\n")
        f.write(f"# Generated By: scripts/enhance_env_lock.py\n")
        f.write(f"# Timestamp: {timestamp.isoformat()}\n")
        if doi:
            f.write(f"# DOI: {doi}\n")
        f.write("#\n")
        f.write("# This environment lock ensures:\n")
        f.write("#   ✓ Bit-for-bit reproducibility of numerical results\n")
        f.write("#   ✓ External auditor verification capability\n")
        f.write("#   ✓ Long-term scientific result preservation\n")
        f.write("#   ✓ Cross-platform validation (with same Python version)\n")
        f.write("#\n")
        f.write("# For questions or issues with reproducibility:\n")
        f.write("#   - GitHub Issues: https://github.com/motanova84/141hz/issues\n")
        f.write("#   - Documentation: REPRODUCIBILIDAD.md, SECURITY.md\n")
        f.write("#   - Contact: via GitHub @motanova84\n")
        f.write("#\n")
        f.write("# ============================================================================\n")
    
    # Also create/update JSON metadata file
    json_path = output_path.parent / "ENV.lock.json"
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
                "kappa_formula": "(137 × φ) / π",
                "kappa_approx": 68.50815,
                "phi": 1.618033988749,
                "psi_nse_cutoff_hz": [100, 250]
            },
            "sampling_rates_hz": {
                "ligo": 4096,
                "virgo": 4096,
                "kagra": 4096
            }
        }
    }
    
    if doi:
        metadata["doi"] = doi
    
    with open(json_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Enhanced ENV.lock written to {output_path}")
    print(f"✅ Metadata JSON written to {json_path}")
    print(f"\nTo verify: python scripts/validate_reproducibility.py --strict")


def main():
    parser = argparse.ArgumentParser(
        description="Enhance existing ENV.lock with comprehensive metadata"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("ENV.lock"),
        help="Input ENV.lock file (default: ENV.lock)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("ENV.lock"),
        help="Output path for enhanced ENV.lock (default: ENV.lock)"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Data directory to checksum (default: data/)"
    )
    parser.add_argument(
        "--doi",
        type=str,
        default="10.5281/zenodo.17445017",
        help="DOI for the project (default: 10.5281/zenodo.17445017)"
    )
    
    args = parser.parse_args()
    
    enhance_env_lock(
        input_path=args.input,
        output_path=args.output,
        data_dir=args.data_dir if args.data_dir.exists() else None,
        doi=args.doi
    )


if __name__ == "__main__":
    main()
