"""Builds docs/shipping.pdf and docs/gear-care.pdf from tools/src/*.txt with real paragraphs, so pypdf extracts
whole sentences. The first line of each page is its heading; ==PAGE== starts a new page.
    uv run --group tools python tools/make_pdfs.py"""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

HERE = Path(__file__).resolve().parent
styles = getSampleStyleSheet()

for src in sorted((HERE / "src").glob("*.txt")):
    story = []
    for n, page in enumerate(src.read_text(encoding="utf-8").split("==PAGE==")):
        if n:
            story.append(PageBreak())
        heading, *paragraphs = [line for line in page.strip().splitlines() if line.strip()]
        story += [Paragraph(heading, styles["Heading1"]), Spacer(1, 6)]
        story += [Paragraph(p.replace("&", "&amp;"), styles["BodyText"]) for p in paragraphs]
    out = HERE.parent / "docs" / f"{src.stem}.pdf"
    SimpleDocTemplate(str(out), pagesize=letter).build(story)
    print(out.name)
