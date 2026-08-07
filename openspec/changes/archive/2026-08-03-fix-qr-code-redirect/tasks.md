## 1. QR links use public application URL

- [x] 1.1 Update `src/config.py` so `APP_URL` falls back to `https://lappquiz.ict.unesp.br` while preserving the environment override.
- [x] 1.2 Add focused `pytest` coverage for the public fallback, custom `APP_URL`, and final question URL composition with `?q=<id>`.
- [x] 1.3 Update `README.md` to document the public default and the local `APP_URL` override convention.
- [x] 1.4 Verify that generated question links and QR codes use the public default when no override is configured, use the custom value when configured, and retain existing PNG generation behavior.
