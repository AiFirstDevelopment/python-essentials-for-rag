"""Keyword search (BM25), vector search, and reciprocal rank fusion: the demo pipeline's retrieval, in Python."""
import math
import re
from collections import Counter

import numpy as np

from rag.chunks import Chunk

RRF_K = 60
STOP = set("a an and are as at be by can could do does for from how i if in is it its me my of on or should so that "
           "the their them there this to was what when where which who why will with would you your".split())


def words(text: str) -> list[str]:
    """Lower-cased runs of letters and digits, stop words out, a plain plural's "s" off."""
    tokens = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]
    return [w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w for w in tokens]


def bm25(chunks: list[Chunk], question: str, limit: int) -> list[Chunk]:
    """The chunks sharing words with the question, best first. k1 = 1.2, b = 0.75."""
    docs = [Counter(words(c.text)) for c in chunks]
    if not docs:
        return []
    frequency = Counter(word for doc in docs for word in doc)          # how many chunks hold each word
    average = sum(doc.total() for doc in docs) / len(docs) or 1
    k1, b = 1.2, 0.75
    scored = []
    for chunk, doc in zip(chunks, docs):
        score = 0.0
        for word in set(words(question)):
            n, tf = frequency[word], doc[word]
            if tf == 0:
                continue
            idf = math.log(1 + (len(chunks) - n + 0.5) / (n + 0.5))
            score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc.total() / average))
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:limit]]


def nearest(vectors: np.ndarray, query: np.ndarray, limit: int) -> list[int]:
    """Vector search: the indexes of the rows most like the query, by cosine similarity, best first."""
    scores = vectors @ query / (np.linalg.norm(vectors, axis=1) * np.linalg.norm(query))
    return [int(i) for i in np.argsort(scores)[::-1][:limit]]


def fuse(chunks: list[Chunk], question: str, near: list[Chunk], limit: int) -> list[Chunk]:
    """Reciprocal rank fusion: each chunk scores 1 / (60 + rank) in each list it is in, and the scores add up."""
    score: dict[int, float] = {}
    for ranking in (bm25(chunks, question, limit * 2), near):
        for rank, chunk in enumerate(ranking, 1):
            score[id(chunk)] = score.get(id(chunk), 0) + 1 / (RRF_K + rank)
    by_id = {id(c): c for c in chunks}
    best = sorted(score, key=score.get, reverse=True)[:limit]
    return [by_id[i] for i in best]
