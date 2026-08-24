## Why

Migrate from direct OpenRouter integration to LiteLLM server with Ollama backend, enabling flexible model selection, improved reliability through fallback mechanisms, and centralized API key management.

## What Changes

- Replace direct OpenRouter API calls with LiteLLM server integration
- Add OpenRouter as a fallback provider for resilience
- Configure primary LLM model as `glm-4.7-flash:q4_K_M` (efficient, fast) via LiteLLM/Ollama
- Configure fallback LLM model as `nvidia/nemotron-3-nano-30b-a3b:nitro` via OpenRouter
- Update environment variable configuration (add new vars, remove deprecated ones)
- Modify `src/llm_service.py` to use LiteLLM client with retry logic
- Update tests to reflect new configuration and fallback behavior

**BREAKING**: Old environment variables `OPENROUTER_API_KEY`, `LLM_MODEL`, and `OPENROUTER_BASE_URL` are deprecated and replaced by `LITELLM_API_KEY`, `LITELLM_MODEL`, `LITELLM_API_BASE_URL`, `OPENROUTER_API_KEY` (fallback), `OPENROUTER_FALLBACK_MODEL`, and `OPENROUTER_BASE_URL` (fallback).

## Capabilities

### New Capabilities

- `llm-fallback`: Automatic fallback to secondary LLM provider when primary fails, ensuring continued availability and graceful degradation

### Modified Capabilities

- `llm-evaluation`: LLM evaluation now uses LiteLLM as primary provider with OpenRouter fallback, replacing direct OpenRouter integration