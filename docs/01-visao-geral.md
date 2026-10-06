# 01. Visão geral: o que é o quiz

## O problema que ele resolve

Ensinar a história da odontologia com perguntas de múltipla escolha é fácil, mas não mostra se o aluno entendeu. A pergunta aberta ("o que era isso e para que servia?") mostra, e é justamente aí que dá trabalho corrigir: cada aluno escreve diferente, e alguém precisa ler, julgar e explicar, de novo e de novo.

O quiz resolve isso assim: o aluno escreve a resposta com as próprias palavras, e um modelo de inteligência artificial (um programa que gera texto a partir de instruções, aqui chamado de **LLM**) assume o papel do professor. Ele compara o que o aluno escreveu com a resposta certa, diz se acertou, explica o assunto, e essa explicação ainda é falada em voz alta por um avatar de cientista.

Analogia do dia a dia: é um explicador particular colado na parede da sala. O aluno pergunta, ele responde na hora, sempre com a mesma paciência, e cobra respeito se a conversa sair do lugar.

## Para quem é

Para quem acessa pelo celular ou pelo computador, normalmente por um link curto ou um QR Code (aquele quadradinho de pontos que a câmera do celular lê). O endereço público padrão está no código: `https://lappquiz.ict.unesp.br`.

Que esse link chegue impresso no quadro ou projetado na tela, com a página aberta durante a aula, é leitura de sala de aula e não fato do código: o repositório não guarda dados de uso. *(inferência)* Está registrada como inferência 1, no fim desta página.

## O banco de perguntas

As perguntas moram em um arquivo só, `questions.json`, na raiz do repositório. Ele é uma lista de objetos com três campos: `id`, `question` (o enunciado) e `correct_answer` (a resposta certa). Neste estado do código há **5 perguntas**, todas sobre instrumentos odontológicos históricos. Exemplo real do arquivo:

```json
{
  "id": 1,
  "question": "Eu sou um instrumento ancestral. No passado, não precisava de eletricidade, apenas da força manual ou de cordas para girar. Eu funcionava com os pés do dentista. Meu nome é:",
  "correct_answer": "Trépano"
}
```

Adicionar uma pergunta é editar esse arquivo de texto. Não existe formulário administrativo nem banco de dados.

## A viagem de um clique, em 6 passos

1. O aluno abre o link `https://lappquiz.ict.unesp.br/?q=2`. O trecho `?q=2` diz qual pergunta ele quer.
2. O programa lê `questions.json`, localiza a pergunta de número 2 e mostra o enunciado dentro de uma caixa colorida, com o botão de responder embaixo.
3. Ele digita a resposta e clica em **Enviar Resposta**.
4. Antes de chamar o professor, o texto passa por um filtro de conteúdo (ver [02-arquitetura.md](02-arquitetura.md)): checagem de palavras na própria máquina, depois uma checagem por inteligência artificial. Na primeira e na segunda falha o aluno recebe advertência; na terceira a sessão dele é bloqueada.
5. O texto aprovado vai para o LLM, que devolve um comentário curto em português, sem marcação, dizendo se acertou e explicando o instrumento. Se o provedor principal falhar, entra automaticamente o provedor de reserva.
6. O comentário é convertido em áudio, o avatar do professor passa a "falar" enquanto o áudio toca, e a tela mostra o link e o QR Code daquela pergunta para ele compartilhar.

## O que o programa **não** faz

Isso evita sustos na leitura:

- **Não guarda histórico.** Não há banco de dados, login, nota, ranking nem progresso. Cada visita começa do zero e a resposta some quando a aba fecha. Isso é leitura direta do código: o único arquivo de dados lido é `questions.json`, e o que existe em memória vive na sessão do navegador (explicado em [04-dados.md](04-dados.md)).
- **Não avalia automaticamente por regra exata.** Não existe comparação literal ("acertou se escreveu 'trépano'"). Quem julga é o LLM, então a mesma resposta pode levar a comentários ligeiramente diferentes de uma vez para outra.
- **Não é garantido que funcione offline.** O áudio sempre depende de um serviço de voz online; a avaliação depende do que estiver configurado no `.env` (endereço do LiteLLM, chave do OpenRouter) e essa configuração fica fora deste repositório (ver [02-arquitetura.md](02-arquitetura.md)).
- **Não tem licença de distribuição declarada.** O próprio README diz: "Este projeto ainda não define uma licença de distribuição."

