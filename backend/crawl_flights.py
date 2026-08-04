import os
import random
import uuid
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from supabase import create_client, Client
import schedule
import time
import sys

# Load environment configurations
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Real-world Airlines backbone structure
AIRLINES = [
    {"name": "Vietnam Airlines", "prefix": "VN", "base_price": 120},
    {"name": "VietJet Air", "prefix": "VJ", "base_price": 60},
    {"name": "Bamboo Airways", "prefix": "BA", "base_price": 85},
    {"name": "Vietravel Airlines", "prefix": "VA", "base_price": 70}
]
TRIP_TYPES = ["one-way", "round-trip"]

def clean_old_flights():
    """Deletes unbooked flights to maintain premium database sizing and avoid duplication."""
    print("Core: Cleaning up unbooked flights to maintain premium database sizing...")
    try:
        # 1. Fetch flight IDs that have bookings
        bookings_res = supabase.table("bookings").select("flight_id").execute()
        booked_flight_ids = {b["flight_id"] for b in bookings_res.data if b.get("flight_id")} if bookings_res.data else set()
        
        # 2. Fetch all flights in database
        all_flights_res = supabase.table("flights").select("id").execute()
        
        if all_flights_res.data:
            # 3. Filter out those that are currently booked
            to_delete = [f["id"] for f in all_flights_res.data if f["id"] not in booked_flight_ids]
            
            if to_delete:
                # Delete unbooked flights in chunks of 100
                for i in range(0, len(to_delete), 100):
                    chunk = to_delete[i:i+100]
                    supabase.table("flights").delete().in_("id", chunk).execute()
                print(f"Successfully cleaned up {len(to_delete)} unbooked flights.")
            else:
                print("No unbooked flights to clean up.")
        else:
            print("No flights found to clean up.")
    except Exception as e:
        print(f"Warning during cleanup: {e}")

def generate_flexible_flights():
    clean_old_flights()
    print("[INFO] Initiating perfectly balanced 50/50 flight generation loop...")
    
    try:
        airports_res = supabase.table("airports").select("code").execute()
        airport_codes = [item['code'] for item in airports_res.data]
    except Exception as e:
        print(f"Error fetching airports from database, using fallbacks: {e}")
        airport_codes = ["SGN", "HAN", "DAD", "CXR", "DLI", "PQC", "HUI", "UIH", "VDO", "HPH"]
        
    print(f"Loaded {len(airport_codes)} airport codes for flight generation.")
    
    base_now = datetime.now()
    flights_to_insert = []
    
    for _ in range(1000):
        origin = random.choice(airport_codes)
        destination = random.choice(airport_codes)
        while origin == destination:
            destination = random.choice(airport_codes)
            
        day_offset = random.randint(0, 7)
        target_date = base_now + timedelta(days=day_offset)
        date_str = target_date.strftime("%Y-%m-%d")
        
        airline = random.choice(AIRLINES)
        flight_num = f"{airline['prefix']}-{random.randint(100, 999)}"
        
        dep_hour = random.randint(5, 22)
        dep_minute = random.choice([0, 15, 30, 45])
        dep_datetime = datetime(
            target_date.year, target_date.month, target_date.day,
            dep_hour, dep_minute, tzinfo=timezone.utc
        )
        
        duration_minutes = random.choice([45, 60, 90, 105, 120])
        arr_datetime = dep_datetime + timedelta(minutes=duration_minutes)
        
        assigned_trip_type = random.choice(['one-way', 'round-trip'])
        
        multiplier = 1.8 if assigned_trip_type == "round-trip" else 1.0
        final_price = round((airline["base_price"] + random.uniform(-15, 35)) * multiplier, 2)
        
        return_date_str = None
        if assigned_trip_type == "round-trip":
            return_datetime = target_date + timedelta(days=random.randint(2, 7))
            return_date_str = return_datetime.strftime("%Y-%m-%d")
            
        flight_row = {
            "flight_number": flight_num,
            "airline": airline["name"],
            "base_price": final_price,
            "origin": origin,
            "destination": destination,
            "departure_date": date_str,
            "departure_time": dep_datetime.isoformat(),
            "arrival_time": arr_datetime.isoformat(),
            "flight_type": "Domestic",
            "trip_type": assigned_trip_type,
            "return_date": return_date_str,
            "origin_country": "VN",
            "destination_country": "VN"
        }
        flights_to_insert.append(flight_row)
        
    chunk_size = 1000
    for i in range(0, len(flights_to_insert), chunk_size):
        chunk = flights_to_insert[i:i + chunk_size]
        try:
            supabase.table("flights").insert(chunk).execute()
            print(f"[SUCCESS] Successfully seeded chunk of {len(chunk)} flights into Supabase!")
        except Exception as e:
            print(f"[ERROR] Failed to insert flight batch chunk: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--now':
        generate_flexible_flights()
    else:
        schedule.every().day.at("07:00").do(generate_flexible_flights)

        print("[INFO] Flight Data Crawler Daemon is active and waiting for scheduled time (07:00 AM)...")
        print("💡 Hint: Run with '--now' argument to execute the seeder immediately.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("🛑 Automation daemon stopped safely.")
            sys.exit()
