@echo off
ECHO =======================================================
ECHO == Document Detector - Full-Stack Installation (Windows) ==
ECHO =======================================================
ECHO.

REM --- Backend Setup ---
ECHO [1/4] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    ECHO   [ERROR] Python is not found. Please install Python 3.9+ and add it to your PATH.
    exit /b 1
)
ECHO   Python found.

ECHO.
ECHO [2/4] Creating Python virtual environment in '.\venv\'...
python -m venv venv
ECHO   Virtual environment created.

ECHO.
ECHO [3/4] Installing Python dependencies from requirements.txt...
call .\venv\Scripts\pip.exe install -r requirements.txt
ECHO   Python dependencies installed successfully.
ECHO.

REM --- Frontend Setup ---
ECHO [4/4] Installing frontend dependencies...
cd document-processor-frontend
if %errorlevel% neq 0 (
    ECHO   [ERROR] Could not find the 'document-processor-frontend' directory.
    exit /b 1
)

npm install
ECHO   Frontend dependencies installed successfully.
cd ..
ECHO.

ECHO ==================================================
ECHO == ✅ Installation Complete!                     ==
ECHO == Run 'start.bat' to launch the application.  ==
ECHO ==================================================