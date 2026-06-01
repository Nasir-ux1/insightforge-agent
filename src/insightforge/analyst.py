from __future__ import annotations

import pandas as pd

from insightforge.models import AnalysisQuestion, Insight


def generate_insights(df: pd.DataFrame, question: AnalysisQuestion) -> list[Insight]:
    if not question.metric:
        return [Insight("No numeric metric found", "Upload a dataset with at least one numeric column.")]

    metric = question.metric
    insights = [_overall_summary(df, metric)]

    for dimension in question.dimensions:
        if dimension in df.columns:
            insights.append(_top_dimension(df, metric, dimension))

    date_column = _first_datetime_column(df)
    if date_column:
        insights.append(_trend_insight(df, metric, date_column))

    if question.wants_drivers and question.dimensions:
        insights.append(_driver_insight(df, metric, question.dimensions[0]))

    return insights


def _overall_summary(df: pd.DataFrame, metric: str) -> Insight:
    total = float(df[metric].sum())
    mean = float(df[metric].mean())
    return Insight(
        title=f"{metric} overview",
        detail=f"Total {metric} is {total:,.2f}; average per row is {mean:,.2f}.",
        evidence={"total": round(total, 2), "mean": round(mean, 2), "rows": int(len(df))},
    )


def _top_dimension(df: pd.DataFrame, metric: str, dimension: str) -> Insight:
    grouped = df.groupby(dimension, dropna=False)[metric].sum().sort_values(ascending=False)
    top_key = str(grouped.index[0])
    top_value = float(grouped.iloc[0])
    share = top_value / float(grouped.sum()) if float(grouped.sum()) else 0
    return Insight(
        title=f"Top {dimension}",
        detail=f"{top_key} leads {metric} with {top_value:,.2f}, contributing {share:.1%} of the total.",
        evidence={"dimension": dimension, "leader": top_key, "value": round(top_value, 2), "share": round(share, 4)},
    )


def _trend_insight(df: pd.DataFrame, metric: str, date_column: str) -> Insight:
    frame = df[[date_column, metric]].dropna().copy()
    frame[date_column] = pd.to_datetime(frame[date_column], errors="coerce")
    monthly = frame.dropna().set_index(date_column)[metric].resample("ME").sum()
    if len(monthly) < 2:
        return Insight("Trend unavailable", "At least two time periods are required for trend analysis.")

    start = float(monthly.iloc[0])
    end = float(monthly.iloc[-1])
    change = (end - start) / start if start else 0
    direction = "increased" if change >= 0 else "decreased"
    return Insight(
        title="Time trend",
        detail=f"{metric} {direction} by {abs(change):.1%} from the first to the last period.",
        evidence={"first_period": round(start, 2), "last_period": round(end, 2), "change_pct": round(change, 4)},
    )


def _driver_insight(df: pd.DataFrame, metric: str, dimension: str) -> Insight:
    grouped = df.groupby(dimension, dropna=False)[metric].sum().sort_values()
    weakest = str(grouped.index[0])
    strongest = str(grouped.index[-1])
    gap = float(grouped.iloc[-1] - grouped.iloc[0])
    return Insight(
        title="Likely performance driver",
        detail=(
            f"The biggest spread is across {dimension}: {strongest} outperforms "
            f"{weakest} by {gap:,.2f} in {metric}."
        ),
        evidence={"dimension": dimension, "strongest": strongest, "weakest": weakest, "gap": round(gap, 2)},
    )


def _first_datetime_column(df: pd.DataFrame) -> str | None:
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            return column
    return None
