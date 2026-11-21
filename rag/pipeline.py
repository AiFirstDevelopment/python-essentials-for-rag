"""Chapter 10: the pipeline. Read and chunk the documents, search them two ways (BM25 and vectors), fuse the
rankings, widen each chunk with its neighbours, and have the model answer from those passages only.
    uv run python -m rag.pipeline "your question" """
import asyncio
import sys
from pathlib import Path

from anthropic import AsyncAnthropic
from pypdf import PdfReader

from rag.chunks import Chunk, chunk_file
from rag.search import fuse, nearest
from rag.widen import Passage, widen

DOCS = Path(__file__).resolve().parent.parent / "docs"
MODEL = "claude-opus-5-5"
SYSTEM = "Answer only from the passages. If the answer is not in them, say you don't know."


def pages(path: Path) -> list[str]:
    if path.suffix == ".pdf":
        return [page.extract_text() or "" for page in PdfReader(path).pages]
    return [path.read_text(encoding="utf-8")]


def load(folder: Path = DOCS) -> list[Chunk]:
    files = sorted(p for p in folder.iterdir() if p.suffix in {".txt", ".md", ".pdf"})
    return [chunk for path in files for chunk in chunk_file(path.name, pages(path))]


class Index:
    """The chunks and their embeddings, computed once."""

    def __init__(self, chunks: list[Chunk], embedder):
        self.chunks, self.embedder = chunks, embedder
        self.vectors = embedder.encode([c.text for c in chunks], normalize_embeddings=True)

    def retrieve(self, question: str, top: int = 3) -> list[Passage]:
        query = self.embedder.encode([question], normalize_embeddings=True)[0]
        near = [self.chunks[i] for i in nearest(self.vectors, query, top * 2)]
        return widen(fuse(self.chunks, question, near, top), self.chunks)


async def answer(question: str, passages: list[Passage], client) -> str:
    context = "\n\n".join(f"[{p.file}, page {p.first_page}]\n{p.text}" for p in passages)
    response = await client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Passages:\n\n{context}\n\nQuestion: {question}"}],
    )
    if response.stop_reason == "refusal":
        return "The model declined."
    return "".join(block.text for block in response.content if block.type == "text")


def embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


async def main():
    question = " ".join(sys.argv[1:]) or "Can I return a sale item for a refund?"
    index = Index(load(), embedder())
    print(await answer(question, index.retrieve(question), AsyncAnthropic()))


if __name__ == "__main__":
    asyncio.run(main())
