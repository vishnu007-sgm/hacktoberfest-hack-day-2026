# Wireframe AI

## Team / attendee

- Team name (if applicable): Team AVM
- Members and GitHub usernames: <name> (@vishnu007-sgm @GITUSERMANOLYA @ashwinivarikuppala2)


## Challenge

- [ ] Best Open-Source AI Project
- [x] Best Use of Gemma 4
- [ ] Build on elah

## Project links

- Public GitHub repository: https://github.com/vishnu007-sgm/WireFrameAI.git
- Open-source license (link to the license file): <repo URL>/blob/main/LICENSE (MIT)

## Problem and solution

Turning a hand-drawn wireframe into working front-end code is slow and repetitive. Wireframe AI is for designers, students and developers who want a quick working prototype from a sketch.

Workflow: the user draws on the built-in canvas or uploads a wireframe (PNG, JPG or PDF), optionally adding style notes. Gemma 4 reads the image and lists every UI element it sees. Three parallel Gemma 4 calls then write three working pages in different styles (Clean Modern, Compact Enterprise, Bold Editorial), each shown in a live preview as soon as it finishes. The user can type a change ("replace the small circle buttons with rectangular boxes with bold labels"), Gemma 4 edits the page, and Undo restores the previous version. The result can be copied or downloaded as standalone HTML.

## Approach and technologies

- Model: Gemma 4 (`gemma-4-26b-a4b-it`) through the Gemini API, using the `google-genai` Python SDK. The model ID is set in `GEMMA_MODEL`.
- Backend: Python, FastAPI, Uvicorn. PyMuPDF renders PDFs to images. python-dotenv loads config.
- Frontend: React 18 and Vite. Tailwind CSS via CDN. Live preview in a sandboxed iframe. HTML5 Canvas for drawing.
- Plain-code safety and checks (no model): generated HTML has scripts, inline event handlers and external links stripped before preview. A recall check confirms each detected element's text appears in each design and shows a match rate.
- Why: Gemma 4 handles the vision, the code writing and the edits, so a single model covers the whole loop.
- AI-assisted development: the code was written with the help of Claude (Anthropic). Libraries used: FastAPI, React, Vite, Tailwind CSS, PyMuPDF, google-genai. <add GitHub Copilot or other tools only if you actually used them>

## Challenge evidence

### Best Use of Gemma 4

- Gemma 4 model identifier and Gemini API integration: `gemma-4-26b-a4b-it` via the Gemini API (`google-genai` SDK).
- Code link showing the integration: <repo URL>/blob/main/backend/gemma.py (`read_elements`, `write_design`, `edit_design`) and <repo URL>/blob/main/backend/main.py (routes `/api/analyze`, `/api/design`, `/api/edit`).
- Input and useful output; multimodal value: input is a wireframe image or PDF. Gemma 4 has to understand the visual layout and handwritten labels to produce the element list and three working web pages. Without the image understanding, the app cannot work.

## Current status

- What works: <edit after testing> backend API, image/PDF input, canvas drawing, three parallel design generations with live preview, the "describe a change" edit box with Undo, element match-rate check, copy and download of HTML.
- Known limitations / incomplete features: handwriting can be misread. The match rate checks that detected elements are present, not that the layout is pixel-perfect. Designs are not saved after a page refresh. No React-component export, offline PWA, diff view or Fabric.js stencils yet.
- What you would improve next: save design history, add the diff view for edits, add React-component export, add an accessibility re-check after each edit.

## Submission checklist

- [x] Project repository is public and links work.
- [x] Required challenge evidence is included.
- [x] Project uses an open-source license where required by the challenge.
- [x] Work and reused materials are represented honestly.
- [x] No API keys, tokens, passwords, or private data are included.
- [x] I followed the organizers' build window and submission instructions.
