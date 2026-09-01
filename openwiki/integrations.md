---
type: Reference
title: External Integrations
description: Runtime external services and Python libraries the Quiz do Professor app depends on — LiteLLM/Ollama and OpenRouter LLM endpoints via LangChain ChatOpenAI, edge-tts speech synthesis, qrcode sharing, PIL avatar generation, and the Streamlit runtime.
tags: [integrations, llm, litellm, openrouter, langchain, chatopenai, edge-tts, tts, qrcode, pil, pillow, streamlit, openai]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-01T12:56:02.391Z
sources:
  - id: openwiki-source-17dded95897e01ee430228e3
    resource: repo://app.py
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
  - id: openwiki-source-ffc42264d7caa035bb1f3478
    resource: repo://src/tts_service.py
generated: { by: "openwiki/0.4.3", at: "2026-09-01T12:56:02.391Z" }
---

# External Integrations

Quiz do Professor is a single-file Streamlit app (`app.py`) whose interesting behavior is delegated to focused modules under `src/`, each of which wraps a distinct external dependency. This page covers the **runtime** integrations — the LLM endpoints, the text-to-speech service, the QR-code generator, the avatar image library, and the Streamlit runtime itself — and how the app talks to each of them. Developer tooling (OpenSpec, OpenWiki, Graphify) and CI/CD live on the [Operations](/openwiki/operations.md) page.

The pinned dependency versions in `requirements.txt` are:

| Package | Constraint | Used by |
|---|---|---|
| `streamlit` | `>=1.30.0` | `app.py` (UI runtime) |
| `langchain` | `>=0.2.0` | `src/llm_service.py` (`ChatPromptTemplate`) |
| `langchain-openai` | `>=0.2.0` | `src/llm_service.py` (`ChatOpenAI`) |
| `openai` | `>=1.0.0` | transitive, required by `langchain-openai` |
| `edge-tts` | `>=6.1.0` | `src/tts_service.py` |
| `python-dotenv` | `>=1.0.0` | `src/config.py` (`.env` loading) |
| `qrcode[pil]` | `>=7.4.0` | `src/qrcode_service.py` |

`Pillow` (imported as `PIL`) is **not** listed in `requirements.txt` directly; it is pulled in transitively by `streamlit` and by the `qrcode[pil]` extra, and `src/avatar.py` imports it at runtime (`from PIL import Image, ImageDraw`).

## LLM Endpoints (LiteLLM + OpenRouter)

The app talks to two LLM endpoints, both of which are **OpenAI-compatible HTTP APIs**. The same LangChain primitive — `langchain_openai.ChatOpenAI` — is reused for both; only `base_url`, `model`, and `api_key` differ. There is no OpenAI-the-company dependency: the client is an OpenAI-*protocol* client pointed at two different proxies.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    subgraph App["src/llm_service.py"]
        Prim["get_litellm_llm()<br/>ChatOpenAI, temp 0.7"]
        Fall["get_openrouter_fallback_llm()<br/>ChatOpenAI, temp 0.7"]
    end
    subgraph Mod["src/content_filter.py"]
        ModLLM["check_text_llm()<br/>reuses get_litellm_llm()"]
    end
    Prim -- "LITELLM_API_BASE_URL<br/>LITELLM_MODEL, LITELLM_API_KEY" --> LiteLLM["LiteLLM server<br/>(Ollama backend)"]
    Fall -- "OPENROUTER_BASE_URL<br/>OPENROUTER_FALLBACK_MODEL, OPENROUTER_API_KEY" --> OpenRouter["OpenRouter"]
    ModLLM -- "same primary client" --> LiteLLM
```

Two LLM clients in `src/llm_service.py` plus a best-effort moderation reuse in `src/content_filter.py`, all built on `ChatOpenAI` against two OpenAI-compatible endpoints.

### Primary — LiteLLM server (Ollama backend)

`get_litellm_llm()` constructs a `ChatOpenAI` pointed at the **LiteLLM server** (which itself fronts an Ollama backend):

- `base_url` = `LITELLM_API_BASE_URL` (e.g. `http://localhost:4000`)
- `model` = `LITELLM_MODEL` (e.g. `glm-4.7-flash:q4_K_M`)
- `api_key` = `LITELLM_API_KEY`, wrapped in `pydantic.SecretStr`
- `temperature` = `0.7`

This client is the primary path for answer evaluation and the sole path for LLM moderation. It requires network access to the LiteLLM server.

### Fallback — OpenRouter

