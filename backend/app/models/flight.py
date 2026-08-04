"""
Flight Database Model
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime


class Flight(Base):
    """Flight model representing a scheduled flight"""
    __tablename__ = "flights"
    
    id = Column(String, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True, nullable=False)
    airline = Column(String, nullable=False)
    airline_code = Column(String, nullable=False)
    
    # Route information
    origin = Column(String, nullable=False)
    origin_city = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    destination_city = Column(String, nullable=False)
    
    # Schedule
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    # Aircraft
    aircraft_type = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    
    # Pricing
    price_economy = Column(Float, nullable=False)
    price_business = Column(Float, nullable=True)
    price_first = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    
    # Availability
    available_seats = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Additional info
    baggage_allowance = Column(String, nullable=True)
    meal_service = Column(Boolean, default=True)
    wifi_available = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
