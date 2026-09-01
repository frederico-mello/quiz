---
type: "Reference"
title: "Source Map"
description: "File-by-file reference for the Quiz do Professor codebase, covering app.py, the src/ modules and their public functions, config, tests, and the openspec feature specs."
tags: [source-map, app.py, src, config, content-filter, llm, tts, avatar, qrcode, openspec, tests]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-01T12:56:02.391Z
sources:
  - id: openwiki-source-5f5b95b3d6a215fa02ceb945
    resource: repo://.env.example
  - id: openwiki-source-4f2678f93d3fd3835f9f2909
    resource: repo://.github/workflows/test.yml
  - id: openwiki-source-17dded95897e01ee430228e3
    resource: repo://app.py
  - id: openwiki-source-484ea79304d0fedbdb4059be
    resource: repo://assets/scientist_idle.gif
  - id: openwiki-source-6715950be4accab07461d0e9
    resource: repo://assets/scientist.gif
  - id: openwiki-source-38af7bdd34d817fbd3c29077
    resource: repo://openspec/config.yaml
  - id: openwiki-source-eb7b34f9cec06f0bccbc206c
    resource: repo://openspec/specs/avatar/spec.md
  - id: openwiki-source-4827d344148f4e0235cf4061
    resource: repo://openspec/specs/content-filter/spec.md
  - id: openwiki-source-fd18c7ac3e340241a92f29f0
    resource: repo://openspec/specs/independent-question-access/spec.md
  - id: openwiki-source-6b032faa35c5b934ac7b1f52
    resource: repo://openspec/specs/llm-evaluation/spec.md
  - id: openwiki-source-646a657f9ca8f2b679a5a033
    resource: repo://openspec/specs/llm-fallback/spec.md
  - id: openwiki-source-9bbee9dc2a9ccc55a88bfdc2
    resource: repo://openspec/specs/question-link-qr-code/spec.md
  - id: openwiki-source-c20c87ad10eba624fc1aa904
    resource: repo://openspec/specs/quiz-ui/spec.md
  - id: openwiki-source-39287d9abf2b2c1792138d1f
    resource: repo://openspec/specs/readme-documentation/spec.md
  - id: openwiki-source-266f08d5fea6115d81c76b9e
    resource: repo://openspec/specs/tts/spec.md
  - id: openwiki-source-e44eab9a26f9187df819fc2a
    resource: repo://pytest.ini
  - id: openwiki-source-cc7a8e8970e0878771c69281
    resource: repo://questions.json
  - id: openwiki-source-042e05bb663605d09adced3b
    resource: repo://requirements-dev.txt
  - id: openwiki-source-373640cd8a0886cee69db282
    resource: repo://requirements.txt
  - id: openwiki-source-e33acebb184e33f455744c7a
    resource: repo://src/avatar.py
  - id: openwiki-source-d502c275990c6476221bf080
    resource: repo://src/config.py
  - id: openwiki-source-f9d47768347023605881a59a
    resource: repo://src/content_filter.py
  - id: openwiki-source-e1a4d69bfefe5039cbbe03ea
    resource: repo://src/llm_service.py
  - id: openwiki-source-7e8ebb5fd2b205c019de32cc
    resource: repo://src/qrcode_service.py
  - id: openwiki-source-a3a1a606dc74b73abab13376
    resource: repo://src/quiz_data.py
  - id: openwiki-source-ffc42264d7caa035bb1f3478
    resource: repo://src/tts_service.py
  - id: openwiki-source-f0a6e7dc03522b2682f88655
    resource: repo://tests/conftest.py
  - id: openwiki-source-aee60addf228e6c9bf133836
    resource: repo://tests/test_app.py
  - id: openwiki-source-ba50025ec5b6ebd5f9b58bad
    resource: repo://tests/test_content_filter.py
  - id: openwiki-source-fbe25e08bbf3954904783586
    resource: repo://tests/test_llm_service.py
generated: { by: "openwiki/0.4.3", at: "2026-09-01T12:56:02.391Z" }
---

# Source Map

