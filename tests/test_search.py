import numpy as np

from rag.chunks import Chunk
from rag.search import bm25, fuse, nearest, words


def chunk(seq, text):
    return Chunk("f.txt", 1, seq, text)


def test_words_drops_stop_words_and_plurals():
    assert words("What are the Returns for invoices?") == ["return", "invoice"]
    assert words("glass bus") == ["glass", "bus"]


def test_bm25_ranks_matches_and_drops_the_rest():
    chunks = [chunk(0, "shipping is free"), chunk(1, "refund refund policy"), chunk(2, "refund window policy")]
    assert bm25(chunks, "refund", 5) == [chunks[1], chunks[2]]


def test_nearest_is_cosine_similarity():
    vectors = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])
    assert nearest(vectors, np.array([1.0, 0.1]), 2) == [0, 2]


def test_fuse_lifts_a_chunk_both_searches_found():
    chunks = [chunk(0, "refund window"), chunk(1, "refund"), chunk(2, "something else")]
    fused = fuse(chunks, "refund window", near=[chunks[2], chunks[0]], limit=2)
    assert fused[0] is chunks[0]


def test_fuse_scores_are_reciprocal_ranks():
    a, b, c = chunk(0, "refund refund refund"), chunk(1, "refund policy text here"), chunk(2, "other")
    # bm25 ranks a 1st and b 2nd; vector search ranks c 1st and b 2nd: b = 1/62 + 1/62 beats a = 1/61 and c = 1/61
    assert fuse([a, b, c], "refund", near=[c, b], limit=3)[0] is b
