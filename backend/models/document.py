from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    filename: str

    risk_score: int = 0

    summary: str = ""

    uploaded_at: datetime = Field(
        default_factory=datetime.utcnow
    )