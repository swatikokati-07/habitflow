@echo off
REM HabitFlow Database Management Script
REM This script provides easy access to database commands

setlocal enabledelayedexpansion

if "%1"=="" (
    echo.
    echo ========================================
    echo HabitFlow Database Manager
    echo ========================================
    echo.
    echo Available commands:
    echo   db.bat init      - Initialize the database
    echo   db.bat seed      - Seed with sample data
    echo   db.bat reset     - Reset database (delete all data^)
    echo   db.bat info      - Show database statistics
    echo   db.bat export    - Export data to JSON backup
    echo   db.bat clear     - Clear all data
    echo.
    exit /b 0
)

if "%1"=="init" (
    echo Initializing database...
    python database.py init
    exit /b 0
)

if "%1"=="seed" (
    echo Seeding database with sample data...
    python database.py seed
    exit /b 0
)

if "%1"=="reset" (
    echo WARNING: This will delete all data!
    set /p confirm="Continue? (yes/no): "
    if /i "!confirm!"=="yes" (
        python database.py reset
    ) else (
        echo Cancelled.
    )
    exit /b 0
)

if "%1"=="info" (
    echo Getting database information...
    python database.py info
    exit /b 0
)

if "%1"=="export" (
    if "%2"=="" (
        echo Exporting to backup.json...
        python database.py export backup.json
    ) else (
        echo Exporting to %2...
        python database.py export %2
    )
    exit /b 0
)

if "%1"=="clear" (
    echo WARNING: This will delete data!
    set /p confirm="Continue? (yes/no): "
    if /i "!confirm!"=="yes" (
        if "%2"=="" (
            python database.py clear
        ) else (
            python database.py clear %2
        )
    ) else (
        echo Cancelled.
    )
    exit /b 0
)

echo Unknown command: %1
echo Run 'db.bat' with no arguments to see available commands.
exit /b 1
