from pydantic import BaseModel
from typing import List, Optional

class StartQuizResponse(BaseModel):
    index: int
    question: str
    options: List[str]

class AnswerRequest(BaseModel):
    choice: int

class QuizFinishedResponse(BaseModel):
    score: int
    total: int
    details: list
