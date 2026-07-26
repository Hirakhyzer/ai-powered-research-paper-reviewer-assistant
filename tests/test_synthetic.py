from paperreview.synthetic import SyntheticPaperConfig, generate_synthetic_review_data


def test_synthetic_generator_shapes():
    data = generate_synthetic_review_data(SyntheticPaperConfig(papers=12, seed=3))
    assert set(data) == {"papers", "citation_library", "paper_citations"}
    assert len(data["papers"]) == 12
    assert not data["citation_library"].empty
    assert not data["paper_citations"].empty
    assert data["papers"]["paper_id"].is_unique


def test_synthetic_papers_have_required_columns():
    papers = generate_synthetic_review_data(SyntheticPaperConfig(papers=4, seed=4))["papers"]
    required = {"paper_id", "title", "abstract", "methodology", "baseline_count", "evaluation_metric_count", "claim_strength", "evidence_strength"}
    assert required.issubset(set(papers.columns))