## Peças nomeadas por analogia

| Peça do programa | Analogia | Onde fica no código |
| --- | --- | --- |
| Vitrine (telas) | O quadro onde a pergunta aparece | `app.py` |
| Portaria (entrada) | Quem decide qual pergunta abrir | `app.py` + `?q=` na URL |
| Cérebro (regras) | O professor que corrige | `src/llm_service.py` |
| Filtro da porta | O porteiro que barra nome impróprio | `src/content_filter.py` |
| Memória (guarda) | A gaveta com as perguntas | `questions.json` |
| Locutor (voz) | Quem lê a explicação em voz alta | `src/tts_service.py` |
| Cartaz (compartilho) | O QR Code da pergunta | `src/qrcode_service.py` |
| Mascote | O avatar do professor cientista | `src/avatar.py` |
| Chave do depósito | As senhas e endereços dos serviços | `src/config.py` + `.env` |

Caminhos reais, em letra miúda: `app.py` → `src/quiz_data.py` (lê o JSON) → `src/content_filter.py` (filtra) → `src/llm_service.py` (avalia) → `src/tts_service.py` (fala) → `src/qrcode_service.py` (compartilha).

## Como rodar (para curiosos)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env   # preencher as chaves
streamlit run app.py   # abre em http://localhost:8501
```

Sem o arquivo `.env` preenchido, o programa abre e avisa quais variáveis faltam: ele valida a configuração na largada, não em silêncio. Instruções completas, incluindo Windows, estão no [README da raiz](../README.md).

## Sustos antecipados

- **Arquivos que existem na sua cópia de trabalho, mas não no repositório.** `.env`, `.venv/`, `tmp/` e `__pycache__/` aparecem em quem já rodou o projeto localmente e são ignorados pelo git: baixar o repositório do GitHub não traz nenhum deles. O `.env.example` é o modelo que existe de verdade.
- **README que apontava para uma pasta morta.** A pasta `openwiki/` foi apagada no commit `2a1e7db` (3 de outubro de 2026), mas o README continuou listando `openwiki/` na estrutura e linkando as sete páginas dela. Corrigir isso — apagar as linhas mortas e apontar para `docs/` — é parte da change `documentacao-permanente`; o achado e o porquê, incluindo o cenário órfão da spec, estão em [06-metodologia.md](06-metodologia.md), seção "Onde o README estava fora do próprio spec".
- **Duas pastas de configuração de agente.** `.github/skills/`, `.github/prompts/` e `.opencode/` guardam cópias dos comandos OpenSpec para duas ferramentas diferentes. São utilitários de desenvolvimento versionados no repositório, não partes do quiz que o aluno vê.

## Inferências desta página

1. *(inferência)* Uso ao vivo em sala com QR Code projetado ou impresso. Base: link público + QR Code por pergunta + avatar falando; não há registro de uso no repositório.
2. *(inferência)* Público jovem, daí a moderação com duas advertências e depois o bloqueio da sessão. Base: a regra de bloqueio existe no código (`app.py`); o perfil do público é suposição sem registro no repositório.
3. *(inferência)* O pedido de no máximo 500 caracteres, escrito no prompt, existe por causa da leitura em voz alta (frase curta soa melhor falada). Base: o prompt manda "MANTENHA A RESPOSTA CURTA: no máximo 500 caracteres" e logo em seguida o mesmo texto vira áudio — o código, porém, não valida nem corta o texto nesse tamanho (ver [03-fluxo-principal.md](03-fluxo-principal.md)).
4. *(inferência)* A ausência de banco de dados é decisão de simplicidade, não limitação técnica. Base: o projeto já usa testes, CI e especificações, então manter tudo em um arquivo de texto parece escolha consciente.
