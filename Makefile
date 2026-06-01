.PHONY: test demo app lint

test:
	PYTHONPATH=src python -m unittest discover -s tests -v

demo:
	PYTHONPATH=src python -m insightforge.cli data/sample_sales.csv --question "What are the main drivers of revenue performance over time?" --output-dir reports

app:
	streamlit run app.py

lint:
	ruff check src tests
