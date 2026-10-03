from dotenv import load_dotenv

load_dotenv()

import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import checks
import gemma

app = FastAPI(title="Wireframe AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "app": "Wireframe AI backend", "docs": "/docs", "info": "/api/info"}


@app.get("/api/info")
def info():
    return {"model": gemma.model_name(), "provider": "Gemini API", "directions": list(gemma.DIRECTIONS)}


async def _img(file: UploadFile):
    return checks.to_png(await file.read(), file.content_type or "")


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), notes: str = Form("")):
    img, mime = await _img(file)
    try:
        return {"elements": await gemma.read_elements(img, mime, notes)}
    except Exception as e:
        raise HTTPException(502, f"Gemma call failed: {e}")


@app.post("/api/design")
async def design(
    file: UploadFile = File(...),
    direction: str = Form(...),
    elements: str = Form("[]"),
    notes: str = Form(""),
):
    img, mime = await _img(file)
    els = json.loads(elements or "[]")
    try:
        raw = await gemma.write_design(img, mime, direction, els, notes)
    except Exception as e:
        raise HTTPException(502, f"Gemma call failed: {e}")
    html = checks.clean_html(raw)
    return {"html": html, "check": checks.recall(html, els)}


class EditBody(BaseModel):
    html: str
    instruction: str
    elements: list = []


@app.post("/api/edit")
async def edit(body: EditBody):
    try:
        raw = await gemma.edit_design(body.html, body.instruction, body.elements)
    except Exception as e:
        raise HTTPException(502, f"Gemma call failed: {e}")
    html = checks.clean_html(raw)
    return {"html": html, "check": checks.recall(html, body.elements)}
