import pandas as pd
def rolling_mean(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()
def sum_window(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).sum()
