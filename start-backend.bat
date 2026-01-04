@echo off
echo 🤖 Starting Jarvis Backend...

cd backend

:: Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if requirements are installed
if not exist "venv\.requirements_installed" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.requirements_installed
)

:: Check for .env file
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit backend\.env and add your OPENAI_API_KEY
    echo    (Optional but recommended for better NLP)
    echo.
)

:: Start the backend
echo 🚀 Starting backend server on http://localhost:8000
echo.
python main.py

