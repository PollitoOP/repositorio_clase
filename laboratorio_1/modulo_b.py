"""
Módulo B — Excepciones
B.1: parsear enteros con captura y continuidad
B.2: excepción personalizada y validaciones con raise
"""
from typing import List, Tuple


def parsear_enteros(entradas: List[str]) -> Tuple[List[int], List[str]]:
    """
    Convierte strings a enteros. Si hay errores, los registra y continúa.
    Devuelve (valores_ok, errores).
    """
    valores: List[int] = []
    errores: List[str] = []

    for idx, s in enumerate(entradas):
        try:
            valores.append(int(s))
        except ValueError:
            errores.append(f"Posición {idx}: '{s}' no es un entero válido")
            # continúa el proceso

    return valores, errores


# ---------- B.2 ----------
class CantidadInvalida(Exception):
    """Se lanza cuando la cantidad es <= 0 en una operación."""


def calcular_total(precio_unitario: float, cantidad: int) -> float:
    """
    Calcula total validando:
    - Cantidad > 0 -> si no, CantidadInvalida
    - precio_unitario >= 0 -> si no, ValueError
    """
    if cantidad <= 0:
        raise CantidadInvalida("La cantidad debe ser mayor que 0.")
    if precio_unitario < 0:
        raise ValueError("El precio unitario no puede ser negativo.")
    return round(precio_unitario * cantidad, 2)


# Ejemplos rápidos 
if __name__ == "__main__":
    print(parsear_enteros(["10", "x", "3"]))  # ([10, 3], ["... x ..."])
    print(calcular_total(10, 3))              # 30.0
