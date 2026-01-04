@echo off
echo 🎨 Starting Jarvis Frontend...

cd frontend

:: Check if node_modules exists
if not exist "node_modules\" (
    echo 📦 Installing dependencies...
    call npm install
)

:: Start the frontend
echo 🚀 Starting frontend on http://localhost:5173
echo.
call npm run dev

