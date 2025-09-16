from fastapi import FastAPI, Depends
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app import routers, models

app = FastAPI()
app.include_router(routers.router)
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)
models.Base.metadata.create_all(bind=engine)
