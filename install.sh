#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

echo "=========================================================="
echo "== Document Detector - Full-Stack Installation (Linux/macOS) =="
echo "=========================================================="
echo

# --- Backend Setup ---
echo "[1/4] Checking for Python 3..."
command -v python3 >/dev/null 2>&1 || { echo "  [ERROR] Python 3 is not found. Please install it." >&2; exit 1; }
echo "  Python 3 found."
echo

echo "[2/4] Creating Python virtual environment in './venv/'..."
python3 -m venv venv
echo "  Virtual environment created."
echo

echo "[3/4] Installing Python dependencies from requirements.txt..."
./venv/bin/pip install -r requirements.txt
echo "  Python dependencies installed successfully."
echo

# --- Frontend Setup ---
echo "[4/4] Installing frontend dependencies..."
if [ ! -d "document-processor-frontend" ]; then
    echo "  [ERROR] Could not find the 'document-processor-frontend' directory." >&2; exit 1;
fi
cd document-processor-frontend
npm install
cd ..
echo "  Frontend dependencies installed successfully."
echo

echo "====================================================="
echo "== ✅ Installation Complete!                       =="
echo "== Run './start.sh' to launch the application.    =="
echo "====================================================="