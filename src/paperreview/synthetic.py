"""Synthetic research-paper corpus generator.

All records are fictional and intended for reviewer-support research only.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

FIELDS = ["artificial_intelligence", "wireless_networks", "digital_health", "privacy_engineering", "education_technology"]
METHODS = ["controlled experiment", "simulation study", "observational analysis", "benchmark comparison", "case study"]
DATASETS = ["SyntheticBench", "OpenProxySet", "CampusSim", "MedTextToy", "MobilityGrid", "EduTrace"]


@dataclass(frozen=True)
class SyntheticPaperConfig:
    """Configuration for the synthetic paper generator."""
    papers: int = 36
    seed: int = 42


def generate_synthetic_review_data(config: SyntheticPaperConfig) -> dict[str, pd.DataFrame]:
    """Generate fictional papers, citation library, and paper-citation links."""
    rng = np.random.default_rng(config.seed)
    citation_library = _citation_library(rng)
    paper_rows = []
    citation_rows = []

    for idx in range(config.papers):
        paper_id = f"P{idx + 1:04d}"
        field = str(rng.choice(FIELDS))
        method = str(rng.choice(METHODS, p=[0.24, 0.25, 0.18, 0.23, 0.10]))
        dataset = str(rng.choice(DATASETS))
        dataset_size = int(rng.integers(80, 6000))
        metric_count = int(rng.integers(1, 6))
        baseline_count = int(rng.integers(0, 6))
        ablation_count = int(rng.integers(0, 4))
        limitation_quality = float(np.round(rng.uniform(0.15, 0.95), 3))
        code_available = bool(rng.random() > 0.42)
        data_available = bool(rng.random() > 0.38)
        preregistered = bool(rng.random() > 0.82)
        claim_strength = float(np.round(rng.uniform(0.25, 0.98), 3))
        novelty_signal = float(np.round(rng.uniform(0.2, 0.95), 3))
        evidence_strength = float(np.round(np.clip(0.15 + 0.13 * baseline_count + 0.11 * metric_count + 0.07 * ablation_count + rng.normal(0, 0.12), 0, 1), 3))
        title = _title(field, idx)
        problem = _problem(field)
        contribution = _contribution(field, method)
        weakness_phrase = _weakness_phrase(baseline_count, metric_count, dataset_size, ablation_count)
        abstract = f"This paper studies {problem}. It proposes {contribution} using a {method} on {dataset}. The study reports {metric_count} evaluation metrics and {baseline_count} baselines."
        methodology = f"The method uses {method}, dataset {dataset}, {dataset_size} samples, {metric_count} metrics, {baseline_count} baselines, and {ablation_count} ablations. {weakness_phrase}"
        experiments = f"Experiments compare service quality, robustness, and error trends with evidence strength {evidence_strength:.2f}."
        limitations = _limitations(limitation_quality, data_available, code_available)
        related_work = f"The related work discusses prior {field.replace('_', ' ')} approaches and adjacent evaluation settings."
        paper_rows.append({
            "paper_id": paper_id,
            "title": title,
            "field": field,
            "year": int(rng.integers(2020, 2027)),
            "venue_type": str(rng.choice(["conference", "journal", "workshop", "preprint"])),
            "abstract": abstract,
            "research_problem": problem,
            "claimed_contribution": contribution,
            "method_family": method,
            "dataset_name": dataset,
            "dataset_size": dataset_size,
            "evaluation_metric_count": metric_count,
            "baseline_count": baseline_count,
            "ablation_count": ablation_count,
            "code_available": code_available,
            "data_available": data_available,
            "preregistered": preregistered,
            "claim_strength": claim_strength,
            "novelty_signal": novelty_signal,
            "evidence_strength": evidence_strength,
            "methodology": methodology,
            "experiments": experiments,
            "related_work": related_work,
            "limitations": limitations,
            "conclusion": f"The paper concludes that the proposed approach can improve {problem}, subject to validation limits.",
        })

        library_matches = citation_library[citation_library["field"].eq(field)]
        chosen = library_matches.sample(n=int(rng.integers(3, min(9, len(library_matches)) + 1)), random_state=int(rng.integers(0, 100000)))
        for _, citation in chosen.iterrows():
            citation_rows.append({
                "paper_id": paper_id,
                "citation_id": citation["citation_id"],
                "citation_role": str(rng.choice(["background", "method", "dataset", "baseline", "evaluation"])),
                "alignment_score": float(np.round(rng.uniform(0.35, 0.98), 3)),
            })

    return {
        "papers": pd.DataFrame(paper_rows),
        "citation_library": citation_library,
        "paper_citations": pd.DataFrame(citation_rows),
    }


def _citation_library(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    evidence_types = ["theory", "benchmark", "survey", "dataset", "system", "evaluation"]
    for field in FIELDS:
        for idx in range(14):
            rows.append({
                "citation_id": f"C-{field[:3].upper()}-{idx + 1:02d}",
                "field": field,
                "title": f"Synthetic reference {idx + 1} for {field.replace('_', ' ')}",
                "year": int(rng.integers(2014, 2027)),
                "method_family": str(rng.choice(METHODS)),
                "evidence_type": str(rng.choice(evidence_types)),
            })
    return pd.DataFrame(rows)


def _title(field: str, idx: int) -> str:
    return f"A Synthetic Study of {field.replace('_', ' ').title()} Review Patterns {idx + 1}"


def _problem(field: str) -> str:
    mapping = {
        "artificial_intelligence": "robust model evaluation under distribution shift",
        "wireless_networks": "adaptive network performance under mobility",
        "digital_health": "safe decision support for clinical text workflows",
        "privacy_engineering": "privacy risk detection in data-processing pipelines",
        "education_technology": "student support prediction under fairness constraints",
    }
    return mapping[field]


def _contribution(field: str, method: str) -> str:
    return f"an interpretable {field.replace('_', ' ')} framework evaluated through {method}"


def _weakness_phrase(baselines: int, metrics: int, dataset_size: int, ablations: int) -> str:
    weaknesses = []
    if baselines < 2:
        weaknesses.append("The baseline comparison is limited")
    if metrics < 2:
        weaknesses.append("The evaluation uses few metrics")
    if dataset_size < 500:
        weaknesses.append("The dataset is small")
    if ablations == 0:
        weaknesses.append("No ablation study is reported")
    return "; ".join(weaknesses) + "." if weaknesses else "The design includes multiple checks and comparison points."


def _limitations(quality: float, data_available: bool, code_available: bool) -> str:
    if quality < 0.35:
        return "Limitations are briefly mentioned but external validity, failure cases, and deployment constraints remain vague."
    parts = ["The paper discusses external validity, failure cases, and evaluation scope."]
    if not data_available:
        parts.append("Dataset release constraints are noted.")
    if not code_available:
        parts.append("Code release is not yet available.")
    return " ".join(parts)
