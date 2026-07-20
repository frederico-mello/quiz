## Purpose

Defines how the professor avatar is programmatically drawn using PIL, animated as talking and idle GIFs, and served as base64-encoded inline images.

## Requirements

### Requirement: Avatar shall be drawn programmatically

The system SHALL draw a cartoon scientist character using PIL primitives (ellipses, polygons, arcs) without external image assets.

#### Scenario: Avatar frame renders with all features
- **WHEN** a frame is drawn with `mouth_open_factor=0` and `is_blinking=False`
- **THEN** the frame SHALL contain hair, face, eyes, glasses, nose, mouth, and coat

#### Scenario: Mouth opens proportionally
- **WHEN** `mouth_open_factor` is between 0 and 1
- **THEN** the mouth SHALL be drawn open with height proportional to the factor

#### Scenario: Eyes close on blink
- **WHEN** `is_blinking=True`
- **THEN** the eyes SHALL be drawn as horizontal lines instead of ellipses

### Requirement: Avatar shall generate talking GIF

The system SHALL generate a multi-frame talking animation GIF with mouth movement synced to audio duration.

#### Scenario: Talking GIF generated with audio duration
- **WHEN** `generate_talking_gif_bytes(audio_duration_seconds)` is called with a positive duration
- **THEN** the GIF SHALL have enough frames to cover the audio duration at 10 FPS and loop once

#### Scenario: Default talking GIF without duration
- **WHEN** `generate_talking_gif_bytes()` is called with no duration
- **THEN** the GIF SHALL have 20 frames and loop infinitely

### Requirement: Avatar shall generate idle GIF

The system SHALL generate a looping idle animation GIF with occasional blinks.

#### Scenario: Idle GIF generated
- **WHEN** `generate_idle_gif_bytes()` is called
- **THEN** the GIF SHALL have 48 frames at 125ms each (6-second cycle) and loop infinitely

#### Scenario: Idle GIF includes blinks
- **WHEN** the idle GIF plays
- **THEN** the avatar SHALL blink approximately every 4 seconds

### Requirement: Avatar shall cache GIFs to disk

The system SHALL cache generated GIFs to disk as base64 and serve them on subsequent runs without regeneration.

#### Scenario: Talking GIF cached on first call
- **WHEN** `get_talking_gif_base64()` is called for the first time
- **THEN** the GIF SHALL be generated and saved to `assets/scientist.gif`

#### Scenario: Cached GIF served on subsequent calls
- **WHEN** `get_talking_gif_base64()` is called and `assets/scientist.gif` exists
- **THEN** the system SHALL read the cached file and return its base64 encoding

#### Scenario: Idle GIF cached on first call
- **WHEN** `get_idle_gif_base64()` is called for the first time
- **THEN** the GIF SHALL be generated and saved to `assets/scientist_idle.gif`
