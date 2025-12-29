#!/usr/bin/env python3
"""
Test suite for badge validation script.

Tests that validate_badges.py correctly identifies working and broken badges.

Author: José Manuel Mota Burruezo
License: MIT
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from validate_badges import check_file_exists  # noqa: E402


class TestBadgeValidation(unittest.TestCase):
    """Test badge validation functionality."""

    def test_check_file_exists_valid(self):
        """Test that check_file_exists correctly identifies existing files."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            result = check_file_exists(tmp_path, "Test file")
            self.assertTrue(result, "Should return True for existing file")
        finally:
            os.unlink(tmp_path)

    def test_check_file_exists_invalid(self):
        """Test that check_file_exists correctly identifies missing files."""
        nonexistent = os.path.join(tempfile.gettempdir(), "this_file_definitely_does_not_exist_12345.txt")
        result = check_file_exists(nonexistent, "Nonexistent file")
        self.assertFalse(result, "Should return False for missing file")

    def test_required_files_exist(self):
        """Test that all required files for badges exist."""
        repo_root = Path(__file__).parent.parent

        required_files = [
            "README.md",
            "LICENSE",
            "AI_ACCESSIBILITY.md",
            "notebooks/141hz_validation.ipynb",
            ".github/FUNDING.yml",
            ".github/workflows/analyze.yml",
            ".github/workflows/production-qcal.yml",
            "requirements.txt"
        ]

        for file_path in required_files:
            full_path = repo_root / file_path
            self.assertTrue(
                full_path.exists(),
                f"Required file missing: {file_path}"
            )

    def test_readme_has_badges(self):
        """Test that README.md contains badge definitions."""
        repo_root = Path(__file__).parent.parent
        readme_path = repo_root / "README.md"

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for key badges
        required_badges = [
            "![CI]",
            "![CD]",
            "![License: MIT]",
            "![Python]",
            "[![DOI]",
            "[![GWPy]",
            "[![GitHub Sponsors]",
        ]

        for badge in required_badges:
            self.assertIn(
                badge,
                content,
                f"Badge not found in README: {badge}"
            )

    def test_workflow_files_have_correct_python_version(self):
        """Test that workflow files use Python 3.11."""
        repo_root = Path(__file__).parent.parent

        workflow_files = [
            ".github/workflows/analyze.yml",
            ".github/workflows/production-qcal.yml",
            ".github/workflows/update_coherence_visualization.yml"
        ]

        for wf_file in workflow_files:
            full_path = repo_root / wf_file
            if full_path.exists():
                with open(full_path, 'r') as f:
                    content = f.read()
                    # Accept either:
                    # 1. Explicit python-version: '3.11' specification, or
                    # 2. Matrix-based python-version with '3.11' in the matrix definition
                    uses_explicit = "python-version: '3.11'" in content
                    uses_matrix = ("python-version: ${{ matrix.python-version }}" in content and 
                                   "'3.11'" in content)
                    self.assertTrue(
                        uses_explicit or uses_matrix,
                        f"{wf_file} should use or include Python 3.11"
                    )

    def test_gwpy_version_consistency(self):
        """Test GWPy version consistency between README and requirements."""
        repo_root = Path(__file__).parent.parent

        # Read README
        with open(repo_root / "README.md", 'r') as f:
            readme = f.read()

        # Read requirements.txt
        with open(repo_root / "requirements.txt", 'r') as f:
            requirements = f.read()

        # README should show version range, not specific version
        self.assertIn(
            "GWPy-3.0+",
            readme,
            "README should show GWPy version range (3.0+)"
        )

        # requirements.txt should have gwpy>=3.0.0
        self.assertIn(
            "gwpy>=3.0.0",
            requirements,
            "requirements.txt should specify gwpy>=3.0.0"
        )


def run_tests():
    """Run all tests."""
    # Change to repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)

    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBadgeValidation)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
