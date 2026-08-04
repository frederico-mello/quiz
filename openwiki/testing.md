---
type: "Reference"
title: "Testing"
description: "Manual and automated testing guidance, known issues, and test gaps for the Quiz do Professor app."
---

# Testing

## Current State

An automated pytest suite lives under `tests/`, and a GitHub Actions workflow (`.github/workflows/test.yml`) runs it on pushes to `main` and on pull requests against `main`. Use the checklist below to cover behavior not exercised by the automated suite.

### Running the Suite

```bash
pip install -r requirements.txt -r requirements-dev.txt   # pytest>=8.0
pytest                       # discover tests/, addopts from pytest.ini
```

`pytest.ini` sets `testpaths = tests`, `pythonpath = src`, and `addopts = -ra --strict-markers`, so `src.*` imports resolve without extra configuration. See [Source Map](source-map.md) for the modules under test.

### Automated Test Inventory

| Test file | Module under test | Coverage focus |
|---|---|---|
| `tests/test_content_filter.py` | `src/content_filter.py` | Keyword/pattern blocking, leet normalization, LLM moderation path, `get_warning_level` escalation |
| `tests/test_llm_service.py` | `src/llm_service.py` | `build_prompt` content (incl. blank-answer marking), `clean_text_for_tts` markdown stripping, `evaluate_answer` orchestration via mocked LLM |
| `tests/test_qrcode_service.py` | `src/qrcode_service.py` | `generate_qr_code` returns `BytesIO` with PNG signature |
| `tests/test_quiz_data.py` | `src/quiz_data.py` | JSON load (valid/invalid), `get_question` index bounds, `get_question_by_id` lookup |

Shared fixtures (`sample_questions`, `tmp_json_file`) live in `tests/conftest.py`. LLM tests inject a fake `OPENROUTER_API_KEY` via `monkeypatch` and mock the LangChain `ChatOpenAI` instance so no network calls are made.

## Manual Testing Checklist

Use this checklist to cover behavior not exercised by the automated suite:

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

## Gaps and Recommendations

| Gap | Priority | Recommendation |
|---|---|---|
| No integration tests | Medium | Add Streamlit component tests for the quiz flow |
| No type checking | Low | Add mypy or pyright configuration |
| No linting | Low | Add ruff or flake8 to CI |
