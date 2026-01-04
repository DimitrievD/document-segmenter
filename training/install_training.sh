#!/bin/bash
set -e

echo "=========================================================="
echo "== Training Environment Installation (Linux/macOS) =="
echo "=========================================================="
echo

cd ..

echo "[1/2] Checking for Python 3..."
command -v python3 >/dev/null 2>&1 || { echo "  [ERROR] Python 3 not found." >&2; exit 1; }
echo "  Python 3 found."
echo

echo "[2/2] Creating Training venv in './venv_training/'..."
python3 -m venv venv_training
echo "  Installing dependencies..."
./venv_training/bin/pip install -r training/requirements.txt
echo "  Training dependencies installed successfully."

echo
echo "====================================================="
echo "== ✅ Installation Complete!                       =="
echo "====================================================="
