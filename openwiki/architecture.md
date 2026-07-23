---
type: "Reference"
title: "Architecture"
description: "Component diagram, data flow, session state model, and QR code question-sharing for the Quiz do Professor Streamlit app."
---

# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit App (app.py)             │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Quiz UI  │  │ Avatar   │  │ Audio Player      │  │
│  │ (HTML/   │  │ (base64  │  │ (base64 inline    │  │
│  │  CSS)    │  │  GIF)    │  │  <audio> + JS)    │  │
│  └────┬─────┘  └────┬─────┘  └───────┬───────────┘  │
│       │              │                │              │
│  ┌────▼──────────────▼────────────────▼───────────┐  │
│  │              Session State Manager              │  │
│  │  questions, answered, response_text,            │  │
│  │  audio_file, moderation_warnings,               │  │
│  │  moderation_blocked                             │  │
│  └────────────────────┬───────────────────────────┘  │
│                       │                              │
│  ┌────────────────────▼───────────────────────────┐  │
│  │              Processing Pipeline               │  │
│  │                                                │  │
│  │  1. Content Filter (content_filter.py)          │  │
│  │     ├─ Local keyword/pattern check              │  │
│  │     └─ LLM semantic moderation (optional)       │  │
│  │                                                │  │
│  │  2. LLM Evaluation (llm_service.py)             │  │
│  │     └─ OpenRouter → DeepSeek v4 Flash           │  │
│  │                                                │  │
│  │  3. TTS Generation (tts_service.py)             │  │
│  │     └─ edge-tts → MP3 file                      │  │
│  │                                                │  │
│  │  4. Avatar GIF (avatar.py)                      │  │
│  │     └─ PIL-drawn talking/idle GIF               │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│   External APIs     │
│  ┌───────────────┐  │
│  │ OpenRouter    │  │
│  │ (LLM + Mod)   │  │
│  └───────────────┘  │
└─────────────────────┘
```

## Data Flow: Answer Submission

Questions are accessed individually via URL query parameters (`?q=<id>`), not sequentially. The user navigates to a specific question URL (optionally via a QR code), types an answer, and submits.

1. **Page load** → `st.query_params` reads `q` parameter; `get_question_by_id()` looks up the question by numeric ID
2. **User types answer** → Streamlit `text_input` widget
3. **Submit clicked** → `st.button("Enviar Resposta")`
3. **Content moderation** → `check_text()` in `content_filter.py`
   - First pass: local keyword + regex pattern matching (fast, no API cost)
   - Second pass: LLM semantic check via OpenRouter (if local pass succeeds)
   - Blocked? → Increment `moderation_warnings`, show warning, or block session at 3 strikes
4. **LLM evaluation** → `evaluate_answer()` in `llm_service.py`
   - Builds a prompt with question, correct answer, and user answer
   - Calls OpenRouter (DeepSeek v4 Flash) via LangChain
   - Strips markdown/formatting for clean TTS output
5. **TTS generation** → `generate_speech()` in `tts_service.py`
   - Converts LLM response to MP3 via edge-tts
   - Saves to temp file in `tmp/audio/`
6. **Avatar animation** → `get_talking_gif_base64()` in `avatar.py`
   - Generates or loads cached talking GIF
   - Returns base64-encoded GIF for inline HTML
7. **Display** → Streamlit renders response text, animated avatar with synced audio player

## Question Access and QR Code Sharing

Questions are accessed individually via URL query parameters rather than sequential navigation. Each question URL follows the pattern `{APP_URL}?q=<question_id>`.

- On page load, `app.py` reads `st.query_params.get("q")` and parses it as an integer
- If no `q` parameter is present, the app shows an info message directing the user to use a `?q=<id>` link
- If the ID is invalid or not found, an error message is displayed
- At the bottom of every question page, `generate_qr_code()` from `src/qrcode_service.py` renders a QR code encoding the question's shareable URL, allowing students to scan and open a specific question on mobile devices

**Key files:** `app.py:104-126` (query param handling), `app.py:250-254` (QR code display), `src/qrcode_service.py`

## Session State Model

All quiz state lives in `st.session_state` (Streamlit's per-browser-tab state):

| Key | Type | Purpose |
|---|---|---|
| `questions` | `list[dict]` | Loaded question bank |
| `answered` | `bool` | Whether current question has been answered |
| `response_text` | `str` | LLM evaluation text |
| `audio_file` | `str\|None` | Path to generated MP3 temp file |
| `moderation_warnings` | `int` | Count of content filter hits |
| `moderation_blocked` | `bool` | Whether session is blocked (3+ warnings) |

No database or persistent storage exists. Closing the browser tab loses all progress.

## Content Moderation Architecture

Two-layer moderation in `content_filter.py`:

**Layer 1 — Local keyword/pattern check** (`check_text_local`):
- `BLOCKED_KEYWORDS`: Set of ~100+ Portuguese and English sexual/violent terms
- `BLOCKED_PATTERNS`: Regex patterns for obfuscated text
- `normalize_leet()`: Leet-speak normalization before matching
- Zero API cost, instant response

**Layer 2 — LLM semantic check** (`check_text_llm`):
- Uses same OpenRouter LLM with a moderation-specific system prompt
- Aware of medical/dental context (allows clinical terms)
- Returns "SEGURO" or "BLOQUEAR"
- Only runs if Layer 1 passes

**Warning escalation**: `get_warning_level()` tracks warnings (first → second → blocked). Three violations blocks the session; user must reload.

## Avatar System

The avatar is a **programmatically drawn cartoon scientist** using PIL (`Pillow`). No external image assets are bundled for the character; `assets/scientist.gif` and `assets/scientist_idle.gif` are generated and cached on first run.

- `_draw_scientist_frame(mouth_open_factor, is_blinking, eye_offset)` → Single PIL frame
- `generate_talking_gif_bytes(audio_duration)` → Multi-frame GIF with mouth animation synced to audio duration
- `generate_idle_gif_bytes()` → Looping idle GIF with occasional blinks
- `TransparentGifConverter` handles palette-based transparency for GIF format
- GIFs are cached to disk under `assets/` and loaded on subsequent runs

The HTML audio player in `app.py` (lines 218-231) uses JavaScript `onplay`/`onended` events to swap between talking and idle GIFs during audio playback.

## LLM Integration

- **Provider**: OpenRouter API (acts as a proxy to multiple LLM providers)
- **Model**: `deepseek/deepseek-v4-flash` (configurable via `LLM_MODEL`)
- **Framework**: LangChain `ChatOpenAI` with OpenRouter's OpenAI-compatible endpoint
- **Provider routing**: `extra_body.provider.order` prioritizes DeepInfra, then Together
- **Temperature**: 0.7 for evaluation, 0.1 for moderation
- **Prompt**: System prompt instructs the LLM to act as a friendly quiz professor, respond in spoken Portuguese (no markdown), and keep responses under 500 characters
