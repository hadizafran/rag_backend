# rag_server_async_google.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import os
from dotenv import load_dotenv
import asyncio

# --- Load environment variables ---
load_dotenv()
NEW_GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# --- FastAPI app ---
app = FastAPI()

# Allow Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load local travel knowledge ---
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "travel_knowledge.json")
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            local_travel_data = json.load(f)
        except json.JSONDecodeError:
            local_travel_data = []
else:
    local_travel_data = []

# --- Async Google Places helpers ---
async def get_coordinates(place_name: str):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": place_name,
        "inputtype": "textquery",
        "fields": "geometry",
        "key": NEW_GOOGLE_PLACES_API_KEY
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
    if data.get("candidates"):
        loc = data["candidates"][0]["geometry"]["location"]
        return loc.get("lat"), loc.get("lng")
    return None, None

async def get_places_near(lat, lon, radius=3000, limit=3):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": NEW_GOOGLE_PLACES_API_KEY,
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": "tourist_attraction"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()
    places = []
    for place in data.get("results", []):
        if "name" in place:
            photo_ref = place.get("photos", [{}])[0].get("photo_reference")
            image_url = None
            if photo_ref:
                image_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={NEW_GOOGLE_PLACES_API_KEY}"
            places.append({
                "name": place["name"],
                "rating": place.get("rating", 4.5),
                "image": image_url
            })
        if len(places) >= limit:
            break
    return places

# --- Main endpoint ---
@app.get("/recommend")
async def recommend(destination: str):
    if not destination:
        return {"recommendations": []}

    # 1. Local recommendations
    local_recs = [
        {"name": str(item.get("title")), "rating": 4.5, "image": item.get("image", None)}
        for item in local_travel_data
        if destination.lower() in str(item.get("city", "")).lower()
    ]

    # 2. Google recommendations (async)
    lat, lon = await get_coordinates(destination)
    google_recs = []
    if lat is not None and lon is not None:
        google_recs = await get_places_near(lat, lon)

    # 3. Combine and deduplicate
    all_recs = local_recs.copy()
    for place in google_recs:
        if place["name"] not in [r["name"] for r in all_recs]:
            all_recs.append(place)

    if not all_recs:
        all_recs = [{"name": "No places found", "rating": 0, "image": None}]

    return {"recommendations": all_recs}
