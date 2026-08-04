from fastapi import APIRouter, HTTPException
from app.core.security import supabase_client

router = APIRouter()

@router.get("/all")
def get_all_airports():
    try:
        response = (
            supabase_client.table("airports")
            .select("*")
            .order("code", desc=False)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
