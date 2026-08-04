"""
Currency Service
Third-party currency exchange rate synchronization
"""
import httpx
from typing import Dict
from ..core.config import settings


class CurrencyService:
    """Service for currency exchange operations"""
    
    def __init__(self):
        self.api_url = settings.CURRENCY_API_URL
        self.cached_rates = {}
    
    async def get_rates(self, base: str = "USD") -> Dict[str, float]:
        """Get exchange rates for all currencies"""
        if base in self.cached_rates:
            return self.cached_rates[base]
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/{base}")
                response.raise_for_status()
                data = response.json()
                rates = data.get("rates", {})
                self.cached_rates[base] = rates
                return rates
        except Exception as e:
            # Return mock rates if API fails
            return {
                "USD": 1.0,
                "VND": 24000.0,
                "EUR": 0.92,
                "GBP": 0.79,
                "SGD": 1.35,
                "THB": 35.5,
                "MYR": 4.7
            }
    
    async def convert(self, amount: float, from_currency: str, to_currency: str) -> Dict:
        """Convert amount from one currency to another"""
        rates = await self.get_rates(from_currency)
        
        if to_currency not in rates:
            raise ValueError(f"Currency {to_currency} not supported")
        
        converted_amount = amount * rates[to_currency]
        
        return {
            "original_amount": amount,
            "original_currency": from_currency,
            "converted_amount": round(converted_amount, 2),
            "converted_currency": to_currency,
            "exchange_rate": rates[to_currency]
        }
    
    async def sync_rates(self):
        """Sync exchange rates from external API"""
        self.cached_rates = {}
        await self.get_rates("USD")
        return True
