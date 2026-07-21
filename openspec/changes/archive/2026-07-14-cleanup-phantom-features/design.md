## Context

The quiz app has three pieces of dead or broken code that are vestiges of abandoned experiments:

1. **Score display** (`app.py:108-116`): A "Pontuação média" caption that computes `total_score / current_index`. `total_score` is never initialized or accumulated — it always resolves to 0 via `.get(..., 0)`. On the first question (`current_index == 0`), this causes a `ZeroDivisionError`. On subsequent questions, it silently shows "0.0%" forever. The scoring feature was never built: `evaluate_answer()` returns only text feedback, and the LLM prompt never requests a numeric score.

2. **`shuffle_questions()`** (`src/quiz_data.py:16-19`): Copies and shuffles a question list. Never called. Questions always appear in JSON file order.

3. **`get_audio_duration()`** (`src/tts_service.py:29-31`): Returns MP3 duration via `mutagen`. Never called. The gif sync (talking ↔ idle) is handled client-side by the browser's `<audio>` `onended` event (`app.py:226`), making server-side duration measurement obsolete.

## Goals / Non-Goals

**Goals:**
- Remove the broken score display so the app no longer crashes on Q1
- Remove unused `shuffle_questions()` and its `random` import
- Remove unused `get_audio_duration()`, its `mutagen` import, and the `mutagen` dependency from `requirements.txt`
- Keep the app functionally identical in all other respects

**Non-Goals:**
- Building a real scoring feature
- Adding tests (separate concern, though this cleanup makes testing easier)
- Adding question shuffling
- Any other refactoring or feature work

## Decisions

### Remove score display entirely (not fix the division)

**Chosen:** Delete the `avg_score_pct` block and "Pontuação média" caption.

**Alternatives considered:**
- *Fix the division with `max(1, ...)`*: The safe version already exists at lines 109-111 but is overwritten by the unsafe version at 113-115. Deleting the unsafe lines would prevent the crash, but the display would still show permanent "0.0%" — misleading and dishonest. Since scoring was never built, removing the display is the honest choice.
- *Build scoring properly*: Requires extracting a numeric score from the LLM (structured output, regex parse, or separate scoring call), initializing `total_score` in session state, and accumulating it. Out of scope — the user confirmed scoring was an experiment, not a desired feature.

### Remove dead functions and their imports

**Chosen:** Delete `shuffle_questions()` + `random` import, and `get_audio_duration()` + `mutagen` import + `mutagen` from `requirements.txt`.

**Rationale:**
- `shuffle_questions()` is the only consumer of `import random` in `quiz_data.py` — both go together.
- `get_audio_duration()` is the only consumer of `from mutagen.mp3 import MP3` in the entire codebase — both go together.
- `mutagen` appears only in `requirements.txt` and `src/tts_service.py:5` — removing both eliminates the dependency.

## Risks / Trade-offs

- **[Risk] Someone later wants question shuffling** → Mitigation: `shuffle_questions()` is trivial to re-implement (3 lines) and preserved in git history.
- **[Risk] Someone later wants audio duration** → Mitigation: same — trivial to restore from git. The current approach (client-side JS events) is the correct one anyway.
- **[Trade-off] Removing `mutagen`** → Saves a dependency with no downside; `mutagen` is only used by the dead function.
