@echo off
echo ================================================
echo DEPLOYING JARVIS 500 ERROR FIX TO RAILWAY
echo ================================================
echo.

REM Check if we're in a git repository
if not exist ".git" (
    echo ERROR: Not a git repository
    echo Please run this from your project root directory
    pause
    exit /b 1
)

REM Add all changes
echo Adding all changes...
git add .

REM Check if there are changes to commit
git diff --cached --quiet
if %errorlevel% equ 0 (
    echo No changes to commit
    echo The fixes might already be deployed
    echo.
    echo Checking Railway deployment status...
) else (
    REM Commit changes
    echo Committing changes...
    git commit -m "Fix: Bulletproof error handling - eliminate 500 errors"

    REM Push to remote
    echo Pushing to remote repository...
    git push

    if %errorlevel% equ 0 (
        echo.
        echo Successfully pushed to Git!
        echo.
        echo Railway will automatically detect this push and deploy.
    ) else (
        echo.
        echo Failed to push to remote
        echo Please check your git credentials and try again
        pause
        exit /b 1
    )
)

echo.
echo ================================================
echo DEPLOYMENT INITIATED
echo ================================================
echo.
echo Next steps:
echo 1. Go to Railway dashboard: https://railway.app/
echo 2. Watch the deployment logs
echo 3. Wait for 'Jarvis is ready!' message (2-5 minutes)
echo 4. Test the backend:
echo    https://jarvis-production-5709a.up.railway.app/health
echo.
echo Or run the test script:
echo    python test_backend.py
echo.
echo ================================================
echo.
pause
