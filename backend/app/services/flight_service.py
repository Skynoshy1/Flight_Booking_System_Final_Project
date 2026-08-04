"""
Flight Service
Business logic for flight operations
"""
import json
from typing import List, Optional
from datetime import datetime, date
from pathlib import Path


class FlightService:
    """Service for flight-related operations"""
    
    def __init__(self):
        # Load mock data from shared-data directory
        self.data_path = Path(__file__).parent.parent.parent.parent / "shared-data" / "flights.json"
        self.flights_data = self._load_flights()
    
    def _load_flights(self):
        """Load flights from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"flights": []}
    
    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: date,
        passengers: int = 1,
        flight_class: str = "economy"
    ) -> List[dict]:
        """Search for flights matching criteria"""
        flights = self.flights_data.get("flights", [])
        
        # Filter flights
        filtered_flights = []
        for flight in flights:
            # Check origin and destination
            if flight["origin"] != origin.upper() or flight["destination"] != destination.upper():
                continue
            
            # Check date
            flight_date = datetime.fromisoformat(flight["departure_time"]).date()
            if flight_date != departure_date:
                continue
            
            # Check availability
            if flight["available_seats"] < passengers:
                continue
            
            filtered_flights.append(flight)
        
        return filtered_flights
    
    async def get_flight_by_id(self, flight_id: str) -> Optional[dict]:
        """Get flight details by ID"""
        flights = self.flights_data.get("flights", [])
        for flight in flights:
            if flight["id"] == flight_id:
                return flight
        return None
    
    async def get_seat_map(self, flight_id: str) -> Optional[dict]:
        """Get seat map for a flight"""
        flight = await self.get_flight_by_id(flight_id)
        if not flight:
            return None
        
        # Generate seat map (3-3 configuration, 20 rows)
        seats = []
        columns = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for row in range(1, 21):
            for col in columns:
                seat_number = f"{row}{col}"
                seats.append({
                    "seat_number": seat_number,
                    "seat_class": "economy" if row > 3 else "business",
                    "row_number": row,
                    "column_letter": col,
                    "is_available": True,  # Mock: all available
                    "is_window": col in ['A', 'F'],
                    "is_aisle": col in ['C', 'D'],
                    "is_exit_row": row in [10, 11],
                    "has_extra_legroom": row in [1, 10, 11],
                    "additional_price": 15.0 if row in [1, 10, 11] else 0.0
                })
        
        return {
            "flight_id": flight_id,
            "seats": seats,
            "total_seats": len(seats),
            "available_seats": flight["available_seats"]
        }
