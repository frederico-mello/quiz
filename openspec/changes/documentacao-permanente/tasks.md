# Tasks

## 1. Criar documentação permanente

- [x] 1.1 Adicionar `docs/README.md`, visão geral, arquitetura, fluxo principal, dados, componentes, metodologia, pesquisa e fontes e glossário, aproveitando o pacote preparado e adaptando-o ao repositório.
- [x] 1.2 Garantir conteúdo em português do Brasil, tom curioso com analogias, diagramas Mermaid e marcação `(inferência)` junto às afirmações inferidas e no fim de cada página que as contenha.
- [x] 1.3 Conferir que as páginas explicam o ciclo OpenSpec completo, LLM via `ChatOpenAI`/LiteLLM com chave virtual e fallback OpenRouter em `evaluate_answer()`, moderação local e semântica, `edge-tts`, QR/link por pergunta, pytest/GitHub Actions, `st.session_state`/`st.rerun()` e `questions.json` sem banco de dados.

## 2. Atualizar README e contrato de documentação

- [x] 2.1 Remover do README a entrada `openwiki/` e os sete links mortos; incluir links relativos válidos para a documentação permanente em `docs/`, sem recriar `openwiki/`.
- [x] 2.2 Incorporar o delta `readme-documentation`: retirar o cenário que pressupõe OpenWiki e manter a exigência de que todos os links apontem para destinos existentes.
- [x] 2.3 Verificar manualmente destinos dos links do README e índice de `docs/`, presença dos tópicos exigidos e renderização/sintaxe dos diagramas Mermaid; não incluir arquivos de instrução para agentes.
