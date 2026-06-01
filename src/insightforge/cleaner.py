from __future__ import annotations

import pandas as pd


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [str(col).strip().lower().replace(" ", "_") for col in cleaned.columns]

    for column in cleaned.columns:
        if pd.api.types.is_object_dtype(cleaned[column]) or pd.api.types.is_string_dtype(cleaned[column]):
            cleaned[column] = cleaned[column].astype(str).str.strip()
            parsed_dates = _parse_possible_dates(cleaned[column])
            if parsed_dates.notna().mean() >= 0.8:
                cleaned[column] = parsed_dates

    cleaned = cleaned.drop_duplicates()

    for column in cleaned.select_dtypes(include="number").columns:
        if cleaned[column].isna().any():
            cleaned[column] = cleaned[column].fillna(cleaned[column].median())

    for column in cleaned.select_dtypes(exclude="number").columns:
        if cleaned[column].isna().any():
            mode = cleaned[column].mode(dropna=True)
            cleaned[column] = cleaned[column].fillna(mode.iloc[0] if not mode.empty else "unknown")

    return cleaned


def _parse_possible_dates(series: pd.Series) -> pd.Series:
    if not _looks_like_date_column(series.name, series):
        return pd.Series([pd.NaT] * len(series), index=series.index)
    return pd.to_datetime(series, errors="coerce")


def _looks_like_date_column(column: object, series: pd.Series) -> bool:
    name = str(column).lower()
    if any(token in name for token in ("date", "time", "month", "year")):
        return True
    sample = series.dropna().astype(str).head(10)
    return bool(sample.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$").mean() >= 0.8)
