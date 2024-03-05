import crud
import json
import os

from dotenv import load_dotenv
from typing import Annotated
from fastapi import APIRouter, Depends, Form
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestSample, Response, QuestionInput
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")

openai_client = OpenAI(api_key=API_KEY)

router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/create")
async def create(request: RequestSample, db: db_dependency):
    crud.create_sample(db, sample=request.parameter)
    return Response(code=200, status="Ok", message="Sample created successfully!").dict(exclude_none=True)


@router.get("/")
async def get(db: Session = Depends(get_db)):
    _sample = crud.get_sample(db, 0, 100)
    return Response(code=200, status="Ok", message="Successfully fetched all data", result=_sample).dict(exclude_none=True)


@router.post('/generate')
async def generate(question: QuestionInput):
    # Parse JSON string into a Python dictionary
    data = json.loads(question.question)

    # Access the value of the "question" key
    question = data["question"]

    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]

    messages.append({"role": "user", "content": f"{question}"})
    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = completion.choices[0].message.content
    return reply
