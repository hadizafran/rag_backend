import os
import google.generativeai as genai

# Load Gemini API key
genai.api_key = os.getenv("GEMINI_API_KEY")

def generate_itinerary(place):
    try:
        result = genai.TextCompletion.create(
            model="text-bison-001",
            prompt=f"Generate a detailed 1-day travel itinerary for tourists visiting {place}. Include morning, afternoon, evening, food, and estimated times in readable paragraphs."
        )
        return result.output[0].content
    except Exception as e:
        print("Gemini API error:", e)
        return None

if __name__ == "__main__":
    itinerary = generate_itinerary("Tokyo")
    print("\nGenerated Itinerary:\n")
    print(itinerary)
