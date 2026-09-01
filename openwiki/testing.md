---
type: Reference
title: Testing
description: Pytest configuration, the mocking strategy (heavy Streamlit and src.* stubbing in test_app), shared fixtures, coverage of the LLM fallback and moderation contracts, the GitHub Actions CI workflow, and known test gaps.
tags: [testing, pytest, mocking, streamlit, llm-fallback, moderation, ci, fixtures, conftest]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-01T12:56:02.391Z
sources:
  - id: openwiki-source-4f2678f93d3fd3835f9f2909
    resource: repo://.github/workflows/test.yml
  - id: openwiki-source-e44eab9a26f9187df819fc2a
    resource: repo://pytest.ini
  - id: openwiki-source-042e05bb663605d09adced3b
    resource: repo://requirements-dev.txt
  - id: openwiki-source-373640cd8a0886cee69db282
    resource: repo://requirements.txt
  - id: openwiki-source-ffc42264d7caa035bb1f3478
    resource: repo://src/tts_service.py
  - id: openwiki-source-f0a6e7dc03522b2682f88655
    resource: repo://tests/conftest.py
  - id: openwiki-source-aee60addf228e6c9bf133836
    resource: repo://tests/test_app.py
  - id: openwiki-source-81af13fa7982f0b3becf1286
    resource: repo://tests/test_config.py
  - id: openwiki-source-ba50025ec5b6ebd5f9b58bad
    resource: repo://tests/test_content_filter.py
  - id: openwiki-source-fbe25e08bbf3954904783586
    resource: repo://tests/test_llm_service.py
  - id: openwiki-source-3d628365f6d719c1775b459f
    resource: repo://tests/test_qrcode_service.py
  - id: openwiki-source-cc6c1b1335786951088356a5
    resource: repo://tests/test_quiz_data.py
generated: { by: "openwiki/0.4.3", at: "2026-09-01T12:56:02.391Z" }
---

# Testing

## Current State

An automated pytest suite lives under `tests/`, and a GitHub Actions workflow (`.github/workflows/test.yml`) runs it on pushes to `main` and on pull requests against `main`. The suite is intentionally unit-oriented: it exercises the pure modules (`quiz_data`, `qrcode_service`, `content_filter`, `llm_service`) directly, and it drives the Streamlit entry point (`app.py`) through a hand-rolled fake Streamlit rather than a real render. Behavior that the stubs bypass — real LLM/TTS/network calls, the avatar GIF pipeline, and a live Streamlit DOM — is covered by the manual checklist below instead.

## Pytest configuration

`pytest.ini` configures the suite:

```ini
[pytest]
testpaths = tests
pythonpath = src
addopts = -ra --strict-markers
```

- `testpaths = tests` scopes collection to the `tests/` directory.
- `pythonpath = src` makes `import src.*` resolve without an install step, so the tests import the application modules directly from the source tree.
- `addopts = -ra --strict-markers` prints a summary of all skipped and non-passing outcomes and errors on any unregistered marker, catching misspelled `@pytest.mark.*` decorator names at collection time.

The development dependency is just `pytest>=8.0` (`requirements-dev.txt`); the runtime dependencies in `requirements.txt` (`streamlit`, `langchain`, `langchain-openai`, `openai`, `edge-tts`, `python-dotenv`, `qrcode[pil]`) must also be installed because the tests import the modules under test.

## CI workflow

`.github/workflows/test.yml` runs the suite on `ubuntu-latest` with Python **3.10**, installing both `requirements.txt` and `requirements-dev.txt` (using `--only-binary=:all:`) before running `pytest`:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.10"
- name: Install production and development dependencies
  run: pip install --only-binary=:all: -r requirements.txt -r requirements-dev.txt
- name: Run pytest
  run: pytest
