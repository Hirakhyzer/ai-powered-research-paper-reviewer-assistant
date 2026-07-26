"""Paper-quality scoring and review-support summaries."""

from __future__ import annotations

import numpy as np
import pandas as pd


def score_paper_quality(methodology: pd.DataFrame, citation_comparison: pd.DataFrame, reproducibility: pd.DataFrame) -> pd.DataFrame:
    """Combine transparent signals into a non-decisive quality-support score."""
    merged = methodology[["paper_id", "methodology_risk_score", "methodology_risk_class"]].merge(
        citation_comparison[["paper_id", "citation_coverage_score"]], on="paper_id", how="outer"
    ).merge(
        reproducibility[["paper_id", "reproducibility_readiness_score"]], on="paper_id", how="outer"
    ).fillna(0)
    rows = []
    for item in merged.itertuples(index=False):
        quality = 0.42 * (1 - float(item.methodology_risk_score)) + 0.30 * float(item.citation_coverage_score) + 0.28 * float(item.reproducibility_readiness_score)
        quality = float(np.clip(quality, 0, 1))
        rows.append({
            "paper_id": item.paper_id,
            "paper_quality_support_score": round(quality, 4),
            "quality_band": _quality_band(quality),
            "review_recommendation": _recommendation(quality, float(item.methodology_risk_score)),
            "decision_boundary": "support signal only; not acceptance, rejection, or misconduct judgment",
        })
    return pd.DataFrame(rows).sort_values("paper_quality_support_score", ascending=False).reset_index(drop=True)


def review_summary(quality: pd.DataFrame) -> dict[str, int | float | str]:
    """Create compact summary for JSON, reports, and audit logs."""
    if quality.empty:
        return {"paper_count": 0, "mean_quality_support_score": 0.0, "review_support_boundary": "human peer review required"}
    return {
        "paper_count": int(len(quality)),
        "mean_quality_support_score": float(quality["paper_quality_support_score"].mean()),
        "deep_review_recommended_count": int(quality["review_recommendation"].eq("deep_methodology_and_related_work_review").sum()),
        "review_support_boundary": "human peer review required; no automatic paper decision",
    }


def _quality_band(score: float) -> str:
    if score >= 0.78:
        return "strong_supporting_evidence"
    if score >= 0.58:
        return "moderate_supporting_evidence"
    if score >= 0.36:
        return "needs_substantial_review"
    return "high_review_risk"


def _recommendation(score: float, methodology_risk: float) -> str:
    if methodology_risk >= 0.58 or score < 0.45:
        return "deep_methodology_and_related_work_review"
    if score < 0.65:
        return "standard_expert_review_with_reproducibility_questions"
    return "standard_expert_review"
