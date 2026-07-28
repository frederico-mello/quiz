## Context

O repositório `quiz` hospeda o Quiz do Professor, uma aplicação Streamlit single-page. O change `add-pytest-suite` (#61) introduziu a primeira suíte automatizada de testes — 45 testes em `tests/` cobrindo `content_filter`, `quiz_data`, `llm_service` e `qrcode_service` — mas esses testes só rodam localmente via `pytest`. Não há nenhuma execução automática em pipeline: pushes para `main` e pull requests não disparam verificação, e regressões passam despercebidas até alguém rodar `pytest` localmente. `openwiki/testing.md:67` registra esse gap como prioridade média.

Este change fecha esse gap adicionando um único workflow de GitHub Actions (`.github/workflows/test.yml`) que executa `pytest` automaticamente em pushes para `main` e em pull requests contra `main`. Não existe outro workflow de CI no repositório hoje, então este é o primeiro arquivo em `.github/workflows/`. O workflow depende exclusivamente do que o change `add-pytest-suite` já estabelece — `pytest.ini`, `requirements-dev.txt`, e a suíte em `tests/` — sem acrescentar dependências, plugins ou scripts novos.

## Goals / Non-Goals

**Goals:**
- Tornar a suíte pytest (`pytest`) automaticamente verificada em pushes para `main` e em pull requests contra `main`.
- Sinalizar regressões como falha de CI no próprio PR, antes do merge.
- Manter a configuração estritamente declarativa em YAML, sem scripts auxiliares nem dependências extras fora do que já existe.

**Non-Goals:**
- Matrix multi-versão Python (3.10, 3.11, 3.12): uma única versão (mínimo do projeto) é suficiente e proporcional ao tamanho da suíte.
- Cache de dependências (`actions/cache`): suíte termina em ~30s; cache adiciona complexidade sem ganho proporcional.
- Type checking, linting, cobertura de código: concerns separados; gaps já documentados em `openwiki/testing.md`.
- Testes de integração ou end-to-end: fora do escopo do change `add-pytest-suite` que originou a suíte.
- Pipelines de deploy, release ou publicação: este change é estritamente CI de testes.
- Configuração de branch protection no GitHub: configuração manual na interface do GitHub, não armazenada em código deste repositório.

## Decisions

### Decisão 1 — Arquivo único em `.github/workflows/test.yml`

Um único arquivo sob `.github/workflows/` é suficiente para o escopo (test runner). O nome `test.yml` segue a convenção da comunidade GitHub Actions para runners de teste e comunica imediatamente a função do workflow. Nomes mais amplos como `ci.yml` reservam espaço para etapas que este change não inclui; nomes específicos como `pytest.yml` comprometem com uma ferramenta em vez de uma função.

### Decisão 2 — Triggers restritos a `main` e PRs contra `main`

O workflow declara dois eventos:
- `on.push` com filtro `branches: [main]` — execuções disparam em pushes para a branch principal.
- `on.pull_request` com filtro `branches: [main]` — execuções disparam em PRs abertas contra `main`, e também em sincronizações (`synchronize`) e reaberturas (`reopened`) pelo comportamento padrão do evento.

Pushes para outras branches não disparam este CI por design — o sinal nessas branches vem do próprio PR aberto contra `main`. Filtros explícitos por branch evitam execuções redundantes em branches de feature e mantêm o orçamento de CI sob controle. Permite-se a um maintainer adicionar outras branches como `release/*` em mudança posterior se necessário.

### Decisão 3 — Python mínimo declarado (`python-version: "3.10"`)

A configuração usa `actions/setup-python@v5` com `python-version: "3.10"` — o mínimo declarado no `README.md` do projeto. Versão única elimina custo de matrix (não-goal declarado na proposal). Se o projeto vier a suportar 3.11 ou 3.12 oficialmente, a versão pode ser atualizada em mudança isolada; a única diferença observável seria qual versão o CI reportaria no log.

### Decisão 4 — `pip install -r requirements.txt -r requirements-dev.txt` antes de pytest

O CI executa exatamente a mesma sequência que um desenvolvedor executa localmente: instala `requirements.txt` e `requirements-dev.txt` na mesma invocação, e depois invoca `pytest` (sem argumentos adicionais — `pytest.ini` já configura `testpaths`, `pythonpath`, `addopts`). Instalar apenas `requirements-dev.txt` é insuficiente porque os testes importam `src/*` módulos que transitivamente dependem de pacotes de produção (`qrcode` via `src/qrcode_service`, `langchain*` via `src/llm_service`); esses imports falham no coletor do pytest se as deps de produção não estiverem presentes, abortando a suite inteira com `ModuleNotFoundError` antes mesmo de qualquer asserção rodar. A escolha de instalar ambos preserva o isolamento lógico entre `requirements.txt` (produção) e `requirements-dev.txt` (testes) — o split continua existindo —, mas o runner de CI precisa enxergar os dois lados porque os testes atravessam o boundary.

### Decisão 5 — Execução a partir do repo root

Sem `working-directory` customizado. CI runners clonam o repo em `$GITHUB_WORKSPACE` por padrão, e os arquivos relevantes (`pytest.ini`, `requirements-dev.txt`, `tests/`) estão todos no root. Caminhos absolutos não são necessários.

### Decisão 6 — Sem flags extras de pytest

`pytest` é invocado sem argumentos: flags como `--strict-markers`, `-ra` e `--tb=short` já vivem em `pytest.ini` (configurado pelo change `add-pytest-suite`). Duplicar no workflow geraria dois lugares para manter flags em sincronia — anti-pattern.

### Decisão 7 — Sem controle explícito de concorrência

Múltiplas execuções paralelas são permitidas. Cancelar runs anteriores em pushes subsequentes no mesmo PR adiciona estado concorrente ao workflow e risco de falsos negativos (cancelar uma run que estava prestes a passar). Para uma suíte de <2 min, espera sequencial raramente é problema; pode ser revisitado em mudança posterior se o volume de PRs crescer.

### Decisão 8 — Pin de actions por SHA (opcional, decisão deferida)

Pinar `actions/checkout` e `actions/setup-python` por SHA em vez de tag é uma prática de supply-chain hardening. Ficará para uma mudança futura dedicada se hardening de supply chain virar prioridade — fora do escopo deste change.

### Decisão 9 — Atualização de `openwiki/testing.md` no mesmo change

A proposal lista entre as mudanças atualizar `openwiki/testing.md` (descrição atual ainda diz "no automated test suite" e a tabela de gaps inclui "No CI test step"). A atualização ocorre no mesmo PR que adiciona o workflow: a descrição do arquivo passa a refletir que existe suíte automatizada e CI, e a linha "No CI test step" sai da tabela de recomendações. Agrupar evita drift entre o workflow e a documentação, e mantém o change atômico do ponto de vista do leitor.

### Decisão 10 — Propagação de falha de `pip install` para o workflow

Caso `pip install -r requirements-dev.txt` falhe (por exemplo, dependência inexistente no PyPI ou quebra de versão), o step de instalação reporta erro e o GitHub Actions marca o job como falho automaticamente — `pytest` não chega a ser invocado, e mesmo se for (por configuração de `continue-on-error` futura), o status final permanece falho pelo exit-code propagation. Não é necessário adicionar `if` ou manipuladores explícitos: a semântica default do GitHub Actions já satisfaz o cenário de spec "ambiente sem dependências falha na preparação" sem ajustes.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| CI falha por bug transitório de rede ao instalar dependências | Aceito como limitação; falha transitória pode ser re-rodada manualmente pelo maintainer via `gh run rerun`. Quando o cache for adicionado (futuro change), esse risco diminui. |
| Maintainer esquece de habilitar a checagem "require status checks" no branch protection | Fora do escopo deste change (não-versionado). Documentar em comentário no `test.yml` ou em `openwiki/operations.md` se necessário. |
| Pip `requirements-dev.txt` cresce e a instalação fica lenta (hoje ~10s) | Aceito; se virar problema, adicionar `actions/cache` é uma mudança isolada. |
| Suíte pytest cresce e CI passa de minutos | Aceito; adicionar matrix paralelo é mudança isolada. YAGNI por agora. |
| Push direto em `main` (sem PR) dispara o mesmo CI que merge via PR | Por design — `on.push` cobre pushes em geral. Mantém cobertura mesmo para merges squash, fast-forward, ou pushes de admin. |
| Versão de Python declarada diverge do que devs usam localmente | Risco minimizado pela escolha de 3.10 (mínimo declarado). Divergência em uma direção (dev usa 3.11, CI usa 3.10) raramente quebra suíte para código compatível; divergência em outra direção seria captada localmente antes do push. |
| PR #61 (suíte pytest) deve estar mergeada em `main` antes deste PR; caso contrário, o CI falha ao executar `pip install -r requirements-dev.txt` (arquivo inexistente) | Sequência de merge: #61 → main, rebase #63 sobre o novo main, push #63. Documentado no PR #63 como pré-requisito operacional. |
| CI executa apenas `pip install -r requirements-dev.txt`: testes que importam `src/qrcode_service` ou `src/llm_service` falham no coletor com `ModuleNotFoundError: qrcode` / `langchain*` porque essas são deps de produção em `requirements.txt` | Instalar ambos `requirements.txt` e `requirements-dev.txt` no mesmo comando; o isolation principle do change `add-pytest-suite` continua válido (os dois arquivos continuam separados no repo), mas o runner de CI precisa enxergar os dois lados. Detectado pela primeira execução do workflow em PR — capturado em design após o evento. |
