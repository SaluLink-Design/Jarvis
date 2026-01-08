# Backend Setup & Troubleshooting Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

You have **two options** to set the OpenAI API key:

#### Option A: Using .env file (Recommended for local development)

```bash
cd backend
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-api-key-here
```

#### Option B: Set as System Environment Variable

**On Linux/macOS:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"
```

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-api-key-here"
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Start the Backend

```bash
cd backend
python main.py
```

You should see output like:
```
================================================================================
🤖 Initializing Jarvis Backend...
================================================================================
[STARTUP] Creating JarvisOrchestrator instance...
[STARTUP] Calling orchestrator.initialize()...
[NLP_INIT] OPENAI_API_KEY present: True
[NLP_INIT] HAS_OPENAI library: True
[NLP_INIT] Attempting to initialize OpenAI client...
✓ OpenAI NLP processor initialized successfully
================================================================================
✅ Jarvis Backend is ready!
================================================================================
```

## Understanding the Error Message

### If you see "No OpenAI API key" message:

**This is NOT an error!** It's an informational tip that appears when:
- The backend cannot connect (HTTP 503 error)
- The backend hasn't fully initialized

The system WORKS WITHOUT an OpenAI API key - it will automatically fall back to rule-based NLP processing. However, with an API key, you get:
- Better natural language understanding
- More complex object descriptions
- Improved scene generation

### What to check if the message appears:

1. **Is the backend running?**
   ```bash
   # Should return {"status": "healthy", ...}
   curl http://localhost:8000/api/health
   ```

2. **Did the backend initialize properly?**
   - Check the console output when you started it
   - Look for any error messages during startup
   - Check that all modules initialized (NLP, CV, Text-to-3D, Scene Builder)

3. **Is the API key correctly configured?**
   ```bash
   # Check if the key is set
   echo $OPENAI_API_KEY  # Linux/macOS
   echo %OPENAI_API_KEY%  # Windows
   ```

4. **Is port 8000 already in use?**
   ```bash
   # Change the port
   PORT=8001 python main.py
   ```

## Backend URL Configuration

### Local Development
- Backend URL: `http://localhost:8000`
- Frontend should automatically connect to `http://localhost:8000/api`

### Production (Railway)
- Backend URL: Set via `VITE_BACKEND_URL` environment variable
- Current value: Check `.env` or the railway deployment settings

## Troubleshooting

### "ModuleNotFoundError" or missing dependencies

```bash
cd backend
pip install -r requirements.txt
```

### "Connection refused" error

The frontend can't reach the backend. Make sure:
1. Backend is running: `python main.py`
2. Backend is on port 8000 (or update frontend `VITE_BACKEND_URL`)
3. There are no firewall blocks

### Backend starts but processes commands slowly

This is normal! The system is:
- Processing your natural language input
- Generating 3D models
- Rendering to the viewport

First request typically takes 2-5 seconds.

### Backend crashes with errors

1. Check the error message in the console
2. Look for missing dependencies: `pip install -r requirements.txt`
3. Ensure Python 3.10+ is installed: `python --version`
4. Check for port conflicts: `PORT=8001 python main.py`

## Diagnostics Endpoint

Get full system status:
```bash
# Returns detailed information about all backend modules
curl http://localhost:8000/api/diagnostics | json_pp
```

Expected response (when everything is working):
```json
{
  "status": "ok",
  "orchestrator_initialized": true,
  "openai_api_key_set": true,
  "openai_client_initialized": true,
  "modules": {
    "nlp_processor_exists": true,
    "cv_processor_exists": true,
    "text_to_3d_exists": true,
    "scene_builder_exists": true
  },
  "using_llm": true,
  "nlp_processor_fallback": "openai_llm"
}
```

## Working WITHOUT an OpenAI API Key

The system is designed to work without an API key!

- **With API key**: Uses GPT-3.5-turbo for natural language understanding
- **Without API key**: Uses rule-based NLP (still very functional)

Both modes support:
- Creating primitive shapes (cube, sphere, cylinder, cone, plane)
- Building environments (forest, city, interior, studio)
- Image-based object generation
- Real-time 3D visualization

## Getting an OpenAI API Key (Optional)

1. Go to https://platform.openai.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy it into your `.env` file or set as environment variable

**Cost**: As of now, basic API calls are very affordable or free tier. Check current pricing at https://openai.com/pricing
