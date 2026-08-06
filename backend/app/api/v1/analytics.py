from fastapi import APIRouter, HTTPException
from app.core.security import supabase_client

router = APIRouter()

@router.get("/admin")
def get_admin_analytics():
    try:
        response = (
            supabase_client.table("reviews")
            .select("rating, bookings(flights(airline, flight_type))")
            .execute()
        )
        
        stats = {}
        
        for item in response.data:
            rating = item.get("rating")
            if rating is None:
                continue
                
            booking = item.get("bookings")
            if not booking:
                continue
                
            if isinstance(booking, list):
                if not booking:
                    continue
                booking = booking[0]
                
            flight = booking.get("flights")
            if not flight:
                continue
                
            if isinstance(flight, list):
                if not flight:
                    continue
                flight = flight[0]
                
            airline = flight.get("airline")
            if not airline:
                continue
                
            flight_type = flight.get("flight_type", "Domestic")
            
            if airline not in stats:
                stats[airline] = {
                    "ratings": [],
                    "domestic": [],
                    "intl": []
                }
                
            stats[airline]["ratings"].append(rating)
            
            ftype_lower = str(flight_type).lower() if flight_type else ""
            if "intl" in ftype_lower or "international" in ftype_lower:
                stats[airline]["intl"].append(rating)
            else:
                stats[airline]["domestic"].append(rating)
                
        airlines = []
        avg_ratings = []
        total_reviews = []
        domestic_avg = []
        intl_avg = []
        
        for airline, data in stats.items():
            airlines.append(airline)
            total_reviews.append(len(data["ratings"]))
            
            avg_val = round(sum(data["ratings"]) / len(data["ratings"]), 2) if data["ratings"] else 0.0
            avg_ratings.append(avg_val)
            
            dom_val = round(sum(data["domestic"]) / len(data["domestic"]), 2) if data["domestic"] else 0.0
            domestic_avg.append(dom_val)
            
            intl_val = round(sum(data["intl"]) / len(data["intl"]), 2) if data["intl"] else 0.0
            intl_avg.append(intl_val)
            
        return {
            "airlines": airlines,
            "avg_ratings": avg_ratings,
            "total_reviews": total_reviews,
            "domestic_avg": domestic_avg,
            "intl_avg": intl_avg
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard-stats")
def get_dashboard_stats():
    try:
        bookings_resp = supabase_client.table("bookings").select("total_price").execute()
        bookings_data = bookings_resp.data or []
        
        total_revenue = sum(float(b.get("total_price") or 0.0) for b in bookings_data)
        total_bookings = len(bookings_data)
        
        flights_resp = supabase_client.table("flights").select("status").execute()
        flights_data = flights_resp.data or []
        
        active_flights = sum(
            1 for f in flights_data
            if str(f.get("status") or "").upper() not in ("CANCELED", "CANCELLED")
        )
        
        avg_booking_value = (total_revenue / total_bookings) if total_bookings > 0 else 0.0
        
        return {
            "total_revenue": round(total_revenue, 2),
            "active_flights": active_flights,
            "total_bookings": total_bookings,
            "avg_booking_value": round(avg_booking_value, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/revenue-weekly")
def get_weekly_revenue():
    try:
        from datetime import datetime, timedelta
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        
        response = (
            supabase_client.table("bookings")
            .select("total_price, created_at")
            .execute()
        )
        
        revenue_map = {d: 0.0 for d in dates}
        for b in response.data:
            created_at = b.get("created_at")
            if created_at:
                date_str = created_at.split("T")[0]
                if date_str in revenue_map:
                    revenue_map[date_str] += float(b.get("total_price") or 0.0)
                    
        return [{"date": d, "amount": round(revenue_map[d], 2)} for d in dates]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/flight-type-popularity")
def get_flight_type_popularity():
    try:
        response = (
            supabase_client.table("bookings")
            .select("flight_id, flights(trip_type)")
            .execute()
        )
        
        one_way_count = 0
        round_trip_count = 0
        
        for b in response.data or []:
            flight_info = b.get("flights")
            trip_type = "one-way"
            if flight_info:
                if isinstance(flight_info, list) and len(flight_info) > 0:
                    trip_type = flight_info[0].get("trip_type", "one-way")
                elif isinstance(flight_info, dict):
                    trip_type = flight_info.get("trip_type", "one-way")
            
            trip_type_clean = str(trip_type).strip().lower()
            if "round" in trip_type_clean or "round-trip" in trip_type_clean:
                round_trip_count += 1
            else:
                one_way_count += 1
                
        return {
            "one_way": one_way_count,
            "round_trip": round_trip_count,
            "total": one_way_count + round_trip_count
        }
    except Exception as e:
        print(f"Error getting flight type popularity: {e}")
        raise HTTPException(status_code=500, detail=str(e))

