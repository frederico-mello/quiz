# Quiz do Professor

Quiz educacional interativo em português brasileiro, desenvolvido com Streamlit. A aplicação apresenta perguntas abertas sobre instrumentos odontológicos históricos, avalia respostas com um LLM via OpenRouter, gera feedback em áudio e permite compartilhar perguntas por link ou QR Code.

## Recursos

- Perguntas abertas carregadas de `questions.json`.
- Avaliação de respostas com LangChain e OpenRouter.
- Moderação local e semântica, configurável por ambiente.
- Feedback em áudio com `edge-tts`.
- Avatar de professor cientista em GIF.
- Links e QR Codes para acesso direto a perguntas.

## Requisitos

- Python 3.10 ou superior.
- Chave de API do [OpenRouter](https://openrouter.ai/).
- Acesso à internet para avaliação por LLM e geração de áudio.

## Instalação

```bash
git clone <url-do-repositorio>
cd quiz
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto e informe, no mínimo, sua chave do OpenRouter:

```dotenv
OPENROUTER_API_KEY=sua-chave-aqui
```

Variáveis disponíveis:

| Variável | Obrigatória | Padrão | Uso |
| --- | --- | --- | --- |
| `OPENROUTER_API_KEY` | Sim | - | Chave de acesso ao OpenRouter. |
| `OPENROUTER_BASE_URL` | Não | `https://openrouter.ai/api/v1` | URL base da API. |
| `LLM_MODEL` | Não | `deepseek/deepseek-v4-flash` | Modelo usado na avaliação. |
| `MODERATION_ENABLED` | Não | `true` | Ativa a moderação de conteúdo quando `true`. |
| `APP_URL` | Não | `http://localhost:8501` | URL base usada nos links compartilháveis e QR Codes das perguntas. |
| `TTS_VOICE` | Não | `pt-BR-FranciscaNeural` | Voz usada pelo `edge-tts`. |
| `TEMP_AUDIO_DIR` | Não | `tmp/audio` | Diretório temporário dos arquivos de áudio. |

Ao publicar a aplicação em outro endereço, defina `APP_URL` com a URL acessível pelos usuários. O valor padrão `http://localhost:8501` é adequado apenas para execução local.

## Execução

Com o ambiente virtual ativo e `.env` configurado:

```bash
streamlit run app.py
```

Acesse <http://localhost:8501> no navegador. `app.py` é o entry point da aplicação.

## Estrutura principal

```text
app.py              # Entry point Streamlit e orquestração da aplicação
questions.json      # Banco de perguntas
requirements.txt    # Dependências de execução
src/
  avatar.py         # Avatar do professor
  config.py         # Configuração via variáveis de ambiente
  content_filter.py # Moderação de conteúdo
  llm_service.py    # Avaliação das respostas
  qrcode_service.py # Geração de QR Codes
  quiz_data.py      # Leitura das perguntas
  tts_service.py    # Geração de áudio
assets/             # GIFs do avatar
tests/              # Testes automatizados
openwiki/           # Documentação detalhada do projeto
```

## Documentação adicional

- [Quickstart](openwiki/quickstart.md): visão técnica e mapa inicial.
- [Arquitetura](openwiki/architecture.md): componentes e fluxo de dados.
- [Workflows](openwiki/workflows.md): fluxos do quiz e da moderação.
- [Operações](openwiki/operations.md): configuração e operação detalhadas.
- [Testes](openwiki/testing.md): orientação e limitações conhecidas.
- [Mapa de fontes](openwiki/source-map.md): referência dos arquivos e símbolos.
- [Integrações](openwiki/integrations.md): serviços externos e ferramentas.

## Licença

Este projeto ainda não define uma licença de distribuição.
