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
        print("Cleaning up old likes data...")
        conn.execute(text("TRUNCATE TABLE airline_likes RESTART IDENTITY CASCADE;"))
        
        print("Altering table airline_likes schema...")
        # 1. Drop constraint unique_user_airline_like
        conn.execute(text("ALTER TABLE airline_likes DROP CONSTRAINT IF EXISTS unique_user_airline_like;"))
        
        # 2. Add booking_id column
        conn.execute(text("ALTER TABLE airline_likes ADD COLUMN IF NOT EXISTS booking_id INTEGER;"))
        
        # 3. Add foreign key constraint referencing bookings(id)
        conn.execute(text("ALTER TABLE airline_likes DROP CONSTRAINT IF EXISTS fk_airline_likes_booking;"))
        conn.execute(text("ALTER TABLE airline_likes ADD CONSTRAINT fk_airline_likes_booking FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE;"))
        
        # 4. Add unique constraint on booking_id
        conn.execute(text("ALTER TABLE airline_likes DROP CONSTRAINT IF EXISTS unique_booking_like;"))
        conn.execute(text("ALTER TABLE airline_likes ADD CONSTRAINT unique_booking_like UNIQUE (booking_id);"))
        
        # 5. Commit transaction
        conn.commit()
        print("Database schema successfully altered!")
except Exception as e:
    print("Failed to alter database schema:", e)
