## Purpose

Defines how a single question is accessed, answered, and reviewed via a stable link, independent of a quiz sequence.

## Requirements

### Requirement: Access question by ID via query parameter

The system SHALL accept a `?q=<id>` query parameter in the URL to load a specific question by its `id` field from `questions.json`.

#### Scenario: Valid question ID provided
- **WHEN** the URL contains `?q=3` and question with `id: 3` exists in `questions.json`
- **THEN** the system SHALL display only that question

#### Scenario: No query parameter
- **WHEN** the URL contains no `?q` parameter
- **THEN** the system SHALL display a friendly message asking the user to select a question

#### Scenario: Invalid question ID
- **WHEN** the URL contains `?q=999` and no question with that ID exists
- **THEN** the system SHALL display a friendly error message "Pergunta não encontrada"

#### Scenario: Non-numeric ID
- **WHEN** the URL contains `?q=abc`
- **THEN** the system SHALL display a friendly error message about invalid ID format

### Requirement: Single question experience

The system SHALL display only the question identified by the query parameter, without navigation to other questions.

#### Scenario: No navigation controls shown
- **WHEN** a question is loaded via `?q=<id>`
- **THEN** the system SHALL NOT show "Próxima pergunta" or progress bar

#### Scenario: Try again available
- **WHEN** a question is loaded via `?q=<id>` and the user has answered
- **THEN** the system SHALL show a "Tentar novamente" button to reset the answer

### Requirement: Session-scoped response

The system SHALL keep the user's answer, AI feedback, and audio available only during the current session.

#### Scenario: Response persists on rerun
- **WHEN** the user answers a question and the app reruns
- **THEN** the system SHALL still display the response text and audio

#### Scenario: Response lost on new session
- **WHEN** the user opens the same link in a new browser session
- **THEN** the system SHALL show the question unanswered