```

It triggers on `push` to `main` and on `pull_request` against `main`, with `permissions: contents: read`.

## Shared fixtures (`conftest.py`)

`tests/conftest.py` provides three fixtures that the rest of the suite depends on:

- **`_required_llm_env` (autouse)** — runs for every test without being requested. It sets `SKIP_CONFIG_VALIDATION=1` so `src.config.validate_config()` becomes a no-op (the suite has no real `.env`), and it fills in the five required LLM environment variables with test values (`LITELLM_API_BASE_URL`, `LITELLM_API_KEY`, `LITELLM_MODEL`, `OPENROUTER_API_KEY`, `OPENROUTER_FALLBACK_MODEL`) but **only when they are unset** — it preserves any value a test has already set via `monkeypatch.setenv`. Because `src.config` reads its constants at import time, tests that need to override config reload the module with `importlib.reload` after the fixture has populated the environment.
- **`sample_questions`** — returns a three-element list of `{"id", "question", "correct_answer"}` dicts used by the `quiz_data` parametrized tests.
- **`tmp_json_file`** — a factory that writes arbitrary JSON to a `tmp_path` file (default `data.json`) and returns the path, used to feed `load_questions` from an isolated temp directory.

## Mocking strategy in `test_app.py`

`app.py` imports Streamlit (`st`, `streamlit.components.v1`) and every `src.*` module at module load time. To run `main()` in a test without a Streamlit server or any of the heavy dependencies, `test_app.py` does not import the real collaborators — it **replaces them in `sys.modules`** before importing `app`.

`_load_app(monkeypatch)` performs the stubbing in a fixed sequence:

1. Reloads `src.config` so its constants reflect the test environment.
2. Builds fresh `types.ModuleType` instances for `streamlit`, `streamlit.components`, and `streamlit.components.v1`, links them into the package hierarchy (`streamlit_module.components = components_module; components_module.v1 = components_v1_module`), and installs each into `sys.modules` via `monkeypatch.setitem`. This makes `import streamlit` and `import streamlit.components.v1` resolve to the empty stubs.
3. Builds stub modules for each `src.*` collaborator and installs them into `sys.modules`:
   - `src.qrcode_service.generate_qr_code` → `lambda url: BytesIO()`
   - `src.avatar.get_idle_gif_base64` / `get_talking_gif_base64` → `lambda: ""`
   - `src.content_filter.check_text` → `lambda text: (False, None)`; `get_warning_level` → `lambda warnings: "none"`
   - `src.llm_service.evaluate_answer` → `lambda question, correct_answer, user_answer: ""`
   - `src.quiz_data.get_question_by_id` → a real linear-scan lookup over the passed `questions`; `load_questions` → `lambda: []`
   - `src.tts_service.generate_speech` → `lambda text: None`
4. Imports `app` (which now binds its top-level `st`/`src.*` names to the stubs) and reloads it so the stubs take effect.

`_run_app_and_capture_qr_urls(monkeypatch)` then instantiates a `_Streamlit` fake and runs `app.main()` with it. The fake `_Streamlit`:

- Holds a `_SessionState` (a `dict` subclass with `__getattr__`/`__setattr__`) preloaded with a single question (`id=7`), `answered=True`, a `response_text`, and `audio_file=None`, plus `query_params = {"q": "7"}`.
- Implements `set_page_config`, `markdown`, `title`, `columns` (returns three `_Column` context managers), `button` (returns `False`), `image`, and `caption` as no-ops or trivial returns.

The helper monkeypatches `app.st` with the fake and `app.generate_qr_code` with a spy that appends each URL it receives to a list and returns a `BytesIO`, so the two tests can assert exactly which share URLs were generated. The two parametrized cases pin the QR link behavior:

- **`test_qr_link_uses_public_default_when_app_url_is_unset`** — with `APP_URL` deleted, `main()` builds `https://lappquiz.ict.unesp.br?q=7`, matching the `APP_URL` default in `src/config.py`.
- **`test_qr_link_uses_custom_app_url`** — with `APP_URL=https://quiz.example.com`, `main()` builds `https://quiz.example.com?q=7`.

Because the stubs short-circuit `check_text`, `evaluate_answer`, `generate_speech`, and the avatar GIF calls, these tests exercise only the QR-link construction path of `main()`; they do **not** validate the real moderation, LLM, TTS, or avatar behavior (those are covered by the dedicated module tests, and the gaps are listed below).

`tests/test_config.py` mirrors the same approach at the config level: it reloads `src.config` under env overrides to assert `APP_URL` defaults to `https://lappquiz.ict.unesp.br` and honors an `APP_URL` override.

## `test_content_filter.py` coverage

This file pins each layer of the two-tier moderation system in `src/content_filter.py` and its fail-open contract. The checks are exercised against the real `BLOCKED_KEYWORDS` set and `BLOCKED_PATTERNS` regexes (no stubbing of the filter itself):

