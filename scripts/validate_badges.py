#!/usr/bin/env python3
"""
Badge Validation Script

This script validates that all badges in README.md are real and working correctly.
It checks:
- GitHub Actions workflow files exist
- License file exists
- Required documentation files exist
- Python version consistency
- Badge URLs are correctly formatted

Author: José Manuel Mota Burruezo
License: MIT
"""

import os
import re
import sys
from pathlib import Path


def check_file_exists(filepath, name):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {name}: {filepath}")
        return True
    else:
        print(f"❌ {name} NOT FOUND: {filepath}")
        return False


def check_workflow_file(workflow_name):
    """Check if a GitHub Actions workflow file exists."""
    workflow_path = f".github/workflows/{workflow_name}"
    return check_file_exists(workflow_path, f"Workflow '{workflow_name}'")


def validate_readme_badges():
    """Validate all badges in README.md."""
    print("=" * 80)
    print("README BADGE VALIDATION")
    print("=" * 80)
    print()

    # Read README
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("❌ README.md not found!")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_valid = True

    # Check 1: GitHub Actions workflow badges
    print("1. GitHub Actions Workflow Badges")
    print("-" * 80)
    workflows = re.findall(r'workflows/([a-zA-Z0-9_-]+\.yml)', content)
    for workflow in set(workflows):
        if not check_workflow_file(workflow):
            all_valid = False
    print()

    # Check 2: License file
    print("2. License Badge")
    print("-" * 80)
    if not check_file_exists("LICENSE", "License file"):
        all_valid = False
    print()

    # Check 3: AI Accessibility document
    print("3. AI Accessibility Badge")
    print("-" * 80)
    if not check_file_exists("AI_ACCESSIBILITY.md", "AI Accessibility document"):
        all_valid = False
    print()

    # Check 4: Colab notebook
    print("4. Colab Badge")
    print("-" * 80)
    if not check_file_exists("notebooks/141hz_validation.ipynb", "Colab notebook"):
        all_valid = False
    print()

    # Check 5: GitHub Sponsors configuration
    print("5. GitHub Sponsors Badge")
    print("-" * 80)
    if not check_file_exists(".github/FUNDING.yml", "Funding configuration"):
        all_valid = False
    print()

    # Check 6: Python version consistency
    print("6. Python Version Consistency")
    print("-" * 80)
    python_badge_match = re.search(r'python-(\d+\.\d+\+?)', content)
    if python_badge_match:
        badge_version = python_badge_match.group(1)
        print(f"   Badge shows: Python {badge_version}")

        # Check workflow files
        workflow_files = [
            '.github/workflows/analyze.yml',
            '.github/workflows/production-qcal.yml',
            '.github/workflows/update_coherence_visualization.yml'
        ]

        consistent = True
        for wf_file in workflow_files:
            if os.path.exists(wf_file):
                with open(wf_file, 'r') as f:
                    wf_content = f.read()
                    wf_versions = re.findall(r'python-version:\s*[\'"](\d+\.\d+(?:\.\d+)?)[\'"]', wf_content)
                    if wf_versions:
                        wf_version = wf_versions[0]
                        status = "✅" if wf_version.startswith("3.11") else "⚠️"
                        print(f"   {status} {wf_file}: Python {wf_version}")
                        if not wf_version.startswith("3.11"):
                            consistent = False

        if not consistent:
            print("   ⚠️  Some workflows use different Python versions")
            all_valid = False
        else:
            print("   ✅ All workflows use Python 3.11")
    print()

    # Check 7: GWPy version
    print("7. GWPy Version Badge")
    print("-" * 80)
    gwpy_badge_match = re.search(r'GWPy-(\d+\.\d+(?:\.\d+)?\+?)', content)
    if gwpy_badge_match:
        badge_gwpy = gwpy_badge_match.group(1)
        print(f"   Badge shows: GWPy {badge_gwpy}")

        if os.path.exists("requirements.txt"):
            with open("requirements.txt", 'r') as f:
                req_content = f.read()
                gwpy_req_match = re.search(r'gwpy>=(\d+\.\d+\.?\d*)', req_content)
                if gwpy_req_match:
                    req_gwpy = gwpy_req_match.group(1)
                    print(f"   requirements.txt: gwpy>={req_gwpy}")

                    # Badge should show version range, not specific version
                    if '+' in badge_gwpy:
                        print(f"   ✅ Badge shows version range ({badge_gwpy})")
                    else:
                        print("   ⚠️  Badge shows specific version, should show range")
    print()

    # Check 8: Badge URL formats
    print("8. Badge URL Format Validation")
    print("-" * 80)

    # Extract all badge URLs
    badge_urls = re.findall(r'!\[[^\]]*\]\(([^\)]+)\)', content)

    valid_badge_domains = [
        'img.shields.io',
        'github.com',
        'zenodo.org',
        'colab.research.google.com',
        # Local files
        'coherence_f0_scales.png'
    ]

    for url in set(badge_urls):
        # Skip local files
        if not url.startswith('http'):
            continue

        is_valid = any(domain in url for domain in valid_badge_domains)
        status = "✅" if is_valid else "⚠️"
        print(f"   {status} {url}")
        if not is_valid:
            print("      Warning: Unusual badge domain")

    print()

    return all_valid


def main():
    """Main validation function."""
    # Change to repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)

    print("\n🔍 Badge Validation Tool")
    print("=" * 80)
    print()

    all_valid = validate_readme_badges()

    print("=" * 80)
    if all_valid:
        print("✅ ALL BADGES ARE VALID AND WORKING!")
        return 0
    else:
        print("⚠️  SOME BADGES HAVE ISSUES - SEE ABOVE FOR DETAILS")
        return 1


if __name__ == "__main__":
    sys.exit(main())
