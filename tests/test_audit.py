from paperreview.audit import append_record, verify_log


def test_hash_chained_audit_log(tmp_path):
    path = tmp_path / "audit.jsonl"
    append_record(path, {"run": 1, "boundary": "synthetic"})
    append_record(path, {"run": 2, "boundary": "synthetic"})
    result = verify_log(path)
    assert result["valid"] is True
    assert result["record_count"] == 2
