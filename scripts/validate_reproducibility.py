#!/usr/bin/env python3
"""
Reproducibility Validation Script

This script validates that the computational environment and results
are reproducible by checking:
1. Python version consistency
2. Dependency versions match ENV.lock
3. Result checksums match expected values
4. Data integrity verification

Usage:
    python scripts/validate_reproducibility.py [--results-dir RESULTS_DIR] [--strict]

Author: QCAL Team
Date: 2025-01-06
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
from typing import Dict, List, Tuple


def get_python_version() -> str:
    """Get the current Python version."""
    return platform.python_version()


def check_python_version(required_versions: List[str] = ["3.11", "3.12"]) -> Tuple[bool, str]:
    """
    Check if Python version matches requirements.
    
    Args:
        required_versions: List of acceptable Python version prefixes
        
    Returns:
        Tuple of (is_valid, version_string)
    """
    current = get_python_version()
    is_valid = any(current.startswith(v) for v in required_versions)
    return is_valid, current


def load_env_lock(path: Path = Path("ENV.lock")) -> Dict[str, str]:
    """
    Parse ENV.lock file to extract package versions.
    
    Args:
        path: Path to ENV.lock file
        
    Returns:
        Dictionary mapping package names to versions
    """
    packages = {}
    
    if not path.exists():
        return packages
    
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse lines like "numpy==1.26.4"
            if '==' in line:
                parts = line.split('==')
                if len(parts) == 2:
                    pkg_name = parts[0].strip()
                    # Extract version, removing any trailing whitespace or comments
                    version = parts[1].split()[0].strip()
                    packages[pkg_name] = version
    
    return packages


def get_installed_packages() -> Dict[str, str]:
    """
    Get currently installed package versions using pip freeze.
    
    Returns:
        Dictionary mapping package names to versions
    """
    packages = {}
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.strip().split('\n'):
            if '==' in line:
                parts = line.split('==')
                if len(parts) == 2:
                    packages[parts[0].strip()] = parts[1].strip()
    
    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze: {e}", file=sys.stderr)
    
    return packages


def verify_dependencies(env_lock_path: Path, strict: bool = False) -> Tuple[bool, List[str]]:
    """
    Verify that installed packages match ENV.lock.
    
    Args:
        env_lock_path: Path to ENV.lock file
        strict: If True, fail on any mismatch
        
    Returns:
        Tuple of (all_match, list_of_mismatches)
    """
    expected = load_env_lock(env_lock_path)
    installed = get_installed_packages()
    
    mismatches = []
    
    for pkg, expected_version in expected.items():
        installed_version = installed.get(pkg)
        
        if installed_version is None:
            mismatches.append(f"Package {pkg} not installed (expected {expected_version})")
        elif installed_version != expected_version:
            mismatches.append(
                f"Version mismatch for {pkg}: "
                f"installed {installed_version}, expected {expected_version}"
            )
    
    all_match = len(mismatches) == 0
    
    return all_match, mismatches


def compute_file_checksum(filepath: Path, algorithm: str = "sha256") -> str:
    """
    Compute checksum of a file.
    
    Args:
        filepath: Path to file
        algorithm: Hash algorithm (sha256, sha512, etc.)
        
    Returns:
        Hex digest of file checksum
    """
    h = hashlib.new(algorithm)
    
    # Read file in 8KB chunks to handle large files efficiently
    # while avoiding excessive memory usage
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    
    return h.hexdigest()


def verify_checksums(
    results_dir: Path,
    checksum_file: Path = None
) -> Tuple[bool, List[str]]:
    """
    Verify checksums of result files.
    
    Args:
        results_dir: Directory containing results
        checksum_file: Path to file containing expected checksums
        
    Returns:
        Tuple of (all_match, list_of_mismatches)
    """
    if checksum_file is None:
        checksum_file = results_dir / "checksums.txt"
    
    if not checksum_file.exists():
        return False, [f"Checksum file not found: {checksum_file}"]
    
    # Resolve results_dir to absolute path for security
    results_dir_abs = results_dir.resolve()
    
    mismatches = []
    
    with open(checksum_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                expected_hash = parts[0]
                # Security: Use pathlib to resolve and validate path
                # Prevent directory traversal attacks
                raw_path = parts[1].lstrip('./')
                filepath = (results_dir / raw_path).resolve()
                
                # Ensure resolved path is within results_dir
                try:
                    filepath.relative_to(results_dir_abs)
                except ValueError:
                    mismatches.append(
                        f"Security: Path outside results directory: {raw_path}"
                    )
                    continue
                
                if not filepath.exists():
                    mismatches.append(f"File not found: {filepath}")
                    continue
                
                actual_hash = compute_file_checksum(filepath)
                
                if actual_hash != expected_hash:
                    mismatches.append(
                        f"Checksum mismatch for {filepath.name}: "
                        f"expected {expected_hash[:16]}..., got {actual_hash[:16]}..."
                    )
    
    all_match = len(mismatches) == 0
    
    return all_match, mismatches


def generate_environment_snapshot() -> Dict:
    """
    Generate a complete snapshot of the computational environment.
    
    Returns:
        Dictionary with environment information
    """
    # Get git info safely
    try:
        git_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_commit = "Not in git repo"
    
    try:
        git_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_branch = "Not in git repo"
    
    return {
        "python_version": get_python_version(),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "git": {
            "commit": git_commit,
            "branch": git_branch,
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate reproducibility of computational environment and results"
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Directory containing results to validate (default: results/)"
    )
    parser.add_argument(
        "--env-lock",
        type=Path,
        default=Path("ENV.lock"),
        help="Path to ENV.lock file (default: ENV.lock)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code on any mismatch"
    )
    parser.add_argument(
        "--generate-snapshot",
        action="store_true",
        help="Generate environment snapshot JSON"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for environment snapshot (default: stdout)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("REPRODUCIBILITY VALIDATION")
    print("=" * 60)
    print()
    
    # Generate environment snapshot if requested
    if args.generate_snapshot:
        snapshot = generate_environment_snapshot()
        snapshot_json = json.dumps(snapshot, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(snapshot_json)
            print(f"✅ Environment snapshot saved to {args.output}")
        else:
            print(snapshot_json)
        
        return 0
    
    all_passed = True
    
    # Check Python version
    print("[1/3] Checking Python version...")
    py_valid, py_version = check_python_version()
    
    if py_valid:
        print(f"  ✅ Python {py_version} (supported)")
    else:
        print(f"  ❌ Python {py_version} (requires 3.11 or 3.12)")
        all_passed = False
    
    print()
    
    # Verify dependencies
    print("[2/3] Verifying dependencies against ENV.lock...")
    
    if not args.env_lock.exists():
        print(f"  ⚠️  ENV.lock not found at {args.env_lock}")
        print("  Skipping dependency verification")
    else:
        deps_match, dep_mismatches = verify_dependencies(args.env_lock, args.strict)
        
        if deps_match:
            print(f"  ✅ All dependencies match ENV.lock")
        else:
            print(f"  ❌ Found {len(dep_mismatches)} dependency mismatches:")
            for mismatch in dep_mismatches[:10]:  # Show first 10
                print(f"     - {mismatch}")
            if len(dep_mismatches) > 10:
                print(f"     ... and {len(dep_mismatches) - 10} more")
            all_passed = False
    
    print()
    
    # Verify result checksums
    print("[3/3] Verifying result checksums...")
    
    if not args.results_dir.exists():
        print(f"  ⚠️  Results directory not found: {args.results_dir}")
        print("  Skipping checksum verification")
    else:
        checksums_match, checksum_mismatches = verify_checksums(args.results_dir)
        
        if checksums_match:
            print(f"  ✅ All result checksums match")
        else:
            print(f"  ❌ Found {len(checksum_mismatches)} checksum mismatches:")
            for mismatch in checksum_mismatches[:10]:
                print(f"     - {mismatch}")
            if len(checksum_mismatches) > 10:
                print(f"     ... and {len(checksum_mismatches) - 10} more")
            all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✅ VALIDATION PASSED: Environment is reproducible")
        print("=" * 60)
        return 0
    else:
        print("❌ VALIDATION FAILED: Reproducibility issues detected")
        print("=" * 60)
        
        if args.strict:
            return 1
        else:
            print()
            print("⚠️  Running in non-strict mode, returning success")
            print("   Use --strict to fail on validation errors")
            return 0


if __name__ == "__main__":
    sys.exit(main())
