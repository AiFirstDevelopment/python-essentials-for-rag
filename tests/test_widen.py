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


def test_the_budget_stops_widening():
    big = "x" * 6000
    chunks = [Chunk("f.txt", 1, i, big) for i in range(5)]
    [first, second] = widen([chunks[1], chunks[3]], chunks)
    # chunk 1 takes chunk 0 (6,000 characters); a second neighbour would pass 10,800, so chunks 2 and 4 stay out
    assert (first.text.count("x"), second.text.count("x")) == (12000, 6000)
