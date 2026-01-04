#!/bin/bash
set -e

echo "=========================================================="
echo "== App Environment Installation (Linux/macOS) =="
echo "=========================================================="
echo

cd ..

echo "[1/2] Checking for Python 3..."
command -v python3 >/dev/null 2>&1 || { echo "  [ERROR] Python 3 not found." >&2; exit 1; }
echo "  Python 3 found."
echo

echo "[2/2] Creating App venv in './venv_app/'..."
python3 -m venv venv_app
echo "  Installing dependencies..."
./venv_app/bin/pip install -r app/requirements.txt
echo "  App dependencies installed successfully."

echo
echo "====================================================="
echo "== ✅ Installation Complete!                       =="
echo "== Run './start_app.sh' to launch.                =="
echo "====================================================="
