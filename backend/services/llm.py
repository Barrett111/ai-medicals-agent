from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_response(prompt: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ stable + fast
            messages=[
                {
                    "role": "system",
                    "content": """You are a medical AI assistant.
Give detailed, structured answers with headings, bullet points, and clear explanations.
Avoid short answers."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=1200   # 🔥 IMPORTANT (fix short answers)
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Empty response from LLM")

        return content

    except Exception as e:
        logging.error(f"❌ LLM ERROR: {str(e)}")
        return None