import crud

from typing import Annotated
from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestSample, Response

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