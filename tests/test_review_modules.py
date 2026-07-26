from paperreview.checklist import build_reproducibility_checklist, build_reviewer_checklist
from paperreview.citations import compare_citations
from paperreview.methodology import audit_methodology
from paperreview.scoring import score_paper_quality
from paperreview.summarizer import summarize_papers
from paperreview.synthetic import SyntheticPaperConfig, generate_synthetic_review_data


def _data():
    return generate_synthetic_review_data(SyntheticPaperConfig(papers=10, seed=9))


def test_review_modules_return_expected_rows():
    data = _data()
    papers = data["papers"]
    summaries = summarize_papers(papers)
    methodology = audit_methodology(papers)
    citations = compare_citations(papers, data["citation_library"], data["paper_citations"])
    reproducibility = build_reproducibility_checklist(papers, methodology)
    reviewer = build_reviewer_checklist(summaries, methodology, citations, reproducibility)
    quality = score_paper_quality(methodology, citations, reproducibility)

    assert len(summaries) == len(papers)
    assert len(methodology) == len(papers)
    assert len(citations) == len(papers)
    assert len(reproducibility) == len(papers)
    assert len(reviewer) == len(papers)
    assert len(quality) == len(papers)
    assert quality["paper_quality_support_score"].between(0, 1).all()


def test_methodology_audit_flags_reviewable_weaknesses():
    papers = _data()["papers"]
    audit = audit_methodology(papers)
    assert "methodology_risk_score" in audit.columns
    assert audit["methodology_risk_score"].between(0, 1).all()
    assert audit["methodology_risk_class"].isin(["low", "medium", "high", "critical"]).all()
