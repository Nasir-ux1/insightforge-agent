from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DatasetProfile:
    rows: int
    columns: int
    numeric_columns: list[str]
    categorical_columns: list[str]
    datetime_columns: list[str]
    missing_values: dict[str, int]
    duplicate_rows: int
    memory_mb: float


@dataclass(frozen=True)
class AnalysisQuestion:
    raw: str
    metric: str | None
    dimensions: list[str]
    wants_trend: bool
    wants_drivers: bool


@dataclass
class Insight:
    title: str
    detail: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    profile: DatasetProfile
    question: AnalysisQuestion
    insights: list[Insight]
    chart_paths: list[Path]
    report_path: Path | None
