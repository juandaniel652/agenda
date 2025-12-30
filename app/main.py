from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://s-link-version1-0.netlify.app",
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend funcionando con CORS habilitado"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        conn.execute(text("select 1"))
        return {"db": "ok"}
