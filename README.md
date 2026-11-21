# Python Essentials for RAG

The Python a JavaScript or TypeScript developer needs to build a RAG pipeline, in ten short chapters. Each file in
`chapters/` is one chapter of the video; `rag/` is the pipeline chapter 10 puts together.

## Run it

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # install uv (macOS/Linux)
uv sync                                            # Python, a virtual environment and the packages
uv run chapters/01_hello.py
uv run pytest
export ANTHROPIC_API_KEY=...                       # chapters 8 and 10 call Claude
uv run -m rag.pipeline "How long do I have to return an item?"
```

| Chapter | File | JavaScript/TypeScript you already know |
|---|---|---|
| 1. Setup | `chapters/01_hello.py` | node, npm |
| 2. Syntax | `chapters/02_syntax.py` | braces, `null`, template strings |
| 3. Data | `chapters/03_data.py` | arrays, objects, `map`/`filter`, `JSON` |
| 4. Types | `chapters/04_types.py` | interfaces, Zod |
| 5. Packages and imports | `chapters/05_imports.py`, `pyproject.toml` | `package.json`, `import` |
| 6. Files | `chapters/06_files.py` | `fs`, `path` |
| 7. NumPy | `chapters/07_vectors.py` | (no operator overloading in JS) |
| 8. Async and a model | `chapters/08_ask.py` | `async`/`await`, `Promise.all` |
| 9. Testing | `tests/` | Jest |
| 10. Putting it together | `rag/pipeline.py` | |

The documents in `docs/` are sample policies for a fictional store.
