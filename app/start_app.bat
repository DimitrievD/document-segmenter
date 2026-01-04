@echo off
setLOCAL
TITLE App Startup

ECHO ==============================================
ECHO == Starting Document Detector App...        ==
ECHO ==============================================
ECHO.

cd ..

ECHO -> Starting Flask API Backend...
START "Flask Backend API" cmd /k "venv_app\Scripts\activate.bat && echo Backend activated. Starting server... && python app/app.py"

ECHO -> Starting React Frontend...
START "React Frontend" cmd /k "cd document-processor-frontend && npm start"

ECHO.
ECHO Two new terminal windows have been opened.
ECHO Frontend: http://localhost:3000
ECHO Backend: http://localhost:5000
ECHO.
ECHO To stop, close both new windows.
endlocal
