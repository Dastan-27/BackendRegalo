"""Punto de entrada de la aplicación FastAPI."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import router

# ── Instancia de FastAPI ─────────────────────────────────────────────────────

app = FastAPI(
    title="Cartas Románticas API",
    description=(
        "API para una aplicación web de cartas románticas con audio. "
        "Cada carta incluye un texto tierno y un archivo de audio asociado."
    ),
    version="1.0.0",
)

# ── CORS (React en desarrollo) ──────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Archivos estáticos (audios e imágenes) ───────────────────────────────────

_static_dir = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

# ── Rutas ────────────────────────────────────────────────────────────────────

app.include_router(router)


# ── Ruta raíz informativa ────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "💌 Bienvenido a la API de Cartas Románticas",
        "docs": "/docs",
        "endpoints": [
            "/api/emociones",
            "/api/cartas",
            "/api/cartas/aleatoria",
            "/api/cartas/{carta_id}",
            "/api/extras",
        ],
    }

