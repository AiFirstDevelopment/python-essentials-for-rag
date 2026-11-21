"""The pipeline and the harness with a fake embedder and a fake model: no network, no API key (like a Jest mock)."""
import asyncio
from types import SimpleNamespace

import numpy as np

from evals.harness import Case, found_sources, load_cases, report, run, score_answer
from rag.pipeline import Index, answer, load
from rag.widen import Passage

VOCAB = ["return", "refund", "sale", "credit", "ship", "express", "deliver", "photo", "gift", "warranty", "point", "down"]


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


def case(behavior="answer", facts=(), sources=()):
    return Case(id="t", category="answerable", question="q", expected_behavior=behavior,
                required_facts=[{"fact": f, "match": [f]} for f in facts], sources=list(sources))


def test_load_reads_every_document_and_every_pdf_page():
    chunks = load()
    files = {c.file for c in chunks}
    assert {"returns.txt", "rewards.md", "shipping.pdf", "gear-care.pdf"} <= files
    assert {c.page for c in chunks if c.file == "gear-care.pdf"} == {1, 2, 3}


def test_retrieval_sends_the_right_document_not_every_document():
    index = Index(load(), FakeEmbedder())
    passages = index.retrieve("Can I get a refund on a sale item?")
    assert any("store credit" in p.text for p in passages)
    assert "gear-care.pdf" not in {p.file for p in passages}


def test_the_prompt_holds_the_passages_and_the_rule():
    client = FakeClient()
    asyncio.run(answer("q", [Passage("returns.txt", 1, 1, "Sale items: store credit.")], client))
    assert "Sale items: store credit." in client.sent["messages"][0]["content"]
    assert "say you don't know" in client.sent["system"]


def test_found_sources_reads_page_ranges_and_files():
    widened = [Passage("gear-care.pdf", 1, 3, "...")]
    assert found_sources(case(sources=[{"file": "gear-care.pdf", "page": 2}]), widened) is True
    assert found_sources(case(sources=[{"file": "returns.txt", "page": 2}]), widened) is False
    assert found_sources(case(), widened) is None


def test_score_answer():
    assert score_answer(case(facts=["14 days"]), "Within 14 days.") == ("pass", [])
    assert score_answer(case(facts=["14 days"]), "Within 30 days.") == ("fail", ["14 days"])
    assert score_answer(case(facts=["14 days"]), "I don't know, 14 days?") == ("fail", [])
    assert score_answer(case("fallback"), "I don't know.") == ("pass", [])
    assert score_answer(case("fallback"), "We open at 9.") == ("review", [])


def test_the_harness_runs_the_golden_set_offline():
    cases = load_cases()
    results = asyncio.run(run(cases, Index(load(), FakeEmbedder()), FakeClient()))
    assert len(results) == len(cases) == 19
    assert "answers" in report(results)
    assert "answers" not in report(asyncio.run(run(cases, Index(load(), FakeEmbedder()))))
