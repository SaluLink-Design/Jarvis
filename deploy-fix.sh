#!/bin/bash

echo "================================================"
echo "DEPLOYING JARVIS 500 ERROR FIX TO RAILWAY"
echo "================================================"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    echo "   Please run this from your project root directory"
    exit 1
fi

# Add all changes
echo "📦 Adding all changes..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "⚠️  No changes to commit"
    echo "   The fixes might already be deployed"
    echo ""
    echo "Checking Railway deployment status..."
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Fix: Bulletproof error handling - eliminate 500 errors

- Added comprehensive error handling to orchestrator
- API endpoints now return valid JSON on all errors
- Multiple fallback layers ensure system never crashes
- Added /api/test endpoint for health checks
- All modules gracefully handle initialization failures"

    # Push to remote
    echo "🚀 Pushing to remote repository..."
    git push

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully pushed to Git!"
        echo ""
        echo "Railway will automatically detect this push and deploy."
    else
        echo ""
        echo "❌ Failed to push to remote"
        echo "   Please check your git credentials and try again"
        exit 1
    fi
fi

echo ""
echo "================================================"
echo "DEPLOYMENT INITIATED"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Go to Railway dashboard: https://railway.app/"
echo "2. Watch the deployment logs"
echo "3. Wait for 'Jarvis is ready!' message (2-5 minutes)"
echo "4. Test the backend:"
echo "   https://jarvis-production-5709a.up.railway.app/health"
echo ""
echo "Or run the test script:"
echo "   python3 test_backend.py"
echo ""
echo "================================================"
