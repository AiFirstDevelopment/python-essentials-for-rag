"""The reranker: the demo pipeline's rerank, in Python. Claude Haiku reads the fused pool and returns the numbers of
the passages that answer the question, best first. Its choice goes first, then the rest of the pool in fusion order:
it orders the context, it does not cut it. A failed call, or a number outside the pool, falls back to fusion order."""
import anthropic
from pydantic import BaseModel

from rag.chunks import Chunk

RERANK_MODEL = "claude-haiku-5-5"
ANSWER_CHUNKS = 3        # the demo sends 12 of a pool of 48; this corpus is 17 chunks, so 3 of 8
RULES = f"""You choose which passages answer a question about a set of documents.
You are given the question and a numbered list of passages.
Return the numbers of the passages that answer the question, best first, at most {ANSWER_CHUNKS}.
Return an empty list if none answers it."""


class Ranking(BaseModel):          # the reply's shape; the SDK checks the model's JSON against it
    ranked: list[int]


async def rerank(client, question: str, pool: list[Chunk]) -> list[Chunk]:
    if not pool:
        return []
    numbered = "\n\n".join(f"[{i}] {chunk.text}" for i, chunk in enumerate(pool))
    try:
        response = await client.messages.parse(
            model=RERANK_MODEL,
            max_tokens=1024,
            output_config={"effort": "low"},
            system=RULES,
            messages=[{"role": "user", "content": f"Question: {question}\n\nPassages:\n\n{numbered}"}],
            output_format=Ranking,
        )
        ranked = response.parsed_output.ranked
        if any(not 0 <= n < len(pool) for n in ranked):
            raise ValueError(f"the reranker named passages it was not given: {ranked}")
    except (anthropic.APIError, ValueError, AttributeError):
        return pool[:ANSWER_CHUNKS]
    chosen = [pool[n] for n in dict.fromkeys(ranked)]          # dict.fromkeys drops repeats and keeps the order
    rest = [chunk for chunk in pool if chunk not in chosen]
    return (chosen + rest)[:ANSWER_CHUNKS]
