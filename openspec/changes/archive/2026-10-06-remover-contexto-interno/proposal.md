# Proposal

## Why

A documentação publicada ainda atribui escolhas e práticas a pedidos, prioridades e hábitos pessoais de quem mantém o repositório, expondo contexto interno que não ajuda a explicar o projeto. Também contém afirmações e contagens que precisam ser alinhadas às evidências verificáveis no código, histórico ou fontes citadas.

## What Changes

- Remover referências a pedidos, prioridades declaradas, conversas entre colaboradores e hábitos pessoais de `docs/` e do README da raiz, preservando o sentido técnico.
- Explicitar quando afirmações sobre o projeto são inferências e atualizar fatos de cron, auditoria de higiene e pesquisa externa.
- Recontar dados do repositório e registrar a revisão efetivamente consultada.
- Definir requisito para que a documentação não exponha contexto interno e baseie afirmações em fontes rastreáveis ou marque inferências.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `repository-documentation`: estabelecer limites sobre contexto interno exposto e fundamentação de afirmações da documentação permanente.

## Non-goals

Não alterar código, testes, workflows, dependências ou `auditoria.yaml`; não recriar OpenWiki; não modificar a spec principal; não criar arquivos de instrução para agentes. Sem pesquisa adicional ou nova dependência.
