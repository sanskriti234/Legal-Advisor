from sqlmodel import SQLModel, Field
from typing import Optional

class Analysis(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    filename: str

    risk_score: int = 0

    summary: str