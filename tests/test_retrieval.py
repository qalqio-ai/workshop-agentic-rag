from agentic_rag.retrieval import ProfileStore


def test_profile_store_reports_available_for_a_usable_client():
    store = ProfileStore(":memory:", in_memory=True)
    try:
        assert store.is_available() is True
    finally:
        store.close()


def test_profile_store_reports_unavailable_after_client_close():
    store = ProfileStore(":memory:", in_memory=True)
    store.close()

    assert store.is_available() is False
