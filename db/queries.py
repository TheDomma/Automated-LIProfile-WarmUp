from datetime import date
import logging
from db.database import get_connection

logger = logging.getLogger(__name__)

def log_session(profile_id: str, status: str, reason: str):
    """
    Logs the outcome of a warmup session.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        today_date = date.today().isoformat()
        
        cursor.execute(
            "INSERT INTO sessions (profile_id, date, status, reason) VALUES (?, ?, ?, ?)",
            (profile_id, today_date, status, reason)
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log session for {profile_id}: {e}")

def get_active_profiles():
    """
    Retrieves all active profile IDs.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT profile_id FROM accounts WHERE is_active = 1")
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
    except Exception as e:
        logger.error(f"Failed to fetch active profiles: {e}")
        return []
