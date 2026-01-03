import json, subprocess, sys
def test_cli_runs_help():
    out = subprocess.check_output([sys.executable, "-m", "qcal", "--help"])
    assert b"QCAL CLI" in out
