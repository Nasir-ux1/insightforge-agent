from __future__ import annotations

import argparse

from insightforge.agent import run_analysis


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the InsightForge autonomous analyst.")
    parser.add_argument("dataset", help="Path to a CSV or XLSX file.")
    parser.add_argument(
        "--question",
        default="What are the main drivers of revenue performance over time?",
        help="Business question to answer.",
    )
    parser.add_argument("--output-dir", default="reports", help="Directory for report and charts.")
    args = parser.parse_args()

    result = run_analysis(args.dataset, args.question, args.output_dir)
    print(f"Report written to: {result.report_path}")
    for insight in result.insights:
        print(f"- {insight.title}: {insight.detail}")


if __name__ == "__main__":
    main()
