# 07. Pesquisa e fontes: o que foi checado fora do repositório

Toda explicação desta documentação foi feita lendo o código real. Mas parte das decisões do projeto só se entende olhando para fora: o que é essa ferramenta, por que ela foi montada assim, o que ela promete. Esta página registra essa checagem, com endereço, data e o que cada fonte mudou na leitura.

**Ferramenta:** `parallel-cli 0.9.3` (busca paralela da Parallel), modo `fast`, executada em **5 de outubro de 2026**. Os identificadores de busca ficam registrados para reprodutibilidade: `search_0556cdbf3927545f2c76be00e3230400` (OpenSpec), `search_fe0fad200292f0a5001ef32f21f21016` (Streamlit), `search_315efdea208cad400b3e1d02fd094437` (LiteLLM e fallback), mais duas buscas sobre `edge-tts` e sobre o propósito do OpenSpec.

## 1. OpenSpec: o que a documentação oficial diz

Fontes consultadas:

- [`docs/overview.md` — "Core Concepts at a Glance"](https://github.com/Fission-AI/OpenSpec/blob/main/docs/overview.md) (arquivo de documentação do próprio projeto, texto integral extraído)
- [Quickstart — o ciclo passo a passo](https://openspec.dev/docs/quickstart)
- [Repositório do projeto](https://github.com/Fission-AI/OpenSpec)
- [Implementação em Go, mesma ideia](https://pkg.go.dev/github.com/santif/openspec-go)

> Nota de verificação: as duas primeiras entradas desta lista já apareceram aqui como `openspec.dev/docs/overview` e `openspec.dev/docs/the-workflow`, URLs que hoje devolvem HTTP 404. Elas foram trocadas pelas fontes primárias acima e a atribuição abaixo foi refeita nelas.

O que a fonte afirma: a spec é apresentada como "a única resposta acordada" sobre o que o software faz, e cinco ideias organizam tudo: (1) **specs são a verdade**, descrevem como o sistema é agora, em `openspec/specs/`; (2) **uma change é uma unidade de trabalho**, uma pasta só em `openspec/changes/`; (3) o **delta** descreve só o que muda, não a spec inteira; (4) os documentos se encadeiam `proposal → specs → design → tasks → implement` (por quê, o que, como, passos, faça); (5) **arquivar dobra a mudança de volta na verdade**: o delta vira parte da spec principal e a pasta vai para `changes/archive/` com data. O quickstart confirma o ciclo de cinco passos e a regra de o arquivo mudar de pasta só depois que as caixinhas de `tasks.md` estão marcadas.

**O que isso mudou na leitura:** confirma que a interpretação dada em [06-metodologia.md](06-metodologia.md) está correta, em especial que `openspec/specs/` é estado presente e `openspec/changes/` é trabalho em andamento. Também explica por que o `config.yaml` do repositório tem uma regra dura sobre sincronizar o delta antes de arquivar: é exatamente o passo que impede a spec principal de virar mentira. E esclarece um ponto que seria lido errado sem a fonte: os documentos de uma change não são burocracia sequencial obrigatória (a fonte chama de "enablers, not gates", ou seja, habilitadores, não barreiras).

## 2. LiteLLM: o que aquele proxy faz por trás

Fontes consultadas:

- [Life of a Request](https://docs.litellm.ai/docs/router_architecture) (arquitetura do roteador, texto integral extraído)
- [Roteamento e balanceamento](https://docs.litellm.ai/docs/routing)
- [Reservas no OpenRouter](https://openrouter.ai/docs/guides/routing/model-fallbacks)

O que a fonte afirma: o LiteLLM proxy (a porta padrão é a 4000) faz, nesta ordem, checagem de chave virtual e orçamento, limite de taxa, roteamento com balanceamento, reservas e repetições, e por fim **traduz o pedido para o formato do fornecedor** mantendo entrada e saída no formato OpenAI. A documentação distingue duas coisas: **repetição** (*retry*) fica dentro do mesmo grupo de modelos que falhou; **reserva** (*fallback*) sai para o grupo seguinte.

**O que isso mudou na leitura:** duas correções e uma confirmação.

- *Correção:* o nome `LITELLM_API_KEY` soaria como "senha do servidor". A fonte mostra que o nome correto é **chave virtual**: o proxy tem seu próprio sistema de contas e orçamento, então a chave não abre o modelo, abre a conta local.
- *Correção:* há um mecanismo de reserva pronto dentro do LiteLLM, e outro no próprio OpenRouter. O que o código do quiz mostra é a reserva escrita à mão em `evaluate_answer()`, com `try/except`. Se os mecanismos externos também estão ativos depende da configuração do proxy e do OpenRouter, que fica fora do repositório e não foi inspecionada — a mesma lacuna registrada na seção 6. *(inferência)* A razão prática de ter escrito a reserva no código é cobrir também o caso de o proxy estar fora do ar, algo que só a aplicação enxerga.
- *Confirmação:* o endereço `http://localhost:4000` do `.env.example` bate com a porta padrão da ferramenta, e o formato de chave virtual explica por que a aplicação pode falar com o proxy usando a biblioteca de cliente OpenAI (`ChatOpenAI`, da LangChain) sem que o provedor real seja a OpenAI.

## 3. Streamlit: por que a tela é remontada o tempo todo

Fontes consultadas:

- [Arquitetura: modelo de execução](https://docs.streamlit.io/develop/concepts/architecture)
- [Caching](https://docs.streamlit.io/develop/concepts/architecture/caching) (cache e memória)
- [Session state](https://docs.streamlit.io/develop/concepts/architecture/session-state) (estado de sessão)
- [Forms: interação do usuário](https://docs.streamlit.io/develop/concepts/architecture/forms) (quando um campo publica o valor)

O que a fonte afirma: o Streamlit **executa o script do começo ao fim a cada interação do usuário ou mudança de código**. Isso resolve o desenvolvimento rápido e cria dois problemas, atacados por ferramentas próprias da biblioteca: `st.cache_data` guarda o resultado de cálculos caros, e `st.session_state` guarda o que precisa sobreviver aos recarregamentos, valendo só para aquela sessão. O quiz usa apenas a segunda. A fonte sobre formulários acrescenta o ponto que derrubava a leitura antiga desta página: um campo de texto não publica valor a cada tecla — ele envia a alteração quando o campo perde o foco ou quando o usuário aperta Enter.

**O que isso mudou na leitura:** é a explicação que faltava para dois trechos do `app.py` que parecem burocracia. O bloco `if "questions" not in st.session_state` existe porque, sem ele, o arquivo `questions.json` seria relido a cada nova execução do script — que acontece por clique de botão, por Enter ou por saída do campo, não por tecla. E o `st.rerun()` no fim do envio é a forma de trocar de tela **dentro** desse modelo de remontagem, em vez de tentar atualizar só um pedaço. Sem essa fonte, essas linhas seriam descritas como "controle de fluxo"; na verdade são adaptações obrigatórias ao modelo de execução da ferramenta.

## 4. edge-tts: de onde vem a voz

Fontes consultadas:

- [`rany2/edge-tts`](https://github.com/rany2/edge-tts) (biblioteca usada pelo projeto, `edge-tts>=6.1.0` no `requirements.txt`)
- [`tianqingyu/ms-edge-tts`](https://github.com/tianqingyu/ms-edge-tts) (implementação irmã, com o código de comunicação)

O que a fonte afirma: a biblioteca usa o serviço online de texto para fala do Microsoft Edge **sem precisar do Edge, sem Windows e sem chave de API**, e permite escolher vozes como `pt-BR-FranciscaNeural`.

**O que isso mudou na leitura:** responde duas perguntas do `.env.example`. Primeiro, por que não existe nenhuma variável de voz ou credencial de áudio: não há chave a guardar. Segundo, por que o README insiste em "acesso à internet" mesmo para um app cujo modelo pode estar atrás de um proxy local: a voz não vem da máquina do professor. *(inferência)* É também o motivo de `TTS_VOICE` ter padrão e de o texto passar pela limpeza em `clean_text_for_tts()`, porque serviço de voz é sensível a formatação.

## 5. repository-hygiene: por que a auditoria semanal não alertou

Fontes consultadas:

- [repository-hygiene 0.2.0](https://pypi.org/project/repository-hygiene/0.2.0/) (a versão fixada no workflow até esta correção)
- [repository-hygiene 1.0.0](https://pypi.org/project/repository-hygiene/1.0.0/) (linha 1.x, indicada para o repin; o pino foi aplicado em 1.1.0 nesta correção)

O que a fonte afirma: a versão 0.2.0 lê o bloco `regras:` (em português) e a versão 1.0.0 lê `rules:` (em inglês).

**O que isso mudou na leitura:** o diagnóstico de [06-metodologia.md](06-metodologia.md) deixa de ser hipótese e passa a ser causa verificada comparando a configuração do repositório com o código do pacote — o workflow fixava a 0.2.0, que procura `regras:`, enquanto o `auditoria.yaml` usa `rules:` desde 26 de julho de 2026, e a 1.0.0 confirma o diagnóstico lendo justamente a chave que o arquivo tem. Sem regra alguma carregada, a auditoria termina com sucesso sem examinar um único arquivo; o repin foi aplicado nesta correção, com o pino subido para 1.1.0, devolvendo a auditoria ao funcionamento.

## 6. O que não foi possível checar

| Item | Situação |
| --- | --- |
| Configuração real do proxy LiteLLM | Fica fora do repositório, em um arquivo `config.yaml` do proxy; a localização da máquina não foi verificada. Só foi visto o `.env.example` do lado do cliente. |
| Endereço `lappquiz.ict.unesp.br` em produção | O endereço respondeu HTTP 200 com a página do Streamlit; o conteúdo exibido não foi inspecionado em navegador. A URL vem do código (`APP_URL`). |
| Pasta `openwiki/` antes da remoção | O conteúdo antigo não foi recuperado. Sei que existia pelo histórico do git e pelas referências que o README ainda fazia. |
| Perfil real dos alunos | Não há dados de uso no repositório. A leitura de sala de aula é inferência. |
| Arquivos locais da cópia de trabalho | `.env` e `.venv/` existem só na máquina de quem roda o projeto e são ignorados pelo git, então não fazem parte do repositório documentado aqui. Já o `AGENTS.md`/`CLAUDE.md` mencionados em versões anteriores desta leitura não existem na base `2a1e7db` — foram removidos no mesmo commit que apagou o OpenWiki. |
| Scaffolding de agentes versionado | `.github/skills/`, `.github/prompts/` e `.opencode/` guardam dezenas de arquivos `.md` **rastreados** pelo git: são instruções para agentes, mas fazem parte do repositório e ficam fora do escopo desta documentação. |

Nenhuma destas lacunas afeta a descrição do funcionamento do programa; elas limitam afirmações sobre **onde** ele roda e **quem** usa.

## Inferências desta página

1. *(inferência)* A reserva escrita à mão em `evaluate_answer()` existe porque precisa cobrir também o caso de o proxy LiteLLM estar fora do ar, cenário que só o código da aplicação enxerga. Base: a documentação do LiteLLM e do OpenRouter descrevem reservas prontas, o código do quiz não aciona nenhuma delas de forma visível e a configuração externa não foi inspecionada.
2. *(inferência)* `TTS_VOICE` tem valor padrão e o texto passa por `clean_text_for_tts()` porque o serviço de voz é sensível a formatação. Base: a fonte do `edge-tts` mostra serviço sem chave e o código aplica a limpeza logo antes de enviar o texto.
