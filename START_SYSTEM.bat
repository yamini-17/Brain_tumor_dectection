@echo off
REM Brain Tumor Detection System - Complete Startup Script
REM Starts both backend and frontend

echo.
echo ═══════════════════════════════════════════════════════════════
echo    BRAIN TUMOR DETECTION SYSTEM - COMPLETE STARTUP
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Node.js is not installed
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo ✅ Node.js version:
node --version
echo.
echo ✅ Python version:
python --version
echo.

REM Setup Frontend
echo ═══════════════════════════════════════════════════════════════
echo STEP 1: Installing Frontend Dependencies
echo ═══════════════════════════════════════════════════════════════
echo.
cd /d "%~dp0frontend"
call npm install
if errorlevel 1 (
    echo ❌ Frontend installation failed
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed
echo.

REM Setup Backend
echo ═══════════════════════════════════════════════════════════════
echo STEP 2: Installing Backend Dependencies
echo ═══════════════════════════════════════════════════════════════
echo.
cd /d "%~dp0backend"
echo Installing Python packages...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Backend installation failed
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed
echo.

REM Start Backend
echo ═══════════════════════════════════════════════════════════════
echo STEP 3: Starting Flask Backend Server
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🚀 Backend starting on http://localhost:5000
echo.
start cmd /k "cd /d "%~dp0backend" && python app.py"
timeout /t 3 /nobreak

REM Start Frontend
echo ═══════════════════════════════════════════════════════════════
echo STEP 4: Starting React Frontend
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🚀 Frontend starting on http://localhost:3000
echo.
cd /d "%~dp0frontend"
call npm run dev

pause
