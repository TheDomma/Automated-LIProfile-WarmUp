from db.database import init_db, get_connection

# Initialize the tables just in case
init_db()

# Replace this with your actual GoLogin Profile ID!
TEST_PROFILE_ID = "6842c6d0fe1416bc8d9af8e8"

conn = get_connection()
cursor = conn.cursor()
cursor.execute(
    "INSERT OR IGNORE INTO accounts (profile_id, name, is_active) VALUES (?, ?, ?)",
    (TEST_PROFILE_ID, "Test Account 1", 1)
)
conn.commit()
conn.close()

print(f"Added profile {TEST_PROFILE_ID} to the database.")