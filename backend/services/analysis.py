from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def analyze_legal_document(text: str):
    prompt = f"""
    Analyze the following legal document.

    Return ONLY valid JSON in this format:

    {{
        "risk_score": 0,
        "summary": "",
        "risks": [],
        "penalties": [],
        "termination_clauses": []
    }}

    Document:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    try:
        return json.loads(result)
    except Exception:
        return {
            "risk_score": 0,
            "summary": result,
            "risks": [],
            "penalties": [],
            "termination_clauses": []
        }