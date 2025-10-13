# Architecture Documentation

## Before Fixes (Broken) ❌

```
┌────────────────────────────────────────────────────────────────┐
│                    Confused Architecture                        │
│                                                                 │
│  Browser                                                        │
│     │                                                           │
│     │ Tries to connect to:                                     │
│     │ - https://stunning-space-sniffle-...github.dev:8000     │
│     │ - http://127.0.0.1:8000 (sometimes)                     │
│     │ - http://backend:8000 (sometimes)                       │
│     ▼                                                           │
│  Frontend (Next.js)                                            │
│  Port: 3000                                                     │
│  Complex conditional API URL logic                             │
│     │                                                           │
│     │ HTTP Request                                             │
│     ▼                                                           │
│  ┌──────────────────┐           ┌──────────────────┐          │
│  │  Backend Option 1│  OR?      │  Backend Option 2│          │
│  │  Node.js/Express │           │  Python/FastAPI  │          │
│  │  Port: 8000      │           │  Port: 8000      │          │
│  │  - Requires HTTPS│           │  - Has CORS      │          │
│  │  - Hardcoded CORS│           │  - DB integration│          │
│  │  - No features   │           │  - Full features │          │
│  └──────────────────┘           └────────┬─────────┘          │
│           ❌                               │                    │
│      Doesn't work                         ▼                    │
│                                  ┌──────────────────┐          │
│                                  │   PostgreSQL DB  │          │
│                                  │   Port: 5432     │          │
│                                  └──────────────────┘          │
│                                                                 │
│  Issues:                                                        │
│  ❌ Two conflicting backends                                   │
│  ❌ CORS errors                                                │
│  ❌ Hardcoded Codespace URL                                    │
│  ❌ HTTPS certificate requirement                              │
│  ❌ Complex frontend logic                                     │
└────────────────────────────────────────────────────────────────┘
```

## After Fixes (Working) ✅

```
┌────────────────────────────────────────────────────────────────┐
│              Clean, Working Architecture                        │
│                                                                 │
│  Browser                                                        │
│     │                                                           │
│     │ http://localhost:3000                                    │
│     ▼                                                           │
│  ┌─────────────────────────────────────────────┐              │
│  │          Frontend (Next.js)                  │              │
│  │          Port: 3000                          │              │
│  │                                              │              │
│  │  Simple API config:                          │              │
│  │  API_BASE = NEXT_PUBLIC_API_BASE ||          │              │
│  │            "http://localhost:8000"           │              │
│  │                                              │              │
│  │  Environment:                                 │              │
│  │  - Docker: NEXT_PUBLIC_API_BASE=             │              │
│  │           http://backend:8000                │              │
│  │  - Local: NEXT_PUBLIC_API_BASE=              │              │
│  │           http://localhost:8000              │              │
│  └──────────────────┬───────────────────────────┘              │
│                     │                                           │
│                     │ HTTP Request                              │
│                     │ (No CORS errors!)                         │
│                     ▼                                           │
│  ┌─────────────────────────────────────────────┐              │
│  │     Backend (Python/FastAPI)                 │              │
│  │     Port: 8000                               │              │
│  │                                              │              │
│  │  Features:                                    │              │
│  │  ✅ User Authentication (JWT)               │              │
│  │  ✅ Document Upload & Processing            │              │
│  │  ✅ Text Extraction (PDF, DOCX, TXT)        │              │
│  │  ✅ Embeddings (OpenAI)                     │              │
│  │  ✅ Semantic Search (FAISS)                 │              │
│  │                                              │              │
│  │  CORS Configuration:                         │              │
│  │  allow_origins=[                             │              │
│  │    "http://localhost:3000",                  │              │
│  │    "http://frontend:3000",                   │              │
│  │    "http://127.0.0.1:3000",                  │              │
│  │    "*"  # Dev mode                           │              │
│  │  ]                                           │              │
│  └──────────────────┬───────────────────────────┘              │
│                     │                                           │
│                     │ SQL Queries                               │
│                     ▼                                           │
│  ┌─────────────────────────────────────────────┐              │
│  │       Database (PostgreSQL)                  │              │
│  │       Port: 5432                             │              │
│  │                                              │              │
│  │  Tables:                                     │              │
│  │  - users (email, hashed_password)            │              │
│  │  - documents (filename, text, user_id)       │              │
│  │                                              │              │
│  │  Vector Storage:                             │              │
│  │  - FAISS index (faiss_index.idx)             │              │
│  └─────────────────────────────────────────────┘              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Docker Network Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Docker Compose                             │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Custom Bridge Network                      │  │
│  │                                                         │  │
│  │  ┌──────────────┐   ┌──────────────┐   ┌───────────┐ │  │
│  │  │  frontend    │   │   backend    │   │    db     │ │  │
│  │  │              │──>│              │──>│           │ │  │
│  │  │  Next.js     │   │  FastAPI     │   │ PostgreSQL│ │  │
│  │  │  :3000       │   │  :8000       │   │  :5432    │ │  │
│  │  └──────┬───────┘   └──────────────┘   └───────────┘ │  │
│  │         │                                              │  │
│  └─────────┼──────────────────────────────────────────────┘  │
│            │                                                  │
│  Host Ports:                                                 │
│  - 3000:3000 (Frontend)                                      │
│  - 8000:8000 (Backend)                                       │
│  - 5432:5432 (Database)                                      │
│            │                                                  │
└────────────┼──────────────────────────────────────────────────┘
             │
             │ Port mapping
             ▼
      ┌─────────────┐
      │   Host OS   │
      │  localhost  │
      └─────────────┘
```

