import requests

# Your OpenTripMap API Key
API_KEY = "5ae2e3f221c38a28845f05b681879c1d039f825913b74a50413fc888"

class RecommendationService:
    def __init__(self):
        self.api_key = API_KEY

    def get_places(self, lat, lon, radius=5000, limit=20):
        url = "https://api.opentripmap.com/0.1/en/places/radius"
        params = {
            "apikey": self.api_key,
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "limit": limit,
            "format": "json"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            places = response.json()
            # Simplify the data for frontend
            return [place.get("name", "Unknown") for place in places]
        else:
            return []
