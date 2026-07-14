# Operations

## Environment Setup

### Prerequisites
- Python 3.10+ (uses `type[...]` syntax, `list[...]` generics)
- pip
- An OpenRouter API key ([openrouter.ai](https://openrouter.ai))

### Configuration

All runtime config is environment-based via `.env` file. See `.env.example` for the template.

| Variable | Required | Default | Notes |
|---|---|---|---|
| `OPENROUTER_API_KEY` | Yes | — | OpenRouter API key for LLM calls |
| `OPENROUTER_BASE_URL` | No | `https://openrouter.ai/api/v1` | Override for proxy/self-hosted |
| `LLM_MODEL` | No | `deepseek/deepseek-v4-flash` | Must be available on OpenRouter |
| `MODERATION_ENABLED` | No | `true` | Set to `false` to disable content filtering |
| `TTS_VOICE` | No | `pt-BR-FranciscaNeural` | edge-tts voice identifier |
| `TEMP_AUDIO_DIR` | No | `tmp/audio` | Created automatically if missing |

### Setup Steps

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
# Edit .env: add your OPENROUTER_API_KEY
streamlit run app.py
```

## Running the App

```bash
streamlit run app.py
```

- Default port: `8501`
- Streamlit auto-reloads on file changes in development
- The app is a single-page application; no routing or multi-page setup

## Temporary Files

- Audio files are generated in `tmp/audio/` (gitignored)
- Each answer generates one `.mp3` file via `tempfile.mkstemp`
- Files are cleaned up when navigating to next question or retrying
- Avatar GIFs are cached in `assets/` (gitignored via `tmp/` pattern, but `assets/*.gif` files are tracked in git)

## Known Issues

### ZeroDivisionError in Score Statistics
**Location:** `app.py` lines 112-116

The safe calculation (line 109-111) is immediately overwritten by an unsafe version (lines 113-115) that divides by `current_index` when it's 0. This crashes on the first question.

**Workaround:** Answer at least one question before the crash manifests (the safe code runs first, then the unsafe overwrite triggers on the same render).

**Fix:** Remove lines 113-115 (the duplicate unsafe calculation).

## CI/CD: OpenWiki Update Workflow

**File:** `.github/workflows/openwiki-update.yml`

- **Trigger:** Daily at 08:00 UTC + manual `workflow_dispatch`
- **Action:** Installs OpenWiki globally, runs `openwiki code --update --print`
- **Output:** Creates a PR on branch `openwiki/update` with documentation changes
- **Model:** `z-ai/glm-5.2` via OpenRouter
- **Tracing:** LangSmith integration for observability

**Required secrets:**
- `OPENROUTER_API_KEY` — for LLM calls during doc generation
- `LANGSMITH_API_KEY` — for LangSmith tracing (optional but configured)

## OpenSpec Workflow

The repo uses [OpenSpec](https://github.com/nicholasgriffintn/openspec) for structured change management via AI-assisted commands.

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
`openspec/config.yaml` uses `schema: spec-driven` with minimal configuration. No active specs in `openspec/specs/`; archived changes in `openspec/changes/archive/`.

## Graphify Plugin

The repo has a [Graphify](https://github.com/nicholasgriffintn/graphify) code knowledge graph plugin configured in `.opencode/plugins/graphify.js`.

Per `AGENTS.md`:
- Run `graphify query "<question>"` for codebase questions
- Run `graphify path "<A>" "<B>"` for relationship queries
- Run `graphify explain "<concept>"` for focused explanations
- Run `graphify update .` after code changes (AST-only, no API cost)
- Graph output lives in `graphify-out/` (gitignored except for tracking)
