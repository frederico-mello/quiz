# repository-documentation Specification

## Purpose
Oferecer a leitores humanos uma explicação permanente, acessível e navegável do quiz, de sua arquitetura, de seus dados e, sobretudo, da metodologia que orienta sua evolução.

## Requirements

### Requirement: A documentação permanente explica o projeto em português acessível

O repositório SHALL manter em `docs/` um índice e páginas temáticas em português do Brasil, com tom curioso, narrativa acessível e analogias que esclareçam termos sem substituir os fatos. O conjunto SHALL cobrir visão geral, arquitetura, fluxo principal, dados, componentes, metodologia, pesquisa e fontes e glossário.

#### Scenario: Leitor encontra os assuntos do projeto
- **WHEN** uma pessoa abre o índice da documentação
- **THEN** ela encontra links para páginas de visão geral, arquitetura, fluxo principal, dados, componentes, metodologia, pesquisa e fontes e glossário
- **AND** cada link aponta para um destino mantido no repositório

#### Scenario: Leitor distingue fato de interpretação
- **WHEN** uma página apresenta uma conclusão que não é demonstrada diretamente pelo código ou por fonte identificada
- **THEN** a afirmação é marcada explicitamente como `(inferência)` e as inferências da página são listadas ao final

### Requirement: A documentação explica a metodologia como ciclo central

A documentação SHALL explicar OpenSpec como um ciclo em que as specs são a descrição de verdade do estado atual, cada change constitui uma unidade de trabalho, o delta registra a diferença proposta, os artefatos se encadeiam para definir por quê/o quê/como/passos, e o archive incorpora o delta sincronizado à verdade das specs. SHALL explicar também o papel do pytest e do GitHub Actions na execução automatizada de testes, sem afirmar que uma ferramenta força a abertura de changes quando isso não é demonstrado.

#### Scenario: Leitor acompanha a evolução de uma mudança
- **WHEN** o leitor consulta a página sobre metodologia
- **THEN** consegue seguir do estado descrito nas specs à change, ao delta, aos artefatos encadeados e à incorporação do delta no archive
- **AND** entende que pytest é executado por automação do GitHub Actions

### Requirement: A documentação descreve os fluxos e limites observáveis do quiz

A documentação SHALL descrever a avaliação de respostas com LangChain `ChatOpenAI` através do servidor LiteLLM autenticado por chave virtual e o fallback automático para OpenRouter implementado em `evaluate_answer()`. SHALL explicar a moderação local e semântica, geração de fala com `edge-tts`, link e QR Code individual por pergunta, o papel de `st.session_state` e `st.rerun()` no modelo de execução do Streamlit, e `questions.json` como fonte de perguntas sem persistência em banco de dados.

#### Scenario: Leitor entende uma resposta do envio ao áudio
- **WHEN** o leitor percorre a explicação do fluxo principal
- **THEN** encontra a ordem entre entrada, moderação, avaliação, fallback quando o provedor primário falha e geração/apresentação do áudio
- **AND** consegue identificar que cada pergunta pode ser acessada e compartilhada por seu próprio link e QR Code

#### Scenario: Leitor entende dados e estado da aplicação
- **WHEN** o leitor consulta as páginas de dados e arquitetura
- **THEN** entende que `questions.json` contém o banco de perguntas, que estado transitório fica em `st.session_state` e que o projeto não persiste respostas em banco de dados
- **AND** entende por que o aplicativo usa `st.rerun()` no modelo de execução do Streamlit

### Requirement: A documentação não expõe contexto interno

O texto publicado em `docs/` SHALL NOT expor pedidos, prioridades declaradas, conversas entre mantenedores e colaboradores ou preferências pessoais de quem mantém o repositório; afirmações sobre o projeto SHALL decorrer do código, do histórico ou de fonte citada, ou estar marcadas como inferência.

#### Scenario: Leitor encontra documentação fundamentada e sem contexto interno

- **WHEN** uma pessoa lê as páginas publicadas em `docs/`
- **THEN** não encontra referência a pedidos, prioridades declaradas ou conversas internas
- **AND** as afirmações decorrem do repositório, de fonte citada ou estão marcadas como `(inferência)`
