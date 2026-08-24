## MODIFIED Requirements

### Requirement: LLM shall evaluate answers via OpenRouter

The system SHALL use the LiteLLM server (Ollama backend) as the primary LLM provider and OpenRouter as the fallback provider, with configurable models for each.

#### Scenario: Answer evaluated successfully
- **WHEN** the user submits an answer and the primary LiteLLM provider responds
- **THEN** the system SHALL return a feedback text evaluating the answer

#### Scenario: Primary provider failure
- **WHEN** the primary LiteLLM provider fails
- **THEN** the system SHALL fall back to the OpenRouter provider and return its response
