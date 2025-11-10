import pdfplumber
# Changed import name to standard 'docx' for clarity
import docx 
import os
from typing import Optional, Union

# Define the full path type for clarity
FilePath = Union[str, os.PathLike]


def extract_text_from_pdf(path: FilePath) -> str:
    """
    Extracts text from a PDF file using pdfplumber, handling potential errors.
    """
    texts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                # Use := (walrus operator) for efficiency and check if text exists
                if (text := page.extract_text()): 
                    texts.append(text)
        
        return "\n".join(texts)
    
    except FileNotFoundError:
        print(f"[UTILS] Error: PDF file not found at path: {path}")
    except Exception as e:
        # Catch errors like corrupted PDF structure, permissions issues, etc.
        print(f"[UTILS] Error processing PDF file {path}: {e}")
    
    return "" # Return empty string on failure


def extract_text_from_docx(path: FilePath) -> str:
    """
    Extracts text from a DOCX file using python-docx, handling potential errors.
    """
    try:
        doc = docx.Document(path)
        # Combine all paragraph text, ignoring empty paragraphs
        texts = [p.text for p in doc.paragraphs if p.text] 
        return "\n".join(texts)
    
    except FileNotFoundError:
        print(f"[UTILS] Error: DOCX file not found at path: {path}")
    except docx.opc.exceptions.PackageNotFoundError:
        print(f"[UTILS] Error: DOCX file is corrupt or not a valid DOCX format at path: {path}")
    except Exception as e:
        print(f"[UTILS] Error processing DOCX file {path}: {e}")
    
    return "" # Return empty string on failure


def extract_text(path: FilePath, filename: str) -> str:
    """
    Routes the extraction based on file extension and provides a robust fallback.
    
    The path should be the local system path to the uploaded file.
    """
    # Ensure filename check is safe even if there are no dots
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    # --- Route Extraction ---
    if ext == "pdf":
        return extract_text_from_pdf(path)
        
    elif ext == "docx":
        # Note: We rely on docx to handle DOCX. DOC files (the older binary format) 
        # usually require external tools or libraries like antiword or python-libmagic.
        # Python-docx only supports DOCX.
        return extract_text_from_docx(path)
        
    # --- Plaintext/Fallback Handling ---
    else:
        # Treat any unknown extension or extension 'txt' as plaintext
        try:
            # Explicitly open as text with standard UTF-8 encoding
            with open(path, 'r', encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"[UTILS] Error: Plaintext file not found at path: {path}")
        except UnicodeDecodeError:
             print(f"[UTILS] Warning: Could not decode file {path} as UTF-8. Trying Latin-1.")
             try:
                 # Fallback for common non-UTF-8 encodings
                 with open(path, 'r', encoding="latin-1") as f:
                     return f.read()
             except Exception:
                 print(f"[UTILS] Error: Could not read file {path} with fallback encoding.")
        except Exception as e:
            print(f"[UTILS] Error processing file {path} as plaintext: {e}")
            
        return "" # Final fallback for any failure