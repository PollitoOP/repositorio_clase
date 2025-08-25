"""
Módulo A — Funciones y Métodos
A.1: funciones como valores y 'ejecutar'
A.2: funciones internas (closures) para descuentos
"""
from typing import Any, Callable, Dict


class AccionNoEncontrada(KeyError):
    """Se lanza cuando la acción solicitada no existe."""


def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"


def despedir(nombre: str) -> str:
    return f"Adiós, {nombre}"


def aplaudir(nombre: str) -> str:
    return f"👏 ¡Bien hecho, {nombre}!"


# Mapa de nombre -> función
acciones: Dict[str, Callable[..., Any]] = {
    "saludar": saludar,
    "despedir": despedir,
    "aplaudir": aplaudir,
}


def ejecutar(accion: str, *args, **kwargs) -> Any:
    """
    Ejecuta la función asociada al nombre 'accion' pasando *args/**kwargs.
    Lanza AccionNoEncontrada si el nombre no está registrado.
    """
    try:
        fn = acciones[accion]
    except KeyError as e:
        raise AccionNoEncontrada(f"La acción '{accion}' no existe.") from e
    return fn(*args, **kwargs)


# ---------- A.2: closures ----------
def crear_descuento(porcentaje: float):
    """
    Crea una función que aplica un descuento fijo al precio recibido.
    porcentaje: 0.10 -> 10%, 0.25 -> 25%, etc.
    """
    if not (0 <= porcentaje <= 1):
        raise ValueError("El porcentaje debe estar entre 0 y 1.")

    def aplicar(precio: float) -> float:
        return round(precio * (1 - porcentaje), 2)

    return aplicar


# Ejemplos rápidos (opcional)
if __name__ == "__main__":
    print(ejecutar("saludar", "Ana"))
    d10 = crear_descuento(0.10)
    d25 = crear_descuento(0.25)
    print(d10(100), d25(80))  # 90.0 60.0
