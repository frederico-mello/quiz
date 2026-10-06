# Proposal

## Why

O repositório não oferece documentação permanente e acessível para leitores humanos, e seu README ainda apresenta a pasta `openwiki/` removida e sete links mortos. Uma documentação em português brasileiro, com a metodologia do projeto como eixo, explica como o sistema funciona e corrige a inconsistência que a spec atual ainda perpetua.

## What Changes

- Criar `docs/` com visão geral, arquitetura, fluxo principal, dados, componentes, metodologia, pesquisa e fontes, glossário e índice de leitura.
- Explicar o ciclo OpenSpec (specs como verdade, change como unidade de trabalho, delta, artefatos encadeados e archive incorporando o delta à verdade), avaliação via LangChain `ChatOpenAI`/LiteLLM e fallback automático para OpenRouter em `evaluate_answer()`, moderação local e semântica, `edge-tts`, QR Code e link por pergunta, pytest/GitHub Actions, `st.session_state`/`st.rerun()` e perguntas em `questions.json` sem banco de dados.
- Usar português do Brasil, tom curioso e acessível, analogias explicativas, diagramas Mermaid e marcação explícita de inferências no texto final.
- Corrigir o README: remover a estrutura `openwiki/` e os sete links mortos, e apontar para a documentação mantida em `docs/`; não recriar `openwiki/` nem incluir instruções para agentes.
- Adaptar a spec `readme-documentation`: retirar o cenário que pressupõe OpenWiki e manter a exigência de que links do README resolvam para destinos existentes.

## Capabilities

### New Capabilities
- `repository-documentation`: documentação permanente, legível e navegável sobre o quiz e sua metodologia.

### Modified Capabilities
- `readme-documentation`: atualizar o contrato de destino da documentação, preservando a verificação de links existentes.

## Impact

Arquivos de conteúdo em `docs/`, README e a spec `openspec/specs/readme-documentation/spec.md`. Não altera comportamento de execução, dependências ou persistência do aplicativo.
