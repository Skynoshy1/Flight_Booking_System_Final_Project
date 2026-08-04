from datetime import datetime
from fastapi import APIRouter, Query, HTTPException
from app.core.security import supabase_client
import json

router = APIRouter()


@router.get("")
def get_all_flights():
    try:
        response = supabase_client.table("flights").select("*").order("id", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching all flights: {e}")
        return []

@router.get("/public")
def get_public_flights(trip_type: str = "one-way"):
    try:
        from datetime import datetime, timezone
        # Use timezone-aware UTC datetime
        now_utc = datetime.now(timezone.utc)
        now_iso = now_utc.isoformat()
        
        # 1. Real-time cleanup: Delete expired flights that have no bookings
        try:
            # Fetch all expired flights
            expired_res = supabase_client.table("flights").select("id").lt("departure_time", now_iso).execute()
            expired_flights = expired_res.data or []
            
            if expired_flights:
                # Fetch flight IDs that have bookings
                bookings_res = supabase_client.table("bookings").select("flight_id").execute()
                booked_flight_ids = {b["flight_id"] for b in bookings_res.data if b.get("flight_id")} if bookings_res.data else set()
                
                # Identify which expired flights can be safely deleted (not booked)
                to_delete = [f["id"] for f in expired_flights if f["id"] not in booked_flight_ids]
                
                if to_delete:
                    # Delete unbooked expired flights in chunks
                    for i in range(0, len(to_delete), 100):
                        chunk = to_delete[i:i+100]
                        supabase_client.table("flights").delete().in_("id", chunk).execute()
                    print(f"Real-time cleanup deleted {len(to_delete)} expired unbooked flights.")
        except Exception as cleanup_err:
            print(f"Error in real-time cleanup: {cleanup_err}")

        # 2. Query active (non-expired) flights
        query = supabase_client.table("flights").select("*").gte("departure_time", now_iso)
        if trip_type:
            query = query.eq("trip_type", trip_type)
        response = query.execute()
        flights = response.data or []

        # 3. If there are no future flights at all, automatically generate new ones
        if not flights:
            try:
                import sys
                import os
                backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                if backend_dir not in sys.path:
                    sys.path.append(backend_dir)
                
                from crawl_flights import generate_flexible_flights
                print("No future flights found. Generating new ones...")
                generate_flexible_flights()
                
                # Re-query
                query = supabase_client.table("flights").select("*").gte("departure_time", now_iso)
                if trip_type:
                    query = query.eq("trip_type", trip_type)
                response = query.execute()
                flights = response.data or []
            except Exception as gen_err:
                print(f"Failed to generate new flights: {gen_err}")
            
        active_flights = [
            f for f in flights 
            if str(f.get("status") or "").upper() not in ["CANCELED", "CANCELLED"]
        ]
        return active_flights
    except Exception as e:
        print(f"Error fetching public flights: {e}")
        return []




@router.get("/{flight_id}")
def get_flight_by_id(flight_id: int):
    try:
        response = supabase_client.table("flights").select("*").eq("id", flight_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching flight {flight_id}: {e}")
        return None

@router.get("/{flight_id}/occupied_seats")
def get_occupied_seats(flight_id: int, user_id: str = Query(None)):
    try:
        bookings_res = supabase_client.table("bookings").select("user_id, selected_seats").eq("flight_id", flight_id).eq("status", "completed").execute()
        
        other_occupied = []
        user_booked = []
        
        for booking in bookings_res.data:
            seats = booking.get("selected_seats") or []
            if isinstance(seats, str):
                try:
                    seats = json.loads(seats)
                except Exception:
                    seats = []
            
            booking_user_id = booking.get("user_id")
            if user_id and str(booking_user_id) == str(user_id):
                user_booked.extend(seats)
            else:
                other_occupied.extend(seats)
                
        return {
            "other_occupied": other_occupied,
            "user_booked": user_booked
        }
    except Exception as e:
        print(f"Error fetching occupied seats: {e}")
        return {"other_occupied": [], "user_booked": []}

@router.put("/{flight_id}")
def update_flight(flight_id: int, flight_data: dict):
    try:
        ALLOWED_FIELDS = {"total_seats", "available_seats", "status", "departure_time", "departure_date"}
        sanitized = {k: v for k, v in flight_data.items() if k in ALLOWED_FIELDS}
        
        response = supabase_client.table("flights").update(sanitized).eq("id", flight_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        # If response.data is empty, re-fetch to confirm update
        refetch = supabase_client.table("flights").select("*").eq("id", flight_id).execute()
        if refetch.data:
            return refetch.data[0]
            
        return {"status": "success", "message": "Flight updated successfully"}
    except Exception as e:
        print(f"Error updating flight {flight_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def create_flight(flight_data: dict):
    try:
        airline = flight_data.get("airline", "Vietnam Airlines")
        flight_number = flight_data.get("flight_number")
        if not flight_number:
            import random
            prefixes = {
                "Vietnam Airlines": "VN",
                "VietJet Air": "VJ",
                "Bamboo Airways": "BA",
                "Vietravel Airlines": "VA"
            }
            prefix = prefixes.get(airline, "FL")
            flight_number = f"{prefix}-{random.randint(100, 999)}"

        total_seats = int(flight_data.get("total_seats", 180))
        available_seats = int(flight_data.get("available_seats", total_seats))
        
        # Calculate arrival time (e.g. +1h 45m from departure_time)
        departure_time_str = flight_data.get("departure_time")
        arrival_time_str = flight_data.get("arrival_time")
        if departure_time_str and not arrival_time_str:
            try:
                from datetime import datetime, timedelta
                dep_dt = None
                if "T" in departure_time_str:
                    dep_dt = datetime.fromisoformat(departure_time_str.replace("Z", "+00:00"))
                else:
                    dep_dt = datetime.strptime(departure_time_str, "%Y-%m-%d %H:%M:%S")
                arr_dt = dep_dt + timedelta(minutes=105) # Default 1h 45m duration
                arrival_time_str = arr_dt.isoformat()
            except Exception as parse_err:
                print(f"Failed to calculate arrival_time: {parse_err}")
                arrival_time_str = departure_time_str

        new_flight = {
            "flight_number": flight_number,
            "airline": airline,
            "origin": flight_data.get("origin", "SGN"),
            "destination": flight_data.get("destination", "HAN"),
            "departure_date": flight_data.get("departure_date"),
            "departure_time": departure_time_str,
            "arrival_time": arrival_time_str,
            "base_price": float(flight_data.get("base_price", 100.0)),
            "trip_type": flight_data.get("trip_type", "one-way"),
            "return_date": flight_data.get("return_date"),
            "total_seats": total_seats,
            "available_seats": available_seats,
            "status": flight_data.get("status", "ON TIME"),
            "flight_type": "Domestic",
            "origin_country": "VN",
            "destination_country": "VN"
        }
        
        response = supabase_client.table("flights").insert(new_flight).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=500, detail="Failed to insert flight record")
    except Exception as e:
        print(f"Error creating flight: {e}")
        raise HTTPException(status_code=500, detail=str(e))


