import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"  # Updated model
HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def flatten_kundli_summary(summary: dict) -> str:
    return "\n".join([f"{key}: {value}" for key, value in summary.items()])

def interpret_horoscope(kundli_summary: dict, user_question: str) -> str:
    kundli_text = flatten_kundli_summary(kundli_summary)

    prompt = f"""You are a knowledgeable Vedic astrologer. Based on the Kundli summary, answer the user's question in simple, respectful language.

Kundli Summary:
{kundli_text}

User Question:
{user_question}

Astrologer Answer:"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200
        }
    }

    try:
        response = requests.post(HF_URL, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()
        return output[0]["generated_text"].strip()
    except Exception as e:
        print("Hugging Face API Exception:", e)
        return "Sorry, I couldn't interpret your horoscope at the moment."
