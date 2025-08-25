# Importaciones absolutas desde el script principal:
from utilidades import (
    es_fecha_iso, formatear_fecha, dias_entre,
    division_segura, clamp, promedio, etiqueta_si_fecha,
)

def demo():
    print("== PAQUETE B ==")
    print("es_fecha_iso('2025-08-25') ->", es_fecha_iso("2025-08-25"))
    print("dias_entre('2025-01-01','2025-01-31') ->", dias_entre("2025-01-01", "2025-01-31"))
    print("division_segura(10,2) ->", division_segura(10, 2))
    print("clamp(15,0,10) ->", clamp(15, 0, 10))
    print("promedio([1,2,3,4]) ->", promedio([1, 2, 3, 4]))
    print("etiqueta_si_fecha('2025-08-25') ->", etiqueta_si_fecha("2025-08-25"))  # usa import relativo interno

    # Caso límite: división por cero
    try:
        division_segura(1, 0)
    except ZeroDivisionError as e:
        print("Division por cero OK ->", e)

if __name__ == "__main__":
    demo()
