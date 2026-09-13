"""CLI doctor exit code."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_doctor_cli_exit_zero_soft_ok():
    r = subprocess.run(
        [sys.executable, str(ROOT / "bin" / "omega"), "doctor"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}),
             "PYTHONPATH": str(ROOT / "lib")},
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "Doctor:" in r.stdout
