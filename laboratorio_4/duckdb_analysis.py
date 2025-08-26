# duckdb_analysis.py (versión corregida)
import os
import duckdb

DATA_PATH = "data/Iris.csv"
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    con = duckdb.connect()

    # B.1 Query directo al CSV
    q1 = f"""
    SELECT Id, SepalLengthCm, SepalWidthCm, Species
    FROM '{DATA_PATH}'
    WHERE SepalLengthCm > 5
    LIMIT 5
    """
    print("Primeras filas con SepalLengthCm > 5:")
    print(con.execute(q1).df(), "\n")

    cnt = con.execute(f"SELECT COUNT(*) FROM '{DATA_PATH}' WHERE SepalLengthCm > 5").fetchone()[0]
    print("Conteo de filas con SepalLengthCm > 5:", cnt, "\n")

    # B.2 Replicamos el análisis de pandas SIN INITCAP
    # Normalizamos Species a "Title case" manual:
    #   UPPER(primera letra) || LOWER(resto)
    # (Nota: si quisieras capitalizar tras guiones, tocaría lógica extra)
    q2 = f"""
    WITH base AS (
      SELECT
        Id,
        SepalLengthCm,
        SepalWidthCm,
        PetalLengthCm,
        PetalWidthCm,
        UPPER(SUBSTR(TRIM(Species), 1, 1)) || LOWER(SUBSTR(TRIM(Species), 2)) AS Species,
        (SepalLengthCm * SepalWidthCm) AS SepalArea
      FROM '{DATA_PATH}'
    ),
    filtered AS (
      SELECT *
      FROM base
      WHERE SepalArea > 20
    )
    SELECT
      Species,
      COUNT(Id) AS count,
      AVG(SepalLengthCm) AS avg_sepal_length,
      AVG(PetalLengthCm) AS avg_petal_length,
      AVG(SepalArea) AS avg_sepal_area
    FROM filtered
    GROUP BY Species
    ORDER BY avg_sepal_area DESC
    """

    duckdf = con.execute(q2).df()
    print("Resumen por especie (DuckDB, SepalArea > 20):")
    print(duckdf, "\n")

    # Exportar a CSV y Parquet
    con.execute(f"COPY ({q2}) TO '{OUT_DIR}/duckdb_summary.csv' (HEADER, DELIMITER ',')")
    con.execute(f"COPY ({q2}) TO '{OUT_DIR}/duckdb_summary.parquet' (FORMAT PARQUET)")

    print("Exportado a outputs/duckdb_summary.csv y .parquet")
    con.close()

if __name__ == "__main__":
    main()