A navigation aid for the Quiz do Professor codebase. The application is a single-page Streamlit app whose logic is split between one top-level entry file (`app.py`) and a set of focused modules under `src/`. Each module owns one concern and exposes a small public surface; `app.py` imports one or two functions from each module and wires them together inside `main()`. The architecture, end-to-end request flow, and session-state lifecycle are covered in detail on the [Architecture](architecture.md) page; this page is the file-level index of who owns what.

## Top-Level Files

### `app.py` — Streamlit Entrypoint

The entire application UI, session state, and orchestration lives in this one file (`main()` is the only top-level entry point; `if __name__ == "__main__": main()` runs it).

- **`QUIZ_CSS`** (`app.py` L18-L76): CSS with light/dark theme support via `prefers-color-scheme`; `.question-box`, `.response-text`, and `.progress-text` are the app's custom classes.
- **`main()`** (`app.py` L81): calls `validate_config()` first, then `st.set_page_config`, injects `QUIZ_CSS`, and guards on `OPENROUTER_API_KEY`. Initializes session state keys (`questions`, `answered`, `response_text`, `audio_file`, `moderation_warnings`, `moderation_blocked`) on first run. Reads `st.query_params["q"]` to select a question by id, renders the question box, the answer input/submit button, the moderation escalation pipeline, and the evaluated response with synchronized avatar + audio. Finally renders a QR code for `APP_URL?q=<id>`.
- **Answer-submission flow** (`app.py` L149-L203): empty answers warn; an already-blocked session refuses further submissions; otherwise `check_text` runs (when `MODERATION_ENABLED`) and, on a block, increments `moderation_warnings` and maps it to `first`/`second`/`blocked` via `get_warning_level`. Clean text calls `_process_answer()` → `evaluate_answer(...)` → `generate_speech(...)` → sets `answered=True` and `st.rerun()`.
- **Response playback** (`app.py` L204-L249): when answered, renders `response_text`, and if `audio_file` exists on disk, embeds `get_talking_gif_base64()` + base64 audio in an `<audio>` element whose `onplay`/`onended` handlers swap the avatar image between the talking and idle GIFs. The "Tentar novamente" button resets `answered`/`response_text`/`audio_file` and reruns.

Imports from `src`: `avatar` (`get_idle_gif_base64`, `get_talking_gif_base64`), `config` (`APP_URL`, `MODERATION_ENABLED`, `OPENROUTER_API_KEY`, `validate_config`), `content_filter` (`check_text`, `get_warning_level`), `llm_service` (`evaluate_answer`), `qrcode_service` (`generate_qr_code`), `quiz_data` (`get_question_by_id`, `load_questions`), `tts_service` (`generate_speech`).

### `questions.json` — Question Bank

A JSON array of question objects, each with three fields: `id` (integer), `question` (the Portuguese text prompt), and `correct_answer`. The current file holds five questions about historical dental instruments and equipment (e.g. "Trépano", "Estojo de coroas metálicas"), written for a Brazilian-Portuguese dentistry course. The schema is `[{ "id": int, "question": str, "correct_answer": str }, ...]`.

### `requirements.txt` — Runtime Dependencies

```
streamlit>=1.30.0
langchain>=0.2.0
langchain-openai>=0.2.0
openai>=1.0.0
edge-tts>=6.1.0
python-dotenv>=1.0.0
qrcode[pil]>=7.4.0
```

`langchain-openai` provides the `ChatOpenAI` wrapper used to talk to the LiteLLM primary and OpenRouter fallback endpoints. `edge-tts` provides Microsoft Edge neural TTS. `python-dotenv` loads `.env`. `qrcode[pil]` generates the shareable-question QR codes. (Development-only tooling is listed in `requirements-dev.txt`.)

### `.env.example` — Environment Template

Documents the full env-var set the app expects. It groups variables into three blocks:

- **LiteLLM primary**: `LITELLM_API_BASE_URL`, `LITELLM_API_KEY`, `LITELLM_MODEL` (e.g. `glm-4.7-flash:q4_K_M`).
- **OpenRouter fallback**: `OPENROUTER_API_KEY`, `OPENROUTER_FALLBACK_MODEL` (e.g. `nvidia/nemotron-3-nano-30b-a3b:nitro`), `OPENROUTER_BASE_URL` (defaults to `https://openrouter.ai/api/v1`).
- **Other**: `MODERATION_ENABLED`.

