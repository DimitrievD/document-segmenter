@echo off
setLOCAL
TITLE App Installation

ECHO =======================================================
ECHO == App Environment Installation (Windows) ==
ECHO =======================================================
ECHO.

ECHO [1/2] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    ECHO [ERROR] Python not found. Please install Python 3.12.3.
    pause
    exit /b 1
)
ECHO Python found.

ECHO.
ECHO [2/2] Creating App virtual environment in '..\venv_app\'...
cd ..
python -m venv venv_app
ECHO Virtual environment created.
ECHO Installing dependencies from app/requirements.txt...
call .\venv_app\Scripts\pip.exe install -r app/requirements.txt
ECHO App dependencies installed successfully.

ECHO.
ECHO ==================================================
ECHO == ✅ Installation Complete!                     ==
ECHO == Run 'start_app.bat' to launch.                ==
ECHO ==================================================
pause
endlocal
