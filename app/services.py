"""Lógica de negocio: lectura del JSON, filtrado y selección aleatoria."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from fastapi import HTTPException, status

# ── Ruta al archivo de datos ─────────────────────────────────────────────────

_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cartas.json"
_AUDIO_BASE = "/static/audios"

# ── Cache en memoria (se carga una sola vez) ─────────────────────────────────

_data: dict[str, Any] | None = None


def _load_data() -> dict[str, Any]:
    """Carga y cachea el contenido de *cartas.json* (UTF-8)."""
    global _data
    if _data is None:
        with open(_DATA_PATH, encoding="utf-8") as f:
            _data = json.load(f)
    return _data


def _build_audio_url(filename: str) -> str:
    """Construye la URL pública del audio a partir del nombre de archivo."""
    return f"{_AUDIO_BASE}/{filename}"


# ── Funciones públicas ───────────────────────────────────────────────────────


def listar_emociones() -> list[dict[str, Any]]:
    """Devuelve las categorías con la cantidad de cartas de cada una."""
    data = _load_data()
    resultado: list[dict[str, Any]] = []
    for emocion in data["emociones"]:
        resultado.append(
            {
                "id": emocion["id"],
                "nombre": emocion["nombre"],
                "cantidad_cartas": len(emocion["cartas"]),
            }
        )
    return resultado


def listar_cartas(emocion_id: str | None = None) -> list[dict[str, Any]]:
    """Devuelve todas las cartas (o solo las de una emoción concreta)."""
    data = _load_data()
    cartas: list[dict[str, Any]] = []

    for emocion in data["emociones"]:
        if emocion_id and emocion["id"] != emocion_id:
            continue
        for carta in emocion["cartas"]:
            cartas.append(
                {
                    **carta,
                    "emocion_id": emocion["id"],
                    "audio_url": _build_audio_url(carta["audio_file"]),
                }
            )

    return cartas


def obtener_carta_por_id(carta_id: str) -> dict[str, Any]:
    """Busca una carta por su *id* único; lanza 404 si no existe."""
    data = _load_data()
    for emocion in data["emociones"]:
        for carta in emocion["cartas"]:
            if carta["id"] == carta_id:
                return {
                    **carta,
                    "emocion_id": emocion["id"],
                    "audio_url": _build_audio_url(carta["audio_file"]),
                }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Carta con id '{carta_id}' no encontrada.",
    )


def carta_aleatoria(emocion_id: str | None = None) -> dict[str, Any]:
    """Elige una carta al azar (global o dentro de una emoción)."""
    cartas = listar_cartas(emocion_id)
    if not cartas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron cartas"
            + (f" para la emoción '{emocion_id}'." if emocion_id else "."),
        )
    return random.choice(cartas)


def obtener_extras() -> dict[str, Any]:
    """Devuelve la config extra: audio del botón AMOR!!! y link de broma."""
    data = _load_data()
    extras = data["extras"]
    return {
        "audio_amor": extras["audio_amor"],
        "audio_amor_url": _build_audio_url(extras["audio_amor"]),
        "link_broma_final": extras["link_broma_final"],
    }

