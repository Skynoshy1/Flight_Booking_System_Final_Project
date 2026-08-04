import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "likes_comments.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS booking_likes (
            booking_id TEXT PRIMARY KEY,
            liked BOOLEAN NOT NULL,
            airline TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS booking_comments (
            booking_id TEXT PRIMARY KEY,
            comment TEXT NOT NULL,
            airline TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS airline_likes (
            airline TEXT PRIMARY KEY,
            likes_count INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

def get_booking_likes_map():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT booking_id, liked FROM booking_likes")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: bool(row[1]) for row in rows}
    except Exception as e:
        print(f"Error getting booking likes map: {e}")
        return {}

def get_booking_comments_map():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT booking_id, comment FROM booking_comments")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}
    except Exception as e:
        print(f"Error getting booking comments map: {e}")
        return {}

def toggle_booking_like(booking_id: str, liked: bool, airline: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Update/insert booking like
    cursor.execute("INSERT OR REPLACE INTO booking_likes (booking_id, liked, airline) VALUES (?, ?, ?)", (str(booking_id), liked, airline))
    
    # 2. Recalculate airline likes
    cursor.execute("SELECT COUNT(*) FROM booking_likes WHERE airline = ? AND liked = 1", (airline,))
    count = cursor.fetchone()[0]
    
    cursor.execute("INSERT OR REPLACE INTO airline_likes (airline, likes_count) VALUES (?, ?)", (airline, count))
    
    conn.commit()
    conn.close()
    return count

def add_booking_comment(booking_id: str, comment: str, airline: str, flight_id: int = None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure flight_id column exists
    try:
        cursor.execute("ALTER TABLE booking_comments ADD COLUMN flight_id INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass
        
    cursor.execute("INSERT OR REPLACE INTO booking_comments (booking_id, comment, airline, flight_id) VALUES (?, ?, ?, ?)", 
                   (str(booking_id), comment, airline, flight_id))
    conn.commit()
    conn.close()

def get_airline_likes():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT airline, likes_count FROM airline_likes")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}
    except Exception as e:
        print(f"Error getting airline likes: {e}")
        return {}
