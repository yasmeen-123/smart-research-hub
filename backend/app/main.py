import os
import shutil
import numpy as np
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# --- Import project modules ---
from . import db, models, auth, utils, embeddings
from .schemas import UserCreate, Token
from .db import SessionLocal, engine

# --- Initialize DB ---
models.Base.metadata.create_all(bind=engine)

# --- Create FastAPI app ---
app = FastAPI(title="Smart Research Hub API", version="1.0")

# --- ✅ Enable CORS (Allow frontend at localhost:3000) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000"
    ],  # both forms, for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- File upload directory ---
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Database dependency ---
def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# --- Root route (test endpoint) ---
@app.get("/")
def root():
    return {"message": "✅ Smart Research Hub Backend is running!"}

# --- Register user ---
@app.post("/register", response_model=Token)
def register(u: UserCreate, db: Session = Depends(get_db)):
    hashed = auth.hash_password(u.password)
    new_user = models.User(email=u.email, hashed_password=hashed)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    token = auth.create_access_token({"sub": new_user.email, "id": new_user.id})
    return {"access_token": token, "token_type": "bearer"}

# --- Login user ---
@app.post("/login", response_model=Token)
def login(u: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == u.email).first()
    if not user or not auth.verify_password(u.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer"}

# --- Auth helper ---
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")

    token = authorization.split(" ")[1] if " " in authorization else authorization
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not (user := db.query(models.User).filter(models.User.email == payload.get("sub")).first()):
        raise HTTPException(status_code=401, detail="User not found")
    else:
        return user

# --- Upload file ---
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = utils.extract_text(save_path, file.filename)
    doc = models.Document(user_id=user.id, filename=file.filename, text=text)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    chunks = embeddings.chunk_text(text)
    if not chunks:
        return {"message": "File saved but no text extracted"}

    vectors = embeddings.embed_texts(chunks)
    index = embeddings.load_index()
    index.add(np.array(vectors).astype("float32"))
    embeddings.save_index(index)

    return {"message": "Uploaded and indexed", "doc_id": doc.id, "chunks": len(chunks)}

# --- Search ---
@app.post("/search")
def search(q: dict, user=Depends(get_current_user)):
    query_text = q.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Missing query")

    emb = embeddings.embeddings_client.embed_query(query_text)
    index = embeddings.load_index()
    if index.ntotal == 0:
        return {"results": []}

    D, I = index.search(np.array([np.array(emb).astype("float32")]), k=5)
    return {"indices": I.tolist(), "distances": D.tolist()}

# --- Run the server ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    