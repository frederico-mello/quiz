## 1. CI workflow runs pytest on push to main and on pull requests against main

- [x] 1.1 Create `.github/workflows/test.yml` declaring triggers for pushes to `main` and for pull requests targeting `main`, with a `test` job running on `ubuntu-latest`, setting up Python 3.10, installing `requirements.txt` and `requirements-dev.txt`, and invoking `pytest`
- [x] 1.2 Verify the workflow file parses as valid YAML and that its parsed structure contains the expected triggers (`push.branches=[main]`, `pull_request.branches=[main]`), the `test` job, and the required steps (checkout, setup-python, pip install of both requirement files, pytest)
- [x] 1.3 Verify that files referenced by the workflow exist at the repo root (`pytest.ini`, `requirements-dev.txt`) and that the `tests/` directory is present
- [ ] 1.4 Open the PR against `main` and confirm GitHub Actions detects the workflow on the PR and that `pytest` runs to completion

> **Cross-PR dependency:** tasks 1.3 and 1.4 cannot be marked complete on this branch alone. `pytest.ini`, `requirements-dev.txt`, and `tests/` are owned by PR #61. They will exist on `main` once #61 is merged; task 1.3 then passes automatically, and task 1.4 verifies on the resulting GitHub Actions run. PR sequencing: #61 → main → rebase #63 → push → CI confirmation.

## 2. openwiki/testing.md reflects that automated test suite and CI exist

- [x] 2.1 Update the file's frontmatter description so it no longer implies the absence of an automated test suite
- [x] 2.2 Remove the "No CI test step" row from the gaps table and adjust any surrounding prose that referenced that gap
- [x] 2.3 Verify the markdown file remains well-formed: frontmatter intact, no orphan references, surrounding sections still consistent with the updated frontmatter
