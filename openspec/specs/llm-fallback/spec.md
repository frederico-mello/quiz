## Purpose

Enables automatic fallback to a secondary LLM provider when the primary provider fails, ensuring continued service availability and graceful degradation under load or outages.

## Requirements

### Requirement: LLM fallback mechanism

The system SHALL have a primary LLM provider configured via LiteLLM server and a fallback provider via OpenRouter. When the primary fails, the system SHALL automatically retry using the fallback provider and return its response. If both fail, the system SHALL raise a custom error with details about both failures.

#### Scenario: Primary LLM succeeds
- **WHEN** the primary LiteLLM server successfully generates a response
- **THEN** the system SHALL return the response from the primary provider

#### Scenario: Primary LLM fails, fallback succeeds
- **WHEN** the primary LiteLLM server fails to generate a response
- **AND** the fallback OpenRouter provider succeeds
- **THEN** the system SHALL return the response from the fallback provider

#### Scenario: Both providers fail
- **WHEN** both the primary LiteLLM server and the fallback OpenRouter provider fail to generate a response
- **THEN** the system SHALL raise a `RuntimeError` containing details about both failures

### Requirement: Configurable fallback models

The system SHALL use a configurable primary model (`glm-4.7-flash:q4_K_M`) via LiteLLM and a configurable fallback model (`nvidia/nemotron-3-nano-30b-a3b:nitro`) via OpenRouter.

#### Scenario: Primary model specified
- **WHEN** the system is configured with a primary LiteLLM model
- **THEN** the system SHALL use that model for primary requests

#### Scenario: Fallback model specified
- **WHEN** the system is configured with a fallback OpenRouter model
- **THEN** the system SHALL use that model for fallback requests

### Requirement: Graceful degradation

The system SHALL handle provider failures transparently and continue operating with the fallback provider, maintaining the same user experience as before the migration.

#### Scenario: Transparent fallback
- **WHEN** a request fails on the primary provider
- **AND** the fallback succeeds
- **THEN** the user SHALL receive a response without noticing the provider switch (aside from potential latency difference)

#### Scenario: Clear error on complete failure
- **WHEN** both providers fail
- **THEN** the user SHALL see a clear error message indicating both providers failed
