# smart-research-hub
A web-based AI-powered knowledge platform that allows users to upload research documents, perform semantic search, generate summaries, and collaborate using LLM integration with a RAG pipeline.

## Architecture
- **Frontend**: Next.js (React) application running on port 3000
- **Backend**: FastAPI (Python) application running on port 8000
- **Database**: PostgreSQL database for storing users and documents

## Local Setup

### Option 1: Using Docker (Recommended)
1. Clone the repository
2. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your OpenAI API key and JWT secret
4. Run the application:
   ```bash
   docker-compose up --build
   ```
5. Open http://localhost:3000 in your browser

### Option 2: Local Development
1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your credentials
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Set up the frontend (in a new terminal):
   ```bash
   cd frontend
   cp .env.example .env.local
   # Edit .env.local if needed
   npm install
   npm run dev
   ```
4. Open http://localhost:3000 in your browser

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for embeddings and LLM features
- `JWT_SECRET`: Secret key for JWT token generation
- `DATABASE_URL`: PostgreSQL connection string
- `NEXT_PUBLIC_API_BASE`: Backend API URL (frontend only)

## Features
- User authentication (register/login)
- Document upload and processing
- Semantic search using embeddings
- RAG pipeline integration