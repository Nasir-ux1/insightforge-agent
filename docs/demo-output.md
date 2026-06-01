# Demo Output

Command:

```bash
PYTHONPATH=src python -m insightforge.cli data/sample_sales.csv --question "What are the main drivers of revenue performance over time?"
```

Expected output:

```text
Report written to: reports/insight_report.md
- revenue overview: Total revenue is 266,700.00; average per row is 11,112.50.
- Top region: West leads revenue with 88,350.00, contributing 33.1% of the total.
- Top product: Alpha leads revenue with 103,450.00, contributing 38.8% of the total.
- Time trend: revenue increased by 21.8% from the first to the last period.
- Likely performance driver: The biggest spread is across region: West outperforms South by 40,350.00 in revenue.
```
