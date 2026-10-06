import io
import re
import urllib.request
from fpdf import FPDF
from PIL import Image

_REPLACEMENTS = {
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u2022": "-",
    "\u00a0": " ",
}


def _clean(text: str) -> str:
    """Make text safe for the built-in PDF fonts (Latin-1 only)."""
    for old, new in _REPLACEMENTS.items():
        text = text.replace(old, new)
    return "".join(ch for ch in text if ord(ch) < 256)


def _inline(text: str) -> str:
    """Keep **bold**, drop other markdown symbols."""
    text = _clean(text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+)(?<!\*)\*(?!\*)", r"\1", text)
    return text


def _download(url: str, timeout: int = 60):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        if len(data) > 1000:
            Image.open(io.BytesIO(data)).verify()
            return data
    except Exception:
        pass
    return None


def markdown_to_pdf(markdown_text: str) -> bytes:
    """Convert the pipeline's Markdown output into a PDF (bytes), with images."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    width = pdf.w - pdf.l_margin - pdf.r_margin

    sizes = {1: 20, 2: 15, 3: 12}
    for raw in markdown_text.split("\n"):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped in ("---", "***"):
            pdf.ln(2)
            continue

        img = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
        if img:
            data = _download(img.group(2))
            if data:
                w, h = Image.open(io.BytesIO(data)).size
                img_w = width
                img_h = img_w * h / w
                if pdf.get_y() + img_h > pdf.h - pdf.b_margin:
                    pdf.add_page()
                pdf.image(io.BytesIO(data), x=pdf.l_margin, w=img_w)
                pdf.ln(2)
            continue

        heading = re.match(r"(#{1,3})\s+(.*)", stripped)
        if heading:
            level = len(heading.group(1))
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", sizes[level])
            pdf.multi_cell(0, 8 if level > 1 else 10, _clean(heading.group(2).replace("*", "")),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            continue

        bullet = re.match(r"[-*]\s+(.*)", stripped)
        if bullet:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_x(pdf.l_margin + 4)
            pdf.multi_cell(0, 6, "- " + _inline(bullet.group(1)), markdown=True,
                           new_x="LMARGIN", new_y="NEXT")
            continue

        quote = re.match(r">\s*(.*)", stripped)
        if quote:
            stripped = quote.group(1)

        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            pdf.set_font("Helvetica", "I", 9)
            pdf.multi_cell(0, 5, _clean(stripped.strip("*")), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            continue

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, _inline(stripped), markdown=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    return bytes(pdf.output())