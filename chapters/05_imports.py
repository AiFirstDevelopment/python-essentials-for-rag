# Chapter 5: packages and imports. rag/ is a package (a folder of modules); uv add put numpy in pyproject.toml.
from rag.chunks import chunk_page   # one function from the rag package

text = "First sentence. " * 80
pieces = chunk_page(text)
print(len(pieces), "pieces;", [len(p) for p in pieces], "characters")
