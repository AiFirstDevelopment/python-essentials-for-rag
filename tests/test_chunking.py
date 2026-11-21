import pytest

from rag.chunking import chunk_text


def test_chunks_overlap():
    chunks = chunk_text("a b c d e f g h", size=4, overlap=1)
    assert chunks == ["a b c d", "d e f g", "g h"]


def test_short_text_is_one_chunk():
    assert chunk_text("just a few words") == ["just a few words"]


def test_overlap_must_be_smaller_than_size():
    with pytest.raises(ValueError):
        chunk_text("a b c", size=2, overlap=2)
