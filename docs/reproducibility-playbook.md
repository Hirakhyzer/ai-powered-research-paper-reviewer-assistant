# Reproducibility Playbook

This playbook defines how to run and report experiments from the AI-Powered Research Paper Reviewer Assistant so that another researcher can inspect the workflow.

## 1. Minimum run record

Each run should record:

| Field | Example |
|---|---|
| Run name | `synthetic_review_seed_42` |
| Number of papers | `36` |
| Random seed | `42` |
| Dataset type | synthetic fictional papers |
| Rubric version | methodology/citation/reproducibility rules in repository commit |
| Output directory | `outputs/` |
| Commit hash | current repository commit |
| Reviewer boundary | human expert required for final judgment |

## 2. Recommended command

```bash
python scripts/run_synthetic_review_lab.py --papers 36 --seed 42
```

For CI or quick smoke testing:

```bash
python scripts/run_synthetic_review_lab.py --papers 16 --seed 7 --output-dir outputs_ci
```

## 3. Outputs to preserve

Preserve the following when reporting a run:

```text
synthetic_papers.csv
synthetic_paper_summaries.csv
synthetic_methodology_audit.csv
synthetic_citation_comparison.csv
synthetic_reproducibility_checklist.csv
synthetic_reviewer_checklist.csv
synthetic_paper_quality_scores.csv
synthetic_review_summary.json
synthetic_research_review_report.md
research_review_audit_log.jsonl
```

## 4. Audit-ledger check

The hash-chained audit ledger should be treated as provenance evidence for the run. It does not prove academic correctness, but it helps track whether outputs correspond to a specific execution.

## 5. Evaluation design

For research studies, compare:

- Different rubric weights.
- Different synthetic paper difficulty levels.
- Different reviewer-support rules.
- Human-only vs assistant-supported review workflows.
- Reviewer confidence before and after assistant output.

## 6. Reporting limitations

Always report:

- Synthetic data limitations.
- Rule-based baseline limitations.
- Absence of final peer-review authority.
- Need for real human expert verification.
- Any missing external validation.

## 7. Publication checklist

Before using this work in a paper or proposal, include:

- Research question.
- Dataset generation description.
- Full configuration.
- Code version or commit hash.
- Output tables and figures.
- Ethical boundary statement.
- Human-review verification procedure.
