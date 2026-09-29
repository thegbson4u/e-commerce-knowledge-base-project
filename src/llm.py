import os
import json
from google import genai
from google.genai import types
from src.prompts import INTENT_EXTRACTION_PROMPT, QA_GROUNDING_PROMPT

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please create a .env file.")
    return genai.Client(api_key=api_key)

def extract_structured_intent(question: str) -> dict:
    """Uses LLM structured output to convert natural language into a deterministic query map."""
    client = get_gemini_client()
    prompt = INTENT_EXTRACTION_PROMPT.format(question=question)
    
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0
        )
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback cleaner in case the LLM ignored mime_type constraints
        cleaned = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)

def generate_grounded_answer(question: str, retrieved_data: str) -> str:
    """Generates the final natural language answer using ONLY the extracted graph data."""
    client = get_gemini_client()
    prompt = QA_GROUNDING_PROMPT.format(
        question=question, 
        retrieved_data=retrieved_data
    )
    
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.1)
    )
    
    return response.text