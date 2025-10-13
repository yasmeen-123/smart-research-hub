# Quick Start Guide 🚀

Get the Smart Research Hub running in under 5 minutes!

## Prerequisites
- Docker and Docker Compose installed
- (Optional) OpenAI API key for full functionality

## Steps

### 1. Clone and Setup Environment
```bash
git clone https://github.com/yasmeen-123/smart-research-hub.git
cd smart-research-hub
cp .env.example .env
```

### 2. Configure (Optional)
Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```
> **Note**: You can skip this for testing authentication and uploads. Search functionality requires a valid API key.

### 3. Start the Application
```bash
docker-compose up --build
```

Wait for the services to start (look for these messages):
- ✅ Backend: `✅ Smart Research Hub Backend is running!`
- ✅ Frontend: `ready - started server on 0.0.0.0:3000`
- ✅ Database: `database system is ready to accept connections`

### 4. Access the Application
Open your browser and go to:
```
http://localhost:3000
```

### 5. Test the Features

#### Test Authentication
1. Enter any email and password
2. Click **Register** → Should see "Registered and logged in successfully!"
3. Click **Login** → Should see "Login successful!"
4. Note: You'll see a token displayed (first 40 characters)

#### Test File Upload
1. Make sure you're logged in (token should be visible)
2. Click **Choose File** and select any text file
3. Click **Upload** → Should see confirmation message with doc_id

#### Test Search
1. Make sure you're logged in
2. Enter a search query in the text box
3. Click **Search** → Should see results (requires OpenAI API key)

## Troubleshooting

### "Network error — cannot reach backend"
- Wait a bit longer for services to fully start
- Check if all containers are running: `docker-compose ps`
- Check logs: `docker-compose logs backend`

### CORS Errors
- This should be fixed! If you still see CORS errors, please report the issue.

### Port Already in Use
If port 3000 or 8000 is already in use:
```bash
# Stop the conflicting service or change ports in docker-compose.yml
# Then restart
docker-compose down
docker-compose up --build
```

## Stopping the Application
```bash
# Press Ctrl+C in the terminal, then:
docker-compose down
```

## What's Next?
- Read [TESTING.md](TESTING.md) for detailed testing instructions
- Read [FIXES_SUMMARY.md](FIXES_SUMMARY.md) to understand what was fixed
- Check [README.md](README.md) for architecture details and local development setup

## Architecture Overview
```
┌─────────────────────────────────────────────────┐
│            Docker Compose Network               │
│                                                 │
│  Browser ──> Frontend:3000 ──> Backend:8000   │
│                                      │          │
│                                      ▼          │
│                               Database:5432     │
└─────────────────────────────────────────────────┘
```

## Features to Try
- ✅ User Registration & Login (JWT authentication)
- ✅ Document Upload (supports PDF, TXT, DOCX)
- ✅ Semantic Search (using OpenAI embeddings)
- ✅ Automatic text chunking and indexing
- ✅ FAISS vector storage for fast retrieval

## Need Help?
Check the comprehensive guides:
- [TESTING.md](TESTING.md) - Detailed testing procedures
- [FIXES_SUMMARY.md](FIXES_SUMMARY.md) - What was fixed and why
- [README.md](README.md) - Full documentation

Happy researching! 📚✨
