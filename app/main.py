from fastapi import FastAPI, UploadFile, File
import os
import shutil
from dotenv import load_dotenv

from app.quiz_engine import QuizEngine
from app.schemas import StartQuizResponse, AnswerRequest

load_dotenv()

app = FastAPI(title="Quiz Mistral API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

engine = QuizEngine(api_key=os.getenv("MISTRAL_API_KEY"))

@app.post("/quiz/start", response_model=StartQuizResponse)
async def start_quiz(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return engine.start_quiz(path)

@app.post("/quiz/answer")
async def answer_quiz(data: AnswerRequest):
    return engine.answer_question(data.choice)
