import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine, text

db_url = os.getenv("DATABASE_URL")
print("Connecting to database to add columns...")
engine = create_engine(db_url)
with engine.connect() as conn:
    conn.execute(text('ALTER TABLE profiles ADD COLUMN IF NOT EXISTS gender text;'))
    conn.execute(text('ALTER TABLE profiles ADD COLUMN IF NOT EXISTS city text;'))
    conn.execute(text('ALTER TABLE profiles ADD COLUMN IF NOT EXISTS "birthDay" text;'))
    conn.execute(text('ALTER TABLE profiles ADD COLUMN IF NOT EXISTS "birthMonth" text;'))
    conn.execute(text('ALTER TABLE profiles ADD COLUMN IF NOT EXISTS "birthYear" text;'))
    conn.commit()
print("Successfully verified and added columns to profiles table!")
