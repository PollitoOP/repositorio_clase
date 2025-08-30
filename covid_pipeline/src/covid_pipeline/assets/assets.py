import os
from datetime import datetime, timezone

import dagster as dg
import pandas as pd

OWID_URL_DEFAULT = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"


@dg.asset(automation_condition=dg.AutomationCondition.on_cron("0 6 * * *"))
def leer_datos(context: dg.AssetExecutionContext) -> pd.DataFrame:
    """Lee el CSV de OWID (o fallback local) y normaliza nombres de columnas."""
    url = os.getenv("COVID_SOURCE_URL", OWID_URL_DEFAULT)
    fallback = os.getenv("COVID_LOCAL_FALLBACK", "data/compact.csv")
    try:
        context.log.info(f"Descargando {url}")
        df = pd.read_csv(url)  # opcional: parse_dates=["date"], usecols=...
        fuente = "remoto"
    except Exception as e:
        context.log.warning(f"Fallo remoto: {e}. Usando {fallback}")
        df = pd.read_csv(fallback)
        fuente = "local"

    # normaliza nombres
    df.columns = [c.strip().lower() for c in df.columns]
    # por si el dataset trae "country" en vez de "location"
    if "country" in df.columns and "location" not in df.columns:
        df = df.rename(columns={"country": "location"})

    context.add_output_metadata({
        "fuente": fuente,
        "filas": len(df),
        "columnas": list(df.columns)[:20],
    })
    return df


@dg.asset_check(
    asset=leer_datos,
    description="Entrada válida (con warnings): columnas clave, unicidad, population > 0.",
    blocking=False,
)
def chequeos_entrada(
    context: dg.AssetCheckExecutionContext,
    leer_datos: pd.DataFrame,
) -> dg.AssetCheckResult:
    df = leer_datos.copy()

    # tolerancia para population nula (default 5%)
    NULL_POP_MAX_PCT = float(os.getenv("COVID_NULL_POP_MAX_PCT", "0.05"))

    # parseo de fecha
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    hoy = pd.Timestamp(datetime.now(timezone.utc).date())

    reglas = []
    def add(n, ok, fa=0, nota=""):
        reglas.append({"nombre": n, "ok": bool(ok), "filas_afectadas": int(fa), "notas": nota})

    # existencia y no-nulos estrictos
    for col in ["location", "date"]:
        if col in df.columns:
            nnull = df[col].isna().sum()
            add(f"{col} no nulo", nnull == 0, nnull)
        else:
            add(f"{col} existe", False, len(df), f"{col} ausente")

    # unicidad (estricto)
    if all(c in df.columns for c in ["location", "date"]):
        dup = df.duplicated(subset=["location", "date"]).sum()
        add("unicidad (location,date)", dup == 0, dup)
    else:
        add("unicidad (location,date)", False, len(df), "cols ausentes")

    # population: permitir % pequeño nulo + >0 estricto
    if "population" in df.columns:
        nnull = df["population"].isna().sum()
        pct = nnull / max(len(df), 1)
        add(f"population no nulo (≤{int(NULL_POP_MAX_PCT*100)}%)", pct <= NULL_POP_MAX_PCT, nnull, f"pct={pct:.2%}")
        bad = (pd.to_numeric(df["population"], errors="coerce") <= 0).sum()
        add("population>0", bad == 0, bad)
    else:
        add("population existe", False, len(df), "population ausente")

    # Warnings informativos (NO bloquean)
    if "new_cases" in df.columns:
        neg = (pd.to_numeric(df["new_cases"], errors="coerce") < 0).sum()
        add("new_cases>=0 (warning)", neg == 0, neg, "revisiones OWID")
    if "date" in df.columns:
        mx = pd.to_datetime(df["date"]).max()
        add("max(date)<=hoy (warning)", (pd.notna(mx) and mx <= hoy), 0, f"max_date={mx}")

    # metadata (tabla markdown)
    tabla_md = (
        "|regla|ok|filas|notas|\n|---|---|---:|---|\n"
        + "\n".join(f"|{r['nombre']}|{r['ok']}|{r['filas_afectadas']}|{r['notas']}|" for r in reglas)
    )
    # pasa si TODO lo no-warning está OK
    passed = all(r["ok"] for r in reglas if "(warning)" not in r["nombre"])

    return dg.AssetCheckResult(
        passed=passed,
        metadata={"resumen_reglas": dg.MetadataValue.md(tabla_md)},
    )


@dg.asset(automation_condition=dg.AutomationCondition.eager())
def datos_procesados(
    context: dg.AssetExecutionContext, leer_datos: pd.DataFrame
) -> pd.DataFrame:
    country_compare = os.getenv("COVID_COUNTRY_COMPARE", "Peru")
    req = {"location", "date", "new_cases", "people_vaccinated", "population"}
    faltan = req - set(leer_datos.columns)
    if faltan:
        raise Exception(f"Faltan columnas requeridas: {sorted(faltan)}")

    df = leer_datos[["location", "date", "new_cases", "people_vaccinated", "population"]].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["new_cases", "people_vaccinated"]).drop_duplicates(subset=["location", "date"])
    df = df[df["location"].isin(["Ecuador", country_compare])]
    context.add_output_metadata({"comparativo": country_compare, "filas": len(df)})
    return df


