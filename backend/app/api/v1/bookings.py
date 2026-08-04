from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.core.security import supabase_client, get_current_user
from app.services.interactions_service import get_booking_likes_map, get_booking_comments_map, toggle_booking_like, add_booking_comment

router = APIRouter()


import uuid
import json
from fastapi import Request
from supabase import create_client
from app.core.security import SUPABASE_URL, SUPABASE_ANON_KEY

@router.post("")
def create_new_booking(booking_data: dict, request: Request):
    # Extract auth token
    auth_header = request.headers.get("Authorization")
    client_to_use = supabase_client
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            client_to_use = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            client_to_use.postgrest.auth(token)
        except Exception as e:
            print(f"Error initializing auth client: {e}")
            client_to_use = supabase_client

    if "booking_reference" not in booking_data:
        booking_data["booking_reference"] = f"TRV{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"

    # Force pending status initially
    booking_data["status"] = "pending"

    # Safely parse selected_seats if stringified
    if "selected_seats" in booking_data and isinstance(booking_data["selected_seats"], str):
        try:
            booking_data["selected_seats"] = json.loads(booking_data["selected_seats"])
        except Exception:
            pass

    flight_id = booking_data.get("flight_id")
    user_id = booking_data.get("user_id")
    seat_class = booking_data.get("seat_class", "Economy")
    trip_type = booking_data.get("trip_type", "one-way")

    # 1. Fetch flight details
    origin_country = "VN"
    destination_country = "VN"
    if flight_id:
        try:
            flight_res = supabase_client.table("flights").select("*").eq("id", flight_id).execute()
            if flight_res.data:
                flight = flight_res.data[0]
                origin_country = flight.get("origin_country", "VN")
                destination_country = flight.get("destination_country", "VN")
        except Exception as e:
            print(f"Error fetching flight details: {e}")

    # 2. Point calculation (we compute this but don't commit it to the profile points yet)
    base_flight_points = 0
    seat_class_points = 0

    if origin_country == 'VN' and destination_country == 'VN':
        base_flight_points = 200
    else:
        base_flight_points = 400

    seat_class_lower = str(seat_class).lower()
    if "first" in seat_class_lower or "business" in seat_class_lower:
        seat_class_points = 50
    elif "mid" in seat_class_lower or "medium" in seat_class_lower:
        seat_class_points = 30
    else:
        seat_class_points = 20

    if trip_type == 'round-trip':
        calculated_points = (base_flight_points * 2) + (seat_class_points * 2)
    else:
        calculated_points = base_flight_points + seat_class_points

    # Initialize discount variables
    discount_percent = 0.0
    discount_amount = 0.0
    original_price = 0.0
    price_key = None
    if "total_price" in booking_data:
        price_key = "total_price"
    elif "price" in booking_data:
        price_key = "price"
    
    if price_key is not None:
        try:
            original_price = float(booking_data[price_key])
        except Exception:
            original_price = 0.0
    final_price = original_price

    # 3. Calculate Discount (do not update user profile points yet)
    new_total_points = 0
    if user_id:
        try:
            profile_res = supabase_client.table("profiles").select("points").eq("id", user_id).execute()
            current_points = 0
            if profile_res.data:
                current_points = profile_res.data[0].get("points") or 0
            
            # Determine discount tier based on current_points
            if current_points >= 5000:
                discount_percent = 0.10
            elif current_points >= 2000:
                discount_percent = 0.05
            elif current_points >= 1000:
                discount_percent = 0.03
            else:
                discount_percent = 0.0

            discount_amount = original_price * discount_percent
            final_price = original_price - discount_amount

            # Update booking_data with discounted values
            if price_key is not None:
                booking_data[price_key] = final_price
                if price_key == "total_price" and "price" in booking_data:
                    booking_data["price"] = final_price
                elif price_key == "price" and "total_price" in booking_data:
                    booking_data["total_price"] = final_price
            booking_data["discount_applied"] = discount_amount

            new_total_points = current_points # No points added yet during pending creation
        except Exception as e:
            print(f"Error calculating discount: {e}")

    # 4. Save booking to the database
    ALLOWED_COLUMNS = {
        "flight_id", "user_id", "total_price", "passenger_count", "status",
        "booking_reference", "discount_applied", "selected_seats"
    }
    sanitized_booking_data = {k: v for k, v in booking_data.items() if k in ALLOWED_COLUMNS}
    booking_res = None
    try:
        booking_res = client_to_use.table("bookings").insert(sanitized_booking_data).execute()
        if not booking_res.data:
            booking_res = supabase_client.table("bookings").insert(sanitized_booking_data).execute()
    except Exception as e:
        print(f"❌ DATABASE INSERTION CRASH: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            booking_res = supabase_client.table("bookings").insert(sanitized_booking_data).execute()
        except Exception as ex:
            print(f"Fallback master saving booking failed: {ex}")

    result_data = booking_res.data[0] if (booking_res and booking_res.data) else booking_data
    result_data["new_total_points"] = new_total_points

    return {
        "status": "success",
        "message": "Booking request received successfully!",
        "received_data": result_data,
        "new_total_points": new_total_points,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "final_price": final_price
    }

@router.put("/{booking_id}/complete")
def complete_booking(booking_id: int, booking_data: dict, request: Request):
    # Extract auth token
    auth_header = request.headers.get("Authorization")
    client_to_use = supabase_client
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            client_to_use = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            client_to_use.postgrest.auth(token)
        except Exception as e:
            print(f"Error initializing auth client: {e}")
            client_to_use = supabase_client

    # Force status to completed
    booking_data["status"] = "completed"

    # Safely parse selected_seats if stringified
    if "selected_seats" in booking_data and isinstance(booking_data["selected_seats"], str):
        try:
            booking_data["selected_seats"] = json.loads(booking_data["selected_seats"])
        except Exception:
            pass

    try:
        # Fetch current booking details for points calculation
        current_booking_res = supabase_client.table("bookings").select("*").eq("id", booking_id).execute()
        if not current_booking_res.data:
            return {"status": "error", "message": "Booking not found"}
        
        booking = current_booking_res.data[0]
        user_id = booking.get("user_id")
        flight_id = booking.get("flight_id")
        seat_class = booking_data.get("seat_class") or booking.get("seat_class", "Economy")
        trip_type = booking_data.get("trip_type") or booking.get("trip_type", "one-way")

        # 1. Fetch flight details
        origin_country = "VN"
        destination_country = "VN"
        if flight_id:
            try:
                flight_res = supabase_client.table("flights").select("*").eq("id", flight_id).execute()
                if flight_res.data:
                    flight = flight_res.data[0]
                    origin_country = flight.get("origin_country", "VN")
                    destination_country = flight.get("destination_country", "VN")
            except Exception as e:
                print(f"Error fetching flight details: {e}")

        # 2. Point calculation
        base_flight_points = 0
        seat_class_points = 0

        if origin_country == 'VN' and destination_country == 'VN':
            base_flight_points = 200
        else:
            base_flight_points = 400

        seat_class_lower = str(seat_class).lower()
        if "first" in seat_class_lower or "business" in seat_class_lower:
            seat_class_points = 50
        elif "mid" in seat_class_lower or "medium" in seat_class_lower:
            seat_class_points = 30
        else:
            seat_class_points = 20

        if trip_type == 'round-trip':
            calculated_points = (base_flight_points * 2) + (seat_class_points * 2)
        else:
            calculated_points = base_flight_points + seat_class_points

        new_total_points = 0
        if user_id:
            try:
                profile_res = supabase_client.table("profiles").select("points").eq("id", user_id).execute()
                current_points = 0
                if profile_res.data:
                    current_points = profile_res.data[0].get("points") or 0
                new_total_points = current_points + calculated_points
                supabase_client.table("profiles").update({"points": new_total_points}).eq("id", user_id).execute()
            except Exception as e:
                print(f"Error updating profile points: {e}")

        # Update booking in database
        ALLOWED_COLUMNS = {
            "flight_id", "user_id", "total_price", "passenger_count", "status",
            "booking_reference", "discount_applied", "selected_seats"
        }
        sanitized_booking_data = {k: v for k, v in booking_data.items() if k in ALLOWED_COLUMNS}
        
        update_res = None
        try:
            update_res = client_to_use.table("bookings").update(sanitized_booking_data).eq("id", booking_id).execute()
            if not update_res.data:
                update_res = supabase_client.table("bookings").update(sanitized_booking_data).eq("id", booking_id).execute()
        except Exception:
            update_res = supabase_client.table("bookings").update(sanitized_booking_data).eq("id", booking_id).execute()

        result_data = update_res.data[0] if (update_res and update_res.data) else booking_data
        result_data["new_total_points"] = new_total_points

        return {
            "status": "success",
            "message": "Booking completed successfully!",
            "received_data": result_data,
            "new_total_points": new_total_points
        }
    except Exception as e:
        print(f"Error completing booking: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/my_summary")
def get_my_summary(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    if not user_id:
        return {"pending": [], "completed": []}
    
    try:
        response = (
            supabase_client.table("bookings")
            .select("*, flights(*)")
            .eq("user_id", user_id)
            .execute()
        )
        airports_res = supabase_client.table("airports").select("*").execute()
        airports_map = {ap["code"]: ap for ap in airports_res.data}
    except Exception as e:
        print(f"Error in my_summary fetch: {e}")
        return {"pending": [], "completed": []}

    likes_map = get_booking_likes_map()
    comments_map = get_booking_comments_map()

    from datetime import datetime, timezone
    current_now = datetime.now(timezone.utc)

    pending = []
    completed = []
    past = []

    for booking in response.data:
        booking_id = str(booking.get("id"))
        booking["liked"] = likes_map.get(booking_id, False)
        booking["comment"] = comments_map.get(booking_id, "")
        
        flight = booking.get("flights")
        if flight:
            dest_code = flight.get("destination")
            flight["airports"] = airports_map.get(dest_code)
        
        status = booking.get("status", "pending")
        if status == "completed":
            flight_completion_datetime = None
            if flight and flight.get("arrival_time"):
                arrival_time_str = flight["arrival_time"]
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
                    flight_completion_datetime = dt_parsed
                except Exception:
                    pass

            if flight_completion_datetime is None:
                completed.append(booking)
            else:
                if current_now < flight_completion_datetime:
                    completed.append(booking)
                else:
                    past.append(booking)
        else:
            # Check if pending booking is expired (departure time in past)
            if flight:
                dep_date = flight.get("departure_date")
                dep_time = flight.get("departure_time")
                if dep_date and dep_time:
                    try:
                        dep_dt_str = f"{dep_date} {dep_time[:5]}"
                        departure_dt = datetime.strptime(dep_dt_str, "%Y-%m-%d %H:%M")
                        if datetime.now() > departure_dt:
                            booking_id = booking.get("id")
                            print(f"Auto-deleting expired pending booking: {booking_id} (departure: {dep_dt_str})")
                            try:
                                supabase_client.table("bookings").delete().eq("id", booking_id).execute()
                            except Exception as del_err:
                                print(f"Failed to auto-delete: {del_err}")
                            continue  # Skip adding to pending list
                    except Exception as parse_err:
                        print(f"Error checking pending expiry: {parse_err}")
            pending.append(booking)

    # Get comment counts from SQLite grouped by flight_id
    comment_counts = {}
    try:
        import sqlite3
        from app.services.interactions_service import DB_PATH
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("ALTER TABLE booking_comments ADD COLUMN flight_id INTEGER")
            conn.commit()
        except sqlite3.OperationalError:
            pass
            
        cursor.execute("SELECT flight_id, COUNT(*) FROM booking_comments WHERE flight_id IS NOT NULL GROUP BY flight_id")
        comment_counts = {int(row[0]): row[1] for row in cursor.fetchall()}
        
        # Backward compatibility for NULL flight_id comments
        cursor.execute("SELECT booking_id, COUNT(*) FROM booking_comments WHERE flight_id IS NULL GROUP BY booking_id")
        null_rows = cursor.fetchall()
        if null_rows:
            null_booking_ids = [int(r[0]) for r in null_rows if r[0].isdigit()]
            if null_booking_ids:
                bookings_res = supabase_client.table("bookings").select("id, flight_id").in_("id", null_booking_ids).execute()
                for b in bookings_res.data or []:
                    fid = b.get("flight_id")
                    if fid:
                        comment_counts[fid] = comment_counts.get(fid, 0) + 1
        conn.close()
    except Exception as e:
        print(f"Error fetching comment counts: {e}")

    return {
        "pending": pending,
        "completed": completed,
        "past": past,
        "comment_counts": comment_counts
    }

@router.get("/user_active")
def get_user_active_bookings(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    return get_user_bookings(user_id)

@router.get("/user/{user_id}")
def get_user_bookings(user_id: str):
    from datetime import datetime, timezone
    current_now = datetime.now(timezone.utc)
    
    try:
        response = (
            supabase_client.table("bookings")
            .select("*, flights(*)")
            .eq("user_id", user_id)
            .execute()
        )
        airports_res = supabase_client.table("airports").select("*").execute()
        airports_map = {ap["code"]: ap for ap in airports_res.data}
    except Exception as e:
        print(f"❌ DETECTED BACKEND ERROR DURING BOOKINGS FETCH: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"active_tickets": [], "flight_history": []}
    
    active_tickets = []
    flight_history = []
    
    for booking in response.data:
        flight = booking.get("flights")
        if flight:
            dest_code = flight.get("destination")
            flight["airports"] = airports_map.get(dest_code)
        flight_completion_datetime = None
        
        if flight and flight.get("arrival_time"):
            arrival_time_str = flight["arrival_time"]
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
                flight_completion_datetime = dt_parsed
            except Exception:
                pass

        if flight_completion_datetime is None:
            active_tickets.append(booking)
        else:
            if current_now < flight_completion_datetime:
                active_tickets.append(booking)
            else:
                flight_history.append(booking)
            
    return {
        "active_tickets": active_tickets,
        "flight_history": flight_history
    }

@router.get("/admin_all")
def get_admin_bookings():
    try:
        response = (
            supabase_client.table("bookings")
            .select("*, profiles(*), flights(*)")
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"Error fetching admin bookings: {e}")
        return []

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, request: Request):
    auth_header = request.headers.get("Authorization")
    client_to_use = supabase_client
    token = None
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            client_to_use = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            client_to_use.postgrest.auth(token)
        except Exception as e:
            print(f"Error initializing auth client: {e}")
            client_to_use = supabase_client
            
    try:
        delete_res = client_to_use.table("bookings").delete().eq("id", booking_id).execute()
        if not delete_res.data:
            delete_res = supabase_client.table("bookings").delete().eq("id", booking_id).execute()
        return {"status": "success", "message": "Booking deleted successfully!"}
    except Exception as e:
        print(f"Error deleting booking: {e}")
        try:
            supabase_client.table("bookings").delete().eq("id", booking_id).execute()
            return {"status": "success", "message": "Booking deleted successfully via admin fallback!"}
        except Exception as ex:
            return {"status": "error", "message": str(ex)}

class LikeToggleRequest(BaseModel):
    liked: bool
    airline: str

class CommentSubmitRequest(BaseModel):
    comment: str
    airline: str

@router.post("/{booking_id}/like")
def toggle_like_endpoint(booking_id: str, payload: LikeToggleRequest, request: Request, current_user: dict = Depends(get_current_user)):
    try:
        new_count = toggle_booking_like(booking_id, payload.liked, payload.airline)
        
        # Synchronize with Supabase database using authenticated client to bypass RLS policies
        auth_header = request.headers.get("Authorization")
        client_to_use = supabase_client
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                client_to_use = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
                client_to_use.postgrest.auth(token)
            except Exception as auth_err:
                print(f"Error authenticating client for like toggle: {auth_err}")
                client_to_use = supabase_client

        user_id = current_user.get("user_id")
        if user_id:
            if payload.liked:
                # Check if it already exists by booking_id to prevent duplicate key violations
                exist_res = client_to_use.table("airline_likes").select("*").eq("booking_id", booking_id).execute()
                if not exist_res.data:
                    client_to_use.table("airline_likes").insert({
                        "user_id": user_id,
                        "airline_name": payload.airline,
                        "booking_id": booking_id
                    }).execute()
            else:
                client_to_use.table("airline_likes").delete().eq("booking_id", booking_id).execute()
                
        return {"status": "success", "liked": payload.liked, "airline": payload.airline, "total_airline_likes": new_count}
    except Exception as e:
        print(f"Error in toggle_like_endpoint Supabase sync: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/comment")
def submit_comment_endpoint(booking_id: str, payload: CommentSubmitRequest, current_user: dict = Depends(get_current_user)):
    try:
        # Fetch flight_id from Supabase bookings table
        flight_id = None
        if booking_id.isdigit():
            booking_res = supabase_client.table("bookings").select("flight_id").eq("id", int(booking_id)).execute()
            if booking_res.data:
                flight_id = booking_res.data[0].get("flight_id")
                
        add_booking_comment(booking_id, payload.comment, payload.airline, flight_id=flight_id)
        return {"status": "success", "comment": payload.comment, "airline": payload.airline, "flight_id": flight_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comments/list")
def get_flight_comments(flight_id: int):
    try:
        import sqlite3
        from app.services.interactions_service import DB_PATH
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Ensure columns exist
        try:
            cursor.execute("ALTER TABLE booking_comments ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
        except sqlite3.OperationalError:
            pass
        try:
            cursor.execute("ALTER TABLE booking_comments ADD COLUMN flight_id INTEGER")
            conn.commit()
        except sqlite3.OperationalError:
            pass
            
        cursor.execute("SELECT booking_id, comment, created_at FROM booking_comments WHERE flight_id = ?", (flight_id,))
        rows = cursor.fetchall()
        
        # Backward compatibility check: check bookings table for NULL flight_id comments
        if not rows:
            cursor.execute("SELECT booking_id, comment, created_at FROM booking_comments WHERE flight_id IS NULL")
            all_null_rows = cursor.fetchall()
            if all_null_rows:
                null_booking_ids = [int(r[0]) for r in all_null_rows if r[0].isdigit()]
                if null_booking_ids:
                    bookings_res = supabase_client.table("bookings").select("id, flight_id").in_("id", null_booking_ids).execute()
                    valid_booking_ids = {str(b["id"]) for b in bookings_res.data or [] if b.get("flight_id") == flight_id}
                    rows = [r for r in all_null_rows if r[0] in valid_booking_ids]
                    
        conn.close()
        
        if not rows:
            return {"status": "success", "comments": []}
            
        # Get booking details from Supabase to match user profiles
        booking_ids = [int(row[0]) for row in rows if row[0].isdigit()]
        
        bookings_map = {}
        if booking_ids:
            bookings_res = supabase_client.table("bookings").select("id, user_id").in_("id", booking_ids).execute()
            user_ids = []
            booking_to_user = {}
            for b in bookings_res.data or []:
                u_id = b.get("user_id")
                if u_id:
                    user_ids.append(u_id)
                    booking_to_user[str(b["id"])] = u_id
            
            profiles_map = {}
            if user_ids:
                profiles_res = supabase_client.table("profiles").select("id, username, avatar_url").in_("id", user_ids).execute()
                for p in profiles_res.data or []:
                    profiles_map[p["id"]] = p
            
            for b_id, u_id in booking_to_user.items():
                if u_id in profiles_map:
                    bookings_map[b_id] = profiles_map[u_id]
                    
        comments_data = []
        for row in rows:
            b_id = row[0]
            prof = bookings_map.get(b_id, {})
            comments_data.append({
                "booking_id": b_id,
                "comment": row[1],
                "created_at": row[2],
                "username": prof.get("username") or "Explorer",
                "avatar_url": prof.get("avatar_url") or ""
            })
                
        return {"status": "success", "comments": comments_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/airline_likes")
def get_all_airline_likes():
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

        # 2. Fetch all likes from SQLite
        import sqlite3
        from app.services.interactions_service import DB_PATH
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT booking_id, airline FROM booking_likes WHERE liked = 1")
        rows = cursor.fetchall()
        conn.close()

        # 3. Aggregate likes only for past bookings
        likes_count_map = {}
        for row in rows:
            booking_id = str(row[0])
            airline = row[1]
            if booking_id in past_booking_ids:
                likes_count_map[airline] = likes_count_map.get(airline, 0) + 1

        # Also initialize known airlines to 0 if not present to keep the chart clean
        for airline in ["VietJet Air", "Bamboo Airways", "Vietravel Airlines", "Vietnam Airlines"]:
            if airline not in likes_count_map:
                likes_count_map[airline] = 0

        return likes_count_map
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))