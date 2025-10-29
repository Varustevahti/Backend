# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app import routers, models

app = FastAPI()

# --- CORS: salli mobiililaitteet ja LAN ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # yksinkertaisin ja varmin devissä
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reitit ja taulut
app.include_router(routers.router)
models.Base.metadata.create_all(bind=engine)

# Palvele ladatut kuvat
app.mount("/uploads", StaticFiles(directory="uploads", check_dir=False), name="uploads")

# Terveystsekki
@app.get("/health")
def health():
    return {"ok": True}