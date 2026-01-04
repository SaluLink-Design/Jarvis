# Deploying to Railway

## Backend Deployment

Your backend is configured for Railway deployment. Here's what you need to do:

### 1. Update Your Railway Deployment

Since I've made changes to fix the 500 error, you need to redeploy:

```bash
# In the backend directory
git add .
git commit -m "Fix: Improved error handling and reduced dependencies"
git push
```

Railway will automatically detect the changes and redeploy.

### 2. Files Used for Railway Deployment

- **`Procfile`** - Tells Railway how to start the server
- **`requirements-railway.txt`** - Lightweight dependencies (removed heavy ML libs)
- **`runtime.txt`** - Specifies Python version

### 3. Changes Made to Fix the 500 Error

1. **Removed heavy dependencies** from `requirements-railway.txt`:
   - Removed PyTorch, transformers, accelerate, diffusers
   - These were causing deployment failures and timeouts

2. **Added robust error handling**:
   - Each module now initializes with try-catch blocks
   - Backend continues to run even if individual modules fail
   - Better logging for debugging

3. **Fixed CORS configuration**:
   - Automatically detects Railway environment
   - Allows all origins in production

### 4. Check Deployment Status

After redeploying, check:

1. **Health endpoint**: `https://jarvis-production-5709a.up.railway.app/health`
   - Should show module status

2. **API health**: `https://jarvis-production-5709a.up.railway.app/api/health`
   - Same as above but under /api prefix

### 5. Environment Variables (Optional)

If you want to use OpenAI for better NLP:
- Set `OPENAI_API_KEY` in Railway dashboard
- Without it, the system uses rule-based NLP (still works fine)

## Frontend Configuration

Your frontend is already configured correctly in `.env.production`:
```
VITE_BACKEND_URL=https://jarvis-production-5709a.up.railway.app
```

## Testing

Once redeployed, try these commands in the UI:
- "Create a red cube"
- "Add a blue sphere"
- "Create a yellow cylinder"

The system should now work without 500 errors.