- **Keyword blocking** — `test_check_keywords_pt_sexual_term_is_blocked` and `test_check_keywords_clean_text_returns_false` pin the blocked/clean return tuple `(bool, Optional[str])`; `test_check_keywords_blocks_term_in_each_category` parametrizes one term from each of the four categories (`pt-sexual`, `pt-violent`, `en-sexual`, `en-violent`) and asserts each is blocked with the term quoted in the message.
- **Leet normalization** — `test_normalize_leet_lowercases_input` (`FODA → foda`), `test_normalize_leet_applies_digit_translation_table` (`4 → 3`, `3 → 8` from the `str.maketrans("aeiou43", "aeiou38")` table), and `test_check_keywords_leet_normalization_detects_blocked_word` confirm an uppercased blocked term is still caught after normalization.
- **Pattern blocking** — `test_check_patterns_blocks_matching_pattern` (`porra` → `"Conteúdo contém padrão bloqueado."`) and `test_check_patterns_clean_text_returns_none` (`olá mundo` → `None`).
- **Local composition** — `test_check_text_local_*` pin the keyword-then-pattern ordering: a blocked keyword short-circuits before patterns run, a keyword-clean/pattern-blocked input returns the pattern message, and a fully clean input returns `(False, None)`.
- **Warning escalation** — `test_get_warning_level_escalates_per_count` parametrizes the `0→none, 1→first, 2→second, 3→blocked` ladder that `app.py` uses to drive the three-strike session escalation.
- **LLM pass** — `test_check_text_llm_blocks_mocked_llm_classification` confirms a `"BLOQUEAR"` response yields `(True, "Conteúdo impróprio identificado pela moderação semântica.")`; `test_check_text_skips_llm_when_text_is_blocked_locally` confirms the LLM is never called once the local check already blocked; `test_check_text_invokes_llm_once_for_clean_text` confirms the LLM is called exactly once with the real `get_litellm_llm` for clean text; `test_check_text_returns_clean_when_llm_raises` confirms the **fail-open** contract (an LLM exception returns `(False, None)`); `test_check_text_skips_llm_when_disabled` confirms `use_llm=False` never invokes the LLM.

See the [Content Moderation System](/openwiki/concepts/content-moderation.md) concept for the full moderation contract these tests pin.

## `test_llm_service.py` coverage

This file pins the two-tier LLM fallback in `src/llm_service.py` by mocking `ChatOpenAI` at the `get_litellm_llm`/`get_openrouter_fallback_llm` boundary (a `llm_service` fixture reloads the module with test env vars). A `create_llm_mock(response_content)` helper builds a `MagicMock` whose `invoke` returns an object with `.content`:

- **`build_prompt`** — `test_build_prompt_contains_question_correct_answer_and_user_answer` asserts all three inputs appear in the formatted prompt; `test_build_prompt_marks_blank_user_answer_as_unanswered` asserts a blank user answer is rendered as the literal `(sem resposta)`.
- **`clean_text_for_tts`** — `test_clean_text_for_tts_removes_markdown_and_normalizes_whitespace` asserts that `**Correto!** Veja [este link](https://example.com)\n\n## _Mais_   \`detalhes\` ~~agora~~` cleans to `Correto! Veja este link. Mais detalhes agora` (markdown stripped, link reduced to its label, double-newline collapsed to `. `, strikethrough/backticks removed, whitespace collapsed).
- **`evaluate_answer`** — three tests pin the three legs of the fallback contract:
  - `test_evaluate_answer_uses_litellm` — the primary is invoked once with the exact built prompt, the fallback constructor is never called, and the return equals `clean_text_for_tts` of the primary's content.
  - `test_evaluate_answer_uses_fallback_when_primary_fails` — when the primary raises, the fallback is constructed and invoked, and its cleaned content is returned.
  - `test_evaluate_answer_raises_on_both_failures` — when both providers raise, a `RuntimeError` is raised whose message contains `ambos os provedores falharam` plus both the primary (`LiteLLM indisponível`) and fallback (`OpenRouter indisponível`) error strings.

See the [LLM Provider Fallback](/openwiki/concepts/llm-fallback.md) concept for the full provider-chain and total-failure contract.

## Other unit tests

- **`test_qrcode_service.py`** — `test_generate_qr_code_returns_bytesio_with_png_signature` asserts `generate_qr_code` returns an `io.BytesIO` whose first 8 bytes are the PNG signature (`\x89PNG\r\n\x1a\n`), exercising the real `qrcode` library.
- **`test_quiz_data.py`** — covers `load_questions` (valid JSON via `tmp_json_file`; invalid JSON raises `json.JSONDecodeError`), `get_question` (valid index returns the question; negative and out-of-range indices return `None`), and `get_question_by_id` (existing id returns the question; missing/zero/out-of-range ids return `None`), using the `sample_questions` fixture and parametrized indices.

