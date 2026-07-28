## Why

O Quiz do Professor não possui suíte automatizada de testes: não há arquivos de teste, nem framework configurado, nem job de CI executando testes, conforme documentado em `openwiki/testing.md`. Toda validação é manual hoje, o que permite regressões passarem despercebidas em refatorações e dificulta mudanças seguras nos módulos centrais. Esse gap está marcado como prioridade alta.

## What Changes

- Introduzir suíte de testes unitários em pytest cobrindo os módulos de lógica central do app, sem dependência de rede ou de API externa.
- Cobrir, com testes isolados e rápidos, `src/content_filter.py`, `src/quiz_data.py`, `src/llm_service.py` (com cliente LLM mockado) e `src/qrcode_service.py`.
- Adicionar configuração mínima de pytest para descoberta e execução local dos testes.
- Adicionar `pytest` como dependência de desenvolvimento, sem afetar dependências de produção.

## Capabilities

### New Capabilities

- `core-unit-testing`: cobertura automatizada via pytest para os módulos de lógica central (`content_filter`, `quiz_data`, `llm_service`, `qrcode_service`), executável localmente sem rede ou credenciais externas.

### Modified Capabilities

Nenhuma. As capacidades existentes (`avatar`, `content-filter`, `independent-question-access`, `llm-evaluation`, `question-link-qr-code`, `quiz-ui`, `tts`) não têm seus requisitos alterados; este change apenas adiciona verificação automatizada por cima delas.

## Non-Goals

- Integração contínua: nenhum workflow de GitHub Actions nem execução automática em pipeline — fica para change posterior dedicado.
- Testes de integração / end-to-end e testes de componentes Streamlit.
- Refatoração do código de produção dos módulos cobertos; os testes devem validar comportamento atual.
- Type checking (mypy/pyright) e linting (ruff/flake8) — concerns separados.
- Cobertura de `avatar.py`, `tts_service.py`, `config.py` e do próprio `app.py` (Streamlit), por exigirem rede, credenciais ou harness de UI fora do escopo deste change.

## Impact

- Novo espaço de testes no repositório, dedicado a verificar comportamento atual sem alterar a aplicação.
- Adição de dependência de desenvolvimento para execução local dos testes, isolada do `requirements.txt` de produção.
- Nenhum contrato de API, schema ou workflow existente é alterado.
- Nenhum arquivo de produção é modificado pelos testes deste change.
