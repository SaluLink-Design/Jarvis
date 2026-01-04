#!/bin/bash

echo "🎨 Starting Jarvis Frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the frontend
echo "🚀 Starting frontend on http://localhost:5173"
echo ""
npm run dev

