from __future__ import annotations

from pathlib import Path

from insightforge.models import AnalysisResult


def write_report(result: AnalysisResult, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "insight_report.md"

    profile = result.profile
    question = result.question
    lines = [
        "# InsightForge Analysis Report",
        "",
        f"**Question:** {question.raw}",
        "",
        "## Dataset Profile",
        "",
        f"- Rows: {profile.rows}",
        f"- Columns: {profile.columns}",
        f"- Numeric columns: {', '.join(profile.numeric_columns) or 'None'}",
        f"- Categorical columns: {', '.join(profile.categorical_columns) or 'None'}",
        f"- Datetime columns: {', '.join(profile.datetime_columns) or 'None'}",
        f"- Duplicate rows removed/detected: {profile.duplicate_rows}",
        f"- Missing values: {profile.missing_values or 'None detected'}",
        "",
        "## Insights",
        "",
    ]

    for index, insight in enumerate(result.insights, start=1):
        lines.extend([
            f"### {index}. {insight.title}",
            "",
            insight.detail,
            "",
            f"Evidence: `{insight.evidence}`",
            "",
        ])

    if result.chart_paths:
        lines.extend(["## Charts", ""])
        for chart in result.chart_paths:
            lines.append(f"- {chart.name}")
        lines.append("")

    lines.extend([
        "## Recommended Next Steps",
        "",
        "- Validate the highest-impact segment with a larger dataset.",
        "- Add external market or operational context before making business decisions.",
        "- Track this analysis as a repeatable notebook or scheduled report.",
        "",
    ])

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
