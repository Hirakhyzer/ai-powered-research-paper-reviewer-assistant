import json
import subprocess
import sys
from pathlib import Path


def test_pipeline_smoke(tmp_path):
    output_dir = tmp_path / "outputs"
    result = subprocess.run(
        [sys.executable, "scripts/run_synthetic_review_lab.py", "--papers", "8", "--seed", "11", "--output-dir", str(output_dir)],
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(result.stdout)
    assert summary["synthetic_paper_count"] == 8
    assert (output_dir / "results" / "synthetic_review_summary.json").exists()
    assert (output_dir / "reports" / "synthetic_research_review_report.md").exists()
    assert (output_dir / "audit" / "research_review_audit_log.jsonl").exists()
    assert (output_dir / "figures" / "synthetic_quality_scores.png").exists()
