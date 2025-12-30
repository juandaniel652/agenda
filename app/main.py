from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.cliente import router as clientes_router
from app.routes.health import router as health_router
from app.models import cliente  # noqa
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agenda Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://s-link-version1-0.netlify.app",
        "http://localhost:3000",
        "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router)
app.include_router(health_router)

@app.get("/")
def read_root():
    return {"message": "Backend funcionando con CORS habilitado"}
