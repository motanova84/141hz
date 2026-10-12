"""Regression coverage for dependencies used by alternative validations."""

from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


def test_requirements_declares_pywavelets():
    """Wavelet validation's unconditional pywt import must be installable."""
    requirements_path = Path(__file__).resolve().parents[1] / "requirements.txt"
    requirements = [
        Requirement(line.strip())
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]

    assert any(canonicalize_name(requirement.name) == "pywavelets" for requirement in requirements)
