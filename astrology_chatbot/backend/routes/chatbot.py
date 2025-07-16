from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.astrology_api import get_full_horoscope

chatbot_router = APIRouter()

class HoroscopeRequest(BaseModel):
    dob: str           # e.g., "1995-06-23"
    tob: str           # e.g., "14:30"
    place: str         # e.g., "Kolkata, India"

@chatbot_router.post("/daily-horoscope")
async def daily_horoscope(request: HoroscopeRequest):
    dob = request.dob
    tob = request.tob
    place = request.place

    data = get_full_horoscope(dob, tob, place)

    if "error" in data:
        return {
            "dob": dob,
            "tob": tob,
            "place": place,
            "error": data["error"]
        }

    basic = data.get("basicDetails", {})

    return {
        "dob": dob,
        "tob": tob,
        "place": place,
        "kundli_summary": {
            "ayanamsha": basic.get("ayanamsha"),
            "tithi": basic.get("tithi"),
            "vaar": basic.get("vaarH"),
            "nakshatra_number": basic.get("nakshatra", [None])[0],
            "nakshatra_pada": basic.get("nakshatra", [None, None])[1],
            "paksha": basic.get("paksha"),
            "maah_solar": basic.get("maahSolar"),
            "maah_lunar_amant": basic.get("maahLunarAmant"),
            "ritu": basic.get("ritu"),
            "ayan": basic.get("ayan"),
            "gol": basic.get("gol"),
            "sunrise": basic.get("sunrise"),
            "sunset": basic.get("sunset"),
            "moonrise": basic.get("moonrise"),
            "moonset": basic.get("moonset")
        }
    }
