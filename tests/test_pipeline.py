"""The pipeline with a fake embedder and a fake model: no network, no API key (like a Jest mock)."""
import asyncio
from types import SimpleNamespace

import numpy as np

from rag.pipeline import answer, load_chunks

WORDS = ["return", "refund", "shipping", "express"]


class FakeEmbedder:
    def encode(self, texts, normalize_embeddings=True):
        return np.array([[t.lower().count(w) + 0.01 for w in WORDS] for t in texts])


class FakeClient:
    def __init__(self):
        self.sent = None
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        self.sent = request
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="30 days.")])


def test_loads_the_text_and_the_pdf():
    text = " ".join(load_chunks())
    assert "30 days of delivery" in text
    assert "Express shipping" in text


def test_answer_sends_the_most_relevant_chunks():
    client = FakeClient()
    chunks = ["Shipping is free over $75.", "Returns within 30 days get a full refund.", "Express costs $19.95."]
    reply = asyncio.run(answer("How do I return an item for a refund?", chunks, FakeEmbedder(), client))
    assert reply == "30 days."
    prompt = client.sent["messages"][0]["content"]
    assert prompt.index("Returns within 30 days") < prompt.index("Question:")
    assert "say you don't know" in client.sent["system"]
