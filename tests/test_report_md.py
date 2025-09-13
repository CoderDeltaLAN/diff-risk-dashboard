from diff_risk_dashboard.report import to_markdown


def test_md_contains_table_and_total():
    s = {
        "total": 3,
        "worst": "HIGH",
        "risk": "yellow",
        "by_severity": {"HIGH": 1, "MEDIUM": 1, "LOW": 1},
    }
    md = to_markdown(s)
    assert "# Diff Risk Dashboard" in md
    assert "| **TOTAL** | **3** |" in md
