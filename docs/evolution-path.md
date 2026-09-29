# Repository evolution path

1. **Apply the Agentic RAG starter.** The API, tests, Docker files, sample profiles, and local/remote CI are the current work.
2. **Verify the gates.** Require local Python CI to pass, GitHub Actions to pass on a pull request, a Docker image build, and black-box API smoke tests against the container.
3. **Add Superpowers later through a separate PRD.** Do not install it during the current baseline work. Keep GitHub Spec Kit artifacts authoritative for product requirements; use Superpowers as the implementation and verification discipline only after its scope and cross-agent invocation are agreed.

The Superpowers PRD should be authored only after the Agentic RAG starter has been applied and its CI/API gates have passed.
