# test_env.py
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read keys
openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_PLACES_API_KEY")

print("OpenAI Key:", openai_key)
print("Google Places Key:", google_key)
