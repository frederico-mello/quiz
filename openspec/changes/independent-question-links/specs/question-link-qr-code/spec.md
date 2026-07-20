## ADDED Requirements

### Requirement: Generate QR code for question link

The system SHALL generate and display a QR code for the current question's shareable link.

#### Scenario: QR code displayed with question
- **WHEN** a question is loaded via `?q=<id>`
- **THEN** the system SHALL display a QR code encoding the full URL with the `?q=<id>` parameter

#### Scenario: QR code updates on different question
- **WHEN** the user loads a different question via `?q=<id2>`
- **THEN** the system SHALL display a QR code for the new question's link

### Requirement: Configurable app URL for QR codes

The system SHALL use a configurable base URL for generating QR code links.

#### Scenario: Default URL used
- **WHEN** no `APP_URL` environment variable is set
- **THEN** the system SHALL use `http://localhost:8501` as the base URL

#### Scenario: Custom URL used
- **WHEN** `APP_URL` environment variable is set to `https://quiz.example.com`
- **THEN** the system SHALL use `https://quiz.example.com` as the base URL for QR codes
