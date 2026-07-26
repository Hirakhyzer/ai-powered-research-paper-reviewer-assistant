# Methodology

This project is a synthetic-first reviewer-support lab. It creates fictional research papers with structured abstracts, claimed contributions, methodology descriptions, experiments, related-work summaries, limitations, and citation links.

The pipeline has five stages:

1. Generate synthetic papers and citation links.
2. Produce transparent summaries and research-question prompts.
3. Audit methodology risk using explicit review heuristics.
4. Compare citation breadth, evidence diversity, recency, and alignment.
5. Generate reproducibility and reviewer checklists with a non-decisive quality-support score.

The methodology audit checks limited baselines, narrow metrics, small datasets, missing ablations, claim-evidence mismatch, weak limitation discussion, and missing artifacts. These checks are deliberately transparent so that reviewers can inspect the rationale rather than trust an opaque decision.

The quality score is a review-support signal only. It combines methodology risk, citation coverage, and reproducibility readiness. It must not be interpreted as acceptance, rejection, plagiarism judgment, or research quality certification.