@dg.asset(automation_condition=dg.AutomationCondition.eager())
def metrica_incidencia_7d(datos_procesados: pd.DataFrame) -> pd.DataFrame:
    df = datos_procesados.sort_values(["location", "date"]).copy()
    df["incidencia_diaria"] = (df["new_cases"] / df["population"]) * 100_000
    df["incidencia_7d"] = df.groupby("location")["incidencia_diaria"].transform(
        lambda s: s.rolling(7, min_periods=7).mean()
    )
    out = (
        df[["date", "location", "incidencia_7d"]]
        .dropna()
        .rename(columns={"date": "fecha", "location": "pais"})
        .reset_index(drop=True)
    )
    return out


@dg.asset(automation_condition=dg.AutomationCondition.eager())
def metrica_factor_crec_7d(datos_procesados: pd.DataFrame) -> pd.DataFrame:
    df = datos_procesados.sort_values(["location", "date"]).copy()
    df["semana_actual"] = df.groupby("location")["new_cases"].transform(
        lambda s: s.rolling(7, min_periods=7).sum()
    )
    df["semana_prev"] = df.groupby("location")["new_cases"].transform(
        lambda s: s.shift(7).rolling(7, min_periods=7).sum()
    )
    df["factor_crec_7d"] = df["semana_actual"] / df["semana_prev"]
    out = (
        df[["date", "location", "semana_actual", "factor_crec_7d"]]
        .dropna()
        .rename(columns={"date": "semana_fin", "location": "pais", "semana_actual": "casos_semana"})
        .reset_index(drop=True)
    )
    return out


@dg.asset_check(
    asset=metrica_incidencia_7d,
    description="incidencia_7d en [0,2000]",
    blocking=True,
)
def chequeos_salida_incidencia(metrica_incidencia_7d: pd.DataFrame) -> dg.AssetCheckResult:
    bad = metrica_incidencia_7d[
        (metrica_incidencia_7d["incidencia_7d"] < 0) | (metrica_incidencia_7d["incidencia_7d"] > 2000)
    ]
    return dg.AssetCheckResult(passed=bad.empty, metadata={"filas_fuera_rango": len(bad)})


@dg.asset(automation_condition=dg.AutomationCondition.eager())
def reporte_excel_covid(
    datos_procesados: pd.DataFrame,
    metrica_incidencia_7d: pd.DataFrame,
    metrica_factor_crec_7d: pd.DataFrame,
) -> str:
    out = "data/reporte_covid.xlsx"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        datos_procesados.to_excel(w, index=False, sheet_name="datos_procesados")
        metrica_incidencia_7d.to_excel(w, index=False, sheet_name="incidencia_7d")
        metrica_factor_crec_7d.to_excel(w, index=False, sheet_name="factor_crec_7d")
    return out


@dg.asset(automation_condition=dg.AutomationCondition.eager())
def eda_perfilado(leer_datos: pd.DataFrame) -> str:
    """Genera data/tabla_perfilado.csv para la entrega (Ecuador vs país comparativo)."""
    import csv

    cc = os.getenv("COVID_COUNTRY_COMPARE", "Peru")
    req = {"location", "date", "new_cases", "people_vaccinated"}
    faltan = req - set(leer_datos.columns)
    if faltan:
        raise Exception(f"Faltan columnas requeridas: {sorted(faltan)}")

    df = leer_datos.copy()
    df = df[df["location"].isin(["Ecuador", cc])].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    tipos = {c: str(t) for c, t in df.dtypes.items()}
    min_nc = pd.to_numeric(df["new_cases"], errors="coerce").min()
    max_nc = pd.to_numeric(df["new_cases"], errors="coerce").max()
    pct_nc = df["new_cases"].isna().mean() * 100
    pct_pv = df["people_vaccinated"].isna().mean() * 100
    fmin, fmax = df["date"].min(), df["date"].max()

    rows = [
        ["columnas", ";".join(df.columns)],
        ["tipos", ";".join([f"{k}:{v}" for k, v in tipos.items()])],
        ["min_new_cases", f"{min_nc}"],
        ["max_new_cases", f"{max_nc}"],
        ["pct_null_new_cases", f"{pct_nc:.2f}%"],
        ["pct_null_people_vaccinated", f"{pct_pv:.2f}%"],
        ["fecha_min", f"{fmin}"],
        ["fecha_max", f"{fmax}"],
    ]
    out = "data/tabla_perfilado.csv"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metrica", "valor"])
        w.writerows(rows)
    return out
