# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app import routers, models
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reitit ja taulut
app.include_router(routers.router)
models.Base.metadata.create_all(bind=engine)

# Palvele ladatut kuvat
app.mount("/uploads", StaticFiles(directory="uploads", check_dir=False), name="uploads")