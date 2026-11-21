# Python Essentials for RAG

The Python you need to build a RAG pipeline and test it with an eval harness. Each
file in `chapters/` is a chapter of the video; `rag/` is the pipeline and `evals/` its harness and golden set.

The pipeline follows the same logic as Joel Stevick's demo pipeline
([joelstevick-demo-rag-pipeline](https://github.com/AiFirstDevelopment/joelstevick-demo-rag-pipeline)), in Python:
chunks of about 900 characters cut at a sentence end, BM25 keyword search and vector search fused by reciprocal rank
(k = 60), Claude Haiku reranking the fused pool, and each chosen chunk widened with its neighbours before the model
answers from those passages only.

## Run it

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh        # install uv (macOS/Linux)
uv sync                                                 # Python, a virtual environment and the packages
uv run chapters/01_hello.py
uv run pytest                                           # no API key needed
uv run python -m evals.harness --retrieval-only         # scores the fused search on the golden set, free
export ANTHROPIC_API_KEY=...                            # the steps below call Claude
uv run python -m rag.pipeline "Can I return a sale item for a refund?"
uv run python -m evals.harness                          # scores the answers too
```

| Chapter | Where |
|---|---|
| 1. Setup | `chapters/01_hello.py` |
| 2. Syntax | `chapters/02_syntax.py` |
| 3. Data | `chapters/03_data.py` |
| 4. Types | `chapters/04_types.py` |
| 5. Packages and imports | `chapters/05_imports.py`, `pyproject.toml` |
| 6. Files | `chapters/06_files.py` |
| 7. NumPy | `chapters/07_vectors.py` |
| 8. Async and a model | `chapters/08_ask.py` |
| 9. Testing | `tests/` |
| 10. The pipeline | `rag/chunks.py`, `rag/search.py`, `rag/rerank.py`, `rag/widen.py`, `rag/pipeline.py` |
| 11. The eval harness | `evals/golden.jsonl`, `evals/harness.py` |

`uv sync` installs PyTorch for sentence-transformers: about 650 MB on macOS, several GB on Linux with NVIDIA's CUDA
packages. The first run also downloads a small embedding model (about 90 MB, `all-MiniLM-L6-v2`); after that, everything but the
model calls runs offline. The pipeline answers with `claude-opus-5-5` and reranks with `claude-haiku-5-5`; a full harness run makes two
calls per golden case.

## The golden set

`evals/golden.jsonl`, one case a line, with the demo's fields: the question, `expected_behavior` (`answer` or
`fallback`), the `required_facts` a right answer must contain (each with the words that count as a match), and the
`sources` (file and page) retrieval must find. `category` is `answerable`, `inferred` (the answer follows from the
documents without being written in them) or `absent` (the documents don't cover it, so the right answer is "I don't
know"). A full run marks each case `pass`, `fail` (naming the facts it missed) or `review` (it answered when it should
have said it doesn't know: a person reads it).

The documents in `docs/` are sample policies for a fictional store; `tools/make_pdfs.py` builds the two PDFs
(`uv run --group tools python tools/make_pdfs.py`).
