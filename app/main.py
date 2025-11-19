# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, SessionLocal
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

# Luodaan taulut
models.Base.metadata.create_all(bind=engine)


# SEED: Koti & Varasto
def seed_default_locations():
    db = SessionLocal()
    try:
        count = db.query(models.Location).count()
        if count == 0:
            db.add_all(
                [
                    models.Location(name="Koti", description="Koti", owner=None),
                    models.Location(name="Varasto", description="Varasto", owner=None),
                ]
            )
            db.commit()
    finally:
        db.close()


seed_default_locations()

# Reitit
app.include_router(routers.router)

# Palvele ladatut kuvat
app.mount("/uploads", StaticFiles(directory="uploads", check_dir=False), name="uploads")