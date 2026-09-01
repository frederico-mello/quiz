---
okf_version: "0.2"
---

# Files

- [Architecture Overview](architecture.md) - System overview, component map, Streamlit session-state model, and the end-to-end data flow from question display through moderation, two-tier LLM evaluation, TTS, and avatar playback for the Quiz do Professor app.
- [External Integrations](integrations.md) - Runtime external services and Python libraries the Quiz do Professor app depends on — LiteLLM/Ollama and OpenRouter LLM endpoints via LangChain ChatOpenAI, edge-tts speech synthesis, qrcode sharing, PIL avatar generation, and the Streamlit runtime.
- [Operations & Configuration](operations.md) - Environment variables, config validation, running locally vs deployed, APP_URL/QR sharing behavior, and the deprecated-variable migration path for the Quiz do Professor project.
- [Quiz do Professor — Quickstart](quickstart.md) - Entry point for the Quiz do Professor code wiki. Tech stack, run steps, environment, and a task-routing map that points engineers to the right page for each kind of change.
- [Source Map](source-map.md) - File-by-file reference for the Quiz do Professor codebase, covering app.py, the src/ modules and their public functions, config, tests, and the openspec feature specs.
- [Testing](testing.md) - Pytest configuration, the mocking strategy (heavy Streamlit and src.* stubbing in test_app), shared fixtures, coverage of the LLM fallback and moderation contracts, the GitHub Actions CI workflow, and known test gaps.

# Directories

- [concepts](concepts/)
- [workflows](workflows/)
