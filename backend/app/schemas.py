from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')


class QuestionInput(BaseModel):
    question: str


class SampleSchema(BaseModel):
    """Sample table schema
    """

    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class RequestSample(BaseModel):
    parameter: SampleSchema = Field(...)


class Response(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T]
