from diff_risk_dashboard.core import summarize

def test_summarize_counts_and_worst():
    data = {"findings":[
        {"severity":"LOW"},{"severity":"MEDIUM"},{"severity":"HIGH"},{"severity":"INFO"}
    ]}
    s = summarize(data)
    assert s["total"] == 4
    assert s["by_severity"]["HIGH"] == 1
    assert s["worst"] == "HIGH"
    assert s["risk_level"] == "red"
