## 1. Setup

- [ ] 1.1 Add `qrcode` library to `requirements.txt`
- [ ] 1.2 Add `APP_URL` config to `src/config.py`

## 2. Query Parameter Routing

- [ ] 2.1 Read `?q=<id>` from `st.query_params` in `app.py`
- [ ] 2.2 Implement question lookup by `id` field (not index)
- [ ] 2.3 Handle missing `?q` parameter with friendly message
- [ ] 2.4 Handle invalid/non-numeric ID with friendly error
- [ ] 2.5 Handle non-existent question ID with "Pergunta não encontrada"

## 3. Single Question Experience

- [ ] 3.1 Remove "Próxima pergunta" button and sequential navigation
- [ ] 3.2 Remove progress bar ("Pergunta X de Y")
- [ ] 3.3 Remove cumulative score display and fix ZeroDivisionError
- [ ] 3.4 Keep "Tentar novamente" button for current question

## 4. QR Code Generation

- [ ] 4.1 Implement QR code generation function in `src/qrcode_service.py`
- [ ] 4.2 Display QR code below the question using configurable base URL
- [ ] 4.3 Use `APP_URL` env var (fallback to `http://localhost:8501`)

## 5. Session State Cleanup

- [ ] 5.1 Remove `current_index`-based state management
- [ ] 5.2 Ensure response/feedback/audio persist per session for the single question
