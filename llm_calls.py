import os
from dotenv import load_dotenv
from google import genai

# Load env
load_dotenv()

# Setup client (Only Gemini)
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(prompt):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"