@echo off
ECHO ==============================================
ECHO == Starting Document Detector Application...  ==
ECHO ==============================================
ECHO.
ECHO -> Starting Flask API Backend in a new window...
START "Flask Backend API" cmd /k "venv\Scripts\activate.bat && echo Backend activated. Starting server... && python app.py"

ECHO -> Starting React Frontend in a new window...
START "React Frontend" cmd /k "cd document-processor-frontend && npm start"

ECHO.
ECHO Two new terminal windows have been opened.
ECHO Frontend will be available at http://localhost:3000
ECHO To stop the application, simply close both new windows.