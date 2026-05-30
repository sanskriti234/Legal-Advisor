from fastapi.middleware.cors import CORSMiddleware
from services.analysis import analyze_legal_document
from services.pdf_parser import extract_pdf_text
from fastapi import FastAPI, UploadFile, File
from models.document import Document
from models.user import User
from services.security import (hash_password, verify_password, create_access_token)
import shutil
import os
from sqlmodel import Session, SQLModel, select
from models.analysis import Analysis
from database import engine

app=FastAPI(title="Legal Advisor")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SQLModel.metadata.create_all(engine)

@app.get("/health")
def check_health():
    return {"status": "ok"}


@app.get("/root")
def read_root():
    return {"message": "Welcome to the Legal Advisor API!"}


@app.post("/analyze")
def analyze():

    sample_text = """
    The employee shall pay a penalty of $5000
    if the agreement is terminated before 12 months.
    """

    result = analyze_legal_document(sample_text)

    return result


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    text = extract_pdf_text(
        file_path
    )

    analysis = analyze_legal_document(
        text
    )

    with Session(engine) as session:

        record = Analysis(
            filename=file.filename,
            risk_score=analysis.get("risk_score", 0),
            summary=analysis.get("summary", "")
        )

        session.add(record)
        session.commit()


    return {
        "filename": file.filename,
        "analysis": analysis
    }


from sqlmodel import select

@app.get("/history")
def history():

    with Session(engine) as session:

        records = session.exec(
            select(Analysis)
        ).all()

        return records
    
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/register")
def register(
    data: RegisterRequest
):

    with Session(engine) as session:

        existing_user = session.exec(
            select(User).where(
                User.email == data.email
            )
        ).first()

        if existing_user:
            return {
                "error": "Email already registered"
            }

        user = User(
            email=data.email,
            password=hash_password(
                data.password
            )
        )

        session.add(user)
        session.commit()

        return {
            "message": "User registered successfully"
        }
    
@app.post("/login")
def login(
    data: LoginRequest
):

    with Session(engine) as session:

        user = session.exec(
            select(User).where(
                User.email == data.email
            )
        ).first()

        if not user:
            return {
                "error": "User not found"
            }

        if not verify_password(
            data.password,
            user.password
        ):
            return {
                "error": "Invalid password"
            }

        token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }