# src/operaciones.py
from __future__ import annotations


def suma(a: float, b: float) -> float:
    """Suma dos números y devuelve un float."""
    return float(a + b)


def division(a: float, b: float) -> float:
    """Divide a entre b. Lanza ZeroDivisionError si b == 0."""
    if b == 0:
        raise ZeroDivisionError("La división por cero no está permitida.")
    return a / b
