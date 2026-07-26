"""Run the complete synthetic AI-powered research paper reviewer assistant lab.

The command uses only fictional papers, methods, claims, citations, and review
signals. It demonstrates summarization, methodology weakness detection, citation
coverage comparison, reproducibility checklist generation, reviewer checklist
creation, reporting, figures, and a hash-chained audit log without real manuscripts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from paperreview.audit import append_record, verify_log
from paperreview.checklist import build_reproducibility_checklist, build_reviewer_checklist, checklist_summary
from paperreview.citations import citation_summary, compare_citations
from paperreview.config import ensure_output_dirs, set_seed
from paperreview.methodology import audit_methodology, methodology_summary
from paperreview.reporting import write_report
from paperreview.scoring import review_summary, score_paper_quality
from paperreview.summarizer import summarize_papers
from paperreview.synthetic import SyntheticPaperConfig, generate_synthetic_review_data
from paperreview.visualization import (
    plot_citation_coverage,
    plot_methodology_risk,
    plot_quality_scores,
    plot_reproducibility,
    plot_review_recommendations,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic research paper reviewer assistant lab.")
    parser.add_argument("--papers", type=int, default=36)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    outputs = ensure_output_dirs(args.output_dir)
    data = generate_synthetic_review_data(SyntheticPaperConfig(papers=args.papers, seed=args.seed))
    papers = data["papers"]
    citation_library = data["citation_library"]
    paper_citations = data["paper_citations"]

    summaries = summarize_papers(papers)
    methodology = audit_methodology(papers)
    citation_comparison = compare_citations(papers, citation_library, paper_citations)
    reproducibility = build_reproducibility_checklist(papers, methodology)
    reviewer = build_reviewer_checklist(summaries, methodology, citation_comparison, reproducibility)
    quality = score_paper_quality(methodology, citation_comparison, reproducibility)

    summary = {"seed": args.seed, "synthetic_paper_count": int(len(papers)), "citation_link_count": int(len(paper_citations))}
    summary.update(methodology_summary(methodology))
    summary.update(citation_summary(citation_comparison))
    summary.update(checklist_summary(reproducibility, reviewer))
    summary.update(review_summary(quality))
    summary["data_origin"] = "synthetic fictional research papers and citations"
    summary["decision_boundary"] = "review support only; not automatic acceptance, rejection, plagiarism judgment, or misconduct finding"

    papers.to_csv(outputs["results"] / "synthetic_papers.csv", index=False)
    citation_library.to_csv(outputs["results"] / "synthetic_citation_library.csv", index=False)
    paper_citations.to_csv(outputs["results"] / "synthetic_paper_citations.csv", index=False)
    summaries.to_csv(outputs["results"] / "synthetic_paper_summaries.csv", index=False)
    methodology.to_csv(outputs["results"] / "synthetic_methodology_audit.csv", index=False)
    citation_comparison.to_csv(outputs["results"] / "synthetic_citation_comparison.csv", index=False)
    reproducibility.to_csv(outputs["results"] / "synthetic_reproducibility_checklist.csv", index=False)
    reviewer.to_csv(outputs["results"] / "synthetic_reviewer_checklist.csv", index=False)
    quality.to_csv(outputs["results"] / "synthetic_paper_quality_scores.csv", index=False)

    audit_path = outputs["audit"] / "research_review_audit_log.jsonl"
    append_record(audit_path, {**summary, "boundary": "independent synthetic paper review support only"})
    summary["audit_log"] = verify_log(audit_path)
    (outputs["results"] / "synthetic_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    write_report(outputs["reports"] / "synthetic_research_review_report.md", summary, quality, methodology, citation_comparison, reproducibility, reviewer)
    plot_methodology_risk(methodology, outputs["figures"] / "synthetic_methodology_risk.png")
    plot_citation_coverage(citation_comparison, outputs["figures"] / "synthetic_citation_coverage.png")
    plot_reproducibility(reproducibility, outputs["figures"] / "synthetic_reproducibility_readiness.png")
    plot_quality_scores(quality, outputs["figures"] / "synthetic_quality_scores.png")
    plot_review_recommendations(quality, outputs["figures"] / "synthetic_review_recommendations.png")

    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
