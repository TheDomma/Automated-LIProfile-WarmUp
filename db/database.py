import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initializes the SQLite database and creates necessary tables if they don't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for tracking individual warmup sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id TEXT NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for storing accounts (optional for V1, but good practice)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            profile_id TEXT PRIMARY KEY,
            name TEXT,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")
