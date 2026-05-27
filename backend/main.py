from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from services.analysis import analyze_legal_document

app=FastAPI(title="Legal Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def check_health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Legal Advisor API!"}

@app.post("/analyze")
async def analyze():

    sample_text = """
    User shall pay penalty of $5000 if contract is terminated early.
    """

    result = analyze_legal_document(sample_text)

    return {
        "analysis": result
    }