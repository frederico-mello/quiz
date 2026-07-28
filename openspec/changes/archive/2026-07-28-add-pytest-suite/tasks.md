## 1. qrcode_service coverage with pytest infrastructure setup

- [x] 1.1 Create `tests/` directory with empty `__init__.py` and `conftest.py` containing shared fixtures needed by the suite (such as a sample questions list and a tmp-file factory for JSON loading)
- [x] 1.2 Create `pytest.ini` at repo root with `testpaths = tests`, `pythonpath = src`, `addopts = -ra --strict-markers`
- [x] 1.3 Create `requirements-dev.txt` at repo root listing `pytest>=8.0`
- [x] 1.4 Implement `tests/test_qrcode_service.py` covering the spec scenario for `generate_qr_code` (returns `BytesIO` with PNG signature bytes for arbitrary data)
- [x] 1.5 Run `pytest tests/test_qrcode_service.py` and verify it passes

## 2. quiz_data coverage

- [x] 2.1 Implement `tests/test_quiz_data.py` covering `load_questions` (returns list from valid JSON, raises on invalid JSON), `get_question` (valid index returns question, negative index returns None, out-of-bounds index returns None), and `get_question_by_id` (existing id returns question, missing id returns None)
- [x] 2.2 Run `pytest tests/test_quiz_data.py` and verify it passes

## 3. content_filter pure-function coverage

- [x] 3.1 Implement `tests/test_content_filter.py` covering `normalize_leet` (mapping and lowercase behavior), `check_keywords` (PT sexual block, PT violent block, EN sexual block, EN violent block, clean text passes), `check_patterns` (regex block returns generic message, clean text returns None), `check_text_local` (combines both), and `get_warning_level` (0/1/2/≥3 states)
- [x] 3.2 Run `pytest tests/test_content_filter.py` excluding the `check_text_llm` and `check_text` scenarios and verify it passes

## 4. llm_service coverage with mocked LLM

- [x] 4.1 Implement `tests/test_llm_service.py` covering `build_prompt` (formatted prompt contains question, correct answer, and user answer; empty user_answer is marked as `(sem resposta)`), `clean_text_for_tts` (markdown markers removed, markdown links stripped, multiple newlines collapsed, multiple spaces collapsed), and `evaluate_answer` (invokes mocked `get_llm` with the prompt produced by `build_prompt`, returns text passed through `clean_text_for_tts`)
- [x] 4.2 Add a scenario verifying that `evaluate_answer` propagates exceptions from the mocked LLM (current behavior: no silent capture)
- [x] 4.3 Run `pytest tests/test_llm_service.py` and verify it passes without network access

## 5. content_filter LLM-orchestration coverage

- [x] 5.1 Extend `tests/test_content_filter.py` with a `check_text_llm` scenario (mocked LLM returning "BLOQUEAR" produces a semantic block message)
- [x] 5.2 Extend `tests/test_content_filter.py` with `check_text` scenarios (text blocked locally returns without invoking the LLM mock; clean text with `use_llm=True` invokes the LLM mock once; clean text with `use_llm=False` returns `(False, None)` without invoking the LLM mock)
- [x] 5.3 Run `pytest tests/test_content_filter.py` and verify the entire file passes

## 6. Full suite isolation validation

- [x] 6.1 Run `pytest` from repo root with `OPENROUTER_API_KEY` unset and verify all tests across the four test files pass
- [x] 6.2 Run `pytest -v` and confirm no test references network resources or real credentials
