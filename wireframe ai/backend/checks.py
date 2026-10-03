"""Plain-code helpers: PDF -> PNG, HTML sanitizing, element recall check. No model calls."""
import re


def to_png(data: bytes, content_type: str):
    """Return (image_bytes, mime). PDFs are rendered to PNG (first page)."""
    if "pdf" in content_type.lower() or data[:4] == b"%PDF":
        import fitz  # pymupdf

        doc = fitz.open(stream=data, filetype="pdf")
        pix = doc[0].get_pixmap(dpi=130)
        return pix.tobytes("png"), "image/png"
    if content_type.startswith("image/"):
        return data, content_type
    return data, "image/png"


def clean_html(raw: str) -> str:
    h = raw.strip()
    fence = re.search(r"```(?:html)?\s*(.*?)```", h, re.S | re.I)
    if fence:
        h = fence.group(1).strip()
    body = re.search(r"<body[^>]*>(.*?)</body>", h, re.S | re.I)
    if body:
        h = body.group(1)
    h = re.sub(r"<!doctype[^>]*>|</?(html|head|body)[^>]*>", "", h, flags=re.I)
    h = re.sub(r"<(script|iframe|object|embed|style)\b[^>]*>.*?</\1\s*>", "", h, flags=re.S | re.I)
    h = re.sub(r"<(script|iframe|object|embed|link|meta|base)\b[^>]*>", "", h, flags=re.I)
    h = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", "", h, flags=re.I)
    h = re.sub(r"(href|src|action)\s*=\s*(\"\s*(javascript:|https?:)[^\"]*\"|'\s*(javascript:|https?:)[^']*')", r'\1="#"', h, flags=re.I)
    return h.strip()


def recall(html: str, elements: list) -> dict:
    text = re.sub(r"<[^>]+>", " ", html).lower()
    text = re.sub(r"\s+", " ", text)
    labels = [str(e.get("text", "")).strip().lower() for e in elements if str(e.get("text", "")).strip()]
    missing = [l for l in labels if l not in text]
    total = len(labels)
    return {"matched": total - len(missing), "total": total, "missing": missing}
