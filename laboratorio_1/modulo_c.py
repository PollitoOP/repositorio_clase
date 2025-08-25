"""
Módulo C — Decoradores
C.1: Decorador de validación de argumentos positivos
"""
from functools import wraps
from numbers import Number
from typing import Any, Callable


def requiere_positivos(func: Callable) -> Callable:
    """
    Verifica que todos los argumentos numéricos (args/kwargs) sean > 0.
    Ignora argumentos no numéricos.
    Lanza ValueError con un mensaje claro si encuentra un no-positivo.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Revisa args
        for i, a in enumerate(args):
            if isinstance(a, Number) and a <= 0:
                raise ValueError(
                    f"Argumento posicional #{i} debe ser > 0. Recibido: {a}"
                )
        # Revisa kwargs
        for k, v in kwargs.items():
            if isinstance(v, Number) and v <= 0:
                raise ValueError(
                    f"Argumento '{k}' debe ser > 0. Recibido: {v}"
                )
        return func(*args, **kwargs)

    return wrapper


@requiere_positivos
def calcular_descuento(precio: float, porcentaje: float) -> float:
    """
    Aplica descuento: porcentaje expresado como 0.2 -> 20% (debe ser > 0).
    Nota: el decorador ya valida que precio y porcentaje sean > 0.
    """
    if porcentaje >= 1:
        # opcional: evita % > 100
        raise ValueError("El porcentaje debe ser menor que 1 (p.ej., 0.2 para 20%).")
    return round(precio * (1 - porcentaje), 2)


@requiere_positivos
def escala(valor: float, factor: float) -> float:
    """Multiplica valor por factor (ambos > 0 por contrato del decorador)."""
    return valor * factor


# Ejemplos rápidos 
if __name__ == "__main__":
    print(calcular_descuento(100, 0.2))  # 80.0
    # calcular_descuento(-1, 0.2) -> ValueError
