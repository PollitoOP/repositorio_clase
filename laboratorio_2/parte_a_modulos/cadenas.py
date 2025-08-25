"""
Módulo de utilidades de cadenas
- normalizar: minúsculas, quita tildes y espacios extra
- slugify: genera identificadores amigables (urls)
- validar_email: valida un email simple; lanza ValueError si no cumple
- truncar_palabras: limita a N palabras
"""
from __future__ import annotations
import re
from typing import Iterable
from unicodedata import normalize as _u_normalize, category as _u_category

_email_re = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def normalizar(texto: str) -> str:
    """
    Convierte a minúsculas, elimina tildes/diacríticos y colapsa espacios.
    """
    # 1) Descompone a NFKD
    txt = _u_normalize("NFKD", texto)
    # 2) Elimina los caracteres con categoría 'Mn' (diacríticos)
    txt = "".join(ch for ch in txt if _u_category(ch) != "Mn")
    # 3) Pasa a minúsculas y colapsa espacios extra
    txt = " ".join(txt.lower().split())
    return txt


def slugify(texto: str, sep: str = "-") -> str:
    """
    Convierte un texto en un slug amigable para URLs.
    """
    base = normalizar(texto)
    base = re.sub(r"[^a-z0-9\s-]", "", base)      # solo letras/números/espacios/-
    base = re.sub(r"\s+", sep, base).strip(sep)   # espacios -> sep
    base = re.sub(rf"{re.escape(sep)}{{2,}}", sep, base)  # colapsa repetidos
    return base or "n-a"


def validar_email(email: str) -> str:
    """
    Valida un email con regex básica. Lanza ValueError si no cumple.
    """
    if not _email_re.match(email):
        raise ValueError(f"Email inválido: {email!r}")
    return email


def truncar_palabras(texto: str, n: int) -> str:
    """
    Devuelve las primeras n palabras del texto.
    """
    if n <= 0:
        return ""
    partes = texto.split()
    return " ".join(partes[:n])


# API pública sugerida
__all__ = ["normalizar", "slugify", "validar_email", "truncar_palabras"]
