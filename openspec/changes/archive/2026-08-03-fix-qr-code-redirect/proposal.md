## Why

Os QR codes atualmente podem apontar para um endereço `localhost:porta`, que não é acessível pelos participantes fora do ambiente local. Eles precisam abrir a aplicação pelo endereço público `https://lappquiz.ict.unesp.br`.

## What Changes

- Alterar o destino padrão dos links codificados nos QR codes para `https://lappquiz.ict.unesp.br`.
- Preservar o identificador da pergunta no parâmetro `?q=<id>` do link compartilhado.
- Manter a possibilidade de substituir a URL base por uma configuração `APP_URL` quando necessário.

## Capabilities

### New Capabilities

- Nenhuma.

### Modified Capabilities

- `question-link-qr-code`: alterar a URL base padrão usada nos QR codes para o endereço público da aplicação, mantendo links específicos por pergunta e URL configurável.

## Impact

- Geração e conteúdo dos QR codes exibidos para perguntas.
- Requisito existente de URL base da capacidade `question-link-qr-code`.
- Acesso externo dos participantes ao endereço público da aplicação; não há mudança prevista no fluxo de perguntas, respostas ou estado de sessão.
