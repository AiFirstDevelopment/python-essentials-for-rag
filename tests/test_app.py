"""The web app with a fake index and a fake model: no network, no API key."""
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app, state
from rag.widen import Passage


class FakeIndex:
    async def retrieve(self, question, client=None):
        return [Passage("returns.txt", 1, 1, "Sale items: store credit within 14 days.")]


class FakeClient:
    def __init__(self):
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="Store credit, within 14 days.")])


def test_the_page_is_served():
    response = TestClient(app).get("/")
    assert response.status_code == 200 and "Ask the store policies" in response.text


def test_ask_answers_with_its_sources():
    state.update(index=FakeIndex(), client=FakeClient())
    response = TestClient(app).post("/ask", json={"question": "Can I return a sale item?"})
    assert response.json() == {"answer": "Store credit, within 14 days.", "sources": ["returns.txt, page 1"]}


def test_a_question_is_required():
    assert TestClient(app).post("/ask", json={}).status_code == 422
