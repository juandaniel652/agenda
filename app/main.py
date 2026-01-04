from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.cliente import router as cliente_router
from app.api.v1.health import router as health_router

app = FastAPI(
    title="Backend Unificado",
    description="Auth + App backend",
    version="1.0.0",
)

# =========================
# CORS CONFIGURACIÓN
# =========================
# Se conserva la config del login (producción)
origins = [
    "https://loginagenda.netlify.app",
    "https://s-link-version1-0.netlify.app",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers API v1
# =========================
app.include_router(auth_router, prefix="/api/v1")
app.include_router(cliente_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")

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
