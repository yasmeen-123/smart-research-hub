# Testing Guide for Smart Research Hub

## What Was Fixed

### Problems Identified:
1. **Two conflicting backends**: The repository had both a Node.js Express backend (`server.js`) and a Python FastAPI backend (`app/main.py`)
2. **CORS issues**: The Node.js backend had hardcoded CORS origins and required HTTPS certificates
3. **Inconsistent API URLs**: The frontend had complex conditional logic for determining the backend URL
4. **Missing environment variable configuration**: No clear documentation on required environment variables

### Solutions Implemented:
1. ✅ **Removed Node.js Express backend** - Deleted `server.js`, `package.json`, and `package-lock.json` from backend
2. ✅ **Updated CORS configuration** - FastAPI backend now allows requests from localhost and Docker network
3. ✅ **Simplified frontend API URL logic** - Now uses single environment variable `NEXT_PUBLIC_API_BASE`
4. ✅ **Added environment variable examples** - Created `.env.example` files in root, backend, and frontend
5. ✅ **Updated docker-compose.yml** - Properly passes environment variables to containers
6. ✅ **Enhanced README** - Added clear setup instructions for both Docker and local development
7. ✅ **Fixed Python import** - Updated deprecated langchain import to use langchain-community
8. ✅ **Fixed __init__.py** - Renamed `_init_.py` to proper `__init__.py`

## Testing the Application

### Option 1: Test with Docker (Recommended)

1. **Prerequisites**:
   - Docker and Docker Compose installed
   - OpenAI API key (or use placeholder for testing auth/upload without embeddings)

2. **Setup**:
   ```bash
   # Copy environment variables
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key (or leave placeholder)
   # The JWT_SECRET can remain as-is for testing
   
   # Build and run
   docker-compose up --build
   ```

3. **Test the application**:
   - Open http://localhost:3000 in your browser
   - You should see the "Smart Research Hub — MVP" page
   - Test authentication:
     - Enter an email and password
     - Click "Register" - you should see "Registered and logged in successfully!"
     - Click "Login" - you should see "Login successful!"
   - Test file upload (if logged in):
     - Select a text file
     - Click "Upload" - should show upload confirmation
   - Test search (if logged in):
     - Enter a query
     - Click "Search" - should return results

### Option 2: Test Locally (Without Docker)

1. **Prerequisites**:
   - Python 3.11+ installed
   - Node.js 18+ installed
   - PostgreSQL database running (or use SQLite by modifying db.py)

2. **Setup Backend**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your credentials
   
   # Create virtual environment (optional but recommended)
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Setup Frontend** (in new terminal):
   ```bash
   cd frontend
   cp .env.example .env.local
   # Edit .env.local if needed (default should work)
   
   # Install dependencies
   npm install
   
   # Run frontend
   npm run dev
   ```

4. **Test the application**:
   - Open http://localhost:3000
   - Follow same testing steps as Docker option

## Verification Checklist

- [ ] Backend starts without errors on port 8000
- [ ] Frontend starts without errors on port 3000
- [ ] Can access frontend at http://localhost:3000
- [ ] Can register a new user
- [ ] Can login with registered user
- [ ] Token is displayed after login
- [ ] Can upload a file when logged in
- [ ] Can perform search when logged in
- [ ] No CORS errors in browser console
- [ ] Backend logs show incoming requests from frontend

## Common Issues and Solutions

### Issue: "Network error — cannot reach backend"
**Solution**: 
- Verify backend is running on port 8000
- Check that `NEXT_PUBLIC_API_BASE` is set correctly in frontend
- For Docker: Should be `http://backend:8000`
- For local: Should be `http://localhost:8000`

### Issue: CORS errors in browser console
**Solution**: 
- This should be fixed now with updated CORS configuration
- If still occurring, check that backend CORS origins include your frontend URL

### Issue: Database connection errors
**Solution**: 
- For Docker: Wait for PostgreSQL to fully start before backend
- For local: Ensure PostgreSQL is running and DATABASE_URL is correct
- Alternative: Modify `backend/app/db.py` to use SQLite for testing

### Issue: OpenAI API errors
**Solution**: 
- Add valid OpenAI API key to .env
- For testing without OpenAI, you can register/login/upload but search may fail

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │  Port 3000 (Next.js)
│   (React/Next)  │
└────────┬────────┘
         │ HTTP
         │ API_BASE
         ▼
┌─────────────────┐
│   Backend       │  Port 8000 (FastAPI/Python)
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Database      │  Port 5432 (PostgreSQL)
│   (PostgreSQL)  │
└─────────────────┘
```

## Files Changed

1. **Removed**:
   - `backend/server.js` - Conflicting Node.js backend
   - `backend/package.json` - Node.js dependencies
   - `backend/package-lock.json` - Node.js lock file

2. **Modified**:
   - `backend/app/main.py` - Updated CORS configuration
   - `backend/app/embeddings.py` - Fixed deprecated import
   - `frontend/pages/index.js` - Simplified API base URL logic
   - `frontend/next.config.js` - Updated rewrites configuration
   - `frontend/dockerfile` - Added environment variable
   - `docker-compose.yml` - Added frontend environment variable
   - `README.md` - Enhanced with detailed setup instructions
   - `.gitignore` - Added database and upload files

3. **Added**:
   - `.env.example` - Root environment variables template
   - `backend/.env.example` - Backend environment variables template
   - `frontend/.env.example` - Frontend environment variables template
   - `backend/app/__init__.py` - Fixed Python package initialization

## Next Steps

After verifying the fixes work:
1. Consider adding more comprehensive error handling
2. Add input validation on frontend forms
3. Implement proper logging for debugging
4. Add health check endpoints
5. Consider adding API documentation with Swagger/OpenAPI
6. Add unit and integration tests
