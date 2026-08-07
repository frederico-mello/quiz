## MODIFIED Requirements

### Requirement: Configurable app URL for QR codes

The system SHALL use a configurable base URL for generating QR code links.

#### Scenario: Default URL used
- **GIVEN** no `APP_URL` environment variable is set
- **WHEN** a QR code link is generated for a question
- **THEN** the system SHALL use `https://lappquiz.ict.unesp.br` as the base URL

#### Scenario: Custom URL used
- **GIVEN** `APP_URL` is set to `https://quiz.example.com`
- **WHEN** a QR code link is generated for a question
- **THEN** the system SHALL use `https://quiz.example.com` as the base URL for QR codes
