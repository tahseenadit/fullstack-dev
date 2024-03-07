import crud
import json
import os
import vertexai
import vertexai.preview.generative_models as generative_models

from vertexai.preview.generative_models import GenerativeModel, Part
from dotenv import load_dotenv
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestSample, Response
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


@router.post('/openai/generate')
async def openai_generate(request: Request):
    content_type = request.headers.get("Content-Type")

    # Check if request contains JSON data
    if content_type != "application/json":
        raise HTTPException(status_code=400, detail="Request content type is not JSON")

    # Read request body
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data in request")

    # Check if JSON data is empty
    if not data:
        raise HTTPException(status_code=400, detail="Empty JSON data")

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


@router.post('/vertexai/generate')
async def vertexai_generate(request: Request):
    content_type = request.headers.get("Content-Type")

    # Check if request contains JSON data
    if content_type != "application/json":
        raise HTTPException(status_code=400, detail="Request content type is not JSON")

    # Read request body
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON data in request")

    # Check if JSON data is empty
    if not data:
        raise HTTPException(status_code=400, detail="Empty JSON data")

    # Access the value of the "question" key
    question = data["question"]

    vertexai.init(project="data-enablement-dp-poc", location="europe-west1")
    model = GenerativeModel("gemini-1.0-pro-001")
    responses = model.generate_content(
        f"""{question}""",
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.9,
            "top_p": 1
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=True,
    )
    
    reply = ""
    for response in responses:
        reply += "\n" + response.text

    return str(reply)


