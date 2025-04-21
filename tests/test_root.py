import os, sys, json
from pathlib import Path

# Ensure project root is in path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from core.find_aimo_root import find_aimo_root

def test_find_aimo_root():
    root = find_aimo_root()
    # Root directory must contain launch.py as basic sanity
    assert (root / 'launch.py').exists(), "launch.py not found at project root"

