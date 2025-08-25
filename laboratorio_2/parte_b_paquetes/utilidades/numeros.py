"""
Utilidades numéricas con una importación relativa hacia fechas.
Demostramos importación relativa dentro del paquete.
"""
from __future__ import annotations
from typing import Iterable, Optional
from statistics import fmean
from .fechas import es_fecha_iso   # <--- importación relativa desde el mismo paquete

def division_segura(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("No se puede dividir para cero.")
    return a / b

def clamp(x: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(x, maximo))

def promedio(valores: Iterable[float]) -> float:
    return float(fmean(valores))

def etiqueta_si_fecha(cadena: str) -> str:
    """Ejemplo tonto que usa es_fecha_iso importado de .fechas."""
    return "ISO" if es_fecha_iso(cadena) else "NO-ISO"

__all__ = ["division_segura", "clamp", "promedio", "etiqueta_si_fecha"]
