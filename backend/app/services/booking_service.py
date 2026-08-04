"""
Booking Service
Business logic for booking operations with seat locking
"""
import uuid
from datetime import datetime
from typing import Optional
from ..schemas.booking import BookingCreate, PaymentRequest


class BookingService:
    """Service for booking-related operations"""
    
    def __init__(self):
        # In-memory storage for demo (use database in production)
        self.bookings = {}
        self.locked_seats = {}
    
    async def create_booking(self, booking_data: BookingCreate) -> dict:
        """Create a new booking with seat locking"""
        # Generate booking ID and reference
        booking_id = str(uuid.uuid4())
        booking_reference = f"TRV{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
        
        # Check seat availability (mock implementation)
        for seat in booking_data.selected_seats:
            if seat in self.locked_seats:
                raise ValueError(f"Seat {seat} is already booked")
        
        # Lock seats
        for seat in booking_data.selected_seats:
            self.locked_seats[seat] = booking_id
        
        # Calculate total price (mock)
        base_price = 150.0  # USD per seat
        total_price = base_price * len(booking_data.selected_seats)
        
        # Create booking
        booking = {
            "id": booking_id,
            "booking_reference": booking_reference,
            "flight_id": booking_data.flight_id,
            "passenger_name": booking_data.passenger_name,
            "passenger_email": booking_data.passenger_email,
            "passenger_phone": booking_data.passenger_phone,
            "passenger_count": booking_data.passenger_count,
            "selected_seats": booking_data.selected_seats,
            "total_price": total_price,
            "currency": "USD",
            "payment_status": "pending",
            "booking_status": "confirmed",
            "created_at": datetime.utcnow()
        }
        
        self.bookings[booking_id] = booking
        return booking
    
    async def process_payment(self, booking_id: str, payment_data: PaymentRequest) -> dict:
        """Process payment for a booking"""
        booking = self.bookings.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        
        # Mock payment processing
        booking["payment_status"] = "completed"
        booking["payment_method"] = payment_data.payment_method
        booking["payment_id"] = str(uuid.uuid4())
        
        return booking
    
    async def get_booking(self, booking_id: str) -> Optional[dict]:
        """Get booking details"""
        return self.bookings.get(booking_id)
    
    async def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking and release seats"""
        booking = self.bookings.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        
        # Release seats
        for seat in booking["selected_seats"]:
            if seat in self.locked_seats:
                del self.locked_seats[seat]
        
        # Update booking status
        booking["booking_status"] = "cancelled"
        return True
