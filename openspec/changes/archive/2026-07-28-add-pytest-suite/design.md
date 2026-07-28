## Context

O Quiz do Professor é um app Streamlit single-page com código em `src/` (módulos `avatar`, `config`, `content_filter`, `llm_service`, `qrcode_service`, `quiz_data`, `tts_service`) e `app.py` na raiz. Não há suíte de testes: nenhum arquivo `test_*.py`, nenhum framework configurado, nenhum job de CI executando testes, conforme `openwiki/testing.md`. Toda validação é manual via checklist.

A change `add-pytest-suite` introduz a primeira suíte automatizada do projeto, cobrindo os módulos de lógica central sem dependência de rede ou de credenciais. Os módulos cobertos (`content_filter`, `quiz_data`, `llm_service`, `qrcode_service`) são os alvos de prioridade alta identificados no gap atual; os demais (`avatar`, `config`, `tts_service`, `app.py`) ficam fora de escopo por exigirem rede, credenciais ou harness de UI.

Convenções atuais do projeto que o design respeita:
- Manifesto de produção em `requirements.txt` (sem `pyproject.toml`, sem `setup.cfg`).
- Nenhum framework de teste, nenhum diretório `tests/`, nenhuma config pytest.
- Dependências gerenciadas via pip + requirements files (sem Poetry/uv).

## Goals / Non-Goals

**Goals:**
- Estabelecer suíte pytest localmente executável que cubra `content_filter`, `quiz_data`, `llm_service` e `qrcode_service` com testes unitários rápidos e isolados.
- Isolar totalmente dependências de teste (`pytest`) das de produção (`requirements.txt`).
- Permitir execução sem rede e sem credenciais reais, via mocks do cliente OpenRouter/ChatOpenAI.
- Fornecer configuração pytest mínima (descoberta + resolução de import) sem introduzir novos formatos de arquivo além do estritamente necessário.
- Cobrir happy paths, casos negativos (entradas inválidas, mocks de exceção) e edge cases (limites de coleção, mocks de dependência lazy).

**Non-Goals:**
- Configuração de CI / GitHub Actions para execução automática em push (change posterior dedicado).
- Testes de integração, end-to-end ou de componentes Streamlit.
- Refatoração do código de produção dos módulos cobertos.
- Type checking (mypy/pyright) ou linting (ruff/flake8).
- Cobertura de `avatar.py`, `tts_service.py`, `config.py` e `app.py`.
- Introdução de `pyproject.toml` ou `setup.cfg` apenas para servir ao teste (escolha por alinhamento à convenção atual).

## Decisions

### Decisão 1 — Layout: `tests/` espelhando `src/`

```
tests/
  __init__.py
  conftest.py
  test_content_filter.py
  test_quiz_data.py
  test_llm_service.py
  test_qrcode_service.py
pytest.ini
requirements-dev.txt
```

`tests/` na raiz é a convenção pytest padrão e simplifica a configuração de `testpaths`. Espelhar a estrutura de `src/` (um arquivo de teste por módulo) facilita localizar o teste correspondente a cada unidade coberta. `__init__.py` vazio torna `tests/` um package Python estável, o que facilita imports compartilhados entre arquivos de teste e fixtures reutilizáveis.

### Decisão 2 — Resolução de import via `pytest.ini` (pythonpath)

`pytest.ini` mínimo:

```ini
[pytest]
testpaths = tests
pythonpath = src
addopts = -ra --strict-markers
```

`pythonpath = src` (suportado nativamente em pytest≥7) elimina a necessidade de `conftest.py` hackeando `sys.path` ou de instalar o package em modo editable. `testpaths` limita descoberta; `addopts` ativa relatório curto e marcadores estritos. Manter `pytest.ini` evita introduzir `pyproject.toml` apenas para servir ao teste.

### Decisão 3 — Dependências: `pytest` em arquivo dev separado

`requirements-dev.txt`:

```
pytest>=8.0
```

Instalação local: `pip install -r requirements-dev.txt`. `requirements.txt` de produção permanece inalterado (sem pytest, sem pytest-mock). Isolamento total impede deploy de produção puxar deps de teste.

### Decisão 4 — Mocking: `unittest.mock` da stdlib, sem plugin

Mocks do `ChatOpenAI` (via `src.llm_service.get_llm` ou `src.content_filter.check_text_llm`) e de `src.config.OPENROUTER_API_KEY` feitos com `unittest.mock.MagicMock`, `monkeypatch.setattr`, e `monkeypatch.setenv`. `setattr` aplica-se a atributos de módulo (ex: `src.llm_service.get_llm`); `MagicMock` aplica-se a retornos de chamada encadeados. Zero dependências extras; cobertura total dos pontos de mock necessários.

### Decisão 5 — Granularidade dos testes (parametrização quando aplicável)

Casos com mesma estrutura e diferentes entradas usam `@pytest.mark.parametrize` para data-driven testing. Casos com setup distinto (mock LLM, monkeypatch de env, fixture de arquivo) ficam em funções separadas para legibilidade. `tmp_path` do pytest dá isolamento de filesystem automático sem fixture custom.

### Decisão 6 — Fronteiras de mock

Mocks são aplicados no **boundary do módulo**, não em cada chamada interna:
- `src.llm_service.get_llm` é mockado, não `langchain_openai.ChatOpenAI.invoke`.
- `src.config.OPENROUTER_API_KEY` é mockado via `monkeypatch.setenv`, não via patch profundo.
- `src.content_filter.check_text_llm` é mockado quando testado de fora (em `check_text`); quando testado diretamente, mocka-se o `llm_client` passado.

Isso mantém testes resilientes a refatorações internas: mudanças no `ChatOpenAI` não quebram testes do `content_filter` enquanto a interface de `get_llm`/`check_text_llm` se mantiver.

### Decisão 7 — Cobertura de erros via mock, não captura

Comportamento atual de `evaluate_answer` é propagar exceções do LLM sem captura. Testes verificam que exceções **sobem** (não capturam silenciosamente) usando `pytest.raises`. Captura seria um refactor fora de escopo.

Para `check_text_llm` quando `OPENROUTER_API_KEY` ausente, código retorna `(False, None)`. Teste valida esse caminho via `monkeypatch.setenv("OPENROUTER_API_KEY", "")`.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| pytest≥8.0 não instalado em ambiente dev → ImportError em `from src.*` | `requirements-dev.txt` com pin mínimo; nota explícita de instalação |
| Mocks frágeis a refatoração interna (ex: `evaluate_answer` ganhar try/except) | Mocks no boundary do módulo (`get_llm`), não em cada chamada; testes de `evaluate_answer` validam chamada + retorno, não implementação interna |
| Testes passam mas produção quebra por divergência de ambiente (versões, deps) | Sem CI neste change → aceito como limitação documentada; mudança futura dedicada cobre o gap |
| `check_text` com import lazy de `src.config` cria acoplamento ao env que pode surpreender em CI futuro | Documentado no docstring do teste; `monkeypatch.setenv` aplicado antes da invocação |
| Cobertura não inclui `avatar`, `tts`, `config`, `app.py` → regressões nesses módulos passam | Aceito como escopo desta change; `openwiki/testing.md` continua apontando esses como gaps separados para mudanças futuras |
| Sem pytest-mock, código de mock pode ficar verboso | Aceito: trade-off por zero dependências extras; ~5-10 linhas a mais por teste com mock complexo |
