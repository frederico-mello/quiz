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
│  │  current_index, answered, response_text,        │  │
│  │  audio_file, moderation_warnings, total_score   │  │
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

1. **User types answer** → Streamlit `text_input` widget
2. **Submit clicked** → `st.button("Enviar Resposta")`
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

## Session State Model

All quiz state lives in `st.session_state` (Streamlit's per-browser-tab state):

| Key | Type | Purpose |
|---|---|---|
| `questions` | `list[dict]` | Loaded question bank |
| `current_index` | `int` | Current question index (0-based) |
| `answered` | `bool` | Whether current question has been answered |
| `response_text` | `str` | LLM evaluation text |
| `audio_file` | `str\|None` | Path to generated MP3 temp file |
| `moderation_warnings` | `int` | Count of content filter hits |
| `moderation_blocked` | `bool` | Whether session is blocked (3+ warnings) |
| `total_score` | `float` | Accumulated score (added in commit `3c2af8e`) |

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

## Score Statistics

Added in commit `3c2af8e` (merged via PR #10). The average score percentage is calculated and displayed per question.

**Known bug** (`app.py` lines 112-116): The score calculation is duplicated. Lines 109-111 compute a safe average with `max(1, ...)` to avoid division by zero, but lines 113-115 immediately overwrite it with an unsafe version that divides by `current_index` directly, causing a `ZeroDivisionError` on the first question.
