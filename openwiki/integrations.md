# Integrations

## External APIs

### OpenRouter
- **Purpose:** LLM proxy providing access to multiple model providers
- **Used by:** `src/llm_service.py`, `src/content_filter.py`
- **Auth:** `OPENROUTER_API_KEY` env var
- **Base URL:** `https://openrouter.ai/api/v1` (OpenAI-compatible)
- **Model:** `deepseek/deepseek-v4-flash` (configurable)
- **Provider routing:** Prefers DeepInfra, falls back to Together (`extra_body.provider`)
- **Usage:** Answer evaluation (temp 0.7), content moderation (temp 0.1)
- **Docs:** [openrouter.ai/docs](https://openrouter.ai/docs)

### edge-tts (Microsoft Edge Text-to-Speech)
- **Purpose:** Free TTS service for Portuguese speech synthesis
- **Used by:** `src/tts_service.py`
- **Auth:** None required (free service)
- **Voice:** `pt-BR-FranciscaNeural` (Brazilian Portuguese female)
- **Output:** MP3 files via async `edge_tts.Communicate`
- **Note:** Uses Microsoft's Edge TTS endpoints; no API key needed but depends on Microsoft service availability
- **PyPI:** [edge-tts](https://pypi.org/project/edge-tts/)

---

## Python Libraries

### Streamlit
- **Version:** `>=1.30.0`
- **Purpose:** Web UI framework — single-file app pattern
- **Usage:** `st.session_state` for state management, `st.markdown` for HTML rendering, `components.html` for inline JS/audio
- **Key pattern:** All UI and orchestration in `app.py:main()`

### LangChain
- **Version:** `>=0.2.0` (core) + `>=0.1.0` (openai)
- **Purpose:** LLM orchestration and prompt management
- **Usage:** `ChatOpenAI` for LLM calls, `ChatPromptTemplate` for prompt construction
- **Integration:** LangChain is also used in the OpenWiki CI workflow for tracing via LangSmith

### Pillow (PIL)
- **Purpose:** Image manipulation for avatar generation
- **Usage:** Drawing scientist avatar frames, GIF generation with transparency
- **Not in requirements.txt:** Installed as a transitive dependency of Streamlit

### mutagen
- **Version:** `>=1.47.0`
- **Purpose:** Audio file metadata reading
- **Usage:** `MP3(filepath).info.length` for getting audio duration
- **Note:** `get_audio_duration()` exists in `tts_service.py` but is not currently called by `app.py`

---

## Developer Tooling

### OpenSpec
- **Purpose:** Structured AI-assisted change management
- **Config:** `openspec/config.yaml` (spec-driven schema)
- **Commands:** `opsx-explore`, `opsx-propose`, `opsx-apply`, `opsx-archive`, `opsx-sync`
- **Skills:** Mirrored under `.opencode/skills/` and `.github/skills/`
- **Integration:** Works with both OpenCode (`.opencode/`) and GitHub Copilot (`.github/prompts/`)

### OpenWiki
- **Purpose:** Automated code documentation generation
- **CI:** `.github/workflows/openwiki-update.yml` — daily scheduled run
- **Model:** `z-ai/glm-5.2` via OpenRouter
- **Output:** PRs on `openwiki/update` branch updating `openwiki/` directory
- **Tracing:** LangSmith integration for observability

### Graphify
- **Purpose:** Code knowledge graph for AI-assisted codebase navigation
- **Plugin:** `.opencode/plugins/graphify.js`
- **Output:** `graphify-out/` directory with graph data
- **Usage:** `graphify query`, `graphify path`, `graphify explain`, `graphify update`

### Codacy
- **Config:** `.codacy/` directory exists (gitignored config)
- **Note:** Minimal integration; codacy instructions file is gitignored

---

## CI/CD

### GitHub Actions
Single workflow: `.github/workflows/openwiki-update.yml`

```yaml
Triggers: schedule (daily 08:00 UTC) + workflow_dispatch
Steps:
  1. Checkout
  2. Setup Node.js 22
  3. npm install -g openwiki
  4. openwiki code --update --print
  5. Create PR via peter-evans/create-pull-request
```

**Required secrets:**
- `OPENROUTER_API_KEY`
- `LANGSMITH_API_KEY`

**PR branch:** `openwiki/update`
**Commit message:** `docs: update OpenWiki`

---

## Streamlit Cloud / Deployment

No deployment configuration exists (no `Dockerfile`, `Procfile`, `streamlit.toml`, or cloud config). The app is currently run locally only. To deploy to Streamlit Cloud:

1. Push repo to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Set `OPENROUTER_API_KEY` in Streamlit Cloud secrets
4. Entry point: `app.py`
