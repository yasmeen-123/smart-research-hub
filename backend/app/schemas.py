from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- 1. Authentication Schemas ---

class Token(BaseModel):
    """Schema for the returned JWT access token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for the data contained within the JWT payload."""
    email: Optional[str] = None
    id: Optional[int] = None # Added user ID for token payload

class UserCreate(BaseModel):
    """Schema for user registration request body."""
    email: EmailStr
    password: str

class UserRead(BaseModel):
    """Schema for returning user data (response model)."""
    id: int
    email: EmailStr
    # You might want to include the creation date for completeness
    created_at: datetime 

    class Config:
        # Allows Pydantic to read ORM data attributes (like id)
        from_attributes = True # Updated to use 'from_attributes' for Pydantic v2+


# --- 2. Document and Chunk Schemas ---

class ChunkRead(BaseModel):
    """Schema for a single document chunk."""
    id: int
    doc_id: int
    user_id: int
    faiss_index_id: int
    content: str
    
    class Config:
        from_attributes = True

class DocumentRead(BaseModel):
    """Schema for returning document data (response model)."""
    id: int
    user_id: int
    filename: str
    created_at: datetime
    # Optionally include text, but be mindful of size for large documents
    text: Optional[str] = None 
    
    # You can nest the relationship for viewing all chunks in a document
    chunks: List[ChunkRead] = [] 

    class Config:
        from_attributes = True

# --- 3. Search Schemas ---

class SearchQuery(BaseModel):
    """Schema for the search query request body."""
    query: str

class SearchResultItem(BaseModel):
    """Schema for a single search result item."""
    index_id: int
    similarity_score: float
    text_snippet: str
    document_id: int

class SearchResponse(BaseModel):
    """Schema for the overall search response."""
    query: str
    total_matches: int
    results: List[SearchResultItem]