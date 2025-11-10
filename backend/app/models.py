from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint 
from .db import Base # 💡 FIX: Import Base from your db.py file

# Note: The 'Base = declarative_base()' line was removed, as it belongs in db.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(512), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    documents = relationship("Document", back_populates="owner")
    # 💡 NEW: Relationship to the individual Chunks created by this user
    chunks = relationship("Chunk", back_populates="user") 


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(512), nullable=False)
    text = Column(Text, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")
    # 💡 NEW: Relationship to the Chunks belonging to this document
    chunks = relationship("Chunk", back_populates="document")
    

## 🚀 NEW: Chunk Model for Semantic Search Mapping
class Chunk(Base):
    """
    Maps a text chunk to its document and user, and stores its global FAISS index ID.
    """
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    
    # CRITICAL: This links the chunk text to the vector in the global FAISS index.
    faiss_index_id = Column(Integer, nullable=False, index=True, unique=True)
    
    # Foreign Keys
    doc_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The actual text content that was embedded
    content = Column(Text, nullable=False)
    
    # Relationships for easy navigation
    document = relationship("Document", back_populates="chunks")
    user = relationship("User", back_populates="chunks")
    
    __table_args__ = (
        # Ensure the FAISS ID is unique to prevent mapping conflicts
        UniqueConstraint('faiss_index_id', name='uq_faiss_id'),
    )