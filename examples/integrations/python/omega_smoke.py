#!/usr/bin/env python3
"""Minimal local smoke check for the CryoOmega CLI."""
from __future__ import annotations
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
result = subprocess.run([str(ROOT / "bin" / "omega"), "doctor"], cwd=ROOT, check=False)
raise SystemExit(result.returncode)
