import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key[:10]}...")

genai.configure(api_key=api_key)

print("\n--- Listing Models ---")
try:
    models = list(genai.list_models())
    for m in models:
        print(f"Model: {m.name}, Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")

print("\n--- Testing Generation with 'gemini-1.5-flash' ---")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content('hi')
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error with gemini-1.5-flash: {e}")

print("\n--- Testing Generation with 'gemini-pro' ---")
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('hi')
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error with gemini-pro: {e}")
