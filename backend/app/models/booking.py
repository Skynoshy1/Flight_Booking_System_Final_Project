"""
Booking Database Model
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime


class Booking(Base):
    """Booking model for flight reservations"""
    __tablename__ = "bookings"
    
    id = Column(String, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, index=True, nullable=False)
    
    # Flight information
    flight_id = Column(String, nullable=False)
    
    # Passenger information
    passenger_name = Column(String, nullable=False)
    passenger_email = Column(String, nullable=False)
    passenger_phone = Column(String, nullable=False)
    passenger_count = Column(Integer, nullable=False, default=1)
    
    # Seat selection
    selected_seats = Column(JSON, nullable=False)  # List of seat numbers
    
    # Pricing
    total_price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    
    # Payment
    payment_status = Column(String, default="pending")  # pending, completed, failed, refunded
    payment_method = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)
    
    # Status
    booking_status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
