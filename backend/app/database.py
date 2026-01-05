import sqlite3
from typing import Generator
from .config import DB_FILE, logger

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Dependency to yield a database connection."""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                rating REAL DEFAULT 0,
                tags TEXT, 
                assets TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plans (
                date TEXT NOT NULL,
                meal_id TEXT NOT NULL,
                FOREIGN KEY (meal_id) REFERENCES meals (id)
            )
        ''')
        
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        conn.close()