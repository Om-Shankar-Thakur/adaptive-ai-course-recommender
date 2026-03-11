import os
import json
from dotenv import load_dotenv
from google import genai
load_dotenv()
# Read API key
api_key = os.getenv("GEMINI_API_KEY")
# Initialize Gemini client
client = genai.Client(api_key=api_key)

def generate_learning_path(prompt: str):
   try:
       response = client.models.generate_content(
           model="gemini-2.5-flash",
           contents=prompt,
           config={
               "response_mime_type": "application/json"
           }
       )
       result = json.loads(response.text)
       return result
   except Exception as e:
       print("Gemini Error:", e)
       return {
           "learning_path": [],
           "status": "error",
           "message": "AI service temporarily unavailable"
       }
