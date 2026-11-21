# Chapter 5: packages and imports. rag/ is a package (a folder of modules); uv add put numpy in pyproject.toml.
from rag.chunks import chunk_page   # like: import { chunkPage } from "./rag/chunks"

text = "First sentence. " * 80
pieces = chunk_page(text)
print(len(pieces), "pieces;", [len(p) for p in pieces], "characters")
