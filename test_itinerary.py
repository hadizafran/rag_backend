# test_itinerary.py
import os
from google.oauth2 import service_account
from google.api_core.client_options import ClientOptions
from google.generativeai import TextGenerationServiceClient

# --- STEP 1: Set your service account JSON path ---
# Option 1: use environment variable
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\flutter_projects\travel_assistant\backend\service_account.json"

# Option 2: hardcode path directly
SERVICE_ACCOUNT_FILE = r"C:\flutter_projects\travel_assistant\backend\service_account.json"

# --- STEP 2: Authenticate ---
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# --- STEP 3: Initialize Gemini (Text-Bison) client ---
client_options = ClientOptions(api_endpoint="generativeai.googleapis.com")
client = TextGenerationServiceClient(credentials=credentials, client_options=client_options)

# --- STEP 4: Function to generate itinerary ---
def generate_itinerary(place_name):
    prompt = f"""
    Create a detailed travel itinerary for {place_name}.
    Include morning, afternoon, and evening activities, recommended sights, food, and local experiences.
    Keep it concise but informative.
    """
    try:
        response = client.generate_text(
            model="text-bison-001",
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=400
        )
        return response.text
    except Exception as e:
        print("Gemini API error:", e)
        return f"Could not generate detailed itinerary for {place_name}."

# --- STEP 5: Test with a city/place ---
if __name__ == "__main__":
    place = input("Enter a city or place: ").strip()
    itinerary = generate_itinerary(place)
    print("\nGenerated Itinerary:\n")
    print(itinerary)
