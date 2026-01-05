import sqlite3
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from ..models import Meal
from ..utils import serialize_meal
from ..config import logger

router = APIRouter(prefix="/plans", tags=["plans"])

@router.get("", response_model=Dict[str, List[Meal]])
def get_all_plans(db: sqlite3.Connection = Depends(get_db)):
    query = '''
        SELECT p.date, m.* FROM plans p 
        JOIN meals m ON p.meal_id = m.id
    '''
    rows = db.execute(query).fetchall()
    
    all_plans = {}
    for row in rows:
        date_str = row["date"]
        meal_data = serialize_meal(row)
        
        if date_str not in all_plans:
            all_plans[date_str] = []
        all_plans[date_str].append(meal_data)
        
    return all_plans

@router.get("/{date}", response_model=List[Meal])
def get_plan(date: str, db: sqlite3.Connection = Depends(get_db)):
    query = '''
        SELECT m.* FROM meals m
        JOIN plans p ON m.id = p.meal_id
        WHERE p.date = ?
    '''
    rows = db.execute(query, (date,)).fetchall()
    return [serialize_meal(row) for row in rows]

@router.post("/{date}", response_model=List[Meal])
def add_meal_to_plan(date: str, meal: Meal, db: sqlite3.Connection = Depends(get_db)):
    try:
        # Check for duplicates manually (Legacy behavior preserved)
        existing = db.execute(
            'SELECT 1 FROM plans WHERE date = ? AND meal_id = ?', 
            (date, meal.id)
        ).fetchone()

        if not existing:
            db.execute('INSERT INTO plans (date, meal_id) VALUES (?, ?)', (date, meal.id))
            db.commit()
            
    except sqlite3.Error as e:
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    
    return get_plan(date, db)

@router.delete("/{date}/{meal_id}", response_model=List[Meal])
def remove_meal_from_plan(date: str, meal_id: str, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute('DELETE FROM plans WHERE date = ? AND meal_id = ?', (date, meal_id))
        db.commit()
    except sqlite3.Error as e:
        logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    
    return get_plan(date, db)
