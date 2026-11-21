"""Each chosen chunk joined with the chunk before and after it in the same file: the demo pipeline's widen, in Python.
A chunk is cut at a sentence end, so a rule and its exception are often split across two chunks."""
from dataclasses import dataclass

from rag.chunks import Chunk

WIDEN_CHARS = 10_800


@dataclass
class Passage:
    file: str
    first_page: int
    last_page: int
    text: str


def widen(given: list[Chunk], everything: list[Chunk]) -> list[Passage]:
    at = {(c.file, c.seq): c for c in everything}
    taken, added = {id(c) for c in given}, 0
    for chunk in given:                                   # best first, so the best chunks get their neighbours first
        for seq in (chunk.seq - 1, chunk.seq + 1):
            n = at.get((chunk.file, seq))
            if n is None or id(n) in taken or added + len(n.text) > WIDEN_CHARS:
                continue
            taken.add(id(n))
            added += len(n.text)
    passages, placed = [], set()
    for chunk in given:
        if id(chunk) in placed:                           # already inside an earlier chunk's passage
            continue
        lo = hi = chunk.seq
        while (c := at.get((chunk.file, lo - 1))) and id(c) in taken:
            lo -= 1
        while (c := at.get((chunk.file, hi + 1))) and id(c) in taken:
            hi += 1
        run = [at[(chunk.file, s)] for s in range(lo, hi + 1)]
        placed.update(id(c) for c in run)
        passages.append(Passage(chunk.file, run[0].page, run[-1].page, "\n".join(c.text for c in run)))
    return passages
