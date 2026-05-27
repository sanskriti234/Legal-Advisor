from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_legal_document(text: str):

    prompt = f"""
    Analyze this legal document.

    Identify:
    - risky clauses
    - penalties
    - suspicious obligations
    - termination conditions
    - financial risks

    Return concise structured analysis.

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
        temperature=0.2,
    )

    return response.choices[0].message.content