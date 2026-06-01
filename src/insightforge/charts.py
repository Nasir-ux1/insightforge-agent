from __future__ import annotations

from pathlib import Path

import pandas as pd

from insightforge.models import AnalysisQuestion


def build_charts(df: pd.DataFrame, question: AnalysisQuestion, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not question.metric:
        return []

    paths: list[Path] = []
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return paths

    metric = question.metric
    if question.dimensions:
        dimension = question.dimensions[0]
        grouped = df.groupby(dimension, dropna=False)[metric].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(9, 5))
        grouped.plot(kind="bar", ax=ax, color="#2f6f73")
        ax.set_title(f"{metric} by {dimension}")
        ax.set_xlabel(dimension)
        ax.set_ylabel(metric)
        fig.tight_layout()
        bar_path = output_dir / "metric_by_dimension.png"
        fig.savefig(bar_path, dpi=160)
        plt.close(fig)
        paths.append(bar_path)

    date_column = _first_datetime_column(df)
    if date_column:
        monthly = df[[date_column, metric]].dropna().set_index(date_column)[metric].resample("ME").sum()
        fig, ax = plt.subplots(figsize=(9, 5))
        monthly.plot(kind="line", marker="o", ax=ax, color="#6b4e9b")
        ax.set_title(f"Monthly {metric} trend")
        ax.set_xlabel("month")
        ax.set_ylabel(metric)
        fig.tight_layout()
        trend_path = output_dir / "metric_trend.png"
        fig.savefig(trend_path, dpi=160)
        plt.close(fig)
        paths.append(trend_path)

    return paths


def _first_datetime_column(df: pd.DataFrame) -> str | None:
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            return column
    return None
