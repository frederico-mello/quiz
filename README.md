# Quiz do Professor

Quiz educacional interativo em português brasileiro, desenvolvido com Streamlit. O aluno responde perguntas abertas sobre instrumentos odontológicos históricos e recebe avaliação pedagógica gerada por LLM, feedback em áudio e animação de um professor cientista.

## Recursos

- Perguntas abertas carregadas de `questions.json`.
- Avaliação de respostas via OpenRouter e LangChain.
- Moderação local e semântica com sistema de advertências.
- Conversão do feedback em áudio usando `edge-tts`.
- Avatar GIF animado com sincronização entre fala e movimento.
- Interface responsiva com suporte a temas claro e escuro.

## Requisitos

- Python 3.10 ou superior
- Chave de API do [OpenRouter](https://openrouter.ai/)
- Conexão com a internet para avaliação LLM e geração de áudio

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
pip install -r requirements.txt
```

## Configuração

Copie `.env.example` para `.env` e informe sua chave:

```bash
cp .env.example .env
```

Variáveis disponíveis:

| Variável | Obrigatória | Padrão | Descrição |
| --- | --- | --- | --- |
| `OPENROUTER_API_KEY` | Sim | - | Chave de acesso ao OpenRouter |
| `OPENROUTER_BASE_URL` | Não | `https://openrouter.ai/api/v1` | URL base da API |
| `LLM_MODEL` | Não | `deepseek/deepseek-v4-flash` | Modelo usado na avaliação |
| `MODERATION_ENABLED` | Não | `true` | Ativa moderação de conteúdo |
| `TTS_VOICE` | Não | `pt-BR-FranciscaNeural` | Voz usada pelo `edge-tts` |
| `TEMP_AUDIO_DIR` | Não | `tmp/audio` | Diretório para arquivos temporários de áudio |

## Execução

```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

## Estrutura

```text
app.py              # Entrada Streamlit e orquestração da aplicação
questions.json      # Banco de perguntas
src/
  avatar.py         # Geração do avatar GIF
  config.py         # Configuração via variáveis de ambiente
  content_filter.py # Moderação de conteúdo
  llm_service.py    # Avaliação das respostas
  quiz_data.py      # Leitura e embaralhamento das perguntas
  tts_service.py    # Geração de áudio
assets/             # GIFs gerados e armazenados em cache
```

## Documentação adicional

- [Quickstart](openwiki/quickstart.md)
- [Arquitetura](openwiki/architecture/overview.md)
- [Fluxo do quiz](openwiki/workflows/quiz-flow.md)
- [Runbook operacional](openwiki/operations/runbook.md)

## Licença

Este projeto ainda não define uma licença de distribuição.
