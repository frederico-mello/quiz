# Documentação do Quiz do Professor

**Em uma frase:** o quiz é um professor particular em forma de página web. O aluno escolhe uma pergunta sobre instrumentos odontológicos antigos, escreve a resposta com as próprias palavras, e um modelo de inteligência artificial faz o papel do professor: diz se acertou, explica o assunto e ainda fala a explicação em voz alta.

## Índice

| Página | O que você encontra |
| --- | --- |
| [01-visao-geral.md](01-visao-geral.md) | O problema que o programa resolve, para quem, e a viagem de um clique |
| [02-arquitetura.md](02-arquitetura.md) | As peças do sistema e como elas se conversam (diagrama) |
| [03-fluxo-principal.md](03-fluxo-principal.md) | O que acontece do clique do aluno até o áudio (diagrama) |
| [04-dados.md](04-dados.md) | Onde as informações ficam guardadas e como se ligam (diagrama) |
| [05-componentes.md](05-componentes.md) | Os módulos do código e a função de cada um (diagrama) |
| [06-metodologia.md](06-metodologia.md) | **A metodologia de desenvolvimento**: especificação antes do código, testes, revisão automatizada (diagrama) |
| [07-pesquisa-e-fontes.md](07-pesquisa-e-fontes.md) | O que foi checado fora do repositório, com fontes, e o que isso mudou na leitura |
| [glossario.md](glossario.md) | Todo termo técnico desta documentação traduzido para o dia a dia |

Caminho sugerido: comece pela [visão geral](01-visao-geral.md), siga para [arquitetura](02-arquitetura.md) e [fluxo principal](03-fluxo-principal.md), desça para [dados](04-dados.md) e [componentes](05-componentes.md), e deixe [metodologia](06-metodologia.md) e [pesquisa e fontes](07-pesquisa-e-fontes.md) para o fim: elas falam de como o projeto é construído, não de como ele roda.

## De onde vem esta documentação

Este texto foi escrito a partir de uma leitura do código real do repositório, não de uma descrição de terceiros. O estado lido é o `main` na revisão `2a1e7db` (3 de outubro de 2026), e a própria documentação é atualizada pelo mesmo ciclo de trabalho descrito em [06-metodologia.md](06-metodologia.md).

O que esta documentação **não** é:

- Não é manual de operação nem guia de instalação — para rodar o projeto, siga o [README da raiz](../README.md).
- Não é material de apresentação pontual: é documentação permanente, feita para envelhecer junto com o código.
- Não inventa comportamento: tudo o que ela afirma sobre o programa vem do código, e o que não vem está marcado.

## Premissas

- *(premissa)* Profundidade **curiosa**: narrativa em português simples, analogias, jargão explicado no mesmo parágrafo.
- *(premissa)* Prioridade declarada pelo dono do repositório: **a metodologia de desenvolvimento**, tratada por isso com uma página inteira em [06-metodologia.md](06-metodologia.md).
- *(premissa)* A referência de estado é o `main` do repositório, por ser o que existe publicamente.

## Como separar fato de interpretação

Nem tudo o que se lê em um código é fato. Quando uma conclusão não é demonstrada diretamente pelo código nem por uma fonte identificada, a afirmação aparece marcada com a etiqueta de inferência entre parênteses, logo ao lado do texto — e cada página que contém esse tipo de afirmação lista todas elas ao final, em "Inferências desta página". Assim dá para distinguir o que o programa **faz** do que alguém **interpretou** que ele quis dizer.

Os diagramas são feitos em Mermaid e renderizam nativamente no GitHub. Em visualizadores que não suportam Mermaid, o texto ao redor continua explicando o mesmo caminho: nenhum trecho depende só do diagrama.

## Inferências desta página

Nenhuma: esta página é índice e convenção de leitura. As inferências de cada assunto estão listadas ao final da página correspondente.
