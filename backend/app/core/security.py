import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
security_bearer = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    token = credentials.credentials
    try:
        auth_response = supabase_client.auth.get_user(token)
        user = auth_response.user
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
            
        profile_response = supabase_client.table("profiles").select("role").eq("id", user.id).single().execute()
        user_role = profile_response.data.get("role", "user")
        
        return {
            "user_id": user.id,
            "email": user.email,
            "role": user_role
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )

def verify_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    return current_user