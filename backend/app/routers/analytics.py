import sqlite3
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from ..database import get_db
from ..models import FrequentMeal
from ..utils import serialize_meal

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/frequent-meals", response_model=List[FrequentMeal])
def get_frequent_meals(days: int = 365, db: sqlite3.Connection = Depends(get_db)):
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    query = '''
        SELECT m.*, COUNT(p.meal_id) as count
        FROM plans p
        JOIN meals m ON p.meal_id = m.id
        WHERE p.date >= ?
        GROUP BY p.meal_id
        ORDER BY count DESC
        LIMIT 50
    '''
    rows = db.execute(query, (cutoff_date,)).fetchall()
    
    result = []
    for row in rows:
        result.append({
            "meal": serialize_meal(row),
            "count": row["count"]
        })
        
    return result
