import csv
import os
import pytest

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Crop.csv")

REQUIRED_COLS = ["N","P","K","ph","EC","S","Cu","Fe","Mn","Zn","B","label"]

def _read_rows(path):
    # Use utf-8-sig to handle BOM in some CSVs
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        yield from reader

def test_csv_exists():
    assert os.path.exists(DATA_PATH), "El dataset Crop.csv debe existir en data/"

def test_required_columns_present():
    with open(DATA_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames is not None
        cols = [c.strip() for c in reader.fieldnames]
        for required in REQUIRED_COLS:
            assert required in cols, f"Falta columna requerida: {required}"

def test_types_and_ranges():
    # Reglas mínimas:
    # - N,P,K,S,Cu,Fe,Mn,Zn,B,EC,ph deben ser numéricos (float convertibles)
    # - No negativos
    # - ph dentro de 0..14
    # - label no vacío
    for i, row in enumerate(_read_rows(DATA_PATH), start=1):
        # label
        label = row.get("label","").strip()
        assert label != "", f"Fila {i}: label vacío"

        # num fields
        for key in ["N","P","K","S","Cu","Fe","Mn","Zn","B"]:
            val = float(row[key])  # debe lanzar si no es numérico
            assert val >= 0, f"Fila {i}: {key} negativo"

        ph = float(row["ph"])
        assert 0.0 <= ph <= 14.0, f"Fila {i}: ph fuera de rango [0,14]"

        ec = float(row["EC"])
        assert ec >= 0.0, f"Fila {i}: EC negativo"

def test_labels_reasonable():
    # Las etiquetas deben ser palabras o combinaciones cortas (sin dígitos)
    for i, row in enumerate(_read_rows(DATA_PATH), start=1):
        label = row["label"].strip()
        assert label.isalpha() or " " in label, f"Fila {i}: label sospechoso '{label}'"

