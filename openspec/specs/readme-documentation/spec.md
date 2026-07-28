## Purpose

Document current project setup, structure, capabilities, and maintained documentation links.

## Requirements

### Requirement: README provides current setup guidance

The project SHALL provide a README that documents current prerequisites, installation, configuration, and application startup instructions.

#### Scenario: New contributor follows setup instructions

GIVEN a contributor has cloned the repository
WHEN the contributor follows the README from prerequisites through startup
THEN the README provides all commands and required configuration needed to start the application

#### Scenario: Configuration variables are documented

GIVEN the application depends on environment variables
WHEN a contributor reads the README configuration section
THEN each required and relevant optional variable is listed with its purpose and default when applicable
AND `APP_URL` is identified as the base URL for shareable question links

### Requirement: README reflects repository structure and resources

The README SHALL describe the main project resources and top-level structure without claiming files or features that are absent from the repository.

#### Scenario: Contributor uses the structure overview

GIVEN a contributor needs to locate an application component
WHEN the contributor reads the README structure section
THEN the section identifies the current entry point and principal source directories or files

#### Scenario: README describes current capabilities

GIVEN a contributor reads the project overview
WHEN the contributor reviews the listed resources
THEN the resources correspond to functionality currently represented by the project
BUT the README does not introduce undocumented application behavior

### Requirement: README links resolve to maintained documentation

The README SHALL link only to files or documentation pages that exist in the repository at their referenced paths.

#### Scenario: Contributor opens documentation links

GIVEN a contributor follows a link from the README
WHEN the linked target is resolved
THEN the target exists at the referenced repository path

#### Scenario: Documentation target is maintained in OpenWiki

GIVEN detailed guidance is maintained in an existing OpenWiki page
WHEN the README references that guidance
THEN the README links to the existing OpenWiki path
AND the README does not duplicate the detailed operational content
