"""
conftest.py for Tests/ directory

Ensures the repository root is on sys.path so that local packages
(e.g. qcal) can be imported without requiring installation.
"""

import sys
from pathlib import Path

# Add the repository root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