## Request Flow

### 1. User Registration/Login
```
Browser                Frontend              Backend              Database
   │                      │                     │                     │
   │──Register Form──────>│                     │                     │
   │                      │──POST /register────>│                     │
   │                      │  {email, password}  │                     │
   │                      │                     │──Hash password─────>│
   │                      │                     │──INSERT user───────>│
   │                      │                     │<──User created──────│
   │                      │                     │──Create JWT token   │
   │                      │<──200 OK────────────│                     │
   │                      │  {access_token}     │                     │
   │<──Token displayed────│                     │                     │
   │                      │                     │                     │
```

### 2. File Upload
```
Browser                Frontend              Backend              Database
   │                      │                     │                     │
   │──Select file────────>│                     │                     │
   │──Click Upload───────>│                     │                     │
   │                      │──POST /upload──────>│                     │
   │                      │  Authorization:     │                     │
   │                      │  Bearer <token>     │                     │
   │                      │  file: <binary>     │                     │
   │                      │                     │──Verify JWT token   │
   │                      │                     │──Extract text       │
   │                      │                     │  (PDF/DOCX/TXT)     │
   │                      │                     │──INSERT document───>│
   │                      │                     │<──Doc ID────────────│
   │                      │                     │──Chunk text         │
   │                      │                     │──Generate embeddings│
   │                      │                     │  (OpenAI API)       │
   │                      │                     │──Store in FAISS     │
   │                      │<──200 OK────────────│                     │
   │                      │  {doc_id, chunks}   │                     │
   │<──Success message────│                     │                     │
   │                      │                     │                     │
```

### 3. Semantic Search
```
Browser                Frontend              Backend              FAISS Index
   │                      │                     │                     │
   │──Enter query────────>│                     │                     │
   │──Click Search───────>│                     │                     │
   │                      │──POST /search──────>│                     │
   │                      │  Authorization:     │                     │
   │                      │  Bearer <token>     │                     │
   │                      │  {query: "..."}     │                     │
   │                      │                     │──Verify JWT token   │
   │                      │                     │──Embed query        │
   │                      │                     │  (OpenAI API)       │
   │                      │                     │──Search────────────>│
   │                      │                     │<──Top K results─────│
   │                      │<──200 OK────────────│                     │
   │                      │  {results: [...]}   │                     │
   │<──Display results────│                     │                     │
   │                      │                     │                     │
```

