## ADDED Requirements

### Requirement: CI SHALL executar a suíte pytest em push para main

O workflow de CI SHALL iniciar uma execução que roda a suíte pytest quando um commit é empurrado para a branch `main`, e SHALL ser concluído com sucesso quando todos os testes passam.

#### Scenario: Push para main dispara a execução do CI
- **WHEN** um commit é empurrado para a branch `main`
- **THEN** o workflow SHALL iniciar uma execução que invoca `pytest`

#### Scenario: Push para main com testes que passam conclui com sucesso
- **WHEN** um commit é empurrado para `main` e todos os testes da suíte passam
- **THEN** o workflow SHALL ser concluído com sucesso

#### Scenario: Push para branch que não é main não dispara este CI
- **WHEN** um commit é empurrado para uma branch diferente de `main` que não tem pull request aberto
- **THEN** o workflow configurado para `main` SHALL não iniciar

### Requirement: CI SHALL executar a suíte pytest em pull requests contra main

O workflow de CI SHALL iniciar uma execução que roda a suíte pytest quando um pull request é aberto, sincronizado ou reaberto contra a branch `main`, e SHALL ser concluído com sucesso quando todos os testes passam.

#### Scenario: Abertura de pull request dispara a execução do CI
- **WHEN** um pull request é aberto contra `main`
- **THEN** o workflow SHALL iniciar uma execução que invoca `pytest`

#### Scenario: Sincronização de pull request dispara nova execução do CI
- **WHEN** novos commits são adicionados a um pull request existente contra `main` (evento synchronize)
- **THEN** o workflow SHALL iniciar uma nova execução que invoca `pytest`

#### Scenario: Reabertura de pull request dispara nova execução do CI
- **WHEN** um pull request previamente fechado contra `main` é reaberto
- **THEN** o workflow SHALL iniciar uma nova execução que invoca `pytest`

#### Scenario: Pull request com testes que falham é sinalizado como falho
- **WHEN** um pull request contra `main` é processado e ao menos um teste falha
- **THEN** o workflow SHALL ser concluído como falho

### Requirement: CI SHALL preparar o ambiente com dependências de desenvolvimento antes de pytest

O workflow de CI SHALL instalar as dependências listadas em `requirements-dev.txt` antes de executar a suíte pytest, de modo que a invocação de pytest encontre `pytest` e seus plugins disponíveis.

#### Scenario: Instalação precede pytest
- **WHEN** o workflow prepara o ambiente para uma execução
- **THEN** SHALL instalar as dependências de `requirements-dev.txt` antes de invocar `pytest`

#### Scenario: pytest em ambiente sem dependências falha na preparação
- **WHEN** o workflow executa em ambiente onde `pip install -r requirements-dev.txt` falha
- **THEN** SHALL concluir como falho sem invocar `pytest` (ou, se invocar, SHALL ainda ser marcado como falho)

### Requirement: CI SHALL reportar sucesso quando todos os testes passam e falha caso contrário

O workflow de CI SHALL reportar o status da execução como bem-sucedido quando a suíte pytest passa, e SHALL reportar como falho quando há falha em qualquer teste, em erros de coleta ou em erros internos do pytest.

#### Scenario: Suíte pytest completa passa
- **WHEN** o workflow executa `pytest` e todos os testes são coletados e passam
- **THEN** o workflow SHALL ser concluído como bem-sucedido

#### Scenario: Suíte pytest com falha em um teste
- **WHEN** o workflow executa `pytest` e ao menos um teste falha
- **THEN** o workflow SHALL ser concluído como falho

#### Scenario: Suíte pytest com erro de coleta
- **WHEN** o workflow executa `pytest` e há erro de coleta (por exemplo, import quebrado em algum teste)
- **THEN** o workflow SHALL ser concluído como falho

### Requirement: CI SHALL usar versão de Python compatível com o projeto

O workflow de CI SHALL rodar pytest em uma versão de Python 3.10 ou superior, conforme declarado como requirement mínimo do projeto.

#### Scenario: Versão de Python declarada e usada
- **WHEN** o workflow configura o interpretador Python para a execução
- **THEN** SHALL utilizar uma versão 3.10 ou superior
- **AND** SHALL executar `pytest` nessa versão
