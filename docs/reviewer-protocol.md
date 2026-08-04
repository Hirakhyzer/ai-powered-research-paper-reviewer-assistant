# Reviewer Protocol

This document defines a structured protocol for using the AI-Powered Research Paper Reviewer Assistant as a reviewer-support research tool.

## 1. Purpose

The system is designed to support—not replace—human scholarly review. It can help organize review attention around summaries, methodology risks, citation coverage, reproducibility readiness, and reviewer action items.

The output should be treated as a set of **review-support signals** rather than a decision.

## 2. Recommended workflow

```text
Generate or load paper records
→ Parse paper sections
→ Produce structured summaries
→ Audit methodology and claims
→ Compare citation coverage
→ Build reproducibility checklist
→ Generate human-review prompts
→ Export report and audit ledger
→ Human reviewer verifies evidence manually
```

## 3. Reviewer-support stages

| Stage | Output | Human verification required |
|---|---|---|
| Summary | Topic, contribution, research question, limitation | Confirm against the manuscript text |
| Methodology audit | Risk flags and method-quality indicators | Inspect experimental design and baselines |
| Citation comparison | Coverage and related-work gap signals | Check field-specific literature manually |
| Reproducibility checklist | Code, data, metrics, seed, artifact readiness | Verify artifacts and repository links |
| Reviewer checklist | Suggested questions and action items | Decide relevance and priority |
| Audit logging | Run metadata and hash-chain ledger | Preserve provenance if used in a study |

## 4. Review boundary

The tool should not be used to:

- Automatically accept or reject papers.
- Accuse authors of plagiarism or misconduct.
- Rank authors, institutions, or journals.
- Replace editorial policy or reviewer expertise.
- Make funding, hiring, grading, or promotion decisions.

## 5. Reporting template

When reporting results from the tool, include:

- Dataset type: synthetic or real-permissioned manuscript set.
- Number of papers.
- Random seed.
- Review rubric version.
- Rules or models used.
- Known limitations.
- Human verification process.
- Whether the outputs were used for research, teaching, or prototype demonstration.

## 6. Quality checklist

Before using outputs in any academic setting, verify:

- The summary accurately reflects the paper.
- No unsupported claims are introduced.
- Citations are checked against actual references.
- Weakness flags are explained and not treated as accusations.
- The final review remains authored and owned by a human expert.
