#!/usr/bin/env python3
"""Launch MCP test server (8506) and Streamlit dashboard (8505) in parallel."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env.setdefault("QCAL_REAL_TESTS", "1")

    mcp_cmd = [sys.executable, str(repo_root / "tests" / "mcp_test_server.py")]
    ui_cmd = [
        "streamlit",
        "run",
        str(repo_root / "app.py"),
        "--server.port",
        "8505",
        "--server.address",
        "127.0.0.1",
    ]

    print("🚀 Iniciando MCP Test Server en 8506...")
    mcp_proc = subprocess.Popen(mcp_cmd, cwd=str(repo_root), env=env)

    print("🚀 Iniciando Streamlit Dashboard en 8505...")
    ui_proc = subprocess.Popen(ui_cmd, cwd=str(repo_root), env=env)

    print("✅ Stack activo: MCP(8506) + Dashboard(8505)")
    print("Presiona Ctrl+C para detener ambos procesos")

    try:
        mcp_proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proc in (ui_proc, mcp_proc):
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
        for proc in (ui_proc, mcp_proc):
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
