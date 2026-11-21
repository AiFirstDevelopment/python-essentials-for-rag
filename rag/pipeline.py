"""Chapter 10: a minimal RAG pipeline. Read the documents, chunk them, embed them, find the chunks most like the
question, and have the model answer from those chunks only.    uv run -m rag.pipeline "your question" """
import asyncio
import sys
from pathlib import Path

from anthropic import AsyncAnthropic
from pypdf import PdfReader

from rag.chunking import chunk_text
from rag.vectors import top_k

DOCS = Path(__file__).resolve().parent.parent / "docs"
SYSTEM = "Answer only from the context. If the answer is not in it, say you don't know."


def read(path: Path) -> str:
    if path.suffix == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
    return path.read_text()


def load_chunks(folder: Path = DOCS) -> list[str]:
    files = sorted(p for p in folder.iterdir() if p.suffix in {".txt", ".md", ".pdf"})
    return [chunk for path in files for chunk in chunk_text(read(path), size=50, overlap=10)]


async def answer(question: str, chunks: list[str], embedder, client) -> str:
    vectors = embedder.encode(chunks, normalize_embeddings=True)
    query = embedder.encode([question], normalize_embeddings=True)[0]
    context = "\n\n".join(chunks[i] for i in top_k(query, vectors, k=2))
    response = await client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
    )
    if response.stop_reason == "refusal":
        return "The model declined."
    return "".join(block.text for block in response.content if block.type == "text")


async def main():
    from sentence_transformers import SentenceTransformer
    question = " ".join(sys.argv[1:]) or "How long do I have to return an item?"
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    print(await answer(question, load_chunks(), embedder, AsyncAnthropic()))


if __name__ == "__main__":
    asyncio.run(main())
