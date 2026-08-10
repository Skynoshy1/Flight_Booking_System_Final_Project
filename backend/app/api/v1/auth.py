from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from typing import Optional
import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.security import get_current_user, verify_admin, supabase_client, SUPABASE_URL, SUPABASE_ANON_KEY
from app.core.database import get_db

router = APIRouter()

class PasswordUpdate(BaseModel):
    new_password: str


class UserAuth(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    username: str
    phone: str
    region: str
    national_id: str
    avatar_url: str
    redirect_to: Optional[str] = None

@router.post("/signup")
def sign_up(data: UserRegister):
    try:
        # Call Supabase auth sign up with options if redirect_to is provided
        signup_params = {"email": data.email, "password": data.password}
        if data.redirect_to:
            signup_params["options"] = {"email_redirect_to": data.redirect_to}
            
        response = supabase_client.auth.sign_up(signup_params)
        user = response.user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register user. No user returned."
            )
        
        # Admin assignment check
        admin_list = ["admin", "superadmin", "manager_2026"]
        role = "admin" if data.username in admin_list else "user"
        
        # Upsert profile with the extra fields
        supabase_client.table("profiles").upsert({
            "id": user.id,
            "username": data.username,
            "email": data.email,
            "role": role,
            "phone": data.phone,
            "region": data.region,
            "national_id": data.national_id,
            "avatar_url": data.avatar_url
        }).execute()
        
        return {
            "status": "success",
            "message": "User registered successfully!",
            "user_id": user.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/signin")
def sign_in(data: UserAuth):
    try:
        # Call Supabase sign in with password
        response = supabase_client.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })
        session = response.session
        user = response.user
        
        if not session or not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials"
            )
            
        # Get username, role, and avatar_url from profiles table
        profile_res = supabase_client.table("profiles").select("username, role, avatar_url").eq("id", user.id).execute()
        username = "Explorer"
        role = "user"
        avatar_url = ""
        if profile_res.data and len(profile_res.data) > 0:
            username = profile_res.data[0].get("username", "Explorer")
            role = profile_res.data[0].get("role", "user")
            avatar_url = profile_res.data[0].get("avatar_url", "")
            
        return {
            "access_token": session.access_token,
            "user_id": user.id,
            "email": user.email,
            "username": username,
            "role": role,
            "avatar_url": avatar_url
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

@router.get("/me")
def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user profile
    """
    try:
        profile_res = supabase_client.table("profiles").select("*").eq("id", current_user["user_id"]).execute()
        if profile_res.data:
            current_user.update(profile_res.data[0])
    except Exception as e:
        print(f"Error fetching profile details for /me: {e}")
        
    return {
        "status": "success",
        "message": "User authenticated successfully",
        "user_info": current_user
    }

@router.get("/admin-only")
def test_admin_endpoint(admin: dict = Depends(verify_admin)):
    """
    Restricted endpoint for admin role only
    """
    return {
        "status": "success",
        "message": "Admin access granted",
        "admin_info": admin
    }

class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    birthDay: Optional[str] = None
    birthMonth: Optional[str] = None
    birthYear: Optional[str] = None

@router.put("/me")
def update_profile(data: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    update_data = {}
    if data.username is not None:
        update_data["username"] = data.username
        update_data["full_name"] = data.username
    if data.gender is not None:
        update_data["gender"] = data.gender
    if data.city is not None:
        update_data["city"] = data.city
    if data.birthDay is not None:
        update_data["birthDay"] = data.birthDay
    if data.birthMonth is not None:
        update_data["birthMonth"] = data.birthMonth
    if data.birthYear is not None:
        update_data["birthYear"] = data.birthYear
        
    if not update_data:
        return {"status": "success", "message": "No changes to update"}
        
    try:
        response = supabase_client.table("profiles").update(update_data).eq("id", user_id).execute()
        return {
            "status": "success",
            "message": "Profile updated successfully",
            "user_info": response.data[0] if response.data else {}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update profile: {str(e)}"
        )

@router.put("/password")
def change_password(
    data: PasswordUpdate, 
    current_user: dict = Depends(get_current_user),
    authorization: str = Header(...)
):
    token = authorization.replace("Bearer ", "")
    try:
        # Request update to Supabase Auth API
        url = f"{SUPABASE_URL}/auth/v1/user"
        headers = {
            "Authorization": f"Bearer {token}",
            "apikey": SUPABASE_ANON_KEY
        }
        res = httpx.put(url, json={"password": data.new_password}, headers=headers)
        if res.status_code != 200:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Failed to update password: {res.text}"
            )
        
        return {
            "status": "success",
            "message": "Password updated successfully"
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update password: {str(e)}"
        )

@router.delete("/me")
def delete_user_account(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    try:
        # Perform cascade deletion inside a database transaction
        db.execute(text("DELETE FROM airline_likes WHERE user_id = :user_id"), {"user_id": user_id})
        db.execute(text("DELETE FROM reviews WHERE user_id = :user_id"), {"user_id": user_id})
        db.execute(text("DELETE FROM bookings WHERE user_id = :user_id"), {"user_id": user_id})
        db.execute(text("DELETE FROM profiles WHERE id = :user_id"), {"user_id": user_id})
        db.execute(text("DELETE FROM auth.users WHERE id = :user_id"), {"user_id": user_id})
        db.commit()
        
        return {
            "status": "success",
            "message": "Account and all associated data deleted successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete account: {str(e)}"
        )