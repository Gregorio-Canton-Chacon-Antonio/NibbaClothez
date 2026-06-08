#!/usr/bin/env python3
"""
Wrapper script to run the project's seed code from the repository root.
Usage:
  python seed_data.py
  ./seed_data.py  (on systems that support direct execution)
This imports and runs `src.database.seed_data.main()` so paths resolve correctly.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.database.seed_data import main
except Exception as e:
    print("ERROR: no se pudo importar src.database.seed_data:", e)
    raise


if __name__ == "__main__":
    main()
