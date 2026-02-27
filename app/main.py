from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.v1.auth import router as auth_router
from app.api.v1.cliente import router as cliente_router
from app.api.v1.health import router as health_router
from app.api.v1.tecnico import router as tecnico_router
from app.api.v1.turno import router as turno_router


app = FastAPI(
    title="Backend Unificado",
    description="Auth + App backend",
    version="1.0.0",
)

# CREAR carpeta uploads automáticamente
os.makedirs("uploads", exist_ok=True)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers
# =========================
app.include_router(auth_router, prefix="/api/v1")
app.include_router(cliente_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(tecnico_router, prefix="/api/v1")
app.include_router(turno_router, prefix="/api/v1")


# SERVIR archivos
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# =========================
# Root
# =========================
@app.get("/")
def root():
    return {
        "service": "backend-unificado",
        "status": "running",
        "version": app.version,
    }
