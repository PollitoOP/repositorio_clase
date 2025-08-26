# pandas_analysis.py
import os
import pandas as pd

DATA_PATH = "data/Iris.csv"
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    # A.1 Lectura y exploración
    df = pd.read_csv(DATA_PATH)

    print("Primeras filas:")
    print(df.head(), "\n")

    print("Info del DataFrame:")
    df.info()
    print()

    print("Nulos por columna:")
    print(df.isna().sum(), "\n")

    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas\n")

    # A.2 Columnas derivadas y limpieza
    # - Columna derivada: Área aproximada del sépalo (SepalLength * SepalWidth)
    df["SepalArea"] = df["SepalLengthCm"] * df["SepalWidthCm"]

    # - Normalizar Species (ej: capitalizar)
    df["Species"] = df["Species"].str.strip().str.title()

    # - Manejo de nulos (si hubiera, rellenar con media en SepalArea)
    if df["SepalArea"].isna().any():
        df["SepalArea"] = df["SepalArea"].fillna(df["SepalArea"].mean())

    # A.3 Agrupaciones y filtros
    # Filtro: considerar solo flores con SepalArea > 20
    filtered = df.query("SepalArea > 20")

    # Agrupar por especie y calcular métricas
    grouped = (
        filtered.groupby("Species")
        .agg(
            count=("Id", "count"),
            avg_sepal_length=("SepalLengthCm", "mean"),
            avg_petal_length=("PetalLengthCm", "mean"),
            avg_sepal_area=("SepalArea", "mean"),
        )
        .reset_index()
    )

    print("Resumen por especie (SepalArea > 20):")
    print(grouped, "\n")

    # Exportar
    grouped.to_csv(os.path.join(OUT_DIR, "pandas_summary.csv"), index=False)
    grouped.to_parquet(os.path.join(OUT_DIR, "pandas_summary.parquet"), index=False)

    print("Exportado a outputs/pandas_summary.csv y .parquet")

if __name__ == "__main__":
    main()
