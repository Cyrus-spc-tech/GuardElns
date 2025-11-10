@echo off
echo ========================================
echo GuardELNS - Network Security Dashboard
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create necessary directories
if not exist "data\logs\" mkdir data\logs
if not exist "data\database\" mkdir data\database
if not exist "data\models\" mkdir data\models
echo.

REM Run the application
echo Starting GuardELNS Dashboard...
echo.
echo Dashboard will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause
