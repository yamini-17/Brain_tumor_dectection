@echo off
REM Frontend Setup Batch File

cd /d c:\Users\91636\Downloads\yolov9\frontend

echo Installing frontend dependencies...
call npm install

if errorlevel 1 (
    echo ❌ npm install failed
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

echo.
echo Starting frontend development server...
echo 🚀 Vite dev server will open at http://localhost:3000
echo.

call npm run dev

pause
