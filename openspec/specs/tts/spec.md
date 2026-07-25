## Purpose

Defines how text-to-speech audio is generated from LLM evaluation text using edge-tts (Microsoft Edge TTS engine).

## Requirements

### Requirement: TTS shall generate MP3 from text

The system SHALL convert text to speech using edge-tts with a configurable voice and save the result as an MP3 file.

#### Scenario: Speech generated successfully
- **WHEN** the system receives evaluation text and a voice is configured
- **THEN** the system SHALL generate an MP3 file at the configured temp directory

#### Scenario: Default voice used
- **WHEN** no custom voice is configured
- **THEN** the system SHALL use `pt-BR-FranciscaNeural` as the default voice

### Requirement: TTS shall handle generation failures

The system SHALL clean up temp files and raise an error if speech generation fails.

#### Scenario: Temp file cleaned on failure
- **WHEN** speech generation fails partway through
- **THEN** the system SHALL remove any partially created temp file and raise a `RuntimeError`
