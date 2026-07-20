## Why

The quiz app carries residue from an abandoned scoring experiment: a broken score display that crashes on the first question (`ZeroDivisionError`), and two unused functions (`shuffle_questions`, `get_audio_duration`) that are vestiges of features or approaches that were never completed. The scoring feature was never built — `total_score` is never accumulated, and `evaluate_answer()` returns only text — so the display is both broken and dishonest. Removing this residue makes the app stable and the code honest about what it actually does.

## What Changes

- **Remove the phantom score display** from `app.py`: delete the `avg_score_pct` computation block and the "Pontuação média" caption that crashes on Q1 and shows permanent 0.0% thereafter
- **Remove `shuffle_questions()`** from `src/quiz_data.py`: unused function that was intended for question randomization but never wired in
- **Remove `get_audio_duration()`** from `src/tts_service.py`: unused function superseded by client-side JS `onended` event for gif sync; also remove the `mutagen` import that only exists to support it
- **Remove `mutagen` from dependencies** if no other code uses it

## Capabilities

### New Capabilities
- `quiz-ui`: Specifies the quiz user interface behavior — the quiz shall present questions and feedback without displaying a score average, since scoring is not implemented

### Modified Capabilities
<!-- None — no existing specs to modify -->

## Impact

- `app.py`: lines 108-116 (score display block) removed
- `src/quiz_data.py`: `shuffle_questions()` function and `random` import removed
- `src/tts_service.py`: `get_audio_duration()` function and `mutagen` import removed
- `requirements.txt` or `pyproject.toml`: `mutagen` dependency removed if unused elsewhere
