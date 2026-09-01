# Files

- [Content Moderation System](content-moderation.md) - How user answers are moderated before evaluation — a local PT+EN keyword/regex blocklist with leet-speak normalization, an optional LLM semantic pass with a dental/medical context exception, and a three-strike session warning escalation.
- [LLM Provider Fallback](llm-fallback.md) - The two-tier LLM architecture in src/llm_service.py — a primary LiteLLM server (Ollama backend) with an OpenRouter fallback, the grading prompt, TTS-oriented response cleaning, and total-failure behavior.
