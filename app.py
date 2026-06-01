from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from insightforge.agent import run_analysis


st.set_page_config(page_title="InsightForge Agent", layout="wide")
st.title("InsightForge")
st.caption("Autonomous data analyst and research-style reporting agent")

uploaded = st.file_uploader("Upload a CSV or XLSX dataset", type=["csv", "xlsx"])
question = st.text_input(
    "Ask a business question",
    "What are the main drivers of revenue performance over time?",
)

if uploaded and st.button("Run analysis", type="primary"):
    suffix = Path(uploaded.name).suffix
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        dataset_path = tmp.name

    with st.spinner("Profiling, cleaning, planning, analyzing, and writing report..."):
        result = run_analysis(dataset_path, question)

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Dataset Profile")
        st.json(result.profile.__dict__)
    with right:
        st.subheader("Agent Plan")
        st.json(result.question.__dict__)

    st.subheader("Insights")
    for insight in result.insights:
        st.markdown(f"**{insight.title}**")
        st.write(insight.detail)
        st.caption(str(insight.evidence))

    if result.chart_paths:
        st.subheader("Charts")
        for chart in result.chart_paths:
            st.image(str(chart))

    if result.report_path:
        st.download_button(
            "Download Markdown report",
            result.report_path.read_text(encoding="utf-8"),
            file_name="insight_report.md",
        )
