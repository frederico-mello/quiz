## Why

O quiz atualmente força todos os participantes a seguir uma sequência única de perguntas, o que impede distribuir desafios específicos e acessar uma pergunta diretamente. O resultado desejado é que cada pergunta funcione como uma experiência independente, com resposta e feedback associados à sessão do participante.

## What Changes

- Adicionar acesso direto a uma pergunta específica por seu identificador estável em um link compartilhável.
- Fazer com que a tela carregue e processe somente a pergunta indicada no link, sem exigir perguntas anteriores ou permitir navegação para outras perguntas.
- Manter resposta, feedback individual gerado por IA e áudio disponíveis apenas durante a sessão atual do participante.
- Disponibilizar um QR code para o link da pergunta exibida, permitindo sua distribuição física ou digital.
- Remover o fluxo sequencial, o embaralhamento e as estatísticas dependentes da progressão por várias perguntas.
- Exibir tratamento amigável para links sem pergunta, IDs inválidos ou perguntas inexistentes.
- Corrigir a falha de inicialização causada pelo cálculo de pontuação sem perguntas respondidas e garantir que a abertura de uma pergunta não produza erro.
- Fora do escopo: autenticação, persistência de respostas entre sessões, edição do catálogo de perguntas e alteração do modelo de avaliação por IA.

## Capabilities

### New Capabilities

- `independent-question-access`: Acessar, responder e revisar uma única pergunta por link estável, sem depender de uma sequência de quiz.
- `question-link-qr-code`: Gerar e exibir um QR code correspondente ao link da pergunta atualmente aberta.

### Modified Capabilities

- Nenhuma. Não existem especificações de capacidades existentes neste projeto.

## Impact

- A experiência principal do quiz e seu estado de sessão serão reorganizados para representar uma pergunta independente, em vez de uma posição em uma sequência.
- O catálogo de perguntas continuará sendo a fonte dos identificadores estáveis usados pelos links.
- A navegação e os controles da interface serão reduzidos ao ciclo responder, receber feedback e tentar novamente para a pergunta atual.
- Será necessário incluir suporte de geração de QR code como dependência da aplicação.
- Links e QR codes devem apontar para o endereço da aplicação que os participantes conseguem acessar.
- O processamento de avaliação por IA, moderação e síntese de áudio continuará sendo usado individualmente para cada pergunta.
