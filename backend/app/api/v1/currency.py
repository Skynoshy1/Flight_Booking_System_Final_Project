from fastapi import APIRouter

router = APIRouter()

@router.get("/rates")
def get_currency_rates():

    return {
        "base": "USD",
        "rates": {
            "VND": 25400.0,
            "SGD": 1.35,
            "THB": 36.5
        }
    }