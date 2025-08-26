# Notas del laboratorio: Módulos, Paquetes y Type Hints

## Parte A — Módulos
**API pública (`cadenas.py`):**
- `normalizar(texto: str) -> str`: minúsculas, sin tildes, espacios colapsados.
- `slugify(texto: str, sep: str = "-") -> str`: identificador URL-friendly.
- `validar_email(email: str) -> str`: valida patrón simple (lanza `ValueError` si falla).
- `truncar_palabras(texto: str, n: int) -> str`: limita a N palabras.

**Por qué módulo independiente:** agrupa funciones cohesivas de *cadenas*, facilita reutilización y testing, mantiene SRP (Single Responsibility Principle).

**Caso límite probado:** `validar_email("no-es-valido@")` lanza `ValueError`.

## Parte B — Paquetes
Estructura de paquete `utilidades/` con dos módulos:
- `fechas.py`: `es_fecha_iso`, `formatear_fecha`, `dias_entre`
- `numeros.py`: `division_segura`, `clamp`, `promedio`, `etiqueta_si_fecha`

**__init__.py expone:** funciones clave de ambos módulos para un API más cómoda desde el consumidor:
`from utilidades import es_fecha_iso, division_segura, ...`

**Importaciones:**
- **Absolutas** en `main_paquete.py` (`from utilidades import ...`) para consumo externo.
- **Relativas** en `numeros.py` (`from .fechas import es_fecha_iso`) para comunicación interna del paquete.

## Parte C — Type Hints (opcional, resumen ≤8 líneas)
- Documentan intención y permiten análisis estático (mypy/pyright).
- No verifican tipos en runtime por defecto.
- Mejoran autocompletado/IDE, mantenimiento y refactors.
- Usar `list[int]`, `dict[str, float]`, `Optional[str]` (`str | None`), `Union[int, str]` (`int | str`).