It also records the deprecated migration path: the old `LLM_MODEL` was replaced by `LITELLM_MODEL`, and `OPENROUTER_BASE_URL` is now only the fallback base URL (the primary base URL is `LITELLM_API_BASE_URL`). The real `.env` is gitignored.

## `src/` — Application Modules

### `src/config.py` — Configuration Loader

Loads `.env` via `python-dotenv` at import time and exports all configuration as module-level constants. Because constants are read at import time, tests and scripts that need to override them reload the module (`importlib.reload`) or set `SKIP_CONFIG_VALIDATION=1`.

| Export | Source | Default |
|---|---|---|
| `LITELLM_API_BASE_URL` | env | `""` (required at runtime) |
| `LITELLM_API_KEY` | env | `""` (required at runtime) |
| `LITELLM_MODEL` | env | `""` (required at runtime) |
| `OPENROUTER_API_KEY` | env | `""` (required at runtime) |
| `OPENROUTER_FALLBACK_MODEL` | env | `""` (required at runtime) |
| `OPENROUTER_BASE_URL` | env | `https://openrouter.ai/api/v1` |
| `MODERATION_ENABLED` | env | `true` (parsed to a bool: `"...".lower() == "true"`) |
| `APP_URL` | env | `https://lappquiz.ict.unesp.br` |
| `TTS_VOICE` | env | `pt-BR-FranciscaNeural` |
| `TEMP_AUDIO_DIR` | env | `tmp/audio` |

**`validate_config()`** (`src/config.py` L19-L38): checks that every variable in `REQUIRED_ENV_VARS` (the five LiteLLM+OpenRouter keys) is set in the environment. It is intentionally **not** called at import time — it is called from `app.main()` on startup — so that tools and tests can import `src.*` without a complete `.env`. Setting `SKIP_CONFIG_VALIDATION=1` makes it a no-op (the test suite relies on this). On missing vars it raises a `ValueError` naming each missing key and its description.

### `src/llm_service.py` — LLM Evaluation & Fallback

Builds the LLM prompt, instantiates the primary and fallback providers, cleans model output for TTS, and orchestrates the two-tier evaluation. Functions:

