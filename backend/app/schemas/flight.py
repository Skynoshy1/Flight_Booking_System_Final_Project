"""
Flight Pydantic Schemas
Data validation and serialization models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class FlightSearchParams(BaseModel):
    """Flight search parameters"""
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    departure_date: date = Field(..., description="Departure date")
    passengers: int = Field(1, ge=1, le=9, description="Number of passengers")
    flight_class: str = Field("economy", description="Flight class")


class FlightResponse(BaseModel):
    """Flight response model"""
    id: str
    flight_number: str
    airline: str
    airline_code: str
    origin: str
    origin_city: str
    destination: str
    destination_city: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    aircraft_type: str
    total_seats: int
    available_seats: int
    price_economy: float
    price_business: Optional[float] = None
    price_first: Optional[float] = None
    currency: str = "USD"
    baggage_allowance: Optional[str] = None
    meal_service: bool = True
    wifi_available: bool = False
    
    class Config:
        from_attributes = True


class SeatResponse(BaseModel):
    """Seat response model"""
    seat_number: str
    seat_class: str
    row_number: int
    column_letter: str
    is_available: bool
    is_window: bool
    is_aisle: bool
    is_exit_row: bool
    has_extra_legroom: bool
    additional_price: float = 0.0
