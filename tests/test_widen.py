from rag.chunks import Chunk
from rag.widen import widen


def test_a_chunk_gets_its_neighbours_in_one_passage():
    chunks = [Chunk("f.txt", 1, i, f"part {i}.") for i in range(5)]
    [passage] = widen([chunks[2]], chunks)
    assert passage.text == "part 1.\npart 2.\npart 3."


def test_neighbouring_picks_become_one_passage_not_two():
    chunks = [Chunk("f.txt", 1, i, f"part {i}.") for i in range(5)]
    passages = widen([chunks[1], chunks[2]], chunks)
    assert [p.text for p in passages] == ["part 0.\npart 1.\npart 2.\npart 3."]


def test_neighbours_never_cross_files():
    chunks = [Chunk("a.txt", 1, 0, "a0."), Chunk("b.txt", 1, 1, "b1.")]
    assert [p.text for p in widen([chunks[1]], chunks)] == ["b1."]
