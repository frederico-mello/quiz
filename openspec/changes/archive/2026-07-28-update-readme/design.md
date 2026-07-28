## Context

O README é a principal porta de entrada do repositório, mas atualmente mistura instruções desatualizadas com referências para páginas que não existem nos caminhos indicados. O projeto também mantém documentação OpenWiki para detalhes de arquitetura, fluxos e operações.

## Goals / Non-Goals

**Goals:**

- Reorganizar o README como guia inicial único para instalação, configuração e execução.
- Alinhar descrição de recursos, estrutura e variáveis de ambiente ao estado atual do projeto.
- Corrigir links para arquivos e páginas existentes.
- Manter links para OpenWiki quando o conteúdo detalhado já estiver documentado lá.

**Non-Goals:**

- Alterar comportamento da aplicação, APIs ou dependências.
- Editar páginas geradas do OpenWiki.
- Criar infraestrutura específica de testes ou um novo sistema de documentação.
- Transformar o README em runbook operacional detalhado.

## Decisions

- **README como porta de entrada:** organizar o documento em visão geral, recursos, requisitos, instalação, configuração, execução, estrutura e documentação adicional. Isso concentra o caminho inicial sem duplicar toda a documentação especializada.
- **OpenWiki como documentação detalhada:** apontar para páginas OpenWiki existentes quando o assunto exigir mais profundidade. O README não será usado para substituir ou editar conteúdo gerado.
- **Atualização manual direcionada:** reconstruir o conteúdo do README com base no estado atual do repositório e nas referências válidas, mantendo a mudança limitada à documentação principal.
- **Configuração explícita:** documentar variáveis obrigatórias e opcionais, incluindo `APP_URL`, cujo padrão é `http://localhost:8501` e cuja finalidade é definir a URL base dos links compartilháveis.
- **Links verificáveis:** substituir referências inválidas para `openwiki/architecture/overview.md`, `openwiki/workflows/quiz-flow.md` e `openwiki/operations/runbook.md` pelos arquivos existentes `openwiki/architecture.md`, `openwiki/workflows.md` e `openwiki/operations.md`. Referências inválidas devem ser removidas ou corrigidas durante a revisão.
- **Validação sem nova infraestrutura:** verificar cada caminho relativo com os arquivos versionados do repositório, executar a auditoria de higiene existente e revisar o diff; não adicionar dependências ou testes exclusivos para o README.

## Risks / Trade-offs

- **Risco:** páginas OpenWiki podem mudar de nome ou caminho → **Mitigação:** usar somente caminhos presentes no repositório e revisar links no mesmo diff.
- **Risco:** a reconstrução ampla pode omitir instruções úteis do README atual → **Mitigação:** preservar requisitos, comandos de instalação, configuração necessária e execução que continuam válidos.
- **Trade-off:** manter detalhes no OpenWiki reduz duplicação, mas exige que os links permaneçam atualizados → **Mitigação:** tratar integridade dos links como critério de aceitação documental.

## Migration Plan

- Substituir o conteúdo atual de `README.md` pela versão reorganizada e corrigida.
- Validar links relativos, comandos documentados e variáveis de ambiente no diff antes da publicação.
- Rollback: reverter o commit que altera `README.md`, sem migração de dados ou alteração de runtime.

## Open Questions

Nenhuma questão técnica permanece aberta para esta mudança; o escopo está limitado à documentação principal e seus links.
