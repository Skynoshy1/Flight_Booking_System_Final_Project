"""
Booking Pydantic Schemas
Data validation and serialization models
"""
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime


class BookingCreate(BaseModel):
    """Booking creation request"""
    flight_id: str = Field(..., description="Flight ID")
    passenger_name: str = Field(..., min_length=2, description="Passenger full name")
    passenger_email: EmailStr = Field(..., description="Passenger email")
    passenger_phone: str = Field(..., description="Passenger phone number")
    passenger_count: int = Field(1, ge=1, le=9, description="Number of passengers")
    selected_seats: List[str] = Field(..., description="List of selected seat numbers")


class PaymentRequest(BaseModel):
    """Payment processing request"""
    payment_method: str = Field(..., description="Payment method (credit_card, paypal, etc.)")
    card_number: str = Field(None, description="Card number (if applicable)")
    card_holder: str = Field(None, description="Card holder name")
    cvv: str = Field(None, description="CVV code")
    expiry_date: str = Field(None, description="Card expiry date")


class BookingResponse(BaseModel):
    """Booking response model"""
    id: str
    booking_reference: str
    flight_id: str
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    passenger_count: int
    selected_seats: List[str]
    total_price: float
    currency: str
    payment_status: str
    booking_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
