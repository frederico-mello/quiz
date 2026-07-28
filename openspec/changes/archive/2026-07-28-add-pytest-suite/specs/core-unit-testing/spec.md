## Purpose

Define o comportamento que a suíte de testes unitários deve garantir sobre os módulos centrais do app (`content_filter`, `quiz_data`, `llm_service`, `qrcode_service`), de forma executável localmente sem rede nem credenciais externas.

## ADDED Requirements

### Requirement: Suíte SHALL executar sem rede e sem credenciais reais

A suíte de testes SHALL ser executável localmente sem conectividade de rede e sem credenciais reais do OpenRouter, fazendo mock de toda dependência externa no boundary do módulo.

#### Scenario: Pytest completa sem rede
- **WHEN** a suíte é executada em um ambiente sem acesso à rede
- **THEN** todos os testes SHALL passar sem erros relacionados a rede

#### Scenario: Pytest completa sem OPENROUTER_API_KEY
- **WHEN** a suíte é executada em um ambiente sem a variável `OPENROUTER_API_KEY` definida
- **THEN** todos os testes SHALL passar

### Requirement: Cobertura SHALL cobrir content_filter

A suíte SHALL cobrir as funções públicas de `src/content_filter.py` para entradas bloqueadas e entradas limpas, incluindo normalização de leet-speak e o caminho de moderação via LLM com cliente mockado.

#### Scenario: Palavra bloqueada é detectada
- **WHEN** um teste invoca `check_keywords` com texto contendo palavra do conjunto bloqueado
- **THEN** o teste SHALL afirmar que a função retorna `(True, mensagem)`

#### Scenario: Texto limpo passa pela checagem de keywords
- **WHEN** um teste invoca `check_keywords` com texto sem palavras bloqueadas
- **THEN** o teste SHALL afirmar que a função retorna `(False, None)`

#### Scenario: Leet-speak é normalizado antes da checagem
- **WHEN** um teste invoca `check_keywords` com caracteres leet-speak representando palavra bloqueada
- **THEN** o teste SHALL afirmar que a função detecta o termo normalizado

#### Scenario: Padrão regex bloqueado é detectado
- **WHEN** um teste invoca `check_patterns` com texto correspondente a um padrão bloqueado
- **THEN** o teste SHALL retornar mensagem de padrão bloqueado

#### Scenario: Nível de advertência escala corretamente
- **WHEN** um teste invoca `get_warning_level` com contagens 0, 1, 2 e ≥3
- **THEN** o teste SHALL afirmar os estados `none`, `first`, `second` e `blocked` respectivamente

#### Scenario: check_text_llm classifica resposta do LLM mockado
- **WHEN** um teste invoca `check_text_llm` com cliente LLM mockado retornando "BLOQUEAR"
- **THEN** o teste SHALL afirmar bloqueio com mensagem de moderação semântica

#### Scenario: check_text pula LLM quando bloqueado localmente
- **WHEN** um teste invoca `check_text` com texto contendo palavra bloqueada localmente
- **THEN** o teste SHALL retornar bloqueio sem chegar a invocar o LLM

#### Scenario: check_text consulta LLM quando local passa e use_llm é verdadeiro
- **WHEN** um teste invoca `check_text` com texto limpo e `use_llm=True`
- **THEN** o teste SHALL invocar o caminho de LLM mockado uma vez

#### Scenario: check_text não consulta LLM quando use_llm é falso
- **WHEN** um teste invoca `check_text` com texto limpo e `use_llm=False`
- **THEN** o teste SHALL retornar `(False, None)` sem invocar o LLM

### Requirement: Cobertura SHALL cobrir quiz_data

A suíte SHALL cobrir as funções públicas de `src/quiz_data.py` para consultas válidas, índices fora do intervalo e consultas por identificador existente e inexistente.

#### Scenario: Índice válido retorna a pergunta correspondente
- **WHEN** um teste invoca `get_question` com índice dentro do intervalo
- **THEN** o teste SHALL afirmar que a pergunta correspondente é retornada

#### Scenario: Índice fora do intervalo retorna None
- **WHEN** um teste invoca `get_question` com índice negativo ou maior que o tamanho da lista
- **THEN** o teste SHALL afirmar que a função retorna `None`

#### Scenario: Pergunta existente é encontrada por id
- **WHEN** um teste invoca `get_question_by_id` com um id presente na lista
- **THEN** o teste SHALL afirmar que a pergunta correspondente é retornada

#### Scenario: Pergunta inexistente por id retorna None
- **WHEN** um teste invoca `get_question_by_id` com um id ausente da lista
- **THEN** o teste SHALL afirmar que a função retorna `None`

### Requirement: Cobertura SHALL cobrir llm_service com LLM mockado

A suíte SHALL cobrir as funções públicas de `src/llm_service.py` mockando o cliente LLM, sem chamadas reais de rede.

#### Scenario: Prompt inclui pergunta e respostas
- **WHEN** um teste invoca `build_prompt` com pergunta, resposta correta e resposta do usuário
- **THEN** o teste SHALL afirmar que o prompt formatado contém os três insumos

#### Scenario: Resposta vazia é marcada como sem resposta
- **WHEN** um teste invoca `build_prompt` com `user_answer` em branco
- **THEN** o teste SHALL afirmar que o prompt contém o marcador `(sem resposta)`

#### Scenario: Markdown é removido para TTS
- **WHEN** um teste invoca `clean_text_for_tts` com entrada formatada em markdown
- **THEN** o teste SHALL afirmar que marcadores markdown são removidos e espaços/newlines são normalizados

#### Scenario: evaluate_answer invoca LLM mockado com o prompt construído
- **WHEN** um teste invoca `evaluate_answer` com o cliente LLM mockado
- **THEN** o teste SHALL afirmar que o mock foi invocado com o prompt produzido por `build_prompt`

#### Scenario: evaluate_answer retorna texto limpo da resposta do LLM
- **WHEN** um teste invoca `evaluate_answer` com mock retornando conteúdo com markdown
- **THEN** o teste SHALL afirmar que o retorno passa por `clean_text_for_tts`

### Requirement: Cobertura SHALL cobrir qrcode_service

A suíte SHALL cobrir `src/qrcode_service.generate_qr_code` verificando que o retorno é um buffer PNG válido.

#### Scenario: QR code retorna buffer PNG
- **WHEN** um teste invoca `generate_qr_code` com dados arbitrários
- **THEN** o teste SHALL afirmar que o retorno é um `BytesIO` cujos primeiros bytes correspondem à assinatura PNG
