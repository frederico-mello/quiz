## Purpose

Defines how the LLM evaluates user answers against correct answers, generates feedback, and cleans output for text-to-speech consumption.

## Requirements

### Requirement: LLM shall evaluate answers via OpenRouter

The system SHALL use the LiteLLM server (Ollama backend) as the primary LLM provider and OpenRouter as the fallback provider, with configurable models for each.

#### Scenario: Answer evaluated successfully
- **WHEN** the user submits an answer and the primary LiteLLM provider responds
- **THEN** the system SHALL return a feedback text evaluating the answer

#### Scenario: Primary provider failure
- **WHEN** the primary LiteLLM provider fails
- **THEN** the system SHALL fall back to the OpenRouter provider and return its response

### Requirement: LLM shall format feedback for spoken output

The system SHALL clean LLM output by removing markdown formatting, links, and excessive whitespace, producing text suitable for TTS.

#### Scenario: Markdown stripped from response
- **WHEN** the LLM returns text containing `*bold*`, `# headers`, or `_italic_`
- **THEN** the system SHALL remove all markdown formatting characters

#### Scenario: Links converted to text
- **WHEN** the LLM returns text containing markdown links `[text](url)`
- **THEN** the system SHALL replace them with just the link text

#### Scenario: Whitespace normalized
- **WHEN** the LLM returns text with multiple newlines or extra spaces
- **THEN** the system SHALL collapse whitespace into single spaces

### Requirement: LLM shall handle inappropriate answers

The system SHALL instruct the LLM to refuse evaluation of sexual, violent, or offensive content and redirect the user to maintain respect.

#### Scenario: Inappropriate answer refused
- **WHEN** the user submits an inappropriate answer that passes content moderation
- **THEN** the LLM SHALL refuse to evaluate it and redirect the user to maintain respect
