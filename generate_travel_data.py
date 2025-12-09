import requests
import json
import os

API_KEY = "AIzaSyDB4DIQRn0hlzZ7hL-zcu8b8xEUPxXqkxA"
cities = ["Paris", "Tokyo", "New York", "London", "Rome"]
os.makedirs("data", exist_ok=True)

travel_data = []

for city in cities:
    print(f"Fetching data for {city}...")
    geo_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    geo_params = {
        "input": city,
        "inputtype": "textquery",
        "fields": "geometry",
        "key": API_KEY
    }
    geo_resp = requests.get(geo_url, params=geo_params).json()
    if not geo_resp.get("candidates"):
        print(f"  ⚠️ City {city} not found. Skipping...")
        continue
    loc = geo_resp["candidates"][0]["geometry"]["location"]
    lat, lng = loc["lat"], loc["lng"]

    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    places_params = {
        "key": API_KEY,
        "location": f"{lat},{lng}",
        "radius": 5000,
        "type": "tourist_attraction"
    }
    places_resp = requests.get(places_url, params=places_params).json()
    results = places_resp.get("results", [])

    for place in results[:10]:
        travel_data.append({
            "id": place.get("place_id"),
            "title": place.get("name"),
            "city": city,
            "text": place.get("vicinity", "")
        })

with open("data/travel_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(travel_data, f, ensure_ascii=False, indent=4)

print(f"✅ Saved {len(travel_data)} places to data/travel_knowledge.json")
