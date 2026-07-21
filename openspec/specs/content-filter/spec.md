## Purpose

Defines how user-submitted answers are moderated for inappropriate content before evaluation. Uses a two-layer approach: local keyword/pattern matching (zero API cost) followed by optional LLM semantic moderation.

## Requirements

### Requirement: Content filter shall block local keywords and patterns

The system SHALL check user answers against a local set of blocked keywords and regex patterns, normalized for leet-speak obfuscation.

#### Scenario: Blocked keyword detected
- **WHEN** the user submits an answer containing a word from the blocked keyword set
- **THEN** the system SHALL block the answer and return a message identifying the detected term

#### Scenario: Blocked pattern detected
- **WHEN** the user submits an answer matching a blocked regex pattern
- **THEN** the system SHALL block the answer with a generic pattern-blocked message

#### Scenario: Leet-speak obfuscation normalized
- **WHEN** the user submits an answer with leet-speak characters (e.g., `f0d4` for `foda`)
- **THEN** the system SHALL normalize the text before keyword matching and block if matched

#### Scenario: Clean text passes local check
- **WHEN** the user submits an answer with no blocked keywords or patterns
- **THEN** the system SHALL pass the local check and proceed to LLM moderation (if enabled)

### Requirement: Content filter shall use LLM semantic moderation

The system SHALL optionally perform a second moderation pass using an LLM, aware of medical/dental context to avoid false positives.

#### Scenario: LLM blocks inappropriate content
- **WHEN** the LLM classifies the answer as "BLOQUEAR"
- **THEN** the system SHALL block the answer with a semantic moderation message

#### Scenario: LLM allows appropriate content
- **WHEN** the LLM classifies the answer as "SEGURO"
- **THEN** the system SHALL allow the answer to proceed to evaluation

#### Scenario: Medical context allowed
- **WHEN** the user submits a clinically accurate answer containing medical terms (e.g., "perfuração de crânio")
- **THEN** the system SHALL NOT block the answer due to medical context awareness

### Requirement: Content filter shall escalate warnings on repeated violations

The system SHALL track moderation violations per session and escalate warnings through three levels before blocking the session.

#### Scenario: First violation shows warning
- **WHEN** the user submits a blocked answer for the first time
- **THEN** the system SHALL display a first warning message

#### Scenario: Second violation shows final warning
- **WHEN** the user submits a blocked answer for the second time
- **THEN** the system SHALL display a second and final warning message

#### Scenario: Third violation blocks session
- **WHEN** the user submits a blocked answer for the third time
- **THEN** the system SHALL block the session and display a permanent block message

#### Scenario: Warning count resets on new session
- **WHEN** the user reloads the page or opens a new browser session
- **THEN** the moderation warning count SHALL reset to zero
