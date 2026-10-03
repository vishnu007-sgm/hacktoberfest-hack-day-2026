"""All Gemma 4 calls (via the Gemini API) live here."""
import json
import os
import re

from google import genai
from google.genai import types

DIRECTIONS = {
    "Clean Modern": "airy whitespace, rounded corners, soft shadows, one calm accent color, friendly sans-serif feel",
    "Compact Enterprise": "dense, table/grid oriented, small type, neutral grays with a single blue accent, efficient and professional",
    "Bold Editorial": "large heavy headings, strong contrast, thick borders, vivid accent color, magazine-like layout",
}

_client = None


def model_name() -> str:
    return os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")


def _client_():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to backend/.env and restart uvicorn.")
        _client = genai.Client(api_key=key)
    return _client


async def _ask(contents):
    # Gemma models take everything in the prompt (no system instruction).
    r = await _client_().aio.models.generate_content(model=model_name(), contents=contents)
    return r.text or ""


def _image(img: bytes, mime: str):
    return types.Part.from_bytes(data=img, mime_type=mime)


async def read_elements(img: bytes, mime: str, notes: str) -> list:
    prompt = (
        "You are reading a UI wireframe (hand-drawn or digital). List every UI element you see, "
        "top to bottom, as JSON only, no markdown: "
        '{"elements":[{"type":"button|input|heading|text|image|nav|list|card|other","text":"visible label or empty"}]}. '
        "Copy any visible text exactly."
    )
    if notes.strip():
        prompt += f"\nUser notes: {notes.strip()}"
    raw = await _ask([_image(img, mime), prompt])
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        raise ValueError("Gemma did not return JSON. Try a clearer wireframe.")
    return json.loads(m.group(0)).get("elements", [])


async def write_design(img: bytes, mime: str, direction: str, elements: list, notes: str) -> str:
    style = DIRECTIONS.get(direction, DIRECTIONS["Clean Modern"])
    prompt = (
        "You are a front-end developer. Turn this wireframe into a working, good-looking web page.\n"
        f"Design direction: {direction} - {style}.\n"
        f"Elements detected in the wireframe: {json.dumps(elements)}\n"
        f"User notes: {notes.strip() or 'none'}\n\n"
        "Rules:\n"
        "- Output ONLY the HTML that goes inside <body>. No <html>, <head>, markdown fences or explanation.\n"
        "- Style with Tailwind CSS utility classes only (the Tailwind CDN is already loaded).\n"
        "- Include EVERY detected element, keeping its text.\n"
        "- No <script>, no inline event handlers, no external images (use colored blocks, inline SVG or emoji).\n"
        "- Use <button> for actions, not links with href.\n"
        "- Responsive and accessible: semantic tags, labels on inputs, good contrast."
    )
    return await _ask([_image(img, mime), prompt])


async def edit_design(html: str, instruction: str, elements: list) -> str:
    prompt = (
        "Here is the current HTML (Tailwind CSS) of a web page body:\n\n"
        f"{html}\n\n"
        f"Change request: {instruction}\n\n"
        "Apply ONLY this change and keep everything else identical. Keep all existing text and elements. "
        "Return the FULL updated HTML body only. No markdown fences, no explanation, no <script>, no inline event handlers."
    )
    return await _ask([prompt])
