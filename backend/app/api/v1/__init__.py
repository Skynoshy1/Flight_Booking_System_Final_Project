"""
API v1 Router Configuration
"""
from fastapi import APIRouter
from .flights import router as flights_router
from .bookings import router as bookings_router
from .currency import router as currency_router
from .auth import router as auth_router
from .reviews import router as reviews_router
from .analytics import router as analytics_router
from .airports import router as airports_router
from .likes import router as likes_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(flights_router, prefix="/flights", tags=["flights"])
api_router.include_router(bookings_router, prefix="/bookings", tags=["bookings"])
api_router.include_router(currency_router, prefix="/currency", tags=["currency"])
api_router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(airports_router, prefix="/airports", tags=["airports"])
api_router.include_router(likes_router, prefix="/likes", tags=["likes"])