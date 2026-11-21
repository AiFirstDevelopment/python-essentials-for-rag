# Chapter 6: files.
from pathlib import Path

from pypdf import PdfReader

docs = Path("docs")
print(sorted(p.name for p in docs.iterdir()))

with open(docs / "returns.txt", encoding="utf-8") as f:
    print(f.read()[:60])

pdf = PdfReader(docs / "shipping.pdf")
print(pdf.pages[0].extract_text()[:60])
