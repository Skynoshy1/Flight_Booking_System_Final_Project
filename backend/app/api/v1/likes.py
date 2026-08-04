from fastapi import APIRouter, Depends, Query
from app.core.security import supabase_client

router = APIRouter()

@router.get("/status")
def get_like_status(user_id: str = Query(None), airline_name: str = Query(None), booking_id: int = Query(None)):
    try:
        query = supabase_client.table("airline_likes").select("*")
        if booking_id is not None:
            query = query.eq("booking_id", booking_id)
        else:
            if user_id:
                query = query.eq("user_id", user_id)
            if airline_name:
                query = query.eq("airline_name", airline_name)
                
        response = query.execute()
        is_liked = len(response.data) > 0 if response.data else False
        return {"is_liked": is_liked}
    except Exception as e:
        print(f"Error fetching like status: {e}")
        return {"is_liked": False}

@router.get("/summary")
def get_likes_summary():
    try:
        from datetime import datetime, timezone
        current_now = datetime.now(timezone.utc)
        
        # 1. Fetch all completed bookings from Supabase
        response = (
            supabase_client.table("bookings")
            .select("*, flights(*)")
            .eq("status", "completed")
            .execute()
        )
        
        past_booking_ids = set()
        for booking in response.data:
            flight = booking.get("flights")
            if not flight:
                continue
            arrival_time_str = flight.get("arrival_time")
            if not arrival_time_str:
                continue
            try:
                dt_parsed = datetime.fromisoformat(str(arrival_time_str))
                base_date_str = booking.get("departure_date") or flight.get("departure_date")
                if base_date_str:
                    try:
                        date_parsed = datetime.fromisoformat(str(base_date_str))
                        dt_parsed = dt_parsed.replace(
                            year=date_parsed.year,
                            month=date_parsed.month,
                            day=date_parsed.day
                        )
                    except Exception:
                        pass
                
                if dt_parsed.tzinfo is None:
                    dt_parsed = dt_parsed.replace(tzinfo=timezone.utc)
                
                if current_now >= dt_parsed:
                    past_booking_ids.add(str(booking.get("id")))
            except Exception:
                pass

        # 2. Fetch all likes from Supabase
        likes_res = supabase_client.table("airline_likes").select("*").execute()

        # 3. Aggregate likes only for past bookings
        likes_count_map = {}
        for like in likes_res.data:
            booking_id = str(like.get("booking_id"))
            airline = like.get("airline_name")
            if booking_id in past_booking_ids:
                likes_count_map[airline] = likes_count_map.get(airline, 0) + 1

        summary = []
        for airline in ["VietJet Air", "Bamboo Airways", "Vietravel Airlines", "Vietnam Airlines"]:
            summary.append({
                "airline": airline,
                "like_count": likes_count_map.get(airline, 0)
            })

        return summary
    except Exception as e:
        import traceback
        traceback.print_exc()
        return []
