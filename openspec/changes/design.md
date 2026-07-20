## Context

O app é um Streamlit single-page que carrega perguntas de `questions.json` por índice sequencial. Não há roteamento por URL, nem suporte a query parameters. O estado da sessão é gerenciado via `st.session_state`. O `id` de cada pergunta existe no JSON mas nunca é usado — o acesso é puramente por índice.

A mudança proposta transforma cada pergunta em uma experiência independente acessível por link direto com o `id` da pergunta.

## Goals / Non-Goals

**Goals:**
- Acessar pergunta específica via query parameter `?q=<id>` na URL
- Carregar e exibir apenas a pergunta indicada, sem navegação sequencial
- Manter resposta, feedback IA e áudio por sessão
- Gerar QR code para o link da pergunta atual
- Tratar erros: sem `?q`, ID inválido, pergunta inexistente
- Corrigir bug de ZeroDivisionError no score (remover score sequencial)

**Non-Goals:**
- Autenticação ou login
- Persistência de respostas entre sessões
- Edição do catálogo de perguntas
- Alteração do modelo de avaliação por IA
- Roteamento multi-página (permanece single-page com query param)

## Decisions

1. **Query parameter `?q=<id>` em vez de path routing**
   - Streamlit não suporta path routing nativo sem `st.navigation` (que exige multi-página)
   - `st.query_params` permite ler `?q=<id>` diretamente
   - Alternativa rejeitada: `st.navigation` com páginas separadas — adiciona complexidade desnecessária

2. **Busca por `id` do JSON, não por índice**
   - O JSON já tem campo `id` estável
   - Permite links duráveis mesmo se a ordem do JSON mudar
   - Alternativa rejeitada: usar índice — quebra se perguntas forem reordenadas

3. **Remover navegação sequencial e score**
   - O score atual está quebrado (ZeroDivisionError, `total_score` nunca escrito)
   - Sem sequência, score cumulativo não faz sentido
   - UI simplifica para: responder → feedback → tentar novamente

4. **QR code via biblioteca `qrcode` (Python)**
   - Geração server-side, sem depender de API externa
   - Leve, sem dependências complexas
   - Alternativa rejeitada: API externa de QR — dependência de rede desnecessária

5. **Manter fluxo de resposta/feedback/try-again existente**
   - O ciclo atual (responder → moderar → avaliar → TTS → feedback) funciona bem
   - Apenas remover o botão "Próxima pergunta" e a barra de progresso

## Risks / Trade-offs

- **Risco**: Query parameter `?q=` pode ser manipulado pelo usuário → Mitigação: validação robusta (ID deve existir no JSON, deve ser número)
- **Risco**: QR code aponta para URL localhost em desenvolvimento → Mitigação: usar `st.get_option("server.address")` ou variável de ambiente `APP_URL`
- **Trade-off**: Remover navegação sequencial significa que o app perde a funcionalidade de "quiz completo" — mas isso está no escopo da proposta
