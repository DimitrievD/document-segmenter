@echo off
setLOCAL
TITLE Training Startup

ECHO ==============================================
ECHO == Starting Training Environment...        ==
ECHO ==============================================
ECHO.

cd ..

ECHO -> Activating Training Environment...
cmd /k "venv_training\Scripts\activate.bat && cd training && echo Training environment ready. You can run train_segmentation.py now."

endlocal
