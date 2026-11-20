"""Endpoints de la API bajo el prefijo /api."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app import services
from app.schemas import Carta, CartasResponse, EmocionesResponse, ExtrasResponse

router = APIRouter(prefix="/api", tags=["Cartas Románticas"])


# ── GET /api/emociones ───────────────────────────────────────────────────────

@router.get("/emociones", response_model=EmocionesResponse, summary="Listar emociones")
def get_emociones():
    """Devuelve la lista de categorías de emociones y la cantidad de cartas
    disponibles en cada una."""
    return EmocionesResponse(emociones=services.listar_emociones())


# ── GET /api/cartas ──────────────────────────────────────────────────────────

@router.get("/cartas", response_model=CartasResponse, summary="Listar cartas")
def get_cartas(
    emocion_id: str | None = Query(
        default=None,
        description="Filtrar cartas por el id de una emoción específica.",
        examples=["insegura"],
    ),
):
    """Devuelve todas las cartas. Acepta `?emocion_id=...` para filtrar por
    categoría."""
    return CartasResponse(cartas=services.listar_cartas(emocion_id))


# ── GET /api/cartas/aleatoria ────────────────────────────────────────────────

@router.get(
    "/cartas/aleatoria",
    response_model=Carta,
    summary="Carta aleatoria",
)
def get_carta_aleatoria(
    emocion_id: str | None = Query(
        default=None,
        description="Elegir al azar dentro de una emoción específica.",
        examples=["extrano"],
    ),
):
    """Devuelve una carta elegida al azar (global o por emoción)."""
    return services.carta_aleatoria(emocion_id)


# ── GET /api/cartas/{carta_id} ───────────────────────────────────────────────

@router.get(
    "/cartas/{carta_id}",
    response_model=Carta,
    summary="Obtener carta por ID",
)
def get_carta_por_id(carta_id: str):
    """Devuelve una carta específica por su ID. Lanza HTTP 404 si no existe."""
    return services.obtener_carta_por_id(carta_id)


# ── GET /api/extras ──────────────────────────────────────────────────────────

@router.get("/extras", response_model=ExtrasResponse, summary="Extras")
def get_extras():
    """Devuelve la URL del audio para el botón flotante \"AMOR!!!\" y el
    enlace de la broma final."""
    return services.obtener_extras()

