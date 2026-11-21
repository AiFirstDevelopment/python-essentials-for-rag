"""The pipeline and the harness with a fake embedder and a fake model: no network, no API key (like a Jest mock)."""
import asyncio
from types import SimpleNamespace

import numpy as np

from evals.harness import load_cases, report, run, score_answer
from rag.pipeline import Index, answer, load

VOCAB = ["return", "refund", "sale", "credit", "ship", "express", "deliver", "photo", "gift"]


class FakeEmbedder:
    def encode(self, texts, normalize_embeddings=True):
        return np.array([[t.lower().count(w) + 0.01 for w in VOCAB] for t in texts])


class FakeClient:
    def __init__(self, reply="Sale items can be returned within 14 days for store credit."):
        self.reply, self.sent = reply, None
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, **request):
        self.sent = request
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=self.reply)])


def test_load_reads_the_text_and_every_pdf_page():
    chunks = load()
    assert {(c.file, c.page) for c in chunks} >= {("returns.txt", 1), ("shipping.pdf", 1), ("shipping.pdf", 2)}


def test_the_prompt_holds_the_passage_and_the_rule():
    index = Index(load(), FakeEmbedder())
    client = FakeClient()
    asyncio.run(answer("Can I get a refund on a sale item?", index.retrieve("Can I get a refund on a sale item?"), client))
    prompt = client.sent["messages"][0]["content"]
    assert "store credit" in prompt
    assert "say you don't know" in client.sent["system"]


def test_score_answer():
    case = {"expected_behavior": "answer", "required_facts": [{"fact": "14 days", "match": ["14 days"]}]}
    assert score_answer(case, "Within 14 days.") == ("pass", [])
    assert score_answer(case, "Within 30 days.") == ("fail", ["14 days"])
    assert score_answer({"expected_behavior": "fallback", "required_facts": []}, "I don't know.") == ("pass", [])


def test_the_harness_runs_the_golden_set_offline():
    results = asyncio.run(run(load_cases(), Index(load(), FakeEmbedder()), FakeClient()))
    assert len(results) == 8
    assert "returns-02" in report(results)
