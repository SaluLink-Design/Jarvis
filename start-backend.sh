#!/bin/bash

echo "🤖 Starting Jarvis Backend..."

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.requirements_installed
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
    echo "   (Optional but recommended for better NLP)"
    echo ""
fi

# Start the backend
echo "🚀 Starting backend server on http://localhost:8000"
echo ""
python main.py

