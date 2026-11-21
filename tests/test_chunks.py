from rag.chunks import CHUNK_CHARS, chunk_file, chunk_page


def test_a_short_page_is_one_piece():
    assert chunk_page("  One sentence.  ") == ["One sentence."]


def test_pieces_fit_and_end_at_a_sentence():
    pieces = chunk_page("This is a sentence. " * 100)
    assert all(len(p) <= CHUNK_CHARS for p in pieces)
    assert all(p.endswith(".") for p in pieces)
    assert " ".join(pieces) == ("This is a sentence. " * 100).strip()


def test_a_line_break_after_a_period_ends_a_sentence():
    pieces = chunk_page(("word " * 100 + "end.\n") * 3)
    assert pieces[0].endswith("end.")


def test_no_sentence_end_past_halfway_cuts_at_a_space():
    pieces = chunk_page("Short. " + "word " * 300)
    assert len(pieces[0]) <= CHUNK_CHARS and pieces[0].endswith("word")


def test_no_space_at_all_cuts_at_the_limit():
    assert [len(p) for p in chunk_page("x" * 2000)] == [900, 900, 200]


def test_chunks_are_numbered_across_pages():
    chunks = chunk_file("a.pdf", ["Page one.", "Page two."])
    assert [(c.page, c.seq) for c in chunks] == [(1, 0), (2, 1)]
