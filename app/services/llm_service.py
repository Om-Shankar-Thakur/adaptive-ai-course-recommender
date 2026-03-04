import re
import json
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_learning_path(prompt: str):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",   # or your current model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content.strip()

    # 🔥 REMOVE MARKDOWN FENCES
    cleaned_output = re.sub(r"```json|```", "", raw_output).strip()

    try:
        return json.loads(cleaned_output)
    except Exception:
        return {
            "error": "LLM returned invalid JSON",
            "raw_output": raw_output
        }