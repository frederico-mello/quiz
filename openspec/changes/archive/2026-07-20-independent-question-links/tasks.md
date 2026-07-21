## 1. Setup

- [x] 1.1 Add `qrcode` library to `requirements.txt`
- [x] 1.2 Add `APP_URL` config to `src/config.py`

## 2. Query Parameter Routing

- [x] 2.1 Read `?q=<id>` from `st.query_params` in `app.py`
- [x] 2.2 Implement question lookup by `id` field (not index)
- [x] 2.3 Handle missing `?q` parameter with friendly message
- [x] 2.4 Handle invalid/non-numeric ID with friendly error
- [x] 2.5 Handle non-existent question ID with "Pergunta não encontrada"

## 3. Single Question Experience

- [x] 3.1 Remove "Próxima pergunta" button and sequential navigation
- [x] 3.2 Remove progress bar ("Pergunta X de Y")
- [x] 3.3 Remove cumulative score display and fix ZeroDivisionError
- [x] 3.4 Keep "Tentar novamente" button for current question

## 4. QR Code Generation

- [x] 4.1 Implement QR code generation function in `src/qrcode_service.py`
- [x] 4.2 Display QR code below the question using configurable base URL
- [x] 4.3 Use `APP_URL` env var (fallback to `http://localhost:8501`)

## 5. Session State Cleanup

- [x] 5.1 Remove `current_index`-based state management
- [x] 5.2 Ensure response/feedback/audio persist per session for the single question
