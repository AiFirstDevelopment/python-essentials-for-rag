# Chapter 5: packages and imports.
from rag.chunks import chunk_page

pieces = chunk_page("First sentence. " * 80)
print(len(pieces), [len(p) for p in pieces])
