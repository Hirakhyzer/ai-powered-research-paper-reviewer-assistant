# Publication Readiness Plan

This plan describes how the project can evolve from a synthetic reviewer-support prototype into a publication-ready research artifact.

## 1. Possible paper framing

Potential paper title:

> Transparent AI-Assisted Peer Review Support Using Synthetic Manuscripts, Methodology Audits, Citation Coverage Signals, and Audit Logs

Core contribution:

- A modular reviewer-support architecture.
- A synthetic manuscript lab for safe experimentation.
- Transparent rule-based baselines for review-support signals.
- Reproducible outputs and hash-chained audit logging.
- A clear governance boundary that keeps human reviewers responsible for final judgment.

## 2. Candidate research questions

| ID | Question |
|---|---|
| RQ1 | Can structured reviewer-support signals improve review completeness? |
| RQ2 | Which methodology weaknesses are easiest to detect with transparent rules? |
| RQ3 | How sensitive are recommendations to rubric weights? |
| RQ4 | Can audit trails improve trust and reproducibility of AI-assisted review? |
| RQ5 | How do human reviewers perceive usefulness, risk, and cognitive load? |

## 3. Needed experiments

### Synthetic pipeline validation

- Run multiple seeds.
- Vary paper quality profiles.
- Compare output stability.
- Check audit-ledger reproducibility.

### Rubric sensitivity analysis

- Change methodology, citation, and reproducibility weights.
- Compare how paper-quality signals shift.
- Identify unstable or overly dominant rules.

### Human-AI collaboration study

Possible study design:

```text
Group A: reviewers inspect paper summaries manually
Group B: reviewers inspect paper summaries with assistant checklist
Compare: review completeness, time, confidence, cognitive load, perceived usefulness
```

## 4. Figures and tables

Publication-ready artifacts could include:

- System architecture diagram.
- Reviewer-support workflow diagram.
- Methodology risk distribution.
- Citation coverage distribution.
- Reproducibility readiness chart.
- Quality-score distribution.
- Example reviewer checklist.
- Audit-ledger provenance example.

## 5. Validity threats

| Threat | Mitigation |
|---|---|
| Synthetic data may not represent real manuscripts | Add permissioned external validation later |
| Rules may encode incomplete review assumptions | Report rubric version and conduct sensitivity analysis |
| Review-support score may be misread as final quality | Use strong governance boundary and human oversight statement |
| Citation coverage may miss field-specific nuance | Require human literature verification |
| Human-study results may be domain-dependent | Recruit varied reviewers and report participant context |

## 6. Ethical position

The research should argue for assistive, transparent, and auditable AI in peer review—not automated editorial decision-making. The system should be evaluated by how well it supports careful human review, not by whether it can replace reviewers.

## 7. Next engineering steps

- Add configuration files for rubric weights.
- Add repeated-seed experiment script.
- Add ablation study script.
- Add report comparison tool.
- Add optional citation-network visualization.
- Add reviewer user-study templates.