- **`get_litellm_llm()`** (`src/llm_service.py` L20-L27): returns a `ChatOpenAI` configured for the **primary** LiteLLM server (`LITELLM_MODEL`, `LITELLM_API_KEY` wrapped in a `pydantic.SecretStr`, `LITELLM_API_BASE_URL`, `temperature=0.7`).
- **`get_openrouter_fallback_llm()`** (`src/llm_service.py` L30-L37): returns a `ChatOpenAI` configured for the **fallback** OpenRouter provider (`OPENROUTER_FALLBACK_MODEL`, `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `temperature=0.7`).
- **`build_prompt(question, correct_answer, user_answer)`** (`src/llm_service.py` L40-L74): builds a `ChatPromptTemplate` with a system persona (a friendly, encouraging quiz professor who explains the correct answer, refuses improper content politely, and caps output at ~500 characters without markdown) and a human message carrying the question/correct-answer/user-answer triple. Blank `user_answer` is rendered as `(sem resposta)` so the model never sees an empty field.
<!-- openwiki: broken internal link [url] file "url" does not exist. Fix the href or restore the target, then delete this comment. -->
- **`clean_text_for_tts(text)`** (`src/llm_service.py` L77-L83): strips markdown (`*`, `#`, `_`, `~`, backticks), rewrites `[text](url)` to `text`, collapses repeated newlines to `. ` and other newlines to spaces, and trims — producing clean, speakable Portuguese for the TTS engine.
- **`evaluate_answer(question, correct_answer, user_answer)`** (`src/llm_service.py` L86-L111): the orchestration entry point. Builds the prompt, tries the primary LiteLLM LLM; on any exception it logs a warning and falls back to the OpenRouter LLM and returns its cleaned response. If **both** providers fail it raises a `RuntimeError` whose message names the primary model and error and the fallback model and error — so the UI can surface a single clear failure.

### `src/content_filter.py` — Content Moderation

A two-layer moderation system: a deterministic local blocklist first, then an optional LLM-based semantic check. `app.py` uses it to escalate repeated improper submissions to a session block.

**Data:**
- `BLOCKED_KEYWORDS` (`src/content_filter.py` L4-L123): a set of ~120 Portuguese and English sexual/violent terms.
- `BLOCKED_PATTERNS` (`src/content_filter.py` L125-L130): regex patterns targeting obfuscated bypasses (leet spacing, specific profanity, non-ASCII glyphs).
- `LEET_SPEAK_MAP` (`src/content_filter.py` L132): a `str.maketrans` table used to normalize leet-speak before matching.

**Functions:**
- **`normalize_leet(text)`** (`src/content_filter.py` L135-L136): applies the leet translation table and lowercases the text.
- **`check_keywords(text)`** (`src/content_filter.py` L150-L155): normalizes and returns `(True, "Termo impróprio detectado: '<keyword>'")` on the first keyword substring hit, else `(False, None)`.
- **`check_patterns(text)`** (`src/content_filter.py` L139-L147): normalizes and runs each `BLOCKED_PATTERNS` regex; returns `"Conteúdo contém padrão bloqueado."` on the first match (a bad regex is skipped, not raised). Returns `None` when clean.
- **`check_text_local(text)`** (`src/content_filter.py` L158-L165): runs `check_keywords` then `check_patterns`; returns `(True, msg)` if either blocks.
- **`check_text_llm(text, llm)`** (`src/content_filter.py` L168-L194): prompts the given LLM as a content moderator that is *medical/odontological context-aware* (explicitly allows procedure-related words like surgery, blood, skull perforation). It coerces a list-of-blocks response to text, lowercases it, and blocks only when the answer starts with `bloquear`; otherwise `(False, None)`.
- **`check_text(text, use_llm=True)`** (`src/content_filter.py` L197-L215): the main entry point used by `app.py`. Runs the local check first and returns immediately if blocked. When `use_llm` is true it lazily imports `get_litellm_llm` and runs the LLM check; if the LLM call raises, it **fails open** (returns `(False, None)`) because the local blocklist is the primary defense and LLM moderation is best-effort.
- **`get_warning_level(warnings)`** (`src/content_filter.py` L218-L226): maps the warning count to `"none"` (0), `"first"` (1), `"second"` (2), or `"blocked"` (≥3), which `app.py` uses to drive escalation and session blocking.

### `src/avatar.py` — Professor Avatar (PIL GIFs)

A ~365-line module that programmatically draws a cartoon scientist and renders talking/idle animated GIFs with transparency, caching them to disk under `assets/`.

**Constants:** `ASSETS_DIR`, `GIF_PATH` (`assets/scientist.gif`), `IDLE_GIF_PATH` (`assets/scientist_idle.gif`), `WIDTH`/`HEIGHT` (200×220), `CENTER_X` (100), `FACE_Y` (95).

**Classes/functions:**
- **`TransparentGifConverter`** (`src/avatar.py` L17-L68): converts RGBA frames to palette (P-mode) GIFs with a transparency index. `process(img)` rewrites the palette so index `0` becomes transparent, remaps any pixels that previously used index `0` to a free index, and sets `info["transparency"]`/`info["background"]` so frames composite cleanly over the page.
- **`_draw_scientist_frame(mouth_open_factor=0.0, is_blinking=False, eye_offset=0.0)`** (`src/avatar.py` L71-L265): draws a single frame — hair, ears, face, eyes (with blink and look-around), eyebrows, glasses, nose, mouth (closed smile arc vs. open talking ellipse), bangs, and a lab-coat body — using PIL primitives.
- **`_frames_to_gif_bytes(frames, duration_ms, loop=0)`** (`src/avatar.py` L268-L285): runs each frame through `TransparentGifConverter` and saves a single animated GIF with `disposal=2`.
- **`generate_talking_gif_bytes(audio_duration_seconds=0)`** (`src/avatar.py` L288-L311): if `audio_duration_seconds > 0`, generates enough frames at 100 ms/frame to match the audio and sets `loop=1` (play once); otherwise 20 frames with `loop=0` (infinite). Mouth openness follows `|sin(frame·π/4)|`, blinks on frames 8/9, eyes drift with `frame·0.4`.
- **`generate_idle_gif_bytes()`** (`src/avatar.py` L314-L331): 48 frames at 125 ms (≈6 s cycle), closed mouth, blink on frames 30/31, infinite loop.
- **`get_talking_gif_base64(duration_seconds=0)`** (`src/avatar.py` L334-L352): returns a base64 talking GIF; with a positive duration it generates an audio-matched GIF in memory, otherwise it uses the disk-cached default at `GIF_PATH` (generating and persisting it on first run).
- **`get_idle_gif_base64()`** (`src/avatar.py` L355-L364): returns a base64 idle GIF, cached to `IDLE_GIF_PATH` (generated on first run).

### `src/quiz_data.py` — Question Loader

Thin JSON loader with no dependencies beyond the stdlib `json`.

- **`load_questions(filepath="questions.json")`** (`src/quiz_data.py` L4-L6): reads and returns the JSON array from the file (raises `json.JSONDecodeError` on bad JSON).
- **`get_question(questions, index)`** (`src/quiz_data.py` L9-L12): returns the question at `0 <= index < len(questions)`, else `None` (negative or out-of-range index returns `None` rather than raising).
- **`get_question_by_id(questions, question_id)`** (`src/quiz_data.py` L15-L19): linear scan returning the first question whose `id` equals `question_id`, else `None`. `app.py` uses this to resolve `?q=<id>`.

### `src/qrcode_service.py` — QR Code Generation

A thin wrapper around the `qrcode` library used to make questions shareable.

- **`generate_qr_code(data)`** (`src/qrcode_service.py` L6-L11): `qrcode.make(data)`, saves the image as PNG into an `io.BytesIO` (rewound to position 0) and returns it. `app.py` feeds it `{APP_URL}?q={question_id}` and passes the buffer straight to `st.image`.

### `src/tts_service.py` — Text-to-Speech

A sync wrapper around the async `edge-tts` API.

- **`generate_speech_async(text, output_path, voice=TTS_VOICE)`** (`src/tts_service.py` L8-L10): the underlying `edge_tts.Communicate(text, voice).save(output_path)` coroutine.
- **`generate_speech(text)`** (`src/tts_service.py` L13-L25): ensures `TEMP_AUDIO_DIR` exists, creates a temp `.mp3` path via `tempfile.mkstemp`, runs the async call through `asyncio.run`. On any exception it removes the temp file and raises `RuntimeError("Falha ao gerar áudio TTS: ...")`; on success it returns the MP3 path.

### `src/__init__.py`

Empty package marker that makes `src/` importable as a Python package.

## `assets/` — Generated Avatar Files

| File | Description |
|---|---|
| `scientist.gif` | Cached talking-animation GIF (~50 KB), written by `avatar.get_talking_gif_base64` on first run |
| `scientist_idle.gif` | Cached idle-animation GIF (~19 KB), written by `avatar.get_idle_gif_base64` on first run |

Both are build artifacts produced by `src/avatar.py` and are safe to delete; the module regenerates them on the next request.

## `tests/` — Pytest Suite

`pytest.ini` sets `testpaths = tests`, `pythonpath = src`, and `addopts = -ra --strict-markers`, so `import src.*` works without an install step.

- **`conftest.py`**: an autouse `_required_llm_env` fixture that sets `SKIP_CONFIG_VALIDATION=1` and fills in the five required LLM env vars with test values, so the whole suite runs without a real `.env`; plus shared `sample_questions` and `tmp_json_file` fixtures.
- **`test_app.py`**: stubs Streamlit/`src.*` modules via `sys.modules` and reloads `app`, then asserts the QR link uses the default public `APP_URL` (`https://lappquiz.ict.unesp.br`) when `APP_URL` is unset and a custom value when it is set.
- **`test_config.py`**: reloads `src.config` under env overrides to assert `APP_URL` defaults to the public application and honors `APP_URL`.
- **`test_content_filter.py`**: covers `check_keywords`, `check_patterns`, `check_text_local`, `normalize_leet`, the `get_warning_level` escalation ladder, the `check_text_llm` "BLOQUEAR" classification, and `check_text`'s LLM-skip/local-block/fail-open/use_llm=False paths.
- **`test_llm_service.py`**: covers `build_prompt` (contains all three inputs; marks blank answers `(sem resposta)`), `clean_text_for_tts`, and `evaluate_answer`'s three outcomes — primary succeeds (fallback not called), primary fails → fallback succeeds, both fail → `RuntimeError` naming both providers.
- **`test_qrcode_service.py`**: asserts `generate_qr_code` returns a `BytesIO` starting with the PNG signature.
- **`test_quiz_data.py`**: covers `load_questions` (valid + invalid JSON), `get_question` (valid/negative/out-of-range), and `get_question_by_id` (existing/missing).

A GitHub Actions workflow at `.github/workflows/test.yml` runs this suite on pushes to `main` and on PRs against `main` (Python 3.10, installing both `requirements.txt` and `requirements-dev.txt`); see [Testing](testing.md).

## `openspec/specs/` — Feature Specifications

Per-feature specifications that document intended behavior for the implemented features. Each lives in its own directory with a `spec.md`; these are the source of truth for *what* each feature should do, while the code in `src/` is the implementation.

| Spec | Intent |
|---|---|
| `openspec/specs/avatar/` | Programmatic PIL scientist avatar, talking/idle GIFs, disk caching |
| `openspec/specs/content-filter/` | Two-layer moderation (local blocklist + LLM semantic check) and escalation |
| `openspec/specs/independent-question-access/` | Each question is an independent page addressed by `?q=<id>` |
| `openspec/specs/llm-evaluation/` | LLM-based answer evaluation with the professor persona |
| `openspec/specs/llm-fallback/` | Automatic fallback from the LiteLLM primary to the OpenRouter provider; `RuntimeError` on total failure |
| `openspec/specs/question-link-qr-code/` | QR code encoding `APP_URL?q=<id>` for sharing a question |
| `openspec/specs/quiz-ui/` | Streamlit single-page quiz UI, query-param routing, session state |
| `openspec/specs/readme-documentation/` | `README.md` as the project's human-readable entry document |
| `openspec/specs/tts/` | edge-tts synthesis and audio playback |

`openspec/config.yaml` declares the `spec-driven` schema and per-artifact rules that route spec/proposal/design/tasks work through the OpenSpec Plus skills; `openspec/changes/` (with `openspec/changes/archive/`) holds change proposals and their archived records.

## Tooling & CI

| Path | Purpose |
|---|---|
| `.github/workflows/test.yml` | Runs `pytest` on pushes/PRs to `main` (Python 3.10) |
| `.github/workflows/repository-hygiene.yml` | Repository hygiene checks |
| `.github/workflows/openwiki-update.yml` | Scheduled daily OpenWiki doc refresh → auto-PR |
| `.github/prompts/opsx-*.prompt.md` | GitHub Copilot prompt files for OpenSpec operations |
| `.github/skills/openspec-*/SKILL.md` | GitHub Copilot skill definitions for OpenSpec |
| `.opencode/commands/opsx-*.md` | OpenCode command definitions for OpenSpec (`apply`, `archive`, `explore`, `propose`, `sync`, …) |
| `.opencode/skills/openspec-*/SKILL.md` | OpenCode skill definitions for OpenSpec operations |
| `.opencode/plugins/graphify.js` | Graphify plugin for the code knowledge graph |
| `pytest.ini` | `testpaths = tests`, `pythonpath = src`, `--strict-markers` |
| `requirements-dev.txt` | Development-only dependencies used by the test workflow |
| `auditoria.yaml` | Audit/checklist configuration |
| `AGENTS.md` / `CLAUDE.md` / `README.md` | Agent and human-facing project guidance |

## Related Pages

- [Architecture](architecture.md) — end-to-end module map and the answer-submission data flow through moderation, two-tier LLM evaluation, TTS, and avatar playback.
- [Quickstart](quickstart.md) — how to install, configure `.env`, and run the app locally.
- [Testing](testing.md) — the pytest suite, the GitHub Actions `test` workflow, and the manual testing checklist.
