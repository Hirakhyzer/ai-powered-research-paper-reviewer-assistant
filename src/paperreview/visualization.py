"""Plotting helpers for local synthetic reviewer outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _save(fig, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_methodology_risk(audit: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts = audit["methodology_risk_class"].value_counts().reindex(["low", "medium", "high", "critical"]).fillna(0)
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Methodology risk classes")
    ax.set_xlabel("Risk class")
    ax.set_ylabel("Paper count")
    _save(fig, path)


def plot_citation_coverage(comparison: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    comparison["citation_coverage_score"].plot(kind="hist", bins=10, ax=ax)
    ax.set_title("Citation coverage score distribution")
    ax.set_xlabel("Coverage score")
    _save(fig, path)


def plot_reproducibility(reproducibility: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    reproducibility["reproducibility_readiness_score"].plot(kind="hist", bins=10, ax=ax)
    ax.set_title("Reproducibility readiness distribution")
    ax.set_xlabel("Readiness score")
    _save(fig, path)


def plot_quality_scores(quality: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    quality["paper_quality_support_score"].plot(kind="hist", bins=10, ax=ax)
    ax.set_title("Paper quality support scores")
    ax.set_xlabel("Support score")
    _save(fig, path)


def plot_review_recommendations(quality: pd.DataFrame, path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    quality["review_recommendation"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Human review recommendations")
    ax.set_xlabel("Recommendation")
    ax.set_ylabel("Paper count")
    ax.tick_params(axis="x", rotation=25)
    _save(fig, path)
