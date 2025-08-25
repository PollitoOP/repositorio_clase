"""
Punto de entrada del paquete. Reexportamos funciones clave para una API cómoda.
"""
from .fechas import es_fecha_iso, formatear_fecha, dias_entre
from .numeros import division_segura, clamp, promedio, etiqueta_si_fecha

__all__ = [
    "es_fecha_iso", "formatear_fecha", "dias_entre",
    "division_segura", "clamp", "promedio", "etiqueta_si_fecha",
]