`get_openrouter_fallback_llm()` constructs a `ChatOpenAI` pointed at **OpenRouter**, OpenRouter's own OpenAI-compatible gateway at `https://openrouter.ai/api/v1` (overridable via `OPENROUTER_BASE_URL`):

- `base_url` = `OPENROUTER_BASE_URL` (default `https://openrouter.ai/api/v1`)
- `model` = `OPENROUTER_FALLBACK_MODEL` (e.g. `nvidia/nemotron-3-nano-30b-a3b:nitro`)
- `api_key` = `OPENROUTER_API_KEY`, wrapped in `pydantic.SecretStr`
- `temperature` = `0.7`

The fallback is only constructed inside `evaluate_answer()` *after* the primary raises. It requires network access to OpenRouter and a valid `OPENROUTER_API_KEY`.

### Two-tier evaluation and total-failure behavior

`evaluate_answer(question, correct_answer, user_answer)` builds a `ChatPromptTemplate` grading prompt and drives the two-tier chain:

1. Invoke the primary `get_litellm_llm()`.
2. On **any** exception from the primary, log a warning (naming `LITELLM_MODEL`) and invoke the fallback `get_openrouter_fallback_llm()` with the same prompt.
3. If the fallback also raises, raise a `RuntimeError` whose message names **both** the primary error and the fallback error.

The successful response (whichever provider produced it) is run through `clean_text_for_tts()` to strip markdown and normalize whitespace before being returned. `app.py` catches the `RuntimeError` in its submit handler and surfaces it as `st.error(...)`. See [LLM Provider Fallback](/openwiki/concepts/llm-fallback.md) for the full prompt, cleaning, and failure contract.

### Moderation reuses the primary client (best-effort, fail-open)

`src/content_filter.py` performs LLM semantic moderation via `check_text_llm(text, llm)`, which invokes a moderation prompt asking the model to classify the text as `SEGURO` (safe) or `BLOQUEAR` (block). The `llm` argument is **the same `get_litellm_llm()` primary client** from `llm_service` — the moderation pass does **not** use the OpenRouter fallback. The moderation pass is **best-effort and fail-open**: if the LiteLLM call raises (timeout, auth error, network failure, etc.), `check_text` swallows the exception and lets the text through, on the principle that the local keyword/regex blocklist is the primary defense and LLM moderation is a supplementary semantic check. `MODERATION_ENABLED` (default `true`) gates whether the LLM pass is attempted at all.

### Configuration

