from __future__ import annotations

import re

import pandas as pd

from insightforge.models import AnalysisQuestion


TREND_WORDS = {"trend", "over time", "monthly", "weekly", "daily", "quarter", "q1", "q2", "q3", "q4"}
DRIVER_WORDS = {"why", "driver", "cause", "reason", "drop", "increase", "decrease", "impact"}


def plan_analysis(question: str, df: pd.DataFrame) -> AnalysisQuestion:
    normalized = question.lower()
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = [
        column
        for column in df.select_dtypes(exclude="number").columns
        if not pd.api.types.is_datetime64_any_dtype(df[column])
    ]

    metric = _select_metric(normalized, numeric_columns)
    dimensions = _select_dimensions(normalized, categorical_columns)
    if not dimensions:
        dimensions = categorical_columns[:2]

    return AnalysisQuestion(
        raw=question,
        metric=metric,
        dimensions=dimensions[:3],
        wants_trend=any(word in normalized for word in TREND_WORDS),
        wants_drivers=any(word in normalized for word in DRIVER_WORDS),
    )


def _select_metric(question: str, numeric_columns: list[str]) -> str | None:
    for column in numeric_columns:
        aliases = {column, column.replace("_", " "), re.sub(r"[_-]", "", column)}
        if any(alias in question for alias in aliases):
            return column
    priority = ["revenue", "sales", "profit", "cost", "units", "amount", "price"]
    for name in priority:
        for column in numeric_columns:
            if name in column:
                return column
    return numeric_columns[0] if numeric_columns else None


def _select_dimensions(question: str, categorical_columns: list[str]) -> list[str]:
    matches = []
    for column in categorical_columns:
        aliases = {column, column.replace("_", " ")}
        if any(alias in question for alias in aliases):
            matches.append(column)
    return matches
