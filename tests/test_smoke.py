from diff_risk_dashboard.core import summarize_apv_json


def test_summary_counts(tmp_path):
    sample = tmp_path / "s.json"
    sample.write_text(
        '[{"predicted_risk":"high"},{"predicted_risk":"medium"},{"predicted_risk":"low"}]',
        encoding="utf-8",
    )
    s = summarize_apv_json(str(sample))
    assert s["total"] == 3
    assert s["by_severity"]["high"] == 1
    assert s["by_severity"]["medium"] == 1
    assert s["by_severity"]["low"] == 1
