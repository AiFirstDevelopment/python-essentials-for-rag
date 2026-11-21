"""Chapter 11: the eval harness. Runs every case of the golden set through the pipeline and scores it.
    uv run python -m evals.harness --retrieval-only   # free: scores retrieval, never calls the model
    uv run python -m evals.harness                    # scores the answers too (calls Claude, costs money)"""
import asyncio
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from rag.widen import Passage

GOLDEN = Path(__file__).resolve().parent / "golden.jsonl"
FALLBACK = ("don't know", "do not know", "not in the passages", "doesn't say", "does not say")


@dataclass
class Result:
    id: str
    retrieved: bool                 # every expected source is inside a passage
    status: str = "not run"         # pass, fail or review
    missing: list[str] = field(default_factory=list)


def load_cases(path: Path = GOLDEN) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def found_sources(case: dict, passages: list[Passage]) -> bool:
    return all(any(p.file == s["file"] and p.first_page <= s["page"] <= p.last_page for p in passages)
               for s in case["sources"])


def score_answer(case: dict, reply: str) -> tuple[str, list[str]]:
    text = reply.lower()
    fell_back = any(phrase in text for phrase in FALLBACK)
    if case["expected_behavior"] == "fallback":
        return ("pass" if fell_back else "review"), []
    missing = [f["fact"] for f in case["required_facts"] if not any(m.lower() in text for m in f["match"])]
    return ("pass" if not missing and not fell_back else "fail"), missing


async def run(cases: list[dict], index, client=None) -> list[Result]:
    from rag.pipeline import answer
    results = []
    for case in cases:
        passages = index.retrieve(case["question"])
        result = Result(case["id"], found_sources(case, passages))
        if client is not None:
            result.status, result.missing = score_answer(case, await answer(case["question"], passages, client))
        results.append(result)
    return results


def report(results: list[Result]) -> str:
    lines = [f"{r.id:<12} retrieved={'yes' if r.retrieved else 'NO ':<4} {r.status:<8} {', '.join(r.missing)}"
             for r in results]
    hits = sum(r.retrieved for r in results)
    passed = sum(r.status == "pass" for r in results)
    lines.append(f"retrieval {hits}/{len(results)}   answers {passed}/{len(results)} passed")
    return "\n".join(lines)


async def main():
    from anthropic import AsyncAnthropic
    from rag.pipeline import Index, embedder, load
    client = None if "--retrieval-only" in sys.argv else AsyncAnthropic()
    print(report(await run(load_cases(), Index(load(), embedder()), client)))


if __name__ == "__main__":
    asyncio.run(main())
