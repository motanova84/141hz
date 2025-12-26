#!/usr/bin/env python3
"""
Security checker script for dependency vulnerabilities.

This script verifies that all dependencies are secure before deployment or testing.
It can be run locally or in CI/CD pipelines.

Usage:
    python3 scripts/check_security.py
    python3 scripts/check_security.py --fail-on-vuln
    python3 scripts/check_security.py --requirements requirements.txt

Exit codes:
    0 - No vulnerabilities found
    1 - Vulnerabilities found (when --fail-on-vuln is used)
    2 - Error running security checks
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_pip_audit(requirements_file=None):
    """
    Run pip-audit to check for vulnerabilities.
    
    Args:
        requirements_file: Path to requirements.txt file
        
    Returns:
        dict: Parsed JSON report from pip-audit
    """
    cmd = ['pip-audit', '--format', 'json', '--desc']
    
    if requirements_file:
        cmd.extend(['-r', requirements_file])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # pip-audit returns non-zero when vulnerabilities are found (expected)
        )
        
        if result.stdout:
            return json.loads(result.stdout)
        else:
            print("⚠️  Warning: pip-audit produced no output", file=sys.stderr)
            return None
            
    except FileNotFoundError:
        print("❌ Error: pip-audit is not installed", file=sys.stderr)
        print("Install it with: pip install pip-audit", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Failed to parse pip-audit output: {e}", file=sys.stderr)
        print(f"Output was: {result.stdout}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error running pip-audit: {e}", file=sys.stderr)
        return None


def analyze_report(report):
    """
    Analyze pip-audit report for vulnerabilities.
    
    Args:
        report: Parsed JSON report from pip-audit
        
    Returns:
        tuple: (has_vulnerabilities: bool, vulnerable_packages: list)
    """
    if not report or 'dependencies' not in report:
        return False, []
    
    vulnerable_packages = []
    
    for dep in report.get('dependencies', []):
        if dep.get('vulns') and len(dep['vulns']) > 0:
            vulnerable_packages.append({
                'name': dep['name'],
                'version': dep['version'],
                'vulns': dep['vulns']
            })
    
    return len(vulnerable_packages) > 0, vulnerable_packages


def print_vulnerability_report(vulnerable_packages):
    """Print a formatted report of vulnerabilities."""
    print("\n" + "="*80)
    print("🔒 SECURITY VULNERABILITY REPORT")
    print("="*80 + "\n")
    
    for pkg in vulnerable_packages:
        print(f"📦 Package: {pkg['name']} (v{pkg['version']})")
        print("-" * 80)
        
        for vuln in pkg['vulns']:
            vuln_id = vuln.get('id', 'Unknown ID')
            description = vuln.get('description', 'No description available')
            fix_versions = vuln.get('fix_versions', [])
            
            print(f"  🔴 {vuln_id}")
            print(f"     Description: {description}")
            
            if fix_versions:
                print(f"     Fix available: {', '.join(fix_versions)}")
            else:
                print("     Fix: No fix version specified")
            
            # Print aliases if available
            if 'aliases' in vuln:
                print(f"     Aliases: {', '.join(vuln['aliases'])}")
            
            print()
        
        print()
    
    print("="*80)
    print(f"Total vulnerable packages: {len(vulnerable_packages)}")
    print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Check dependencies for security vulnerabilities'
    )
    parser.add_argument(
        '--requirements',
        default='requirements.txt',
        help='Path to requirements.txt file (default: requirements.txt)'
    )
    parser.add_argument(
        '--fail-on-vuln',
        action='store_true',
        help='Exit with code 1 if vulnerabilities are found'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    args = parser.parse_args()
    
    # Check if requirements file exists
    req_path = Path(args.requirements)
    if not req_path.exists():
        print(f"❌ Error: Requirements file not found: {args.requirements}", 
              file=sys.stderr)
        return 2
    
    print(f"🔍 Scanning dependencies from {args.requirements}...")
    print()
    
    # Run pip-audit
    report = run_pip_audit(args.requirements)
    
    if report is None:
        print("❌ Failed to run security check", file=sys.stderr)
        return 2
    
    # Analyze report
    has_vulns, vulnerable_packages = analyze_report(report)
    
    if args.json:
        # Output JSON format
        output = {
            'has_vulnerabilities': has_vulns,
            'vulnerable_count': len(vulnerable_packages),
            'packages': vulnerable_packages
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        if has_vulns:
            print_vulnerability_report(vulnerable_packages)
            print("⚠️  ACTION REQUIRED: Please update vulnerable packages\n")
            
            if args.fail_on_vuln:
                return 1
        else:
            print("✅ No vulnerabilities found!")
            print("   All dependencies are secure.\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
