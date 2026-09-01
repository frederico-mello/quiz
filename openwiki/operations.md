---
type: Reference
title: Operations & Configuration
description: Environment variables, config validation, running locally vs deployed, APP_URL/QR sharing behavior, and the deprecated-variable migration path for the Quiz do Professor project.
tags: [operations, configuration, environment-variables, deployment, qr-code]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-01T12:56:02.391Z
sources:
  - id: openwiki-source-5f5b95b3d6a215fa02ceb945
    resource: repo://.env.example
  - id: openwiki-source-6d4b4e707b8d60b6ccfa3425
    resource: repo://.github/workflows/openwiki-update.yml
  - id: openwiki-source-17dded95897e01ee430228e3
    resource: repo://app.py
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-d502c275990c6476221bf080
    resource: repo://src/config.py
  - id: openwiki-source-e1a4d69bfefe5039cbbe03ea
    resource: repo://src/llm_service.py
  - id: openwiki-source-7e8ebb5fd2b205c019de32cc
    resource: repo://src/qrcode_service.py
  - id: openwiki-source-ffc42264d7caa035bb1f3478
    resource: repo://src/tts_service.py
  - id: openwiki-source-aee60addf228e6c9bf133836
    resource: repo://tests/test_app.py
  - id: openwiki-source-81af13fa7982f0b3becf1286
    resource: repo://tests/test_config.py
generated: { by: "openwiki/0.4.3", at: "2026-09-01T12:56:02.391Z" }
---

# Operations & Configuration

## Environment Setup

