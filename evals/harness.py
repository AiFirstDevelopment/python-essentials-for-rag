"""Chapter 11: the eval harness. Runs every case of the golden set through the pipeline and scores it.
    uv run python -m evals.harness --retrieval-only   # free: scores the fused search, no model call, no reranker
    uv run python -m evals.harness                    # reranks, answers and scores both (calls Claude, costs money)
A fallback case passes when the reply says it doesn't know; an answer case passes when it holds every required fact."""
import asyncio
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from rag.widen import Passage

GOLDEN = Path(__file__).resolve().parent / "golden.jsonl"
FALLBACK = ("don't know", "do not know", "not in the passages", "doesn't say", "does not say")


class Fact(BaseModel):
    fact: str
    match: list[str]


class Source(BaseModel):
    file: str
    page: int


class Case(BaseModel):                 # a typo in golden.jsonl fails loudly here, not silently in a score
    id: str
    category: Literal["answerable", "inferred", "absent"]
    question: str
    expected_behavior: Literal["answer", "fallback"]
    required_facts: list[Fact]
    sources: list[Source]


@dataclass
class Result:
    id: str
    retrieved: bool | None             # every expected source inside a passage; None when the case has no source
    status: str = "not run"            # pass, fail, or review (a person reads it)
    missing: list[str] = field(default_factory=list)


def load_cases(path: Path = GOLDEN) -> list[Case]:
    return [Case.model_validate_json(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def found_sources(case: Case, passages: list[Passage]) -> bool | None:
    if not case.sources:
        return None
    return all(any(p.file == s.file and p.first_page <= s.page <= p.last_page for p in passages) for s in case.sources)


def score_answer(case: Case, reply: str) -> tuple[str, list[str]]:
    text = reply.lower()
    fell_back = any(phrase in text for phrase in FALLBACK)
    if case.expected_behavior == "fallback":
        return ("pass" if fell_back else "review"), []
    missing = [f.fact for f in case.required_facts if not any(m.lower() in text for m in f.match)]
    return ("fail" if missing else "pass"), missing      # a right answer with a caveat still passes


async def run(cases: list[Case], index, client=None) -> list[Result]:
    from rag.pipeline import answer

    async def one(case: Case) -> Result:
        passages = await index.retrieve(case.question, client)
        result = Result(case.id, found_sources(case, passages))
        if client is not None:
            result.status, result.missing = score_answer(case, await answer(case.question, passages, client))
        return result

    return await asyncio.gather(*(one(case) for case in cases))      # every case at the same time, results in order


def report(results: list[Result]) -> str:
    mark = {True: "yes", False: "NO", None: "-"}
    lines = [f"{r.id:<12} retrieved {mark[r.retrieved]:<4} {r.status:<8} {', '.join(r.missing)}" for r in results]
    with_source = [r for r in results if r.retrieved is not None]
    summary = f"retrieval {sum(r.retrieved for r in with_source)}/{len(with_source)}"
    if any(r.status != "not run" for r in results):
        summary += f"   answers {sum(r.status == 'pass' for r in results)}/{len(results)} passed"
    return "\n".join(lines + [summary])


async def main():
    from anthropic import AsyncAnthropic
    from rag.pipeline import Index, embedder, load
    client = None if "--retrieval-only" in sys.argv else AsyncAnthropic()
    print(report(await run(load_cases(), Index(load(), embedder()), client)))


if __name__ == "__main__":
    asyncio.run(main())
