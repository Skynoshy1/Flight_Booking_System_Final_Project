import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine, text

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("DATABASE_URL not found!")
    exit(1)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("Altering table bookings to add selected_seats column...")
        conn.execute(text("ALTER TABLE bookings ADD COLUMN IF NOT EXISTS selected_seats JSONB DEFAULT '[]'::jsonb;"))
        conn.commit()
        print("Database schema successfully altered!")
except Exception as e:
    print("Failed to alter database schema:", e)
