"""Configuration and output-directory helpers."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import yaml


def set_seed(seed: int) -> None:
    """Set deterministic seeds for the synthetic experiment."""
    random.seed(seed)
    np.random.seed(seed)


def ensure_output_dirs(root: str | Path = "outputs") -> dict[str, Path]:
    """Create output folders and return useful paths."""
    root = Path(root)
    paths = {
        "root": root,
        "results": root / "results",
        "figures": root / "figures",
        "reports": root / "reports",
        "audit": root / "audit",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def load_yaml(path: str | Path) -> dict:
    """Load a YAML file. Empty files return an empty dictionary."""
    path = Path(path)
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
