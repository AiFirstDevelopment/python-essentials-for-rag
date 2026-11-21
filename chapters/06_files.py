# Chapter 6: files. pathlib for paths, with for anything that must be closed, pypdf for a PDF.
from pathlib import Path

from pypdf import PdfReader

docs = Path(__file__).resolve().parent.parent / "docs"

for path in sorted(docs.iterdir()):
    print(path.name, path.suffix)

with open(docs / "returns.txt", encoding="utf-8") as f:        # closed when the block ends, even on an error
    print(f.read()[:60])

pdf = PdfReader(docs / "shipping.pdf")
print(len(pdf.pages), "page(s):", pdf.pages[0].extract_text()[:60])
