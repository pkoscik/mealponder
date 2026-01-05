from typing import List, Optional
from pydantic import BaseModel

class Meal(BaseModel):
    id: str
    name: str
    tags: List[str] = []
    assets: List[str] = []
    description: Optional[str] = ""
    rating: float = 0

class FrequentMeal(BaseModel):
    meal: Meal
    count: int