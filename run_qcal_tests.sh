#!/usr/bin/env bash
# Test runner for QCAL package
# Temporarily renames root qcal to avoid conflicts

set -euo pipefail

cd "$(dirname "$0")"

# Backup root qcal if it exists
if [ -d "qcal" ] && [ ! -d "qcal_llm_backup" ]; then
    echo "Backing up root qcal directory..."
    mv qcal qcal_llm_backup
fi

# Set Python path to include src/
export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"

# Run tests
echo "Running QCAL tests..."
python3 -m pytest tests/test_cli.py tests/test_signal_band_141hz.py tests/test_hashes.py -v

# Restore root qcal
if [ -d "qcal_llm_backup" ]; then
    echo "Restoring root qcal directory..."
    mv qcal_llm_backup qcal
fi

echo "Tests completed!"
