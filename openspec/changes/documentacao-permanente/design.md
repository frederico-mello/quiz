# Design

## Context

Ver `proposal.md` para a motivação. O README atual inclui `openwiki/` e sete caminhos sem destino; o material factual preparado fora do repositório descreve o estado-alvo `main` em `2a1e7db` e marca inferências explicitamente. O aplicativo tem `app.py`, oito módulos em `src/` (incluindo `__init__.py`) e perguntas em `questions.json`; não há armazenamento de respostas em banco de dados.

## Goals / Non-Goals

**Goals:** organizar a documentação em páginas Markdown navegáveis em `docs/`; fazer da metodologia o fio condutor; preservar fatos e separar inferências; atualizar o README e sua spec sem criar novamente OpenWiki.

**Non-Goals:** alterar código executável, dependências, workflow CI, serviços externos ou formato de dados; criar instruções para agentes; produzir documentação operacional privada ou presumir configuração externa não observada.

## Decisions

- Criar `docs/README.md` como índice e páginas temáticas separadas para visão geral, arquitetura, fluxo, dados, componentes, metodologia, pesquisa/fontes e glossário. A separação mantém cada assunto localizável e o índice fornece um caminho de leitura.
- Redigir em português brasileiro, com narrativa acessível, analogias curtas e Mermaid embutido em Markdown. Para fatos não demonstrados diretamente pelo código ou pela configuração acessível, manter o rótulo `(inferência)` junto à afirmação e registrar as inferências ao final da página correspondente.
- Apresentar OpenSpec como ciclo encadeado: specs descrevem a verdade atual; change é unidade de trabalho e reúne proposal, design, tasks e delta; delta registra a alteração proposta; archive, após sincronização, incorpora o delta à verdade das specs. Não afirmar que o repositório força automaticamente a abertura de changes.
- Documentar os limites entre aplicativo e serviços externos: avaliação por LangChain `ChatOpenAI` através do servidor LiteLLM com chave virtual, fallback de código para OpenRouter dentro de `evaluate_answer()`, moderação local e semântica, síntese via `edge-tts`, compartilhamento por URL/QR por pergunta. Explicar `st.session_state` e `st.rerun()` como consequência do modelo de execução do Streamlit, e `questions.json` como fonte das perguntas sem persistência em banco.
- Remover do README a referência à estrutura `openwiki/` e seus sete links, substituindo-os por links relativos às páginas existentes em `docs/`. Ajustar o delta de `readme-documentation` para remover o cenário específico OpenWiki e manter o requisito geral de destinos existentes.

## Risks / Trade-offs

- A documentação pode envelhecer junto com código e configuração; links relativos para arquivos do próprio repositório reduzem, mas não eliminam, esse risco.
- Uma analogia pode ser lida como fato técnico; limitar analogias a explicações e identificar inferências evita confundir interpretação com comportamento comprovado.
- Mermaid renderiza nativamente no GitHub, mas outros visualizadores Markdown podem não renderizá-lo; manter o texto explicativo compreensível sem depender exclusivamente do diagrama.
- A leitura de pesquisa externa pode atribuir mais certeza que a evidência permite; citar fontes e separar observação, fonte externa e inferência em `07-pesquisa-e-fontes.md`.
