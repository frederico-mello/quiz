# Source Map

## Top-Level Files

### `app.py` — Streamlit Entrypoint
The entire application UI and orchestration lives in this single file (~265 lines).

- **Lines 17-74**: CSS with light/dark theme support via `prefers-color-scheme`
- **Lines 78-99**: `main()` — Page config, session state initialization
- **Lines 100-127**: Score statistics display, question retrieval, completion screen
- **Lines 129-201**: Question display, answer input, content moderation pipeline, LLM evaluation
- **Lines 202-261**: Response display (text + animated avatar + audio), retry/next buttons
- **Line 264**: `if __name__ == "__main__": main()`

Key imports: `avatar`, `config`, `content_filter`, `llm_service`, `quiz_data`, `tts_service`

### `questions.json` — Question Bank
JSON array of 5 question objects. Each has `id`, `question` (text prompt), and `correct_answer`. Questions are about dental instruments and equipment history (in Portuguese). Currently hardcoded for a dentistry course context.

### `requirements.txt` — Dependencies
```
streamlit>=1.30.0        # Web UI framework
langchain>=0.2.0         # LLM orchestration
langchain-openai>=0.1.0  # OpenAI-compatible LLM wrapper
openai>=1.0.0            # OpenAI client (used by langchain-openai)
edge-tts>=6.1.0          # Microsoft Edge TTS (free)
mutagen>=1.47.0           # Audio metadata (MP3 duration)
python-dotenv>=1.0.0     # .env file loading
```

### `.env.example` — Environment Template
Two variables: `OPENROUTER_API_KEY` and `MODERATION_ENABLED`. Actual `.env` is gitignored.

---

## `src/` — Application Modules

### `src/config.py` — Configuration Loader
Loads `.env` via `python-dotenv` and exports all config constants.

| Export | Source | Default |
|---|---|---|
| `OPENROUTER_API_KEY` | env | *required*, raises `ValueError` if missing |
| `OPENROUTER_BASE_URL` | env | `https://openrouter.ai/api/v1` |
| `LLM_MODEL` | env | `deepseek/deepseek-v4-flash` |
| `MODERATION_ENABLED` | env | `true` |
| `TTS_VOICE` | env | `pt-BR-FranciscaNeural` |
| `TEMP_AUDIO_DIR` | env | `tmp/audio` |

### `src/llm_service.py` — LLM Evaluation
Three functions:

- **`get_llm()`** → Returns a configured `ChatOpenAI` instance pointing at OpenRouter with DeepSeek provider routing
- **`build_prompt(question, correct_answer, user_answer)`** → Constructs a `ChatPromptTemplate` with system persona (friendly quiz professor) and human message containing the quiz context
- **`clean_text_for_tts(text)`** → Strips markdown, links, excessive whitespace for clean TTS output
- **`evaluate_answer(question, correct_answer, user_answer)`** → Orchestrates: get LLM → build prompt → invoke → clean for TTS → return string

### `src/content_filter.py` — Content Moderation
Two-layer moderation system:

**Data structures:**
- `BLOCKED_KEYWORDS` (lines 4-123): Set of ~120 Portuguese and English sexual/violent terms
- `BLOCKED_PATTERNS` (lines 125-130): Regex patterns for obfuscated bypasses
- `LEET_SPEAK_MAP` (line 132): Character substitution table for normalization

**Functions:**
- **`normalize_leet(text)`** → Translates leet-speak characters, lowercases
- **`check_keywords(text)`** → Scans normalized text against keyword set
- **`check_patterns(text)`** → Tests regex patterns against normalized text
- **`check_text_local(text)`** → Runs keyword then pattern checks
- **`check_text_llm(text, llm)`** → LLM-based semantic moderation (medical context-aware)
- **`check_text(text, use_llm=True)`** → Main entry: local first, then LLM
- **`get_warning_level(warnings)`** → Maps warning count to escalation level (`none`, `first`, `second`, `blocked`)

### `src/avatar.py` — Professor Avatar
Programmatic cartoon scientist drawing and GIF generation (~365 lines).

**Constants:** `ASSETS_DIR`, `GIF_PATH`, `IDLE_GIF_PATH`, `WIDTH/HEIGHT`, `CENTER_X`, `FACE_Y`

**Key classes/functions:**
- **`TransparentGifConverter`** — Handles palette-based GIF transparency. Converts RGBA frames to P-mode with transparency index 0
- **`_draw_scientist_frame(mouth_open_factor, is_blinking, eye_offset)`** — Draws a single frame of the scientist character using PIL primitives (ellipses, polygons, arcs). Features: hair, glasses, nose, mouth (open/closed), lab coat
- **`_frames_to_gif_bytes(frames, duration_ms, loop)`** — Converts PIL frames to GIF bytes with transparency
- **`generate_talking_gif_bytes(audio_duration_seconds)`** — Generates mouth-animated GIF. If audio duration provided, GIF duration matches audio (plays once); otherwise 20-frame default loop
- **`generate_idle_gif_bytes()`** — 48-frame idle animation with occasional blinks (125ms/frame = 6s cycle)
- **`get_talking_gif_base64(duration_seconds)`** — Returns base64 talking GIF (cached to `assets/scientist.gif`)
- **`get_idle_gif_base64()`** — Returns base64 idle GIF (cached to `assets/scientist_idle.gif`)

### `src/quiz_data.py` — Question Loader
Simple JSON loader:

- **`load_questions(filepath)`** → Reads and returns JSON array from file
- **`get_question(questions, index)`** → Returns question dict at index, or `None` if out of bounds
- **`shuffle_questions(questions)`** → Returns a shuffled copy (not currently used in `app.py`)

### `src/tts_service.py` — Text-to-Speech
Wrapper around `edge-tts`:

- **`generate_speech_async(text, output_path, voice)`** → Async edge-tts call
- **`generate_speech(text)`** → Sync wrapper: creates temp dir, generates MP3, returns path
- **`get_audio_duration(filepath)`** → Returns MP3 duration in seconds via `mutagen` (not currently used in `app.py`)

### `src/__init__.py`
Empty file. Makes `src/` a Python package.

---

## `assets/` — Generated Avatar Files

| File | Description |
|---|---|
| `scientist.gif` | Cached talking animation GIF (50 KB) |
| `scientist_idle.gif` | Cached idle animation GIF (19 KB) |

Both are generated on first run by `avatar.py` and persisted to disk.

---

## `.opencode/` — OpenCode Tooling

| Path | Purpose |
|---|---|
| `commands/opsx-apply.md` | OpenSpec apply-change command |
| `commands/opsx-archive.md` | OpenSpec archive-change command |
| `commands/opsx-explore.md` | OpenSpec explore command |
| `commands/opsx-propose.md` | OpenSpec propose-change command |
| `commands/opsx-sync.md` | OpenSpec delta sync command |
| `skills/openspec-*/SKILL.md` | Skill definitions for OpenSpec operations |
| `plugins/graphify.js` | Graphify plugin for code knowledge graph |

---

## `.github/` — CI/CD and AI Prompts

| Path | Purpose |
|---|---|
| `workflows/openwiki-update.yml` | Scheduled daily OpenWiki doc refresh → auto-PR |
| `prompts/opsx-*.prompt.md` | GitHub Copilot prompt files for OpenSpec |
| `skills/openspec-*/SKILL.md` | GitHub Copilot skill definitions |

---

## `openspec/` — Change Management

| Path | Purpose |
|---|---|
| `config.yaml` | OpenSpec schema config (spec-driven, minimal) |
| `specs/` | Empty — no active specs |
| `changes/archive/` | Archived change records |
