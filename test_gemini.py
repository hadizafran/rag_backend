import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt = "Generate a detailed 1-day itinerary for tourists visiting Tokyo. Include morning, afternoon, evening, food recommendations, and popular activities in readable paragraphs."

try:
    response = genai.TextCompletion.create(model="text-bison-001", prompt=prompt, temperature=0.7, max_output_tokens=500)
    print(response.text)
except Exception as e:
    print("Gemini API error:", e)
