# Use-Case Detail Endpoint

`GET /v1/use-cases/{use_case_id}` returns the ID, name, and description
for a configured use case. An unknown ID returns HTTP 404 with
`{"detail":{"code":"unknown_use_case"}}`.