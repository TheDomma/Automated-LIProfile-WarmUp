import os

# Paste the API Token you just generated in the quotes below
GOLOGIN_API_TOKEN = os.getenv("GOLOGIN_API_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NTllODM1NmUwN2U1Yjk2YmM4YzY1NTciLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2OWZiYTI5MGNiNDM4ZjFjYjFlZGFmZGUifQ.LGkp70tmMrZj15UuRPH7LIAR1CpmPKPFh2lEnowJZ_c")

# SQLite Database
DB_PATH = os.getenv("DB_PATH", "linkedin_sessions.db")

# Timeouts
PAGE_LOAD_TIMEOUT = 30000  # 30 seconds