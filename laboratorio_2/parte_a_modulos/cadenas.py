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
from unicodedata import normalize as _u_normalize

_email_re = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def normalizar(texto: str) -> str:
    # pasa a NFKD, elimina diacríticos, a minúsculas y colapsa espacios
    txt = _u_normalize("NFKD", texto)
    txt = "".join(ch for ch in txt if not _is_diacritic(ch))
    txt = " ".join(txt.lower().split())
    return txt

def _is_diacritic(ch: str) -> bool:
    return "Mn" in _u_normalize("NFD", ch).encode("unicode_escape").decode()

def slugify(texto: str, sep: str = "-") -> str:
    base = normalizar(texto)
    base = re.sub(r"[^a-z0-9\s-]", "", base)     # solo letras, números, espacios y guiones
    base = re.sub(r"\s+", sep, base).strip(sep)  # espacios -> sep
    base = re.sub(r"-{2,}", sep, base)           # colapsa repeticiones
    return base or "n-a"

def validar_email(email: str) -> str:
    if not _email_re.match(email):
        raise ValueError(f"Email inválido: {email!r}")
    return email

def truncar_palabras(texto: str, n: int) -> str:
    if n <= 0:
        return ""
    partes = texto.split()
    return " ".join(partes[:n])

# API pública sugerida
__all__ = ["normalizar", "slugify", "validar_email", "truncar_palabras"]
