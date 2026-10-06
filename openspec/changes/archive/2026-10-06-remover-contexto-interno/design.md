# Design

## Context

Veja `proposal.md` para a motivação. A documentação publicada está em `docs/` e no README raiz; o requisito aplicável está em `repository-documentation`. A inspeção confirmou 10 specs principais (439 linhas), 8 changes arquivadas, 135 commits e 8 arquivos sob `tests/` (6 módulos de teste). O histórico local aponta `auditoria.yaml` como alterado por último em 2026-07-26; o workflow agenda o cron semanal `0 6 * * 1` e fixa `repository-hygiene==0.2.0`, enquanto o YAML fornece chaves `rules:`.

## Goals / Non-Goals

**Goals:** propor mudanças documentais mínimas, preservar os fatos técnicos e identificar base verificável para cada afirmação, incluindo evidências recentes e contagens recontadas.

**Non-Goals:** alterar código, testes, automações, dependências ou arquivos de configuração; sincronizar o delta na spec principal nesta change.

## Decisions

- Concentrar a varredura em todo `docs/` e no `README.md` raiz, buscando referências a dono, pedidos internos, prioridade declarada, colegas, insumos, conversas, contexto do projeto e hábitos pessoais. Corrigir somente exposições de contexto interno; pedidos ao modelo/LLM em documentação técnica permanecem.
- Tratar a regra nova como requisito de `repository-documentation`: remover categorias de contexto interno especificadas e exigir que afirmações sobre o projeto derivem de código, histórico ou fonte citada, ou estejam explicitamente marcadas como `(inferência)`.
- Atualizar os fatos documentados com as evidências verificadas: conversão do cron para UTC e horário de Brasília; incompatibilidade entre `rules:` no arquivo e o formato lido pela versão fixada, incluindo o marco de 2026-07-26 e o repin indicado para a linha 1.x; resposta HTTP 200 do endereço Streamlit sem inspeção visual; e contagens do repositório no commit `d53b80e`.
- Manter as alterações dentro dos artefatos OpenSpec e da documentação indicada. A spec principal não muda nesta etapa.

## Risks / Trade-offs

- A auditoria é descrita a partir do código e do histórico disponíveis; não se deve afirmar inspeção visual da aplicação nem atribuir causa a evidência ausente.
- Contagens podem envelhecer: registrar a revisão usada (`d53b80e`) torna o retrato temporal explícito.
- Uma varredura lexical ampla pode encontrar termos técnicos legítimos; aplicar a decisão pelo contexto para evitar remover conteúdo técnico, particularmente pedidos ao LLM.