## Known gaps

The stubs in `test_app.py` deliberately bypass the collaborators that need network or heavy resources, so several behaviors have **no automated integration coverage**:

| Gap | Why untested | Recommendation |
|---|---|---|
| `tts_service.generate_speech` end-to-end | Calls the real `edge-tts` network API and writes to `tmp/audio/`; the `test_app` stub replaces `generate_speech` with a no-op. | Add a network-mocked or recorded integration test for `generate_speech` (success path + the `RuntimeError("Falha ao gerar áudio TTS: ...")` failure path). |
| Avatar GIF generation (`src/avatar.py`) | `test_app` stubs `get_idle_gif_base64`/`get_talking_gif_base64` to return `""`; no test exercises the PIL drawing, `TransparentGifConverter`, or the on-disk cache at `assets/scientist*.gif`. | Add tests for `generate_idle_gif_bytes`/`generate_talking_gif_bytes` and the disk-caching behavior. |
| Full Streamlit render / answer pipeline | `test_app` uses a fake `_Streamlit`; the moderation escalation, `_process_answer`, audio-visual sync HTML, and "Tentar novamente" reset are not asserted against a real Streamlit component tree. | Add Streamlit component/integration tests (e.g. `streamlit-app testing` or AppTest) covering the submit → moderation → evaluate → TTS → playback flow. |
| `test_app` stubs bypass real moderation/LLM/TTS/avatar | The `check_text`, `evaluate_answer`, `generate_speech`, and avatar stubs short-circuit the real logic, so `test_app` validates only QR-link construction. | Rely on the dedicated module tests for those contracts; consider wiring the real modules (with network mocks) for at least one integration test. |
| No type checking | No `mypy`/`pyright` configuration. | Add a type-checking step to CI. |
| No linting | No `ruff`/`flake8` in CI. | Add a lint step to CI. |

## Manual Testing Checklist

Use this checklist to cover behavior not exercised by the automated suite.

### Core Quiz Flow
- [ ] App loads without errors at `http://localhost:8501`
- [ ] No `?q=` param → info message about using `?q=<id>` links
- [ ] `?q=1` → first question displays correctly
- [ ] Invalid `?q=abc` → "ID da pergunta inválido" error
- [ ] Non-existent `?q=999` → "Pergunta não encontrada" error
- [ ] Submitting empty answer shows warning
- [ ] Submitting a correct answer → LLM response displays
- [ ] Submitting an incorrect answer → LLM response with feedback displays
- [ ] Audio plays automatically after evaluation
- [ ] Avatar switches from idle to talking during audio playback
- [ ] Avatar returns to idle when audio ends
- [ ] "Tentar novamente" resets to unanswered state
- [ ] QR code displays at bottom of question page
- [ ] QR code encodes the correct shareable URL

### Content Moderation (with `MODERATION_ENABLED=true`)
- [ ] Typing a blocked keyword → warning message appears
- [ ] Second violation → "segunda advertência" warning
- [ ] Third violation → session blocked, must reload
- [ ] Typing a medical term (e.g., "cirurgia") → not blocked
- [ ] LLM semantic moderation runs after local check passes

### Content Moderation (with `MODERATION_ENABLED=false`)
- [ ] All answers pass through without moderation
- [ ] No moderation warnings displayed

### Avatar System
- [ ] `assets/scientist.gif` generated on first run
- [ ] `assets/scientist_idle.gif` generated on first run
- [ ] GIFs loaded from cache on subsequent runs
- [ ] Talking animation syncs with audio duration

### TTS
- [ ] Audio file generated in `tmp/audio/`
- [ ] Audio cleaned up on "Tentar novamente"
- [ ] Fallback warning if TTS fails

### Configuration
- [ ] Missing `.env` → Streamlit error message about missing API key
- [ ] Invalid API key → LLM call fails with error
- [ ] Custom `LLM_MODEL` respected
- [ ] Custom `TTS_VOICE` respected

## Relationships

- The moderation tests pin the contract documented in [Content Moderation System](/openwiki/concepts/content-moderation.md); the LLM tests pin [LLM Provider Fallback](/openwiki/concepts/llm-fallback.md).
- The `test_app` stubbing strategy and `conftest` fixtures are referenced from the [Source Map](/openwiki/source-map.md); see the [Quickstart](/openwiki/quickstart.md) for local install and `.env` setup.
- The CI workflow and the `pytest.ini` configuration are described in [Operations](/openwiki/operations.md) alongside the other `.github/workflows` pipelines.
