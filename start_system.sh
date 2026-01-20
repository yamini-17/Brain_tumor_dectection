#!/bin/bash

# Brain Tumor Detection System - Unix/Linux/Mac Startup Script

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "   BRAIN TUMOR DETECTION SYSTEM - COMPLETE STARTUP"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python is not installed"
    echo "Please install Python from https://www.python.org"
    exit 1
fi

echo "✅ Node.js version:"
node --version
echo ""
echo "✅ Python version:"
python3 --version
echo ""

# Setup Frontend
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 1: Installing Frontend Dependencies"
echo "═══════════════════════════════════════════════════════════════"
echo ""
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Frontend installation failed"
    exit 1
fi
echo "✅ Frontend dependencies installed"
echo ""

# Setup Backend
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 2: Installing Backend Dependencies"
echo "═══════════════════════════════════════════════════════════════"
echo ""
cd ../backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Backend installation failed"
    exit 1
fi
echo "✅ Backend dependencies installed"
echo ""

# Start Backend
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 3: Starting Flask Backend Server"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Backend starting on http://localhost:5000"
echo ""
python3 app.py &
BACKEND_PID=$!
sleep 3

# Start Frontend
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 4: Starting React Frontend"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Frontend starting on http://localhost:3000"
echo ""
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
