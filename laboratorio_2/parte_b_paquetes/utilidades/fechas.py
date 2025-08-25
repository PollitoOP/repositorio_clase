"""
Utilidades de fechas: formato e intervalos simples.
"""
from __future__ import annotations
from datetime import date, datetime
from typing import Optional

def es_fecha_iso(cadena: str) -> bool:
    try:
        datetime.fromisoformat(cadena)
        return True
    except ValueError:
        return False

def formatear_fecha(fecha: date, formato: str = "%Y-%m-%d") -> str:
    return fecha.strftime(formato)

def dias_entre(a: str, b: str) -> int:
    """
    Recibe dos strings en ISO (YYYY-mm-dd) y devuelve la diferencia en días.
    """
    da = datetime.fromisoformat(a).date()
    db = datetime.fromisoformat(b).date()
    return abs((db - da).days)

__all__ = ["es_fecha_iso", "formatear_fecha", "dias_entre"]
