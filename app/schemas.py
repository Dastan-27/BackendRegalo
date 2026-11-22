"""Modelos Pydantic v2 para validar las respuestas de la API."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Emociones ────────────────────────────────────────────────────────────────

class EmocionResumen(BaseModel):
    """Resumen de una categoría de emoción."""

    id: str = Field(..., examples=["insegura"])
    nombre: str = Field(..., examples=["Me siento insegura / Tengo dudas"])
    cantidad_cartas: int = Field(..., ge=0, examples=[2])


class EmocionesResponse(BaseModel):
    """Lista de emociones disponibles."""

    emociones: list[EmocionResumen]


# ── Cartas ───────────────────────────────────────────────────────────────────

class Carta(BaseModel):
    """Carta romántica con texto y URL de audio generada automáticamente."""

    id: str = Field(..., examples=["insegura_01"])
    emocion_id: str = Field(..., examples=["insegura"])
    titulo: str = Field(..., examples=["Nunca dudes de lo que siento"])
    texto: str
    audio_file: str = Field(..., examples=["insegura_01.mp3"])
    audio_url: str = Field(..., examples=["/static/audios/insegura_01.mp3"])


class CartasResponse(BaseModel):
    """Respuesta con una o varias cartas."""

    cartas: list[Carta]


# ── Extras ───────────────────────────────────────────────────────────────────

class ExtrasResponse(BaseModel):
    """Configuración extra: audio del botón AMOR!!! y link de broma."""

    audio_amor: str = Field(default="amor_01.m4a", examples=["amor_01.m4a"])
    audio_amor_url: str = Field(
        default="/static/audios/amor_01.m4a", examples=["/static/audios/amor_01.m4a"]
    )
    audios_amor: list[str] = Field(
        default_factory=list,
        examples=[["amor_01.m4a", "amor_02.m4a", "amor_03.m4a", "amor_04.m4a", "amor_05.m4a"]],
    )
    audios_amor_urls: list[str] = Field(
        default_factory=list,
        examples=[["/static/audios/amor_01.m4a", "/static/audios/amor_02.m4a"]],
    )
    link_broma_final: str = Field(
        ..., examples=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    )

