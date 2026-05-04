import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

def get_gemini_response(prompt):
    # Load env with override to catch newly saved API keys without restarting server
    load_dotenv(override=True)
    try:
        gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"

def get_openai_response(prompt):
    # Load env with override to catch newly saved API keys without restarting server
    load_dotenv(override=True)
    try:
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to OpenAI: {str(e)}"

def get_llm_response(prompt, model_choice):
    if model_choice == "OpenAI":
        return get_openai_response(prompt)
    else:
        return get_gemini_response(prompt)