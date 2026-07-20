## 1. Remove phantom score display

- [x] 1.1 Delete the `avg_score_pct` computation block and "Pontuação média" caption from `app.py` (lines 108-116)

## 2. Remove dead functions

- [x] 2.1 Delete `shuffle_questions()` function and `import random` from `src/quiz_data.py`
- [x] 2.2 Delete `get_audio_duration()` function and `from mutagen.mp3 import MP3` from `src/tts_service.py`

## 3. Remove unused dependency

- [x] 3.1 Remove `mutagen>=1.47.0` from `requirements.txt`

## 4. Verify

- [x] 4.1 Run the app and confirm the first question renders without `ZeroDivisionError`
- [x] 4.2 Confirm no "Pontuação média" caption appears on any question
- [x] 4.3 Confirm questions still appear in JSON file order
- [x] 4.4 Confirm avatar gif sync (talking/idle) still works via audio events
