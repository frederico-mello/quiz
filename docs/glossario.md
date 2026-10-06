# Glossário

Todo termo técnico que aparece nesta documentação, em ordem alfabética, com a tradução para o dia a dia e onde ele é usado na explicação.

| Termo | Tradução | Onde aparece |
| --- | --- | --- |
| **`.env`** | Arquivo de texto com os segredos e endereços do projeto. Fica fora do git, e existe um `.env.example` de modelo. Analogia: a ficha de senhas que não sai da gaveta. | `04-dados.md` |
| **Ambiente virtual (venv)** | Uma cópia isolada das bibliotecas instaladas, para um projeto não bagunçar o outro. Analogia: caixa de ferramentas própria da obra. | `01-visao-geral.md`, README da raiz |
| **Arquivo `.md`** | Texto com marcação simples (Markdown), lido por qualquer navegador ou editor. É o formato desta documentação e das specs. | toda esta documentação |
| **Archive** | O fim de uma mudança: as tarefas foram concluídas, o delta foi sincronizado na spec principal e a pasta da change vira histórico datado. | `06-metodologia.md` |
| **Avatar** | O mascote desenhado, no caso o professor cientista que anima enquanto o áudio toca. | `05-componentes.md` |
| **API** | Um ponto de encontro padronizado: um programa oferece um balcão e outro programa fala com ele. | `07-pesquisa-e-fontes.md` |
| **Base64** | Jeito de embutir um arquivo (como um som) dentro de um texto, usando só letras e números. Por isso o áudio viaja junto na página. | `03-fluxo-principal.md`, `04-dados.md` |
| **Branch** | Uma linha de desenvolvimento paralela dentro do git. A principal aqui chama `main`. | `06-metodologia.md` |
| **Cache** | Guardar um resultado pronto para não calcular de novo. No avatar, os GIFs ficam salvos em `assets/` e são reaproveitados. | `03-fluxo-principal.md`, `05-componentes.md` |
| **Change** | Uma unidade de trabalho do OpenSpec: uma pasta em `openspec/changes/` com proposal, design, tasks e delta. Analogia: a ficha da obra que está começando. | `06-metodologia.md` |
| **Chave virtual** | Conta local criada pelo proxy LiteLLM com seu próprio orçamento. A chave não abre o modelo, abre a conta de quem está falando com o proxy. | `02-arquitetura.md`, `07-pesquisa-e-fontes.md` |
| **CI (integração contínua)** | Robô que recebe cada envio de código, monta um ambiente limpo e roda os testes. Aqui, um workflow do GitHub Actions. | `06-metodologia.md` |
| **Commit** | Uma "fotografia" do código salva no histórico do git, com uma mensagem. | `06-metodologia.md` |
| **Commit convencional** | Mensagem de commit no formato `tipo: o que mudou`, como `fix:` (correção), `chore:` (ajuste de rotina), `ci:` (automação), `docs:` (documentação), `test:` (teste). | `06-metodologia.md` |
| **Delta** | Dentro de uma change, o trecho que diz o que muda na spec: o que foi adicionado, alterado ou removido. Analogia: o adendo à planta, não a planta inteira. | `06-metodologia.md` |
| **Dependabot** | Serviço do GitHub que avisa e propõe atualização das bibliotecas e ações usadas. | `06-metodologia.md` |
| **`fail-open`** | Política de "em caso de dúvida, deixar passar": se a segunda opinião de moderação não responde, o texto segue, porque a checagem local já rodou. | `02-arquitetura.md`, `03-fluxo-principal.md` |
| **Fallback (reserva)** | Plano B: quando o provedor principal falha, outro assume automaticamente. No quiz, o OpenRouter entra no lugar do proxy LiteLLM. | `02-arquitetura.md` |
| **Git / GitHub** | Git é o sistema que guarda o histórico do código na máquina; GitHub é o site onde esse histórico fica publicado e onde o robô de testes roda. | `06-metodologia.md` |
| **GIF** | Formato de imagem animada, o que o avatar do professor usa para "falar". | `05-componentes.md` |
| **HTML** | A linguagem de marcação das páginas web. O prompt do professor proíbe o modelo de devolver HTML, para o texto sair limpo na tela e no áudio. | `03-fluxo-principal.md` |
| **JSON** | Formato de arquivo de texto organizado em listas e campos legíveis, usado em `questions.json`. | `01-visao-geral.md`, `04-dados.md` |
| **LangChain** | Biblioteca Python para montar conversas com modelos de linguagem (o objeto de prompt e o cliente de modelo `ChatOpenAI` vêm dela). | `02-arquitetura.md`, `05-componentes.md`, `07-pesquisa-e-fontes.md` |
| **Limite de taxa (rate limit)** | Quanto uma conta pode pedir por minuto ou por dia. O proxy LiteLLM aplica esse controle. | `07-pesquisa-e-fontes.md` |
| **LLM** | Modelo de linguagem, o programa que gera texto a partir de instruções. É quem faz o papel de professor. | `01-visao-geral.md` |
| **Merge** | Juntar uma linha de desenvolvimento na principal, depois de revisada. Os `Merge pull request` do histórico são isso. | `06-metodologia.md` |
| **Mock (dublê)** | Falso serviço usado nos testes: responde o que o teste espera, sem chamar a rede. Por isso os testes rodam em menos de um segundo. | `05-componentes.md`, `06-metodologia.md` |
| **Moderação semântica** | Segunda checagem de conteúdo feita por um modelo de IA, que entende o sentido do texto e não só a lista de palavras. | `02-arquitetura.md` |
| **OpenRouter** | Provedor de modelos na nuvem, usado aqui como reserva. | `02-arquitetura.md` |
| **OpenSpec** | Metodologia de trabalho em que se escreve primeiro como o sistema deve se comportar e só depois o código. Suas peças ficam em `openspec/`. | `06-metodologia.md` |
| **Prompt** | O texto de instruções enviado ao modelo. No quiz, ele define o tom (professor entusiasmado), o limite (500 caracteres) e as proibições (sem markdown). | `03-fluxo-principal.md`, `05-componentes.md` |
| **Proxy** | Programa intermediário que recebe um pedido em um padrão só e o repassa no formato que o destino entende. O LiteLLM é o tradutor entre o quiz e o modelo. | `02-arquitetura.md` |
| **pytest** | A ferramenta que roda os testes automatizados do projeto. | `06-metodologia.md` |
| **QR Code** | Aquele quadradinho de pontos que a câmera do celular lê e abre o link. Cada pergunta tem o seu. | `01-visao-geral.md` |
| **Requisito e cenário** | Unidades da spec: o requisito diz o que o sistema deve fazer ("o README só pode linkar o que existe"), e o cenário dá um exemplo concreto com começo, meio e fim. | `06-metodologia.md` |
| **`st.rerun()`** | Comando que refaz a tela dentro do próprio Streamlit, sem recarregar a página no navegador. | `03-fluxo-principal.md`, `04-dados.md` |
| **`st.session_state`** | A memória temporária de cada visita, que guarda o que precisa sobreviver aos recarregamentos da tela. | `03-fluxo-principal.md`, `04-dados.md` |
| **SHA (código de versão)** | Impressão digital de um arquivo ou de uma versão de ferramenta. Fixar por SHA significa travar exatamente aquela versão, para mudança lá fora não afetar aqui. | `06-metodologia.md` |
| **Spec (especificação)** | Documento que descreve como o sistema se comporta hoje, em requisitos e cenários. A "planta da obra" que fica em `openspec/specs/`. | `06-metodologia.md` |
| **Streamlit** | Biblioteca Python que transforma código em página web interativa, sem escrever HTML. É o que dá a tela do quiz. | `01-visao-geral.md` |
| **Teste automatizado** | Programa que confere se uma parte do código continua fazendo o que deve. Roda sozinho, sem pessoa, e aqui também no CI. | `06-metodologia.md` |
| **TTS (texto para fala)** | Converter texto escrito em voz falada. O quiz usa o serviço online do Edge, com voz `pt-BR-FranciscaNeural`. | `03-fluxo-principal.md` |
| **Workflow (GitHub Actions)** | O roteiro de automação que o GitHub executa: instalar, testar, revisar. Fica em `.github/workflows/`. | `06-metodologia.md` |
