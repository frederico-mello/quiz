---
type: "Reference"
title: "Testing"
description: "Manual testing guidance, known issues, and test gaps for the Quiz do Professor app — no automated test suite exists yet."
---

# Testing

## Current State

**There is no automated test suite.** The repository has no test files, no test framework configured, and no CI step that runs tests. All validation is manual.

## Manual Testing Checklist

Since there are no automated tests, use this checklist when making changes:

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
| No unit tests | High | Add pytest tests for `content_filter.py`, `quiz_data.py`, `llm_service.py` (mock LLM), `qrcode_service.py` |
| No integration tests | Medium | Add Streamlit component tests for the quiz flow |
| No CI test step | Medium | Add GitHub Actions job to run pytest on push |
| No type checking | Low | Add mypy or pyright configuration |
| No linting | Low | Add ruff or flake8 to CI |
