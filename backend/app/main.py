import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import db, models, auth, utils, embeddings
from .schemas import UserCreate, Token
from sqlalchemy.exc import IntegrityError
from .db import SessionLocal, engine
import shutil
import numpy as np

# create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# --- Auth endpoints
@app.post("/register", response_model=Token)
def register(u: UserCreate, db: Session = Depends(get_db)):
    hashed = auth.hash_password(u.password)
    new = models.User(email=u.email, hashed_password=hashed)
    db.add(new)
    try:
        db.commit()
        db.refresh(new)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    token = auth.create_access_token({"sub": new.email, "id": new.id})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
def login(u: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == u.email).first()
    if not user or not auth.verify_password(u.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    token = authorization.split(" ")[1] if " " in authorization else authorization
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# --- File upload + processing
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    text = utils.extract_text(save_path, file.filename)
    # store in DB
    doc = models.Document(user_id=user.id, filename=file.filename, text=text)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    # chunk & embed
    chunks = embeddings.chunk_text(text)
    if not chunks:
        return {"message": "file saved but no text extracted"}
    vectors = embeddings.embed_texts(chunks)
    # load or create index and add vectors
    index = embeddings.load_index()
    index.add(np.array(vectors).astype("float32"))
    embeddings.save_index(index)
    return {"message": "uploaded and indexed", "doc_id": doc.id, "chunks": len(chunks)}

# --- search
@app.post("/search")
def search(q: dict, user=Depends(get_current_user)):
    query_text = q.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Missing query")
    # embed query
    emb = embeddings.embeddings_client.embed_query(query_text)
    index = embeddings.load_index()
    if index.ntotal == 0:
        return {"results": []}
    D, I = index.search(np.array([np.array(emb).astype("float32")]), k=5)
    # In MVP we do not map chunk->doc text storage. We'll return indices and distances.
    return {"indices": I.tolist(), "distances": D.tolist()}
