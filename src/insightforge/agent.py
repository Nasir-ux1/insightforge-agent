from __future__ import annotations

from pathlib import Path

from insightforge.analyst import generate_insights
from insightforge.charts import build_charts
from insightforge.cleaner import clean_dataset
from insightforge.models import AnalysisResult
from insightforge.planner import plan_analysis
from insightforge.profiler import load_dataset, profile_dataset
from insightforge.reporter import write_report


def run_analysis(dataset_path: str, question: str, output_dir: str = "reports") -> AnalysisResult:
    output_path = Path(output_dir)
    raw_df = load_dataset(dataset_path)
    df = clean_dataset(raw_df)
    profile = profile_dataset(df)
    plan = plan_analysis(question, df)
    insights = generate_insights(df, plan)
    charts = build_charts(df, plan, output_path)

    result = AnalysisResult(
        profile=profile,
        question=plan,
        insights=insights,
        chart_paths=charts,
        report_path=None,
    )
    result.report_path = write_report(result, output_path)
    return result
