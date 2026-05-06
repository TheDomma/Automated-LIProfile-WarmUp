import os

# GoLogin Local API settings
GOLOGIN_PORT = os.getenv("GOLOGIN_PORT", "35000")
GOLOGIN_API_URL = f"http://127.0.0.1:{GOLOGIN_PORT}"

# SQLite Database
DB_PATH = os.getenv("DB_PATH", "linkedin_sessions.db")

# Timeouts
PAGE_LOAD_TIMEOUT = 30000  # 30 seconds
