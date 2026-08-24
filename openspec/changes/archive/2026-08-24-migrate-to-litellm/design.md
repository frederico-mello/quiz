## Context

The current implementation uses direct OpenRouter API calls via LangChain's `ChatOpenAI` client, with a custom `extra_body` configuration to enable provider fallback between DeepInfra and Together. This approach couples the application directly to OpenRouter's ecosystem and complicates model switching or adding alternative providers.

The user has a LiteLLM server running at `http://200.145.92.242:4000` with Ollama backend and access to multiple models including `glm-4.7-flash:q4_K_M` (primary) and `nvidia/nemotron-3-nano-30b-a3b:nitro` (fallback on OpenRouter).

## Goals / Non-Goals

**Goals:**
- Migrate from direct OpenRouter integration to LiteLLM server as primary provider
- Implement automatic fallback to OpenRouter when LiteLLM fails
- Use lightweight, fast models for primary requests (`glm-4.7-flash:q4_K_M`)
- Maintain the same evaluation and feedback behavior (prompts, response cleaning, TTS)
- Keep existing configuration for moderation, TTS, and other features unchanged

**Non-Goals:**
- Modifying the prompt engineering or system messages
- Changing the content moderation flow or policies
- Implementing rate limiting, caching, or other advanced LiteLLM features (out of scope)
- Supporting additional fallback providers beyond OpenRouter
- Migrating test data or questions.json

## Decisions

### Primary LLM Model: `glm-4.7-flash:q4_K_M`

**Rationale:**
- Flash models are optimized for low latency and fast responses
- q4_K_M quantization reduces memory footprint while maintaining good quality
- 4.7B parameters offer a good balance between speed and response quality for educational chat
- Sufficiently smaller than alternatives (9B, 27B, 31B, 30B) for better performance

**Alternatives Considered:**
- `qwen3.5:9b`: Larger model with potentially better quality but slower
- `gemma4:12b`: Similar trade-off to qwen3.5:9b
- Larger models (27B, 31B): Better quality but significantly slower and more memory-intensive
- `nemotron-3.5-lightning:30b`: Fast but heavy, may not be ideal for primary requests

### Fallback Strategy: Try/Except with Two-Stage Retry

**Rationale:**
- Simple, well-understood pattern
- Clear separation of primary and fallback logic
- Easy to understand and debug
- Allows logging or monitoring of fallback events separately

**Alternatives Considered:**
- Single retry with model fallback in same provider: Complex, harder to reason about
- Parallel request: Over-engineered, increases costs and latency
- Circuit breaker pattern: Overkill for this use case

### Error Handling: Custom RuntimeError with Dual Failure Details

**Rationale:**
- Provides clear, actionable information to users and operators
- Preserves both failure details for debugging
- Follows Python's exception handling best practices
- Easy to test and validate

## Risks / Trade-offs

**Risk: LiteLLM Server Unavailability**

- **Impact**: If the LiteLLM server is down, the fallback will be used immediately
- **Mitigation**: OpenRouter fallback is well-established; fallback model is configured
- **Trade-off**: Primary request latency might increase if LiteLLM server is slow or unavailable

**Risk: API Key Management Complexity**

- **Impact**: Multiple API keys to manage (LiteLLM virtual key, OpenRouter key)
- **Mitigation**: Clear configuration via environment variables; documented in .env.example
- **Trade-off**: More environment variables to configure and document

**Risk: Latency Difference Between Providers**

- **Impact**: LiteLLM (Ollama) vs OpenRouter may have different response times
- **Mitigation**: Primary model selected for speed; fallback only used on failure
- **Trade-off**: Fallback requests may be slower than primary (acceptable given fallback scenario)

**Risk: Model Quality Differences**

- **Impact**: Primary (LiteLLM) vs Fallback (OpenRouter) may produce different response quality
- **Mitigation**: Primary model chosen for educational purposes; fallback available as last resort
- **Trade-off**: Users might notice slight differences in feedback style during fallbacks

## Environment Variables

### LiteLLM Configuration (Primary)

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `LITELLM_API_BASE_URL` | Yes | - | URL of LiteLLM server (http://200.145.92.242:4000) |
| `LITELLM_API_KEY` | Yes | - | Virtual key for LiteLLM server authentication |
| `LITELLM_MODEL` | Yes | - | Primary model to use (glm-4.7-flash:q4_K_M) |

### OpenRouter Configuration (Fallback)

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENROUTER_API_KEY` | Yes | - | OpenRouter API key for fallback |
| `OPENROUTER_BASE_URL` | No | https://openrouter.ai/api/v1 | OpenRouter API base URL |
| `OPENROUTER_FALLBACK_MODEL` | Yes | - | Fallback model (nvidia/nemotron-3-nano-30b-a3b:nitro) |

### Deprecated Variables (To Be Removed)

| Variable | Replacement |
|----------|-------------|
| `OPENROUTER_BASE_URL` (primary) | Replaced by `LITELLM_API_BASE_URL` |
| `LLM_MODEL` | Replaced by `LITELLM_MODEL` |
| `OPENROUTER_API_KEY` (primary context) | Replaced by `LITELLM_API_KEY` |

## Implementation Approach

### Code Changes

**`requirements.txt`:**
- Add `litellm` dependency (for fallback if needed, though not directly used)

**`src/config.py`:**
- Import environment variables for LiteLLM configuration
- Add `LITELLM_API_BASE_URL`, `LITELLM_API_KEY`, `LITELLM_MODEL`
- Keep `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `OPENROUTER_FALLBACK_MODEL` for fallback
- Deprecate `OPENROUTER_BASE_URL` (old primary context)

**`src/llm_service.py`:**
- Import `ChatOpenAI` from `langchain_openai`
- Create `get_litellm_llm()` function returning `ChatOpenAI` configured for LiteLLM
- Create `get_openrouter_fallback_llm()` function returning `ChatOpenAI` configured for OpenRouter
- Modify `evaluate_answer()` to use `get_litellm_llm()` with try/except and fallback to `get_openrouter_fallback_llm()`
- Keep `build_prompt()` and `clean_text_for_tts()` unchanged

**`.env.example`:**
- Update to show new environment variables
- Document breaking changes and migration path
- Include API key placeholders (not actual keys)

**`tests/test_llm_service.py`:**
- Update fixture to set new environment variables
- Mock `get_litellm_llm()` and `get_openrouter_fallback_llm()`
- Test fallback scenario: primary fails, fallback succeeds
- Test complete failure scenario: both fail
- Keep existing tests for `build_prompt()` and `clean_text_for_tts()`

### Migration Path

1. Update `.env` with new environment variables
2. Restart application
3. Test primary LLM functionality
4. Monitor for fallback events
5. Remove deprecated environment variables after successful migration