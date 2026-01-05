import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .config import UPLOAD_DIR, DATA_DIR, logger
from .database import init_db
from .routers import meals, plans, analytics

# XXX(pkoscik): Create directories immediately when the script loads, 
# BEFORE app.mount tries to access them.
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("lifespan: wakeup")
    init_db()
    yield
    logger.info("lifespan: shutdown")

app = FastAPI(title="MealPonder API", lifespan=lifespan)

# Mount static files (URL /uploads -> maps to data/uploads)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(meals.router)
app.include_router(plans.router)
app.include_router(analytics.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)