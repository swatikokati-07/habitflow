@echo off
echo ========================================
echo HabitFlow Backend Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Creating database...
python -c "from app import app, db; app.app_context().push(); print('Database ready!')"

echo.
echo [3/3] Starting Flask server...
echo.
echo ========================================
echo Server is running at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py
pause
