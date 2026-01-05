import uuid
import json
import sqlite3
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from ..database import get_db
from ..models import Meal
from ..utils import serialize_meal, save_upload_file, process_tags
from ..config import logger

router = APIRouter(prefix="/meals", tags=["meals"])

@router.get("", response_model=List[Meal])
def get_meals(db: sqlite3.Connection = Depends(get_db)):
    rows = db.execute('SELECT * FROM meals').fetchall()
    return [serialize_meal(row) for row in rows]

@router.post("", response_model=Meal)
def create_meal(
    name: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""), 
    rating: float = Form(0),
    file: Optional[UploadFile] = File(None),
    db: sqlite3.Connection = Depends(get_db)
):
    assets = []
    if file:
        assets.append(save_upload_file(file))

    meal_id = str(uuid.uuid4())
    tags_list = process_tags(tags)
    
    try:
        db.execute(
            'INSERT INTO meals (id, name, description, rating, tags, assets) VALUES (?, ?, ?, ?, ?, ?)',
            (meal_id, name, description, rating, json.dumps(tags_list), json.dumps(assets))
        )
        db.commit()
    except sqlite3.Error as e:
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

    return {
        "id": meal_id,
        "name": name,
        "description": description,
        "rating": rating,
        "tags": tags_list,
        "assets": assets
    }

@router.put("/{meal_id}", response_model=Meal)
def update_meal(
    meal_id: str,
    name: str = Form(...),
    description: str = Form(""),
    tags: str = Form(""), 
    rating: float = Form(0),
    file: Optional[UploadFile] = File(None),
    db: sqlite3.Connection = Depends(get_db)
):
    row = db.execute('SELECT * FROM meals WHERE id = ?', (meal_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    current_assets = json.loads(row["assets"]) if row["assets"] else []
    assets = current_assets

    if file:
        assets = [save_upload_file(file)]

    tags_list = process_tags(tags)

    try:
        db.execute(
            '''UPDATE meals 
               SET name = ?, description = ?, rating = ?, tags = ?, assets = ?
               WHERE id = ?''',
            (name, description, rating, json.dumps(tags_list), json.dumps(assets), meal_id)
        )
        db.commit()
    except sqlite3.Error as e:
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

    return {
        "id": meal_id,
        "name": name,
        "description": description,
        "rating": rating,
        "tags": tags_list,
        "assets": assets
    }

@router.delete("/{meal_id}")
def delete_meal(meal_id: str, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute('DELETE FROM plans WHERE meal_id = ?', (meal_id,))
        cursor = db.execute('DELETE FROM meals WHERE id = ?', (meal_id,))
        db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Meal not found")
            
        return {"success": True, "id": meal_id}
    except sqlite3.Error as e:
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
