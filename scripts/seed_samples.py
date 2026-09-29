#!/usr/bin/env python3
"""Ingest the three fictional starter documents into a running API."""
import json
from pathlib import Path
from urllib.request import Request, urlopen

SAMPLES = [
    ("workshop-knowledge", "workshop-quickstart", "Workshop Quickstart", "workshop-quickstart.md"),
    ("policy-handbook", "sample-travel-policy", "Fictional Travel Policy", "policy-handbook.md"),
    (
        "technical-troubleshooting",
        "sample-retrieval-troubleshooting",
        "Fictional Retrieval Troubleshooting Guide",
        "technical-troubleshooting.md",
    ),
]

for use_case_id, source_id, title, filename in SAMPLES:
    text = Path("sample_data", filename).read_text(encoding="utf-8")
    text = text.split("---", 2)[-1].strip()
    request = Request(
        "http://127.0.0.1:8000/v1/documents",
        data=json.dumps(
            {"use_case_id": use_case_id, "source_id": source_id, "title": title, "text": text}
        ).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=10) as response:
        print(response.read().decode())
