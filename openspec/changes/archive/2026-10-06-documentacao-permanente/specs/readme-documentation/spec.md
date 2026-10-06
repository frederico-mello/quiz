## MODIFIED Requirements

### Requirement: README links resolve to maintained documentation

The README SHALL link only to files or documentation pages that exist in the repository at their referenced paths. Links to detailed project documentation SHALL target the maintained documentation in `docs/` rather than the removed `openwiki/` directory.

#### Scenario: Contributor opens documentation links

GIVEN a contributor follows a documentation link from the README
WHEN the linked target is resolved
THEN the target exists at the referenced repository path
AND detailed project documentation links lead to maintained pages in `docs/`
