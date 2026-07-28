## Why

A suíte pytest introduzida pelo change `add-pytest-suite` (#61) só roda localmente hoje: nenhum job de CI executa os testes automaticamente em push ou em pull requests, conforme gap documentado em `openwiki/testing.md:67`. Sem execução automática em pipeline, regressões em PRs futuros passam despercebidas até alguém rodar `pytest` localmente, e o valor da suíte degrada com o tempo. GitHub Actions é a escolha natural porque o repositório já está hospedado em GitHub e a configuração fica versionada junto com o código.

## What Changes

- Adicionar um workflow de CI sob `.github/workflows/` que executa `pytest` automaticamente em pushes para `main` e em todos os pull requests.
- Instalar dependências de desenvolvimento a partir de `requirements-dev.txt` antes de invocar a suíte.
- Falhar o workflow se qualquer teste falhar, sinalizando regressões diretamente no PR.
- Atualizar `openwiki/testing.md` para refletir que existe suíte automatizada (descrição atual diz "no automated test suite") e remover o gap "No CI test step" da tabela de recomendações.
- Fora do escopo: matrix multi-Python, cache de dependências, type checking, linting, cobertura de código, testes de integração, pipelines de deploy ou release, configuração de branch protection no GitHub.

## Capabilities

### New Capabilities

- `ci-pytest-runner`: workflow de CI executado em push para `main` e em pull requests, que instala `requirements-dev.txt` e roda `pytest`, sinalizando falha quando algum teste quebra.

### Modified Capabilities

-

## Impact

- Novo arquivo de workflow versionado no repositório; nenhuma mudança em código de produção.
- Mudança de uma linha em `openwiki/testing.md` (atualização da descrição e da tabela de gaps).
- Nenhuma alteração em `requirements.txt`, `pytest.ini`, ou em qualquer módulo Python de produção.
- Cada push em `main` e cada PR aberta passa a disparar uma execução de CI de curta duração.
