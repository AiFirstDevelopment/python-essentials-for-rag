import asyncio
from types import SimpleNamespace

import anthropic

from rag.chunks import Chunk
from rag.rerank import rerank

POOL = [Chunk("f.txt", 1, i, f"passage {i}") for i in range(6)]


class Reranker:
    def __init__(self, ranked=None, error=None):
        self.ranked, self.error = ranked, error
        self.messages = SimpleNamespace(parse=self.parse)

    async def parse(self, **request):
        if self.error:
            raise self.error
        return SimpleNamespace(parsed_output=SimpleNamespace(ranked=self.ranked))


def run(client):
    return asyncio.run(rerank(client, "q", POOL))


def test_its_choice_goes_first_then_the_pool_in_fusion_order():
    assert run(Reranker([4])) == [POOL[4], POOL[0], POOL[1]]


def test_repeats_count_once():
    assert run(Reranker([2, 2, 5])) == [POOL[2], POOL[5], POOL[0]]


def test_a_number_outside_the_pool_falls_back_to_fusion_order():
    assert run(Reranker([1, 9])) == POOL[:3]


def test_a_failed_call_falls_back_to_fusion_order():
    error = anthropic.APIConnectionError(request=SimpleNamespace(method="POST", url="x"))
    assert run(Reranker(error=error)) == POOL[:3]


def test_an_empty_pool_gives_nothing():
    assert asyncio.run(rerank(Reranker([0]), "q", [])) == []
