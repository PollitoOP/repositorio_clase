# Laboratorio: Pytest + Módulo simple y CSV (Python 3.12)

Este repo trae dos partes:

- **Parte A:** módulo `src/utils.py` con 3 funciones simples y sus pruebas en `tests/test_utils.py`.
- **Parte B:** validación de un dataset CSV usando la librería estándar `csv` con pruebas en `tests/test_csv_validation.py`.
  El dataset utilizado es `data/Crop.csv` (incluido).

## Requisitos
- Python 3.12
- `pytest`

Instalación (en Codespaces o local con venv):
```bash
pip install -r requirements.txt
```

## Estructura
```
src/
  __init__.py
  utils.py
tests/
  test_utils.py
  test_csv_validation.py
data/
  Crop.csv
```

## Cómo ejecutar las pruebas
Desde la raíz del repo:

```bash
pytest -q

## Para ver mas detalles ejecutar
pytest -v

```

## Funciones del módulo

- `normalize_text(s: str) -> str`  
  Normaliza texto a minúsculas, recorta espacios y colapsa espacios internos.

- `is_palindrome(s: str) -> bool`  
  Verifica si una cadena es palíndroma ignorando espacios y signos de puntuación.

- `moving_average(values: Iterable[float], window: int) -> List[float]`  
  Calcula el promedio móvil simple para una ventana dada.

## Validación del CSV
Archivo: `data/Crop.csv` (codificación `utf-8-sig` por posible BOM).  
Reglas validadas por `tests/test_csv_validation.py`:
- Columnas obligatorias presentes: `N,P,K,ph,EC,S,Cu,Fe,Mn,Zn,B,label`.
- Tipos numéricos para N,P,K,S,Cu,Fe,Mn,Zn,B,EC,ph; valores **no negativos**.
- `ph` en rango `[0,14]`.
- `label` no vacío y razonable (sin dígitos).
```

