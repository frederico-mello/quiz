# Spec Delta

## ADDED Requirements

### Requirement: A documentação não expõe contexto interno

O texto publicado em `docs/` SHALL NOT expor pedidos, prioridades declaradas, conversas entre mantenedores e colaboradores ou preferências pessoais de quem mantém o repositório; afirmações sobre o projeto SHALL decorrer do código, do histórico ou de fonte citada, ou estar marcadas como inferência.

#### Scenario: Leitor encontra documentação fundamentada e sem contexto interno

- **WHEN** uma pessoa lê as páginas publicadas em `docs/`
- **THEN** não encontra referência a pedidos, prioridades declaradas ou conversas internas
- **AND** as afirmações decorrem do repositório, de fonte citada ou estão marcadas como `(inferência)`
