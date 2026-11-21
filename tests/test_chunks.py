from rag.chunks import CHUNK_CHARS, chunk_file, chunk_page


def test_a_short_page_is_one_piece():
    assert chunk_page("  One sentence.  ") == ["One sentence."]


def test_pieces_fit_and_end_at_a_sentence():
    pieces = chunk_page("This is a sentence. " * 100)
    assert all(len(p) <= CHUNK_CHARS for p in pieces)
    assert all(p.endswith(".") for p in pieces)
    assert " ".join(pieces) == ("This is a sentence. " * 100).strip()


def test_chunks_are_numbered_across_pages():
    chunks = chunk_file("a.pdf", ["Page one.", "Page two."])
    assert [(c.page, c.seq) for c in chunks] == [(1, 0), (2, 1)]
