@echo off
setLOCAL
TITLE Training Installation

ECHO =======================================================
ECHO == Training Environment Installation (Windows) ==
ECHO =======================================================
ECHO.

ECHO [1/2] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    ECHO [ERROR] Python not found.
    pause
    exit /b 1
)
ECHO Python found.

ECHO.
ECHO [2/2] Creating Training venv in '..\venv_training\'...
cd ..
python -m venv venv_training
ECHO Virtual environment created.
ECHO Installing dependencies from training/requirements.txt...
call .\venv_training\Scripts\pip.exe install -r training/requirements.txt
ECHO Training dependencies installed successfully.

ECHO.
ECHO ==================================================
ECHO == ✅ Installation Complete!                     ==
ECHO ==================================================
pause
endlocal
