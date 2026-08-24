## 1. Update Dependencies

- [x] 1.1 Add `litellm` to `requirements.txt` for fallback capability
- [x] 1.2 Update `langchain-openai` constraint to ensure compatibility with `chat-openai` client patterns

**Verification:** Run `pip install -r requirements.txt` succeeds without errors

## 2. Update Environment Configuration

- [x] 2.1 Update `.env.example` with new environment variables:
  - `LITELLM_API_BASE_URL="http://200.145.92.242:4000"`
  - `LITELLM_API_KEY` (placeholder for virtual key)
  - `LITELLM_MODEL="glm-4.7-flash:q4_K_M"`
  - `OPENROUTER_API_KEY` (placeholder for OpenRouter key)
  - `OPENROUTER_FALLBACK_MODEL="nvidia/nemotron-3-nano-30b-a3b:nitro"`
  - `OPENROUTER_BASE_URL` (default: `https://openrouter.ai/api/v1`)
- [x] 2.2 Document deprecated variables and migration path in `.env.example`
- [x] 2.3 Add validation for missing required environment variables in `src/config.py`
- [x] 2.4 Update `src/config.py` to import new configuration variables
- [x] 2.5 Remove old variable imports (`OPENROUTER_BASE_URL` for primary context, `LLM_MODEL`)

**Verification:** Check `.env.example` contains all required new variables with proper documentation

## 3. Modify LLM Service

- [x] 3.1 Update `src/llm_service.py` imports to include `SecretStr` from `pydantic`
- [x] 3.2 Create `get_litellm_llm()` function:
  - Uses `ChatOpenAI` with `base_url` from `LITELLM_API_BASE_URL`
  - Uses `api_key` from `LITELLM_API_KEY`
  - Uses `model` from `LITELLM_MODEL`
  - Sets `temperature=0.7`
- [x] 3.3 Create `get_openrouter_fallback_llm()` function:
  - Uses `ChatOpenAI` with `base_url` from `OPENROUTER_BASE_URL`
  - Uses `api_key` from `OPENROUTER_API_KEY`
  - Uses `model` from `OPENROUTER_FALLBACK_MODEL`
  - Sets `temperature=0.7`
- [x] 3.4 Modify `evaluate_answer()` function:
  - Call `get_litellm_llm()` to get primary LLM
  - Try `invoke()` with built prompt
  - If exception occurs, call `get_openrouter_fallback_llm()` for fallback
  - Return cleaned response from successful provider
  - If both fail, raise `RuntimeError` with both errors
- [x] 3.5 Keep `build_prompt()` function unchanged
- [x] 3.6 Keep `clean_text_for_tts()` function unchanged

**Verification:** Run Streamlit app and verify `evaluate_answer()` uses new functions

## 4. Update Tests

- [x] 4.1 Update test fixture in `tests/test_llm_service.py`:
  - Set new environment variables in `llm_service` fixture
- [x] 4.2 Add test for primary LLM invocation: `test_evaluate_answer_uses_litellm()`
  - Mock `get_litellm_llm()` to return a successful response
  - Verify `evaluate_answer()` uses the primary LLM
- [x] 4.3 Add test for fallback scenario: `test_evaluate_answer_uses_fallback_when_primary_fails()`
  - Mock primary LLM to raise an exception
  - Mock fallback LLM to return a successful response
  - Verify `evaluate_answer()` returns the fallback response
- [x] 4.4 Add test for complete failure: `test_evaluate_answer_raises_on_both_failures()`
  - Mock both primary and fallback LLMs to raise exceptions
  - Verify `evaluate_answer()` raises `RuntimeError` with details
- [x] 4.5 Ensure existing tests for `build_prompt()` and `clean_text_for_tts()` still pass

**Verification:** Run `pytest tests/test_llm_service.py` - all tests pass

## 5. Integration Testing

- [x] 5.1 Restart Streamlit application with new environment variables
- [x] 5.2 Submit a test question and verify primary LLM (LiteLLM) responds correctly
- [x] 5.3 Simulate primary LLM failure and verify fallback to OpenRouter works
- [x] 5.4 Verify response text is properly cleaned for TTS (markdown removed, whitespace normalized)
- [x] 5.5 Verify moderation system continues to work with fallback LLM
- [x] 5.6 Verify audio generation works with new responses

**Verification:** User can successfully submit questions and receive responses with fallback working

## 6. Documentation Updates

- [x] 6.1 Update `README.md` "Configuração" section with new environment variables
- [x] 6.2 Document migration path from old to new configuration in README
- [x] 6.3 Add architecture diagram showing LiteLLM primary with OpenRouter fallback (optional, can be in openwiki)

**Verification:** README.md accurately documents new configuration process

## 7. Cleanup

- [x] 7.1 Remove deprecated environment variables from `.env` (only if user confirms)
- [x] 7.2 Remove old variable imports from `src/config.py`
- [x] 7.3 Verify all tests still pass after cleanup

**Verification:** After cleanup, running `streamlit run app.py` succeeds and all tests pass

## 8. Final Verification

- [x] 8.1 Run full test suite: `pytest tests/`
- [x] 8.2 Verify no linting or formatting issues with `ruff check .` (if used)
- [x] 8.3 Confirm all OpenSpec artifacts are in sync
- [x] 8.4 Test graceful degradation: temporarily disable LiteLLM server and verify OpenRouter fallback
- [x] 8.5 Verify prompt language and behavior remain in Portuguese Brazilian

**Verification:** All tests pass, fallback works, documentation is complete