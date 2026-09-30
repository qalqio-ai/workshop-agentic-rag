from pydantic import BaseModel, Field, field_validator


class DocumentIn(BaseModel):
    use_case_id: str
    source_id: str = Field(min_length=1, max_length=128)
    title: str = Field(min_length=1, max_length=256)
    text: str = Field(min_length=1, max_length=50_000)

    @field_validator("source_id", "title", "text")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must contain non-whitespace characters")
        return value.strip()


class QueryIn(BaseModel):
    use_case_id: str
    question: str = Field(min_length=1, max_length=4_000)
    session_id: str | None = Field(default=None, max_length=128)

    @field_validator("question")
    @classmethod
    def reject_blank_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question must contain non-whitespace characters")
        return value.strip()


class Citation(BaseModel):
    source_id: str
    title: str
    chunk_id: str


class QueryOut(BaseModel):
    answer: str
    evidence_status: str
    citations: list[Citation]
    session_id: str
    trace_id: str
