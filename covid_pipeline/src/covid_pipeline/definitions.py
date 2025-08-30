import dagster as dg
from .assets.assets import (
    leer_datos,
    chequeos_entrada,
    datos_procesados,
    metrica_incidencia_7d,
    metrica_factor_crec_7d,
    chequeos_salida_incidencia,
    reporte_excel_covid,
    eda_perfilado,
)

defs = dg.Definitions(
    assets=[
        leer_datos,
        datos_procesados,
        metrica_incidencia_7d,
        metrica_factor_crec_7d,
        reporte_excel_covid,
        eda_perfilado,
    ],
    asset_checks=[chequeos_entrada, chequeos_salida_incidencia],
)
