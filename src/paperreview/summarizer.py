"""Transparent summarization helpers for synthetic papers."""

from __future__ import annotations

import pandas as pd


def summarize_papers(papers: pd.DataFrame) -> pd.DataFrame:
    """Create compact paper summaries and extracted review cues."""
    rows = []
    for paper in papers.itertuples(index=False):
        rows.append({
            "paper_id": paper.paper_id,
            "title": paper.title,
            "field": paper.field,
            "short_summary": _first_sentence(paper.abstract),
            "research_question": f"How well does the paper address {paper.research_problem}?",
            "claimed_contribution": paper.claimed_contribution,
            "method_family": paper.method_family,
            "limitation_signal": _limitation_signal(str(paper.limitations)),
            "human_reader_note": "Use this summary as a navigation aid, not as a substitute for reading the full paper.",
        })
    return pd.DataFrame(rows)


def _first_sentence(text: str) -> str:
    sentence = str(text).split(".")[0].strip()
    return sentence + "." if sentence else "No summary available."


def _limitation_signal(text: str) -> str:
    low = text.lower()
    if "vague" in low or "briefly" in low:
        return "limitations_need_review"
    if "not yet available" in low or "constraints" in low:
        return "artifact_or_data_release_constraint"
    return "limitations_discussed"