### Prerequisites
- Python 3.10+ (uses `type[...]` syntax, `list[...]` generics)
- pip
- A LiteLLM server reachable with a virtual API key (primary LLM provider)
- An [OpenRouter](https://openrouter.ai) API key (fallback LLM provider)
- Internet access for LLM evaluation and audio (TTS) generation

### Configuration

All runtime configuration is environment-based, loaded from a `.env` file at the project root via `dotenv.load_dotenv()` in `src/config.py`. `.env.example` is the canonical template.

#### Required variables

| Variable | Default | Notes |
|---|---|---|
| `LITELLM_API_BASE_URL` | — | URL of the LiteLLM server (primary provider), e.g. `http://localhost:4000` |
| `LITELLM_API_KEY` | — | Virtual authentication key for the LiteLLM server |
| `LITELLM_MODEL` | — | Primary model, e.g. `glm-4.7-flash:q4_K_M` |
| `OPENROUTER_API_KEY` | — | OpenRouter API key (used only for fallback) |
| `OPENROUTER_FALLBACK_MODEL` | — | Model used when the LiteLLM primary fails, e.g. `nvidia/nemotron-3-nano-30b-a3b:nitro` |

#### Optional variables

| Variable | Default | Notes |
|---|---|---|
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` | OpenRouter API base URL (fallback provider only) |
| `MODERATION_ENABLED` | `true` | Enables local content moderation when `true`; set to `false` to disable |
| `APP_URL` | `https://lappquiz.ict.unesp.br` | Base URL for shareable question links and QR codes |
| `TTS_VOICE` | `pt-BR-FranciscaNeural` | `edge-tts` voice identifier |
| `TEMP_AUDIO_DIR` | `tmp/audio` | Temporary directory for generated audio files (created if missing) |
| `SKIP_CONFIG_VALIDATION` | unset | Set to `1` to skip startup config validation |

### Config validation

`validate_config()` in `src/config.py` enforces that all required variables are present. It collects any missing variable (with its description) and raises a `ValueError` listing them, instructing the operator to copy `.env.example` to `.env` and fill in the values. Setting `SKIP_CONFIG_VALIDATION=1` makes the function return immediately without checking, so auxiliary tools and scripts can import `src.*` without a complete `.env`.

Validation is **not** performed at import time — `src.config` only reads the environment into module-level constants when imported. It is invoked explicitly at startup as the first call inside `app.main()`, before `st.set_page_config`, so a misconfigured deployment fails fast with a clear message rather than starting a half-functional Streamlit app. `app.py` additionally guards the OpenRouter key with an inline `st.error`/`return`, but that is a secondary UI check; `validate_config()` is the authoritative startup gate.

### Deprecated-variable migration

The configuration moved from OpenRouter as the primary LLM provider to a LiteLLM server as primary with OpenRouter as automatic fallback. The old variables were replaced:

| Old variable | Replaced by |
|---|---|
| `LLM_MODEL` | `LITELLM_MODEL` |
| `OPENROUTER_BASE_URL` (used as primary base URL) | `LITELLM_API_BASE_URL` (now `OPENROUTER_BASE_URL` is used only for the fallback) |
| `OPENROUTER_API_KEY` (used as the primary key) | `LITELLM_API_KEY` (the OpenRouter key is still used, but only for fallback) |

Migration path:

1. Set `LITELLM_API_BASE_URL`, `LITELLM_API_KEY`, and `LITELLM_MODEL` in `.env`.
2. Set `OPENROUTER_API_KEY` and `OPENROUTER_FALLBACK_MODEL` for the fallback.
3. Restart the application and test both the primary flow and the fallback.
4. Remove the old variables from `.env`.

### Setup steps

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env
# Edit .env: fill LITELLM_* (primary) and OPENROUTER_* (fallback)
streamlit run app.py
```

## Running the App

```bash
streamlit run app.py
```

- Default port: `8501` (open <http://localhost:8501>)
- `app.py` is the Streamlit entry point; the app is a single-page application driven by the `q` query parameter
- Streamlit auto-reloads on file changes in development

## Local vs Deployed: APP_URL and QR Sharing

Each question is an independent page addressed by its numeric `q` query parameter. `app.py` composes the shareable URL as `f"{APP_URL}?q={question_id}"` and passes it to `generate_qr_code()` in `src/qrcode_service.py`, which encodes the URL as a PNG and returns it as a `BytesIO` buffer. The QR code and link caption are rendered at the bottom of every question page.

`APP_URL` defaults to the public deployment `https://lappquiz.ict.unesp.br`, so QR codes and links point at the production host even when no environment override is set. To scan/open questions against a local server instead, set `APP_URL=http://localhost:8501` in `.env` (or any other reachable address). When publishing to a different host, set `APP_URL` to the user-accessible address. The QR generator intentionally performs no validation or normalization of `APP_URL`; operators are responsible for supplying an accessible URL.

## LLM Provider Configuration

`src/llm_service.py` builds two `ChatOpenAI` clients from the config constants:

- **Primary** (`get_litellm_llm()`): uses `LITELLM_MODEL`, `LITELLM_API_KEY`, and `LITELLM_API_BASE_URL` at `temperature=0.7`.
- **Fallback** (`get_openrouter_fallback_llm()`): uses `OPENROUTER_FALLBACK_MODEL`, `OPENROUTER_API_KEY`, and `OPENROUTER_BASE_URL` at `temperature=0.7`.

`evaluate_answer()` tries the primary LiteLLM client first. On any exception it logs a warning and retries the same prompt with the OpenRouter fallback. If both providers fail, it raises a `RuntimeError` containing both the primary and fallback error details. A successful response is passed through `clean_text_for_tts()` (strips markdown) before being returned for display and TTS.

See [LLM fallback](/openwiki/concepts/llm-fallback.md) for the full fallback control flow, and [Integrations](/openwiki/integrations.md) for the external service boundaries.

## Temporary Files

- Audio files are generated in `tmp/audio/` (gitignored) via `tempfile.mkstemp` with a `.mp3` suffix
- `generate_speech()` in `src/tts_service.py` creates `TEMP_AUDIO_DIR` if missing; on TTS failure it removes the temp file and raises `RuntimeError`
- On "Tentar novamente" the stored audio file is removed with `os.remove` (errors ignored) and the session is reset
- Avatar GIFs live in `assets/`

## CI/CD: OpenWiki Update Workflow

**File:** `.github/workflows/openwiki-update.yml`

- **Trigger:** Daily at 08:00 UTC (`cron: "0 8 * * *"`) plus manual `workflow_dispatch`
- **Action:** Installs OpenWiki globally (`npm install --global openwiki`), runs `openwiki code --update --print`
- **Output:** Creates a PR on branch `openwiki/update` with documentation changes (`openwiki`, `AGENTS.md`, `CLAUDE.md`, and the workflow file itself)
- **Model:** `z-ai/glm-5.2` via OpenRouter (`OPENWIKI_PROVIDER=openrouter`, `OPENWIKI_MODEL_ID=z-ai/glm-5.2`)
- **Tracing:** LangSmith integration (`LANGCHAIN_PROJECT=openwiki`, `LANGCHAIN_TRACING_V2=true`)

**Required secrets:**
- `OPENROUTER_API_KEY` — for LLM calls during doc generation
- `LANGSMITH_API_KEY` — for LangSmith tracing (optional but configured)

## OpenSpec Workflow

The repo uses [OpenSpec](https://github.com/nicholasgriffintn/openspec) for structured, AI-assisted change management.

### Commands (`.opencode/commands/`)
| Command | Purpose |
|---|---|
| `opsx-explore` | Explore codebase for a proposed change |
| `opsx-propose` | Create a change proposal |
| `opsx-apply` | Apply a proposed change |
| `opsx-archive` | Archive a completed change |
| `opsx-sync` | Sync delta specs |

### Skills (`.opencode/skills/`)
Mirror the commands with detailed skill definitions. Also present under `.github/skills/` for GitHub Copilot integration.

### Config
`openspec/config.yaml` uses `schema: spec-driven` with minimal configuration. Active specs in `openspec/specs/` cover avatar, content-filter, independent-question-access, llm-evaluation, question-link-qr-code, quiz-ui, and tts. Archived changes live in `openspec/changes/archive/`.

## Graphify Plugin

The repo has a [Graphify](https://github.com/nicholasgriffintn/graphify) code knowledge graph plugin configured in `.opencode/plugins/graphify.js`.

Per `AGENTS.md`:
- Run `graphify query "<question>"` for codebase questions
- Run `graphify path "<A>" "<B>"` for relationship queries
- Run `graphify explain "<concept>"` for focused explanations
- Run `graphify update .` after code changes (AST-only, no API cost)
- Graph output lives in `graphify-out/` (gitignored except for tracking)

## Focused Tests

- `tests/test_config.py` — verifies `APP_URL` resolves to the public default `https://lappquiz.ict.unesp.br` when unset, and to the environment override (e.g. `https://quiz.example.com`) when set.
- `tests/test_app.py` — stubs `streamlit` and all `src.*` submodules in `sys.modules`, reloads `app`, and runs `main()` with a fake `_Streamlit`; captures the URL passed to `generate_qr_code` and asserts it is `https://lappquiz.ict.unesp.br?q=7` with `APP_URL` unset and `https://quiz.example.com?q=7` with a custom `APP_URL`.