## Technology Stack

### Frontend
- **Framework**: Next.js 15.5.4
- **UI Library**: React 18.2.0
- **Styling**: Tailwind CSS 4.1.14
- **HTTP Client**: Axios 1.4.0
- **Animations**: Framer Motion 10.12.16

### Backend
- **Framework**: FastAPI
- **Web Server**: Uvicorn
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with bcrypt
- **Database ORM**: SQLAlchemy
- **Embeddings**: LangChain + OpenAI
- **Vector Store**: FAISS (CPU)
- **Document Processing**:
  - PDF: pdfplumber
  - DOCX: python-docx
  - TXT: Built-in

### Database
- **DBMS**: PostgreSQL 15
- **Storage**: Persistent volume
- **Connection**: SQLAlchemy ORM

### Infrastructure
- **Container**: Docker
- **Orchestration**: Docker Compose
- **Network**: Custom bridge network

## Environment Variables

### Backend
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/smartdb
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret-key
```

### Frontend
```bash
NEXT_PUBLIC_API_BASE=http://backend:8000  # Docker
NEXT_PUBLIC_API_BASE=http://localhost:8000  # Local
```

## File Structure

```
smart-research-hub/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Package initialization
│   │   ├── main.py              # FastAPI app & routes
│   │   ├── auth.py              # JWT authentication
│   │   ├── db.py                # Database setup
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── embeddings.py        # OpenAI + FAISS
│   │   └── utils.py             # Text extraction
│   ├── Dockerfile               # Backend container
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
├── frontend/
│   ├── pages/
│   │   ├── _app.js              # Next.js app wrapper
│   │   └── index.js             # Main page
│   ├── styles/
│   │   └── globals.css          # Global styles
│   ├── dockerfile               # Frontend container
│   ├── next.config.js           # Next.js configuration
│   ├── tailwind.config.js       # Tailwind setup
│   ├── package.json             # Node dependencies
│   └── .env.example             # Environment template
├── docker-compose.yml           # Container orchestration
├── .env.example                 # Root environment template
├── README.md                    # Main documentation
├── TESTING.md                   # Testing guide
├── QUICKSTART.md                # Quick start guide
├── FIXES_SUMMARY.md             # What was fixed
└── ARCHITECTURE.md              # This file
```

## Security Considerations

### Current (Development):
- ✅ JWT token-based authentication
- ✅ Password hashing with bcrypt
- ✅ CORS enabled for development
- ⚠️  Wildcard CORS (`"*"`)
- ⚠️  Default JWT secret
- ⚠️  HTTP only (no HTTPS)

### Production Recommendations:
- 🔒 Restrict CORS to specific origins
- 🔒 Use strong, unique JWT secret
- 🔒 Enable HTTPS with valid certificates
- 🔒 Add rate limiting
- 🔒 Implement request validation
- 🔒 Use environment secrets management
- 🔒 Enable database SSL connections
- 🔒 Add API request logging
- 🔒 Implement CSRF protection

## Performance Characteristics

### Current Limitations:
- FAISS index loaded in memory (limited by RAM)
- Synchronous document processing
- No caching layer
- Sequential embedding generation

### Scalability Improvements:
- Use FAISS GPU for faster search
- Implement async document processing
- Add Redis cache for frequent queries
- Batch embedding generation
- Use managed vector database (Pinecone, Weaviate)
- Add load balancer for multiple backend instances
- Implement database connection pooling

## Monitoring & Logging

### Current State:
- Basic console logging
- Docker logs via `docker-compose logs`

### Recommended Additions:
- Structured logging (JSON format)
- Log aggregation (ELK stack, Loki)
- Application metrics (Prometheus)
- Error tracking (Sentry)
- Request tracing (OpenTelemetry)
- Health check endpoints
- Performance monitoring (APM)
