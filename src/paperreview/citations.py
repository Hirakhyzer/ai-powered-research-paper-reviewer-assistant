"""Citation coverage comparison for synthetic papers."""

from __future__ import annotations

import pandas as pd


def compare_citations(papers: pd.DataFrame, citation_library: pd.DataFrame, paper_citations: pd.DataFrame) -> pd.DataFrame:
    """Compare each paper's citation breadth, recency, and evidence diversity."""
    links = paper_citations.merge(citation_library, on="citation_id", how="left", suffixes=("", "_library"))
    rows = []
    for paper in papers.itertuples(index=False):
        group = links[links["paper_id"].eq(paper.paper_id)].copy()
        count = int(len(group))
        method_diversity = int(group["method_family"].nunique()) if count else 0
        evidence_diversity = int(group["evidence_type"].nunique()) if count else 0
        recent_share = float((group["year"] >= 2021).mean()) if count else 0.0
        aligned_share = float((group["alignment_score"] >= 0.65).mean()) if count else 0.0
        coverage_score = min(1.0, 0.10 * count + 0.10 * method_diversity + 0.09 * evidence_diversity + 0.22 * recent_share + 0.24 * aligned_share)
        gaps = []
        if count < 5:
            gaps.append("low_citation_count")
        if method_diversity < 2:
            gaps.append("narrow_method_coverage")
        if evidence_diversity < 3:
            gaps.append("limited_evidence_types")
        if recent_share < 0.35:
            gaps.append("limited_recent_work")
        rows.append({
            "paper_id": paper.paper_id,
            "field": paper.field,
            "citation_count": count,
            "method_diversity": method_diversity,
            "evidence_diversity": evidence_diversity,
            "recent_citation_share": round(recent_share, 4),
            "aligned_citation_share": round(aligned_share, 4),
            "citation_coverage_score": round(float(coverage_score), 4),
            "related_work_gap_flags": "|".join(gaps) if gaps else "coverage_appears_broad",
            "requires_related_work_review": bool(gaps),
        })
    return pd.DataFrame(rows).sort_values("citation_coverage_score").reset_index(drop=True)


def citation_summary(comparison: pd.DataFrame) -> dict[str, int | float]:
    """Summarize citation comparison outputs."""
    if comparison.empty:
        return {"low_citation_coverage_count": 0, "mean_citation_coverage_score": 0.0}
    return {
        "low_citation_coverage_count": int((comparison["citation_coverage_score"] < 0.55).sum()),
        "mean_citation_coverage_score": float(comparison["citation_coverage_score"].mean()),
    }
