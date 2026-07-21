## Purpose

Defines the behavior of the quiz user interface — how questions are presented, how feedback is shown, and how the avatar animation is synchronized with audio playback.

## Requirements

### Requirement: Quiz UI shall not display score average
The quiz user interface SHALL present questions and feedback without displaying a score average, since numeric scoring is not implemented.

#### Scenario: First question renders without crash
- **WHEN** the user starts a new quiz session and the first question is displayed
- **THEN** the page renders without a `ZeroDivisionError` and no "Pontuação média" caption is shown

#### Scenario: Subsequent questions render without score display
- **WHEN** the user advances to any question beyond the first
- **THEN** the page renders without a "Pontuação média" caption

### Requirement: Quiz UI shall not show progress indicator
The quiz SHALL NOT display a "Pergunta X de Y" progress indicator, since questions are accessed individually by link.

#### Scenario: No progress text shown
- **WHEN** a question is loaded via `?q=<id>`
- **THEN** the system SHALL NOT display "Pergunta X de Y" progress text

### Requirement: Quiz UI shall sync avatar gif via client-side audio events
The quiz SHALL use the browser's `<audio>` `onplay` and `onended` events to switch the avatar gif between talking and idle states, without server-side duration measurement.

#### Scenario: Avatar switches to talking on audio play
- **WHEN** the audio element starts playing
- **THEN** the avatar gif switches to the talking animation

#### Scenario: Avatar switches to idle on audio end
- **WHEN** the audio element finishes playing
- **THEN** the avatar gif switches to the idle animation
