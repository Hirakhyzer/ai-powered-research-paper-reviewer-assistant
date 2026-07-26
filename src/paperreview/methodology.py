"""Methodology weakness detection for synthetic papers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def audit_methodology(papers: pd.DataFrame) -> pd.DataFrame:
    """Score methodology risk using transparent, review-support heuristics."""
    rows = []
    for paper in papers.itertuples(index=False):
        weaknesses = []
        risk = 0.0
        if paper.baseline_count < 2:
            weaknesses.append("limited_baseline_comparison")
            risk += 0.23
        if paper.evaluation_metric_count < 2:
            weaknesses.append("narrow_metric_set")
            risk += 0.16
        if paper.dataset_size < 500:
            weaknesses.append("small_dataset")
            risk += 0.18
        if paper.ablation_count == 0:
            weaknesses.append("missing_ablation")
            risk += 0.16
        if paper.claim_strength > paper.evidence_strength + 0.25:
            weaknesses.append("claim_evidence_mismatch")
            risk += 0.20
        if "vague" in str(paper.limitations).lower():
            weaknesses.append("weak_limitations_discussion")
            risk += 0.12
        if not bool(paper.code_available):
            weaknesses.append("code_not_available")
            risk += 0.08
        risk_score = float(np.clip(risk, 0, 1))
        rows.append({
            "paper_id": paper.paper_id,
            "field": paper.field,
            "method_family": paper.method_family,
            "methodology_risk_score": round(risk_score, 4),
            "methodology_risk_class": _risk_class(risk_score),
            "weakness_count": len(weaknesses),
            "weaknesses": "|".join(weaknesses) if weaknesses else "no_major_methodology_warning",
            "requires_methodology_review": bool(risk_score >= 0.40),
        })
    return pd.DataFrame(rows).sort_values("methodology_risk_score", ascending=False).reset_index(drop=True)


def methodology_summary(audit: pd.DataFrame) -> dict[str, int | float]:
    """Summarize methodology risk."""
    if audit.empty:
        return {"high_methodology_risk_count": 0, "mean_methodology_risk_score": 0.0}
    return {
        "high_methodology_risk_count": int(audit["methodology_risk_class"].isin(["high", "critical"]).sum()),
        "mean_methodology_risk_score": float(audit["methodology_risk_score"].mean()),
    }


def _risk_class(score: float) -> str:
    if score >= 0.78:
        return "critical"
    if score >= 0.58:
        return "high"
    if score >= 0.32:
        return "medium"
    return "low"
