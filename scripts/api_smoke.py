#!/usr/bin/env python3
"""Black-box smoke checks against a running local container."""
import json
import os
import time
import urllib.error
import urllib.request

base = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


def request(path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        base + path,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req, timeout=4) as response:
        return response.status, json.loads(response.read())


for _attempt in range(40):
    try:
        status, body = request("/health")
        if status == 200 and body.get("status") == "ok":
            break
    except (OSError, urllib.error.URLError):
        time.sleep(1)
else:
    raise SystemExit("API container did not become healthy within 40 seconds")

status, profiles = request("/v1/use-cases")
assert status == 200 and len(profiles) == 3
request(
    "/v1/documents",
    {
        "use_case_id": "workshop-knowledge",
        "source_id": "smoke-guide",
        "title": "Smoke Guide",
        "text": "Run the API container with Docker Compose for the workshop demo.",
    },
)
status, answer = request(
    "/v1/query",
    {
        "use_case_id": "workshop-knowledge",
        "question": "How do I run the API container with Docker?",
    },
)
assert status == 200 and answer["evidence_status"] == "grounded" and answer["citations"]
print("Docker API smoke checks passed: health, profiles, ingestion, grounded query, citation.")
