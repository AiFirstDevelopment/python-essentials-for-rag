"""A page's text cut into the pieces the pipeline retrieves: the demo pipeline's chunkPage, in Python.
About CHUNK_CHARS a piece, cut at a sentence end past the halfway mark, else at a space. A piece never crosses a page."""
from dataclasses import dataclass

CHUNK_CHARS = 900
ENDS = (". ", "? ", "! ", ".\n", "?\n", "!\n")


@dataclass
class Chunk:
    file: str
    page: int
    seq: int          # its place in its file's order of chunks, for widening
    text: str


def chunk_page(text: str) -> list[str]:
    pieces, rest = [], text.strip()
    while len(rest) > CHUNK_CHARS:
        window = rest[:CHUNK_CHARS]
        sentence = max(window.rfind(end) for end in ENDS)
        space = window.rfind(" ")
        cut = sentence + 1 if sentence > CHUNK_CHARS / 2 else space if space > 0 else CHUNK_CHARS
        pieces.append(rest[:cut].strip())
        rest = rest[cut:].strip()
    if rest:
        pieces.append(rest)
    return pieces


def chunk_file(file: str, pages: list[str]) -> list[Chunk]:
    """Every page of one file, chunked, numbered in reading order across the file."""
    texts = [(page, piece) for page, text in enumerate(pages, 1) for piece in chunk_page(text)]
    return [Chunk(file, page, seq, piece) for seq, (page, piece) in enumerate(texts)]
