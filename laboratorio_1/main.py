"""
Pequeña demo para verificar los criterios del laboratorio.
Ejecuta:  python main.py
"""
from modulo_a import ejecutar, crear_descuento
from modulo_b import parsear_enteros, calcular_total, CantidadInvalida
from modulo_c import calcular_descuento, escala

def demo_modulo_a():
    print("== Módulo A ==")
    print(ejecutar("saludar", "Ana"))  # "Hola, Ana"
    try:
        ejecutar("no_existe", "X")
    except Exception as e:
        print("Acción inexistente OK ->", e)

    d10 = crear_descuento(0.10)
    d25 = crear_descuento(0.25)
    print("descuento10(100) =", d10(100))  # 90.0
    print("descuento25(80)  =", d25(80))   # 60.0


def demo_modulo_b():
    print("\n== Módulo B ==")
    valores, errores = parsear_enteros(["10", "x", "3"])
    print("valores:", valores)   # [10, 3]
    print("errores:", errores)   # contiene el error de "x"

    print("calcular_total(10, 3) =", calcular_total(10, 3))  # 30.0
    try:
        calcular_total(10, 0)
    except CantidadInvalida as e:
        print("CantidadInvalida OK ->", e)


def demo_modulo_c():
    print("\n== Módulo C ==")
    print("calcular_descuento(100, 0.2) =", calcular_descuento(100, 0.2))  # 80.0
    try:
        calcular_descuento(-1, 0.2)
    except ValueError as e:
        print("Validación positivos OK ->", e)

    print("escala(5, 3) =", escala(5, 3))  # 15.0


if __name__ == "__main__":
    demo_modulo_a()
    demo_modulo_b()
    demo_modulo_c()
