from __future__ import annotations

import pandas as pd

from insightforge.models import DatasetProfile


def load_dataset(path: str) -> pd.DataFrame:
    if path.lower().endswith(".xlsx"):
        return pd.read_excel(path)
    return pd.read_csv(path)


def infer_datetime_columns(df: pd.DataFrame) -> list[str]:
    datetime_columns: list[str] = []
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            datetime_columns.append(column)
            continue
        if pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_string_dtype(df[column]):
            if not _looks_like_date_column(column, df[column]):
                continue
            parsed = pd.to_datetime(df[column], errors="coerce")
            if parsed.notna().mean() >= 0.8:
                datetime_columns.append(column)
    return datetime_columns


def _looks_like_date_column(column: object, series: pd.Series) -> bool:
    name = str(column).lower()
    if any(token in name for token in ("date", "time", "month", "year")):
        return True
    sample = series.dropna().astype(str).head(10)
    return bool(sample.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$").mean() >= 0.8)


def profile_dataset(df: pd.DataFrame) -> DatasetProfile:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    datetime_columns = infer_datetime_columns(df)
    categorical_columns = [
        col
        for col in df.columns
        if col not in numeric_columns and col not in datetime_columns
    ]
    memory_mb = float(df.memory_usage(deep=True).sum() / (1024 * 1024))
    return DatasetProfile(
        rows=int(df.shape[0]),
        columns=int(df.shape[1]),
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        datetime_columns=datetime_columns,
        missing_values={k: int(v) for k, v in df.isna().sum().items() if int(v) > 0},
        duplicate_rows=int(df.duplicated().sum()),
        memory_mb=round(memory_mb, 3),
    )
