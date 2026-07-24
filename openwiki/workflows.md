---
type: "Reference"
title: "Workflows"
description: "Step-by-step workflows for the Quiz do Professor app: answer pipeline, moderation, avatar generation, QR code sharing, and question access via URL query params."
---

# Workflows

## 1. Quiz Answer Flow (Core Loop)

This is the primary user-facing workflow. Triggered when a student clicks "Enviar Resposta".

```
User types answer → Submit button
       │
       ▼
  Is answer empty? ──yes──→ Show warning, stop
       │ no
       ▼
  Session blocked? ──yes──→ Show block error, stop
       │ no
       ▼
  MODERATION_ENABLED? ──no──→ Skip to LLM
       │ yes
       ▼
  check_text() ──local keywords──→ Blocked? → Escalate warning
       │                              (1st → 2nd → block session)
       │ passed
       ▼
  check_text() ──LLM semantic──→ Blocked? → Escalate warning
       │ passed
       ▼
  evaluate_answer() ──OpenRouter/DeepSeek──→ Response text
       │
       ▼
  clean_text_for_tts() ──Strip markdown──→ Clean text
       │
       ▼
  generate_speech() ──edge-tts──→ MP3 temp file
       │
       ▼
  Set session_state: answered=True, response_text, audio_file
       │
       ▼
  Display: response text + talking GIF + audio player
```

**Key files:** `app.py:147-201`, `content_filter.py:218-233`, `llm_service.py:71-75`, `tts_service.py:14-26`

## 2. Audio-Visual Sync

After an answer is evaluated, the professor avatar "speaks" the response.

1. `get_talking_gif_base64()` returns base64 GIF (cached or newly generated)
2. Audio file is read and base64-encoded
3. Inline HTML component renders:
   - `<img>` with talking GIF as `src`
   - `<audio autoplay>` with base64 MP3
   - JavaScript `onplay` event swaps GIF to talking version
   - JavaScript `onended` event swaps GIF back to idle version
4. Component height fixed at 250px

**Key file:** `app.py:208-231`

## 3. Content Moderation Pipeline

Two-layer check with escalation:

### Layer 1: Local (instant, no API cost)
- Normalize input: leet-speak translation, lowercase
- Scan against `BLOCKED_KEYWORDS` set (~120 terms in Portuguese + English)
- Test against `BLOCKED_PATTERNS` regex patterns
- If hit → return blocked immediately

### Layer 2: LLM Semantic (API call)
- Only runs if Layer 1 passes
- Uses same OpenRouter LLM with low temperature (0.1)
- Prompt is medical-context-aware (allows clinical terms like "skull perforation", "surgery")
- Returns binary: "SEGURO" (safe) or "BLOQUEAR" (block)

### Escalation
- Warning 1 → "Esta é sua primeira advertência"
- Warning 2 → "Esta é sua segunda advertência. Uma última chance"
- Warning 3+ → Session blocked, must reload page

**Key files:** `content_filter.py:150-244`, `app.py:175-197`

## 4. Avatar Generation and Caching

Avatars are drawn programmatically — no image files are bundled.

### On first run (or cache miss):
1. `_draw_scientist_frame()` draws individual PIL frames with parametric mouth, eyes, blinks
2. `_frames_to_gif_bytes()` converts frames to palette-mode GIF with transparency
3. Bytes written to `assets/scientist.gif` (talking) or `assets/scientist_idle.gif` (idle)

### On subsequent runs:
- GIFs loaded directly from disk cache

### Talking animation details:
- 10 FPS (100ms per frame)
- Mouth opens/closes using `sin()` wave
- Eyes blink every 10th frame
- If audio duration provided: GIF duration matches audio, plays once
- If no duration: 20-frame default, infinite loop

### Idle animation details:
- 48 frames at 125ms = 6-second cycle
- Mouth closed, occasional blink (frames 30-31)
- Gentle eye movement

**Key file:** `avatar.py:288-364`

## 5. Question Access via URL Query Params

Questions are accessed individually via URL query parameters, not sequentially:

1. Questions loaded from `questions.json` on first page load
2. `st.query_params.get("q")` reads the question ID from the URL
3. If no `q` parameter → info message directing user to use a `?q=<id>` link
4. If `q` is not a valid integer → error message "ID da pergunta inválido"
5. If `q` does not match any question → error message "Pergunta não encontrada"
6. Matching question is displayed for answering
7. "Tentar novamente" → resets `answered` state, allows re-answer

**Note:** There is no "next question" or sequential navigation. Each question is an independent page accessed via its URL. Question IDs come from the `id` field in `questions.json`.

**Key file:** `app.py:104-126`, `app.py:239-248`

## 6. QR Code Question Sharing

Each question page displays a QR code at the bottom for easy mobile sharing:

1. `APP_URL` from `src/config.py` is combined with the current `question_id` to build the share URL: `{APP_URL}?q={question_id}`
2. `generate_qr_code(question_url)` in `src/qrcode_service.py` creates a QR code PNG via the `qrcode` library
3. The QR code is displayed at 150px width with a caption showing the shareable link
4. Scanning the QR code opens the specific question page on the user's device

**Key file:** `app.py:250-254`, `src/qrcode_service.py`

## 7. Git Commit History (Development Progression)

| Commit | Change | Significance |
|---|---|---|
| `7fe5f94` | Initial commit | Full working app with OpenSpec tooling |
| `bed06d7` | Content moderation | Added `content_filter.py`, LLM-based filtering |
| `151919e` | Refactor config | Environment-based settings, `.env` support |
| `b361c5b` | Avatar sync | Switch to idle-talking GIF swap with audio |
| `e4b5b38` | Idle animation | Added `scientist_idle.gif` asset |
| `d9f1185` | OpenSpec sync | Added `opsx-sync` command |
| `79d3153` | Dynamic paths | OpenSpec commands use status JSON paths |
| `ea7147f` | PR #35 merge | Repo hygiene audit — added `.gitignore`, `.env.example`, independent question access, QR code sharing, OpenSpec specs |
