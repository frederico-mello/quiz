---
type: "Reference"
title: "Quiz do Professor — Quickstart"
description: "Entry point for the Quiz do Professor code wiki. Interactive dental/medical quiz with Streamlit, LangChain, edge-tts, and QR code question sharing."
---

# Quiz do Professor — Quickstart

An interactive quiz application for dental/medical students built with **Streamlit**, **LangChain**, and **edge-tts**. A cartoon "professor" avatar evaluates answers using an LLM (via OpenRouter) and reads feedback aloud via text-to-speech.

**Language:** Brazilian Portuguese (pt-BR). All UI text, questions, and LLM prompts are in Portuguese.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (single-page app, URL query-param routing) |
| LLM | OpenRouter API → DeepSeek v4 Flash (via LangChain) |
| TTS | edge-tts (`pt-BR-FranciscaNeural`) |
| Avatar | Programmatic PIL-drawn scientist GIF, cached to disk |
| Moderation | Local keyword blocklist + LLM semantic check |
| QR Sharing | `qrcode` library generates scannable question links |
| Config | python-dotenv (`.env` file) |

## Quick Start

```bash
# 1. Clone and enter the repo
git clone <repo-url> && cd quiz

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
# Edit .env and add your OPENROUTER_API_KEY

# 5. Run
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Key Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | *required* | OpenRouter API key for LLM calls |
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` | API base URL |
| `LLM_MODEL` | `deepseek/deepseek-v4-flash` | Model identifier |
| `MODERATION_ENABLED` | `true` | Enable content moderation |
| `APP_URL` | `http://localhost:8501` | Base URL for QR code question links |
| `TTS_VOICE` | `pt-BR-FranciscaNeural` | edge-tts voice |
| `TEMP_AUDIO_DIR` | `tmp/audio` | Temp directory for generated audio |

See [.env.example](/.env.example) for the template.

## Documentation Map

| Page | What it covers |
|---|---|
| [Architecture](architecture.md) | Component diagram, data flow, session state model |
| [Source Map](source-map.md) | File-by-file reference with key functions |
| [Workflows](workflows.md) | Quiz answer pipeline, moderation, avatar generation |
| [Operations](operations.md) | Config, deployment, CI/CD, OpenSpec/OpenWiki tooling |
| [Testing](testing.md) | Known bugs, manual test guidance, test gaps |
| [Integrations](integrations.md) | External services and developer tooling |

## Repository Structure (Top Level)

```
quiz/
├── app.py                    # Streamlit entrypoint
├── questions.json            # Quiz question bank (5 items)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── assets/                   # Generated/cached avatar GIFs
├── src/                      # Application modules
│   ├── avatar.py             # PIL-based scientist avatar
│   ├── config.py             # Environment config loader
│   ├── content_filter.py     # Two-layer moderation
│   ├── llm_service.py        # LangChain + OpenRouter LLM
│   ├── qrcode_service.py     # QR code generation for question sharing
│   ├── quiz_data.py          # Question JSON loader
│   └── tts_service.py        # edge-tts wrapper
├── openspec/                 # OpenSpec change management
├── .opencode/                # OpenCode commands/skills
├── .github/                  # CI workflow + OpenSpec prompts
└── openwiki/                 # This documentation
```

## Backlog

| Area | Source | Reason deferred |
|---|---|---|
| Automated testing | No test files exist | No test framework or test files present in the repo |
| Question content management | `questions.json` (5 items) | No admin interface; questions are manually edited JSON |
| User authentication | `app.py` session state | No auth layer; relies on Streamlit's anonymous sessions |
| Database persistence | `app.py` session state only | All state is in-memory Streamlit session; no DB |
| Multi-language support | Hardcoded pt-BR | All UI, prompts, and content are Portuguese-only |
