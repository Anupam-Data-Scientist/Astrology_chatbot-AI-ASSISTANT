# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# def get_full_horoscope(dob: str, tob: str, place: str) -> str:
#     url = "https://astroapi.dev/api/v1/horoscope/daily"  # ✅ Replace with correct endpoint

#     headers = {
#         "Authorization": f"Bearer {os.getenv('ASTRO_API_KEY')}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "birth_date": dob,
#         "birth_time": tob,
#         "birth_place": place
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 200:
#         data = response.json()
#         return data.get("horoscope", "No horoscope found.")
#     else:
#         print("Astrology API Error:", response.status_code, response.text)
#         return "Unable to fetch horoscope at the moment."

# backend/services/astrology_api.py

# backend/services/astrology_api.py

import requests
from datetime import datetime
from geopy.geocoders import Nominatim

def get_full_horoscope(dob: str, tob: str, place: str) -> dict:
    try:
        print("📥 Parsing DOB and TOB...")
        # Combine date and time into datetime object
        dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")

        print(f"📍 Looking up coordinates for: {place}")
        # Convert place name to lat/lon using geopy
        geolocator = Nominatim(user_agent="astro_chatbot")
        location = geolocator.geocode(place, timeout=10)
        if location is None:
            return {"error": f"Could not find location for '{place}'"}

        payload = {
            "year": dt.year,
            "month": dt.month,
            "day": dt.day,
            "hour": dt.hour,
            "minute": dt.minute,
            "second": 0,
            "timezone": "Asia/Kolkata",
            "dst": False,
            "place": place,
            "lat": location.latitude,
            "lon": location.longitude
        }

        print("🚀 Sending request to AstroAPI...")
        headers = {
            "Authorization": "Token a24cf4584aa36fe4f38c0a1f54b6fbd64692ae67",  # 🔐 Replace with os.getenv in prod
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://astroapi.dev/api/vedic/v0/kundali/",
            json=payload,
            headers=headers,
            timeout=20
        )

        print(f"📨 API Response Status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ AstroAPI Error:", response.status_code, response.text)
            return {
                "error": f"Astrology API Error {response.status_code}: {response.text}"
            }

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return {"error": str(e)}



