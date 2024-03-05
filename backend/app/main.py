import tables
import router

from fastapi import FastAPI
from config import engine

tables.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
async def home():
    return 'Welcome home!'

app.include_router(router=router.router, prefix="/sample", tags=["sample"])