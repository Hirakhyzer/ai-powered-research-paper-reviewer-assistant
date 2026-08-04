# Contributing

Thank you for considering a contribution to the AI-Powered Research Paper Reviewer Assistant.

## Project direction

This repository focuses on transparent, auditable reviewer-support workflows. Contributions should preserve the core boundary: the project assists human reviewers but does not automate peer-review decisions.

## Useful contribution areas

- Improve synthetic paper generation.
- Add more transparent methodology audit rules.
- Improve citation coverage features.
- Add reproducibility checklist items.
- Add tests for reviewer-support modules.
- Improve figures and reporting.
- Add documentation for ethical and academic boundaries.
- Add experiment scripts for repeated-seed studies.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q tests
```

## Contribution standards

Please keep contributions:

- Reproducible.
- Transparent.
- Well documented.
- Covered by tests where practical.
- Clear about limitations.
- Consistent with the human-in-the-loop peer-review boundary.

## Pull request checklist

Before opening a pull request, check:

- [ ] Tests pass locally.
- [ ] Documentation is updated if behavior changes.
- [ ] New outputs do not claim automatic acceptance or rejection authority.
- [ ] Synthetic data remains the default unless a safe, permissioned dataset is clearly documented.
- [ ] Any new review-support score is explained as non-decisive.

## Responsible research note

Do not add functionality that encourages automated paper rejection, misconduct accusation, author ranking, or confidential manuscript processing without safeguards.
