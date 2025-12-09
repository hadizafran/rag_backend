import requests

API_KEY = "5ae2e3f221c38a28845f05b681879c1d039f825913b74a50413fc888"  # Replace with your actual key

def get_coordinates(place_name: str):
    """Convert a place name to latitude and longitude."""
    url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {
        "name": place_name,
        "apikey": API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        lat = data.get("lat")
        lon = data.get("lon")
        return lat, lon
    return None, None

def get_recommendations(lat, lon, radius=1000, limit=10):
    """Fetch nearby places from OpenTripMap based on coordinates."""
    url = "https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "radius": radius,
        "limit": limit,
        "lat": lat,
        "lon": lon,
        "apikey": API_KEY,
        "format": "json"
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        return [place["name"] for place in data if "name" in place]
    return []
