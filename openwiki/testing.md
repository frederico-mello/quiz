# Testing

## Current State

**There is no automated test suite.** The repository has no test files, no test framework configured, and no CI step that runs tests. All validation is manual.

## Known Bugs

### ZeroDivisionError — Score Statistics
**File:** `app.py`, lines 112-116

```python
# BUG: current_index is 0-based, causing ZeroDivisionError on first question
avg_score_pct = (
    st.session_state.get("total_score", 0) / st.session_state.current_index
) * 100
```

This overwrites the safe calculation on lines 109-111 that uses `max(1, current_index)`. On the first question (`current_index == 0`), this throws `ZeroDivisionError`.

**Impact:** App crashes when rendering the first question's score display. The error appears as a Streamlit exception in the UI.

**Fix:** Delete lines 113-115 (the duplicate unsafe block).

## Manual Testing Checklist

Since there are no automated tests, use this checklist when making changes:

### Core Quiz Flow
- [ ] App loads without errors at `http://localhost:8501`
- [ ] First question displays correctly
- [ ] Submitting empty answer shows warning
- [ ] Submitting a correct answer → LLM response displays
- [ ] Submitting an incorrect answer → LLM response with feedback displays
- [ ] Audio plays automatically after evaluation
- [ ] Avatar switches from idle to talking during audio playback
- [ ] Avatar returns to idle when audio ends
- [ ] "Tentar novamente" resets to unanswered state
- [ ] "Próxima pergunta" advances to next question
- [ ] Last question → completion screen with "Recomeçar" button
- [ ] Score statistics display (after first question)

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
- [ ] Audio cleaned up on "Próxima pergunta"
- [ ] Fallback warning if TTS fails

### Configuration
- [ ] Missing `.env` → Streamlit error message about missing API key
- [ ] Invalid API key → LLM call fails with error
- [ ] Custom `LLM_MODEL` respected
- [ ] Custom `TTS_VOICE` respected

## Gaps and Recommendations

| Gap | Priority | Recommendation |
|---|---|---|
| No unit tests | High | Add pytest tests for `content_filter.py`, `quiz_data.py`, `llm_service.py` (mock LLM) |
| No integration tests | Medium | Add Streamlit component tests for the quiz flow |
| No CI test step | Medium | Add GitHub Actions job to run pytest on push |
| No type checking | Low | Add mypy or pyright configuration |
| No linting | Low | Add ruff or flake8 to CI |
| ZeroDivisionError bug | High | Fix lines 113-115 in `app.py` |
