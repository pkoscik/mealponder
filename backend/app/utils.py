import os
import shutil
import uuid
import json
import sqlite3
from fastapi import UploadFile, HTTPException
from .config import UPLOAD_DIR, ALLOWED_IMAGE_TYPES, logger

def process_tags(tags_str: str) -> list[str]:
    return [t.strip() for t in tags_str.split(",") if t.strip()]

def serialize_meal(row: sqlite3.Row) -> dict:
    """Helper to convert DB row to Dict with JSON parsing."""
    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "rating": row["rating"],
        "tags": json.loads(row["tags"]) if row["tags"] else [],
        "assets": json.loads(row["assets"]) if row["assets"] else []
    }

def save_upload_file(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image file type.")
    
    try:
        file_ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return f"http://localhost:8000/uploads/{filename}"
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail="Could not save file")