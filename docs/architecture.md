# Architecture

InsightForge is split into small modules so each agent step is testable.

```text
Dataset -> Cleaner -> Profiler -> Planner -> Analyst -> Charts -> Report
```

## Modules

- `cleaner.py`: normalizes columns, infers dates, removes duplicates, fills missing values.
- `profiler.py`: identifies numeric, categorical, and datetime fields.
- `planner.py`: converts a natural-language question into a metric/dimension plan.
- `analyst.py`: generates deterministic insights using pandas.
- `charts.py`: creates static visual evidence for the report.
- `reporter.py`: writes a Markdown executive report.

This keeps the project usable without an LLM API key while leaving clear extension points for RAG, code-generation, or model-backed narrative summaries.
