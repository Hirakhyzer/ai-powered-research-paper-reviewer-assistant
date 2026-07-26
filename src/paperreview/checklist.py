"""Reproducibility and reviewer checklist generation."""

from __future__ import annotations

import pandas as pd


def build_reproducibility_checklist(papers: pd.DataFrame, methodology_audit: pd.DataFrame) -> pd.DataFrame:
    """Create a reproducibility checklist per paper."""
    audit_lookup = methodology_audit.set_index("paper_id") if not methodology_audit.empty else pd.DataFrame()
    rows = []
    for paper in papers.itertuples(index=False):
        methods_clear = paper.dataset_size >= 500 and paper.evaluation_metric_count >= 2
        baselines_ready = paper.baseline_count >= 2
        ablations_ready = paper.ablation_count > 0
        artifacts_ready = bool(paper.code_available and paper.data_available)
        limitations_ready = "vague" not in str(paper.limitations).lower()
        score = sum([methods_clear, baselines_ready, ablations_ready, artifacts_ready, limitations_ready]) / 5
        risk_class = audit_lookup.loc[paper.paper_id, "methodology_risk_class"] if not audit_lookup.empty and paper.paper_id in audit_lookup.index else "unknown"
        rows.append({
            "paper_id": paper.paper_id,
            "methods_clear": bool(methods_clear),
            "baselines_sufficient": bool(baselines_ready),
            "ablation_reported": bool(ablations_ready),
            "artifacts_available": bool(artifacts_ready),
            "limitations_discussed": bool(limitations_ready),
            "reproducibility_readiness_score": round(float(score), 4),
            "methodology_risk_class": risk_class,
            "reproducibility_review_items": _items(methods_clear, baselines_ready, ablations_ready, artifacts_ready, limitations_ready),
        })
    return pd.DataFrame(rows).sort_values("reproducibility_readiness_score").reset_index(drop=True)


def build_reviewer_checklist(summaries: pd.DataFrame, methodology_audit: pd.DataFrame, citation_comparison: pd.DataFrame, reproducibility: pd.DataFrame) -> pd.DataFrame:
    """Generate human-review prompts without making accept/reject decisions."""
    merged = summaries.merge(methodology_audit, on=["paper_id", "field", "method_family"], how="left")
    merged = merged.merge(citation_comparison[["paper_id", "citation_coverage_score", "related_work_gap_flags"]], on="paper_id", how="left")
    merged = merged.merge(reproducibility[["paper_id", "reproducibility_readiness_score", "reproducibility_review_items"]], on="paper_id", how="left")
    rows = []
    for paper in merged.itertuples(index=False):
        prompts = ["Read the full paper before forming any review judgment"]
        if paper.methodology_risk_score >= 0.40:
            prompts.append("Inspect methodology design and claimed evidence strength")
        if paper.citation_coverage_score < 0.55:
            prompts.append("Check whether related work coverage is broad and current")
        if paper.reproducibility_readiness_score < 0.70:
            prompts.append("Request clearer reproducibility or artifact details")
        if paper.limitation_signal != "limitations_discussed":
            prompts.append("Review limitations and external-validity discussion")
        rows.append({
            "paper_id": paper.paper_id,
            "title": paper.title,
            "review_focus_count": len(prompts),
            "reviewer_prompts": " | ".join(prompts),
            "human_review_recommendation": "full_expert_review_required",
        })
    return pd.DataFrame(rows)


def checklist_summary(reproducibility: pd.DataFrame, reviewer: pd.DataFrame) -> dict[str, int | float]:
    if reproducibility.empty:
        return {"low_reproducibility_count": 0, "mean_reproducibility_readiness": 0.0, "review_checklist_count": int(len(reviewer))}
    return {
        "low_reproducibility_count": int((reproducibility["reproducibility_readiness_score"] < 0.6).sum()),
        "mean_reproducibility_readiness": float(reproducibility["reproducibility_readiness_score"].mean()),
        "review_checklist_count": int(len(reviewer)),
    }


def _items(methods_clear: bool, baselines_ready: bool, ablations_ready: bool, artifacts_ready: bool, limitations_ready: bool) -> str:
    items = []
    if not methods_clear:
        items.append("clarify_dataset_metrics_or_protocol")
    if not baselines_ready:
        items.append("add_or_justify_baselines")
    if not ablations_ready:
        items.append("add_ablation_or_component_analysis")
    if not artifacts_ready:
        items.append("clarify_code_data_artifact_access")
    if not limitations_ready:
        items.append("expand_limitations_and_external_validity")
    return "|".join(items) if items else "reproducibility_details_appear_sufficient"
