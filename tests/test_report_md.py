from diff_risk_dashboard.report import to_markdown


def test_md_total():
    md = to_markdown(
        {
            "total": 3,
            "worst": "HIGH",
            "risk": "yellow",
            "by_severity": {"HIGH": 1, "MEDIUM": 1, "LOW": 1},
        }
    )
    assert "| **TOTAL** | **3** |" in md
