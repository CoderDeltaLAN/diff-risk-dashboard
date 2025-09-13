from __future__ import annotations
from typing import Dict, Any
import json
from collections import Counter

def summarize_apv_json(path: str) -> Dict[str, Any]:
    '''
    Expect a JSON array or object containing findings with a 'predicted_risk'
    field in {'low','medium','high'} (interface compatible with ai-patch-verifier output).
    '''
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data if isinstance(data, list) else data.get("findings", [])
    risks = [str(i.get("predicted_risk", "")).lower() for i in items]
    counts = Counter(risks)
    total = sum(counts.values())
    return {
        "total": total,
        "by_severity": {
            "high": counts.get("high", 0),
            "medium": counts.get("medium", 0),
            "low": counts.get("low", 0),
        },
    }