All LLM endpoint config is read from the environment by `src/config.py` at import time (via `python-dotenv`) and enforced by `validate_config()` at app startup (not at import time, so test imports don't require real credentials):

| Constant | Env var | Required | Default |
|---|---|---|---|
| `LITELLM_API_BASE_URL` | `LITELLM_API_BASE_URL` | yes | — |
| `LITELLM_API_KEY` | `LITELLM_API_KEY` | yes | — |
| `LITELLM_MODEL` | `LITELLM_MODEL` | yes | — |
| `OPENROUTER_API_KEY` | `OPENROUTER_API_KEY` | yes | — |
| `OPENROUTER_FALLBACK_MODEL` | `OPENROUTER_FALLBACK_MODEL` | yes | — |
| `OPENROUTER_BASE_URL` | `OPENROUTER_BASE_URL` | no | `https://openrouter.ai/api/v1` |
| `MODERATION_ENABLED` | `MODERATION_ENABLED` | no | `true` |

`LITELLM_MODEL` and `OPENROUTER_FALLBACK_MODEL` are interpolated into the fallback warning log and the total-failure `RuntimeError`, so changing them changes operator-visible diagnostics. See [Operations](/openwiki/operations.md) for the full environment table and `.env.example` for the template.

## Text-to-Speech (edge-tts)

`src/tts_service.py` wraps the [`edge-tts`](https://pypi.org/project/edge-tts/) library, Microsoft's free Edge TTS endpoint. No API key is required — it depends only on Microsoft's public TTS service availability — but it does require network access.

`generate_speech(text)`:

1. Ensures `TEMP_AUDIO_DIR` (default `tmp/audio`) exists.
2. Allocates a temp `.mp3` file path via `tempfile.mkstemp(suffix=".mp3", dir=TEMP_AUDIO_DIR)` and closes the file descriptor.
3. Runs `asyncio.run(generate_speech_async(text, tmp_path))`, which creates an `edge_tts.Communicate(text, voice)` and `await`s its `.save(output_path)` — `edge-tts` is async, so the module drives its own event loop with `asyncio.run`.
4. The voice is `TTS_VOICE` (default `pt-BR-FranciscaNeural`, a Brazilian-Portuguese female neural voice), overridable via the environment.
5. On **any** exception during synthesis, the temp file is deleted (if it exists) and a `RuntimeError("Falha ao gerar áudio TTS: ...")` is raised.
6. On success, the path to the `.mp3` file is returned and stored in `st.session_state.audio_file`.

`app.py` deletes the temp audio file when the user clicks "Tentar novamente" (retry): it `os.remove`s `st.session_state.audio_file`, resets it to `None`, and reruns. Temp files therefore accumulate one-per-answer until the user retries or the process cleans `tmp/audio`.

## QR Code Sharing (qrcode)

`src/qrcode_service.py` wraps the [`qrcode`](https://pypi.org/project/qrcode/) library (installed with the `[pil]` extra). `generate_qr_code(data)` calls `qrcode.make(data)` to build a QR image, saves it as a PNG into an `io.BytesIO` buffer (`img.save(buf, format="PNG")`), seeks the buffer back to position 0, and returns the `BytesIO` — which `app.py` renders directly via `st.image(qr_img, width=150)`.

The encoded URL is the question's shareable link, derived from `APP_URL`: `app.py` constructs `f"{APP_URL}?q={question_id}"` and passes it to `generate_qr_code`. `APP_URL` defaults to `https://lappquiz.ict.unesp.br` and is overridable via the environment so the QR code points at the deployed host. Each question is an independent page addressed by its numeric `q` query parameter; the QR code lets students scan and open a specific question on a mobile device.

## Avatar Generation (Pillow / PIL)

`src/avatar.py` uses **Pillow** (imported as `PIL`) to draw a cartoon "professor" scientist programmatically — there are no pre-bundled character image assets. The avatar appears in two forms:

- **Talking** — `generate_talking_gif_bytes(audio_duration_seconds)` builds a multi-frame GIF at 10 FPS with the mouth animated via a `sin` wave and blinks every 10th frame. When an audio duration is supplied the frame count is matched to the audio length and the GIF plays once (`loop=1`); otherwise it defaults to 20 frames with an infinite loop.
- **Idle** — `generate_idle_gif_bytes()` builds a 48-frame, 6-second idle loop (mouth closed, occasional blink) with an infinite loop.

A single frame is drawn by `_draw_scientist_frame(mouth_open_factor, is_blinking, eye_offset)`, which composes hair, face, eyes, glasses, nose, mouth, and lab coat onto an `RGBA` canvas with `ImageDraw`. `TransparentGifConverter` converts each `RGBA` frame into a palette-mode (`P`) GIF with a transparency index (`info["transparency"] = 0`), so the avatar has a transparent background rather than a solid fill.

### Caching and inlining

The GIFs are **cached on disk** under `assets/`:

- `assets/scientist.gif` — the default talking GIF (20-frame infinite loop).
- `assets/scientist_idle.gif` — the idle GIF.

`get_talking_gif_base64(duration_seconds=0)` and `get_idle_gif_base64()` check the disk cache first; on a cache miss they `makedirs(ASSETS_DIR, exist_ok=True)`, generate the bytes, write the file, and then read it back. The duration-matched talking GIF (when `duration_seconds > 0`) is generated fresh each time and **not** cached — it is encoded to base64 directly. Both functions return base64 strings that `app.py` inlines into an HTML `<img>` element, with an `<audio>` element whose `onplay`/`onended` JavaScript handlers swap the image source between the talking and idle GIFs during playback.

## Streamlit Runtime

The entire UI is a single Streamlit app (`app.py`), run with `streamlit run app.py` (default port 8501). Streamlit provides:

- **`st.session_state`** — per-browser-tab state holding the loaded `questions`, the `answered` flag, `response_text`, the `audio_file` path, and the moderation warning count and block flag. There is no database or server-side persistence; closing the tab loses all progress.
- **`st.query_params`** — reads the `q` parameter to route to a specific question by numeric `id`.
- **`st.text_input` / `st.button` / `st.spinner` / `st.error` / `st.warning`** — the input and feedback widgets.
- **`st.image`** — renders the QR-code PNG.
- **`st.markdown(..., unsafe_allow_html=True)`** — injects CSS and the response HTML.
- **`streamlit.components.v1.html`** — inlines the avatar `<img>` + `<audio>` HTML block with the base64-encoded GIFs and MP3 so playback and the avatar swap happen client-side.

Streamlit auto-reloads on file changes in development. The app is a single page with no multi-page routing; each question is an independent view addressed by URL rather than sequential navigation. See [Architecture Overview](/openwiki/architecture.md) for the full session-state model and request pipeline.
