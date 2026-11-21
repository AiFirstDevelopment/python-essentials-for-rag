# Python Essentials for RAG

The Python a JavaScript or TypeScript developer needs to build a RAG pipeline and test it with an eval harness. Each
file in `chapters/` is a chapter of the video; `rag/` is the pipeline and `evals/` its harness and golden set.

The pipeline follows the same logic as Joel Stevick's demo pipeline
([joelstevick-demo-rag-pipeline](https://github.com/AiFirstDevelopment/joelstevick-demo-rag-pipeline)), in Python:
chunks of about 900 characters cut at a sentence end, BM25 keyword search and vector search fused by reciprocal rank
(k = 60), and each chosen chunk widened with its neighbours before the model answers from those passages only.

## Run it

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh        # install uv (macOS/Linux)
uv sync                                                 # Python, a virtual environment and the packages
uv run chapters/01_hello.py
uv run pytest                                           # no network, no API key
uv run python -m evals.harness --retrieval-only         # scores retrieval on the golden set, free
export ANTHROPIC_API_KEY=...                            # the steps below call Claude
uv run python -m rag.pipeline "Can I return a sale item for a refund?"
uv run python -m evals.harness                          # scores the answers too
```

| Chapter | Where | The JavaScript/TypeScript you already know |
|---|---|---|
| 1. Setup | `chapters/01_hello.py` | node, npm |
| 2. Syntax | `chapters/02_syntax.py` | braces, `null`, template strings |
| 3. Data | `chapters/03_data.py` | arrays, objects, `map`/`filter`, `JSON` |
| 4. Types | `chapters/04_types.py` | interfaces, Zod |
| 5. Packages and imports | `chapters/05_imports.py`, `pyproject.toml` | `package.json`, `import` |
| 6. Files | `chapters/06_files.py` | `fs`, `path` |
| 7. NumPy | `chapters/07_vectors.py` | (JavaScript has no operator overloading) |
| 8. Async and a model | `chapters/08_ask.py` | `async`/`await`, `Promise.all` |
| 9. Testing | `tests/` | Jest |
| 10. The pipeline | `rag/chunks.py`, `rag/search.py`, `rag/widen.py`, `rag/pipeline.py` | |
| 11. The eval harness | `evals/golden.jsonl`, `evals/harness.py` | |

The documents in `docs/` are sample policies for a fictional store.
