"""Markdown report generation for the synthetic reviewer assistant."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_report(path: str | Path, summary: dict, quality: pd.DataFrame, methodology: pd.DataFrame, citation_comparison: pd.DataFrame, reproducibility: pd.DataFrame, reviewer: pd.DataFrame) -> None:
    """Write a compact reviewer-support report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    top_risk = methodology.head(8)[["paper_id", "methodology_risk_score", "methodology_risk_class", "weaknesses"]]
    low_citations = citation_comparison.head(8)[["paper_id", "citation_coverage_score", "related_work_gap_flags"]]
    low_repro = reproducibility.head(8)[["paper_id", "reproducibility_readiness_score", "reproducibility_review_items"]]
    recommendations = reviewer.head(8)[["paper_id", "review_focus_count", "reviewer_prompts"]]

    content = [
        "# Synthetic Research Paper Reviewer Assistant Report",
        "",
        "> This report is generated from fictional synthetic papers. It supports human review only and must not be used for automatic acceptance, rejection, plagiarism judgment, or misconduct determinations.",
        "",
        "## Summary",
        "",
        _dict_table(summary),
        "",
        "## Highest methodology-risk papers",
        "",
        top_risk.to_markdown(index=False),
        "",
        "## Lowest citation-coverage papers",
        "",
        low_citations.to_markdown(index=False),
        "",
        "## Reproducibility review items",
        "",
        low_repro.to_markdown(index=False),
        "",
        "## Reviewer checklist sample",
        "",
        recommendations.to_markdown(index=False),
        "",
        "## Quality support score bands",
        "",
        quality["quality_band"].value_counts().rename_axis("quality_band").reset_index(name="paper_count").to_markdown(index=False),
        "",
        "## Governance note",
        "",
        "Every output is a review-support signal. Final interpretation requires careful full-paper reading, domain expertise, confidentiality controls, and editorial policy.",
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def _dict_table(summary: dict) -> str:
    return pd.DataFrame([{"metric": key, "value": value} for key, value in summary.items()]).to_markdown(index=False)
