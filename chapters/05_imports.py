# Chapter 5: packages and imports. rag/ is a package (a folder of modules); uv add put numpy in pyproject.toml.
from rag.chunking import chunk_text   # like: import { chunkText } from "./rag/chunking"

print(chunk_text("one two three four five six", size=4, overlap=1))
