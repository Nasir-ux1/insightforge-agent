# InsightForge: Autonomous Data Analyst Agent

InsightForge is a portfolio-ready AI/ML agent project that turns a raw CSV/XLSX dataset and a natural-language business question into a structured analysis report.

The project demonstrates agent-style decomposition: dataset profiling, cleaning, analysis planning, insight generation, visualization, and report writing.

## Features

- Upload or pass a CSV/XLSX dataset
- Automatic data profiling: rows, columns, missing values, duplicates, numeric/categorical/date fields
- Data cleaning: normalized columns, duplicate removal, missing value handling, date inference
- Natural-language question planning
- Automated metric and dimension selection
- Trend analysis over time
- Segment/driver analysis
- Chart generation with matplotlib
- Markdown executive report export
- CLI and Streamlit app entry points
- Unit tests for planner, cleaner, and end-to-end agent flow

## Architecture

```text
User Question + Dataset
        |
        v
Dataset Profiler -> Data Cleaner -> Analysis Planner
        |                              |
        v                              v
 Insight Generator -> Chart Builder -> Report Writer
        |
        v
 Markdown Report + PNG Charts + Follow-up Ready Insights
```

## Tech Stack

- Python
- pandas / numpy
- matplotlib
- Streamlit
- pytest

Optional extension points:

- OpenAI/Claude/Gemini for narrative generation
- FAISS/ChromaDB for RAG over uploaded reports
- FastAPI for API deployment
- Docker for reproducible execution

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the CLI:

```bash
python -m insightforge.cli data/sample_sales.csv --question "What are the main drivers of revenue performance over time?"
```

Run the Streamlit UI:

```bash
streamlit run app.py
```

Run tests:

```bash
pytest
```

## Example Output

For the included sample sales dataset, InsightForge produces:

- Dataset profile
- Revenue overview
- Top-performing region/product/channel
- Monthly revenue trend
- Driver insight
- Markdown report in `reports/insight_report.md`
- PNG charts in `reports/`

## Why This Project Is Strong

This is heavier than a normal chatbot because the agent uses tools and intermediate reasoning steps instead of only generating text. It performs real data operations, creates artifacts, and gives explainable evidence for each insight.

Resume bullet:

```text
Built InsightForge, an autonomous data analyst agent that profiles uploaded datasets, cleans data, plans analysis from natural-language questions, generates pandas-based insights, creates visualizations, and exports executive Markdown reports.
```

## Roadmap

- Add LLM-generated executive summaries
- Add RAG over uploaded PDF reports
- Add sandboxed Python code-generation agent
- Add dataset quality scoring
- Add Docker deployment
- Add benchmark/evaluation suite for generated insights
