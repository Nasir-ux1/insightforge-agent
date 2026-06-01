from __future__ import annotations

import unittest
from pathlib import Path

import pandas as pd

from insightforge.agent import run_analysis
from insightforge.cleaner import clean_dataset
from insightforge.planner import plan_analysis


ROOT = Path(__file__).resolve().parents[1]


class InsightForgeTests(unittest.TestCase):
    def test_clean_dataset_normalizes_columns_and_dates(self) -> None:
        df = pd.DataFrame(
            {
                "Order Date": ["2025-01-01", "2025-01-02"],
                " Revenue ": [100, 200],
                "Region": [" North ", "South"],
            }
        )

        cleaned = clean_dataset(df)

        self.assertEqual(list(cleaned.columns), ["order_date", "revenue", "region"])
        self.assertTrue(str(cleaned["order_date"].dtype).startswith("datetime64"))
        self.assertEqual(cleaned.loc[0, "region"], "North")

    def test_plan_analysis_selects_revenue_and_region(self) -> None:
        df = pd.DataFrame({"revenue": [100, 200], "region": ["North", "South"]})

        plan = plan_analysis("Why did revenue change by region?", df)

        self.assertEqual(plan.metric, "revenue")
        self.assertIn("region", plan.dimensions)
        self.assertTrue(plan.wants_drivers)

    def test_plan_analysis_excludes_datetime_dimensions(self) -> None:
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2025-01-01", "2025-02-01"]),
                "region": ["North", "South"],
                "revenue": [100, 200],
            }
        )

        plan = plan_analysis("What drives revenue over time?", df)

        self.assertNotIn("date", plan.dimensions)
        self.assertIn("region", plan.dimensions)

    def test_run_analysis_writes_report(self) -> None:
        result = run_analysis(
            str(ROOT / "data" / "sample_sales.csv"),
            "What are the main drivers of revenue performance over time?",
            str(ROOT / "reports"),
        )

        self.assertIsNotNone(result.report_path)
        self.assertTrue(result.report_path.exists())
        self.assertTrue(result.insights)
        self.assertEqual(result.profile.rows, 24)


if __name__ == "__main__":
    unittest.main()
