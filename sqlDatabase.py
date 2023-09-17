import sqlite3

# Creating the SQLite database and table for user data storage
db_name = "./user_data_storage.db"

def initialize_db():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                website_url TEXT,
                company_name TEXT,
                product_name TEXT,
                product_text TEXT
            )
        """)
        conn.commit()

initialize_db()
db_name