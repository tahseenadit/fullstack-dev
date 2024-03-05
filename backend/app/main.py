import tables
import router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine


tables.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get('/')
async def home():
    return 'Welcome home!'

app.include_router(router=router.router, prefix="/sample", tags=["sample"])